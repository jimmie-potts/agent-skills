#!/usr/bin/env python3
"""Verify the pinned Architect skill and its design-decision fixtures without
executing skill code."""

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
CALLER_EXAMPLES_PATH = SKILL_DIRECTORY / "references" / "caller-examples.md"
METADATA_PATH = SKILL_DIRECTORY / "agents" / "openai.yaml"
SOURCE_PATH = SKILL_DIRECTORY / "SOURCE.md"
LICENSE_PATH = SKILL_DIRECTORY / "LICENSE"
PROVENANCE_PATH = REPOSITORY_ROOT / "PROVENANCE.md"
FIXTURES = REPOSITORY_ROOT / "tests" / "fixtures" / "design-decisions"
ANCHOR_SKILLS = ("architect", "prototype")
ACCEPTANCE_CRITERIA = {1, 2, 3, 4, 5, 6}
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


def normalized(text: str) -> str:
    return " ".join(text.split())


def fixture_sections(path: Path) -> dict[str, tuple[str, str]]:
    """Map each `## D<n> Title` heading to its title and section body."""
    text = path.read_text(encoding="utf-8")
    level_two = re.findall(r"^## .*$", text, flags=re.M)
    parts = re.split(r"^## (D\d+) ([^\n]+)\n", text, flags=re.M)
    ids = parts[1::3]
    if len(ids) != len(level_two):
        raise AssertionError(f"{path.name} has a level-two heading that is not `## D<n> Title`")
    if len(set(ids)) != len(ids):
        raise AssertionError(f"{path.name} repeats a case ID")
    return {case_id: (title, body) for case_id, title, body in zip(ids, parts[2::3], parts[3::3])}


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
            ["caller-examples.md", "design-review.md", "rationale-template.md"],
        )
        for path in (
            SKILL_PATH,
            DESIGN_REVIEW_PATH,
            RATIONALE_PATH,
            CALLER_EXAMPLES_PATH,
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
        text = normalized(body)

        for required in (
            "This skill grants no authority to modify tracked files",
            "If the user asks only for architecture or design, stop after the design package",
            "Write the caller's usage first",
            "at least two structurally different candidate designs",
            "Do not average designs with conflicting ownership or data models",
            "Treat deviations as evidence",
            "Do not put throwing stubs or unfinished bodies into production paths",
            "A consequential interface is one that other modules, services, jobs, or people call",
            "For a consequential interface, do not endorse a candidate before its caller example shows the caller, owner, success path, and failure and recovery path",
            "Choose directly when one candidate clearly wins or no real alternative needs investigation",
            "write a comparison brief before any artifact exists",
            "Run it with `prototype` only when the user explicitly invokes prototype for this task",
            "keep the decision open until the user answers",
        ):
            self.assertIn(required, text)

        for reference in (
            "references/design-review.md",
            "references/caller-examples.md",
            "references/rationale-template.md",
        ):
            self.assertIn(f"]({reference})", body)

        for dependency in ("how", "why", "arena", "interrogate", "prototype", "unslop"):
            self.assertIn(f"`{dependency}`", body)
            self.assertTrue(
                (REPOSITORY_ROOT / "skills" / dependency / "SKILL.md").is_file()
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

    def test_caller_example_reference_defines_the_design_contract(self) -> None:
        reference = CALLER_EXAMPLES_PATH.read_text(encoding="utf-8")
        text = normalized(reference)
        for heading in (
            "## Write the caller example first",
            "## Encode invariants selectively",
            "## Explain the chosen shape",
        ):
            self.assertIn(heading, reference)
        for field in (
            "**Caller and real setup:**",
            "**Owner:**",
            "**Smallest useful operation:**",
            "**Success path:**",
            "**Failure and recovery path:**",
            "**Caller knowledge:**",
        ):
            self.assertIn(field, reference)
        for required in (
            "Do not endorse a candidate whose example lacks an owner or a failure and recovery path",
            "An internal helper or a local change with no new public contract needs no separate example",
            "when it prevents a demonstrated class of error",
            "Do not start a repository-wide type migration, compiler-strictness change, or blanket style rule",
            "Do not create a slide deck, report page, or other presentation artifact unless the user asks for one",
        ):
            self.assertIn(required, text)
        # The worked examples must show a failure path and a rejected invalid state.
        self.assertEqual(reference.count("```ts"), 2)
        for token in ('case "declined"', 'case "pending"', "idempotencyKey",
                      '{ status: "captured"; receiptId: string }', "raw: unknown"):
            self.assertIn(token, reference)
        self.assertIn(
            "](caller-examples.md",
            DESIGN_REVIEW_PATH.read_text(encoding="utf-8"),
        )

    def test_design_decision_fixtures_cover_acceptance_and_cite_live_rules(self) -> None:
        cases = fixture_sections(FIXTURES / "cases.md")
        graders = fixture_sections(FIXTURES / "graders.md")
        self.assertEqual(sorted(cases), sorted(graders))
        self.assertGreaterEqual(len(cases), 11)

        covered: set[int] = set()
        kinds: set[str] = set()
        for case_id, (title, case) in cases.items():
            with self.subTest(case=case_id):
                self.assertEqual(title, graders[case_id][0])
                invoked_line = re.search(r"^Invoked: (.+)$", case, re.M)
                self.assertIsNotNone(invoked_line)
                invoked = set(invoked_line.group(1).split(", "))
                self.assertTrue(invoked)
                self.assertLessEqual(invoked, set(ANCHOR_SKILLS))
                self.assertIn("Prompt:", case)
                self.assertIn("Setup:", case)
                # Inputs must not leak the expected outcome or its rule anchors.
                for leak in ("Expected:", "Anchors:", "Acceptance:"):
                    self.assertNotIn(leak, case)

                grader = graders[case_id][1]
                acceptance = re.search(r"^Acceptance: (\d+)$", grader, re.M)
                kind = re.search(r"^Kind: (positive|negative)$", grader, re.M)
                self.assertIsNotNone(acceptance)
                self.assertIsNotNone(kind)
                self.assertIn("Expected:", grader)
                covered.add(int(acceptance.group(1)))
                kinds.add(kind.group(1))

                anchor_block = grader.split("Anchors:\n", 1)[1]
                anchor_lines = [line for line in anchor_block.splitlines() if line.strip()]
                anchors = [re.fullmatch(r'- (skills/[^:]+): "(.+)"', line) for line in anchor_lines]
                self.assertTrue(anchors, "each grader cites at least one rule")
                self.assertTrue(all(anchors), f"{case_id} has a malformed anchor line")
                anchors = [match.groups() for match in anchors]
                for relative, phrase in anchors:
                    path = REPOSITORY_ROOT / relative
                    # A trial sees only its invoked skills, so graders may
                    # rely only on their rules.
                    self.assertIn(Path(relative).parts[1], invoked)
                    self.assertTrue(path.is_file(), relative)
                    self.assertIn(
                        normalized(phrase),
                        normalized(path.read_text(encoding="utf-8")),
                        f"{case_id} anchor missing from {relative}",
                    )
        self.assertEqual(covered, ACCEPTANCE_CRITERIA)
        self.assertEqual(kinds, {"positive", "negative"})

    def test_comparison_brief_fields_match_prototype(self) -> None:
        # Architect writes the brief that prototype runs; the fields must agree.
        architect = normalized(SKILL_PATH.read_text(encoding="utf-8"))
        prototype = normalized(
            (REPOSITORY_ROOT / "skills" / "prototype" / "SKILL.md").read_text(encoding="utf-8")
        )
        architect_brief = architect[architect.index("write a comparison brief"):]
        architect_brief = architect_brief[: architect_brief.index("Run it with")]
        prototype_brief = prototype[prototype.index("write the comparison brief"):]
        prototype_brief = prototype_brief[: prototype_brief.index("Build each alternative")]
        for field in (
            ("the question", "the question"),
            ("who owns that decision", "who owns that decision"),
            ("how each is observed", "how each one will be observed"),
            ("normally two", "normally two"),
            ("the stop condition", "the stop condition"),
        ):
            self.assertIn(field[0], architect_brief)
            self.assertIn(field[1], prototype_brief)

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
