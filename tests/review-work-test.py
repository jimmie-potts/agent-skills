#!/usr/bin/env python3
"""Structural and result-contract checks; behavior uses held-out scenarios."""
from pathlib import Path
import hashlib
import importlib.util
import re
import tomllib
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'skills'
SKILL = SKILLS / 'review-work'
FIXTURES = ROOT / 'tests/fixtures/workflow-evaluation'
POSTED = ROOT / 'tests/fixtures/review-results'
BULLETS_SPEC = importlib.util.spec_from_file_location(
    'labelled_bullets', ROOT / 'tests/labelled-bullets.py')
BULLETS = importlib.util.module_from_spec(BULLETS_SPEC)
BULLETS_SPEC.loader.exec_module(BULLETS)

# Each protection class keeps its label and the anchors that carry its core
# commitment; any other wording may change. A weakened sentence that keeps its
# anchors passes, so inspection and review cover the rest.
BOUNDARIES = {
    'Authority': ('grants no authority', 'belongs to the caller'),
    'Ownership': ('reviewers are read-only', 'launch no agents'),
    'Independence': ('fresh read-only context', 'never fills an axis'),
    'Evidence': ('never approved', 'gates are a floor'),
    'Scope': ('do not invent acceptance criteria', 'scope owner'),
}

ROWS = ('Work', 'Round', 'Comparison', 'Requirements', 'Policy', 'Standards',
        'Specification', 'Reviewers', 'Open findings')
AXES = ('Standards', 'Specification')
STATUS = r'(?:satisfied|action-required|incomplete)'
TOKEN = r'[^\s|()+,;]+'
LABEL = r'[a-z0-9]+(?:-[a-z0-9]+)*'
KNOWN = rf'(?!unknown ){TOKEN} \((?:host-observed|user-stated|self-reported)\)'
SOURCED = rf'(?:unknown \(unknown\)|{KNOWN}(?: \+ {KNOWN})*)'
POLICY = rf'(?!unknown\b)(?:[\w.-]+(?:/[\w.-]+)?@[0-9a-f]{{40}}|{TOKEN} read \d{{4}}-\d{{2}}-\d{{2}})'
REVIEWER = (rf'({LABEL}): ([a-z]+), requested {TOKEN} at {TOKEN}, '
            rf'model {SOURCED}, level {SOURCED}')
CELLS = {
    'Work': r'[\w.-]+/[\w.-]+#\d+|[A-Z][A-Z0-9]*-\d+|https?://\S+|none',
    'Round': r'(?:final|task) [1-9]\d*',
    'Comparison': (r'base [0-9a-f]{40}; head [0-9a-f]{40}; merge-base [0-9a-f]{40}'
                   r'|patch sha256:[0-9a-f]{64}'),
    'Requirements': rf'{TOKEN} at {TOKEN}|none',
    'Policy': rf'unknown|{POLICY}(?: \+ {POLICY})*',
    'Standards': STATUS,
    'Specification': STATUS,
    'Reviewers': rf'none|{REVIEWER}(?:; {REVIEWER})*',
    'Open findings': r'P0 \d+; P1 \d+; P2 \d+; P3 \d+',
}
FINDING = re.compile(
    r'- ([A-Za-z0-9]+(?:-[A-Za-z0-9]+)*) \((P[0-3]), ([a-z]+(?:\+[a-z]+)*), '
    r'(unresolved|resolved|regression|accepted|deferred)\): ([^\s:,]+).*; '
    r'first ((?:final|task) \d+), latest ((?:final|task) \d+)')
OPEN = ('unresolved', 'regression')
RETURN_ROWS = ('Axis', 'Comparison', 'Requirements', 'Policy', 'Return',
               'Digest', 'Redactions')
RETURN_CELLS = {
    'Axis': r'[a-z]+',
    'Comparison': CELLS['Comparison'],
    'Requirements': CELLS['Requirements'],
    'Policy': CELLS['Policy'],
    'Return': r'complete|partial|failed',
    'Digest': r'sha256:[0-9a-f]{64}',
    'Redactions': r'none|[1-9]\d*: [a-z]+(?: [a-z]+)*(?:, [a-z]+(?: [a-z]+)*)*',
}
PROVENANCE = ('Comparison', 'Requirements', 'Policy')


def parse_table(block, cells, order):
    rows = {}
    for line in block.splitlines():
        match = re.fullmatch(r'\| ([^|]+?) \| ([^|]+?) \|', line)
        if not match or match.group(1) in rows or match.group(1) not in cells:
            raise ValueError(f'bad, repeated or unknown row: {line}')
        field, value = match.groups()
        if not re.fullmatch(cells[field], value):
            raise ValueError(f'bad {field} value: {value}')
        rows[field] = value
    if tuple(rows) != order:
        raise ValueError(f'rows out of order or missing: {list(rows)}')
    return rows


def parse_returns(text):
    """Parse the retained reviewer returns and check each digest."""
    returns = []
    if not text:
        return returns
    for block in re.split(r'\n(?=### Reviewer return: )', text):
        match = re.fullmatch(
            r'### Reviewer return: ([^\n]+)\n\n\| Field \| Value \|\n'
            r'\| --- \| --- \|\n((?:\|[^\n]*\|\n)+)\n(~{3,})text\n'
            r'((?:[^\n]*\n)+?)\3\n?', block)
        if not match:
            raise ValueError('reviewer return outside its block shape')
        fence, body = match.group(3), match.group(4)
        if any(re.match(rf'~{{{len(fence)},}}', line)
               for line in body.splitlines()):
            raise ValueError('a return line would close its fence')
        rows = parse_table(match.group(2), RETURN_CELLS, RETURN_ROWS)
        digest = hashlib.sha256(body.encode()).hexdigest()
        if rows['Digest'] != f'sha256:{digest}':
            raise ValueError(f'digest does not match the return: {match.group(1)}')
        returns.append((match.group(1), rows, body))
    return returns


def covered(axis):
    """The axes one reviewer return covers; `both` is a task-round reviewer."""
    return {'standards', 'specification'} if axis == 'both' else {axis}


def parse_review_result(text):
    """Parse one Review result strictly and enforce its status rules."""
    match = re.fullmatch(
        r'## Review result\n\n\| Field \| Value \|\n\| --- \| --- \|\n'
        r'((?:\|[^\n]*\|\n)+)'
        r'\n\*\*Findings:\*\*\n((?:- [^\n]+\n)+|none\n)'
        r'\n\*\*Coverage:\*\* (\S[^\n]*)\n'
        r'(?:\n(### Reviewer return: .+)|\n?)', text, re.DOTALL)
    if not match:
        raise ValueError('section outside the Review result shape')
    rows = parse_table(match.group(1), CELLS, ROWS)
    returns = parse_returns(match.group(4) or '')

    reviewers = [] if rows['Reviewers'] == 'none' else [
        re.match(REVIEWER, entry).groups()
        for entry in rows['Reviewers'].split('; ')]
    labels = [label for label, _ in reviewers]
    if len(set(labels)) != len(labels):
        raise ValueError('repeated reviewer label')
    if any(label.startswith('coordinator') for label in labels):
        raise ValueError('the coordinator cannot fill an axis')
    kind, number = rows['Round'].split()
    if any(axis == 'both' for _, axis in reviewers) and kind != 'task':
        raise ValueError('only a task-round reviewer covers both axes')
    if [(label, axis) for label, axis in reviewers] != [
            (label, ret['Axis']) for label, ret, _ in returns]:
        raise ValueError('each reviewer entry needs its own retained return')
    reviewed = set()
    for _, ret, _ in returns:
        if ret['Return'] == 'complete' and all(
                ret[field] == rows[field] for field in PROVENANCE):
            reviewed |= covered(ret['Axis'])

    findings = []
    if match.group(2) != 'none\n':
        for line in match.group(2).splitlines():
            parsed = FINDING.fullmatch(line)
            if not parsed:
                raise ValueError(f'bad finding: {line}')
            fid, severity, axes, state, location, first, latest = parsed.groups()
            findings.append((fid, severity, axes.split('+'), state, location,
                             first, latest))
    ids = [finding[0] for finding in findings]
    if len(set(ids)) != len(ids):
        raise ValueError('repeated finding ID')
    known = {'standards', 'specification'} | {
        axis for _, axis in reviewers if axis != 'both'}
    for fid, severity, axes, state, location, _, latest in findings:
        if 'both' in axes:
            raise ValueError('a finding lists its axes, never both')
        if len(set(axes)) != len(axes):
            raise ValueError(f'{fid} lists an axis twice')
        if set(axes) - known:
            raise ValueError(f'{fid} lists an unknown axis')
        if state in ('accepted', 'deferred') and severity != 'P3':
            raise ValueError('only P3 findings take accepted or deferred')
        latest_kind, latest_number = latest.split()
        if latest_kind == kind and int(latest_number) > int(number):
            raise ValueError('finding reviewed in a later round than this one')
        # Support: each listed axis's return in this round names the finding's
        # file. This is a static proxy for the coordinator's reconciliation; it
        # cannot tell whether the return raises the same failure condition.
        if latest == rows['Round']:
            cited = location.rsplit('/', 1)[-1]
            for axis in axes:
                if not any(axis in covered(ret['Axis']) and cited in body
                           for _, ret, body in returns):
                    raise ValueError(f'{fid} lists {axis}, but no {axis} return '
                                     'in this round supports it')

    counts = dict(re.findall(r'(P\d) (\d+)', rows['Open findings']))
    for severity in ('P0', 'P1', 'P2', 'P3'):
        open_count = sum(1 for f in findings if f[1] == severity and f[3] in OPEN)
        if int(counts[severity]) != open_count:
            raise ValueError(f'{severity} count disagrees with the findings')

    for axis in AXES:
        status, name = rows[axis], axis.lower()
        blockers = [f for f in findings
                    if name in f[2] and f[1] != 'P3' and f[3] in OPEN]
        if status != 'incomplete' and name not in reviewed:
            raise ValueError(f'{axis} decided without a complete retained '
                             'return from its own reviewer for these inputs')
        if status == 'satisfied' and blockers:
            raise ValueError(f'{axis} satisfied with an open blocker')
        if status == 'action-required' and not blockers:
            raise ValueError(f'{axis} action-required without a blocker')
    if rows['Specification'] == 'satisfied' and rows['Requirements'] == 'none':
        raise ValueError('Specification satisfied without a requirement')
    return {'rows': rows, 'reviewers': reviewers, 'findings': findings,
            'returns': returns}


def accepts(result, comparison, requirements, policy):
    """A consumer's final-review gate: both axes satisfied for current inputs."""
    rows = result['rows']
    return (rows['Round'].startswith('final ')
            and all(rows[axis] == 'satisfied' for axis in AXES)
            and rows['Comparison'] == comparison
            and rows['Requirements'] == requirements
            and rows['Policy'] != 'unknown'
            and rows['Policy'] == policy)


def split_returns(example):
    """Split an example into its summary and its retained return blocks."""
    summary, *blocks = re.split(r'\n(?=### Reviewer return: )', example)
    return summary, blocks


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

    def test_package_resources(self):
        for path in SKILL.rglob('*'):
            self.assertFalse(path.is_symlink(), str(path))
            if path.is_file():
                allowed = {'.md', '.yaml'}
                if path.relative_to(SKILL).as_posix() == 'scripts/process_reviewer.py':
                    allowed = {'.py'}
                if path.relative_to(SKILL).parts[0] == 'assets':
                    allowed = {'.md', '.toml'}
                self.assertIn(path.suffix, allowed, str(path))

    def test_each_protection_class_keeps_its_commitment(self):
        BULLETS.assert_guarded(self, (SKILL / 'SKILL.md').read_text(),
                               '## Boundaries', BOUNDARIES)

    def test_canonical_check_wiring(self):
        for path in (ROOT / 'AGENTS.md', ROOT / 'README.md',
                     ROOT / '.github/workflows/validate.yml'):
            self.assertIn('python3 tests/review-work-test.py', path.read_text(),
                          str(path))


class ResultContractTest(unittest.TestCase):
    def test_examples_parse_and_gate(self):
        complete, standalone = map(parse_review_result, examples())
        rows = complete['rows']
        self.assertTrue(accepts(complete, rows['Comparison'], rows['Requirements'],
                                rows['Policy']))
        other = standalone['rows']
        self.assertEqual(other['Specification'], 'incomplete')
        self.assertFalse(accepts(standalone, other['Comparison'],
                                 other['Requirements'], other['Policy']))

    def test_one_task_reviewer_covers_both_verdicts(self):
        summary, blocks = split_returns(examples()[0])
        good = summary + '\n' + blocks[0].replace(
            '### Reviewer return: standards-reviewer-2',
            '### Reviewer return: task-reviewer-1').replace(
            '| Axis | standards |', '| Axis | both |')
        entries = good.split('| Reviewers | ', 1)[1].split(' |\n', 1)[0]
        task = (good.replace('| Round | final 2 |', '| Round | task 2 |')
                .replace('first final 1, latest final 2', 'first task 1, latest task 2')
                .replace('first final 1, latest final 1', 'first task 1, latest task 1')
                .replace(entries, 'task-reviewer-1: both, requested opus at '
                         'default, model unknown (unknown), level unknown (unknown)'))
        parsed = parse_review_result(task)
        self.assertEqual(parsed['rows']['Specification'], 'satisfied')
        self.assertFalse(accepts(parsed, parsed['rows']['Comparison'],
                                 parsed['rows']['Requirements'],
                                 parsed['rows']['Policy']))
        with self.assertRaisesRegex(ValueError, 'task-round reviewer'):
            parse_review_result(task.replace('| Round | task 2 |',
                                             '| Round | final 2 |'))

    def test_gate_rejects_stale_inputs(self):
        result = parse_review_result(examples()[0])
        rows = result['rows']
        current = (rows['Comparison'], rows['Requirements'], rows['Policy'])
        newer_head = rows['Comparison'].replace('head 3333', 'head 4444', 1)
        self.assertNotEqual(newer_head, rows['Comparison'])
        for stale in ((newer_head, *current[1:]),
                      (current[0], current[1] + '-edited', current[2]),
                      (*current[:2], current[2] + '-newer')):
            with self.subTest(stale=stale):
                self.assertFalse(accepts(result, *stale))
        unknown = parse_review_result(examples()[0].replace(
            f"| Policy | {rows['Policy']} |", '| Policy | unknown |'))
        self.assertFalse(accepts(unknown, *current[:2], 'unknown'))

    def test_rejects_known_bad_results(self):
        good, standalone = examples()
        requirement = good.split('| Requirements | ', 1)[1].split(' |', 1)[0]
        mutations = {
            'specification without requirement': (
                good, f'| Requirements | {requirement} |',
                '| Requirements | none |', 'without a requirement', -1),
            'axis without its reviewer': (
                standalone, '| Specification | incomplete |',
                '| Specification | action-required |', 'from its own reviewer'),
            'satisfied with open blocker': (
                good.replace('P2 0; P3 0', 'P2 1; P3 0'),
                'F1 (P2, specification, resolved)',
                'F1 (P2, specification, unresolved)', 'satisfied with an open'),
            'action-required without blocker': (
                good, '| Standards | satisfied |',
                '| Standards | action-required |', 'without a blocker'),
            'coordinator fills an axis': (
                good, 'standards-reviewer-2: standards',
                'coordinator: standards', 'coordinator'),
            'repeated reviewer label': (
                good, 'specification-reviewer-2: specification',
                'standards-reviewer-2: specification', 'repeated reviewer'),
            'open count disagrees': (
                standalone, 'P0 0; P1 1;', 'P0 0; P1 0;', 'count disagrees'),
            'deferred blocker': (
                standalone, '(P1, standards, unresolved)',
                '(P1, standards, deferred)', 'only P3'),
            'finding from a later round': (
                good, 'latest final 2\n', 'latest final 3\n', 'later round'),
            'finding for both axes': (
                good, 'F1 (P2, specification, resolved)',
                'F1 (P2, both, resolved)', 'never both'),
            'final round reviewer for both axes': (
                good, 'specification-reviewer-2: specification',
                'specification-reviewer-2: both', 'task-round reviewer'),
            'short commit': (
                good, 'head 3333333333333333333333333333333333333333',
                'head 3333333', 'bad Comparison'),
            'unknown status': (
                good, '| Standards | satisfied |', '| Standards | approved |',
                'bad Standards'),
            'unlabelled reviewer level': (
                good, 'level high (user-stated); specification',
                'level high; specification', 'bad Reviewers'),
            'missing coverage': (
                good, '\n**Coverage:** Both', '\nBoth', 'shape'),
            'row order': (
                good, '| Standards | satisfied |\n| Specification | satisfied |',
                '| Specification | satisfied |\n| Standards | satisfied |',
                'out of order'),
        }
        for name, (example, old, new, message, *count) in mutations.items():
            with self.subTest(mutation=name):
                self.assertIn(old, example)
                with self.assertRaisesRegex(ValueError, message):
                    parse_review_result(example.replace(old, new, *(count or [1])))

    def test_retained_returns_decide_axes(self):
        good, standalone = examples()
        summary, (standards, specification) = split_returns(good)
        text = specification.split('~~~text\n', 1)[1].split('~~~', 1)[0]
        head = 'head 3333333333333333333333333333333333333333'
        mutations = {
            'missing return': (summary + '\n' + standards, 'own retained return'),
            'returns out of order': (
                summary + '\n' + specification + '\n' + standards,
                'own retained return'),
            'edited return text': (
                good.replace('now rejects an empty filter', 'rejects empties'),
                'digest does not match'),
            'return for another head': (
                summary + '\n' + standards + '\n'
                + specification.replace(head, head.replace('3', '4')),
                'Specification decided without a complete retained return'),
            'return for another requirement version': (
                summary + '\n' + standards + '\n' + specification.replace(
                    '| Requirements | example-org/example-app#42 at 2026-09-25',
                    '| Requirements | example-org/example-app#42 at 2026-09-24'),
                'Specification decided without a complete retained return'),
            'partial return decides its axis': (
                good.replace('| Return | complete |\n| Digest | sha256:e6d8',
                             '| Return | partial |\n| Digest | sha256:e6d8'),
                'Specification decided without a complete retained return'),
            'unknown return state': (
                good.replace('| Return | complete |', '| Return | approved |', 1),
                'bad Return'),
            'unlisted redaction kinds': (
                standalone.replace('| Redactions | 1: credential |',
                                   '| Redactions | yes |'), 'bad Redactions'),
            'short policy commit': (
                good.replace('abcdef1234567890abcdef1234567890abcdef12',
                             'abcdef1'), 'bad Policy'),
        }
        self.assertTrue(text)
        for name, (mutated, message) in mutations.items():
            with self.subTest(mutation=name):
                self.assertNotEqual(mutated, good)
                with self.assertRaisesRegex(ValueError, message):
                    parse_review_result(mutated)

    def test_failed_return_is_kept_and_leaves_axis_undecided(self):
        good = examples()[0]
        summary, (standards, specification) = split_returns(good)
        body = 'The review stopped: the tool call timed out.\n'
        failed = (specification
                  .replace('specification-reviewer-2', 'specification-reviewer-1')
                  .replace('| Return | complete |', '| Return | failed |')
                  .split('~~~text\n', 1)[0]
                  + '~~~text\n' + body + '~~~\n')
        failed = re.sub(r'sha256:[0-9a-f]{64}', 'sha256:'
                        + hashlib.sha256(body.encode()).hexdigest(), failed)
        entry = ('specification-reviewer-1: specification, requested opus at '
                 'default, model unknown (unknown), level unknown (unknown); ')
        replaced = summary.replace('specification-reviewer-2: specification',
                                   entry + 'specification-reviewer-2: specification')
        parsed = parse_review_result(replaced + '\n' + standards + '\n' + failed
                                     + '\n' + specification)
        self.assertEqual([r['Return'] for _, r, _ in parsed['returns']],
                         ['complete', 'failed', 'complete'])
        rows = parsed['rows']
        self.assertTrue(accepts(parsed, rows['Comparison'], rows['Requirements'],
                                rows['Policy']))
        alone = replaced + '\n' + standards + '\n' + failed
        with self.assertRaisesRegex(ValueError, 'own retained return'):
            parse_review_result(alone)
        alone = alone.replace('; specification-reviewer-2: specification, requested '
                              'opus at default, model claude-opus-5-5 (self-reported), '
                              'level high (user-stated)', '')
        with self.assertRaisesRegex(ValueError, 'no specification return'):
            parse_review_result(alone)
        # A failed reviewer reassesses nothing, so F1 stays as final 1 left it.
        alone = (alone.replace('F1 (P2, specification, resolved)',
                               'F1 (P2, specification, unresolved)')
                 .replace('latest final 2\n', 'latest final 1\n')
                 .replace('P2 0; P3 0', 'P2 1; P3 0'))
        with self.assertRaisesRegex(ValueError, 'Specification decided without'):
            parse_review_result(alone)
        undecided = parse_review_result(alone.replace(
            '| Specification | satisfied |', '| Specification | incomplete |'))
        self.assertFalse(accepts(undecided, rows['Comparison'],
                                 rows['Requirements'], rows['Policy']))

    def test_no_reviewer_result_has_no_returns(self):
        standalone = examples()[1]
        summary, _ = split_returns(standalone)
        none = (summary.replace(
            summary.split('| Reviewers | ', 1)[1].split(' |\n', 1)[0], 'none')
            .replace('| Standards | action-required |', '| Standards | incomplete |')
            .replace('P1 1;', 'P1 0;')
            .replace('- F1 (P1, standards, unresolved): lib/auth.py:88, an expired '
                     'token passes the check; first final 1, latest final 1\n',
                     'none\n'))
        parsed = parse_review_result(none.rstrip('\n') + '\n')
        self.assertEqual(parsed['returns'], [])
        self.assertFalse(accepts(parsed, *(parsed['rows'][f] for f in
                                          ('Comparison', 'Requirements', 'Policy'))))
        with self.assertRaisesRegex(ValueError, 'own retained return'):
            parse_review_result(summary)

    def test_return_containing_a_tilde_fence(self):
        good = examples()[0]
        summary, (standards, specification) = split_returns(good)
        body = 'Verdict: satisfied.\n~~~\nquoted fence\n~~~\nCoverage: all.\n'
        digest = hashlib.sha256(body.encode()).hexdigest()
        head = standards.split('~~~text\n', 1)[0]
        head = re.sub(r'sha256:[0-9a-f]{64}', 'sha256:' + digest, head)
        longer = head + '~~~~text\n' + body + '~~~~\n'
        self.assertEqual(len(parse_review_result(
            summary + '\n' + longer + '\n' + specification)['returns']), 2)
        with self.assertRaises(ValueError):
            parse_review_result(summary + '\n' + head + '~~~text\n' + body
                                + '~~~\n\n' + specification)

    def test_policy_versions(self):
        good = examples()[0]
        policy = 'example-app@abcdef1234567890abcdef1234567890abcdef12'
        for value in ('wiki/standards read 2026-09-20',
                      'example-org/example-app@' + 'a' * 40,
                      f'{policy} + wiki/standards read 2026-09-20'):
            with self.subTest(policy=value):
                parsed = parse_review_result(good.replace(
                    f'| Policy | {policy} |', f'| Policy | {value} |'))
                self.assertEqual(parsed['rows']['Policy'], value)


def posted(name):
    """A posted report rewritten in the multi-axis form, from its result on."""
    text = (POSTED / name).read_text()
    return text[text.index('\n## Review result\n') + 1:]


def rewrite_return(text, label, old, new):
    """Edit one retained return's text and give it the matching digest."""
    head, rest = text.split(f'### Reviewer return: {label}\n', 1)
    table, rest = rest.split('~~~text\n', 1)
    body, tail = rest.split('\n~~~\n', 1)
    body = body.replace(old, new)
    digest = hashlib.sha256((body + '\n').encode()).hexdigest()
    table = re.sub(r'sha256:[0-9a-f]{64}', 'sha256:' + digest, table)
    return (f'{head}### Reviewer return: {label}\n{table}~~~text\n{body}'
            f'\n~~~\n{tail}')


class SharedFindingTest(unittest.TestCase):
    """Issue #102: one finding lists every axis that raised it."""

    REPORTS = {'pr96-final-1.md': ['71-F1'],
               'pr97-final-1.md': ['83-F1', '83-F4', '83-F7'],
               'pr100-final-2.md': ['99-F1', '99-F2', '99-F6']}

    def test_posted_reports_parse_in_the_multi_axis_form(self):
        self.assertEqual(sorted(p.name for p in POSTED.iterdir()),
                         sorted(self.REPORTS))
        for name, shared in self.REPORTS.items():
            with self.subTest(report=name):
                result = parse_review_result(posted(name))
                rows = result['rows']
                self.assertEqual((rows['Standards'], rows['Specification']),
                                 ('action-required', 'action-required'))
                both = [f[0] for f in result['findings']
                        if f[2] == ['standards', 'specification']]
                self.assertEqual(both, shared)
                blockers = [f for f in result['findings']
                            if f[1] != 'P3' and f[3] in OPEN]
                self.assertEqual(len(blockers), 1)
                self.assertIn('P2 1;', rows['Open findings'])
                self.assertEqual(len(result['returns']), 2)

    def test_one_axis_workaround_fails(self):
        for name, shared in self.REPORTS.items():
            blocker = next(i for i in shared if f'{i} (P2,' in posted(name))
            with self.subTest(report=name), self.assertRaisesRegex(
                    ValueError, 'Specification action-required without'):
                parse_review_result(posted(name).replace(
                    f'{blocker} (P2, standards+specification,',
                    f'{blocker} (P2, standards,'))

    def test_rejects_known_bad_shared_findings(self):
        good = posted('pr96-final-1.md')
        shared = '71-F1 (P2, standards+specification, unresolved)'
        mutations = {
            'shared blocker missing from one return': (
                rewrite_return(good, 'specification-reviewer-1',
                               'execution-recommendations.md',
                               'another-reference.md'),
                '71-F1 lists specification, but no specification return'),
            'shared blocker counted twice': (
                good.replace('P0 0; P1 0; P2 1;', 'P0 0; P1 0; P2 2;'),
                'P2 count disagrees'),
            'unknown axis': (
                good.replace(shared, shared.replace('+specification',
                                                    '+specifcation')),
                'unknown axis'),
            'specialist axis without its reviewer': (
                good.replace(shared, shared.replace('+specification',
                                                    '+security')),
                'unknown axis'),
            'axis listed twice': (
                good.replace(shared, shared.replace('+specification',
                                                    '+standards')),
                'axis twice'),
            'both as a listed axis': (
                good.replace(shared, shared.replace('+specification',
                                                    '+both')),
                'never both'),
            'spaced finding ID': (
                good.replace('- 71-F1 (', '- 71 F1 ('), 'bad finding'),
        }
        self.assertIn(shared, good)
        for name, (mutated, message) in mutations.items():
            with self.subTest(mutation=name):
                self.assertNotEqual(mutated, good)
                with self.assertRaisesRegex(ValueError, message):
                    parse_review_result(mutated)

    def test_resolved_shared_finding_needs_both_returns(self):
        # Fix verification: 99-F2 is resolved in final 2 on both axes, so
        # each axis's final 2 return must reassess README.md.
        good = posted('pr100-final-2.md')
        self.assertIn('99-F2 (P3, standards+specification, resolved)', good)
        for label, axis in (('standards-reviewer-1', 'standards'),
                            ('specification-reviewer-1', 'specification')):
            with self.subTest(axis=axis), self.assertRaisesRegex(
                    ValueError, f'99-F2 lists {axis}, but no {axis} return'):
                parse_review_result(rewrite_return(good, label, 'README',
                                                   'OVERVIEW'))


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
        self.assertIn('### Update the installed catalog', readme)
        self.assertIn('Explicit `$review-work`', readme)

    def test_scenario_cases_match_graders(self):
        scenarios = (SKILL / 'references/validation-scenarios.md').read_text()
        delivery = (SKILLS / 'deliver-work/references/validation-scenarios.md'
                    ).read_text()
        for name, prefix in (('review-work', 'RW'), ('review-evidence', 'RE')):
            with self.subTest(fixture=name):
                cases = (FIXTURES / f'{name}-cases.md').read_text()
                graders = (FIXTURES / f'{name}-graders.md').read_text()
                case_ids = re.findall(rf'^## ({prefix}\d+):', cases, re.MULTILINE)
                grader_ids = re.findall(rf'^\| ({prefix}\d+) \|', graders,
                                        re.MULTILINE)
                self.assertTrue(case_ids)
                self.assertEqual(case_ids, grader_ids)
                for reference in (scenarios, delivery):
                    self.assertIn(f'{name}-cases.md', reference)
                    self.assertIn(f'{name}-graders.md', reference)


def claude_profile(path):
    match = re.fullmatch(r'---\n(.*?)\n---\n\n(.+)', path.read_text(), re.DOTALL)
    return yaml.safe_load(match.group(1)), match.group(2)


class ReviewerProfileTest(unittest.TestCase):
    ASSETS = SKILL / 'assets'
    CLAUDE = {'review-work-reviewer': None, 'review-work-reviewer-high': 'high'}

    def test_profile_set_is_exact(self):
        shipped = sorted(path.relative_to(self.ASSETS).as_posix()
                         for path in self.ASSETS.rglob('*') if path.is_file())
        self.assertEqual(shipped, [
            'claude-code/review-work-reviewer-high.md',
            'claude-code/review-work-reviewer.md',
            'codex/review-work-reviewer.toml'])

    def test_claude_profiles_restrict_tools_and_differ_only_in_effort(self):
        bodies = set()
        for name, effort in self.CLAUDE.items():
            with self.subTest(profile=name):
                meta, body = claude_profile(self.ASSETS / f'claude-code/{name}.md')
                bodies.add(body)
                expected = {'name', 'description', 'tools', 'skills'}
                self.assertEqual(set(meta), expected | ({'effort'} if effort else set()))
                self.assertEqual(meta['name'], name)
                self.assertEqual(meta.get('effort'), effort)
                self.assertIn('review-work', meta['description'])
                # No Agent, editing, Skill or MCP tools; no model, permission
                # mode, isolation or background override.
                self.assertEqual(meta['tools'].split(', '),
                                 ['Read', 'Grep', 'Glob', 'Bash'])
                self.assertEqual(meta['skills'], ['code-review'])
        self.assertEqual(len(bodies), 1)

    def test_codex_profile_leaves_selection_to_the_spawn_call(self):
        profile = tomllib.loads(
            (self.ASSETS / 'codex/review-work-reviewer.toml').read_text())
        self.assertEqual(set(profile), {'name', 'description', 'sandbox_mode',
                                        'developer_instructions', 'agents'})
        self.assertEqual(profile['name'], 'review_work_reviewer')
        self.assertEqual(profile['sandbox_mode'], 'read-only')
        self.assertEqual(profile['agents'], {'enabled': False})
        _, body = claude_profile(self.ASSETS / 'claude-code/review-work-reviewer.md')
        self.assertEqual(profile['developer_instructions'].strip(), body.strip())

    def test_adapters_link_their_profiles(self):
        for adapter, host in (('claude-code-reviewers.md', 'claude-code'),
                              ('codex-reviewers.md', 'codex')):
            path = SKILL / 'references' / adapter
            with self.subTest(adapter=adapter):
                targets = {(path.parent / link).resolve() for link in links(path)}
                for asset in (self.ASSETS / host).iterdir():
                    self.assertIn(asset.resolve(), targets)
                self.assertIn('reviewer-execution.md', links(path))
                self.assertIn('| Impact | Reviewer default |', path.read_text())

    def test_execution_cases_match_graders(self):
        cases = (FIXTURES / 'reviewer-execution-cases.md').read_text()
        graders = (FIXTURES / 'reviewer-execution-graders.md').read_text()
        case_ids = re.findall(r'^## (RX\d+):', cases, re.MULTILINE)
        self.assertTrue(case_ids)
        self.assertEqual(case_ids,
                         re.findall(r'^\| (RX\d+) \|', graders, re.MULTILINE))
        scenarios = (SKILL / 'references/validation-scenarios.md').read_text()
        self.assertIn('reviewer-execution-cases.md', scenarios)
        self.assertIn('reviewer-execution-graders.md', scenarios)


def reviewer_table(adapter):
    """Return (condition, default) rows of a host adapter's reviewer table."""
    text = (SKILL / 'references' / adapter).read_text()
    table = text.split('| Impact | Reviewer default |', 1)[1].split('\n\n', 1)[0]
    rows = [line.split(' | ') for line in table.splitlines()[2:]]
    return [(cells[0].lstrip('| '), cells[1]) for cells in rows]


class ReviewerSelectionTest(unittest.TestCase):
    """Issue #71: reviewers follow the review task as well as impact."""

    def test_cross_interface_work_gets_sol_reviewers_at_low_impact(self):
        # Hub #278: low impact, several interfaces, a Sol-level implementation.
        rows = reviewer_table('codex-reviewers.md')
        below_high = [row for row in rows if row[0].startswith('Low or medium')]
        self.assertEqual(len(below_high), 2, below_high)
        matches = [default for condition, default in below_high
                   if 'interfaces' in condition]
        self.assertEqual(len(matches), 1)
        self.assertIn('Sol (`gpt-6-sol`) at `high` or stronger', matches[0])
        self.assertNotIn('luna', matches[0].lower())

    def test_luna_reviewers_are_limited_to_bounded_work(self):
        rows = reviewer_table('codex-reviewers.md')
        luna = [(condition, default) for condition, default in rows
                if 'gpt-6-luna' in default]
        self.assertEqual(len(luna), 1)
        condition, default = luna[0]
        for requirement in ('bounded review task', 'Luna-level implementation',
                            'settled requirements', 'reliable checks'):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, condition)
        self.assertNotIn('interfaces', condition)
        # The pre-#71 row selected Luna for every low- or medium-impact change.
        self.assertNotEqual(condition, 'Low or medium impact')

    def test_high_impact_floor_is_unchanged(self):
        rows = reviewer_table('codex-reviewers.md')
        high = [default for condition, default in rows
                if condition.startswith('High impact, even with a tiny diff')]
        self.assertEqual(high, ['Strongest evidenced relevant choice of Sol '
                                '(`gpt-6-sol`) at `high` or Astra '
                                '(`gpt-6-astra`) at `high`'])

    def test_claude_code_default_stays_opus(self):
        rows = reviewer_table('claude-code-reviewers.md')
        self.assertEqual(rows[0][0], 'Low or medium impact')
        self.assertEqual(rows[0][1], '`opus` for each axis')
        for _, default in rows:
            self.assertNotIn('sonnet', default.split('.')[0].lower())

    def test_review_selection_states_the_rule(self):
        text = ' '.join((SKILL / 'references/review-selection.md')
                        .read_text().split())
        for rule in ('Impact sets the minimum; the review task can only raise it',
                     'select that tier or stronger, even at low or medium impact',
                     'a stronger implementer than the work needed raises '
                     'nothing, and a weaker one lowers nothing',
                     'not an automatic equivalent of a larger one',
                     'task, fix-verification and final reviewers',
                     'Selection changes no reviewer count, frozen comparison, '
                     'scope, or specialist or human gate',
                     'Evidence never goes below the impact floor',
                     "in the input's Settings field"):
            with self.subTest(rule=rule):
                self.assertIn(rule, text)
        self.assertNotIn('## Start from impact', text)

    def test_selection_cases_match_graders(self):
        cases = (FIXTURES / 'reviewer-selection-cases.md').read_text()
        graders = (FIXTURES / 'reviewer-selection-graders.md').read_text()
        case_ids = re.findall(r'^## (RS\d+):', cases, re.MULTILINE)
        rows = dict(re.findall(r'^\| (RS\d+) \| ([^|]+) \|', graders,
                               re.MULTILINE))
        self.assertTrue(case_ids)
        self.assertEqual(case_ids, list(rows))
        criteria = {c for value in rows.values() for c in value.split(', ')}
        self.assertEqual(criteria, {'A1', 'A2', 'A3', 'A4', 'A5'})
        self.assertIn('example/hub#278', cases)
        grader_rows = {row.split(' | ')[0].lstrip('| '): row for row in
                       graders.splitlines() if row.startswith('| RS')}
        self.assertIn('Luna for either axis fails the case', grader_rows['RS01'])
        self.assertIn('Luna reviewers for Codex fail the case',
                      grader_rows['RS02'])
        # A Fable or Astra start does not select Fable or Astra reviewers.
        self.assertIn('Fable reviewers fail the case', grader_rows['RS07'])
        self.assertIn('choosing Astra because the start is Astra fails',
                      grader_rows['RS07'])
        for skill in ('review-work', 'plan-work'):
            scenarios = (SKILLS / skill / 'references/validation-scenarios.md'
                         ).read_text()
            with self.subTest(skill=skill):
                self.assertIn('reviewer-selection-cases.md', scenarios)
                self.assertIn('reviewer-selection-graders.md', scenarios)


def load_tests(loader, tests, pattern):
    spec = importlib.util.spec_from_file_location(
        'review_process_tests', ROOT / 'tests/review-process-test.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    tests.addTests(loader.loadTestsFromModule(module))
    return tests


if __name__ == '__main__':
    unittest.main()
