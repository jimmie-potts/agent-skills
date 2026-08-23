#!/usr/bin/env python3
"""Verify the pinned Interrogate skill without executing skill code."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIRECTORY = REPOSITORY_ROOT / "skills" / "interrogate"
SKILL_PATH = SKILL_DIRECTORY / "SKILL.md"
RUBRIC_PATH = SKILL_DIRECTORY / "references" / "review-rubric.md"
METADATA_PATH = SKILL_DIRECTORY / "agents" / "openai.yaml"
SOURCE_PATH = SKILL_DIRECTORY / "SOURCE.md"
LICENSE_PATH = SKILL_DIRECTORY / "LICENSE"
PROVENANCE_PATH = REPOSITORY_ROOT / "PROVENANCE.md"
EXPECTED_REVISION = "46125561306434d8a1d7745d540d8932ab0cd2a2"
EXPECTED_DIGESTS = (
    "a009220dfe6869c8f7980a94fb1c9c7763a081a0b32fb6d0afb65b8ff1868146",
    "2462f1347b99b412b04fcb0577b96d8744c801f792f2651746f9409fd4465dc9",
    "d2cea6cc308758201c6b8b82baf780947645f1ab752707ddf97fab374bf473f9",
    "a397cc61102add709803d917fb23d726920525bf23e7c06dc4ed0b5cbeb00e54",
    "a67bf02426f88714634ff481d667db821d4b2cea7b335bcd165fe3126e427fb5",
)


def split_frontmatter(markdown: str) -> tuple[dict[str, object], str]:
    match = re.fullmatch(r"---\n(.*?)\n---\n(.*)", markdown, re.DOTALL)
    if match is None:
        raise AssertionError("SKILL.md must start with YAML frontmatter")
    frontmatter = yaml.safe_load(match.group(1))
    if not isinstance(frontmatter, dict):
        raise AssertionError("SKILL.md frontmatter must be a mapping")
    return frontmatter, match.group(2)


class InterrogateSkillTest(unittest.TestCase):
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
            ["review-rubric.md"],
        )
        for path in (SKILL_PATH, RUBRIC_PATH, METADATA_PATH, SOURCE_PATH, LICENSE_PATH):
            self.assertTrue(path.is_file(), f"{path} must be a regular file")
            self.assertFalse(path.is_symlink(), f"{path} must not be a symlink")

    def test_metadata_is_explicit_only_and_portable(self) -> None:
        frontmatter, _ = split_frontmatter(SKILL_PATH.read_text(encoding="utf-8"))
        metadata = yaml.safe_load(METADATA_PATH.read_text(encoding="utf-8"))

        self.assertEqual(sorted(frontmatter), ["description", "name"])
        self.assertEqual(frontmatter["name"], "interrogate")
        self.assertIn("explicitly", str(frontmatter["description"]))
        self.assertEqual(sorted(metadata), ["interface", "policy"])
        self.assertIn("$interrogate", metadata["interface"]["default_prompt"])
        self.assertIs(metadata["policy"]["allow_implicit_invocation"], False)
        self.assertNotIn("dependencies", metadata)

    def test_review_is_independent_read_only_and_adjudicated(self) -> None:
        _, body = split_frontmatter(SKILL_PATH.read_text(encoding="utf-8"))
        normalized = " ".join(body.split())

        for required in (
            "This skill grants no authority to modify files",
            "Use at least two genuine independent reviewers",
            "Do not present repeated work from one reasoning pass as a multi-reviewer result",
            "Agreement raises confidence but does not prove a finding",
            "Severity, reproducibility, likelihood, and impact matter more than reviewer count",
            "Do not apply changes unless the user separately asks for fixes",
        ):
            self.assertIn(required, normalized)

        for cursor_specific in (
            "generalPurpose",
            "claude-fable",
            "claude-opus",
            "grok-4.6",
            "~/.cursor",
            "Task tool",
        ):
            self.assertNotIn(cursor_specific, body)

    def test_rubric_covers_material_review_lenses(self) -> None:
        rubric = RUBRIC_PATH.read_text(encoding="utf-8")
        normalized = " ".join(rubric.split())
        for heading in (
            "## Correctness",
            "## Root cause and ownership",
            "## Structural quality",
            "## Verification",
            "## Complexity and evolution",
            "## Security and privacy",
            "## Finding quality",
        ):
            self.assertIn(heading, rubric)
        self.assertIn("reachable failure mode", normalized)
        self.assertIn("Omit nits", normalized)

    def test_provenance_and_mit_notice_are_pinned(self) -> None:
        source = SOURCE_PATH.read_text(encoding="utf-8")
        license_text = LICENSE_PATH.read_text(encoding="utf-8")
        provenance = PROVENANCE_PATH.read_text(encoding="utf-8")

        for required in (
            EXPECTED_REVISION,
            *EXPECTED_DIGESTS,
            "2026-08-23",
            "pstack/skills/interrogate/",
        ):
            self.assertIn(required, source)
        for required in (
            EXPECTED_REVISION,
            "https://github.com/cursor/plugins",
            "skills/interrogate/LICENSE",
            "skills/interrogate/SOURCE.md",
        ):
            self.assertIn(required, provenance)
        self.assertTrue(license_text.startswith("MIT License\n"))
        self.assertIn("Copyright (c) 2026 Lauren Tan", license_text)
        self.assertIn('THE SOFTWARE IS PROVIDED "AS IS"', license_text)


if __name__ == "__main__":
    unittest.main()
