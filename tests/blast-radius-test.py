#!/usr/bin/env python3
"""Verify the pinned Blast Radius skill without executing skill code."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIRECTORY = REPOSITORY_ROOT / "skills" / "blast-radius"
SKILL_PATH = SKILL_DIRECTORY / "SKILL.md"
METADATA_PATH = SKILL_DIRECTORY / "agents" / "openai.yaml"
SOURCE_PATH = SKILL_DIRECTORY / "SOURCE.md"
LICENSE_PATH = SKILL_DIRECTORY / "LICENSE"
PROVENANCE_PATH = REPOSITORY_ROOT / "PROVENANCE.md"
EXPECTED_SOURCE_REVISION = "e46364b8be46000b7df0f260550cd712afbb8d36"
EXPECTED_SOURCE_DIGEST = (
    "b060df3ca85803eabbce9fab53f5cc024ca8d784bdde5513c1c1a784947523f8"
)


def split_frontmatter(markdown: str) -> tuple[dict[str, object], str]:
    match = re.fullmatch(r"---\n(.*?)\n---\n(.*)", markdown, re.DOTALL)
    if match is None:
        raise AssertionError("SKILL.md must start with YAML frontmatter")
    frontmatter = yaml.safe_load(match.group(1))
    if not isinstance(frontmatter, dict):
        raise AssertionError("SKILL.md frontmatter must be a mapping")
    return frontmatter, match.group(2)


class BlastRadiusSkillTest(unittest.TestCase):
    def test_skill_has_a_closed_regular_file_inventory(self) -> None:
        self.assertEqual(
            sorted(path.name for path in SKILL_DIRECTORY.iterdir()),
            ["LICENSE", "SKILL.md", "SOURCE.md", "agents"],
        )
        self.assertEqual(
            sorted(path.name for path in (SKILL_DIRECTORY / "agents").iterdir()),
            ["openai.yaml"],
        )

        for path in (SKILL_PATH, METADATA_PATH, SOURCE_PATH, LICENSE_PATH):
            self.assertTrue(path.is_file(), f"{path} must be a regular file")
            self.assertFalse(path.is_symlink(), f"{path} must not be a symlink")

    def test_metadata_is_explicit_only_and_grants_no_tools(self) -> None:
        frontmatter, _ = split_frontmatter(SKILL_PATH.read_text(encoding="utf-8"))
        metadata = yaml.safe_load(METADATA_PATH.read_text(encoding="utf-8"))

        self.assertEqual(sorted(frontmatter), ["description", "name"])
        self.assertEqual(frontmatter["name"], "blast-radius")
        self.assertIn("explicitly asks", str(frontmatter["description"]))
        self.assertIn("what a change could break", str(frontmatter["description"]))
        self.assertEqual(sorted(metadata), ["interface", "policy"])
        self.assertIn("$blast-radius", metadata["interface"]["default_prompt"])
        self.assertIs(metadata["policy"]["allow_implicit_invocation"], False)
        self.assertNotIn("dependencies", metadata)

    def test_workflow_composes_catalog_skills_and_preserves_authority(self) -> None:
        _, body = split_frontmatter(SKILL_PATH.read_text(encoding="utf-8"))
        normalized_body = " ".join(body.split())

        for required in (
            "grants no authority to pull remote refs",
            "Do not execute untrusted code",
            "Treat any load-bearing fact that does not reach step 4 as unproven",
            "Use `$arena` only when the user explicitly requests competing parallel reviews",
            "Apply `$unslop` to the final narrative prose",
        ):
            self.assertIn(required, normalized_body)

        for dependency in ("$how", "$why", "$arena", "$unslop"):
            self.assertIn(dependency, body)
            dependency_name = dependency.removeprefix("$")
            self.assertTrue(
                (REPOSITORY_ROOT / "skills" / dependency_name / "SKILL.md").is_file()
            )

    def test_confidence_and_output_contract_are_complete(self) -> None:
        _, body = split_frontmatter(SKILL_PATH.read_text(encoding="utf-8"))

        confidence_levels = [
            int(level)
            for level in re.findall(
                r"^(\d+)\. (?:Assertion|Source|Reasoning|Execution|Runtime):",
                body,
                re.MULTILINE,
            )
        ]
        self.assertEqual(confidence_levels, list(range(1, 6)))
        for section in (
            "**What changed.**",
            "**Safety fact.**",
            "**Risks.**",
            "**Cleared.**",
            "**Before merge.**",
        ):
            self.assertIn(section, body)

    def test_provenance_and_mit_notice_are_pinned(self) -> None:
        source = SOURCE_PATH.read_text(encoding="utf-8")
        license_text = LICENSE_PATH.read_text(encoding="utf-8")
        provenance = PROVENANCE_PATH.read_text(encoding="utf-8")

        for required in (
            EXPECTED_SOURCE_REVISION,
            EXPECTED_SOURCE_DIGEST,
            "2026-08-22",
            "pstack/skills/blast-radius/SKILL.md",
        ):
            self.assertIn(required, source)
        for required in (
            EXPECTED_SOURCE_REVISION,
            "https://github.com/cursor/plugins",
            "skills/blast-radius/LICENSE",
            "skills/blast-radius/SOURCE.md",
        ):
            self.assertIn(required, provenance)
        self.assertTrue(license_text.startswith("MIT License\n"))
        self.assertIn("Copyright (c) 2026 Lauren Tan", license_text)
        self.assertIn('THE SOFTWARE IS PROVIDED "AS IS"', license_text)


if __name__ == "__main__":
    unittest.main()
