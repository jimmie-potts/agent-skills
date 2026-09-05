#!/usr/bin/env python3
"""Verify the pinned Matt Pocock productivity skills without executing skill code."""

from __future__ import annotations

import hashlib
import re
import unittest
from pathlib import Path

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPOSITORY_ROOT / "skills"
PROVENANCE_PATH = REPOSITORY_ROOT / "PROVENANCE.md"
HANDOFF_DIRECTORY = SKILLS_ROOT / "handoff"
LEARNING_DIRECTORY = SKILLS_ROOT / "learning-workspace"
TEACH_DIRECTORY = SKILLS_ROOT / "teach"
EXPECTED_REVISION = "5b15a47f2d7150f545fbcacbfe381787fc0230dc"
EXPECTED_LICENSE_DIGEST = "0e7ac423bf2c6e223b7c5b156f8cf72da49d748e56a1641402c31f22ad07dbb5"
EXPECTED_MATT_LICENSE = b"""MIT License

Copyright (c) 2026 Matt Pocock

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

EXPECTED_UPSTREAM_FILES = {
    "handoff": {
        "SKILL.md": "7c62de979fdc7ac32fb5ddb2146156c917f80ee070d30fadc9d40343c4b6ed25",
        "agents/openai.yaml": "5c479fd562c691851690e8b18c8501045bef0943c10743d636b2fae26add1d28",
    },
    "learning-workspace": {
        "GLOSSARY-FORMAT.md": "9b99859ec28437668130d8f2ce5a342938970f8a1ed4fd38c3eab4f4b5fff210",
        "LEARNING-RECORD-FORMAT.md": "701fa34b6748aa89e6c960ffb815257f481a7d77fb2900f9028f7edf3fdd6052",
        "MISSION-FORMAT.md": "8cacbb3c0644d3ae0ea4965564797099401a6930a23f7cf462918576587f2418",
        "RESOURCES-FORMAT.md": "e9cacf34026e11a8d1c8f9de88abe5bcbf654f4ebdb25cae8c0de0d5f48f44ec",
        "SKILL.md": "a32df9dcdfc0c4fdc1c98e1ed3940c5f56b84c1aa90ff60346f32b8b53915b43",
        "agents/openai.yaml": "5856f3ae8aec742f1499c640aecdd5f1d6af5fa210a7c6ec794de8263a6f733f",
    },
}

EXPECTED_TEACH_DIGESTS = {
    "LICENSE": "bc957ca6bee02792566a1a028d105e02e247c6e77cf057061674273da77b200e",
    "SKILL.md": "40d6beaf69e7790b2472d2010d0685738a9be05b7d0dbd53f00d5be7eb1f64af",
    "SOURCE.md": "4af2279d1a000bb47801deb6fb030e25773ecaaf7764127b2818220786b26618",
    "agents/openai.yaml": "cf6a8b25789ca5dc538b30618c587d33377e4bca6fa9d3ce2e709d87f6b31e5f",
}


def split_frontmatter(markdown: str) -> tuple[dict[str, object], str]:
    match = re.fullmatch(r"---\n(.*?)\n---\n(.*)", markdown, re.DOTALL)
    if match is None:
        raise AssertionError("SKILL.md must start with YAML frontmatter")
    frontmatter = yaml.safe_load(match.group(1))
    if not isinstance(frontmatter, dict):
        raise AssertionError("SKILL.md frontmatter must be a mapping")
    return frontmatter, match.group(2)


def read_skill(directory: Path) -> tuple[dict[str, object], str]:
    return split_frontmatter((directory / "SKILL.md").read_text(encoding="utf-8"))


def read_metadata(directory: Path) -> dict[str, object]:
    metadata = yaml.safe_load((directory / "agents" / "openai.yaml").read_text(encoding="utf-8"))
    if not isinstance(metadata, dict):
        raise AssertionError("agents/openai.yaml must be a mapping")
    return metadata


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize(text: str) -> str:
    return " ".join(text.split())


class MattProductivitySkillsTest(unittest.TestCase):
    def assert_closed_inventory(
        self,
        directory: Path,
        *,
        files: set[str],
        directories: set[str],
    ) -> None:
        actual_paths = {
            path.relative_to(directory).as_posix()
            for path in directory.rglob("*")
        }
        actual_files = {
            path.relative_to(directory).as_posix()
            for path in directory.rglob("*")
            if path.is_file()
        }
        actual_directories = {
            path.relative_to(directory).as_posix()
            for path in directory.rglob("*")
            if path.is_dir()
        }
        self.assertEqual(actual_paths, files | directories)
        self.assertEqual(actual_files, files)
        self.assertEqual(actual_directories, directories)
        for relative_path in files | directories:
            self.assertFalse((directory / relative_path).is_symlink())

    def test_closed_regular_file_inventories(self) -> None:
        self.assert_closed_inventory(
            HANDOFF_DIRECTORY,
            files={"LICENSE", "SKILL.md", "SOURCE.md", "agents/openai.yaml"},
            directories={"agents"},
        )
        self.assert_closed_inventory(
            LEARNING_DIRECTORY,
            files={
                "LICENSE",
                "SKILL.md",
                "SOURCE.md",
                "agents/openai.yaml",
                "references/glossary.md",
                "references/learning-record.md",
                "references/mission.md",
                "references/resources.md",
            },
            directories={"agents", "references"},
        )

    def test_frontmatter_and_codex_metadata_are_portable_and_explicit_only(self) -> None:
        for directory, expected_name in (
            (HANDOFF_DIRECTORY, "handoff"),
            (LEARNING_DIRECTORY, "learning-workspace"),
        ):
            frontmatter, _ = read_skill(directory)
            metadata = read_metadata(directory)

            self.assertEqual(sorted(frontmatter), ["description", "name"])
            self.assertEqual(frontmatter["name"], expected_name)
            self.assertIsInstance(frontmatter["description"], str)
            self.assertTrue(str(frontmatter["description"]).strip())
            self.assertIn("Use only when the user directly invokes", str(frontmatter["description"]))
            self.assertEqual(sorted(metadata), ["interface", "policy"])
            self.assertEqual(
                sorted(metadata["interface"]),
                ["default_prompt", "display_name", "short_description"],
            )
            self.assertIn(f"${expected_name}", metadata["interface"]["default_prompt"])
            self.assertEqual(metadata["policy"], {"allow_implicit_invocation": False})
            runtime_text = "\n".join(
                path.read_text(encoding="utf-8")
                for path in directory.rglob("*")
                if path.is_file() and path.name not in {"SOURCE.md", "LICENSE"}
            )
            for forbidden in (
                "disable-model-invocation",
                "argument-hint",
                "setup-matt-pocock-skills",
                "~/.cursor",
                "generalPurpose",
                "readonly:",
            ):
                self.assertNotIn(forbidden, runtime_text)

    def test_pinned_sources_and_exact_mit_license_bytes(self) -> None:
        provenance = PROVENANCE_PATH.read_text(encoding="utf-8")
        source_expectations = (
            (HANDOFF_DIRECTORY, "skills/productivity/handoff/", EXPECTED_UPSTREAM_FILES["handoff"]),
            (
                LEARNING_DIRECTORY,
                "skills/productivity/teach/",
                EXPECTED_UPSTREAM_FILES["learning-workspace"],
            ),
        )
        for directory, upstream_path, expected_files in source_expectations:
            source = (directory / "SOURCE.md").read_text(encoding="utf-8")
            self.assertIn("https://github.com/mattpocock/skills", source)
            self.assertIn(upstream_path, source)
            self.assertIn(EXPECTED_REVISION, source)
            for upstream_file, digest in expected_files.items():
                self.assertIn(f"`{upstream_file}`: `{digest}`", source)
            self.assertIn(f"Repository `LICENSE`: `{EXPECTED_LICENSE_DIGEST}`", source)
            self.assertIn("Updates are manual.", source)
            self.assertEqual((directory / "LICENSE").read_bytes(), EXPECTED_MATT_LICENSE)
            self.assertEqual(sha256(directory / "LICENSE"), EXPECTED_LICENSE_DIGEST)
            name = directory.name
            for required in (
                f"## `{name}`",
                f"skills/{name}/SKILL.md",
                f"skills/{name}/LICENSE",
                f"skills/{name}/SOURCE.md",
                upstream_path,
                EXPECTED_REVISION,
            ):
                self.assertIn(required, provenance)

    def test_all_references_and_named_skill_dependencies_resolve(self) -> None:
        _, handoff_body = read_skill(HANDOFF_DIRECTORY)
        _, learning_body = read_skill(LEARNING_DIRECTORY)

        expected_references = {
            "references/glossary.md",
            "references/learning-record.md",
            "references/mission.md",
            "references/resources.md",
        }
        linked_references = set(re.findall(r"\]\((references/[^)#]+\.md)\)", learning_body))
        self.assertEqual(linked_references, expected_references)
        for reference in linked_references:
            self.assertTrue((LEARNING_DIRECTORY / reference).is_file())

        dependencies = {
            "handoff": {"unslop"},
            "learning-workspace": {"how", "teach", "unslop"},
        }
        for dependency in dependencies["handoff"]:
            self.assertIn(f"`{dependency}` skill", handoff_body)
            self.assertTrue((SKILLS_ROOT / dependency / "SKILL.md").is_file())
        for dependency in dependencies["learning-workspace"]:
            marker = f"`{dependency}` skill" if dependency == "unslop" else f"`{dependency}`"
            self.assertIn(marker, learning_body)
            self.assertTrue((SKILLS_ROOT / dependency / "SKILL.md").is_file())

    def test_handoff_captures_verified_state_and_bounds_native_tool_effects(self) -> None:
        _, body = read_skill(HANDOFF_DIRECTORY)
        normalized = normalize(body)
        for required in (
            "repository path and worktree path",
            "issue identifier and full title when one is present",
            "branch name",
            "frozen `HEAD` commit or other immutable comparison identifier",
            "dirty state and the paths of relevant tracked and untracked changes",
            "authority granted, authority explicitly absent, and required approvals",
            "blockers, risks, assumptions, and unresolved decisions",
            "exact verification commands and their pass, fail, or unavailable results",
            "Return the complete snapshot in the response by default",
            "Use a host's native context-transfer operation only when the user authorizes that transfer to an identified recipient",
            "the documented tool behavior matches the requested effects",
            "Moving Git state, interrupting a task, or starting work requires authorization for those effects",
            "Write a handoff file only when the user authorizes an exact destination",
        ):
            self.assertIn(required, normalized)
        self.assertIn("a tool named handoff is not sufficient", normalized)
        self.assertIn("nonauthoritative and time-bound", normalized)
        self.assertIn("Use `<REDACTED>`", normalized)

    def test_handoff_preserves_authority_and_avoids_automatic_effects(self) -> None:
        _, body = read_skill(HANDOFF_DIRECTORY)
        normalized = normalize(body)
        for required in (
            "This skill grants no authority to change the repository, trackers, delivery records, Git state, personal files, or external systems",
            "A handoff transfers context and existing authority boundaries; it does not broaden them",
            "Do not create a temporary file automatically",
            "Do not transition an issue, comment, label, branch, commit, merge, publish, close, install, or start the next workflow",
        ):
            self.assertIn(required, normalized)

    def test_learning_workspace_requires_an_exact_approved_root_for_every_write(self) -> None:
        _, body = read_skill(LEARNING_DIRECTORY)
        normalized = normalize(body)
        for required in (
            "Ask the user to name an exact teaching directory and explicitly approve it for this workspace",
            "Do not create or edit any file before that approval",
            "An explicit invocation of this skill alone is not directory approval",
            "Before every write, confirm the target remains inside that root and does not escape through a symlink or parent path",
            "Keep all missions, resources, lessons, references, assets, notes, glossaries, and learning records inside the approved teaching workspace",
        ):
            self.assertIn(required, normalized)

    def test_learning_workspace_uses_cited_sources_without_browser_or_community_automation(self) -> None:
        _, body = read_skill(LEARNING_DIRECTORY)
        normalized = normalize(body)
        resources = normalize(
            (LEARNING_DIRECTORY / "references" / "resources.md").read_text(encoding="utf-8")
        )
        for required in (
            "Prefer primary sources, peer-reviewed work, official documentation, recognized experts with cited evidence",
            "Cite material claims in lessons and reference documents",
            "Do not rely on uncited model memory for claims that guide instruction",
            "Do not automatically delegate questions to communities or contact anyone",
            "Do not open a lesson automatically",
        ):
            self.assertIn(required, normalized)
        self.assertIn("grants no authority to install dependencies, open a browser, contact or delegate to a community", normalized)
        self.assertIn("Do not contact, join, post to, or delegate to any community", resources)

    def test_learning_workspace_is_a_rename_distinct_from_teach(self) -> None:
        learning_source = (LEARNING_DIRECTORY / "SOURCE.md").read_text(encoding="utf-8")
        learning_frontmatter, learning_body = read_skill(LEARNING_DIRECTORY)
        teach_frontmatter, teach_body = read_skill(TEACH_DIRECTORY)

        for required in (
            "Upstream path: `skills/productivity/teach/`",
            "Upstream name: `teach`",
            "Local name: `learning-workspace`",
            "renamed `learning-workspace`",
            "existing pstack-derived `teach`",
        ):
            self.assertIn(required, learning_source)
        self.assertEqual(learning_frontmatter["name"], "learning-workspace")
        self.assertEqual(teach_frontmatter["name"], "teach")
        self.assertIn("stateful teaching workspace", learning_body)
        self.assertIn("Return the explanation itself", teach_body)
        self.assertNotIn("approved teaching directory", teach_body)

    def test_pstack_teach_inventory_and_adapted_bytes_are_pinned(self) -> None:
        self.assert_closed_inventory(
            TEACH_DIRECTORY,
            files={"LICENSE", "SKILL.md", "SOURCE.md", "agents/openai.yaml"},
            directories={"agents"},
        )
        for relative_path, expected_digest in EXPECTED_TEACH_DIGESTS.items():
            self.assertEqual(sha256(TEACH_DIRECTORY / relative_path), expected_digest)

    def test_prompt_selection_contract_keeps_both_workflows_explicit_only(self) -> None:
        metadata = {
            "handoff": read_metadata(HANDOFF_DIRECTORY),
            "learning-workspace": read_metadata(LEARNING_DIRECTORY),
            "teach": read_metadata(TEACH_DIRECTORY),
        }

        def selected(prompt: str, skill_name: str) -> bool:
            explicit_tokens = (f"${skill_name}", f"/{skill_name}")
            if any(token in prompt for token in explicit_tokens):
                return True
            return bool(metadata[skill_name]["policy"]["allow_implicit_invocation"])

        cases = (
            ("Use $handoff to prepare this task for the named Codex recipient.", {"handoff"}),
            ("Summarize this finished conversation.", set()),
            ("Use $learning-workspace to teach me Rust over several sessions.", {"learning-workspace"}),
            ("Explain how this parser handles errors.", set()),
            ("Teach me how this codebase was shaped.", set()),
            ("Use $teach to explain how this code works.", {"teach"}),
        )
        for prompt, expected in cases:
            actual = {skill_name for skill_name in metadata if selected(prompt, skill_name)}
            self.assertEqual(actual, expected, prompt)

        handoff_description = str(read_skill(HANDOFF_DIRECTORY)[0]["description"])
        learning_description = str(read_skill(LEARNING_DIRECTORY)[0]["description"])
        self.assertIn("identifies or authorizes the recipient context", handoff_description)
        self.assertIn("do not select for a one-off code explanation", learning_description)
        self.assertIn("ordinary teaching conversation", learning_description)


if __name__ == "__main__":
    unittest.main()
