#!/usr/bin/env python3
"""Verify the pinned Architect skill without executing skill code."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIRECTORY = REPOSITORY_ROOT / "skills" / "architect"
SKILL_PATH = SKILL_DIRECTORY / "SKILL.md"
DESIGN_REVIEW_PATH = SKILL_DIRECTORY / "references" / "design-review.md"
RATIONALE_PATH = SKILL_DIRECTORY / "references" / "rationale-template.md"
METADATA_PATH = SKILL_DIRECTORY / "agents" / "openai.yaml"
SOURCE_PATH = SKILL_DIRECTORY / "SOURCE.md"
LICENSE_PATH = SKILL_DIRECTORY / "LICENSE"
PROVENANCE_PATH = REPOSITORY_ROOT / "PROVENANCE.md"
EXPECTED_REVISION = "46125561306434d8a1d7745d540d8932ab0cd2a2"
EXPECTED_DIGESTS = (
    "585d7a9e03c0cced84c80d4b60c09c8dc76010bb36c579f92d9e4deafec53df7",
    "905066f9bbac81c573c2b325be47751d2c0f9325e0a0772bd4384e82dafe9336",
    "6645a0e5f68c003298ec95b85a23262bdda0c79f998b926060169b54d9f23fbb",
    "3ef8c1452a0382a15b7601c7c94f2a16a00954170d705b7af8cc49ac78080ec9",
)


def split_frontmatter(markdown: str) -> tuple[dict[str, object], str]:
    match = re.fullmatch(r"---\n(.*?)\n---\n(.*)", markdown, re.DOTALL)
    if match is None:
        raise AssertionError("SKILL.md must start with YAML frontmatter")
    frontmatter = yaml.safe_load(match.group(1))
    if not isinstance(frontmatter, dict):
        raise AssertionError("SKILL.md frontmatter must be a mapping")
    return frontmatter, match.group(2)


class ArchitectSkillTest(unittest.TestCase):
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
            ["design-review.md", "rationale-template.md"],
        )
        for path in (
            SKILL_PATH,
            DESIGN_REVIEW_PATH,
            RATIONALE_PATH,
            METADATA_PATH,
            SOURCE_PATH,
            LICENSE_PATH,
        ):
            self.assertTrue(path.is_file(), f"{path} must be a regular file")
            self.assertFalse(path.is_symlink(), f"{path} must not be a symlink")

    def test_metadata_is_explicit_only_and_portable(self) -> None:
        frontmatter, _ = split_frontmatter(SKILL_PATH.read_text(encoding="utf-8"))
        metadata = yaml.safe_load(METADATA_PATH.read_text(encoding="utf-8"))

        self.assertEqual(sorted(frontmatter), ["description", "name"])
        self.assertEqual(frontmatter["name"], "architect")
        self.assertIn("explicitly", str(frontmatter["description"]))
        self.assertEqual(sorted(metadata), ["interface", "policy"])
        self.assertIn("$architect", metadata["interface"]["default_prompt"])
        self.assertIs(metadata["policy"]["allow_implicit_invocation"], False)
        self.assertNotIn("dependencies", metadata)

    def test_workflow_preserves_design_and_authority_invariants(self) -> None:
        _, body = split_frontmatter(SKILL_PATH.read_text(encoding="utf-8"))
        normalized = " ".join(body.split())

        for required in (
            "This skill grants no authority to modify tracked files",
            "If the user asks only for architecture or design, stop after the design package",
            "Write the caller's usage first",
            "at least two structurally different candidate designs",
            "Do not average designs with conflicting ownership or data models",
            "Treat deviations as evidence",
            "Do not put throwing stubs or unfinished bodies into production paths",
        ):
            self.assertIn(required, normalized)

        for dependency in ("$how", "$why", "$arena", "$interrogate", "$unslop"):
            self.assertIn(dependency, body)
            self.assertTrue(
                (REPOSITORY_ROOT / "skills" / dependency[1:] / "SKILL.md").is_file()
            )

        for cursor_specific in (
            "claude-fable",
            "claude-opus",
            "grok-4.6",
            "~/.cursor",
            "Task tool",
        ):
            self.assertNotIn(cursor_specific, body)

    def test_references_define_candidate_and_rationale_contracts(self) -> None:
        design_review = DESIGN_REVIEW_PATH.read_text(encoding="utf-8")
        rationale = RATIONALE_PATH.read_text(encoding="utf-8")

        for heading in (
            "## Build the candidate",
            "### Shallow modules",
            "### Information leakage",
            "### Temporal decomposition",
            "### Pass-through layers",
            "### Escape-hatch types",
            "### Accidental shared state",
            "## Compare candidates",
        ):
            self.assertIn(heading, design_review)
        for heading in (
            "## Problem",
            "## Caller usage",
            "## Proposed shape",
            "## Synthesis decision",
            "## Tradeoffs accepted",
            "## Alternatives considered",
            "## Open questions and risks",
            "## Next implementation step",
        ):
            self.assertIn(heading, rationale)

    def test_provenance_and_mit_notice_are_pinned(self) -> None:
        source = SOURCE_PATH.read_text(encoding="utf-8")
        license_text = LICENSE_PATH.read_text(encoding="utf-8")
        provenance = PROVENANCE_PATH.read_text(encoding="utf-8")

        for required in (
            EXPECTED_REVISION,
            *EXPECTED_DIGESTS,
            "2026-08-23",
            "pstack/skills/architect/",
        ):
            self.assertIn(required, source)
        for required in (
            EXPECTED_REVISION,
            "https://github.com/cursor/plugins",
            "skills/architect/LICENSE",
            "skills/architect/SOURCE.md",
        ):
            self.assertIn(required, provenance)
        self.assertTrue(license_text.startswith("MIT License\n"))
        self.assertIn("Copyright (c) 2026 Lauren Tan", license_text)
        self.assertIn('THE SOFTWARE IS PROVIDED "AS IS"', license_text)


if __name__ == "__main__":
    unittest.main()
