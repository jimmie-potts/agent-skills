#!/usr/bin/env python3
"""Verify the pinned grilling skill family without executing skill code."""

from __future__ import annotations

import hashlib
import re
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPOSITORY_ROOT / "skills"
PROVENANCE_PATH = REPOSITORY_ROOT / "PROVENANCE.md"
EXPECTED_REVISION = "5b15a47f2d7150f545fbcacbfe381787fc0230dc"
EXPECTED_RETRIEVAL_DATE = "2026-08-23"
EXPECTED_LICENSE_DIGEST = (
    "0e7ac423bf2c6e223b7c5b156f8cf72da49d748e56a1641402c31f22ad07dbb5"
)
EXPECTED_SKILLS = {
    "grilling": {
        "implicit": True,
        "upstream_path": "skills/productivity/grilling/",
        "digests": {
            "SKILL.md": "10ff989e7498b23b5acb49d5048f11dcd906757d2f79c5cdf8a00001381296f2",
            "agents/openai.yaml": "1411d7df7d99b7e621a1ff8283c8133cc2464be63d064e52d8ce169c6800ee9b",
        },
    },
    "grill-me": {
        "implicit": False,
        "upstream_path": "skills/productivity/grill-me/",
        "digests": {
            "SKILL.md": "caaf8b8de1684f96e26b28f3c29189db5c89cce4b73e1c93d86164f66ef88637",
            "agents/openai.yaml": "c061e39c3e0f9d865fb1b97556d485704af2a8a58f4b8221a8917a5c2074a32b",
        },
    },
    "grill-with-docs": {
        "implicit": False,
        "upstream_path": "skills/engineering/grill-with-docs/",
        "digests": {
            "SKILL.md": "7de372c13488f1ee96cc11cd8907b56b6809cc93eef776eeddd37de6b6cbe3fe",
            "agents/openai.yaml": "94cd0ab161fb468a836349f5ed482ba58ce8e709a05c57ce533d739dbd35cca9",
        },
    },
}
EXPECTED_INVENTORY = [
    "LICENSE",
    "SKILL.md",
    "SOURCE.md",
    "agents/",
    "agents/openai.yaml",
]
SKILL_TOKEN_PATTERN = re.compile(r"\$([a-z0-9]+(?:-[a-z0-9]+)*)\b")
NAMED_SKILL_DEPENDENCIES = {
    "grilling": {"unslop"},
    "grill-me": {"grilling"},
    "grill-with-docs": {"domain-modeling", "grilling", "unslop"},
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def split_frontmatter(markdown: str) -> tuple[dict[str, object], str]:
    match = re.fullmatch(r"---\n(.*?)\n---\n(.*)", markdown, re.DOTALL)
    if match is None:
        raise AssertionError("SKILL.md must start with YAML frontmatter")
    frontmatter = yaml.safe_load(match.group(1))
    if not isinstance(frontmatter, dict):
        raise AssertionError("SKILL.md frontmatter must be a mapping")
    return frontmatter, match.group(2)


def inventory(directory: Path) -> list[str]:
    entries: list[str] = []
    for path in directory.rglob("*"):
        relative = path.relative_to(directory).as_posix()
        entries.append(f"{relative}/" if path.is_dir() else relative)
    return sorted(entries)


def operational_text(directory: Path) -> str:
    paths = [directory / "SKILL.md", directory / "agents" / "openai.yaml"]
    references = directory / "references"
    if references.is_dir():
        paths.extend(sorted(references.rglob("*.md")))
    return "\n".join(path.read_text(encoding="utf-8") for path in paths)


def unresolved_dependencies(catalog: Path, name: str) -> list[str]:
    skill_directory = catalog / name
    tokens = set(SKILL_TOKEN_PATTERN.findall(operational_text(skill_directory)))
    tokens.update(NAMED_SKILL_DEPENDENCIES[name])
    tokens.discard(name)
    return sorted(
        token
        for token in tokens
        if not (catalog / token / "SKILL.md").is_file()
    )


class GrillingSkillsTest(unittest.TestCase):
    def test_each_skill_has_a_closed_regular_file_inventory(self) -> None:
        for name in EXPECTED_SKILLS:
            directory = SKILLS_ROOT / name
            self.assertEqual(inventory(directory), EXPECTED_INVENTORY)
            self.assertFalse(directory.is_symlink(), f"{directory} must not be a symlink")
            for path in directory.rglob("*"):
                self.assertFalse(path.is_symlink(), f"{path} must not be a symlink")
                self.assertTrue(
                    path.is_dir() or path.is_file(),
                    f"{path} must be a regular file or directory",
                )

    def test_frontmatter_and_codex_invocation_policies_are_portable(self) -> None:
        for name, expected in EXPECTED_SKILLS.items():
            directory = SKILLS_ROOT / name
            frontmatter, _ = split_frontmatter(
                (directory / "SKILL.md").read_text(encoding="utf-8")
            )
            metadata = yaml.safe_load(
                (directory / "agents/openai.yaml").read_text(encoding="utf-8")
            )

            self.assertEqual(sorted(frontmatter), ["description", "name"])
            self.assertEqual(frontmatter["name"], name)
            self.assertIsInstance(frontmatter["description"], str)
            self.assertTrue(str(frontmatter["description"]).strip())
            self.assertEqual(sorted(metadata), ["interface", "policy"])
            self.assertEqual(
                sorted(metadata["interface"]),
                ["default_prompt", "display_name", "short_description"],
            )
            self.assertEqual(
                sorted(metadata["policy"]), ["allow_implicit_invocation"]
            )
            for value in metadata["interface"].values():
                self.assertIsInstance(value, str)
                self.assertTrue(value.strip())
            self.assertIn(f"${name}", metadata["interface"]["default_prompt"])
            self.assertIs(
                metadata["policy"]["allow_implicit_invocation"],
                expected["implicit"],
            )
            self.assertNotIn("dependencies", metadata)
            runtime_text = operational_text(directory)
            for forbidden in (
                "disable-model-invocation",
                "argument-hint",
                "setup-matt-pocock-skills",
                "~/.cursor",
                "generalPurpose",
                "readonly:",
            ):
                self.assertNotIn(forbidden, runtime_text)

    def test_pinned_provenance_and_mit_licenses_are_complete(self) -> None:
        provenance = PROVENANCE_PATH.read_text(encoding="utf-8")
        for name, expected in EXPECTED_SKILLS.items():
            directory = SKILLS_ROOT / name
            source = (directory / "SOURCE.md").read_text(encoding="utf-8")
            license_path = directory / "LICENSE"
            license_text = license_path.read_text(encoding="utf-8")

            for required in (
                "https://github.com/mattpocock/skills",
                expected["upstream_path"],
                EXPECTED_REVISION,
                EXPECTED_RETRIEVAL_DATE,
                "## Local adaptations",
                "Updates are manual.",
            ):
                self.assertIn(required, source)
            for upstream_path, digest in expected["digests"].items():
                self.assertIn(f"`{upstream_path}`: `{digest}`", source)
            self.assertIn(
                f"Repository `LICENSE`: `{EXPECTED_LICENSE_DIGEST}`", source
            )
            self.assertEqual(sha256(license_path), EXPECTED_LICENSE_DIGEST)
            self.assertTrue(license_text.startswith("MIT License\n"))
            self.assertIn("Copyright (c) 2026 Matt Pocock", license_text)
            self.assertIn('THE SOFTWARE IS PROVIDED "AS IS"', license_text)
            for required in (
                f"## `{name}`",
                f"skills/{name}/SKILL.md",
                f"skills/{name}/LICENSE",
                f"skills/{name}/SOURCE.md",
                expected["upstream_path"],
                EXPECTED_REVISION,
            ):
                self.assertIn(required, provenance)

    def test_named_cross_skill_dependencies_resolve(self) -> None:
        for name in EXPECTED_SKILLS:
            self.assertEqual(unresolved_dependencies(SKILLS_ROOT, name), [])

        grill_me = operational_text(SKILLS_ROOT / "grill-me")
        grill_with_docs = operational_text(SKILLS_ROOT / "grill-with-docs")
        grilling = operational_text(SKILLS_ROOT / "grilling")
        self.assertIn("$grilling", grill_me)
        self.assertIn("$grilling", grill_with_docs)
        self.assertIn("$domain-modeling", grill_with_docs)
        self.assertIn("`unslop` skill", grilling)
        self.assertIn("`unslop` skill", grill_with_docs)

    def test_grill_me_dependency_check_fails_in_an_incomplete_catalog(self) -> None:
        with tempfile.TemporaryDirectory(prefix="grill-me-catalog-") as temporary:
            catalog = Path(temporary) / "skills"
            catalog.mkdir()
            shutil.copytree(SKILLS_ROOT / "grill-me", catalog / "grill-me")

            missing = unresolved_dependencies(catalog, "grill-me")
            self.assertEqual(missing, ["grilling"])
            with self.assertRaisesRegex(
                AssertionError,
                "grill-me has unresolved catalog dependencies: grilling",
            ):
                self.assertEqual(
                    missing,
                    [],
                    "grill-me has unresolved catalog dependencies: "
                    + ", ".join(missing),
                )

    def test_grilling_preserves_grouped_frontier_behavior(self) -> None:
        _, body = split_frontmatter(
            (SKILLS_ROOT / "grilling" / "SKILL.md").read_text(encoding="utf-8")
        )
        normalized = " ".join(body.split())

        for required in (
            "Map every unresolved decision and the prerequisites",
            "The current frontier contains every unresolved question whose prerequisites are settled",
            "Ask all independent frontier questions in one numbered group",
            "give a recommended answer and the evidence or reasoning behind it",
            "explain the observable consequence or acceptance boundary",
            "Recommendation:",
            "Observable consequence or acceptance boundary:",
            "A frontier group is incomplete if any item lacks",
            "A one-question round is valid only when the frontier contains one question",
            "Do not ask a dependent question in the same round as its unresolved prerequisite",
            "wait for the user's answers to the whole group",
            "recompute the tree and ask the new frontier",
            "Investigate facts available through authorized read-only",
            "Pending fact discovery defers only questions that depend on that fact",
        ):
            self.assertIn(required, normalized)

    def test_grilling_returns_decisions_and_stops_before_action(self) -> None:
        _, body = split_frontmatter(
            (SKILLS_ROOT / "grilling" / "SKILL.md").read_text(encoding="utf-8")
        )
        normalized = " ".join(body.split())

        for required in (
            "accepted decisions and their observable boundaries",
            "accepted assumptions",
            "unresolved questions, including blocked factual prerequisites",
            "This substep returns decisions and questions only",
            "Do not implement, edit documentation, update trackers or planning artifacts, branch, commit, merge, or publish inside it",
            "The consuming repository defines the owners of scope, dependencies, planning, and delivery",
            "return control to its coordinator",
            "questioning neither grants nor cancels the underlying request's authority",
        ):
            self.assertIn(required, normalized)

    def test_grill_me_is_only_a_small_explicit_alias(self) -> None:
        skill_text = (SKILLS_ROOT / "grill-me" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        frontmatter, body = split_frontmatter(skill_text)
        normalized = " ".join(body.split())

        self.assertIn("Use only when the user directly invokes grill-me", frontmatter["description"])
        self.assertIn("Load and follow the canonical `grilling` skill", normalized)
        self.assertIn("This alias contains no second interviewing method", normalized)
        self.assertIn("If `grilling` is unavailable, stop and report", normalized)
        self.assertLessEqual(len(body.split()), 90)
        self.assertNotRegex(body, r"(?m)^## ")
        self.assertNotRegex(body, r"(?m)^\d+\. ")

    def test_grill_with_docs_composes_without_immediate_writes(self) -> None:
        skill_text = (SKILLS_ROOT / "grill-with-docs" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        frontmatter, body = split_frontmatter(skill_text)
        normalized = " ".join(body.split())

        self.assertIn(
            "Use when explicitly requested by the user or composed by an authorized workflow",
            frontmatter["description"],
        )
        for required in (
            "Load and follow both `grilling` and `domain-modeling`",
            "Ask every independent current frontier question in one numbered group",
            "Wait for the user's answers to the whole group",
            "Keep dependent questions for later rounds",
            "During each round, collect without writing",
            "After the user confirms the decisions",
            "show every exact proposed path and change",
            "Write only when the underlying request explicitly authorizes those exact repository edits",
            "does not create tracker work, publish plans, or implement code",
            "The consuming repository defines the owners of scope, dependencies, planning, and delivery",
            "return the accepted decisions to its coordinator without discarding existing authority",
            "Do not transition, commit, merge, close, publish, or implement",
        ):
            self.assertIn(required, normalized)

    def test_prompt_selection_contract_is_discriminating(self) -> None:
        descriptions = {
            name: str(
                split_frontmatter(
                    (SKILLS_ROOT / name / "SKILL.md").read_text(encoding="utf-8")
                )[0]["description"]
            ).lower()
            for name in EXPECTED_SKILLS
        }

        for cue in ("grill", "stress-test", "pressure-test", "interrogate", "sharpen"):
            self.assertIn(cue, descriptions["grilling"])
        self.assertIn("do not use for ordinary planning or summarization", descriptions["grilling"])
        self.assertIn("directly invokes grill-me", descriptions["grill-me"])
        self.assertIn("explicitly requested by the user or composed by an authorized workflow", descriptions["grill-with-docs"])
        code_review_description = str(
            split_frontmatter(
                (SKILLS_ROOT / "code-review" / "SKILL.md").read_text(encoding="utf-8")
            )[0]["description"]
        ).lower()
        interrogate_description = str(
            split_frontmatter(
                (SKILLS_ROOT / "interrogate" / "SKILL.md").read_text(encoding="utf-8")
            )[0]["description"]
        ).lower()
        self.assertIn("explicit interrogate", code_review_description)
        self.assertIn("multi-review", code_review_description)
        self.assertIn("explicitly asks to interrogate", interrogate_description)

        selection_cases = {
            "Grill me on this service design": "grilling",
            "Stress-test this rollout plan": "grilling",
            "Interrogate this PR diff": "interrogate",
            "Use $grill-me on this service design": "grill-me",
            "Use $grill-with-docs on this design": "grill-with-docs",
            "Implement this approved story": None,
            "Summarize this finished plan": None,
        }
        grilling_cues = ("grill", "stress-test", "pressure-test", "interrogate", "sharpen")
        for prompt, expected in selection_cases.items():
            lowered = prompt.lower()
            if "$grill-with-docs" in lowered:
                selected = "grill-with-docs"
            elif "$grill-me" in lowered:
                selected = "grill-me"
            elif any(term in lowered for term in ("pr diff", "code change", "branch diff")):
                selected = "interrogate" if any(cue in lowered for cue in grilling_cues) else None
            elif any(cue in lowered for cue in grilling_cues) and any(
                subject in lowered for subject in ("plan", "decision", "architecture", "design")
            ):
                selected = "grilling"
            else:
                selected = None
            self.assertEqual(selected, expected, prompt)


if __name__ == "__main__":
    unittest.main()
