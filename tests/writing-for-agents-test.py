#!/usr/bin/env python3
"""Verify the pinned Writing for Agents skill without executing skill code."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIRECTORY = REPOSITORY_ROOT / "skills" / "writing-for-agents"
SKILL_PATH = SKILL_DIRECTORY / "SKILL.md"
SKILL_REFERENCE_PATH = SKILL_DIRECTORY / "references" / "skill-mechanics.md"
METADATA_PATH = SKILL_DIRECTORY / "agents" / "openai.yaml"
SOURCE_PATH = SKILL_DIRECTORY / "SOURCE.md"
LICENSE_PATH = SKILL_DIRECTORY / "LICENSE"
PROVENANCE_PATH = REPOSITORY_ROOT / "PROVENANCE.md"
EXPECTED_REVISION = "5b15a47f2d7150f545fbcacbfe381787fc0230dc"
EXPECTED_DIGESTS = (
    "551adca942227b44192edba88acd4e8db911f0121ce58ad16944ccf6a896a74a",
    "c768e6307c7c10728c401c213f2c4ba71c542127eeb7ad2956aabd15a0fa0059",
    "eacb24b2a618cfb81dacb0416f4fdd75ddf3a8060f8ddb99aae1b1e301907e4b",
    "0e7ac423bf2c6e223b7c5b156f8cf72da49d748e56a1641402c31f22ad07dbb5",
    "9d1f87a2d1cb55b4782b95abe710692b35b9659789c2db31a22c7074a3383e8e",
)


def split_frontmatter(markdown: str) -> tuple[dict[str, object], str]:
    match = re.fullmatch(r"---\n(.*?)\n---\n(.*)", markdown, re.DOTALL)
    if match is None:
        raise AssertionError("SKILL.md must start with YAML frontmatter")
    frontmatter = yaml.safe_load(match.group(1))
    if not isinstance(frontmatter, dict):
        raise AssertionError("SKILL.md frontmatter must be a mapping")
    return frontmatter, match.group(2)


class WritingForAgentsSkillTest(unittest.TestCase):
    def test_skill_has_a_closed_regular_file_inventory(self) -> None:
        self.assertEqual(
            sorted(path.name for path in SKILL_DIRECTORY.iterdir()),
            ["LICENSE", "SKILL.md", "SOURCE.md", "agents", "references"],
        )
        self.assertEqual(
            sorted(path.name for path in (SKILL_DIRECTORY / "agents").iterdir()),
            ["openai.yaml"],
        )
        self.assertEqual(
            sorted(path.name for path in (SKILL_DIRECTORY / "references").iterdir()),
            ["skill-mechanics.md"],
        )
        for path in (
            SKILL_PATH,
            SKILL_REFERENCE_PATH,
            METADATA_PATH,
            SOURCE_PATH,
            LICENSE_PATH,
        ):
            self.assertTrue(path.is_file(), f"{path} must be a regular file")
            self.assertFalse(path.is_symlink(), f"{path} must not be a symlink")

    def test_metadata_supports_automatic_selection_and_portable_frontmatter(self) -> None:
        frontmatter, _ = split_frontmatter(SKILL_PATH.read_text(encoding="utf-8"))
        metadata = yaml.safe_load(METADATA_PATH.read_text(encoding="utf-8"))

        self.assertEqual(sorted(frontmatter), ["description", "name"])
        self.assertEqual(frontmatter["name"], "writing-for-agents")
        for trigger in ("Agent Skills", "AGENTS.md", "conditional references"):
            self.assertIn(trigger, str(frontmatter["description"]))
        self.assertIn("do not use for ordinary human documentation", str(frontmatter["description"]))
        self.assertEqual(sorted(metadata), ["interface", "policy"])
        self.assertIn("$writing-for-agents", metadata["interface"]["default_prompt"])
        self.assertIs(metadata["policy"]["allow_implicit_invocation"], True)
        self.assertNotIn("dependencies", metadata)

    def test_provenance_and_mit_notice_are_pinned(self) -> None:
        source = SOURCE_PATH.read_text(encoding="utf-8")
        license_text = LICENSE_PATH.read_text(encoding="utf-8")
        provenance = PROVENANCE_PATH.read_text(encoding="utf-8")

        for required in (
            EXPECTED_REVISION,
            *EXPECTED_DIGESTS,
            "2026-08-23",
            "skills/productivity/writing-for-agents/",
        ):
            self.assertIn(required, source)
        for required in (
            EXPECTED_REVISION,
            "https://github.com/mattpocock/skills",
            "skills/writing-for-agents/LICENSE",
            "skills/writing-for-agents/SOURCE.md",
        ):
            self.assertIn(required, provenance)
        self.assertTrue(license_text.startswith("MIT License\n"))
        self.assertIn("Copyright (c) 2026 Matt Pocock", license_text)
        self.assertIn('THE SOFTWARE IS PROVIDED "AS IS"', license_text)


if __name__ == "__main__":
    unittest.main()
