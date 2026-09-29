# Run review rounds and track findings

Read before the first round and before every later round, fix verification,
disagreement or explicit limit. This reference owns round identity, stable
findings, evidence-based reassessment, fix verification and renewal of the
final axes. [Review selection](review-selection.md) and its host adapters own
reviewer settings. A composing workflow owns corrections, worker attempts,
provider feedback and check reruns; keep their counts separate from rounds.

Keep this evidence in the [input and result](result-contract.md) records held
in the caller's existing task evidence. Do not add a ledger, service,
executable router or storage format.

## Identify rounds

A review round assesses one frozen comparison. A final round contains the
separate independent Standards and Specification perspectives the caller
requires, plus any stricter project requirement such as a specialist axis. A
task round returns distinct Specification and Standards verdicts for one task
boundary; in a task round, Standards judges implementation quality, tests,
failure behavior, affected contracts and the integration boundary. Two
perspectives on one comparison are one round, not two.

Before a round starts, record its identity and the full input. Retain incomplete
rounds and missing perspectives as such. Clarifying an active assessment,
reassessing a dispute on the same comparison, and replacing a failed reviewer
return on that comparison all belong to that round. Retain a failed return's
findings in the history, but keep them out of the replacement reviewer's initial
brief. Reassessing a repaired candidate is a new round, even when it is called
fix verification. Intermediate commits the caller makes between rounds add no
rounds. Changing scope, requirements, project policy, base, head or content
requires a new frozen comparison. Resuming or renaming work never resets
history.

Provider feedback, check reruns, worker corrections and advisor consultations
keep their own counts and identities. Reading a comment or accepting a worker
return is not an independent review.

## Run a task round

The caller names the task boundary and the reason it needs inspection. Use a
fresh read-only context independent of the implementer, with the raw
requirements, task and attempt identity, accepted inputs, fixed artifact or
diff, actual validation, coverage and limits. One reviewer may return both task
verdicts, recorded with the axis `both`, unless project policy requires separate
contexts. A failed or missing verdict leaves the round `incomplete` and
withholds task acceptance and dependent work. Report the gap when required
independence is unavailable; the caller continues unrelated authorized work.
Passing task review never replaces the final axes.

## Preserve finding identity

Give each finding a stable task-local identifier. Retain severity, axes,
affected behavior and governing requirement; first and latest reviewed
comparisons; the corrections the caller reports, with the worker and attempt,
any changed approach and the resulting revisions; covering checks and actual
results; disposition, reason, owner and the review evidence that confirmed it.
Link existing feedback records rather than copying transcripts.

- Unresolved: the behavior remains defective or required evidence is missing.
- Resolved: current evidence establishes the correction or an accepted,
  independently reassessed disposition.
- Regression: a previously resolved finding returns. Reopen the same
  identifier and retain the prior resolution and the returning revision.
- New: a materially different failure condition or requirement gap. Assign its
  own identifier, linking related causes when useful.

Rewording, changing reviewers or workers, and resuming preserve identity and
history. Keep aliases for duplicate descriptions, and record a reviewer's own
IDs as the result contract's axis aliases. For a failure condition that
reviewers on more than one axis raise, follow the
[result contract](result-contract.md#write-the-result).
Reconcile ambiguous identity against behavior and evidence before reporting it.
Missing transcripts or private runtime metadata do not require a reset.

P0 to P2 findings and project-defined blockers make each axis they list
`action-required`, except findings from a failed return, which leave it
`incomplete` as [reviewer execution](reviewer-execution.md) describes. Record a
disposition for every P3 finding with its reason and owner. A round that returns
only P3 findings starts no correction round by itself; the caller disposes of
them in one pass and folds any fixes into a later candidate only when one is
needed for another reason.

## Settle disagreements with evidence

Initial reviewers work from raw sources. Share one reviewer's conclusions with
another only after both have returned independent initial findings. A dispute
needs concrete evidence, such as a reproduction, a failing or passing check, or
a cited requirement, and reassessment by an independent reviewer. Implementer
assertions, reviewer vote counts, pressure to approve and exhausted budgets
cannot resolve a finding.

A reviewer cannot add an acceptance criterion or change product scope. When a
finding depends on a requirement that the authoritative sources do not state,
or on a conflict between them, record it as an open question for the scope
owner. It blocks only the work it governs.

## Verify fixes at the necessary boundary

Start from the stable finding IDs and the exact comparison previously reviewed.
Supply the prior findings, raw requirements, the current full comparison, the
intervening fix diff and actual validation. Ask for an evidenced disposition of
each finding, including covering checks and results, and an inspection of the
repair for new defects. These are inputs, not a preferred conclusion.

Begin with the correction and the affected behavior. Expand when concrete
evidence points to an affected contract, unchanged consumer, shared state,
migration or failure path; a diff-only rule cannot hide a material interaction.
Record the expansion and why. Reuse unrelated factual evidence only while its
inputs and coverage remain valid.

## Renew the final axes

Both final axes assess every changed final comparison. Still-valid factual
evidence, such as an unaffected check result, may be reused; an old whole-change
approval never approves a new comparison. A later round may resume the same
reviewer context when it stayed independent and none of its returns failed; it
remains a fresh reviewer in the sense that it never implemented, advised or
coordinated the change, and it assesses the new comparison in full. Renew any
required specialist or human evidence the change affects. When the change edits
review or delivery instructions, the first round's gates are a floor that the
candidate cannot lower; record policy as the result contract describes.

## Honor explicit limits

Record each explicit round, time or spending limit in the input before limited
work starts, with the counting definition its source gives. Check remaining
capacity before each round, including rounds already in flight, and start none
beyond the limit. Missing accounting is unknown, never zero; when compliance
with a hard cap cannot be established, do not start the round. Without an
explicit cap, unknown cost creates no gate. Introduce no default cap; productive
severity-driven rounds continue while the caller keeps supplying changed
candidates.

At the limit, return the latest result unchanged for the comparison it
reviewed, with the unresolved finding IDs, the consumed and unknown capacity
and the next owner. Any later candidate has no result: its axes are
`incomplete`. A resumed or renamed review gets no fresh
allowance. An exhausted limit never resolves a finding or satisfies an axis.

Design reference: [Superpowers fix verification](https://github.com/openai/plugins/blob/33bd9529725fcee78c9e51fcbaa93cd963c3a47b/plugins/superpowers/skills/subagent-driven-development/re-review-prompt.md)
informs the prior-revision and per-finding inputs. Its unconditional exclusion of
risks outside the fix diff and its model defaults are not adopted.
