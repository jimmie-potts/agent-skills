#!/usr/bin/env python3
"""Verify portable Pi discovery without requiring Pi in CI."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPOSITORY_ROOT / "skills"
README_PATH = REPOSITORY_ROOT / "README.md"
HOST_COMMAND_PATTERN = re.compile(r"\$[a-z][a-z0-9-]*|/skill:[a-z]")


def catalog_names() -> list[str]:
    return sorted(
        path.name
        for path in SKILLS_ROOT.iterdir()
        if path.is_dir() and not path.name.startswith(".")
    )


def portable_markdown_paths() -> list[Path]:
    paths = list(SKILLS_ROOT.glob("*/SKILL.md"))
    paths.extend(SKILLS_ROOT.glob("*/references/*.md"))
    return sorted(paths)


def pi_package_directory() -> Path | None:
    configured = os.environ.get("PI_CODING_AGENT_PACKAGE_DIR")
    if configured:
        return Path(configured).expanduser().resolve()

    pi_binary = shutil.which("pi")
    if pi_binary is None:
        return None
    resolved_binary = Path(pi_binary).resolve()
    if resolved_binary.parent.name != "dist":
        return None
    return resolved_binary.parent.parent


class PiSkillsTest(unittest.TestCase):
    def test_portable_instructions_do_not_embed_host_skill_commands(self) -> None:
        for path in portable_markdown_paths():
            text = path.read_text(encoding="utf-8")
            self.assertIsNone(
                HOST_COMMAND_PATTERN.search(text),
                f"{path} must compose skills by name, not host command syntax",
            )

    def test_readme_documents_pi_discovery_and_limitations(self) -> None:
        readme = README_PATH.read_text(encoding="utf-8")
        normalized = " ".join(readme.split())

        for required in (
            "Codex, Claude Code, and Pi",
            "| Pi | `~/.agents/skills/<skill-name>` | `/skill:<skill-name>` |",
            "The manager has no separate `--agent pi` option",
            "Pi's `/reload` command",
            "Pi must have a separate orchestration extension or package",
            "`architect` can still compare alternatives in one pass",
        ):
            self.assertIn(required, normalized)

    def test_pi_default_resource_loader_accepts_the_complete_catalog(self) -> None:
        package_directory = pi_package_directory()
        if package_directory is None:
            self.skipTest(
                "Pi is unavailable; set PI_CODING_AGENT_PACKAGE_DIR for the loader smoke test"
            )

        index_path = package_directory / "dist" / "index.js"
        self.assertTrue(index_path.is_file(), f"Pi package is missing {index_path}")
        node_binary = shutil.which("node")
        self.assertIsNotNone(node_binary, "Pi loader smoke test requires node")

        script = """
const { DefaultResourceLoader } = await import(process.env.PI_INDEX_URL);
const loader = new DefaultResourceLoader({
  cwd: process.env.SKILLS_REPOSITORY,
  agentDir: process.env.PI_TEST_AGENT_DIR,
  additionalSkillPaths: [process.env.PI_SKILLS_ROOT],
  noSkills: true,
  noExtensions: true,
  noPromptTemplates: true,
  noThemes: true,
  noContextFiles: true,
});
await loader.reload();
const result = loader.getSkills();
console.log(JSON.stringify({
  names: result.skills.map((skill) => skill.name).sort(),
  diagnostics: result.diagnostics,
}));
"""
        with tempfile.TemporaryDirectory(prefix="pi-skill-loader.") as agent_dir:
            environment = os.environ.copy()
            environment.update(
                {
                    "PI_INDEX_URL": index_path.as_uri(),
                    "SKILLS_REPOSITORY": str(REPOSITORY_ROOT),
                    "PI_TEST_AGENT_DIR": agent_dir,
                    "PI_SKILLS_ROOT": str(SKILLS_ROOT),
                }
            )
            result = subprocess.run(
                [node_binary, "--input-type=module", "-e", script],
                cwd=REPOSITORY_ROOT,
                env=environment,
                check=True,
                capture_output=True,
                text=True,
            )

        loaded = json.loads(result.stdout)
        self.assertEqual(loaded["names"], catalog_names())
        self.assertEqual(loaded["diagnostics"], [])


if __name__ == "__main__":
    unittest.main()
