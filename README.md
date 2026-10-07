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

- [`architect`](skills/architect/SKILL.md), an explicit or deliberately
  composed design-first code architecture workflow;
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
- [`prototype`](skills/prototype/SKILL.md), an explicit or deliberately
  composed bounded experiment or functional delivery-slice workflow;
- [`research`](skills/research/SKILL.md), source-backed investigation with
  claim-level citations;
- [`worker-with-astra`](skills/worker-with-astra/SKILL.md), a Luna or Sol worker with the
  original Astra agent providing approach feedback, blocker advice, and final
  review through a verified host adapter;
- [`teach`](skills/teach/SKILL.md), a layered code and design lesson workflow;
- [`tdd`](skills/tdd/SKILL.md), explicit or deliberately composed incremental
  TDD for bugs and features;
- [`technical-writing`](skills/technical-writing/SKILL.md), an explicit technical
  prose drafting and review standard;
- [`unslop`](skills/unslop/SKILL.md), an optional editorial pass for prose that needs it;
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
  Each item's Execution recommendation starts with the session type to open
  (`One-shot`, `Pair`, `Orchestrate` or `Investigate first`) and records the
  work surface (`UI`, `Backend` or `Unknown`), then gives both hosts' model and
  reasoning/effort level, worker subagents and required reviewers in a table,
  a paste-ready prompt per host, and a cheaper start; on Claude Code that is
  usually Sonnet, which is not itself a starting recommendation. See
  [execution recommendations](skills/plan-work/references/execution-recommendations.md).
  Before calling an item ready, it checks the item against the owning
  project's accepted decisions, current code and related backlog, scaled to
  the item; see [alignment](skills/plan-work/references/alignment.md).
  It follows project-owned guide and publication checkpoints within the user's
  authority, including a pending-documentation report for tracker-only work.
  It reads the installed `deliver-work` package's canonical assessment and
  task-planning contracts and `review-work`'s reviewer selection without
  invoking either, and composes
  `grill-with-docs` for material unresolved decisions. A bounded read-only
  investigation may compose the host's advisory pairing. Install those
  dependencies when using this planner; missing resources are reported, never
  copied. When the owning project declares installation as a completion
  condition, an item's acceptance includes installation and its readback,
  unless the item uses the project's opt-out, by default a source-only marking
  with a reason and a linked install issue. Its `Checkpoints` row names only
  uncovered owner decisions; applicable request or standing authority needs no
  renewed approval. Planning itself never installs anything;
- [`grill-with-docs`](skills/grill-with-docs/SKILL.md), which composes
  [`grilling`](skills/grilling/SKILL.md) and
  [`domain-modeling`](skills/domain-modeling/SKILL.md) for grouped decisions and
  documentation proposals;
- [`code-review`](skills/code-review/SKILL.md), separate Standards and
  Specification reviews against one fixed comparison. Its assigned-axis mode
  reviews one axis for a coordinating workflow and launches no agents;
- [`review-work`](skills/review-work/SKILL.md), an explicit complete independent
  review of one change without delivery. It freezes the comparison, runs
  separate fresh Standards and Specification reviewers through rounds with
  stable findings, and returns a per-axis `satisfied`, `action-required` or
  `incomplete` [result](skills/review-work/references/result-contract.md). A
  missing specification, partial return or stale comparison is never approval.
  Each result carries every reviewer's actual return, redacted and digested.
  It implements, publishes and merges nothing; `deliver-work` composes it for
  its required reviews and keeps corrections, CI and merge;
- [`deliver-work`](skills/deliver-work/SKILL.md), explicit delivery of
  one Jira issue, GitHub issue, or document requirement using the owning
  project's planning, hosting, review, and completion policy. It supports a
  ready-PR-only limit and requires no specific specification framework;
  it assesses verification needs and selects implementation settings from
  available host capabilities, composing `review-work` for reviewer selection
  and review rounds. The shared
  [work assessment](skills/deliver-work/references/work-assessment.md), also
  used by `plan-work`, fits scope to the owning project's actual needs at
  drafting and pickup: cuts must name what they lose, and required protections
  stay unless the scope owner decides otherwise. It may compose the host's
  advisory pairing for bounded implementation with checkpoints,
  `worker-with-astra` under Codex
  collaboration tools or `worker-with-fable` under Claude Code subagent tools,
  choosing by verified host tooling rather than by request wording; install the
  applicable skill separately when using the optional pairing. Advisory
  inspection never replaces its two independent delivery reviews. Shared
  [task planning](skills/deliver-work/references/task-planning.md) maps acceptance
  to verifiable tasks, distinguishes input dependencies from coordination, and
  checks contracts, resources and ownership before parallel dispatch.
  Task planning selects task reviews at dependency or risk boundaries, and
  [corrections](skills/deliver-work/references/corrections.md) acts on review
  results, diagnoses surviving blockers and honors explicit round, time and
  spending limits. Productive rounds have no universal cap; exhausted limits
  leave unmet gates pending. Task reviews never replace the two final
  independent reviews.
  [Verification maintenance](skills/deliver-work/references/verification-maintenance.md)
  updates the owning project's feature map or recipe with changed behavior,
  classifies failed verification and shows that risk-selected checks fail on
  a known bad result; a screenshot or simulated pass is never acceptance by
  itself. Substantive
  checkpoints and final handoff include the chosen strategy and reason, decision
  contributors, model roles and observed settings, active and distinct agent
  counts, planned additional agents, and advisor consultations. See
  [execution reporting](skills/deliver-work/references/execution-reporting.md)
  for counting rules. Each delivery keeps one `## Execution record` section in
  its PR body, or in the final response without one, so a project guide can
  parse the recommended and actual model, level and session type, the workers
  and reviewers, and the review rounds, findings, finding causes and
  corrections. Every model and level carries its source: `host-observed`,
  `user-stated`, `self-reported` or `unknown`. Routine updates report
  changes, blockers and next actions; consequential strategy, setting, team
  and authority changes are reported immediately. [Selection](skills/deliver-work/references/model-selection.md)
  loads only the chosen role and host. Workers receive a bounded brief and,
  for a pairing, its worker protocol rather than the coordinator's setup rules. Its
  [resumption packet](skills/deliver-work/references/resumption.md) retains task
  and artifact revisions, completed work, retry history and pending effects in
  existing authorized evidence. Resumption checks current scope, ownership and
  repository state before accepting artifacts or continuing dependent work;
  [PR supervision](skills/deliver-work/references/pr-supervision.md) tracks
  published feedback and current checks through the requested finish line.
  It diagnoses failures from logs, handles fixes before obsolete check reruns,
  and resumes supervision after each push or rerun.
  [Review reports](skills/deliver-work/references/review-reports.md) publish
  each final round with its retained reviewer returns, keep the PR's current
  review state, and limit replies to facts about scoped fixes. When the owning
  project declares installation or deployment as a completion condition and
  defines its procedure, delivery prepares the complete step after verified
  merge and post-merge CI. It runs within applicable request or standing
  authority without asking again, preserving narrower requests and requiring
  authority for uncovered effects. A completion condition alone grants no
  permission. Without a declared procedure it never improvises one and keeps
  a step the item still requires pending with its owner. Every delivery ends
  with a cleanup outcome for the temporary
  resources it created: removed where the owning project's policy allows,
  otherwise retained with a reason, owner and next action;
- [`close-work`](skills/close-work/SKILL.md), an explicit session closeout that
  files, comments and records. It runs after a delivery's completion checks,
  never in place of them. It files uncovered P1 and P2 follow-ups in the
  owning repository's issue form, posts a parseable `## Closeout record` with a
  resume prompt on the owning issue, saves verified memory notes, deletes only
  guarded completed local branches, and reports in eight sections ending
  `Safe to archive` or `Needs attention`. It never changes product code,
  installs, merges, closes issues, deletes remote branches, removes worktrees
  or changes another session's work;
- the six OpenSpec 1.12.0 core workflows: `openspec-propose`, `openspec-explore`,
  `openspec-apply-change`, `openspec-update-change`, `openspec-sync-specs`, and
  `openspec-archive-change`. They use the consuming repository's pinned CLI.

A repository can deliberately compose the existing explicit-only TDD and
Grill with Docs methods without changing their global invocation switches.
Repository instructions must name that composition and preserve the underlying
request's action boundaries. A context pointer does not change host discovery
or install a missing skill. `plan-work` and `deliver-work` likewise compose the
explicit-only `architect` and `prototype` methods for a named question under
their uncertainty routing; the composing request's authority binds them.

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
| Explicit `$review-work` for a branch, PR or local change | Select `review-work`; freeze the comparison, run two fresh independent axes and return the per-axis result without implementing, publishing or merging. |
| Explicit `$deliver-work` for an issue | Select `deliver-work`, which composes `review-work` for its required reviews; the review is a substep, not a second coordinator. |
| `Interrogate this PR diff` | Select `interrogate`, not `code-review`, because the explicit adversarial multi-review request takes precedence. |
| `Review this small diff I do not trust; what could it break?` | Select `blast-radius`, not `code-review`, because explicit breakage-risk analysis takes precedence. |
| `Where should rate limiting live?` | Select `how` Placement, not `codebase-design`. |
| `Critique this module boundary` | Select `how` Critique, not `codebase-design`. |
| `Research the current API limits using official sources` | Select `research`; implementation from supplied sources does not. |
| Explicit `$close-work` at the end of a session | Select only `close-work` and run its closeout sweep within its authority boundary; an ordinary `Did we miss anything?` question does not select it or authorize its writes. |
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
python3 tests/installed-files-test.py
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
./scripts/manage-skills.sh status --agent grok
./scripts/manage-skills.sh status --agent both

./scripts/manage-skills.sh install --agent codex <skill-name>
./scripts/manage-skills.sh install --agent claude <skill-name>
./scripts/manage-skills.sh install --agent grok <skill-name>
./scripts/manage-skills.sh install --agent both <skill-name>
./scripts/manage-skills.sh install --agent both --all

./scripts/manage-skills.sh install --agent both --dry-run <skill-name>
./scripts/manage-skills.sh install --agent both --existing-only <skill-name>
./scripts/manage-skills.sh uninstall --agent both --dry-run <skill-name>
./scripts/manage-skills.sh uninstall --agent both <skill-name>
./scripts/manage-skills.sh uninstall --agent grok <skill-name>
```

`install --existing-only` verifies already-correct links without creating links
or destination roots. It refuses missing or conflicting targets and preserves
the manager's adjacent ownership checks. The guarded adapter below uses this
mode after updating existing skill files.

`--agent both` installs Codex and Claude Code only. It does **not** include
Grok Bot; install or uninstall Grok destinations with `--agent grok`.

Defaults and discovery:

| Agent | Personal destination | Explicit invocation |
| --- | --- | --- |
| Codex | `~/.agents/skills/<skill-name>` | `$skill-name` |
| Claude Code | `~/.claude/skills/<skill-name>` | `/skill-name` |
| Pi | `~/.agents/skills/<skill-name>` | `/skill:<skill-name>` |
| Grok Bot | `/home/box/agent-data/workflows/<skill-name>` | Host `/` skill menu / UpdateSkill after install |

Codex, Claude Code, and Pi may also select a skill automatically when its
description matches the request. Pi discovers the same `~/.agents/skills/`
destination as Codex, so a skill installed with `--agent codex` is available to
both of those hosts. The manager has no separate `--agent pi` option because it
would address the same links. Grok Bot uses the Cursor workflows tree as its
managed destination (`--agent grok`); after symlink install, the host loads
those skill directories through its UpdateSkill / workflows readback path—prove
installation with `./scripts/manage-skills.sh status --agent grok` (owned link
resolves into this checkout) and, when the host UI is available, confirm the
skill appears for the Bot after a fresh session or host reload. After adding or
changing skills, use Pi's `/reload` command or restart the relevant local
agent.

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

GROK_SKILLS_DIR=/tmp/grok-skills \
./scripts/manage-skills.sh install --agent grok --dry-run <skill-name>
```

`GROK_SKILLS_DIR` overrides the default Grok root
(`/home/box/agent-data/workflows`) the same way `CODEX_SKILLS_DIR` and
`CLAUDE_SKILLS_DIR` override their hosts. Leave it unset for normal box
installs.

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
`description`, and the catalog installs no `.claude/agents` definitions.
`review-work` ships reviewer profile templates, including one that sets
`effort: high`, for the owning environment to provision; see its
[reviewer execution](skills/review-work/references/reviewer-execution.md)
reference. The Agent tool has no per-call effort parameter, and a subagent
inherits the session level unless its definition sets `effort`. Claude Code's
documented default is `high` on every model that supports effort except
Opus 4.7 (`xhigh`) and Opus 5.5 (`medium`), unless an organization default
applies; see the
[model configuration docs](https://code.claude.com/docs/en/model-config).
The [skill substitutions reference](https://code.claude.com/docs/en/skills#available-string-substitutions)
describes `${CLAUDE_EFFORT}` inside skill text to read the level. The portable
entrypoints here do not use it, and an agent cannot reliably read its own
effort: on 2026-09-24 an Opus session set to `high` reported `low`. The
[Claude Code adapter](skills/deliver-work/references/claude-code-model-selection.md)
records why a host-observed value does not replace your statement.
`plan-work` and `deliver-work` record the level you state, beside any
host-observed value, otherwise unknown, and never claim to change it.

Set effort per session rather than per skill. When starting planned work,
choose the model and effort in the host first, then paste the item's prompt for
that host. The prompt states your choice; the agent confirms only the model and
takes the level as stated. Simple implementation may suit a
lower level; difficult reasoning or orchestration may warrant a stronger model
at `high`. Verify support in the chosen host. For example, these launch flags
select a level for one Claude Code session:

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

The earlier planning-versus-delivery guidance drew on Anthropic's effort measurements
([Optimizing for cost and intelligence](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence),
read September 2026). On four knowledge-work benchmarks run with Claude
Fable 5, `medium` matched the default's accuracy at about 70 to 87 percent
of its cost, and `low` gave up one to three points for a third to a half
off. On SWE-bench Pro with Claude Opus 5, `medium` gave up about two points
for half the cost and `low` about eight for a quarter. This note treats
planning with `plan-work` as knowledge work and delivery with `deliver-work`
as coding. The per-item recommendations now distinguish task difficulty and
session role; these measurements do not validate that model-selection table.
The source advises sweeping levels on your own traffic, so measure
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
uses GPT-6 models: Luna/low for narrow read-only work, Luna/medium for bounded
investigation or implementation with reliable checks, and Sol/medium or high
for harder work.
Verify live host support and preserve explicit stronger settings. Strategy is a
separate choice: direct work, one assigned worker, independent parallel workers,
or worker-with-astra advice at useful checkpoints.

An initial result plus one guided correction at unchanged settings triggers
reassessment if still inadequate. Diagnose missing facts, authority, or broken
infrastructure before promoting capability. These are bounded defaults, not
measured savings. Independent reviewers use Luna/high only for bounded review
tasks below high impact, and Sol/high or stronger otherwise. Claude keeps
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
./scripts/manage-skills.sh install --agent codex deliver-work review-work tdd grill-with-docs grilling domain-modeling code-review openspec-propose openspec-explore openspec-apply-change openspec-update-change openspec-sync-specs openspec-archive-change
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

The coordinator composes `review-work` for delivery review, which composes
`code-review` for each axis; `plan-work` reads `review-work`'s reviewer
selection. Install both with any delivery or planning coordinator, and
`code-review` with a standalone `review-work`. Other shared
skills are needed only when their substeps apply; the complete example above
includes them. Installing only the coordinator does not install its composed
skills.

### Update the installed catalog

Installed links on both hosts resolve into one checkout of this repository, so
updating it changes the skills of every running Codex, Claude Code and Pi
session at once, even when the update was wanted for unrelated work. Use this
one procedure for every update: installing a merged change that
[`AGENTS.md`](AGENTS.md) says needs installation, working an install issue that
batches source-only changes, or picking up `main` for any other reason.
`AGENTS.md` also records the owner's standing installation authority, its limits
and the pending state when authority or verification is missing. The procedure
uses only Git and the manager, so it works while a newly required skill is
still missing. From a checkout older than the update,
read this section from the target revision, for example
`git show origin/main:README.md`.

1. Find the checkout the installed links resolve to by reading one managed
   link, such as `readlink -f ~/.claude/skills/deliver-work`; the checkout is
   two directories above the skill it prints. Run everything from that
   checkout. Never run the manager from a worktree: it builds its source path
   from its own location, and links made from a worktree break when the
   worktree is removed.
2. Preflight before changing anything. After `git fetch`, confirm that the
   checkout is on `main`, that `origin/main` includes the merge you are
   installing (`git merge-base --is-ancestor <merge> origin/main`), that the
   update is a fast-forward (`git merge-base --is-ancestor HEAD origin/main`)
   and that no local change in `git status --short` blocks it. A local change
   inside a skill the update changes or adds
   (`git status --short -- skills/<skill>`) also blocks it, because step 6
   would then fail. If any check fails, stop and report the checkout's owner
   and the next action. Never
   stash, reset, switch branches, roll back or remove another session's files.
3. List everything the update brings, including changes merged for other work:
   `git diff --name-status HEAD origin/main -- skills/`. Classify each skill as
   changed, added, renamed or removed. Read the changed callers for newly
   required skills, such as `review-work` for `deliver-work` and `plan-work`,
   and run `./scripts/manage-skills.sh status --agent both` to see which are
   missing, and record which changed skills are installed on each host. An
   issue marked source-only does not keep its changed callers out of the
   update; the fast-forward brings every merged change at once.
4. Prepare the complete step and check its effects against the current request
   and standing authority in `AGENTS.md`. Ask only for uncovered effects;
   a step within existing authority needs no renewed approval.
   - For each renamed or removed skill, uninstall its owned links with the
     current, older catalog before the fast-forward, dry-run first, as the
     retirement paragraph below describes. Rerun step 2's checks just before
     the uninstall.
   - Fast-forward with `git merge --ff-only origin/main`.
   - For each added skill, new name of a renamed skill and newly required
     skill, run
     `./scripts/manage-skills.sh install --agent <host> --dry-run <skill>` and
     then the install, for each host the skill supports. Most skills support
     both hosts (`--agent both`). Host-specific skills install for their host
     only, such as `worker-with-fable` for Claude Code and `worker-with-astra`
     for Codex.
   - List the readbacks in step 6, the host reload or fresh session that new
     skills need before they can be discovered, and the recovery in step 5.
   - Name the sessions using the installed skills and agree timing with their
     owners; do not interrupt another owner's work.
5. Within the verified authority, run the prepared step and nothing else.
   Routine installation authority does not extend to unrelated skills or
   settings. If the fast-forward refuses, reinstall any links the step
   uninstalled from the unchanged checkout,
   dry-run first, then stop as in step 2. Until every readback passes, the
   update is incomplete: record which parts ran, and have callers that need a
   missing skill report it and pause the dependent step rather than resume
   against a partial skill set. To recover, read status and rerun only the
   manager commands for the missing owned links, dry-run first. Preserve
   unrelated files.
6. Read back the evidence:
   - the checkout's revision includes the merge
     (`git merge-base --is-ancestor <merge> HEAD`);
   - each changed skill that status showed installed on a host before the
     update still resolves into the checkout there (`readlink -f`); a changed
     skill that was not installed on a host stays as it was, unless it is newly
     required;
   - `git status --short -- skills/<skill>` is empty for each changed or added
     skill, so its installed files match the fetched revision. Other sessions'
     local changes elsewhere do not fail this readback; a local change inside
     an affected skill does, so report its owner;
   - status shows each new or newly required skill correctly installed on
     each host it supports, and no owned links for retired names.

   Resume paused callers only after a fresh session on each host lists a newly
   required skill. Run a fresh-session behavioral check of the changed skills
   only when the issue asks for one. Link readback alone does not establish
   reviewer quality or optional profile qualification.

#### Guarded updates of existing skills

`python3 scripts/installed_skills.py --config <private-config.json>` implements
the existing-skill part of this procedure for the shared supervisor. It accepts
one JSON stdin request:

```json
{"schemaVersion":1,"operation":"install","repository":"jimmie-potts/agent-skills","issue":140,"merge":"<full SHA>","owner":"<named owner>","deadline":1234567890,"evidenceDirectory":"<private empty directory>"}
```

The trusted, owner-only configuration has these exact fields:

```json
{"schemaVersion":1,"repository":"jimmie-potts/agent-skills","owner":"<named owner>","checkout":"<canonical main checkout>","stateDirectory":"<private journal>","evidenceRoot":"<private evidence root>","git":"<resolved Git executable>","path":"<qualified Python bin>:/usr/bin:/bin","allowedPaths":["skills/example/SKILL.md"],"protectedPaths":[],"requiredSkills":["example"],"links":[{"agent":"codex","skill":"example","path":"<existing Codex root>/example"},{"agent":"claude","skill":"example","path":"<existing Claude root>/example"}],"files":{"<trusted tool or manager file>":"<SHA256>"}}
```

Keep the configuration and both disjoint private roots outside the checkout.
Each request supplies an empty owner-only directory under `evidenceRoot`.
Pin the adapter, configuration and interpreter in the supervisor's fixed adapter
entry. The owning configuration also pins the canonical manager and validator,
Git and every tool named in the adapter's `TOOLS` inventory. `path` contains only
qualified existing tool directories; its Python needs the existing PyYAML
dependency. The adapter supplies its own manager source/target environment and
does not inherit Python search paths or shell startup settings.

`requiredSkills` and `links` declare the reviewed dependencies and supported
installed targets. Refresh that declaration when reviewing the selected issue's
complete update; the adapter cannot infer semantic dependencies from a prompt.
Unknown dependency coverage stays pending. Each required skill must exist in
the reviewed catalog and have its declared existing links. An undeclared owned
link for a required skill on either configured host refuses the update.

The adapter checks canonical main, the owning origin and the complete incoming
bundle. It fetches main, proves ancestry, and fast-forwards only the exact
requested merge. `allowedPaths` is an exact file inventory under `skills/`,
`tests/` or `docs/`, including every tracked file in each affected skill.
New, renamed or removed skills, removed resources, missing links and unsupported
paths remain pending. Affected skills must be clean; unrelated dirty bytes and
index entries must survive unchanged. No stashing, reset, rollback, copying
installer or automatic discovery follows a refusal.

Root instructions, `scripts/`, the active `deliver-work`, `review-work`,
`code-review`, `plan-work`, `tdd`, `writing-for-agents` and `unslop` packages,
pinned dependencies and configured `protectedPaths` require the established
stopped boundary. Configure any other active policies there too. Git hooks and
filesystem-monitor hooks are disabled only for the fixed installer Git commands
to avoid executing local or candidate hook code. Attribute-driven processing is
unsupported. Codex/Claude agent hooks and permissions are unchanged.

The existing manager validates the catalog, reports status on both configured
hosts and performs `install --existing-only`, dry-run first. The retained
`installed-files/1.0` receipt binds repository, issue, owner, exact target, plan
hash, included commits, complete affected-skill bytes, installed-link identity,
configuration hash and preserved dirty-state hash. Its `readback` contains
`kind:"installed-files"`, exact `revision`, `files`, `links`,
`preservedDirtySha256`, and `managerStatus` for `codex` and `claude`, each with
`status:"correct"` and the manager-output SHA256. Canonical plan/dirt hashes use
Python's sorted compact JSON with default ASCII escaping, encoded as UTF-8.

Success returns the supervisor's `readbackKind:"installed-files"` response with
matching repository/merge/owner, `installedRevision` and `{path,sha256}` receipt.
It makes no running-process or health claim. The owning closeout adapter must
validate the semantic receipt before issue completion. A known pre-dispatch
refusal returns `status:"blocked",effects:"none"`; uncertain effects retain the
journal and ownership.

`operation:"reconcile"` reads only an existing owned plan and current
checkout/link/manager status. It can write private proof of an observed result,
but never fetches, merges, installs or recreates a link. A lost fast-forward
response therefore cannot trigger a second update. An unobserved or mismatched
result stays uncertain. New skills and newly required missing links still need
the fresh-session discovery and owner-coordinated procedure above; this adapter
does not provide that acceptance.

Run `python3 tests/installed-files-test.py` with the other required checks. Its
real Git and manager fixtures use disposable repositories and skill targets.
On WSL, set `TMPDIR` to a repository `.local/scratch/` directory. Source tests do
not qualify the personal installation or activate scheduling.

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
