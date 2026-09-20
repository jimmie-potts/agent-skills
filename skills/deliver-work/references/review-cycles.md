# Control review cycles and explicit limits

Read before selecting task reviews, starting a review/correction cycle, or
working under explicit round, time or spending limits. This reference owns
review progress, finding continuity, fix verification and stopping decisions.
[Model selection](model-selection.md) and its host adapters own worker settings
and correction thresholds. [PR supervision](pr-supervision.md) owns provider
feedback and check reruns. Preserve the composing workflow's authority and gates.

Keep this evidence in the existing [task packet](resumption.md) or authorized
work record. Do not add a ledger, service, executable router or storage format.

## Separate rounds, attempts and corrections

- A worker attempt is an implementation or investigation assignment at one
  selected configuration. Replacement or promotion starts another attempt,
  while preserving the unresolved task's failure history and used allowances.
- A guided correction asks the same worker at unchanged settings to repair an
  evidenced defect. Count it separately from attempts.
- A review round assesses one frozen candidate comparison. A task round returns
  distinct specification and quality verdicts. A whole-change round contains
  the separate independent Standards and Specification perspectives required
  for delivery. Two perspectives do not double that round.
- Provider feedback, check reruns and advisor consultations keep separate counts
  and identities. Reading a comment or accepting a worker return is not itself
  an independent candidate review.

Before review starts, record a round identity, review kind and task boundary,
accepted scope/inputs, base/head and merge-base or artifact digests, comparison
command, validation evidence and coverage. Retain incomplete rounds and missing
perspectives as such. Clarifying an active assessment belongs to that round;
reassessing a repaired candidate is a new round, even if called fix verification.
Multiple compatible corrections may be batched before the next review, within
the host's worker allowances. Intermediate commits do not themselves add rounds.
Changing scope, inputs, base, head or content requires a new frozen comparison
and renewal of affected evidence. Resuming or renaming work never resets history.

## Select intermediate task review

Select independent task review when downstream work relies on the result or
assessed risk warrants inspection before integration. Record the task boundary,
reason and required evidence, for example a producer contract consumed by later
tasks or a small high-impact permission change. Trivial edits and same-shape
mechanical batches do not automatically need another context. Use proportional
acceptance evidence unless dependency, risk or project policy requires review.

For a selected review, use a fresh read-only context independent of the
implementer. Supply raw requirements, task/attempt identity, accepted inputs,
fixed artifact/diff, actual validation, coverage and limits. Apply the selection
policy's reviewer suitability and impact floor. Require separate verdicts:

- Specification: scoped requirements, exclusions, inputs and acceptance criteria.
- Quality: implementation, tests, failure behavior, affected contracts and the
  integration boundary.

One independent task reviewer may return both verdicts unless project policy
requires separate contexts. A failed or missing verdict withholds task acceptance
and dependent work. Report the gap if required independence is unavailable;
continue unrelated authorized work. Passing task review, advisor inspection and
implementer approval replace neither final independent delivery review.

## Preserve finding identity

Assign each finding a stable task-local identifier. Retain severity, affected
behavior and governing requirement; first and latest reviewed comparisons;
attempted corrections with worker/attempt and resulting revision; changed approach;
covering checks and actual results; disposition, reason, owner and confirming
review evidence. Link existing feedback records rather than copying transcripts.

Distinguish these states:

- Unresolved: the behavior remains defective or required evidence is missing.
- Resolved: current evidence establishes the correction or an accepted,
  independently reassessed disposition.
- Regression: a previously resolved finding returns. Reopen the same identifier
  and retain the prior resolution and returning revision.
- New: a materially different failure condition or requirement gap. Assign its
  own identifier, linking related causes when useful.

Rewording, changing reviewers/workers or resuming preserves identity and history.
Keep aliases for duplicate descriptions. Reconcile ambiguous identity against
behavior and evidence before using it to justify another attempt. Missing
transcripts or private runtime metadata do not require a reset.

Fix P0-P2 defects and all project-defined blockers. Retain accepted or deferred
P3 dispositions with reason and owner; do not leave minor findings unaccounted
for. Disputes need concrete evidence and independent reviewer reassessment.
Implementer assertions, model votes and exhausted budgets cannot resolve findings.

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

Continue productive, severity-driven rounds without a universal numerical cap.
Progress needs evidence that behavior, acceptance coverage or understanding has
improved; fewer findings alone prove none of these. Repeated new blockers that
expose the same misunderstood behavior also trigger reassessment. Do not keep
retrying an unchanged approach. If reassessment yields no viable changed action,
report the concrete blocker and next owner while preserving unfinished work.

## Verify fixes at the necessary boundary

Start from stable finding IDs and the exact revision previously reviewed. Supply
the prior findings, raw requirements, current full comparison, intervening fix
diff and actual validation. Return an evidenced disposition for each finding,
including covering checks/results, and inspect the repair for new defects.
These are fix-verification inputs, not a preferred approval conclusion.

Begin with the correction and affected behavior. Expand inspection when concrete
evidence points to an affected contract, unchanged consumer, shared state,
migration or failure path. A diff-only rule cannot hide a material interaction.
Record the expansion and reason. Reuse unrelated factual evidence only while
its inputs and coverage remain valid. Batch compatible fixes while preserving
per-finding history, failed checks, remaining blockers and minor dispositions.

## Honor explicit limits

Before limited work starts, record each user/repository limit's source, scope,
unit and threshold, starting count/time, observable accounting source and owner.
Distinguish task, whole-delivery, worker-retry and review-round scopes. State
whether task rounds are included. Apply the source's counting definition;
resolve material ambiguity before dependent bounded work. Track started and
in-flight rounds so an unfinished assessment cannot disappear from accounting.

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

## Renew the final independent axes

For whole-change review, freeze one comparison and compose `code-review` in
separate independent read-only Standards and Specification contexts as the
entrypoint requires. Give initial reviewers raw sources and validation facts,
without implementer/advisor approval narratives, other reviewers' conclusions
or a preferred verdict. Share conclusions for reassessment only after independent
initial findings. Missing authoritative acceptance evidence cannot pass
Specification; one axis cannot supply the other.

Changed final scope, base, head or content requires both axes to assess the new
comparison. Renew affected tests and any required specialist/human evidence.
Unrelated underlying evidence may remain usable, but old whole-change approvals
do not approve the new comparison. Required current PR/head CI, guarded merge
and completion checks remain independent gates. A candidate modifying these
instructions cannot waive the agreed gates used to approve it.

Planning consumers carry proposed review boundaries, explicit limits and required
accounting/handoff evidence into work items. Publication of future constraints
does not start their counters, reviews, workers or implementation. Preserve
proposal-only, tracker-only and deferred-selection boundaries.

Design reference: [Superpowers fix verification](https://github.com/openai/plugins/blob/33bd9529725fcee78c9e51fcbaa93cd963c3a47b/plugins/superpowers/skills/subagent-driven-development/re-review-prompt.md)
informs the prior-revision and per-finding inputs. Its unconditional exclusion of
risks outside the fix diff and its model defaults are not adopted.
