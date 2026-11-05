#!/usr/bin/env python3
"""Validate packaging contracts; behavioral evidence uses isolated scenarios."""
from pathlib import Path
import importlib.util
import re
import unittest
import sys

sys.dont_write_bytecode = True
import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'plan-work'
BULLETS_SPEC = importlib.util.spec_from_file_location(
    'labelled_bullets', ROOT / 'tests/labelled-bullets.py')
BULLETS = importlib.util.module_from_spec(BULLETS_SPEC)
BULLETS_SPEC.loader.exec_module(BULLETS)

# Each protection class keeps its label and the anchors that carry its core
# commitment; any other wording may change. A weakened sentence that keeps its
# anchors passes, so inspection and review cover the rest.
BOUNDARIES = {
    'Authority': ('does not authorize publication',
                  'neither mode starts implementation'),
    'Existing systems': ("project's tracker", 'create no tracker'),
    'Shared resources': ('report the gap', 'never silently install'),
    'Evidence': ('explicitly unexecuted', 'never becomes implemented behavior'),
}


class PlanWorkStructureTest(unittest.TestCase):
    def test_explicit_portable_entrypoint(self):
        text = (SKILL / 'SKILL.md').read_text()
        match = re.fullmatch(r'---\n(.*?)\n---\n(.+)', text, re.DOTALL)
        self.assertIsNotNone(match)
        metadata = yaml.safe_load(match.group(1))
        self.assertEqual(set(metadata), {'name', 'description'})
        self.assertEqual(metadata['name'], SKILL.name)
        self.assertTrue(metadata['description'].strip())
        self.assertLessEqual(len(text.splitlines()), 500)
        adapter = yaml.safe_load((SKILL / 'agents/openai.yaml').read_text())
        self.assertIs(adapter['policy']['allow_implicit_invocation'], False)
        self.assertIn('$plan-work', adapter['interface']['default_prompt'])

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
        self.assertTrue(set((SKILL / 'references').glob('*.md')) <= visited)

    def test_canonical_shared_dependencies(self):
        for resource in ('references/work-assessment.md',
                         'references/model-selection.md',
                         'references/task-planning.md',
                         'references/corrections.md'):
            with self.subTest(resource=resource):
                self.assertTrue((ROOT / 'skills/deliver-work' / resource).is_file())
                self.assertFalse((SKILL / resource).exists())
                self.assertIn(resource, (SKILL / 'SKILL.md').read_text())

    def test_each_protection_class_keeps_its_commitment(self):
        BULLETS.assert_guarded(self, (SKILL / 'SKILL.md').read_text(),
                               '## Boundaries', BOUNDARIES)

    def test_instruction_only_package(self):
        for path in SKILL.rglob('*'):
            self.assertFalse(path.is_symlink(), str(path))
            if path.is_file():
                self.assertIn(path.suffix, {'.md', '.yaml'})


    def test_declared_installation_is_planned(self):
        entry = ' '.join((SKILL / 'SKILL.md').read_text().split())
        for rule in ('declares installation or deployment as a completion '
                     'condition', "the item's acceptance includes that step "
                     'and its readback by default', 'Record applicable request or '
                     'standing authority', "recommendation's `Checkpoints` row "
                     'names only uncovered owner decisions',
                     "use the project's declared opt-out or, by default, be "
                     'marked source-only, but only with a reason and a link to '
                     'the install issue', 'Write no blanket exclusion',
                     'Without a declaration, leave installation and deployment '
                     'out of the item'):
            with self.subTest(rule=rule):
                self.assertIn(rule, entry)
        reference = ' '.join(
            (SKILL / 'references/execution-recommendations.md').read_text().split())
        self.assertIn('including any uncovered authority for an installation or '
                      'deployment step in acceptance', reference)
        scenarios = (SKILL / 'references/validation-scenarios.md').read_text()
        self.assertIn('IC11 to IC13', scenarios)
        self.assertIn('installation-graders.md', scenarios)
        graders = (ROOT / 'tests/fixtures/workflow-evaluation/'
                   'installation-graders.md').read_text()
        rows = re.findall(r'^\| (IC1[1-3]) \| (P\d) \|', graders, re.MULTILINE)
        self.assertEqual(rows, [('IC11', 'P1'), ('IC12', 'P2'), ('IC13', 'P3')])

    def test_scenario_fixtures_exist(self):
        fixtures = ROOT / 'tests/fixtures/workflow-evaluation'
        scenarios = (SKILL / 'references/validation-scenarios.md').read_text()
        names = re.findall(r'`([^`\s]+\.md)`', scenarios)
        self.assertTrue(names)
        for name in names:
            if '*' in name:
                continue
            path = ROOT / name if '/' in name else fixtures / name
            with self.subTest(name=name):
                self.assertTrue(path.is_file())

    def assert_rubric_covers_every_case(self, stem):
        fixtures = ROOT / 'tests/fixtures/workflow-evaluation'
        cases = (fixtures / f'{stem}-cases.md').read_text()
        graders = (fixtures / f'{stem}-graders.md').read_text()
        self.assertIn(f'Do not read `{stem}-graders.md`', cases)
        expected = set()
        for number, body in re.findall(r'^## (\d+)\. .*?\n(.*?)(?=^## |\Z)',
                                       cases, re.DOTALL | re.MULTILINE):
            variants = re.findall(r'^- Variant ([A-Z]):', body, re.MULTILINE)
            expected |= ({f'{number} {v}' for v in variants} or {number})
        self.assertGreaterEqual(len(expected), 5)
        rows = set(re.findall(r'^\| (\d+(?: [A-Z])?) \|', graders, re.MULTILINE))
        self.assertEqual(rows, expected)

    def test_alignment_rubric_covers_every_case(self):
        self.assert_rubric_covers_every_case('alignment')

    def test_issue_refresh_rubric_covers_every_case(self):
        self.assert_rubric_covers_every_case('issue-refresh')

    def test_issue_refresh_route_keeps_its_limits(self):
        entry = ' '.join((SKILL / 'SKILL.md').read_text().split())
        self.assertIn('[issue refresh](references/issue-refresh.md)', entry)
        self.assertIn('read-only unless the user names the tracker effect', entry)
        self.assertIn('asks to refresh, reassess or prune existing work, '
                      'whatever its scope', entry)
        self.assertIn('Use only when the user explicitly invokes plan-work', entry)
        reference = ' '.join(
            (SKILL / 'references/issue-refresh.md').read_text().split())
        self.assertIn('](alignment.md)', reference)
        for rule in (
            'adds no schema, service, tracker field or backlog sweep',
            'this route needs a selection and write nothing',
            'Stale guidance never makes the requirement obsolete',
            'inspect the source and content paths that could already supply it',
            'Never remove a useful visible feature merely to simplify',
            'cannot establish that an issue is obsolete',
            '| Unknown | Evidence the comparison needs is missing',
            'evidence for one establishes no other',
            'generate no replacement',
            'A refresh request is read-only',
            'each needing its own name',
            'write nothing and report no change',
            'Keep the body and update time you assessed',
            'Reread just before writing',
            'Preserve unrelated content',
            'never overwrite it',
            "owner-set planning fields such as a Project's Phase or Commitment",
            'Read back the saved issue',
            'accepted change affects its outcome',
        ):
            with self.subTest(rule=rule):
                self.assertIn(rule, reference)
        fixtures = ROOT / 'tests/fixtures/workflow-evaluation'
        self.assertIn('synthetic and contain no personal transcript',
                      ' '.join((fixtures / 'issue-refresh-cases.md')
                               .read_text().split()))
        self.assertNotIn('| Criteria |',
                         (fixtures / 'issue-refresh-cases.md').read_text())
        for text in (reference, (fixtures / 'issue-refresh-cases.md').read_text()):
            self.assertNotRegex(text.lower(), r'b\.u\.n\.n\.y|bunny|device-hub')

    def test_uncertainty_routing_rubric_covers_every_case(self):
        self.assert_rubric_covers_every_case('uncertainty-routing')

    def test_uncertainty_routing_is_wired_and_composition_stays_explicit(self):
        deliver = ROOT / 'skills/deliver-work'
        routing = ' '.join((deliver / 'references/uncertainty-routing.md')
                           .read_text().split())
        for anchor in (
            'A routine, well-specified change skips this reference',
            'grants no authority',
            'Never ask the owner what inspection answers',
            'while a cheap decisive step is still missing',
            'the next decision each outcome leads to',
            'write the comparison brief that `architect` and `prototype` define',
            'An experiment needs authority for every effect its brief lists',
            'Never replace it with a silent installation, a copied script',
            'Loading a skill authorizes no launch, installation or device use',
            "use the project's documented alternative",
            'Keep refuted and inconclusive outcomes',
            'Never extend the bound or rerun silently',
        ):
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, routing)
        self.assertIn('This reference only uses those entrypoints and maps.', routing)
        self.assertIn('read [verification maintenance](verification-maintenance.md)',
                      routing)
        link = '](uncertainty-routing.md)'
        self.assertIn(link, (deliver / 'references/work-assessment.md').read_text())
        self.assertIn('](references/uncertainty-routing.md)',
                      (deliver / 'SKILL.md').read_text())
        self.assertIn('`references/uncertainty-routing.md`',
                      (SKILL / 'SKILL.md').read_text())
        for name, explicit in (
            ('prototype', 'Use only when the user directly invokes prototype'),
        ):
            with self.subTest(skill=name):
                root = ROOT / 'skills' / name
                text = (root / 'SKILL.md').read_text()
                description = yaml.safe_load(text.split('---')[1])['description']
                self.assertIn(explicit, description)
                self.assertIn('an authorized workflow deliberately composes it',
                              description)
                self.assertIn('composition adds no authority', ' '.join(text.split()))
                adapter = yaml.safe_load((root / 'agents/openai.yaml').read_text())
                self.assertIs(adapter['policy']['allow_implicit_invocation'], False)

    def test_execution_choice_cases_have_separate_graders(self):
        fixtures = ROOT / 'tests/fixtures/workflow-evaluation'
        cases = (fixtures / 'execution-choice-cases.md').read_text()
        graders = (fixtures / 'execution-choice-graders.md').read_text()
        ids = re.findall(r'^## (EC\d+):', cases, re.MULTILINE)
        self.assertEqual(ids, [f'EC{n:02d}' for n in range(1, 11)])
        self.assertEqual(ids, re.findall(r'^\| (EC\d+) \|', graders, re.MULTILINE))
        self.assertNotIn('| Required behavior |', cases)
        for name in ('plan-work', 'deliver-work', 'review-work'):
            scenario = (ROOT / 'skills' / name / 'references/validation-scenarios.md').read_text()
            self.assertIn('execution-choice-cases.md', scenario)
            self.assertIn('execution-choice-graders.md', scenario)

    def test_check_wiring(self):
        for path in (ROOT / 'README.md', ROOT / 'AGENTS.md',
                     ROOT / '.github/workflows/validate.yml'):
            self.assertIn('python3 tests/plan-work-test.py', path.read_text())


if __name__ == '__main__':
    unittest.main()
