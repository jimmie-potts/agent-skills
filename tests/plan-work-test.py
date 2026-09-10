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

    def test_canonical_assessment_dependency(self):
        resource = 'references/work-assessment.md'
        selection = 'references/model-selection.md'
        self.assertTrue((ROOT / 'skills/deliver-work' / selection).is_file())
        self.assertFalse((SKILL / selection).exists())
        self.assertIn(selection, (SKILL / 'SKILL.md').read_text())
        self.assertTrue((ROOT / 'skills/deliver-work' / resource).is_file())
        self.assertFalse((SKILL / resource).exists())
        self.assertIn(resource, (SKILL / 'SKILL.md').read_text())

    def test_instruction_only_package(self):
        for path in SKILL.rglob('*'):
            self.assertFalse(path.is_symlink(), str(path))
            if path.is_file():
                self.assertIn(path.suffix, {'.md', '.yaml'})

    def test_check_wiring(self):
        for path in (ROOT / 'README.md', ROOT / 'AGENTS.md',
                     ROOT / '.github/workflows/validate.yml'):
            self.assertIn('python3 tests/plan-work-test.py', path.read_text())


if __name__ == '__main__':
    unittest.main()
