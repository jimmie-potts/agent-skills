#!/usr/bin/env python3
"""Check packaging, inert report markup, and the behavioral fixtures' premises."""

from html.parser import HTMLParser
import hashlib
from pathlib import Path
import re
import subprocess
import sys
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/improve-codebase-architecture"
FIXTURES = ROOT / "tests/fixtures/architecture-review"


class ReportMarkup(HTMLParser):
    """Check the shipped static example; not a sanitizer for arbitrary HTML."""

    TAGS = {
        "html", "head", "meta", "title", "style", "body", "main", "header",
        "article", "section", "footer", "h1", "h2", "h3", "p", "span", "div",
        "figure", "figcaption", "svg", "desc", "rect", "text", "path", "dl",
        "dt", "dd", "code", "ul", "li", "strong",
    }

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.errors = []
        self.ids = set()
        self.labels = []
        self.text = []
        self.svg_count = 0

    def handle_starttag(self, tag, attrs):
        if tag not in self.TAGS:
            self.errors.append(f"Active or unsupported element: {tag}")
        values = dict(attrs)
        if tag == "meta" and values.get("http-equiv", "").lower() == "refresh":
            self.errors.append("Meta refresh")
        for key, value in attrs:
            if key.startswith("on") or key in {"src", "href", "xlink:href", "srcdoc"}:
                self.errors.append(f"Active or resource attribute: {key}")
            if key == "id":
                if value in self.ids:
                    self.errors.append(f"Duplicate ID: {value}")
                self.ids.add(value)
            if key == "aria-labelledby":
                self.labels.extend(value.split())
        if tag == "svg":
            self.svg_count += 1
            if not all(values.get(key) for key in ("viewbox", "role", "aria-labelledby")):
                self.errors.append("SVG needs dimensions and an accessible name")

    def handle_data(self, data):
        self.text.append(data)


def inspect_report(text):
    parser = ReportMarkup()
    parser.feed(text)
    parser.close()
    parser.errors.extend(f"Missing label: {label}" for label in parser.labels
                         if label not in parser.ids)
    if re.search(r"@import\b|url\s*\(|expression\s*\(", text, re.IGNORECASE):
        parser.errors.append("Active or remote CSS")
    return parser


class ArchitectureReviewTests(unittest.TestCase):
    def test_portable_package_and_explicit_codex_adapter(self):
        text = (SKILL / "SKILL.md").read_text()
        metadata = yaml.safe_load(text.split("---", 2)[1])
        self.assertEqual(set(metadata), {"name", "description"})
        self.assertEqual(metadata["name"], SKILL.name)
        self.assertLessEqual(len(text.splitlines()), 500)
        adapter = yaml.safe_load((SKILL / "agents/openai.yaml").read_text())
        self.assertIs(adapter["policy"]["allow_implicit_invocation"], False)
        self.assertIn("$improve-codebase-architecture", adapter["interface"]["default_prompt"])
        self.assertFalse((SKILL / "scripts").exists())
        self.assertEqual({str(p.relative_to(SKILL)) for p in SKILL.rglob("*") if p.is_file()}, {
            "SKILL.md", "SOURCE.md", "LICENSE", "agents/openai.yaml",
            "references/report.md", "references/validation-scenarios.md", "assets/report.html",
        })

    def test_referenced_resources_are_used_and_local(self):
        pending, visited = [SKILL / "SKILL.md"], set()
        while pending:
            path = pending.pop().resolve()
            if path in visited:
                continue
            visited.add(path)
            for link in re.findall(r"\]\(([^)]+)\)", path.read_text()):
                if "://" in link or link.startswith("#"):
                    continue
                target = (path.parent / link.split("#")[0]).resolve()
                self.assertTrue(target.is_relative_to(SKILL.resolve()), link)
                self.assertTrue(target.is_file(), link)
                pending.append(target)
        expected = set((SKILL / "references").glob("*.md")) | set((SKILL / "assets").glob("*"))
        self.assertTrue({p.resolve() for p in expected} <= visited)

    def test_license_and_source_record(self):
        digest = hashlib.sha256((SKILL / "LICENSE").read_bytes()).hexdigest()
        self.assertEqual(digest, "0e7ac423bf2c6e223b7c5b156f8cf72da49d748e56a1641402c31f22ad07dbb5")
        source = (SKILL / "SOURCE.md").read_text()
        self.assertIn(digest, source)
        self.assertIn("3cca18b368ae95cdbdebbff572ccafa662551015", source)
        self.assertIn("skills/improve-codebase-architecture/SOURCE.md", (ROOT / "PROVENANCE.md").read_text())

    def test_check_wiring(self):
        for relative in ("README.md", "AGENTS.md", ".github/workflows/validate.yml"):
            self.assertIn("python3 tests/improve-codebase-architecture-test.py", (ROOT / relative).read_text())
            self.assertIn("node tests/architecture-report-browser-test.cjs", (ROOT / relative).read_text())

    def test_report_is_offline_inert_and_labeled(self):
        report = inspect_report((SKILL / "assets/report.html").read_text())
        self.assertEqual(report.errors, [])
        self.assertEqual(report.svg_count, 2)

    def test_report_contract_rejects_active_content(self):
        for markup in (
            '<script src="https://example.invalid/cdn.js"></script>',
            '<svg onload="alert(1)"></svg>',
            '<svg><foreignObject>active</foreignObject></svg>',
            '<meta http-equiv="refresh" content="0;url=https://example.invalid">',
            '<style>@import "https://example.invalid/style.css";</style>',
            '<style>body { background: url(https://example.invalid/a); }</style>',
        ):
            with self.subTest(markup=markup):
                self.assertTrue(inspect_report(markup).errors)

    def test_escaped_hostile_label_remains_text(self):
        from html import escape
        label = '</text><script>alert("x")</script><svg onload="alert(2)">&'
        markup = '<p>' + escape(label, quote=True) + '</p>'
        parsed = inspect_report(markup)
        self.assertEqual(parsed.errors, [])
        self.assertEqual("".join(parsed.text), label)

    def test_coupled_fixture_exposes_gap_despite_passing_existing_tests(self):
        result = subprocess.run([sys.executable, "-B", "-m", "unittest", "test_commerce"],
                                cwd=FIXTURES / "coupled", capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        probe = subprocess.run([sys.executable, "-B", "-c",
            "from checkout import checkout; from invoice import invoice; "
            "assert checkout([5000]) == {'total_cents': 5000}; "
            "assert invoice([5000]) == {'amount_due': 5500}"],
            cwd=FIXTURES / "coupled", capture_output=True, text=True)
        self.assertEqual(probe.returncode, 0, probe.stderr)

    def test_healthy_and_guarded_fixture_checks_pass(self):
        for case in ("healthy", "guarded"):
            result = subprocess.run([sys.executable, "-B", "-m", "unittest", "discover"],
                                    cwd=FIXTURES / case, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
