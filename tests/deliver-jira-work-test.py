#!/usr/bin/env python3
"""Static delivery-skill contracts; not simulated decisions or host discovery."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "deliver-jira-work"
ENTRY = SKILL / "SKILL.md"
DISCOVERY = SKILL / "references" / "project-discovery.md"
SCENARIOS = SKILL / "references" / "validation-scenarios.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


class DeliverJiraWorkStaticTest(unittest.TestCase):
    def test_closed_instruction_only_inventory(self) -> None:
        self.assertEqual(
            sorted(str(path.relative_to(SKILL)) for path in SKILL.rglob("*")
                   if path.is_file()),
            ["SKILL.md", "agents/openai.yaml", "references/project-discovery.md",
             "references/validation-scenarios.md"],
        )
        for path in SKILL.rglob("*"):
            self.assertFalse(path.is_symlink(), str(path))
        self.assertLessEqual(len(ENTRY.read_text().splitlines()), 500)

    def test_explicit_invocation_and_portable_frontmatter(self) -> None:
        match = re.fullmatch(r"---\n(.*?)\n---\n(.+)", ENTRY.read_text(), re.DOTALL)
        self.assertIsNotNone(match)
        frontmatter = yaml.safe_load(match.group(1))
        self.assertEqual(sorted(frontmatter), ["description", "name"])
        self.assertEqual(frontmatter["name"], "deliver-jira-work")
        description = frontmatter["description"]
        for phrase in ("only when the user explicitly invokes", "named issue",
                       "planning", "investigation", "review-only",
                       "ordinary implementation"):
            self.assertIn(phrase, description)
        metadata = yaml.safe_load((SKILL / "agents" / "openai.yaml").read_text())
        self.assertEqual(sorted(metadata), ["interface", "policy"])
        self.assertEqual(metadata["policy"], {"allow_implicit_invocation": False})
        self.assertIn("$deliver-jira-work", metadata["interface"]["default_prompt"])

    def test_references_have_conditional_entrypoint_pointers(self) -> None:
        entry = normalized(ENTRY)
        self.assertIn("For an unfamiliar project, changed policy", entry)
        self.assertIn("references/project-discovery.md", entry)
        self.assertIn("When evaluating or revising this skill", entry)
        self.assertIn("references/validation-scenarios.md", entry)
        for target in re.findall(r"\]\((references/[^)]+)\)", ENTRY.read_text()):
            self.assertTrue((SKILL / target).is_file(), target)

    def test_operating_rules_do_not_pin_a_consuming_project(self) -> None:
        operating = normalized(ENTRY) + " " + normalized(DISCOVERY)
        for forbidden in ("Notification Service", "notification-service", "NS-",
                          "GitHub", "github.com", "origin/main", "`main`",
                          "In Progress", "In Review", "`Done`", "gpt-",
                          "Sprint Delivery"):
            self.assertNotIn(forbidden, operating)
        for phrase in ("hosting provider", "actual target branch",
                       "required fields", "risk classification",
                       "model and reasoning settings", "completion conditions"):
            self.assertIn(phrase, operating)

    def test_authority_is_not_inferred_from_workflow(self) -> None:
        entry = normalized(ENTRY)
        for rule in (
            "The coordinating root owns repository writes",
            "Workers return proposed patches, reviews, or evidence without performing durable effects",
            "A planning-only invocation authorizes no delivery effects",
            "Do not change sprint membership or lifecycle",
            "Leave dirty or stale shared checkouts untouched",
            "Reuse verified, authorized existing work without duplicating its PR",
            "Existing authorization covers routine in-scope repairs",
            "Use OpenSpec only when the project requires it",
            "Missing policy requires a concrete decision request before the work it governs",
        ):
            self.assertIn(rule, entry)

    def test_revision_and_completion_gates_remain_inline(self) -> None:
        entry = normalized(ENTRY)
        for rule in (
            "Freeze base SHA, head SHA, merge-base, diff command",
            "fresh independent read-only review of that comparison",
            "A self-review or unavailable independent review cannot enable merge",
            "Read all pages of provider reviews",
            "this PR's exact current head",
            "A new commit, changed target, conflict resolution, or scope change invalidates affected validation and review",
            "Require the candidate to include the current target",
            "expected-head guard or equivalent atomic precondition",
            "retain the appropriate Jira state and report the checkpoint and owner",
            "do not merge or declare the issue complete",
            "read back status and resolution as applicable",
            "immutable published revision",
        ):
            self.assertIn(rule, entry)

    def test_uncertain_effects_require_authoritative_reconciliation(self) -> None:
        entry = normalized(ENTRY)
        for rule in (
            "Record each consequential effect's intent, object, expected prior state",
            "Reconcile an uncertain effect before any recovery attempt",
            "A delayed or stale read alone does not prove absence",
            "If applied, continue from verified state without repeating the effect",
            "If verified not applied, retry only within existing authority and project recovery policy",
            "Reconcile a partial effect",
            "If unknown or recovery exceeds scope, request the specific decision needed",
        ):
            self.assertIn(rule, entry)

    def test_scenarios_and_evidence_categories_are_explicit(self) -> None:
        text = SCENARIOS.read_text()
        headings = re.findall(r"^## Case (\d+): (.+)$", text, re.MULTILINE)
        self.assertEqual([number for number, _ in headings],
                         [str(number) for number in range(1, 13)])
        self.assertIn("Withhold the evaluator checks", normalized(SCENARIOS))
        for category in ("Static checks", "Simulated decisions", "Actual discovery"):
            self.assertIn(category, text)
        self.assertIn("Supplying the SKILL.md body in a prompt or parsing YAML is not discovery evidence",
                      normalized(SCENARIOS))
        self.assertIn("## Evaluator checks", text)

    def test_check_lists_and_selection_examples_are_wired(self) -> None:
        command = "python3 tests/deliver-jira-work-test.py"
        for path in (ROOT / "AGENTS.md", ROOT / "README.md",
                     ROOT / ".github" / "workflows" / "validate.yml"):
            self.assertIn(command, path.read_text(), str(path))
        readme = (ROOT / "README.md").read_text()
        for prompt in ("$deliver-jira-work DEMO-21", "ready PR only",
                       "Plan how to deliver DEMO-21", "planning only"):
            self.assertIn(prompt, readme)


if __name__ == "__main__":
    unittest.main()
