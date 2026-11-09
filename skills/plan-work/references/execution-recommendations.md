# Give execution advice when requested

Read only when the user or owning repository asks for execution recommendations.
Ordinary planning needs one planned-start sentence about the next useful action,
not model selection, a host matrix, pasted prompts or a fingerprint.

Tailor advice to the requested hosts, available controls, task and evidence.
Explain a consequential choice briefly. Use host defaults where suitable; this
skill has no prescribed model, thinking level or orchestration pattern. Missing
optional telemetry does not make an otherwise ready work item insufficient.
Recommendations remain advice unless explicitly adopted as requirements.

Use the discovered deliver-work package's references/model-selection.md when
worker advice is needed, and review-work's references/review-selection.md for
review coverage. Read only the relevant host adapters. Advice launches no agents.
Give concrete settings only when supported and requested; distinguish unknown
availability from verified host capability. A recommendation does not authorize
publication, installation or physical work.

## Existing project formats

Some projects parse the established `## Execution recommendation` format. Use
the format below only when that project explicitly requires it, retaining its
fields and unknowns. Preserve existing records; do not bulk-reformat issues.
For ordinary requested advice, a short paragraph is sufficient. These labels
and fields describe a recommendation, not mandatory execution choices.

1. `**Start with:**` names the proposed next action and any requested settings.
2. `**Work surface:**` is `UI`, `Backend` or `Unknown`, using the project's
   definition when available. It describes the work and adds no approval gate.
3. Preserve the consuming project's host table, with `Model`, `Thinking level`,
   `Session type`, `Subagents`, `Reviewers` and `Availability` rows. The established
   three-host format uses `Claude Code`, `Codex` and `Grok` columns. Use it only
   when required; ordinary advice need not cover hosts the user did not ask for.
   `Model` cells carry the host's model identifier in backticks beside any
   display name, such as Opus (`opus`) or Sol (`gpt-6.1-sol`), so a delivery
   that keeps the Execution record can copy it into its `Recommended` row.
   Name unavailable settings honestly. `Checkpoints` covers only uncovered
   decisions, including any uncovered authority for an installation or
   deployment step in acceptance. Existing standing authority needs no renewal.
4. Include `**Prompt (Claude Code):**`, `**Prompt (Codex):**` and
   `**Prompt (Grok):**` only where the consuming format requires them. Use `n/a`
   with a reason for an excluded host. Prompts carry the work reference, finish
   line, explicit limits and required independent review. They must not declare
   that a suggested model is already running or that its settings were verified.
5. For required `**Cheaper start:**` and `**Cheaper prompt (...)**` fields, give
   an alternative only when supported by evidence; otherwise write `none`.
   There is no prescribed model mapping or cheaper-start ladder.
6. `**Why:**` states the evidence behind the advice; `**Reassess when:**` states
   what would change it. `**Assessed:**` records the date and policy revision.
   Include a fingerprint only when the project defines and requires one.

When a requested recommendation cannot be supported, mark that advice
`**Status:** insufficient` and `**Missing:**` with the specific gap. This does
not by itself block the work item's readiness. Preserve any known work surface
and useful next action.

The established session labels remain available to those consumers:

| Session type | Description |
| --- | --- |
| `One-shot` | Direct implementation without worker delegation |
| `Pair` | A deliberately selected advisory pairing |
| `Orchestrate` | Coordination of delegated implementation tasks |
| `Investigate first` | Resolve a named uncertainty before dependent implementation |

These labels do not select a model, number of workers or thinking level.
Independent delivery reviews remain required for every implementation approach.
An investigation alone does not launch delivery reviewers.
