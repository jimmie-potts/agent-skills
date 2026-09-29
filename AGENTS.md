# Agent Skills Repository

This repository is the canonical source for reusable, portable Agent Skills used
locally by Codex and Claude Code. Keep project-specific skills in the project
that owns them. Plugin publishing, remote distribution, automatic updates, and
organization-wide governance are out of scope.

## Catalog rules

- Put each production skill at `skills/<skill-name>/SKILL.md`. Direct children
  of `skills/` must be complete skill directories; test fixtures are not catalog
  entries.
- Use lowercase ASCII letters, digits, and single hyphens. Names must be shorter
  than 64 characters, and the directory name must match frontmatter `name`.
- Keep portable `SKILL.md` frontmatter to nonempty `name` and `description`.
  The description must say what the skill does and when it should trigger.
- Write concise, imperative instructions. Put substantial conditional detail in
  directly referenced files under `references/` rather than growing an
  oversized `SKILL.md`; keep `SKILL.md` at or below 500 lines.
- Add only resources the skill uses. Do not add a per-skill `README.md`,
  changelog, duplicated documentation, secrets, caches, or machine-specific data.
- Keep shared skills portable between Codex and Claude. If host-specific behavior
  is unavoidable, document a narrow adapter instead of changing the shared
  implementation silently.
- Treat scripts and requested tool permissions as security-sensitive. Review
  their full behavior and permission scope explicitly before accepting them.
- Preserve unrelated user changes.

## Installation

- A merged change that adds, changes, renames or removes a skill under
  `skills/` is complete only after it is installed and its readback passes.
  Changes that touch only tests, scripts, fixtures or documentation need no
  installation. An issue may instead mark a skill change source-only, with a
  reason and a link to the install issue that batches it; that issue then
  closes at merge, and the install issue carries the installation.
- Ask the owner at a checkpoint before the fast-forward or install, unless the
  delivery request names that step. Such a request covers only a step that
  installs or updates its own change's skills. Present the step at the
  checkpoint anyway when it would uninstall, rename or retire any skill,
  including the change's own, install any other skill, or bring other merged
  skill changes whose installation still awaits an owner's decision. Approval
  covers only the step presented. If the owner declines or is unavailable,
  the issue stays open, with installation pending and its owner and next
  action recorded.
- Before updating, installing or checking the installed catalog, read the
  README's installed-catalog update section,
  [Update the installed catalog](README.md#update-the-installed-catalog).

## Review requirements

This project requires host-enforced reviewer tool restriction on Claude Code, a
mandatory control in `review-work`'s reviewer execution preflight. A Standards,
Specification or specialist reviewer that a Claude Code coordinator launches
with its `Agent` tool must use the `review-work-reviewer` or
`review-work-reviewer-high` profile, and host evidence for that reviewer must
show that its tools exclude `Agent`, editing tools, `Skill` and MCP tools, as
`review-work`'s Claude Code adapter describes. Without that evidence, the axis
is `incomplete`. The profile keeps `Bash`, so file writes, publication and
agents launched through the shell stay instruction-only; record them that way. A
packet-only process reviewer under `review-work`'s separate-process adapter
meets this requirement once host evidence verifies its empty tool set, as that
adapter requires. On Codex, restriction stays instruction-only until a surface
can select the named profile, as the Codex adapter records. Evidence:
[#80](https://github.com/jimmie-potts/agent-skills/issues/80) and
[#108](https://github.com/jimmie-potts/agent-skills/issues/108).

## Checks

Create and activate a local virtual environment once before running the checks:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

Then run:

```bash
python3 scripts/validate-skills.py
python3 tests/architect-test.py
python3 tests/blast-radius-test.py
python3 tests/close-work-test.py
python3 tests/deliver-work-test.py
python3 tests/plan-work-test.py
python3 tests/review-work-test.py
python3 tests/improve-codebase-architecture-test.py
python3 tests/pairing-skills-test.py
python3 tests/workflow-evaluation-test.py
python3 tests/grilling-skills-test.py
python3 tests/interrogate-test.py
python3 tests/matt-engineering-skills-test.py
python3 tests/matt-productivity-skills-test.py
python3 tests/pi-skills-test.py
python3 tests/pstack-analysis-skills-test.py
python3 tests/pstack-workflow-skills-test.py
python3 tests/unslop-test.py
python3 tests/writing-for-agents-test.py
bash -n scripts/manage-skills.sh
bash -n tests/manage-skills-test.sh
bash tests/manage-skills-test.sh
git diff --check
```

Do not execute scripts bundled in catalog skills merely to validate them.

For changes to the architecture report example or its browser check, also run
`node tests/architecture-report-browser-test.cjs` with Playwright 1.62.1 and
Chromium available. `NODE_PATH` may point to an existing dependency directory;
`ARCHITECTURE_REPORT_CHROMIUM` may select an available executable, and
`ARCHITECTURE_REPORT_OUTPUT` may select an authorized artifact directory.
Do not install into personal directories merely to run this check. If local
browser execution is unavailable, report the limit and require the hosted
`architecture-report` job and its screenshots before claiming render acceptance.
