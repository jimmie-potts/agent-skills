# Correct findings and honor explicit limits

Read before acting on a review result, correcting a finding or failed
acceptance, diagnosing a surviving blocker, or working under an explicit round,
time or spending limit. The composed `review-work` skill owns review rounds,
finding identity, fix verification and the per-axis result.
[Model selection](model-selection.md) and its host adapters own worker settings
and correction thresholds. [PR supervision](pr-supervision.md) owns provider
feedback and check reruns.

Keep this evidence in the existing [task packet](resumption.md) or authorized
work record. Do not add a ledger, service, executable router or storage format.

## Separate attempts, corrections and rounds

- A worker attempt is an implementation or investigation assignment at one
  selected configuration. Replacement or promotion starts another attempt,
  while preserving the unresolved task's failure history and used allowances.
- A guided correction asks the same worker at unchanged settings to repair an
  evidenced defect. Count it separately from attempts.
- A correction pass is each new candidate made to resolve findings or failed
  acceptance, by a worker or by the coordinator. Compatible fixes batched
  before the next review count once.
- Review rounds come from review-work's result. Provider feedback, check reruns
  and advisor consultations keep their own counts.

## Act on a review result

Treat `satisfied` on both final axes for the current comparison and requirement
version as the review gate's evidence; CI, merge and completion gates remain
separate. For `action-required`, correct the P0 to P2 findings and every
project-defined blocker within scope, then bring the changed candidate back to
review-work for a new round with the finding IDs and the fix diff. For
`incomplete`, obtain the missing specification, reviewer, control or evidence
it names, or report the gap and its owner; never treat it as approval. Record
a disposition for each P3 finding; a P3-only result starts no correction pass
by itself.

Disputed findings go back to review-work with concrete evidence for
independent reassessment. A finding that depends on a requirement the sources
do not state goes to the scope owner; the implementer's assertion never
settles it.

## Diagnose a surviving blocker

When a blocker survives correction, diagnose it before another attempt:

| Cause | Next action and evidence |
| --- | --- |
| Capability or reasoning limitation | Apply the current host adapter's correction/promotion policy to the failure evidence and changed brief. |
| Missing facts or inputs | Obtain the bounded source, versioned contract or runtime evidence from its owner before dependent work. |
| Unclear or conflicting requirements | Obtain an authoritative decision and renew affected scope/acceptance evidence. |
| Infrastructure fault or broken check | Diagnose or repair within authority, then obtain actual check results; do not alter product behavior merely to get green. |
| Unavailable authority or capability | Identify the owner and needed permission/control, or an authorized alternative; pause the dependent action. |

Record the cause, changed approach and expected evidence. Recurrence alone does
not mandate a stronger model. Read the
[Codex](codex-model-selection.md) or [Claude Code](claude-code-model-selection.md)
adapter for its distinct worker threshold. Review counts do not replace, reset
or copy those thresholds.

Continue productive, severity-driven corrections without a universal numerical
cap. Progress needs evidence that behavior, acceptance coverage or
understanding has improved; fewer findings alone prove none of these. Repeated
new blockers that expose the same misunderstood behavior also trigger
reassessment. Do not keep retrying an unchanged approach. If reassessment
yields no viable changed action, report the concrete blocker and next owner
while preserving unfinished work.

## Honor explicit limits

Before limited work starts, record each user/repository limit's source, scope,
unit and threshold, starting count/time, observable accounting source and owner.
Distinguish task, whole-delivery, worker-retry and review-round scopes. State
whether task rounds are included. Apply the source's counting definition;
resolve material ambiguity before dependent bounded work. Pass review-round
limits and their consumed amounts to review-work in its input. Track started
and in-flight work so an unfinished assessment cannot disappear from
accounting.

Check remaining capacity before corrections, dispatch, renewed review and
consequential effects, and at responsive checkpoints during active work. Account
for in-flight commitments or reliable upper bounds before starting more work.
Do not introduce a default spend allowance or review cap. Keep subscription
usage separate from API dollars. Missing telemetry is unknown, never zero.
If a hard cap cannot be enforced with observable accounting or a reliable bound,
pause actions whose compliance cannot be established. Reconcile the gap or
obtain a limit/control decision; continue independently authorized work outside
that limit. Without an explicit cap, unknown cost alone creates no spending gate.

At the limit, start no more affected attempts, corrections, reviews or dependent
work. Safely stop owned in-flight work through supported controls; reconcile
pending external effects rather than duplicating or forgetting them. Record any
unavoidable overrun or unknown outcome. Preserve partial artifacts and hand off:

- unresolved finding IDs and dispositions, attempted fixes and changed approach;
- last reviewed and current revisions, valid/stale/missing evidence and results;
- separate round/attempt/correction counts, limit scope, used or unknown capacity;
- incomplete gates, next action and responsible owner.

If correction finishes before the limit but renewed review cannot run, keep the
changed candidate unreviewed. Renaming a review, replacing a worker or resuming
does not create another allowance. Budget exhaustion cannot authorize merge,
resolve a finding, supply evidence or establish completion. Preserve any narrower
local-only, ready-PR-only or explicit watch boundary.

Planning consumers carry proposed review boundaries, explicit limits and required
accounting/handoff evidence into work items. Publication of future constraints
does not start their counters, reviews, workers or implementation. Preserve
proposal-only, tracker-only and deferred-selection boundaries.
