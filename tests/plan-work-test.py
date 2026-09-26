#!/usr/bin/env python3
"""Validate packaging contracts; behavioral evidence uses isolated scenarios."""
from pathlib import Path
import re
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'plan-work'


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
                         'references/review-cycles.md'):
            with self.subTest(resource=resource):
                self.assertTrue((ROOT / 'skills/deliver-work' / resource).is_file())
                self.assertFalse((SKILL / resource).exists())
                self.assertIn(resource, (SKILL / 'SKILL.md').read_text())

    def test_instruction_only_package(self):
        for path in SKILL.rglob('*'):
            self.assertFalse(path.is_symlink(), str(path))
            if path.is_file():
                self.assertIn(path.suffix, {'.md', '.yaml'})

    def test_execution_recommendation_shape(self):
        reference = (SKILL / 'references/execution-recommendations.md').read_text()
        entry = (SKILL / 'SKILL.md').read_text()
        scenarios = (SKILL / 'references/validation-scenarios.md').read_text()
        for session_type in ('One-shot', 'Pair', 'Orchestrate',
                             'Investigate first'):
            with self.subTest(session_type=session_type):
                self.assertIn(f'| `{session_type}` |', reference)
                self.assertIn(f'`{session_type}`', entry)
                self.assertIn(f'`{session_type}`', scenarios)
        for label in ('**Start with:**', '**Prompt (Claude Code):**',
                      '**Prompt (Codex):**', '**Cheaper start:**',
                      '**Cheaper prompt (Claude Code):**',
                      '**Cheaper prompt (Codex):**', '**Why:**',
                      '**Reassess when:**', '**Assessed:**',
                      '**Status:** insufficient', '**Missing:**'):
            with self.subTest(label=label):
                self.assertIn(label, reference)
        for row in ('Model', 'Thinking level', 'Session type', 'Subagents',
                    'Reviewers', 'Availability', 'Checkpoints'):
            with self.subTest(row=row):
                self.assertIn(f'`{row}`', reference)
        self.assertIn('| Work to start | Claude Code model / effort | '
                      'Codex model / reasoning | Session role |', reference)
        prompts = re.findall(r'```text\n(.+?)\n```', reference, re.DOTALL)
        self.assertEqual(len(prompts), 1)
        prompt = prompts[0]
        self.assertTrue(prompt.endswith(
            "If deliver-work isn't available here, say so and stop."))
        self.assertIn('stop if it is not', prompt)
        self.assertIn('take the effort as stated rather than guessing it', prompt)
        self.assertIn('Execution recommendation (assessed', prompt)
        self.assertIn('without worker subagents', prompt)
        self.assertRegex(prompt, r'two fresh read-only \w+ reviewers')
        self.assertNotIn('without subagents', prompt)
        self.assertNotRegex(prompt.lower(), r'(report|verify|confirm)\w* (your|its) effort')

    def test_work_surface_line(self):
        reference = (SKILL / 'references/execution-recommendations.md').read_text()
        entry = (SKILL / 'SKILL.md').read_text()
        scenarios = (SKILL / 'references/validation-scenarios.md').read_text()
        values = ('UI', 'Backend', 'Unknown')
        for value in values:
            with self.subTest(value=value):
                self.assertIn(f'| `{value}` |', reference)
                self.assertIn(f'`{value}`', entry)
                self.assertIn(f'**Work surface:** {value}', scenarios)
        examples = re.findall(r'```markdown\n(.+?)\n```', reference, re.DOTALL)
        self.assertEqual(len(examples), 1)
        lines = examples[0].splitlines()
        starts = [index for index, line in enumerate(lines)
                  if line.startswith('**Start with:** ')]
        self.assertEqual(len(starts), 1)
        following = lines[starts[0] + 1:starts[0] + 2] or ['']
        self.assertRegex(following[0], r'^\*\*Work surface:\*\* \S')
        for text in (reference, scenarios):
            for value in re.findall(r'\*\*Work surface:\*\* (\w+)', text):
                with self.subTest(found=value):
                    self.assertIn(value, values)

    def test_check_wiring(self):
        for path in (ROOT / 'README.md', ROOT / 'AGENTS.md',
                     ROOT / '.github/workflows/validate.yml'):
            self.assertIn('python3 tests/plan-work-test.py', path.read_text())


if __name__ == '__main__':
    unittest.main()
