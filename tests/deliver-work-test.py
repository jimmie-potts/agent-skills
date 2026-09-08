#!/usr/bin/env python3
"""Structural contracts only; behavioral evaluation uses held-out scenarios."""
from pathlib import Path
import re
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'deliver-work'


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

    def test_assessment_resource_is_exposed_to_consumers(self):
        # Other workflows discover this stable resource without invoking delivery.
        resource = 'references/work-assessment.md'
        self.assertTrue((SKILL / resource).is_file())
        links = re.findall(r'\]\(([^)]+)\)',
                           (SKILL / 'SKILL.md').read_text())
        self.assertIn(resource, links)

    def test_selection_resources_are_routed(self):
        entry_links = re.findall(r'\]\(([^)]+)\)',
                                (SKILL / 'SKILL.md').read_text())
        self.assertIn('references/model-selection.md', entry_links)
        policy = SKILL / 'references/model-selection.md'
        adapter_links = re.findall(r'\]\(([^)]+)\)', policy.read_text())
        self.assertIn('codex-model-selection.md', adapter_links)

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
