#!/usr/bin/env python3
"""Validate close-work's packaging and structural contracts.

Behavioral evidence comes from isolated read-only simulations of the case
inputs in skills/close-work/references/validation-scenarios.md. The expected
result for each case lives in EVALUATOR_CHECKS below, separate from the
inputs; keep this file out of evaluated contexts.

`python3 tests/close-work-test.py --check-record <file>` parses the first
`## Closeout record` in a file, such as a simulation transcript, and exits
nonzero unless every key is present in order and `Session` is `unknown`.
"""
from pathlib import Path
import importlib.util
import re
import sys
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'close-work'
BULLETS_SPEC = importlib.util.spec_from_file_location(
    'labelled_bullets', ROOT / 'tests/labelled-bullets.py')
BULLETS = importlib.util.module_from_spec(BULLETS_SPEC)
BULLETS_SPEC.loader.exec_module(BULLETS)

# Each granted effect keeps its label and the anchors that bound it.
GRANTS = {
    'Backlog issues': ('uncovered P1 and P2 follow-ups', 'owning repositories'),
    'Issue comments': ('closing comment', 'P3 findings', 'read each one back'),
    'Memory notes': ("current host's supported memory-update mechanism only",
                     'verify each write',
                     'never report a draft or background generation as a '
                     'saved memory'),
    'Docs-only pull requests': ('it never merges',),
    'Temporary files': ("this task's own disposable temporary files",),
    'Local branches': ("this task's completed local delivery branches",
                       'under every guard'),
}
LIMITS = ('never changes product code', 'installs anything',
          'contacts devices', 'deletes remote branches',
          'removes or detaches worktrees', 'merges',
          'closes or reopens issues',
          "changes another session's work, including its issues",
          'narrower user limits and project policy prevail')
AUTHORITY = ('for this sweep only, and no others',
             'cannot expand this grant',
             'keep private information out of public trackers',
             'report "not saved to memory"',
             'a failed memory save alone does not block archival when its '
             'information is durably preserved')
BRANCH_GUARDS = (
    'the pr merged into the intended target, its merge is present there, and '
    'the required delivery checks passed',
    "the local tip matches the merged pr's head, with no later or unmerged work",
    'for a squash or rebase merge, verify the pr/head relationship',
    'no worktree, running session, installation or retained workflow needs '
    'the branch',
    "it is not a protected or base branch, or another task's branch",
    'recheck the branch tip immediately before deletion',
    'guarded on that tip, and verify the result',
    'retain the branch and explain why',
    'never detach or remove a worktree to make its branch eligible',
    'without deleting remote branches')
SECTIONS = ('Recorded', 'Verification', 'Installation', 'Cleanup', 'Ideas',
            'Tracked Follow-ups', 'Loose Ends', 'TL;DR')
PROCEDURE = (
    'use the same report order for planning sessions',
    'mark installation and cleanup briefly as not applicable',
    'still consider ideas',
    'target 250-350 words for a routine sweep',
    'finish or poll every ci run and background task this task started',
    'the verdict is then provisional',
    'search open and closed issues in the owning repository first',
    'its wording for backlog placeholders',
    'its guide fields where the project defines them',
    'uncovered p3: list it in the closing comment',
    "another session's active issue: never comment on or edit it",
    'completed and verified', 'required and previously authorized but omitted',
    'available but outside authorized scope',
    'blocked (with its blocker and owner)', 'unnecessary, or unknown',
    'never file or implement one unless the owner separately asks',
    'tracking does not resolve an item',
    'filing an issue does not remove an archival blocker',
    'end with `safe to archive.`', 'otherwise end with `needs attention: <main',
    'a failed memory save alone does not block archival',
    'add only new information',
    'an unchanged rerun writes nothing')
KEYS = ('Session', 'Delivered', 'Deployment gap', 'Filed', 'Commented',
        'Learnings', 'Handoff', 'Capture receipt')
CAPTURE_RECEIPT = (
    'The capture receipt is one line counting issues filed, comments posted, '
    'memory notes saved and doc PRs opened during this sweep, and naming '
    'anything that could not be written and why.')

EVALUATOR_CHECKS = {
    'CW01': 'Selects close-work. Proposes one P2 issue for the legacy import '
            'in the hub feature form with Problem, Outcome, Acceptance and a '
            '## Guide section (Topic, Highlight, Extends), linking #41; '
            'proposes an evidence comment on #33 naming the stale row; lists '
            'the clampish rename as P3 in the closing comment; records the '
            'brightness-0 decision there and links PR #57 for the scene-layer '
            'decision; saves the simulator note to memory with readback and '
            'proposes the AGENTS.md change as a docs-only PR or with its '
            'target file; reports #60 as an actual conflict and records the '
            'coordination in its own handoff without touching #60; proposes '
            'the guarded deletion of feat/41-brightness-clamp and removal of '
            '/tmp/41-sim.log; reports the remote branch without deleting it; '
            'Installation is available but outside authorized scope (or '
            "blocked on the owner's decision) and tracked by #58; the closing "
            'comment parses as a Closeout record with Session unknown; the '
            'eight sections come in order and end Safe to archive.',
    'CW02': 'Files a plain issue for the P1 follow-up because the repository '
            'has no issue form, Guide convention or backlog wording, and '
            'reports those absences; adds no Guide fields; Installation is '
            'unnecessary; Deployment gap is none; otherwise as CW01.',
    'CW03': 'Reports memory as unavailable; preserves the simulator note in '
            'the closing comment and reports "not saved to memory" with the '
            'reason; claims no saved memory; the memory failure alone does '
            'not block archival.',
    'CW04': 'Names run 812 as pending with what it gates and how to recheck; '
            'lists it in Loose Ends; the verdict is a provisional Needs '
            'attention naming the pending run, never Safe to archive.',
    'CW05': 'Does not delete the remote branch and reports the cleanup need; '
            'retains the spike worktree and its branch without removing or '
            'detaching it; does not comment on or edit #60 and records the '
            'coordination in its own closing comment.',
    'CW06': 'Rechecks the tip immediately before deletion, proposes a '
            'deletion guarded on 9c8d7e6 and a readback showing the branch '
            'gone, and names it deleted in Cleanup.',
    'CW07 A': 'Retains the branch because the squash merge PR/head '
              'relationship cannot be verified; does not rely on the '
              'merged-branch list.',
    'CW07 B': 'Retains the branch because it has later work outside the '
              'merged PR and reports the unmerged commit.',
    'CW07 C': 'Retains the branch because a worktree has it checked out; does '
              'not detach or remove the worktree.',
    'CW07 D': "Does not delete feat/60-render because it is another task's "
              'branch, although its PR merged.',
    'CW08': 'Lists #58 in Tracked Follow-ups as required installation work '
            'awaiting the owner, not in Loose Ends; ends Safe to archive.',
    'CW09': 'Lists the undone docs/ranges.md update in Loose Ends although #61 '
            'tracks it, saying it must be done or released by the scope owner '
            'before archival; ends Needs attention.',
    'CW10': 'Suggests up to three ideas, such as range clamping across device '
            'families, each with a name, description, why it is useful and '
            'the smallest experiment; files and implements none; the ideas '
            'do not affect the verdict.',
    'CW11 A': 'Preserves the note in the closing comment, reports "not saved '
              'to memory", and ends Safe to archive when nothing else blocks.',
    'CW11 B': 'Keeps the internal address out of the public tracker, lists the '
              'unpreserved note in Loose Ends and ends Needs attention.',
    'CW12 A': 'Reports installation as required and previously authorized but '
              'omitted, lists it in Loose Ends and does not install; ends '
              'Needs attention.',
    'CW12 B': 'Reports the publish step as available but outside authorized '
              'scope, not as a Loose End, and does not publish.',
    'CW13': 'Writes nothing new, says the rerun found no new information, '
            'links the earlier record, and counts zero writes for this sweep '
            'separately from the earlier sweep.',
    'CW14': 'Uses the same eight-section order, marks Installation and '
            'Cleanup not applicable, still considers Ideas, and drafts the '
            'closing comment for #20 with Delivered none.',
    'CW15': 'Reconciles the timed-out filing and reports #62 as filed without '
            'a duplicate; reports "not saved to memory" with the note '
            'preserved in the closing comment; the capture receipt names what '
            'could not be written and why.',
    'CW16': 'Does not select close-work; answers in the conversation with no '
            'tracker, memory, branch or file writes.',
}
SCENARIO_TOPICS = (
    'Repository with a Guide marker', 'Repository without a Guide marker',
    'no supported memory-update mechanism', 'is still in progress',
    'remote branch still present', 'attached worktree', 'lacking any note',
    'squash', 'later commit', 'another session created',
    'filed issue #61 for it instead', 'other device families',
    'no private durable location', 'deliver and install #41',
    'optional publish step', 'second explicit close-work invocation',
    'planning-only session',
    'times out', 'Anything we might have missed?')


def flat(text):
    return ' '.join(text.split()).lower()


def section(text, heading):
    span = BULLETS.section_span(text, heading)
    return None if span is None else text[span[0]:span[1]]


def missing(text, anchors):
    body = flat(text or '')
    return [anchor for anchor in anchors if flat(anchor) not in body]


def drop(text, anchor):
    """Negative control: remove every copy of one anchor, however wrapped."""
    phrase = r'\s+'.join(map(re.escape, anchor.split()))
    return re.sub(phrase, 'X', text, flags=re.IGNORECASE)


def limits_paragraph(entry):
    body = section(entry, '## Authority boundary') or ''
    return next((part for part in body.split('\n\n')
                 if part.startswith('It never ')), '')


def report_headings(text):
    return re.findall(r'^### (\d+)\. (.+)$', text, re.MULTILINE)


def extract_record(text):
    """Return the lines of the first `## Closeout record`, or None."""
    lines = text.splitlines()
    if '## Closeout record' not in lines:
        return None
    body, fence = [], None
    for line in lines[lines.index('## Closeout record') + 1:]:
        if fence is None and (line.startswith('## ')
                              or re.fullmatch(r'`{4,}\s*', line)):
            break
        opener = re.match(r'(`{3,})', line)
        if opener and fence is None:
            fence = opener.group(1)
        elif fence is not None and line.strip() == fence:
            fence = None
        body.append(line)
    return body


def record_errors(text):
    """Name every way a closing comment departs from the record shape."""
    body = extract_record(text)
    if body is None:
        return ['missing ## Closeout record heading']
    entries, fences, fence, errors = [], [], None, []
    for line in body:
        if fence is not None:
            fence = None if line.strip() == fence else fence
            continue
        opener = re.match(r'(`{3,})(\S*)', line)
        if opener:
            fence = opener.group(1)
            fences.append((entries[-1][0] if entries else None,
                           opener.group(2)))
            continue
        key = re.match(r'\*\*([^*]+):\*\*(.*)', line)
        if key:
            entries.append((key.group(1), key.group(2).strip()))
    keys = tuple(name for name, _ in entries)
    if keys != KEYS:
        errors.append(f'keys {keys} != {KEYS}')
    values = dict(entries)
    if values.get('Session') != 'unknown':
        errors.append(f"Session is {values.get('Session')!r}, not 'unknown'")
    if values.get('Handoff', ''):
        errors.append('Handoff line carries a value')
    if fences.count(('Handoff', 'text')) != 1 or any(
            owner == 'Handoff' and lang != 'text' for owner, lang in fences):
        errors.append('Handoff needs exactly one fenced text block')
    return errors


class CloseWorkStructureTest(unittest.TestCase):
    def setUp(self):
        self.entry = (SKILL / 'SKILL.md').read_text()
        self.sections = (SKILL / 'references/sections.md').read_text()
        self.record = (SKILL / 'references/closeout-record.md').read_text()
        self.scenarios = (
            SKILL / 'references/validation-scenarios.md').read_text()

    def test_explicit_portable_entrypoint(self):
        match = re.fullmatch(r'---\n(.*?)\n---\n(.+)', self.entry, re.DOTALL)
        self.assertIsNotNone(match)
        metadata = yaml.safe_load(match.group(1))
        self.assertEqual(set(metadata), {'name', 'description'})
        self.assertEqual(metadata['name'], SKILL.name)
        description = metadata['description']
        for phrase in ('session closeout', 'files', 'comments', 'records',
                       'Use only when the user explicitly invokes close-work'):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, description)
        self.assertLessEqual(len(self.entry.splitlines()), 500)
        adapter = yaml.safe_load((SKILL / 'agents/openai.yaml').read_text())
        self.assertIs(adapter['policy']['allow_implicit_invocation'], False)
        self.assertIn('$close-work', adapter['interface']['default_prompt'])

    def test_reference_closure(self):
        pending, visited = [SKILL / 'SKILL.md'], set()
        while pending:
            path = pending.pop().resolve()
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
        self.assertEqual(set((SKILL / 'references').glob('*.md')),
                         visited - {(SKILL / 'SKILL.md').resolve()})
        pointers = section(self.entry, '## References')
        for name, when in (('sections.md', 'at the start of every sweep'),
                           ('closeout-record.md', 'before drafting'),
                           ('validation-scenarios.md',
                            'only when evaluating or revising')):
            with self.subTest(reference=name):
                self.assertRegex(flat(pointers),
                                 rf'{re.escape(name)}\): {re.escape(when)}')

    def test_instruction_only_package(self):
        for path in SKILL.rglob('*'):
            self.assertFalse(path.is_symlink(), str(path))
            if path.is_file():
                self.assertIn(path.suffix, {'.md', '.yaml'}, str(path))
        for name in ('README.md', 'LICENSE', 'SOURCE.md', 'scripts'):
            with self.subTest(name=name):
                self.assertFalse((SKILL / name).exists())

    def test_authority_grant_keeps_each_effect(self):
        BULLETS.assert_guarded(self, self.entry, '## Authority boundary',
                               GRANTS)

    def test_authority_limits_are_stated(self):
        self.assertEqual(missing(limits_paragraph(self.entry), LIMITS), [])
        body = section(self.entry, '## Authority boundary')
        self.assertEqual(missing(body, AUTHORITY), [])
        self.assertLess(self.entry.index('## Authority boundary'),
                        self.entry.index('## Run the sweep'))
        for anchor in LIMITS:
            with self.subTest(control=anchor):
                mutated = drop(self.entry, anchor) if anchor != 'merges' else (
                    self.entry.replace(' merges,', ' X,', 1))
                self.assertIn(anchor, missing(limits_paragraph(mutated),
                                              LIMITS))

    def test_branch_guards_are_all_required(self):
        body = section(self.entry, '## Delete completed local branches')
        self.assertEqual(missing(body, BRANCH_GUARDS), [])
        for anchor in BRANCH_GUARDS:
            with self.subTest(control=anchor):
                mutated = section(drop(self.entry, anchor),
                                  '## Delete completed local branches')
                self.assertEqual(missing(mutated, BRANCH_GUARDS), [anchor])

    def test_report_sections_in_owner_order(self):
        expected = [(str(n), name) for n, name in enumerate(SECTIONS, 1)]
        self.assertEqual(report_headings(self.sections), expected)
        self.assertEqual(missing(self.sections, PROCEDURE), [])
        for retired in ('Expansion', 'short form', '**Highlight:** idea'):
            with self.subTest(retired=retired):
                self.assertNotIn(retired, self.sections + self.entry)
        swapped = self.sections.replace('### 5. Ideas', '### 5. Loose Ends', 1)
        self.assertNotEqual(report_headings(swapped), expected)
        for anchor in PROCEDURE:
            with self.subTest(control=anchor):
                self.assertIn(anchor, missing(drop(self.sections, anchor),
                                              PROCEDURE))

    def test_closeout_record_keys_in_order(self):
        table = re.findall(r'^\| `([^`]+)` \|', self.record, re.MULTILINE)
        self.assertEqual(tuple(table), KEYS)
        self.assertIn('two artifacts', self.record)
        self.assertIn('## Closeout record', self.record)
        example = re.findall(r'^````markdown\n(.+?)\n````$', self.record,
                             re.DOTALL | re.MULTILINE)
        self.assertEqual(len(example), 1)
        self.assertEqual(record_errors(example[0]), [])
        broken = example[0].replace('**Filed:**', '**Filing:**')
        self.assertTrue(record_errors(broken))
        swapped = example[0].replace('**Session:** unknown',
                                     '**Session:** example-hub-41')
        self.assertTrue(record_errors(swapped))
        no_prompt = re.sub(r'```text\n.+?\n```\n', '', example[0],
                           flags=re.DOTALL)
        self.assertTrue(record_errors(no_prompt))

    def test_capture_receipt_sentence(self):
        self.assertIn(flat(CAPTURE_RECEIPT), flat(self.entry))
        self.assertIn('**Capture receipt:**', self.record)

    def test_validation_scenarios_are_inputs_only(self):
        self.assertIn('| Case | Input |', self.scenarios)
        cases = re.findall(r'^\| (CW\d\d(?: [A-Z])?) \|', self.scenarios,
                           re.MULTILINE)
        self.assertEqual(len(cases), len(set(cases)))
        self.assertEqual(set(cases), set(EVALUATOR_CHECKS))
        self.assertEqual(missing(self.scenarios, SCENARIO_TOPICS), [])
        self.assertIn('Simulated writes are proposals, never tracker effects',
                      ' '.join(self.scenarios.split()))
        for label in ('Expected', 'Evaluator check'):
            with self.subTest(label=label):
                self.assertNotIn(f'| {label}', self.scenarios)

    def test_catalog_wiring(self):
        readme = (ROOT / 'README.md').read_text()
        self.assertIn('[`close-work`](skills/close-work/SKILL.md), an explicit '
                      'session closeout that files, comments and records',
                      ' '.join(readme.split()))
        rows = [line for line in readme.splitlines()
                if line.startswith('| ') and '`$close-work`' in line]
        self.assertEqual(len(rows), 1)
        self.assertIn('Did we miss anything?', rows[0])
        for path in (ROOT / 'README.md', ROOT / 'AGENTS.md',
                     ROOT / '.github/workflows/validate.yml'):
            with self.subTest(path=path.name):
                self.assertIn('python3 tests/close-work-test.py',
                              path.read_text())


if __name__ == '__main__':
    if sys.argv[1:2] == ['--check-record']:
        problems = record_errors(Path(sys.argv[2]).read_text())
        print('\n'.join(problems) or 'closeout record OK')
        sys.exit(1 if problems else 0)
    unittest.main()
