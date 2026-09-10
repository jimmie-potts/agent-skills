# Agent Skills

`agent-skills` is the canonical authoring repository for reusable Agent Skills
that should work in Codex, Claude Code, and Pi. A skill is maintained once under
`skills/` and can be exposed to local agents through one symlink per selected
skill.

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
- [`codebase-design`](skills/codebase-design/SKILL.md), focused interface, seam,
  locality, and testability design guidance;
- [`improve-codebase-architecture`](skills/improve-codebase-architecture/SKILL.md),
  an explicit, evidence-backed review that ranks module improvements before
  detailed design and supports offline visual reports;
- [`diagnosing-bugs`](skills/diagnosing-bugs/SKILL.md), a red-capable,
  evidence-first diagnosis workflow;
- [`grill-me`](skills/grill-me/SKILL.md), an explicit compatibility alias for
  `grilling`;
- [`handoff`](skills/handoff/SKILL.md), an explicit verified continuation
  snapshot;
- [`how`](skills/how/SKILL.md), a code-flow and architecture explainer;
- [`interrogate`](skills/interrogate/SKILL.md), an explicit independent
  adversarial-review workflow;
- [`learning-workspace`](skills/learning-workspace/SKILL.md), an explicit
  source-backed workspace for sustained learning;
- [`plan-jira-sprints`](skills/plan-jira-sprints/SKILL.md), agent-driven sprint
  planning and approved Jira issue updates with human-owned sprint setup;
- [`prototype`](skills/prototype/SKILL.md), an explicit bounded experiment or
  functional delivery-slice workflow;
- [`research`](skills/research/SKILL.md), source-backed investigation with
  claim-level citations;
- [`worker-with-astra`](skills/worker-with-astra/SKILL.md), a Terra or Sol worker with the
  original Astra agent providing approach feedback, blocker advice, and final
  review through a verified host adapter;
- [`teach`](skills/teach/SKILL.md), a layered code and design lesson workflow;
- [`tdd`](skills/tdd/SKILL.md), explicit or deliberately composed incremental
  TDD for bugs and features;
- [`technical-writing`](skills/technical-writing/SKILL.md), an explicit technical
  prose drafting and review standard;
- [`unslop`](skills/unslop/SKILL.md), an editorial workflow for narrative prose;
- [`why`](skills/why/SKILL.md), an evidence-based design-rationale investigator;
- [`worker-with-fable`](skills/worker-with-fable/SKILL.md), a Haiku, Sonnet, or
  Opus worker with the original Fable agent providing approach feedback,
  blocker advice, and final review through Claude Code subagent tools; the
  Claude Code counterpart of `worker-with-astra`;
- [`writing-for-agents`](skills/writing-for-agents/SKILL.md), guidance for
  reliable skills, `AGENTS.md`, and conditional instruction references.

Reusable SDLC workflows also include:

- [`plan-work`](skills/plan-work/SKILL.md), explicit requirements definition and
  authorized GitHub/Jira publication with assessments and acceptance evidence.
  It reads the installed `deliver-work` package's canonical
  `references/work-assessment.md` without invoking delivery, and composes
  `grill-with-docs` for material unresolved decisions. A bounded read-only
  investigation may compose the host's advisory pairing. Install those
  dependencies when using this planner; missing resources are reported, never
  copied;
- [`grill-with-docs`](skills/grill-with-docs/SKILL.md), which composes
  [`grilling`](skills/grilling/SKILL.md) and
  [`domain-modeling`](skills/domain-modeling/SKILL.md) for grouped decisions and
  documentation proposals;
- [`code-review`](skills/code-review/SKILL.md), separate Standards and
  Specification reviews against one fixed comparison;
- [`deliver-work`](skills/deliver-work/SKILL.md), explicit delivery of
  one Jira issue, GitHub issue, or document requirement using the owning
  project's planning, hosting, review, and completion policy. It supports a
  ready-PR-only limit and requires no specific specification framework;
  it assesses verification needs and selects implementation/reviewer settings
  from available host capabilities. It may compose the host's advisory pairing
  for bounded implementation with checkpoints, `worker-with-astra` under Codex
  collaboration tools or `worker-with-fable` under Claude Code subagent tools,
  choosing by verified host tooling rather than by request wording; install the
  applicable skill separately when using the optional pairing. Advisory
  inspection never replaces its two independent delivery reviews;
- the six OpenSpec 1.12.0 core workflows: `openspec-propose`, `openspec-explore`,
  `openspec-apply-change`, `openspec-update-change`, `openspec-sync-specs`, and
  `openspec-archive-change`. They use the consuming repository's pinned CLI.

A repository can deliberately compose the existing explicit-only TDD and
Grill with Docs methods without changing their global invocation switches.
Repository instructions must name that composition and preserve the underlying
request's action boundaries. A context pointer does not change host discovery
or install a missing skill.

Third-party licenses and source records travel with their skills. Root-level
provenance is recorded in [`PROVENANCE.md`](PROVENANCE.md). The examples under
`tests/fixtures/` are validation fixtures, not installable catalog entries.

## Selection contract

The focused tests treat these prompts as the intended selection boundary. This
table documents the contract; it is not evidence that a fresh host session ran
the prompts.

| Prompt | Intended result |
| --- | --- |
| Explicit `$plan-work`, proposal only | Define assessed work and planned acceptance evidence without writes. |
| Explicit `$plan-work`, define and publish these outcomes | Settle requirements, publish authorized GitHub/Jira work, verify readbacks, and stop before implementation. |
| `How might we improve this?` | Do not select the explicit-only plan-work workflow. |
| `Grill me on this service design` | Select `grilling` and ask all currently independent questions as one group. |
| `Stress-test this rollout plan` | Select `grilling`. |
| Explicit `$grill-me` | Select `grill-me`, which loads `grilling` and adds no second method. |
| Explicit `$grill-with-docs` | Compose `grilling` and `domain-modeling`; collect proposals without immediate writes. |
| `Implement this approved story` | Do not select `grilling`. |
| `Review the completed sprint, refine the next one, and forecast the following sprint` | Select `plan-jira-sprints`; propose changes before any unauthorized writes. |
| `Apply the Jira issue changes from the approved sprint plan` | Select `plan-jira-sprints`; preserve human ownership of sprint creation and metadata. |
| `Implement DEMO-21 and open its PR` | Do not select `plan-jira-sprints` or start sprint planning. |
| Explicit `$deliver-work owner/repo#418` or an issue URL | Resolve the GitHub issue and owning code repository; use established tracking conventions. |
| Explicit `$deliver-work docs/requirements.md#REQ-17` | Use the requirement as scope without creating a tracker. |
| Explicit `$deliver-work 418` | Resolve only with an unambiguous tracker and namespace; otherwise ask. |
| Explicit `$deliver-work DEMO-21` | Discover the owning project and deliver that issue within the user's authority and project gates. |
| `$deliver-work DEMO-21, ready PR only` | Stop at the ready PR and its required handoff evidence; retain the appropriate tracking state. |
| `Plan how to deliver DEMO-21` | Do not select `deliver-work` or start delivery effects. |
| `$deliver-work DEMO-21, planning only` | Read the skill's authority boundary and produce read-only planning; do not implement or update tracking. |
| `Implement this approved Jira story` | Do not implicitly select `deliver-work`; it requires explicit invocation. |
| `Summarize this finished plan` | Do not start a grilling session. |
| `Read CONTEXT.md so you use the right terminology` | Select neither `domain-modeling` nor `grill-with-docs`. |
| `Resolve whether Account means tenant or login identity` | Select `domain-modeling`. |
| Explicit `$improve-codebase-architecture` | Review bounded scope, rank evidenced candidates or recommend no change, then let the user select. |
| `Explain or critique this subsystem` | Select `how`; do not select the explicit architecture improvement workflow. |
| `Design a testable seam for this module` | Select `codebase-design`; a runtime explanation selects `how`. |
| `Diagnose why this request is slow` | Select `diagnosing-bugs`; implementing a confirmed fix does not. |
| `Review this pull request against its specification` | Select `code-review`; a plain change summary does not. |
| `Interrogate this PR diff` | Select `interrogate`, not `code-review`, because the explicit adversarial multi-review request takes precedence. |
| `Review this small diff I do not trust; what could it break?` | Select `blast-radius`, not `code-review`, because explicit breakage-risk analysis takes precedence. |
| `Where should rate limiting live?` | Select `how` Placement, not `codebase-design`. |
| `Critique this module boundary` | Select `how` Critique, not `codebase-design`. |
| `Research the current API limits using official sources` | Select `research`; implementation from supplied sources does not. |
| Explicit `$prototype`, `$handoff`, or `$learning-workspace` | Select only the named explicit workflow; nearby ordinary requests do not. |
| `Explain how this parser handles errors` | Do not select `learning-workspace`. |

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

The offline architecture report has a separate browser check:
`node tests/architecture-report-browser-test.cjs`. It needs Playwright 1.62.1
and Chromium. An existing package directory can be selected with `NODE_PATH`,
an existing browser with `ARCHITECTURE_REPORT_CHROMIUM`, and a temporary output
directory with `ARCHITECTURE_REPORT_OUTPUT`. CI provisions these dependencies
in its temporary workspace and retains desktop/mobile screenshots and a result
receipt. Local browser unavailability is reported, not counted as a pass; the
hosted `architecture-report` job supplies that acceptance evidence.

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
python3 tests/deliver-work-test.py
python3 tests/plan-work-test.py
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

Defaults and discovery:

| Agent | Personal destination | Explicit invocation |
| --- | --- | --- |
| Codex | `~/.agents/skills/<skill-name>` | `$skill-name` |
| Claude Code | `~/.claude/skills/<skill-name>` | `/skill-name` |
| Pi | `~/.agents/skills/<skill-name>` | `/skill:<skill-name>` |

All three hosts may also select a skill automatically when its description
matches the request. Pi discovers the same `~/.agents/skills/` destination as
Codex, so a skill installed with `--agent codex` is available to both hosts.
The manager has no separate `--agent pi` option because it would address the
same links. After adding or changing skills, use Pi's `/reload` command or
restart the relevant local agent.

Pi can also load this catalog for one session without installing links:

```bash
pi --skill /path/to/agent-skills/skills
```

For persistent direct loading, add the catalog path to the `skills` array in
`~/.pi/agent/settings.json`. See Pi's
[skill documentation](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/skills.md)
for its discovery, trust, and collision rules.

`arena` and `interrogate` need genuine independent candidate or reviewer
sessions. Pi must have a separate orchestration extension or package that
provides that capability. Without one, those skills report the limitation
instead of presenting repeated work from one reasoning pass as independent.
`architect` can still compare alternatives in one pass and must disclose that
fallback.

`improve-codebase-architecture` uses the existing `codebase-design` skill and
conditionally `grilling` or `grill-with-docs` with `domain-modeling`. Keep those
companions available through supported discovery. A missing companion blocks
only its dependent phase; the workflow does not install it. It can investigate
sequentially and return Markdown when sub-agents, report writing, or browser
preview are unavailable.

The shared package requires explicit invocation in its description and body.
Codex additionally enforces selection through `agents/openai.yaml`. Claude Code
and Pi support native `disable-model-invocation` frontmatter, but this catalog
keeps its shared entrypoint to `name` and `description`; explicit-only behavior
there is an instruction contract, not a native invocation switch or permission
boundary. Verify host behavior before claiming it has been enforced. See
[Codex](https://developers.openai.com/codex/skills),
[Claude Code](https://code.claude.com/docs/en/skills#control-who-invokes-a-skill),
and [Pi](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/skills.md).

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

### Session effort on Claude Code

No skill in this catalog sets the reasoning effort. Claude Code documents an
`effort` frontmatter field for [skills](https://code.claude.com/docs/en/skills)
and [subagent definitions](https://code.claude.com/docs/en/sub-agents), but the
catalog's shared frontmatter stays portable with only `name` and
`description`, and the catalog ships no `.claude/agents` definitions. The
Agent tool has no per-call effort parameter, and a subagent inherits the
session level by default. Claude Code's documented default is `high` on
every model that supports effort except Opus 4.7, unless an organization
default applies; see the [model configuration docs](https://code.claude.com/docs/en/model-config).
The [skill substitutions reference](https://code.claude.com/docs/en/skills#available-string-substitutions)
describes `${CLAUDE_EFFORT}` inside skill text to read the level. The portable
entrypoints here do not use it. `plan-work` and `deliver-work` record the level
they can observe or that you state, otherwise unknown, and never claim to
change it.

Set effort per session rather than per skill. Start a planning session at a
lower level and a delivery session at `high`, the Fable default:

```bash
claude --effort medium
```

```bash
claude --effort high
```

The launch flag applies to that session. In an interactive session, a typed
`/effort medium` or `/effort high` is saved for the active model and applies
to later sessions on it. Use the launch flag for a one-session choice;
`/effort auto` clears the saved level. The `effortLevel` key in `settings.json` and the per-model
`modelSettings` entry persist a choice, and the `CLAUDE_CODE_EFFORT_LEVEL`
environment variable takes precedence for a process. Some older models hold
their default ahead of saved settings until an interactive effort choice
ends that hold; `--effort` overrides it for one launch. Check the session
header or `/effort` to confirm the effective level.

The recommendation follows Anthropic's published effort measurements
([Optimizing for cost and intelligence](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence),
read September 2026). On four knowledge-work benchmarks run with Claude
Fable 5, `medium` matched the default's accuracy at about 70 to 87 percent
of its cost, and `low` gave up one to three points for a third to a half
off. On SWE-bench Pro with Claude Opus 5, `medium` gave up about two points
for half the cost and `low` about eight for a quarter. This note treats
planning with `plan-work` as knowledge work and delivery with `deliver-work`
as coding. The source advises sweeping levels on your own traffic, so measure
before relying on it; the decision to accept whatever loss appears on
planning work is recorded in
[issue 24](https://github.com/jimmie-potts/agent-skills/issues/24).

Without a host override, a spawned worker inherits the session level. The advisory
pairing recommends default effort because a low-effort worker can stop
consulting; the effect depends on the task. These catalog skills cannot raise
the level for the worker alone. For Fable sessions that may compose the
pairing, start at `high`, or disclose the inherited reduced level and monitor
consultations. The same inheritance applies to read-only investigation
workers.

## Codex worker routing

The [Codex selection adapter](skills/deliver-work/references/codex-model-selection.md)
uses Luna/low for narrow read-only work, Terra/medium for bounded investigation
or implementation with reliable checks, and Sol/medium or high for harder work.
Verify live host support and preserve explicit stronger settings. Strategy is a
separate choice: direct work, one assigned worker, independent parallel workers,
or worker-with-astra advice at useful checkpoints.

An initial result plus one guided correction at unchanged settings triggers
reassessment if still inadequate. Diagnose missing facts, authority, or broken
infrastructure before promoting capability. These are bounded defaults, not
measured savings. Routine independent reviewers remain Terra/high. Claude keeps
its own first-failed-attempt escalation and effort-inheritance rules.

## Shared and domain skill ownership

Maintain reusable methods here. Consuming projects keep domain contracts,
validation commands, scope ownership, and workflow policy in their own agent
instructions and documentation. A project-local skill belongs there only when
its procedure depends on that project's domain. Do not create renamed project
wrappers or vendor shared skills into application repositories.

For local Codex and Pi use, select the required skills from this catalog with
the manager. For example, from this repository:

```bash
./scripts/manage-skills.sh install --agent codex deliver-work tdd grill-with-docs grilling domain-modeling code-review openspec-propose openspec-explore openspec-apply-change openspec-update-change openspec-sync-specs openspec-archive-change
```

The resulting personal symlinks point to this canonical checkout. Do not
commit external symlinks into a consuming repository. Keep the catalog available
while agents use it, and restart a host when it needs to refresh discovery.
The manager preserves conflicting installations and reports them for resolution.

To install only the explicit delivery coordinator, use a reviewed catalog
checkout and run:

```bash
./scripts/manage-skills.sh install --agent codex --dry-run deliver-work
./scripts/manage-skills.sh install --agent codex deliver-work
./scripts/manage-skills.sh status --agent codex
```

The coordinator loads `code-review` for delivery review. Other shared skills
are needed only when their substeps apply; the complete example above includes
them. Installing only the coordinator does not install its composed skills.

`deliver-work` replaces `deliver-jira-work` and `github-delivery` without aliases.
Update calls in consuming project instructions and inspect manager status for
stale installations. Before updating an existing source checkout, use its old
catalog and the manager to uninstall owned links for the retired names. After
source removal, status reports dangling owned links but uninstall preserves
them; reconcile those links separately after verifying ownership. Preserve
foreign installations and do not rewrite consuming projects automatically.

Keep the source checkout available. Verify discovery in a fresh neutral Codex
context outside any consuming repository with a same-named local skill. Record
the discovered path and published revision. Static metadata tests and the
[synthetic delivery scenarios](skills/deliver-work/references/validation-scenarios.md)
are separate evidence from actual host discovery. Codex explicit-only policy
uses `agents/openai.yaml`; the shared instructions also state the invocation
boundary for other hosts. See [OpenAI's skill documentation](https://learn.chatgpt.com/docs/build-skills)
for discovery and invocation controls.

For a fresh or cloud environment, provision a reviewed catalog revision as a
separate dependency using the host's supported user-skill mechanism. A local
symlink does not make a skill available in the cloud. If a required shared skill
is unavailable, report the missing prerequisite; do not silently copy its body
into the application or claim the workflow was loaded. Cloud setup is not
verified by the local manager tests.

Update OpenSpec integrations here, using the pinned generator in an isolated
scratch project. Preserve source records, licenses, and shared authority/CLI
adaptations during upgrades. Application projects keep their specifications
and OpenSpec configuration, without generated integration copies.

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
