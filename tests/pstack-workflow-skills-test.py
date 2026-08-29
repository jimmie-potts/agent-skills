#!/usr/bin/env python3
"""Verify the pinned Teach, TDD, and Technical Writing catalog skills."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPOSITORY_ROOT / "skills"
PROVENANCE_PATH = REPOSITORY_ROOT / "PROVENANCE.md"
EXPECTED_REVISION = "46125561306434d8a1d7745d540d8932ab0cd2a2"
EXPECTED_DIGESTS = {
    "teach": "0a5987b0588dc56e14bfd84d0300e2ab405abc7c5c2aa81e0d3d7c6b243db7a7",
    "tdd": "adad031f9e79d7f7389fa128f7af8e03344831270e282cf4e40bdacb8418c386",
    "technical-writing": "bd0cb21034f4fe6695cfdf8cd3561026eec943f0bb6e9300bc78a2b3340865a7",
}
EXPECTED_IMPLICIT_INVOCATION = {
    "teach": False,
    "tdd": False,
    "technical-writing": True,
}


def split_frontmatter(markdown: str) -> tuple[dict[str, object], str]:
    match = re.fullmatch(r"---\n(.*?)\n---\n(.*)", markdown, re.DOTALL)
    if match is None:
        raise AssertionError("SKILL.md must start with YAML frontmatter")
    frontmatter = yaml.safe_load(match.group(1))
    if not isinstance(frontmatter, dict):
        raise AssertionError("SKILL.md frontmatter must be a mapping")
    return frontmatter, match.group(2)


class PstackWorkflowSkillsTest(unittest.TestCase):
    def test_each_skill_has_a_closed_regular_file_inventory(self) -> None:
        for name in EXPECTED_DIGESTS:
            directory = SKILLS_ROOT / name
            self.assertEqual(
                sorted(path.name for path in directory.iterdir()),
                ["LICENSE", "SKILL.md", "SOURCE.md", "agents"],
            )
            self.assertEqual(
                sorted(path.name for path in (directory / "agents").iterdir()),
                ["openai.yaml"],
            )
            for relative in ("SKILL.md", "SOURCE.md", "LICENSE", "agents/openai.yaml"):
                path = directory / relative
                self.assertTrue(path.is_file(), f"{path} must be a regular file")
                self.assertFalse(path.is_symlink(), f"{path} must not be a symlink")

    def test_skills_have_portable_frontmatter_and_intended_invocation_policy(self) -> None:
        self.assertEqual(set(EXPECTED_DIGESTS), set(EXPECTED_IMPLICIT_INVOCATION))
        for name, allow_implicit in EXPECTED_IMPLICIT_INVOCATION.items():
            directory = SKILLS_ROOT / name
            frontmatter, _ = split_frontmatter(
                (directory / "SKILL.md").read_text(encoding="utf-8")
            )
            metadata = yaml.safe_load(
                (directory / "agents/openai.yaml").read_text(encoding="utf-8")
            )
            self.assertEqual(sorted(frontmatter), ["description", "name"])
            self.assertEqual(frontmatter["name"], name)
            description = str(frontmatter["description"]).lower()
            if allow_implicit:
                self.assertNotIn("explicit", description)
            else:
                self.assertIn("explicit", description)
            self.assertEqual(sorted(metadata), ["interface", "policy"])
            self.assertIn(f"${name}", metadata["interface"]["default_prompt"])
            self.assertIs(
                metadata["policy"]["allow_implicit_invocation"], allow_implicit
            )
            self.assertNotIn("dependencies", metadata)

        technical_description = str(
            split_frontmatter(
                (SKILLS_ROOT / "technical-writing" / "SKILL.md").read_text(
                    encoding="utf-8"
                )
            )[0]["description"]
        ).lower()
        for trigger in (
            "documentation",
            "rfcs",
            "readmes",
            "pull-request descriptions",
            "commit messages",
            "formal technical reports",
        ):
            self.assertIn(trigger, technical_description)
        for boundary in (
            "code-only work",
            "ordinary code explanations",
            "nontechnical prose",
        ):
            self.assertIn(boundary, technical_description)

    def test_workflows_keep_their_material_invariants(self) -> None:
        bodies = {
            name: " ".join(
                split_frontmatter(
                    (SKILLS_ROOT / name / "SKILL.md").read_text(encoding="utf-8")
                )[1].split()
            )
            for name in EXPECTED_DIGESTS
        }

        for body in bodies.values():
            self.assertIn("grants no authority", body)
            self.assertIn("$unslop", body)
            for cursor_specific in (
                "disable-model-invocation",
                "generalPurpose",
                "run_in_background",
                "~/.cursor",
            ):
                self.assertNotIn(cursor_specific, body)

        for dependency in ("$how", "$why", "$unslop"):
            self.assertIn(dependency, bodies["teach"])
        self.assertIn("fails for the expected reason", bodies["tdd"])
        self.assertIn("same regression test and confirm it passes", bodies["tdd"])
        for mode in ("Tutorial", "How-to", "Reference", "Explanation"):
            self.assertIn(mode, bodies["technical-writing"])
        self.assertIn("Remove ambiguous syntax", bodies["technical-writing"])

    def test_teach_dependencies_resolve_to_catalog_entries(self) -> None:
        teach = (SKILLS_ROOT / "teach" / "SKILL.md").read_text(encoding="utf-8")
        for dependency in ("how", "why", "unslop"):
            self.assertIn(f"${dependency}", teach)
            self.assertTrue((SKILLS_ROOT / dependency / "SKILL.md").is_file())

    def test_provenance_and_mit_notices_are_pinned(self) -> None:
        provenance = PROVENANCE_PATH.read_text(encoding="utf-8")
        for name, digest in EXPECTED_DIGESTS.items():
            source = (SKILLS_ROOT / name / "SOURCE.md").read_text(encoding="utf-8")
            license_text = (SKILLS_ROOT / name / "LICENSE").read_text(
                encoding="utf-8"
            )
            for required in (
                EXPECTED_REVISION,
                digest,
                "2026-08-22",
                f"pstack/skills/{name}/SKILL.md",
            ):
                self.assertIn(required, source)
            for required in (
                EXPECTED_REVISION,
                "https://github.com/cursor/plugins",
                f"skills/{name}/LICENSE",
                f"skills/{name}/SOURCE.md",
            ):
                self.assertIn(required, provenance)
            self.assertTrue(license_text.startswith("MIT License\n"))
            self.assertIn("Copyright (c) 2026 Lauren Tan", license_text)
            self.assertIn('THE SOFTWARE IS PROVIDED "AS IS"', license_text)


if __name__ == "__main__":
    unittest.main()
