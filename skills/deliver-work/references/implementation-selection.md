# Select and continue investigation or implementation workers

Read for worker selection, implementation strategy changes, or an inadequate
worker return. Direct trivial work at the coordinator's existing settings needs
no worker selection. Apply [the common policy](model-selection.md) and only the
selected host's worker adapter. Planning consumers remain read-only.

Complexity determines suitable coding capability; interacting state may need
higher reasoning and testable decomposition. High uncertainty requires
investigation or clarification before dependent implementation. High impact
sets a stronger capability floor even for a tiny diff; choose the strongest
evidenced relevant option when suitability is uncertain. Do not average ratings
or try to replace a missing product decision with a stronger model.

## Choose an implementation strategy

For decomposed or delegated work, read [task planning and dispatch](task-planning.md)
before selecting a strategy. Establish required-input readiness and independent
contracts/resources; file paths alone do not justify parallel workers.
Direct coordinator implementation is the baseline: use it
for trivial work or continuously difficult reasoning when existing settings
suit the task. For eligible bounded work, apply the host adapter's cheaper
worker default; merely fitting one context does not override it. Judge
alternatives by cost per completed task, including
corrections and reruns, rather than tokens per request. Use one bounded worker
when different settings or isolation materially help, and separate bounded
workers when the work splits into independent pieces or exceeds one context.
Workers return proposed patches and evidence; the coordinator applies changes.
Give each worker outcome, source/revision, applicable instructions, assessment,
acceptance mapping, constraints, ownership, and the
[bounded brief and return contract](worker-briefs.md). Use a self-contained
brief when overrides prevent full-history inheritance.
Distinguish requested settings from observable runtime identity.

Name the chosen strategy in the record. The strategies are direct
implementation by the coordinator; an assigned worker with one brief and no
advisor loop; parallel workers for independent pieces, which the coordinator
merges; and the advisory pairing, where one worker runs the implementation
loop and consults the coordinator at approach, blocker, and final review. The
coordinator owns durable writes and runs the independent reviews as a separate
step under every strategy.

Choose the host's advisory pairing when bounded, capable worker implementation
benefits from coordinator approach/blocker checkpoints: serial work with a few
hard decision points rather than continuous difficult reasoning. Select the
pairing skill from verified host tooling, never from a persona or a model list.
Codex collaboration tools select worker-with-astra. Claude Code subagent tools
select worker-with-fable. Any other host has no pairing. Discover and read the
selected skill and its host adapter before starting. Its original-coordinator
identity, worker availability, parent communication or worker resumption, and
consultation requirements remain mandatory. Record what the worker can decide
and what requires consultation. Apply selected reasoning through supported
controls without changing the advisor.

When difficult reasoning is continuous rather than separable into checkpoints,
prefer direct implementation or a directly assigned, suitably capable worker.
If an optional pairing cannot be established, choose another suitable strategy
and disclose why. If the user explicitly requested the pairing, report its
unmet prerequisite; do not create a replacement advisor or silently substitute
another arrangement. Advisory inspection never replaces independent delivery
reviews.

## Correct, consult, or hand off an attempt

A correction asks the same worker to repair its result. A consultation asks the
same original advisor for a decision and pauses dependent work until answered.
A promoted attempt starts a fresh worker when supported settings cannot change
in place. These events have separate counts. Apply the host adapter's failure
policy where defined; otherwise use the shared evidence-based reassessment
rule below. Preserve explicit model/pairing requirements.

Diagnose an inadequate result before changing settings. For a new attempt,
stop the old assignment and verify its state before transferring ownership.
Carry its artifact or patch, source/candidate revision, acceptance criteria,
failed checks and outcomes, attempt/settings history, unresolved question,
permissions and write ownership in a self-contained brief. Preserve history
across replacements and resumptions; do not pass a new spawn off as a resume.
Host adapters own stop/spawn/resume mechanics. An unavailable stop or required
control blocks the affected replacement, not independent authorized work.

When composing delivery, carry this state in the canonical
[task packet](resumption.md), including task/attempt identity and artifact source
revisions. Reconcile it before resuming or accepting a late result. A planning
consumer only proposes the handoff; reading this policy does not start delivery.

For a new advisory attempt, retain the original advisor and re-establish all
pairing prerequisites and mandatory approach/final consultations. A standalone
pairing reports the inadequate attempt to its coordinator; the composing
workflow chooses promotion. Explicit requirements have no silent fallback.
Use existing labeled worker returns and task evidence; include handoff rationale
and history without replaying transcripts. Advice never expands authority.

## Reassess and report

Use the review-cycle diagnosis when a blocker survives a correction or new
blockers reveal misunderstood behavior. Keep findings and rounds in existing
evidence; read the selected host's worker adapter for escalation, without resetting
its allowance when the reviewer, finding wording or candidate changes.

Reassess on material scope changes, disproved assumptions, repeated failure
without new progress, or blocking findings exposing misunderstood behavior.
Diagnose the gap: stronger settings may help reasoning, investigation supplies
facts, and users decide unresolved product choices or authority. Retry only
with a changed approach and explicit expected result; a stronger worker tier
for the affected step is a changed approach. Unresolved repeated failures
require a concrete blocker rather than an unbounded loop. Continue independent
authorized work.

Record source/candidate revision, assessment, role, strategy, coordinator and
worker requested model/reasoning separately, observable runtime settings,
correction/attempt history, attributable usage, consultation count for a pairing,
rationale, fallback/escalation, and verification limits in existing task evidence.
During delivery, use [execution reporting](execution-reporting.md) to expose the
decision owner and contributors, model roles, and planned versus actual agent
counts at selection, team changes, checkpoints, and final handoff. A planning
consumer records proposed selections as planned; reading this policy does not
start delivery or agents. Keep public PR evidence free of private runtime metadata
and do not invent telemetry. Reuse still-current evidence, renew affected tests
and reviews, and retain mandatory requirements throughout reassessment.
