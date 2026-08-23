# Agent Skills

`agent-skills` is the canonical authoring repository for reusable Agent Skills
that should work in both Codex and Claude Code. A skill is maintained once under
`skills/` and can be exposed to either local agent through one symlink per
selected skill.

This repository provides local authoring, validation, testing, status, install,
and uninstall workflows for WSL/Linux. It is not a plugin, marketplace, custom
registry, cloud-sync service, automatic updater, or organization-wide
distribution system. Project-specific skills should remain in the project that
uses them.

The catalog currently contains:

- [`architect`](skills/architect/SKILL.md), an explicit design-first code
  architecture workflow;
- [`arena`](skills/arena/SKILL.md), an explicit parallel-candidate synthesis
  workflow;
- [`blast-radius`](skills/blast-radius/SKILL.md), an explicit change-risk
  analysis workflow;
- [`how`](skills/how/SKILL.md), a code-flow and architecture explainer;
- [`interrogate`](skills/interrogate/SKILL.md), an explicit independent
  adversarial-review workflow;
- [`teach`](skills/teach/SKILL.md), a layered code and design lesson workflow;
- [`tdd`](skills/tdd/SKILL.md), an explicit failing-test-first bug-fix workflow;
- [`technical-writing`](skills/technical-writing/SKILL.md), an explicit technical
  prose drafting and review standard;
- [`unslop`](skills/unslop/SKILL.md), an editorial workflow for narrative prose;
- [`why`](skills/why/SKILL.md), an evidence-based design-rationale investigator.

Their licenses and source records travel with each skill, and root-level
provenance is recorded in [`PROVENANCE.md`](PROVENANCE.md). The examples under
`tests/fixtures/` are validation fixtures, not installable catalog entries.

## Prerequisites

- Bash, Python 3, and standard GNU/Linux utilities such as `find`, `realpath`,
  `readlink`, `sha256sum`, `stat`, and `ln`
- The development dependency used for YAML validation. Install it in a local
  virtual environment so distributions with a protected system Python remain
  untouched:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

The manager never installs packages or executes scripts bundled in a skill.

## Skill format

Each non-hidden direct child of `skills/` is one complete skill:

```text
skills/<skill-name>/
├── SKILL.md                 # required
├── agents/
│   └── openai.yaml          # optional Codex metadata
├── scripts/                 # optional deterministic helpers
├── references/              # optional detail loaded when needed
└── assets/                  # optional templates or output resources
```

`SKILL.md` begins with portable YAML frontmatter containing only `name` and
`description`, followed by nonempty Markdown instructions:

```markdown
---
name: example-skill
description: Perform a specific workflow. Use when the user asks for that workflow.
---

# Example Skill

Follow the workflow in a concise, imperative form.
```

Names use lowercase letters, digits, and single hyphens, are shorter than 64
characters, and exactly match the directory name. Keep `SKILL.md` at or below
500 lines. Put substantial optional detail in a directly linked file such as
`references/policy.md`, and create only resource directories the skill uses.

Do not add a per-skill README, changelog, duplicated host-specific copy, secret,
credential, generated cache, or machine-specific configuration.

## Add a skill

1. Create `skills/<skill-name>/SKILL.md` using the format above.
2. Add only the scripts, references, assets, or optional
   `agents/openai.yaml` that the workflow actually needs.
3. Review the complete directory, especially executable helpers and tool
   permissions.
4. Run all checks:

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

Validate an isolated catalog root with:

```bash
python3 scripts/validate-skills.py --skills-dir /path/to/catalog
```

The supplied path must contain skill directories as direct children; it is not
the path to an individual `SKILL.md`.

## Manage local skills

The command requires an explicit agent. Install and uninstall also require
either `--all` or one or more skill names; omission never means “all.”

```bash
./scripts/manage-skills.sh validate
./scripts/manage-skills.sh status --agent codex
./scripts/manage-skills.sh status --agent claude
./scripts/manage-skills.sh status --agent both

./scripts/manage-skills.sh install --agent codex <skill-name>
./scripts/manage-skills.sh install --agent claude <skill-name>
./scripts/manage-skills.sh install --agent both <skill-name>
./scripts/manage-skills.sh install --agent both --all

./scripts/manage-skills.sh install --agent both --dry-run <skill-name>
./scripts/manage-skills.sh uninstall --agent both --dry-run <skill-name>
./scripts/manage-skills.sh uninstall --agent both <skill-name>
```

Defaults:

| Agent | Personal destination | Explicit invocation |
| --- | --- | --- |
| Codex | `~/.agents/skills/<skill-name>` | `$skill-name` |
| Claude Code | `~/.claude/skills/<skill-name>` | `/skill-name` |

Both hosts may also select a skill automatically when its description matches
the request. If a newly created top-level skills directory is not detected,
restart the relevant local agent.

For tests or an intentional advanced setup, override the roots without changing
`HOME`:

```bash
CODEX_SKILLS_DIR=/tmp/codex-skills \
CLAUDE_SKILLS_DIR=/tmp/claude-skills \
./scripts/manage-skills.sh install --agent both --dry-run <skill-name>
```

`AGENT_SKILLS_SOURCE_DIR` can point the manager at an isolated catalog, which
the test suite uses. Normal use leaves it unset so the source is this
repository's `skills/` directory.

Installation validates the whole source catalog before any destination change.
It creates absolute, per-skill symlinks and is idempotent when the correct link
already exists. It refuses regular files, directories, dangling links, and
foreign links; version one intentionally has no `--force`. Uninstall removes
only an exact symlink that resolves to the corresponding canonical source.

Status classifies each catalog entry as correctly installed, missing, a
conflicting regular file or directory, a foreign symlink, or a broken owned
symlink. It also finds owned links left dangling after their source skill is
removed. Missing optional skills do not make status fail; validation errors and
conflicts do.

## Personal, project-local, and cloud availability

Personal symlinks are local to this WSL machine. Codex discovers them under
`~/.agents/skills/`; Claude Code discovers them under `~/.claude/skills/`.
Cloud agents cannot follow links to this machine.

For a repository-local or cloud-visible snapshot, choose the relevant host and
copy real files into only that host's project directory.

Codex project or cloud:

```bash
mkdir -p /path/to/project/.agents/skills
if [[ ! -e /path/to/project/.agents/skills/<skill-name> && ! -L /path/to/project/.agents/skills/<skill-name> ]]; then
  cp -a -- skills/<skill-name> /path/to/project/.agents/skills/<skill-name>
else
  printf 'Conflict: Codex target already exists; preserved.\n' >&2
fi
```

Claude project or cloud, as an alternative:

```bash
mkdir -p /path/to/project/.claude/skills
if [[ ! -e /path/to/project/.claude/skills/<skill-name> && ! -L /path/to/project/.claude/skills/<skill-name> ]]; then
  cp -a -- skills/<skill-name> /path/to/project/.claude/skills/<skill-name>
else
  printf 'Conflict: Claude target already exists; preserved.\n' >&2
fi
```

If the same target project genuinely needs both hosts, keep one real in-project
copy and add an internal relative symlink for the other host. Both Codex and
Claude Code support symlinked skill directories:

```bash
mkdir -p /path/to/project/.agents/skills /path/to/project/.claude/skills
if [[ ! -e /path/to/project/.agents/skills/<skill-name> && ! -L /path/to/project/.agents/skills/<skill-name> ]]; then
  cp -a -- skills/<skill-name> /path/to/project/.agents/skills/<skill-name>
  if [[ ! -e /path/to/project/.claude/skills/<skill-name> && ! -L /path/to/project/.claude/skills/<skill-name> ]]; then
    ln -s -- ../../.agents/skills/<skill-name> /path/to/project/.claude/skills/<skill-name>
  else
    printf 'Conflict: Claude target already exists; preserved.\n' >&2
  fi
else
  printf 'Conflict: canonical project target already exists; preserved.\n' >&2
fi
```

Commit `.agents/skills/<skill-name>/` for Codex cloud or
`.claude/skills/<skill-name>/` for Claude cloud only when that target project
needs the skill. A dual-host internal symlink must resolve to real files inside
the same repository. Never commit a symlink whose target is outside the target
repository, and never maintain separate real Codex and Claude copies of one
shared skill. These are deliberate export snapshots; refresh the one real copy
from the canonical catalog. Plugin or account distribution is deferred.

## Security and provenance

Treat every skill as an executable agent dependency even when it contains only
instructions:

- Review the entire directory before adding or updating it, including scripts,
  assets, references, metadata, and requested permissions.
- Never commit secrets, credentials, private exports, `.env` files, generated
  caches, or machine-specific configuration.
- Do not let a skill override host sandbox, approval, or permission policy.
- Give deployment, deletion, messaging, purchasing, and production-operation
  skills explicit-only invocation controls when the host supports them.
- Re-review third-party content whenever its pinned source version changes. Do
  not update it automatically.

Third-party skill sources, licenses, and pinned Git commits are recorded in
[`PROVENANCE.md`](PROVENANCE.md). Add an entry when a third-party skill enters
the catalog, and remove the record if the catalog no longer contains any
third-party skills.

## Official documentation

- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills)
- [Anthropic: Extend Claude with skills](https://code.claude.com/docs/en/skills)
- [Agent Skills specification](https://agentskills.io/specification)

Host discovery behavior can change; verify paths against these sources before
changing the manager defaults.
