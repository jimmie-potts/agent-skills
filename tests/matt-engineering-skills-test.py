#!/usr/bin/env python3
"""Verify the adapted Matt Pocock engineering skills without running skill code."""

from __future__ import annotations
from pstack_skills import PSTACK_SKILLS

from collections import Counter
from dataclasses import dataclass
import hashlib
import re
import stat
import subprocess
import unittest
from pathlib import Path

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPOSITORY_ROOT / "skills"
PROVENANCE_PATH = REPOSITORY_ROOT / "PROVENANCE.md"
SKILL_NAMES = (
    "domain-modeling",
    "diagnosing-bugs",
    "code-review",
    "codebase-design",
    "research",
    "prototype",
)
UPSTREAM_REPOSITORY = "https://github.com/mattpocock/skills"
EXPECTED_REVISION = "5b15a47f2d7150f545fbcacbfe381787fc0230dc"
# Skills refreshed from a newer upstream revision: name -> (revision, retrieved).
REFRESHED_SOURCES = {
    "domain-modeling": ("49dd158d1076134a641b33efb035946536778336", "2026-10-17"),
}
EXPECTED_RETRIEVAL_DATE = "2026-08-23"

EXPECTED_LICENSE_BYTES = b"""MIT License

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
EXPECTED_LICENSE_DIGEST = "0e7ac423bf2c6e223b7c5b156f8cf72da49d748e56a1641402c31f22ad07dbb5"

EXPECTED_INVENTORIES = {
    "domain-modeling": {
        "LICENSE",
        "SKILL.md",
        "SOURCE.md",
        "agents/openai.yaml",
        "references/context.md",
        "references/decision-record-format.md",
    },
    "diagnosing-bugs": {
        "LICENSE",
        "SKILL.md",
        "SOURCE.md",
        "agents/openai.yaml",
        "scripts/hitl-loop.template.sh",
    },
    "code-review": {
        "LICENSE",
        "SKILL.md",
        "SOURCE.md",
        "agents/openai.yaml",
    },
    "codebase-design": {
        "LICENSE",
        "SKILL.md",
        "SOURCE.md",
        "agents/openai.yaml",
        "references/alternative-designs.md",
        "references/deepening.md",
    },
    "research": {
        "LICENSE",
        "SKILL.md",
        "SOURCE.md",
        "agents/openai.yaml",
    },
    "prototype": {
        "LICENSE",
        "SKILL.md",
        "SOURCE.md",
        "agents/openai.yaml",
        "references/logic.md",
        "references/ui.md",
    },
}

EXPECTED_POLICIES = {
    "domain-modeling": True,
    "diagnosing-bugs": True,
    "code-review": True,
    "codebase-design": True,
    "research": True,
    "prototype": False,
}

UPSTREAM_DIGESTS = {
    "domain-modeling": {
        "ADR-FORMAT.md": "944c92aa790e8fbdc9199640b170979abb8a34ba8d0fe18c2a01a63bce140ca0",
        "GLOSSARY-FORMAT.md": "21dcc40cdec8e151a829b98ab1517c1867bc444e3665134a98c6983411996801",
        "SKILL.md": "7b925d7b1e341a2eeae33ad68a8a8c0ab889a38ddd22a7598e4c240e5a7556a3",
        "agents/openai.yaml": "f6bf2aa996c6e6f53fdd0708e18a0d16a56aed8322cca59fedbe3c0d2c75f06b",
    },
    "diagnosing-bugs": {
        "SKILL.md": "77f3cf31bc99b2f49af943222526531fcc9fc41d047626d3640e875e85af3e84",
        "agents/openai.yaml": "3e430dbe4334a87597488c060cb3dc3786bb00c9182877d6f5ec41f62490e90b",
        "scripts/hitl-loop.template.sh": "35103539fc36873eea36074769ad454f9379d6fc8b2dc0e26ce987fd3bfe5503",
    },
    "code-review": {
        "SKILL.md": "47f4e52c21694def9c7c11cbfbf891ca35eac7a93e395797515be3c8a409ae50",
        "agents/openai.yaml": "8229ca854e11dc8e6aef2131ee03f31fb1561cf905fab9ccc325180cf3331352",
    },
    "codebase-design": {
        "DEEPENING.md": "f3dd099ce99289bd213914d8ee3e2429b78309c3957ca4583f7659551b1d53c1",
        "DESIGN-IT-TWICE.md": "8e740bf98446dbd4dfdc132ac4346d9a7eedaf93de6a495889171cf7f99f16bd",
        "SKILL.md": "2c20617f87ec8af6a434859f381b2f061a69b530444e74eb39e78bb016a6d1e2",
        "agents/openai.yaml": "edebc9e4fcfe102114012575eaa9600b9b5fd08c311664f389c36e7bc717740f",
    },
    "research": {
        "SKILL.md": "985569f15739c713d6784887c3d186d4ef9ac85bec5ad9c068d25bf0739928e4",
        "agents/openai.yaml": "9b4c470d63221c1f68f22df70b83e2f12401b317babe0d1b7b5f24a974474d0d",
    },
    "prototype": {
        "LOGIC.md": "f61c7d249e786a79ef289018901c348271e1798dd0b0bc5607b5c6f4d4a01ab9",
        "SKILL.md": "714de632d116bb73f65cdb5a882db15b9369a6713b9a47c0fad827848f0bfbe3",
        "UI.md": "723211e878acbc7b6ff09755263f3295cde724ba902ff0064da41eed51d45ad3",
        "agents/openai.yaml": "5af65e43ab41a350436697b81e27b7f848d36782043b73c322bb2c9fa9cc55dc",
    },
}

EXPECTED_LINKS = {
    "domain-modeling": {
        "references/context.md",
        "references/decision-record-format.md",
    },
    "diagnosing-bugs": {"scripts/hitl-loop.template.sh"},
    "code-review": set(),
    "codebase-design": {
        "references/alternative-designs.md",
        "references/deepening.md",
    },
    "research": set(),
    "prototype": {"references/logic.md", "references/ui.md"},
}

NAMED_SKILL_DEPENDENCIES = {
    "domain-modeling": {"unslop"},
    "diagnosing-bugs": {"tdd", "unslop"},
    "code-review": {"unslop"},
    "codebase-design": {"architect", "how", "why", "unslop"},
    "research": {"unslop"},
    "prototype": {"unslop"},
}


@dataclass(frozen=True)
class SelectionCase:
    skill: str
    positive_prompt: str
    expected_positive: str
    positive_term: str
    near_miss_prompt: str
    expected_near_miss: None
    exclusion_evidence: str


SELECTION_MATRIX = (
    SelectionCase(
        skill="domain-modeling",
        positive_prompt="Reconcile these overloaded order and booking domain terms.",
        expected_positive="domain-modeling",
        positive_term="domain terms",
        near_miss_prompt="Read CONTEXT.md so you use the right terminology.",
        expected_near_miss=None,
        exclusion_evidence="do not select merely to read existing vocabulary",
    ),
    SelectionCase(
        skill="diagnosing-bugs",
        positive_prompt="Diagnose why this request is slow.",
        expected_positive="diagnosing-bugs",
        positive_term="diagnose",
        near_miss_prompt="Implement the already-confirmed cache fix.",
        expected_near_miss=None,
        exclusion_evidence="diagnosis does not authorize a fix",
    ),
    SelectionCase(
        skill="code-review",
        positive_prompt="Review this pull request against the approved specification.",
        expected_positive="code-review",
        positive_term="review",
        near_miss_prompt="Summarize the changes in this branch.",
        expected_near_miss=None,
        exclusion_evidence="do not select for a plain change summary",
    ),
    SelectionCase(
        skill="codebase-design",
        positive_prompt="Design a testable seam for this module.",
        expected_positive="codebase-design",
        positive_term="seam",
        near_miss_prompt="Explain how this module works at runtime.",
        expected_near_miss=None,
        exclusion_evidence="how for current runtime explanation",
    ),
    SelectionCase(
        skill="research",
        positive_prompt="Research the current API limits using official sources.",
        expected_positive="research",
        positive_term="research",
        near_miss_prompt="Implement the client using these already supplied API docs.",
        expected_near_miss=None,
        exclusion_evidence="do not select for implementation from already supplied sources",
    ),
    SelectionCase(
        skill="prototype",
        positive_prompt="Use prototype to test whether this state model supports cancellation.",
        expected_positive="prototype",
        positive_term="prototype",
        near_miss_prompt="Show me three UI options.",
        expected_near_miss=None,
        exclusion_evidence="use only when the user directly invokes prototype",
    ),
)

MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def split_frontmatter(markdown: str) -> tuple[dict[str, object], str]:
    match = re.fullmatch(r"---\n(.*?)\n---\n(.*)", markdown, re.DOTALL)
    if match is None:
        raise AssertionError("SKILL.md must start with YAML frontmatter")
    frontmatter = yaml.safe_load(match.group(1))
    if not isinstance(frontmatter, dict):
        raise AssertionError("SKILL.md frontmatter must be a mapping")
    return frontmatter, match.group(2)


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def expected_directories(files: set[str]) -> set[str]:
    directories: set[str] = set()
    for relative_file in files:
        parent = Path(relative_file).parent
        while parent != Path("."):
            directories.add(parent.as_posix())
            parent = parent.parent
    return directories


class MattEngineeringSkillsTest(unittest.TestCase):
    def test_skills_have_closed_regular_file_inventories(self) -> None:
        for name, expected_files in EXPECTED_INVENTORIES.items():
            with self.subTest(skill=name):
                skill_root = SKILLS_ROOT / name
                self.assertTrue(skill_root.is_dir())
                self.assertFalse(skill_root.is_symlink())

                entries = list(skill_root.rglob("*"))
                for entry in entries:
                    self.assertFalse(entry.is_symlink(), f"{entry} must not be a symlink")
                    self.assertTrue(
                        entry.is_file() or entry.is_dir(),
                        f"{entry} must be a regular file or directory",
                    )

                actual_files = {
                    path.relative_to(skill_root).as_posix()
                    for path in entries
                    if path.is_file()
                }
                actual_directories = {
                    path.relative_to(skill_root).as_posix()
                    for path in entries
                    if path.is_dir()
                }
                self.assertEqual(actual_files, expected_files)
                self.assertEqual(actual_directories, expected_directories(expected_files))

    def test_frontmatter_and_codex_metadata_are_portable(self) -> None:
        for name in SKILL_NAMES:
            with self.subTest(skill=name):
                skill_root = SKILLS_ROOT / name
                skill_text = (skill_root / "SKILL.md").read_text(encoding="utf-8")
                frontmatter, _ = split_frontmatter(skill_text)
                metadata_text = (skill_root / "agents" / "openai.yaml").read_text(
                    encoding="utf-8"
                )
                metadata = yaml.safe_load(metadata_text)

                self.assertEqual(sorted(frontmatter), ["description", "name"])
                self.assertEqual(frontmatter["name"], name)
                self.assertIsInstance(frontmatter["description"], str)
                self.assertTrue(str(frontmatter["description"]).strip())

                self.assertEqual(sorted(metadata), ["interface", "policy"])
                self.assertEqual(
                    sorted(metadata["interface"]),
                    ["default_prompt", "display_name", "short_description"],
                )
                for value in metadata["interface"].values():
                    self.assertIsInstance(value, str)
                    self.assertTrue(value.strip())
                self.assertIn(f"${name}", metadata["interface"]["default_prompt"])
                self.assertEqual(
                    sorted(metadata["policy"]), ["allow_implicit_invocation"]
                )
                self.assertIs(
                    metadata["policy"]["allow_implicit_invocation"],
                    EXPECTED_POLICIES[name],
                )

                runtime_metadata = f"{skill_text}\n{metadata_text}".lower()
                self.assertNotIn("disable-model-invocation", runtime_metadata)
                self.assertNotIn("cursor", runtime_metadata)
                self.assertNotIn("dependencies:", metadata_text.lower())

    def test_pinned_source_pairs_and_mit_license_bytes(self) -> None:
        provenance = PROVENANCE_PATH.read_text(encoding="utf-8")
        self.assertEqual(
            hashlib.sha256(EXPECTED_LICENSE_BYTES).hexdigest(),
            EXPECTED_LICENSE_DIGEST,
        )

        for name, expected_digests in UPSTREAM_DIGESTS.items():
            with self.subTest(skill=name):
                skill_root = SKILLS_ROOT / name
                source = (skill_root / "SOURCE.md").read_text(encoding="utf-8")
                revision, retrieved = REFRESHED_SOURCES.get(
                    name, (EXPECTED_REVISION, EXPECTED_RETRIEVAL_DATE)
                )

                self.assertIn(f"Upstream repository: `{UPSTREAM_REPOSITORY}`", source)
                self.assertIn(
                    f"Upstream path: `skills/engineering/{name}/`", source
                )
                self.assertIn(f"Pinned source revision: `{revision}`", source)
                self.assertIn(f"Retrieved: `{retrieved}`", source)
                self.assertIn("Updates are manual.", source)

                for relative_path, digest in expected_digests.items():
                    self.assertIn(f"- `{relative_path}`: `{digest}`", source)
                self.assertIn(
                    f"Repository `LICENSE`: `{EXPECTED_LICENSE_DIGEST}`", source
                )

                recorded_digests = Counter(
                    re.findall(r"`([0-9a-f]{64})`", source)
                )
                expected_recorded = Counter(
                    [*expected_digests.values(), EXPECTED_LICENSE_DIGEST]
                )
                self.assertEqual(recorded_digests, expected_recorded)
                self.assertEqual(
                    (skill_root / "LICENSE").read_bytes(), EXPECTED_LICENSE_BYTES
                )
                for required in (
                    f"## `{name}`",
                    f"skills/{name}/SKILL.md",
                    f"skills/{name}/LICENSE",
                    f"skills/{name}/SOURCE.md",
                    f"skills/engineering/{name}/",
                    revision,
                ):
                    self.assertIn(required, provenance)

    def test_all_local_markdown_links_and_named_dependencies_resolve(self) -> None:
        for name in SKILL_NAMES:
            with self.subTest(skill=name):
                skill_root = SKILLS_ROOT / name
                skill_text = (skill_root / "SKILL.md").read_text(encoding="utf-8")
                for expected_link in EXPECTED_LINKS[name]:
                    self.assertIn(f"]({expected_link})", skill_text)

                for markdown_path in skill_root.rglob("*.md"):
                    markdown = markdown_path.read_text(encoding="utf-8")
                    for raw_target in MARKDOWN_LINK.findall(markdown):
                        target = raw_target.strip().strip("<>").split("#", 1)[0]
                        if not target or re.match(r"^[a-z][a-z0-9+.-]*:", target):
                            continue
                        self.assertFalse(
                            Path(target).is_absolute(),
                            f"{markdown_path} uses nonportable absolute link {target}",
                        )
                        resolved = (markdown_path.parent / target).resolve()
                        try:
                            resolved.relative_to(skill_root.resolve())
                        except ValueError as error:
                            self.fail(f"{markdown_path} links outside its skill: {target}: {error}")
                        self.assertTrue(
                            resolved.is_file(),
                            f"{markdown_path} has unresolved link {target}",
                        )

                body = skill_text.lower()
                dollar_dependencies = set(re.findall(r"\$([a-z][a-z0-9-]+)", body))
                for dependency in (dollar_dependencies | NAMED_SKILL_DEPENDENCIES[name]) - PSTACK_SKILLS:
                    self.assertTrue(
                        (SKILLS_ROOT / dependency / "SKILL.md").is_file(),
                        f"{name} depends on missing catalog skill {dependency}",
                    )
                for dependency in NAMED_SKILL_DEPENDENCIES[name]:
                    self.assertRegex(
                        body,
                        rf"(?<![a-z0-9-])\$?{re.escape(dependency)}(?![a-z0-9-])",
                    )

    def test_runtime_files_have_no_setup_dependency_or_cursor_metadata(self) -> None:
        for name in SKILL_NAMES:
            with self.subTest(skill=name):
                skill_root = SKILLS_ROOT / name
                runtime_files = [
                    path
                    for path in skill_root.rglob("*")
                    if path.is_file() and path.name not in {"SOURCE.md", "LICENSE"}
                ]
                runtime_text = "\n".join(
                    path.read_text(encoding="utf-8") for path in runtime_files
                ).lower()
                self.assertNotIn("setup-matt-pocock-skills", runtime_text)
                self.assertNotIn("disable-model-invocation", runtime_text)
                self.assertNotIn("cursor", runtime_text)

        code_review_source = (
            SKILLS_ROOT / "code-review" / "SOURCE.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "The dependency on `setup-matt-pocock-skills`", code_review_source
        )
        self.assertIn("were removed", code_review_source)

    def test_hitl_template_is_parse_only_and_cannot_capture_free_form_secrets(self) -> None:
        script_path = (
            SKILLS_ROOT
            / "diagnosing-bugs"
            / "scripts"
            / "hitl-loop.template.sh"
        )
        script = script_path.read_text(encoding="utf-8")

        syntax = subprocess.run(
            ["bash", "-n", str(script_path)],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(syntax.returncode, 0, syntax.stderr)
        self.assertEqual(stat.S_IMODE(script_path.stat().st_mode) & 0o111, 0)

        self.assertIn("set -euo pipefail", script)
        self.assertIn("Output-only human-in-the-loop reproduction template", script)
        self.assertIn("reads no standard input, arguments, or", script)
        self.assertIn("report only yes, no, or unclear", script)
        self.assertNotIn("read ", script)
        self.assertNotIn("read\t", script)
        self.assertNotIn("mapfile", script)
        self.assertNotIn("select ", script)
        self.assertNotIn("$", script)

        for forbidden in (
            "eval ",
            "source ",
            "$(",
            "`",
            "curl ",
            "wget ",
            "ssh ",
            "scp ",
            "nc ",
            "printenv",
            "set -x",
            "history",
            "http://",
            "https://",
            "ERROR_MSG",
            "Export",
            "capture()",
            "Paste the error message",
            "read -r -p",
        ):
            self.assertNotIn(forbidden, script)
        self.assertIn("Complete authentication directly in", script)
        self.assertIn("the target application", script)

        operational_lines = [
            line.strip()
            for line in script.splitlines()
            if line.strip() and not line.startswith("#")
        ]
        self.assertEqual(operational_lines[0], "set -euo pipefail")
        self.assertTrue(
            all(
                re.fullmatch(r"printf '[^']*'", line)
                for line in operational_lines[1:]
            )
        )

    def test_prompt_level_selection_matrix_matches_descriptions_and_policies(self) -> None:
        positive_description_evidence = {
            "domain-modeling": "use when the user is defining, reconciling, or proposing changes to domain terms",
            "diagnosing-bugs": "use when the user asks to diagnose or debug",
            "code-review": "use when the user asks for a code review or findings on a change",
            "codebase-design": "use for focused code-structure and interface design work",
            "research": "use when the user requests source-backed research",
            "prototype": "use only when the user directly invokes prototype",
        }
        self.assertEqual({case.skill for case in SELECTION_MATRIX}, set(SKILL_NAMES))
        for case in SELECTION_MATRIX:
            with self.subTest(skill=case.skill):
                skill_root = SKILLS_ROOT / case.skill
                frontmatter, _ = split_frontmatter(
                    (skill_root / "SKILL.md").read_text(encoding="utf-8")
                )
                description = str(frontmatter["description"]).lower()
                metadata = yaml.safe_load(
                    (skill_root / "agents" / "openai.yaml").read_text(
                        encoding="utf-8"
                    )
                )

                self.assertEqual(case.expected_positive, case.skill)
                self.assertIsNone(case.expected_near_miss)
                self.assertIn(case.positive_term, case.positive_prompt.lower())
                self.assertIn(positive_description_evidence[case.skill], description)
                self.assertIn(case.exclusion_evidence, description)
                self.assertNotIn(f"${case.skill}", case.near_miss_prompt.lower())
                self.assertIs(
                    metadata["policy"]["allow_implicit_invocation"],
                    EXPECTED_POLICIES[case.skill],
                )

                if EXPECTED_POLICIES[case.skill]:
                    self.assertNotIn(f"${case.skill}", case.positive_prompt.lower())
                else:
                    self.assertIn(case.skill, case.positive_prompt.lower())

        code_review_description = str(
            split_frontmatter(
                (SKILLS_ROOT / "code-review" / "SKILL.md").read_text(encoding="utf-8")
            )[0]["description"]
        ).lower()
        self.assertIn("explicit interrogate or adversarial multi-review request", code_review_description)
        self.assertIn("explicit blast-radius or breakage-risk request", code_review_description)

        codebase_description = str(
            split_frontmatter(
                (SKILLS_ROOT / "codebase-design" / "SKILL.md").read_text(encoding="utf-8")
            )[0]["description"]
        ).lower()
        self.assertIn("ownership or layering placement", codebase_description)
        self.assertIn("architectural critique", codebase_description)

        selection_contract = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")
        for prompt, expected in (
            ("Interrogate this PR diff", "interrogate"),
            ("Review this small diff I do not trust; what could it break?", "blast-radius"),
            ("Where should rate limiting live?", "how"),
            ("Critique this module boundary", "how"),
        ):
            self.assertIn(f"| `{prompt}` | Select `{expected}`", selection_contract)


if __name__ == "__main__":
    unittest.main()
