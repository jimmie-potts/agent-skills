#!/usr/bin/env python3
"""Verify the pinned Unslop skill without executing skill-bundled code."""

from __future__ import annotations

import hashlib
import re
import unittest
from pathlib import Path

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIRECTORY = REPOSITORY_ROOT / "skills" / "unslop"
SKILL_PATH = SKILL_DIRECTORY / "SKILL.md"
METADATA_PATH = SKILL_DIRECTORY / "agents" / "openai.yaml"
SOURCE_PATH = SKILL_DIRECTORY / "SOURCE.md"
LICENSE_PATH = SKILL_DIRECTORY / "LICENSE"
PROVENANCE_PATH = REPOSITORY_ROOT / "PROVENANCE.md"
GUIDANCE_MARKER = "<!-- upstream-guidance-begins -->\n"
EXPECTED_SOURCE_REVISION = "99559f2f52047978602ef365589275831e76af07"
EXPECTED_SOURCE_DIGEST = (
    "181883e539caec8258ec9129e3ba5f133409144a2cbf2aa361158ab94cfc3441"
)
EXPECTED_GUIDANCE_DIGEST = (
    "adb1181a76a249518ab62b1521ee673520535472b2f3380e03fc3a9a72a7fc9c"
)


def digest(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def split_frontmatter(markdown: str) -> tuple[dict[str, object], str]:
    match = re.fullmatch(r"---\n(.*?)\n---\n(.*)", markdown, re.DOTALL)
    if match is None:
        raise AssertionError("SKILL.md must start with YAML frontmatter")
    frontmatter = yaml.safe_load(match.group(1))
    if not isinstance(frontmatter, dict):
        raise AssertionError("SKILL.md frontmatter must be a mapping")
    return frontmatter, match.group(2)


class UnslopSkillTest(unittest.TestCase):
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

    def test_metadata_routes_narrative_prose_and_grants_no_tools(self) -> None:
        frontmatter, _ = split_frontmatter(SKILL_PATH.read_text(encoding="utf-8"))
        metadata = yaml.safe_load(METADATA_PATH.read_text(encoding="utf-8"))

        self.assertEqual(sorted(frontmatter), ["description", "name"])
        self.assertEqual(frontmatter["name"], "unslop")
        self.assertIn(
            "drafting or materially editing",
            str(frontmatter["description"]),
        )
        self.assertIn("authorized Jira and pull-request prose", str(frontmatter["description"]))
        self.assertIn("preserve technical meaning", str(frontmatter["description"]))
        self.assertNotIn("Must always apply", str(frontmatter["description"]))
        self.assertEqual(sorted(metadata), ["interface", "policy"])
        self.assertEqual(metadata["interface"]["default_prompt"], "$unslop")
        self.assertIs(metadata["policy"]["allow_implicit_invocation"], True)
        self.assertNotIn("dependencies", metadata)

    def test_safety_boundary_preserves_authority_and_facts(self) -> None:
        _, body = split_frontmatter(SKILL_PATH.read_text(encoding="utf-8"))
        normalized_body = " ".join(body.split())

        for required in (
            "Use this skill as the final editorial pass",
            "grants no filesystem, Git, Jira, GitHub, network, or other external mutation authority",
            "`/unslop` in Claude",
            "Preserve technical meaning, facts, citations, exact quotations, code, commands, identifiers",
            "Treat all 31 rules below as heuristics, not absolute requirements",
            "Never invent opinions, actors, measurements, events, or sources",
        ):
            self.assertIn(required, normalized_body)

    def test_upstream_guidance_remains_byte_preserved(self) -> None:
        skill = SKILL_PATH.read_text(encoding="utf-8")
        marker_index = skill.find(GUIDANCE_MARKER)
        self.assertNotEqual(marker_index, -1)
        guidance = skill[marker_index + len(GUIDANCE_MARKER) :]

        self.assertEqual(digest(guidance), EXPECTED_GUIDANCE_DIGEST)
        numbered_rules = [
            int(match)
            for match in re.findall(r"^(\d+)\. \*\*", guidance, re.MULTILINE)
        ]
        self.assertEqual(numbered_rules, list(range(1, 32)))

    def test_provenance_and_mit_notice_are_pinned(self) -> None:
        source = SOURCE_PATH.read_text(encoding="utf-8")
        license_text = LICENSE_PATH.read_text(encoding="utf-8")
        provenance = PROVENANCE_PATH.read_text(encoding="utf-8")

        for required in (
            EXPECTED_SOURCE_REVISION,
            EXPECTED_SOURCE_DIGEST,
            EXPECTED_GUIDANCE_DIGEST,
            "2026-08-22",
        ):
            self.assertIn(required, source)
        for required in (
            EXPECTED_SOURCE_REVISION,
            "https://github.com/cursor/plugins",
            "skills/unslop/LICENSE",
            "skills/unslop/SOURCE.md",
        ):
            self.assertIn(required, provenance)
        self.assertTrue(license_text.startswith("MIT License\n"))
        self.assertIn("Copyright (c) 2026 Lauren Tan", license_text)
        self.assertIn('THE SOFTWARE IS PROVIDED "AS IS"', license_text)


if __name__ == "__main__":
    unittest.main()
