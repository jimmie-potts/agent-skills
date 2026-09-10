# Codex selection adapter

Use only when current collaboration tools expose model and reasoning overrides.
Inspect their actual schema and host model descriptions before calling. Policy
does not add capabilities or override host permissions.

For a supported override, use collaboration.spawn_agent with the exact selected
model and supported reasoning_effort, fork_turns="none", and a self-contained
brief. Full-history forks in this host inherit parent settings and cannot accept
those overrides. If inheritance is intended, omit overrides and report inherited
settings only to the extent observable. Do not guess a reasoning enum.

Record requested parameters and actual returned runtime metadata separately.
A successful spawn establishes the request succeeded, not independent proof of
the executing model's identity. Disclose unknown identity; handle a verified
mismatch against explicit requirements before dependent work. Model options
alone never prove that the current coordinator is Astra.

For worker-with-astra, discover its installed package and follow its
references/codex.md rather than copying the consultation protocol. Keep durable
writes with this delivery coordinator. Fresh independent review briefs carry
the fixed comparison and raw sources without prior approval narratives.

## Continue or replace a worker

These mechanics apply to assigned workers and advisory workers. Retain the
returned identifier. Use `list_agents` when state is unclear. Use
`send_message` for a running worker and `followup_task` for a completed/idle
worker needing a correction or answer; a queued message does not resume an
idle worker. A correction keeps the same worker and settings.

When reassessment selects a new attempt, follow the shared attempt-handoff
contract. Stop an active old assignment with `interrupt_agent` and verify its
state before spawning a replacement; a completed assignment is already stopped.
Start a fresh context with supported selected settings and the complete handoff.
A missing stop/resumption capability blocks its affected operation. Never call
a fresh spawn a resume. Paired workers additionally follow the discovered
pairing adapter's prerequisites and consultations with the original advisor.

## Map assessment evidence to settings

Read the shared assessment and strategy policy first. Select the least costly
suitable supported starting configuration below, preserving stronger explicit
requirements. These are task-suitability hypotheses, not measured cost or
quality results. Verify current model identifiers, descriptions, effort enums,
and context controls from the live host schema. A supported request may be
attempted without a prior recorded spawn; availability is not runtime identity.
A rejected default permits a disclosed suitable fallback under shared policy;
an unavailable explicitly required model/effort blocks that selection.

| Work evidence | Worker default | Strategy and limits |
| --- | --- | --- |
| Narrow read-only lookup, extraction, classification, structured transformation | Luna (`gpt-5.6-luna`) at `low` | Assigned scout; parallel only for independent questions; no advisory loop |
| Bounded investigation or implementation; low/medium complexity and impact, reliable acceptance checks, no unresolved material requirement | Terra (`gpt-5.6-terra`) at `medium` | Assigned worker, or worker-with-astra when approach/blocker advice helps |
| Open-ended implementation requiring additional design judgment | Sol (`gpt-5.6-sol`) at `medium` | Assigned worker or advisory pairing at separable decision points |
| High complexity or impact | Sol at `high`, or original coordinator | Stronger implementation floor; direct coordination when difficult reasoning is continuous |
| High uncertainty or missing material facts | Investigate before dependent implementation | Luna for a narrow fact lookup; Terra for bounded read-only investigation with checks; Sol when open-ended reasoning warrants it; user owns product decisions |
| Many independent pieces | Select each piece using the rows above | Parallel workers only where pieces are independent; coordinator integrates |

Scouting is a read-only role, orchestration is the coordinator's activity, and
advisory pairing is an optional strategy. Do not force scouting into parallel
work or implementation into advice loops. Keep leaf workers from spawning
further agents and respect the current host concurrency limit. Direct work by
the original coordinator remains the baseline for trivial or continuously hard
work. Preserve its settings; Astra (`gpt-6-astra`) is not spawned as an
implementation worker. Luna is outside worker-with-astra's supported tiers.

## Bound corrections and promotion

For each unchanged Codex worker configuration, allow an initial returned result
and at most one evidence-guided correction. A second inadequate result requires
reassessment; escalate earlier when evidence warrants it. A consultation is not
itself a failed attempt. Expected red tests during TDD do not count as inadequate
returned results. Diagnose acceptance failures, including plausible incorrect
output, before treating them as worker-capability failures. Missing facts,
product decisions, authority, dependencies, or broken infrastructure require
their own resolution, not automatic model promotion.

When capability is the diagnosed gap, permit one effort increase up to `high`
for an otherwise sound approach that needs deeper reasoning. Otherwise promote
Luna to Terra to Sol, skipping rungs when the assessment justifies it. Start a
promoted model at `medium` unless the assessment requires `high`; preserve any
stronger explicit requirement. The one effort increase applies per unresolved
task, not again at every new worker. After it is used, further capability gaps
require model promotion or return to the coordinator. Do not automatically select
`xhigh`, `max`, or `ultra`, even when the schema supports them. Explicit stronger
settings still require host support and cannot be silently reduced.

Return unresolved Sol/high capability failures to the original coordinator at
its existing settings. Do not spawn an Astra implementation worker or reset the
ladder. Returning work is a handoff for diagnosis and reassessment, not a
mandate to implement below a capability floor. The coordinator preserves its
settings and required gates; if its suitability cannot be established, report
the unresolved blocker instead of claiming the stronger-worker failure is
resolved. The same rule applies if Sol/medium exhausts its correction allowance
after the task's effort increase was already used.

A new independent task gets a fresh cheaper-start assessment; rephrasing,
resuming, or replacing workers on unresolved work preserves failure history.
Use the shared attempt-handoff contract and the continuation mechanics above
when changed settings require a fresh worker. Keep model promotion distinct from
same-worker correction and restore mandatory consultations for a new pairing.

This threshold governs investigation/implementation worker configurations, not
the number of independent delivery review rounds. Reviewer selection remains
separate, and no retry allowance waives an acceptance or review gate. Claude's
first-failed-bounded-attempt Sonnet-to-Opus policy remains in its own adapter.

## Record settings and total work

Use existing labeled returns and task evidence. Record coordinator and worker
requested settings separately from reported or independently observed settings;
unexposed values remain `unknown`. Include the role, strategy, correction count,
effort-increase history, model promotions, rationale, acceptance results, and
attributable usage when exposed. Count failed attempts, review corrections,
coordination, consultations, and retries in total-work accounting. Separate
subscription usage from API dollars; unavailable telemetry is not zero cost.
Do not infer savings from fewer tokens, a successful spawn, or a small trial.

## Map impact to independent reviewers

Use this mapping for both Standards and Specification, independently of the
implementation row. Complexity or uncertainty may warrant stronger settings.

| Impact | Reviewer default | Rationale and limits |
| --- | --- | --- |
| Low or medium impact | Terra (`gpt-5.6-terra`) at `high` for each axis | Capable mid-tier verification is the default for routine work |
| High impact, even with a tiny diff | Strongest evidenced relevant choice of Sol (`gpt-5.6-sol`) at `high` or Astra (`gpt-6-astra`) at `high` | Use separate fresh reviewer contexts; inspect high-impact negative cases |

Select reviewer overrides through the verified spawn schema above. Astra in
this table is an independent reviewer, not an implementation worker or a
replacement coordinator. Reviewer suitability remains a hypothesis until
evaluated on comparable work; a model listing is not live review verification.
Explicit user/project requirements and stronger evidence override these
defaults. Different models for the two axes remain optional.

Call collaboration tools through the interface actually exposed by the host.
Do not launch replacement sessions, change personal settings, install adapters,
or simulate multiple models by writing both sides of a conversation.
