#!/usr/bin/env python3
"""Structural contracts for the host-specific advisory pairing skills."""
from pathlib import Path
import re
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'skills'
PAIRINGS = {
    'sol-with-astra': 'references/codex.md',
    'worker-with-fable': 'references/claude-code.md',
}


def links(path):
    return re.findall(r'\]\(([^)]+)\)', path.read_text())


def reference_closure(skill):
    pending, visited = [skill / 'SKILL.md'], set()
    while pending:
        path = pending.pop().resolve()
        if path in visited:
            continue
        visited.add(path)
        for link in links(path):
            if '://' in link or link.startswith('#'):
                continue
            target = (path.parent / link.split('#')[0]).resolve()
            assert target.is_relative_to(skill.resolve()), link
            assert target.is_file(), link
            if target.suffix == '.md':
                pending.append(target)
    return visited


class PairingSkillsStructureTest(unittest.TestCase):
    def test_portable_explicit_entrypoints(self):
        for name in PAIRINGS:
            skill = SKILLS / name
            text = (skill / 'SKILL.md').read_text()
            match = re.fullmatch(r'---\n(.*?)\n---\n(.+)', text, re.DOTALL)
            self.assertIsNotNone(match, name)
            metadata = yaml.safe_load(match.group(1))
            self.assertEqual(set(metadata), {'name', 'description'}, name)
            self.assertEqual(metadata['name'], name)
            self.assertIn('explicitly invoked', metadata['description'])
            self.assertLessEqual(len(text.splitlines()), 500, name)

    def test_host_adapters_are_routed_without_orphans(self):
        for name, adapter in PAIRINGS.items():
            skill = SKILLS / name
            self.assertIn(adapter, links(skill / 'SKILL.md'), name)
            self.assertIn('references/validation-scenarios.md',
                          links(skill / 'SKILL.md'), name)
            visited = reference_closure(skill)
            references = set((skill / 'references').glob('*.md'))
            self.assertTrue(references <= visited, references - visited)

    def test_instruction_only_packages(self):
        for name in PAIRINGS:
            for path in (SKILLS / name).rglob('*'):
                self.assertFalse(path.is_symlink(), str(path))
                if path.is_file():
                    self.assertEqual(path.suffix, '.md', str(path))
            self.assertFalse((SKILLS / name / 'scripts').exists())

    def test_each_pairing_names_its_host_counterpart(self):
        astra = (SKILLS / 'sol-with-astra/SKILL.md').read_text()
        fable = (SKILLS / 'worker-with-fable/SKILL.md').read_text()
        self.assertIn('worker-with-fable', astra)
        self.assertIn('sol-with-astra', fable)
        for text in (astra, fable):
            self.assertIn('plan-work', text)
            self.assertIn('deliver-work', text)

    def test_composing_workflows_route_by_host(self):
        deliver = SKILLS / 'deliver-work'
        policy = deliver / 'references/model-selection.md'
        self.assertIn('claude-code-model-selection.md', links(policy))
        self.assertIn('codex-model-selection.md', links(policy))
        for path in (deliver / 'SKILL.md', policy,
                     SKILLS / 'plan-work/SKILL.md'):
            text = path.read_text()
            self.assertIn('sol-with-astra', text, str(path))
            self.assertIn('worker-with-fable', text, str(path))
        adapter = (deliver / 'references/claude-code-model-selection.md').read_text()
        self.assertIn('references/worker-tiers.md', adapter)
        self.assertTrue((SKILLS / 'worker-with-fable/references/worker-tiers.md').is_file())

    def test_check_wiring(self):
        for path in (ROOT / 'README.md', ROOT / 'AGENTS.md',
                     ROOT / '.github/workflows/validate.yml'):
            self.assertIn('python3 tests/pairing-skills-test.py',
                          path.read_text(), str(path))


if __name__ == '__main__':
    unittest.main()
