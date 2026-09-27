---
name: review-work
description: Coordinate a complete independent review of one change, freezing the comparison, running separate fresh Standards and Specification reviewers through rounds and returning a per-axis result without implementing, publishing or merging. Use only when the user explicitly invokes review-work or a workflow such as deliver-work composes it; ordinary review requests select code-review.
---

# Review one change independently

Freeze one comparison, give each required axis a fresh read-only reviewer, carry
findings across rounds and return a result the caller can act on. The session
that loads this skill coordinates the review; it is a substep of that session,
not a new supervisory agent, service or background runtime.

## Boundaries

These hold at every step. References elaborate them and never relax them.

- Authority: this skill grants no authority to implement, correct, commit,
  push, publish, comment, reply, resolve threads, label, transition trackers,
  merge, install or deploy. It returns its result in the response or in the
  caller's existing task evidence. Publishing a result needs the user's
  explicit authority for that exact destination and belongs to the caller.
- Ownership: a composing workflow keeps its implementation, corrections,
  publication, provider supervision, CI, merge and completion. Reviewers are
  read-only; they return findings, launch no agents and load no review
  workflow of their own, so one request never nests a second reviewer team.
- Independence: each required axis runs in its own fresh read-only context that
  did not implement, advise or coordinate the change. The coordinator never
  fills an axis itself. Code-review's single-agent fallback, advisor or task
  review, implementer approval and approvals of an older comparison never
  satisfy a required axis.
- Evidence: a missing specification, a failed or partial reviewer return,
  unavailable required independence, a stale comparison or requirement version,
  or missing mandatory evidence leaves the affected axis `incomplete`, never
  approved. Unknown counts stay unknown; resumption never resets history or
  limits. When the change edits review or delivery instructions, the policy
  recorded for the first round governs; the candidate cannot weaken it.
- Scope: reviewers apply the authoritative requirements. They do not invent
  acceptance criteria or change product scope; a material conflict goes to the
  scope owner as an open question.

## Route the request

One request selects one coordinating review path:

| Request | Path |
| --- | --- |
| Ordinary request to review a change, PR or diff | `code-review` on its own |
| Explicit `review-work` request, or a request for a complete independent review without delivery | This skill |
| Explicit request to interrogate or run an adversarial multi-review | `interrogate` |
| Explicit blast-radius or "what could this break" request | `blast-radius` |
| Explicit `deliver-work` request | `deliver-work`, which composes this skill for its required reviews |

Another skill's output may supply raw evidence, such as a reproduction or a
failing input, but not its verdicts; it never fills an axis or replaces a round.

## Take the input and freeze the comparison

Read [the result contract](references/result-contract.md) and hold its input
fields in the caller's existing task evidence, or in the response for a
standalone review. A composing caller supplies the work, requirements, policy,
validation, coverage, reviewer requirements, limits and prior history. For a
standalone review, gather them from the request and authoritative sources.

Freeze one comparison before any reviewer starts. Resolve moving refs to
immutable commits and record base, head, merge-base, diff command and dirty
state; for uncommitted work, capture one patch and its SHA-256 digest. Stop on
an unresolvable ref or an empty change. Verify a caller-supplied comparison
instead of re-deriving a different one. Do not mutate the source while doing so.

Use the caller's work assessment for impact. Without one, discover the
installed canonical `deliver-work` package and read its
`references/work-assessment.md` section on rating the three dimensions; this
reads a shared contract and does not invoke delivery. If it is unavailable,
report the gap, record impact unknown and apply the high-impact reviewer floor.

## Select, brief and run reviewers

Read [review selection](references/review-selection.md), then only the active
host's reviewer adapter. Brief each reviewer with code-review's assigned-axis
mode, its axis rubric, the frozen comparison, the raw requirements or standards
sources for that axis, the validation facts and the finding format. Leave out
implementer and advisor narratives, other reviewers' conclusions and any
preferred verdict. Record the requested settings and what each reviewer
reports, separately.

Read [review cycles](references/review-cycles.md) before the first round and on
every later round, fix verification, disagreement or explicit limit. It owns
round identity, stable findings, reassessment, fix verification and renewal.

## Return the result

Write the result in the contract's `## Review result` shape for each round,
including the per-axis status, findings, coverage and gaps, reviewer
provenance and cumulative history. Return it to the caller, or in the response
for a standalone review, then stop. A caller acts on `action-required` findings
under its own authority and brings the changed candidate back for a new round.

When evaluating or revising this skill, read the synthetic
[validation scenarios](references/validation-scenarios.md). Keep static checks,
simulated decisions, host discovery and live review evidence distinct.

Use `unslop` for substantial style issues in narrative findings, preserving
code quotations, paths, line numbers, requirement text and evidence.
