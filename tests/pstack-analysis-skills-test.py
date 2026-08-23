#!/usr/bin/env python3
"""Verify the pinned How, Why, and Arena skills without executing skill code."""

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
    "arena": "a2241e8500a44d9c16bd3260c8c70e28c4bb8a857c33061d42b267057e6f7093",
    "how": "fe503e7a9b2a3a7ad2622a2de6124cb06c466922fb44bc61817b49b52042b885",
    "why": "dc8f2d8a7dbef7d0467cca8e6d055a4dbde027db6e2cbbfb18aa9071d8f20b6c",
}


def split_frontmatter(markdown: str) -> tuple[dict[str, object], str]:
    match = re.fullmatch(r"---\n(.*?)\n---\n(.*)", markdown, re.DOTALL)
    if match is None:
        raise AssertionError("SKILL.md must start with YAML frontmatter")
    frontmatter = yaml.safe_load(match.group(1))
    if not isinstance(frontmatter, dict):
        raise AssertionError("SKILL.md frontmatter must be a mapping")
    return frontmatter, match.group(2)


class PstackAnalysisSkillsTest(unittest.TestCase):
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

    def test_frontmatter_and_codex_policy_are_portable(self) -> None:
        expected_policy = {"arena": False, "how": True, "why": True}
        for name, allow_implicit in expected_policy.items():
            directory = SKILLS_ROOT / name
            frontmatter, _ = split_frontmatter(
                (directory / "SKILL.md").read_text(encoding="utf-8")
            )
            metadata = yaml.safe_load(
                (directory / "agents/openai.yaml").read_text(encoding="utf-8")
            )
            self.assertEqual(sorted(frontmatter), ["description", "name"])
            self.assertEqual(frontmatter["name"], name)
            self.assertEqual(sorted(metadata), ["interface", "policy"])
            self.assertIn(f"${name}", metadata["interface"]["default_prompt"])
            self.assertIs(
                metadata["policy"]["allow_implicit_invocation"], allow_implicit
            )
            self.assertNotIn("dependencies", metadata)

    def test_workflows_preserve_authority_and_host_portability(self) -> None:
        bodies = {
            name: split_frontmatter(
                (SKILLS_ROOT / name / "SKILL.md").read_text(encoding="utf-8")
            )[1]
            for name in EXPECTED_DIGESTS
        }
        for body in bodies.values():
            self.assertIn("grants no authority", " ".join(body.split()))
            self.assertIn("$unslop", body)
            for cursor_specific in (
                "generalPurpose",
                "grok-4.6",
                "claude-fable",
                "claude-opus",
                "~/.cursor",
                "readonly: false",
            ):
                self.assertNotIn(cursor_specific, body)

        normalized = {name: " ".join(body.split()) for name, body in bodies.items()}
        self.assertIn("implemented behavior from caller-driven assumptions", normalized["how"])
        self.assertIn("null result is evidence only", normalized["why"])
        self.assertIn("do not simulate an arena", normalized["arena"])
        self.assertIn("allow_implicit_invocation: false", (SKILLS_ROOT / "arena" / "agents" / "openai.yaml").read_text(encoding="utf-8"))

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

    def test_blast_radius_dependencies_resolve_to_catalog_entries(self) -> None:
        blast_radius = (SKILLS_ROOT / "blast-radius" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        for dependency in ("how", "why", "arena", "unslop"):
            self.assertIn(f"${dependency}", blast_radius)
            self.assertTrue((SKILLS_ROOT / dependency / "SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
