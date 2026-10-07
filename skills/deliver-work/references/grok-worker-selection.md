# Grok Bot worker selection and continuation

Use with the [Grok Bot adapter](grok-model-selection.md) for worker roles only.

## Continue or replace a worker

These mechanics apply to assigned workers and advisory workers. Retain the
returned agent or task identifier. Use host listing or status tools when state
is unclear. Use `MessageSubagent` for a running or idle worker that needs a
correction or answer; a queued message alone does not prove the worker resumed.
A correction keeps the same worker and settings.

When reassessment selects a new attempt, follow the [attempt-handoff contract](worker-continuation.md).
Stop an active old assignment with `StopSubagent` (or the verified stop control)
and verify its state before spawning a replacement; a completed assignment is
already stopped. Start a fresh context with supported selected settings and the
complete handoff. A missing stop/resumption capability blocks its affected
operation. Never call a fresh `Task` spawn a resume. Paired workers additionally
follow the discovered pairing adapter's prerequisites and consultations with the
original advisor.

For delivery, include the shared [task packet](resumption.md) or an authorized
reference in each resumed/replacement brief. Match returned task, assignment and
source revision before applying a patch, including late messages from a stopped
worker. Host resumption alone does not establish that its context is current.

## Map assessment evidence to settings

Read the shared assessment and implementation-selection policy first. Select the
least costly suitable supported starting configuration below, preserving stronger
explicit requirements. These are task-suitability hypotheses, not measured cost
or quality results. Verify current model identifiers, descriptions, effort
controls, and context controls from the live host schema. Do not invent Codex
Luna/Sol or Claude Sonnet/Opus aliases. A supported request may be attempted
without a prior recorded spawn; availability is not runtime identity. A rejected
default permits a disclosed suitable fallback under shared policy, limited to
models the live host exposes for spawning or the original coordinator; an
unavailable explicitly required model/effort blocks that selection.

| Work evidence | Worker default | Strategy and limits |
| --- | --- | --- |
| Narrow read-only lookup, extraction, classification, structured transformation | One `Task` executor at the lowest suitable host-supported model/effort | Assigned scout; parallel only for independent questions; no advisory loop |
| Bounded investigation or implementation; low/medium complexity and impact, reliable acceptance checks, no unresolved material requirement | One executor at host-default or composing-workflow model/effort (`medium` when the host exposes effort) | Assigned worker, or worker-with-grok when approach/blocker advice helps |
| Open-ended implementation requiring additional design judgment | One executor with any stronger host-supported reasoning the assessment warrants | Assigned worker or advisory pairing at separable decision points |
| High complexity or impact | Stronger host-supported effort (at least `high` when exposed), or original coordinator | Stronger implementation floor; direct coordination when difficult reasoning is continuous |
| High uncertainty or missing material facts | Investigate before dependent implementation | Lowest suitable executor for a narrow fact lookup; medium/bounded investigation with checks; stronger reasoning when open-ended; user owns product decisions |
| Many independent pieces | Select each piece using the rows above | Parallel workers only where pieces are independent; coordinator integrates |

Scouting is a read-only role, orchestration is the coordinator's activity, and
advisory pairing is an optional strategy. Do not force scouting into parallel
work or implementation into advice loops. Keep leaf workers from spawning
further agents and respect the current host concurrency limit. Direct work by
the original coordinator remains the baseline for trivial or continuously hard
work. Preserve its settings; Grok Bot is not spawned as an implementation
worker under a second advisor. Narrow low-effort scouting is outside
worker-with-grok.

## Bound corrections and promotion

For each unchanged Grok worker configuration, allow an initial returned result
and at most one evidence-guided correction. A second inadequate result requires
reassessment; escalate earlier when evidence warrants it. A consultation is not
itself a failed attempt. Expected red tests during TDD do not count as inadequate
returned results. Diagnose acceptance failures, including plausible incorrect
output, before treating them as worker-capability failures. Missing facts,
product decisions, authority, dependencies, or broken infrastructure require
their own resolution, not automatic model promotion.

When capability is the diagnosed gap, permit one effort increase up to `high`
(or the next host-supported step below above-high) for an otherwise sound
approach that needs deeper reasoning. Otherwise promote to a stronger
host-supported model/effort the assessment justifies, or start there when the
assessment warrants it. Start a promoted configuration at `medium` unless the
assessment requires `high`; preserve any stronger explicit requirement. The one
effort increase applies per unresolved task, not again at every new worker.
After it is used, further capability gaps require model promotion or return to
the coordinator. Do not automatically select `xhigh`, `max`, or equivalent
above-high levels, even when the schema supports them, without a task-specific
reason or explicit requirement. Explicit stronger settings still require host
support and cannot be silently reduced.

Return unresolved high-capability failures to the original Grok Bot coordinator
at its existing settings. Do not spawn Grok Bot as an implementation worker
under another advisor or reset the ladder. Returning work is a handoff for
diagnosis and reassessment, not a mandate to implement below a capability floor.
The coordinator preserves its settings and required gates; if its suitability
cannot be established, report the unresolved blocker instead of claiming the
stronger-worker failure is resolved.

A new independent task gets a fresh cheaper-start assessment; rephrasing,
resuming, or replacing workers on unresolved work preserves failure history.
Use the [attempt-handoff contract](worker-continuation.md) and the continuation
mechanics above when changed settings require a fresh worker. Keep model
promotion distinct from same-worker correction and restore mandatory
consultations for a new pairing.

This threshold governs investigation/implementation worker configurations, not
the number of independent delivery review rounds. Review-work owns finding
continuity; [corrections](corrections.md) owns diagnosis and explicit limits.
Reviewer selection remains separate, and no retry allowance waives an acceptance
or review gate. Claude's first-failed-bounded-attempt Sonnet-to-Opus policy and
Codex's Luna-to-Sol ladder remain in their own adapters.

## Record settings and total work

Use existing labeled returns and task evidence. Record coordinator and worker
requested settings separately from reported or independently observed settings;
unexposed values remain `unknown`. Include the role, strategy, correction count,
effort-increase history, model promotions, rationale, acceptance results, and
attributable usage when exposed. Count failed attempts, review corrections,
coordination, replacements, and retries in total-work accounting. Separate
subscription usage from API dollars; unavailable telemetry is not zero cost.
Do not infer savings from fewer tokens, a successful spawn, or a small trial.
