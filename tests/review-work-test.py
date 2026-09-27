#!/usr/bin/env python3
"""Structural and result-contract checks; behavior uses held-out scenarios."""
from pathlib import Path
import re
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'skills'
SKILL = SKILLS / 'review-work'
FIXTURES = ROOT / 'tests/fixtures/workflow-evaluation'

ROWS = ('Work', 'Round', 'Comparison', 'Requirements', 'Policy', 'Standards',
        'Specification', 'Reviewers', 'Open findings')
AXES = ('Standards', 'Specification')
STATUS = r'(?:satisfied|action-required|incomplete)'
TOKEN = r'[^\s|()+,;]+'
LABEL = r'[a-z0-9]+(?:-[a-z0-9]+)*'
KNOWN = rf'(?!unknown ){TOKEN} \((?:host-observed|user-stated|self-reported)\)'
SOURCED = rf'(?:unknown \(unknown\)|{KNOWN}(?: \+ {KNOWN})*)'
REVIEWER = (rf'({LABEL}): ([a-z]+), requested {TOKEN} at {TOKEN}, '
            rf'model {SOURCED}, level {SOURCED}')
CELLS = {
    'Work': r'[\w.-]+/[\w.-]+#\d+|[A-Z][A-Z0-9]*-\d+|https?://\S+|none',
    'Round': r'(?:final|task) [1-9]\d*',
    'Comparison': (r'base [0-9a-f]{40}; head [0-9a-f]{40}; merge-base [0-9a-f]{40}'
                   r'|patch sha256:[0-9a-f]{64}'),
    'Requirements': rf'{TOKEN} at {TOKEN}|none',
    'Policy': TOKEN,
    'Standards': STATUS,
    'Specification': STATUS,
    'Reviewers': rf'none|{REVIEWER}(?:; {REVIEWER})*',
    'Open findings': r'P0 \d+; P1 \d+; P2 \d+; P3 \d+',
}
FINDING = re.compile(
    r'- (F\d+) \((P[0-3]), ([a-z]+), '
    r'(unresolved|resolved|regression|accepted|deferred)\): .+; '
    r'first ((?:final|task) \d+), latest ((?:final|task) \d+)')
OPEN = ('unresolved', 'regression')


def parse_review_result(text):
    """Parse one Review result strictly and enforce its status rules."""
    match = re.fullmatch(
        r'## Review result\n\n\| Field \| Value \|\n\| --- \| --- \|\n'
        r'((?:\|[^\n]*\|\n)+)'
        r'\n\*\*Findings:\*\*\n((?:- [^\n]+\n)+|none\n)'
        r'\n\*\*Coverage:\*\* (\S[^\n]*)\n?', text)
    if not match:
        raise ValueError('section outside the Review result shape')
    rows = {}
    for line in match.group(1).splitlines():
        cells = re.fullmatch(r'\| ([^|]+?) \| ([^|]+?) \|', line)
        if not cells or cells.group(1) in rows or cells.group(1) not in CELLS:
            raise ValueError(f'bad, repeated or unknown row: {line}')
        field, value = cells.groups()
        if not re.fullmatch(CELLS[field], value):
            raise ValueError(f'bad {field} value: {value}')
        rows[field] = value
    if tuple(rows) != ROWS:
        raise ValueError(f'rows out of order or missing: {list(rows)}')

    reviewers = [] if rows['Reviewers'] == 'none' else [
        re.match(REVIEWER, entry).groups()
        for entry in rows['Reviewers'].split('; ')]
    labels = [label for label, _ in reviewers]
    if len(set(labels)) != len(labels):
        raise ValueError('repeated reviewer label')
    if any(label.startswith('coordinator') for label in labels):
        raise ValueError('the coordinator cannot fill an axis')
    reviewed = {axis for _, axis in reviewers}

    findings = []
    if match.group(2) != 'none\n':
        for line in match.group(2).splitlines():
            parsed = FINDING.fullmatch(line)
            if not parsed:
                raise ValueError(f'bad finding: {line}')
            findings.append(parsed.groups())
    ids = [finding[0] for finding in findings]
    if len(set(ids)) != len(ids):
        raise ValueError('repeated finding ID')
    kind, number = rows['Round'].split()
    for _, severity, _, state, _, latest in findings:
        if state in ('accepted', 'deferred') and severity != 'P3':
            raise ValueError('only P3 findings take accepted or deferred')
        latest_kind, latest_number = latest.split()
        if latest_kind == kind and int(latest_number) > int(number):
            raise ValueError('finding reviewed in a later round than this one')

    counts = dict(re.findall(r'(P\d) (\d+)', rows['Open findings']))
    for severity in ('P0', 'P1', 'P2', 'P3'):
        open_count = sum(1 for f in findings if f[1] == severity and f[3] in OPEN)
        if int(counts[severity]) != open_count:
            raise ValueError(f'{severity} count disagrees with the findings')

    for axis in AXES:
        status, name = rows[axis], axis.lower()
        blockers = [f for f in findings
                    if f[2] == name and f[1] != 'P3' and f[3] in OPEN]
        if status != 'incomplete' and name not in reviewed:
            raise ValueError(f'{axis} decided without its own reviewer')
        if status == 'satisfied' and blockers:
            raise ValueError(f'{axis} satisfied with an open blocker')
        if status == 'action-required' and not blockers:
            raise ValueError(f'{axis} action-required without a blocker')
    if rows['Specification'] == 'satisfied' and rows['Requirements'] == 'none':
        raise ValueError('Specification satisfied without a requirement')
    return {'rows': rows, 'reviewers': reviewers, 'findings': findings}


def accepts(result, comparison, requirements):
    """A consumer's final-review gate: both axes satisfied for current inputs."""
    rows = result['rows']
    return (rows['Round'].startswith('final ')
            and all(rows[axis] == 'satisfied' for axis in AXES)
            and rows['Comparison'] == comparison
            and rows['Requirements'] == requirements)


def examples():
    reference = (SKILL / 'references/result-contract.md').read_text()
    return re.findall(r'```markdown\n(.+?)```', reference, re.DOTALL)


def links(path):
    return [link for link in re.findall(r'\]\(([^)]+)\)', path.read_text())
            if '://' not in link and not link.startswith('#')]


class ReviewWorkStructureTest(unittest.TestCase):
    def test_explicit_portable_entrypoint(self):
        text = (SKILL / 'SKILL.md').read_text()
        match = re.fullmatch(r'---\n(.*?)\n---\n(.+)', text, re.DOTALL)
        self.assertIsNotNone(match)
        metadata = yaml.safe_load(match.group(1))
        self.assertEqual(set(metadata), {'name', 'description'})
        self.assertEqual(metadata['name'], SKILL.name)
        self.assertIn('explicitly invokes review-work', metadata['description'])
        self.assertLessEqual(len(text.splitlines()), 500)
        adapter = yaml.safe_load((SKILL / 'agents/openai.yaml').read_text())
        self.assertIs(adapter['policy']['allow_implicit_invocation'], False)
        self.assertIn('$review-work', adapter['interface']['default_prompt'])

    def test_reference_closure(self):
        pending, visited = [SKILL / 'SKILL.md'], set()
        while pending:
            path = pending.pop().resolve()
            if path in visited:
                continue
            visited.add(path)
            for link in links(path):
                target = (path.parent / link.split('#')[0]).resolve()
                self.assertTrue(target.is_relative_to(SKILL.resolve()), link)
                self.assertTrue(target.is_file(), link)
                if target.suffix == '.md':
                    pending.append(target)
        references = {path.resolve() for path in (SKILL / 'references').glob('*.md')}
        self.assertTrue(references <= visited, references - visited)

    def test_instruction_only_package(self):
        for path in SKILL.rglob('*'):
            self.assertFalse(path.is_symlink(), str(path))
            if path.is_file():
                self.assertIn(path.suffix, {'.md', '.yaml'})

    def test_canonical_check_wiring(self):
        for path in (ROOT / 'AGENTS.md', ROOT / 'README.md',
                     ROOT / '.github/workflows/validate.yml'):
            self.assertIn('python3 tests/review-work-test.py', path.read_text(),
                          str(path))


class ResultContractTest(unittest.TestCase):
    def test_examples_parse_and_gate(self):
        complete, standalone = map(parse_review_result, examples())
        rows = complete['rows']
        self.assertTrue(accepts(complete, rows['Comparison'], rows['Requirements']))
        self.assertEqual(standalone['rows']['Specification'], 'incomplete')
        self.assertFalse(accepts(standalone, standalone['rows']['Comparison'],
                                 standalone['rows']['Requirements']))

    def test_gate_rejects_stale_inputs(self):
        result = parse_review_result(examples()[0])
        rows = result['rows']
        newer_head = rows['Comparison'].replace('head 3333', 'head 4444', 1)
        self.assertNotEqual(newer_head, rows['Comparison'])
        self.assertFalse(accepts(result, newer_head, rows['Requirements']))
        self.assertFalse(accepts(result, rows['Comparison'],
                                 rows['Requirements'] + '-edited'))

    def test_rejects_known_bad_results(self):
        good, standalone = examples()
        mutations = {
            'specification without requirement': (
                standalone, '| Specification | incomplete |',
                '| Specification | satisfied |'),
            'axis without its reviewer': (
                standalone, '| Specification | incomplete |',
                '| Specification | action-required |'),
            'satisfied with open blocker': (
                good, 'F1 (P2, specification, resolved)',
                'F1 (P2, specification, unresolved)'),
            'action-required without blocker': (
                good, '| Standards | satisfied |',
                '| Standards | action-required |'),
            'coordinator fills an axis': (
                good, 'standards-reviewer-2: standards',
                'coordinator: standards'),
            'repeated reviewer label': (
                good, 'specification-reviewer-2: specification',
                'standards-reviewer-2: specification'),
            'open count disagrees': (
                standalone, 'P0 0; P1 1;', 'P0 0; P1 0;'),
            'deferred blocker': (
                standalone, '(P1, standards, unresolved)',
                '(P1, standards, deferred)'),
            'finding from a later round': (
                good, 'latest final 2\n', 'latest final 3\n'),
            'short commit': (
                good, 'head 3333333333333333333333333333333333333333',
                'head 3333333'),
            'unknown status': (
                good, '| Standards | satisfied |', '| Standards | approved |'),
            'unlabelled reviewer level': (
                good, 'level high (user-stated); specification',
                'level high; specification'),
            'missing coverage': (
                good, '\n**Coverage:** Both', '\nBoth'),
            'row order': (
                good, '| Standards | satisfied |\n| Specification | satisfied |',
                '| Specification | satisfied |\n| Standards | satisfied |'),
        }
        for name, (example, old, new) in mutations.items():
            with self.subTest(mutation=name):
                self.assertIn(old, example)
                with self.assertRaises(ValueError):
                    parse_review_result(example.replace(old, new, 1))


class MigrationTest(unittest.TestCase):
    def test_procedure_moved_once(self):
        for moved in ('review-cycles.md', 'review-selection.md',
                      'claude-code-reviewer-selection.md',
                      'codex-reviewer-selection.md'):
            self.assertFalse((SKILLS / 'deliver-work/references' / moved).exists())
        tables = [path.relative_to(SKILLS).as_posix()
                  for path in SKILLS.rglob('*.md')
                  if '| Impact | Reviewer default |' in path.read_text()]
        self.assertEqual(sorted(tables), [
            'review-work/references/claude-code-reviewers.md',
            'review-work/references/codex-reviewers.md'])

    def test_callers_name_existing_resources(self):
        deliver = (SKILLS / 'deliver-work/SKILL.md').read_text()
        self.assertIn('`review-work`', deliver)
        self.assertIn('references/corrections.md', links(SKILLS / 'deliver-work/SKILL.md'))
        plan = (SKILLS / 'plan-work/SKILL.md').read_text()
        for resource in ('references/review-selection.md',
                         'references/claude-code-reviewers.md',
                         'references/codex-reviewers.md'):
            with self.subTest(resource=resource):
                self.assertTrue((SKILL / resource).is_file())
                self.assertIn(resource, plan)
        for caller in ('deliver-work', 'plan-work'):
            for path in (SKILLS / caller).rglob('*.md'):
                self.assertNotIn('review-cycles.md', path.read_text(), str(path))
        self.assertIn('## Review an assigned axis',
                      (SKILLS / 'code-review/SKILL.md').read_text())

    def test_installation_example_includes_review_work(self):
        readme = (ROOT / 'README.md').read_text()
        command = next(line for line in readme.splitlines() if line.startswith(
            './scripts/manage-skills.sh install --agent codex deliver-work '))
        self.assertIn('review-work', command.split())
        self.assertIn('code-review', command.split())
        self.assertIn('### Adopt an update that adds a required skill', readme)
        self.assertIn('Explicit `$review-work`', readme)

    def test_scenario_cases_match_graders(self):
        cases = (FIXTURES / 'review-work-cases.md').read_text()
        graders = (FIXTURES / 'review-work-graders.md').read_text()
        case_ids = re.findall(r'^## (RW\d+):', cases, re.MULTILINE)
        grader_ids = re.findall(r'^\| (RW\d+) \|', graders, re.MULTILINE)
        self.assertTrue(case_ids)
        self.assertEqual(case_ids, grader_ids)
        scenarios = (SKILL / 'references/validation-scenarios.md').read_text()
        self.assertIn('review-work-cases.md', scenarios)
        self.assertIn('review-work-graders.md', scenarios)


if __name__ == '__main__':
    unittest.main()
