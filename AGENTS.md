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
python3 tests/interrogate-test.py
python3 tests/pstack-analysis-skills-test.py
python3 tests/pstack-workflow-skills-test.py
python3 tests/unslop-test.py
bash -n scripts/manage-skills.sh
bash -n tests/manage-skills-test.sh
bash tests/manage-skills-test.sh
```

Do not execute scripts bundled in catalog skills merely to validate them.
