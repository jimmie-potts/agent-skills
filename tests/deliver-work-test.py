#!/usr/bin/env python3
"""Structural contracts only; behavioral evaluation uses held-out scenarios."""
from pathlib import Path
import re
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'deliver-work'

RECORD_ROWS = ('Issue', 'Recommended', 'Coordinator model',
               'Coordinator level', 'Session type', 'Session label', 'Workers',
               'Reviewers', 'Agents', 'Consultations', 'Review rounds',
               'Findings', 'Finding causes', 'Corrections')
PROVENANCE = ('host-observed', 'user-stated', 'self-reported', 'unknown')
SESSION_TYPE = r'(?:One-shot|Pair|Orchestrate|Investigate first)'
COUNT = r'(?:\d+|at least \d+|unknown)'
TOKEN = r'[^\s|()+,;]+'
LABEL = r'[a-z0-9]+(?:-[a-z0-9]+)*'
KNOWN = rf'(?!unknown ){TOKEN} \((?:host-observed|user-stated|self-reported)\)'
SOURCED = rf'(?:unknown \(unknown\)|{KNOWN}(?: \+ {KNOWN})*)'
AGENT = (rf'{LABEL}: requested {TOKEN} at {TOKEN}, '
         rf'model {SOURCED}, level {SOURCED}')
RECORD_CELLS = {
    'Issue': r'[\w.-]+/[\w.-]+#\d+|[A-Z][A-Z0-9]*-\d+|https?://\S+',
    'Recommended': rf'{SESSION_TYPE}, {TOKEN}, {TOKEN}|insufficient|none',
    'Coordinator model': SOURCED,
    'Coordinator level': SOURCED,
    'Session type': SESSION_TYPE,
    'Session label': LABEL,
    'Workers': rf'none|{AGENT}(?:; {AGENT})*',
    'Reviewers': rf'none|{AGENT}(?:; {AGENT})*',
    'Agents': COUNT,
    'Consultations': rf'{COUNT}|not applicable',
    'Review rounds': rf'final {COUNT}; task {COUNT}',
    'Findings': rf'P0 {COUNT}; P1 {COUNT}; P2 {COUNT}; P3 {COUNT}',
    'Finding causes': (rf'edge-case {COUNT}; untested-bug {COUNT}; '
                       rf'wrong-approach {COUNT}; other {COUNT}'),
    'Corrections': COUNT,
}


def parse_execution_record(text):
    """Read an Execution record's shape strictly: rows, order and cell grammar.

    Cross-row consistency, such as Agents against listed contexts, is not checked.
    """
    match = re.fullmatch(
        r'## Execution record\n\n\| Field \| Value \|\n\| --- \| --- \|\n'
        r'((?:\|[^\n]*\|\n)+)'
        r'(?:\n\*\*Fixes delivery:\*\* ([\w.-]+/[\w.-]+(?:#\d+|@[0-9a-f]{7,40}))\n)?'
        r'\n\*\*Recorded:\*\* (\d{4}-\d{2}-\d{2}), '
        r'(agent-skills@[0-9a-f]{7,40}|unknown)\n?', text)
    if not match:
        raise ValueError('section outside the Execution record shape')
    rows = {}
    for line in match.group(1).splitlines():
        cells = re.fullmatch(r'\| ([^|]+?) \| ([^|]+?) \|', line)
        if not cells or cells.group(1) in rows:
            raise ValueError(f'bad or repeated row: {line}')
        field, value = cells.groups()
        if field not in RECORD_CELLS:
            raise ValueError(f'unknown row: {field}')
        if not re.fullmatch(RECORD_CELLS[field], value):
            raise ValueError(f'bad {field} value: {value}')
        rows[field] = value
    expected = [row for row in RECORD_ROWS
                if row != 'Session label' or row in rows]
    if list(rows) != expected:
        raise ValueError(f'rows out of order or missing: {list(rows)}')
    return {'rows': rows, 'fixes': match.group(2),
            'recorded': match.group(3), 'policy': match.group(4)}


class DeliverWorkStructureTest(unittest.TestCase):
    def test_single_portable_explicit_entrypoint(self):
        text = (SKILL / 'SKILL.md').read_text()
        match = re.fullmatch(r'---\n(.*?)\n---\n(.+)', text, re.DOTALL)
        self.assertIsNotNone(match)
        metadata = yaml.safe_load(match.group(1))
        self.assertEqual(set(metadata), {'name', 'description'})
        self.assertEqual(metadata['name'], SKILL.name)
        self.assertTrue(metadata['description'].strip())
        self.assertLessEqual(len(text.splitlines()), 500)
        adapter = yaml.safe_load((SKILL / 'agents' / 'openai.yaml').read_text())
        self.assertIs(adapter['policy']['allow_implicit_invocation'], False)
        self.assertIn('$deliver-work', adapter['interface']['default_prompt'])
        for retired in ('deliver-jira-work', 'github-delivery'):
            self.assertFalse((ROOT / 'skills' / retired).exists())

    def test_references_resolve_and_have_no_orphans(self):
        entry = SKILL / 'SKILL.md'
        pending, visited = [entry], set()
        while pending:
            path = pending.pop()
            if path in visited:
                continue
            visited.add(path)
            for link in re.findall(r'\]\(([^)]+)\)', path.read_text()):
                if '://' in link or link.startswith('#'):
                    continue
                target = (path.parent / link.split('#')[0]).resolve()
                self.assertTrue(target.is_relative_to(SKILL.resolve()), link)
                self.assertTrue(target.is_file(), link)
                if target.suffix == '.md':
                    pending.append(target)
        references = set((SKILL / 'references').glob('*.md'))
        self.assertTrue(references)
        self.assertTrue(references <= visited, references - visited)

    def test_instruction_only_package(self):
        for path in SKILL.rglob('*'):
            self.assertFalse(path.is_symlink(), str(path))
            if path.is_file():
                self.assertIn(path.suffix, {'.md', '.yaml'})
        self.assertFalse((SKILL / 'scripts').exists())

    def test_shared_resources_are_exposed_to_consumers(self):
        # Stable pointers expose shared contracts without copied definitions.
        links = re.findall(r'\]\(([^)]+)\)',
                           (SKILL / 'SKILL.md').read_text())
        for resource in ('references/work-assessment.md',
                         'references/resumption.md',
                         'references/pr-supervision.md',
                         'references/task-planning.md',
                         'references/review-cycles.md'):
            self.assertTrue((SKILL / resource).is_file())
            self.assertIn(resource, links)

    def test_selection_resources_are_routed(self):
        entry_links = re.findall(r'\]\(([^)]+)\)',
                                (SKILL / 'SKILL.md').read_text())
        self.assertIn('references/model-selection.md', entry_links)
        policy = SKILL / 'references/model-selection.md'
        adapter_links = re.findall(r'\]\(([^)]+)\)', policy.read_text())
        self.assertIn('codex-model-selection.md', adapter_links)

    def test_execution_record_examples_parse_strictly(self):
        reference = (SKILL / 'references/execution-reporting.md').read_text()
        documented = re.findall(r'^\| `([A-Z][a-z]+(?: [a-z]+)?)` \|',
                                reference, re.MULTILINE)
        self.assertEqual(tuple(documented[:len(RECORD_ROWS)]), RECORD_ROWS)
        for term in PROVENANCE:
            self.assertIn(f'| `{term}` |', reference)
        examples = re.findall(r'```markdown\n(.+?)```', reference, re.DOTALL)
        self.assertEqual(len(examples), 2)
        complete, partial = map(parse_execution_record, examples)
        self.assertEqual(list(complete['rows']), list(RECORD_ROWS))
        self.assertIsNotNone(complete['fixes'])
        self.assertNotEqual(complete['policy'], 'unknown')
        self.assertNotIn('Session label', partial['rows'])
        self.assertIsNone(partial['fixes'])
        self.assertEqual(partial['rows']['Coordinator level'], 'unknown (unknown)')
        self.assertIn('at least', partial['rows']['Agents'])
        self.assertIn('unknown', partial['rows']['Corrections'])
        used = ' '.join(complete['rows'].values()) + ' '.join(partial['rows'].values())
        for term in PROVENANCE:
            self.assertIn(f'({term})', used)

    def test_execution_record_parser_rejects_inferred_shapes(self):
        reference = (SKILL / 'references/execution-reporting.md').read_text()
        example = re.findall(r'```markdown\n(.+?)```', reference, re.DOTALL)[0]
        mutations = {
            'unlabelled model': ('gpt-6-astra (user-stated) + ', 'gpt-6-astra + '),
            'unknown vocabulary': ('(host-observed)', '(requested)'),
            'unknown with value': ('level unknown (unknown)', 'level medium (unknown)'),
            'bare unknown': ('level unknown (unknown)', 'level unknown'),
            'unknown mixed with a source': ('high (user-stated) + high (host-observed)',
                                            'unknown (unknown) + high (host-observed)'),
            'repeated unknown': ('high (user-stated) + high (host-observed)',
                                 'unknown (unknown) + unknown (unknown)'),
            'unknown value with a source': ('high (user-stated) + ', 'unknown (user-stated) + '),
            'display name with a space': ('gpt-6-astra (user-stated) + ',
                                          'GPT 6 Astra (user-stated) + '),
            'old requested shape': ('requested gpt-6-luna at medium', 'requested gpt-6-luna/medium'),
            'missing row': ('| Corrections | 1 |\n', ''),
            'row order': ('| Agents | 5 |\n| Consultations | not applicable |',
                          '| Consultations | not applicable |\n| Agents | 5 |'),
            'invented session type': ('| Session type | Orchestrate |',
                                      '| Session type | Solo |'),
            'raw session path': ('| Session label | example-app-42 |',
                                 '| Session label | /home/me/.codex/sessions/1 |'),
            'missing recorded line': ('\n**Recorded:** 2026-09-25, agent-skills@1a2b3c4\n', ''),
            'extra prose': ('| Corrections | 1 |\n', '| Corrections | 1 |\n\nNotes.\n'),
        }
        for name, (old, new) in mutations.items():
            with self.subTest(mutation=name):
                self.assertIn(old, example)
                with self.assertRaises(ValueError):
                    parse_execution_record(example.replace(old, new, 1))

    def test_execution_record_is_wired_into_delivery(self):
        entry = ' '.join((SKILL / 'SKILL.md').read_text().split())
        self.assertIn("Execution record's `Recommended` row", entry)
        self.assertIn('`## Execution record` section', entry)
        self.assertIn('in the final response without one', entry)
        links = re.findall(r'\]\(([^)]+)\)', entry)
        self.assertIn('references/execution-reporting.md', links)
        scenarios = (SKILL / 'references/validation-scenarios.md').read_text()
        self.assertIn('`**Fixes delivery:**`', scenarios)
        readme = (ROOT / 'README.md').read_text()
        self.assertIn('`## Execution record`', readme)
        for term in PROVENANCE:
            self.assertIn(f'`{term}`', readme)

    def test_canonical_check_wiring(self):
        command = 'python3 tests/deliver-work-test.py'
        for path in (ROOT / 'AGENTS.md', ROOT / 'README.md',
                     ROOT / '.github/workflows/validate.yml'):
            self.assertIn(command, path.read_text(), str(path))
            self.assertNotIn('python3 tests/deliver-jira-work-test.py', path.read_text())
        self.assertFalse((ROOT / 'tests/deliver-jira-work-test.py').exists())

    def test_documented_dependencies_are_installed_in_example(self):
        readme = (ROOT / 'README.md').read_text()
        command = next(line for line in readme.splitlines()
                       if line.startswith('./scripts/manage-skills.sh install --agent codex deliver-work '))
        for dependency in ('code-review', 'tdd', 'grilling', 'grill-with-docs',
                           'domain-modeling', 'openspec-propose',
                           'openspec-apply-change', 'openspec-archive-change'):
            self.assertIn(dependency, command.split())
            self.assertTrue((ROOT / 'skills' / dependency / 'SKILL.md').is_file())


if __name__ == '__main__':
    unittest.main()
