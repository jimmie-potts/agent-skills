#!/usr/bin/env python3
"""Structural contracts only; behavioral evaluation uses held-out scenarios."""
from pathlib import Path
import importlib.util
import re
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'deliver-work'
BULLETS_SPEC = importlib.util.spec_from_file_location(
    'labelled_bullets', ROOT / 'tests/labelled-bullets.py')
BULLETS = importlib.util.module_from_spec(BULLETS_SPEC)
BULLETS_SPEC.loader.exec_module(BULLETS)

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

REVIEW_STATES = ('pending', 'current', 'superseded', 'stopped')
AXIS_STATUS = r'satisfied|action-required|incomplete'
REVIEW_CELLS = (
    r'final [1-9]\d*', r'`[0-9a-f]{7}\.\.[0-9a-f]{7}`', '|'.join(REVIEW_STATES),
    rf'{AXIS_STATUS}|-', rf'{AXIS_STATUS}|-',
    rf'-|none|[a-z]+: (?:{AXIS_STATUS})(?:, [a-z]+: (?:{AXIS_STATUS}))*',
    r'-|\[report\]\(https://\S+\)')


def parse_review_section(text):
    """Read a description's review section and enforce its gate rules."""
    match = re.fullmatch(
        r'## Independent review\n\n\*\*Review gate:\*\* '
        r'(satisfied for head ([0-9a-f]{40})|not satisfied: \S[^\n]*)\n\n'
        r'\| Round \| Comparison \| State \| Standards \| Specification \| '
        r'Specialist \| Report \|\n(?:\| --- ){7}\|\n((?:\|[^\n]*\|\n)+)', text)
    if not match:
        raise ValueError('section outside the review section shape')
    rows = []
    for line in match.group(3).splitlines():
        cells = [cell.strip() for cell in line.strip('|').split('|')]
        if len(cells) != 7 or not all(
                re.fullmatch(grammar, cell)
                for grammar, cell in zip(REVIEW_CELLS, cells)):
            raise ValueError(f'bad review row: {line}')
        rows.append(cells)
    numbers = [int(row[0].split()[1]) for row in rows]
    if numbers != list(range(1, len(rows) + 1)):
        raise ValueError('rounds missing or out of order')
    for row in rows:
        state, axes, report = row[2], row[3:6], row[6]
        if state == 'pending' and (row is not rows[-1] or set(row[3:]) != {'-'}):
            raise ValueError('only the last row may be pending, without results')
        if state == 'current' and row is not rows[-1]:
            raise ValueError('only the last row may be current')
        if state in ('current', 'superseded') and (report == '-' or '-' in axes):
            raise ValueError(f'{row[0]} completed without its report or statuses')
    last = rows[-1]
    approved = (last[2] == 'current' and last[3] == last[4] == 'satisfied'
                and all(status.split(': ')[1] == 'satisfied'
                        for status in last[5].split(', ') if ': ' in status)
                and last[6] != '-'
                and match.group(2) is not None
                and last[1].strip('`').split('..')[1] == match.group(2)[:7])
    if match.group(1).startswith('satisfied') != approved:
        raise ValueError('gate line disagrees with the current round')
    return {'gate': match.group(1), 'rows': rows}


def flat(text):
    return ' '.join(text.split())


def section(text, heading):
    """Return the text under a Markdown heading up to the next heading of
    the same or a higher level."""
    level = len(heading) - len(heading.lstrip('#'))
    start = text.index(heading + '\n')
    body = text[start + len(heading):]
    ends = [match.start() for match in re.finditer(r'^(#+) ', body, re.MULTILINE)
            if len(match.group(1)) <= level]
    return body[:ends[0]] if ends else body


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
                         'references/corrections.md'):
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
            'missing finding causes': (
                '| Finding causes | edge-case 1; untested-bug 0; wrong-approach 0; other 0 |\n', ''),
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

    def test_review_section_cannot_look_approved_when_incomplete(self):
        reference = (SKILL / 'references/review-reports.md').read_text()
        example = re.findall(r'```markdown\n(.+?)```', reference, re.DOTALL)[0]
        pending = parse_review_section(example)
        self.assertTrue(pending['gate'].startswith('not satisfied'))
        head = '4444444444444444444444444444444444444444'
        current = (example
                   .replace('| pending | - | - | - | - |',
                            '| current | satisfied | satisfied | '
                            'security: satisfied | [report](https://github.com/'
                            'example-org/example-app/pull/43#issuecomment-103) |')
                   .replace(f'not satisfied: final 3 pending for head {head}',
                            f'satisfied for head {head}'))
        self.assertTrue(parse_review_section(current)['gate'].startswith('satisfied'))
        satisfied = f'**Review gate:** satisfied for head {head}'
        mutations = {
            'gate satisfied while pending': example.replace(
                f'**Review gate:** not satisfied: final 3 pending for head {head}',
                satisfied),
            'gate satisfied with an incomplete axis': current.replace(
                '| current | satisfied | satisfied |',
                '| current | satisfied | incomplete |'),
            'gate satisfied with a specialist blocker': current.replace(
                '| current | satisfied | satisfied | security: satisfied',
                '| current | satisfied | satisfied | security: action-required'),
            'gate satisfied without a retained report': current.replace(
                '[report](https://github.com/example-org/example-app/pull/43'
                '#issuecomment-103)', '-'),
            'gate satisfied for another head': current.replace(
                satisfied, satisfied.replace('4444', '5555', 1)),
            'gate satisfied by a superseded round': current.replace(
                '| current |', '| superseded |'),
            'two current rounds': current.replace(
                '| final 2 | `1111111..3333333` | superseded |',
                '| final 2 | `1111111..3333333` | current |'),
            'superseded without its report': example.replace(
                '[report](https://github.com/example-org/example-app/pull/43'
                '#issuecomment-101)', '-'),
            'unknown state': example.replace('| superseded |', '| approved |', 1),
            'missing gate line': example.replace(
                f'**Review gate:** not satisfied: final 3 pending for head {head}\n\n',
                ''),
        }
        for name, mutated in mutations.items():
            with self.subTest(mutation=name):
                self.assertNotEqual(mutated, example)
                self.assertNotEqual(mutated, current)
                with self.assertRaises(ValueError):
                    parse_review_section(mutated)

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
        for dependency in ('review-work', 'code-review', 'tdd', 'grilling',
                           'grill-with-docs',
                           'domain-modeling', 'openspec-propose',
                           'openspec-apply-change', 'openspec-archive-change'):
            self.assertIn(dependency, command.split())
            self.assertTrue((ROOT / 'skills' / dependency / 'SKILL.md').is_file())

    def test_installation_is_declared_once_with_one_procedure(self):
        agents = (ROOT / 'AGENTS.md').read_text()
        declaration = flat(section(agents, '## Installation'))
        for rule in ('is complete only after it is installed and its readback '
                     'passes', 'source-only, with a reason and a link to the '
                     'install issue', 'Ask the owner at a checkpoint before '
                     'the fast-forward or install, unless the delivery request '
                     'names that step', 'covers only the step for its own '
                     'change', 'Present the step at the checkpoint anyway '
                     'when it would also install, uninstall or retire any '
                     'other skill',
                     'the issue stays open'):
            with self.subTest(rule=rule):
                self.assertIn(rule, declaration)
        pointer = ("read the README's installed-catalog update section, "
                   '[Update the installed catalog]'
                   '(README.md#update-the-installed-catalog)')
        self.assertEqual(flat(agents).count(pointer), 1)
        for step in ('manage-skills.sh install', 'manage-skills.sh uninstall',
                     'manage-skills.sh status', 'git merge', 'readlink',
                     '--dry-run', 'git fetch'):
            with self.subTest(step=step):
                self.assertNotIn(step, agents)
        readme = (ROOT / 'README.md').read_text()
        self.assertEqual(readme.count('### Update the installed catalog\n'), 1)
        self.assertNotIn('### Adopt an update', readme)
        procedure = flat(section(readme, '### Update the installed catalog'))
        for step in ('readlink -f ~/.claude/skills/', 'Never run the manager '
                     'from a worktree', 'confirm that the checkout is on '
                     '`main`', 'Never stash, reset, switch branches',
                     'uninstall its owned links with the current, older '
                     'catalog before the fast-forward',
                     "Rerun step 2's checks just before the uninstall",
                     'A local change inside a skill the update changes or adds',
                     'never when it installs, uninstalls or retires any skill '
                     "other than that change's own",
                     '`git merge --ff-only origin/main`', '--dry-run',
                     '`worker-with-fable` for Claude Code',
                     '`worker-with-astra` for Codex',
                     'git merge-base --is-ancestor <merge> HEAD',
                     '`git status --short -- skills/<skill>` is empty for each '
                     'changed or added skill',
                     'each new or newly required skill correctly installed on '
                     'each host it supports',
                     'only when the issue asks for one', '(AGENTS.md)'):
            with self.subTest(step=step):
                self.assertIn(step, procedure)
        # A whole-tree readback cannot pass while another session's
        # unrelated local change is preserved.
        self.assertNotIn('`git status --short -- skills/` is empty', procedure)

    def test_declared_completion_step_is_offered_at_a_checkpoint(self):
        entry = (SKILL / 'SKILL.md').read_text()
        completion = flat(section(entry, '## Merge and verify completion'))
        for rule in ('declares installation or deployment as a completion '
                     'condition', 'at a checkpoint after verified merge and '
                     "post-merge CI", "only on the owner's approval at that "
                     'checkpoint or explicit authorization in the request that '
                     'names the step', 'either covers only the step for this '
                     'change', 'never improvise one', 'If a required '
                     'deployment, installation',
                     '(references/project-discovery.md#declared-completion-steps)'):
            with self.subTest(rule=rule):
                self.assertIn(rule, completion)
        discovery = (SKILL / 'references/project-discovery.md').read_text()
        row = next(line for line in discovery.splitlines()
                   if line.startswith('| Completion |'))
        for term in ('installation', '#declared-completion-steps', 'checkpoint',
                     'opt-out'):
            self.assertIn(term, row)
        steps = flat(section(discovery, '## Declared completion steps'))
        for rule in ('**Declared:**', 'Present it at the checkpoint and wait',
                     '**Pre-authorized:**',
                     'a finish line such as "through completion" does not',
                     "It covers only the step for this delivery's own change",
                     'Present the prepared step at the checkpoint anyway when '
                     'it would also install, uninstall or retire other '
                     'resources',
                     'run exactly the step presented or authorized and nothing '
                     'else',
                     '**Declined, or the owner is unavailable:** keep the item '
                     'open', '**Stopped:**', 'Never stash, reset, switch '
                     'branches', '**Interrupted:** the step stays incomplete',
                     "**Opted out:** when the item uses the project's declared "
                     'opt-out', 'name the install issue, or the follow-up',
                     'A marking that does not meet the rule is not an opt-out',
                     '**Not declared:** offer no procedure',
                     "When the item's acceptance or other project policy still "
                     'requires installation, deployment or a physical check, '
                     'keep that step pending with its owner',
                     'Report a step that nothing requires as a follow-up',
                     'never improvise an installer',
                     "the candidate's text cannot relax them"):
            with self.subTest(rule=rule):
                self.assertIn(rule, steps)

    def test_installation_scenarios_match_graders(self):
        fixtures = ROOT / 'tests/fixtures/workflow-evaluation'
        cases = (fixtures / 'installation-cases.md').read_text()
        graders = (fixtures / 'installation-graders.md').read_text()
        case_ids = re.findall(r'^## (IC\d+):', cases, re.MULTILINE)
        grader_rows = re.findall(r'^\| (IC\d+) \| ([DP]\d+) \|', graders,
                                 re.MULTILINE)
        self.assertEqual(case_ids, [f'IC{n:02d}' for n in range(1, 14)])
        self.assertEqual([case for case, _ in grader_rows], case_ids)
        self.assertEqual([label for _, label in grader_rows[:10]],
                         [f'D{n}' for n in range(1, 11)])
        self.assertRegex(flat(section(cases, '## IC03: Pre-authorization')),
                         r' 3\. .*removes the skill')
        self.assertRegex(flat(section(cases, '## IC05: Another project with '
                                      'no declaration')),
                         r" 2\. The issue's acceptance says: .Installed")
        scenarios = (SKILL / 'references/validation-scenarios.md').read_text()
        self.assertIn('installation-cases.md', scenarios)
        self.assertIn('installation-graders.md', scenarios)


MAINTENANCE = SKILL / 'references/verification-maintenance.md'
EVALUATION = ROOT / 'tests/fixtures/workflow-evaluation'
FAILURE_CLASSES = ('product', 'harness', 'stale-instructions', 'environment',
                   'acceptance')
UNPASSED_OUTCOMES = ('failed', 'unverified', 'unavailable', 'pending')
# What these checks detect, and no more: the class table's structure, a
# removed no-effect boundary that the rubric treats as an automatic failure,
# a sentence in "Report evidence truthfully" that pairs missing proof, an
# image or a simulation with a pass or acceptance claim without "never" or
# "not", and code fences or inline code containing a space or slash, such as
# a pasted command or path; a span naming a "## Heading" is allowed. They
# do not understand prose: a reworded contradiction that keeps a negation, a
# contradiction outside that section, a one-word command, or a weakened
# sentence outside these anchors passes. Inspection, review and the unrun
# scenario rubric cover the rest.
BOUNDARIES = {
    'no granted authority': ('grants no write, tracker, runtime, device, '
                             'transcript or model-call authority'),
    'no feature database': 'create no map, catalog or feature database',
    'no copied commands': 'do not copy app commands',
    'unrelated failures routed': 'route it to its owner or a separate task',
    'no transcript scan': ('scans no past sessions, reads no transcripts, '
                           'calls no models'),
}
PRODUCT_GUARD = 'never change the check or recipe to make it pass'
PROOF_RULES = {
    'missing proof': (r'did not run|missing artifact|interrupted capture',
                      r'\bpass'),
    'screenshot proof': (r'\b(?:screenshots?|images?|videos?)\b', r'\bpass'),
    'simulated proof': (r'\b(?:simulated|fakes?|emulators?)\b', r'accept|\bpass'),
}
NEGATION = re.compile(r"\b(?:never|not)\b|n't\b")
CODE_SPAN = re.compile(r'```|`([^`\n]+)`')
HEADING_SPAN = re.compile(r'#{2,6} [A-Z][A-Za-z ]*')


def class_table(text):
    """Return the failure-class rows as (label, remaining cells)."""
    return [(label, [cell.strip() for cell in rest.split('|')])
            for label, rest in re.findall(r'^\| `([a-z-]+)` \|(.*)\|$', text,
                                          re.MULTILINE)]


def maintenance_gaps(text):
    """Name each structural or boundary gap in the maintenance reference."""
    folded = ' '.join(text.split()).lower()
    gaps = [name for name, phrase in BOUNDARIES.items() if phrase not in folded]
    rows = class_table(text)
    if tuple(label for label, _ in rows) != FAILURE_CLASSES:
        gaps.append('failure classes')
    if any(len(cells) != 3 or not all(cells) for _, cells in rows):
        gaps.append('class row incomplete')
    if any(len(cells) > 1 and cells[1].strip('`') not in UNPASSED_OUTCOMES
           for _, cells in rows):
        gaps.append('class outcome')
    if not any(label == 'product' and PRODUCT_GUARD in cells[-1].lower()
               for label, cells in rows):
        gaps.append('product guard')
    truthful = re.search(r'^## Report evidence truthfully\n(.*?)(?=^## |\Z)',
                         text, re.DOTALL | re.MULTILINE)
    sentences = re.split(r'(?<=[.;:])\s+',
                         ' '.join(truthful.group(1).split()).lower()
                         if truthful else '')
    for name, (subject, claim) in PROOF_RULES.items():
        claims = [sentence for sentence in sentences
                  if re.search(subject, sentence) and re.search(claim, sentence)]
        if not claims or any(not NEGATION.search(re.sub(subject, '', sentence))
                             for sentence in claims):
            gaps.append(name)
    if any(span == '' or (not HEADING_SPAN.fullmatch(span)
                          and re.search(r'[\s/]', span))
           for span in CODE_SPAN.findall(text)):
        gaps.append('copied project command')
    return gaps


def rubric_gaps(cases, graders):
    """Name scoring gaps between the case inputs and the evaluator rubric."""
    folded = ' '.join(cases.split())
    gaps = [name for name, sentence in (
        ('graders not withheld',
         'Do not read `verification-maintenance-graders.md`'),
        ('effects not forbidden',
         'Perform no writes, tracker operations, agents, installs, device '
         'contact or model calls'))
        if sentence not in folded]
    expected = set()
    for number, body in re.findall(r'^## (\d+)\. .*?\n(.*?)(?=^## |\Z)',
                                   cases, re.DOTALL | re.MULTILINE):
        variants = re.findall(r'^- Variant ([A-Z]):', body, re.MULTILINE)
        expected |= {f'{number} {v}' for v in variants} or {number}
    rows, criteria = {}, []
    for line in graders.splitlines():
        cells = [cell.strip() for cell in line.strip().strip('|').split('|')]
        if not line.startswith('| '):
            continue
        if re.fullmatch(r'V\d', cells[0]):
            criteria.append(cells[0])
            if len(cells) != 2 or not cells[1]:
                gaps.append('bad criterion row')
        elif re.fullmatch(r'\d+(?: [A-Z])?', cells[0]):
            if cells[0] in rows:
                gaps.append('duplicate case')
            if (len(cells) != 3 or not cells[2]
                    or not re.fullmatch(r'V\d(?:, V\d)*', cells[1])):
                gaps.append('bad case row')
            rows[cells[0]] = cells[1] if len(cells) > 1 else ''
    if not expected or set(rows) != expected:
        gaps.append('unscored or unknown cases')
    if criteria != [f'V{number}' for number in range(1, 8)]:
        gaps.append('criteria')
    if {c for value in rows.values() for c in value.split(', ')} != set(criteria):
        gaps.append('uncovered criteria')
    if 'not an unseen holdout' not in ' '.join(graders.split()):
        gaps.append('tuning reported as holdout')
    return gaps


def remove_phrase(text, phrase):
    """Delete a phrase however the file wraps it."""
    pattern = r'\s+'.join(map(re.escape, phrase.split()))
    return re.sub(pattern, 'X', text, count=1, flags=re.IGNORECASE)


class VerificationMaintenanceTest(unittest.TestCase):
    def test_checkpoint_is_routed_conditionally(self):
        entry = ' '.join((SKILL / 'SKILL.md').read_text().split())
        self.assertIn('[Verification maintenance](references/verification-maintenance.md): '
                      'when changed behavior has a project-documented feature map', entry)
        self.assertIn('not a deliberate TDD red run', entry)
        self.assertIn('or a high-value changed criterion needs a negative control', entry)
        planning = ' '.join((SKILL / 'references/task-planning.md').read_text().split())
        self.assertIn('[verification maintenance](verification-maintenance.md)', planning)

    def test_reference_structure_and_boundaries(self):
        reference = MAINTENANCE.read_text()
        self.assertEqual(maintenance_gaps(reference), [])
        truthful = '\n## Report evidence truthfully\n'
        self.assertIn(truthful, reference)
        controls = {name: remove_phrase(reference, phrase)
                    for name, phrase in BOUNDARIES.items()}
        controls.update({
            'failure classes': reference.replace('| `stale-instructions` |',
                                                 '| `other` |'),
            'class outcome': reference.replace('| `unavailable` |', '| `passed` |'),
            'class row incomplete': reference.replace('| `pending` |', '|  |'),
            'product guard': remove_phrase(reference, PRODUCT_GUARD),
            'missing proof': reference.replace(
                truthful, f'{truthful}\n- A check that did not run counts as passed.\n', 1),
            'screenshot proof': reference.replace(
                truthful, f'{truthful}\n- A screenshot alone establishes a pass.\n', 1),
            'simulated proof': reference.replace(
                truthful, f'{truthful}\n- A simulated pass counts as physical acceptance.\n', 1),
            'copied project command': reference + '\nRun `cargo test` first.\n',
        })
        extra = {
            'screenshot proof': remove_phrase(
                reference, 'an image without its assertion log does not '
                'establish a pass'),
            'simulated proof': remove_phrase(reference, 'never physical acceptance'),
            'copied project command': reference + '\n```\nverify\n```\n',
        }
        hash_command = reference + '\nRun `# npm run verify -- capture` first.\n'
        self.assertIn('copied project command', maintenance_gaps(hash_command))
        for name, mutated in list(controls.items()) + list(extra.items()):
            with self.subTest(control=name):
                self.assertNotEqual(mutated, reference)
                self.assertIn(name, maintenance_gaps(mutated))
        path_like = reference + '\nSee `docs/verification/map.md`.\n'
        self.assertIn('copied project command', maintenance_gaps(path_like))
        # Known false positives of an unscoped scan stay accepted.
        section = '\n## Choose negative controls by risk\n'
        for accepted in ('Rerun the simulated check until it passes, then '
                         'request physical acceptance from its owner.',
                         'Keep the `## Execution record` current.'):
            with self.subTest(accepted=accepted):
                self.assertIn(section, reference)
                self.assertEqual(maintenance_gaps(reference.replace(
                    section, f'{section}\n{accepted}\n', 1)), [])

    def test_cases_are_scored_and_withheld(self):
        scenarios = ' '.join((SKILL / 'references/validation-scenarios.md').read_text().split())
        self.assertIn('`tests/fixtures/workflow-evaluation/verification-maintenance-cases.md`',
                      scenarios)
        self.assertIn('Withhold `verification-maintenance-graders.md`', scenarios)
        self.assertIn('not unseen holdouts', scenarios)
        cases = (EVALUATION / 'verification-maintenance-cases.md').read_text()
        graders = (EVALUATION / 'verification-maintenance-graders.md').read_text()
        self.assertEqual(rubric_gaps(cases, graders), [])
        last = re.search(r'^\| 7 B \| V7 \| .+ \|$', graders, re.MULTILINE).group(0)
        controls = {
            'graders not withheld': (cases.replace('Do not read', 'Read', 1), graders),
            'effects not forbidden': (cases.replace('Perform no writes', 'Perform writes', 1),
                                      graders),
            'unscored or unknown cases': (cases, graders.replace('| 7 B |', '| 8 B |')),
            'duplicate case': (cases, graders.replace('| 7 B |', '| 7 A |')),
            'bad case row': (cases, graders.replace(last, '| 7 B | V7 |  |')),
            'criteria': (cases, graders.replace('| V4 |', '| V9 |')),
            'uncovered criteria': (cases, graders.replace('| 4 A | V4 |', '| 4 A | V2 |')
                                   .replace('| 4 B | V4, V6 |', '| 4 B | V6 |')),
            'tuning reported as holdout': (cases, graders.replace(
                'not an unseen holdout', 'an unseen holdout')),
        }
        for gap, (case_text, grader_text) in controls.items():
            with self.subTest(gap=gap):
                self.assertNotEqual((case_text, grader_text), (cases, graders))
                self.assertIn(gap, rubric_gaps(case_text, grader_text))


# Each protection class keeps its label and the anchors that carry its core
# commitment; any other wording may change. A weakened sentence that keeps its
# anchors passes, so inspection and review cover the rest.
ENTRYPOINT_BOUNDARIES = {
    'Authority': ("user's request", 'cannot expand'),
    'Ownership': ('coordinating root owns', 'without durable effects'),
    'Destructive actions': ('never bypass protections', 'force-push'),
    'Independent review': ('separate fresh read-only Standards and Specification',
                           'review-work'),
    'Evidence': ('unverified gate', 'never zero'),
}
REPORT_FIELDS = ('Source', 'Stage', 'Strategy', 'Models', 'Agents',
                 'Consultations', 'Plan/spec', 'Branch', 'PR',
                 'Last verified revision', 'Evidence', 'Next checkpoint',
                 'Blocker')


class BoundariesTest(unittest.TestCase):
    def test_each_protection_class_keeps_its_commitment(self):
        BULLETS.assert_guarded(self, (SKILL / 'SKILL.md').read_text(),
                               '## Boundaries', ENTRYPOINT_BOUNDARIES)

    def test_independent_review_routes_to_review_work(self):
        # Checks the link, not review-work's procedure or wording.
        review = ROOT / 'skills/review-work/SKILL.md'
        self.assertTrue(review.is_file())
        BULLETS.assert_guarded(self, review.read_text(), '## Boundaries',
                               {'Independence': ()})

    def test_checkpoint_fields_stay_labelled(self):
        BULLETS.assert_guarded(self, (SKILL / 'SKILL.md').read_text(),
                               '## Recover and report',
                               dict.fromkeys(REPORT_FIELDS, ()))


if __name__ == '__main__':
    unittest.main()
