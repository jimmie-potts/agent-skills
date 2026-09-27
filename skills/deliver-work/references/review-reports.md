# Publish and retain review evidence

Read before publishing a review-round report, an inline finding or a reply
about a fix, before updating the change review's summary, and when reconciling
any of these after an interruption. `review-work` returns each round's result
with the reviewers' retained returns; this coordinator is their only
publisher. [PR supervision](pr-supervision.md) owns reading feedback, and the
code-host adapter supplies the operations.

## Stay within the communication boundary

- An explicit delivery request authorizes, on its own change review: one report
  per completed or stopped final round, inline comments for its own blocking
  findings, the description's review section, and factual replies about its
  scoped fixes. Repository policy and narrower user limits prevail.
- It does not authorize replying to a disagreement, arguing a disputed finding
  or disposition, resolving any thread, submitting an approving or
  change-requesting review, dismissing a review, or posting anywhere else.
  Draft the needed response in the task, name the decision and its owner, and
  continue independent work. Existing explicit approval of an exact reply or
  resolution persists.
- Standalone `review-work` or `code-review` returns evidence and posts nothing
  unless the user names the destination.
- Reviewers never publish. A comment from the delivery's own account and a
  digest are evidence of what was retained, not native approval, independent
  sign-off or a tamper-proof attestation.

Keep all review evidence outside the candidate commit; publishing it never
creates a commit or changes the head it describes.

## Retain every final round

Each final round's report holds its result and every reviewer's retained
return, as review-work's `references/result-contract.md` defines them. The
report on the change review is the durable destination. Where reports are not
possible, use another existing destination the user or project authorizes and
link it from the change review.

When publication is denied, narrowed or unavailable, keep the result and
returns in the task evidence and the response, and report that they are
retained only in this conversation. The final review then counts as not
retained: do not report it complete or merge until an authorized destination
holds the round's evidence and reads back. Task rounds stay in the task
evidence.

## Report each final round

Publish one report after review-work returns a final round, or when a round
stops without a complete result, such as a failed reviewer, a limit or a user
stop. Never publish a round before its result. In order:

1. The effect's identity marker (see below).
2. `**Review gate for this comparison:**` followed by `satisfied` only when
   every required axis is `satisfied`; otherwise `not satisfied` and the
   blocking axes or gaps, or `stopped` and why.
3. The round's `## Review result` unchanged, with each reviewer return
   collapsed so the report stays short. Keep its bytes, so its digest still
   matches.
4. Each specialist or provider result, such as a security scan, with the
   revision and coverage it reports. A result for another head is
   `superseded` and never approves this one.

A report describes only its comparison, and later heads never edit it. When a
stopped round later completes on the same comparison, append the completion to
that report and keep the stopped content. Split a report longer than the
provider allows into ordered parts that share its key; never truncate a
return.

## Keep the current result in the description

Keep one `## Independent review` section in the change review's description:
a gate line, then one row per final round, newest last.

| State | Meaning |
| --- | --- |
| `pending` | A round for the current comparison has not returned; its cells are `-` |
| `current` | The latest completed round, whose comparison, requirement version and policy equal the current ones |
| `superseded` | A completed round whose comparison, requirements or policy has since changed |
| `stopped` | A round that ended without a complete result |

Write `**Review gate:** satisfied for head <full sha>` only when the last row is
`current`, every required axis in it is `satisfied` and its report link reads
back; otherwise write `**Review gate:** not satisfied:` with the reason. A
changed head, requirement or policy marks the current row `superseded` and adds
a `pending` row. Read the description immediately before each update, change
only this section, and read it back.

```markdown
## Independent review

**Review gate:** not satisfied: final 3 pending for head 4444444444444444444444444444444444444444

| Round | Comparison | State | Standards | Specification | Specialist | Report |
| --- | --- | --- | --- | --- | --- | --- |
| final 1 | `1111111..2222222` | superseded | action-required | action-required | security: satisfied | [report](https://github.com/example-org/example-app/pull/43#issuecomment-101) |
| final 2 | `1111111..3333333` | superseded | satisfied | satisfied | security: satisfied | [report](https://github.com/example-org/example-app/pull/43#issuecomment-102) |
| final 3 | `1111111..4444444` | pending | - | - | - | - |
```

## Post blockers where they apply

Post a P0 to P2 or project-defined blocker inline when it has a file and line
in the reviewed diff and the round first reports it, batching the round's new
inline findings in one non-approving review. Put blockers without a diff line,
missing acceptance evidence, scope gaps and P3 findings in the report only. Do
not repost a finding that keeps its ID; later reports cite it. When review-work
marks it `resolved` or `regression`, add one factual reply to its thread naming
the revision and the round that established it.

## Reply about scoped fixes

After a pushed head fixes published feedback within scope, reply once in that
item's thread: what changed, the revision, and the check or round that verified
it. Facts only. Feedback that is declined, disputed or out of scope gets a
drafted response for its owner, not a reply. Never resolve the thread.

## Identify each effect and recover it

Key each effect by work and purpose: `report final <n>`, `finding <ID>`,
`reply <ID> <state> final <n>`, or `reply <feedback ID> <version>` for another
author's item. Embed the key, the work reference and the reviewed head in a
hidden marker in the body. Before the request, record the intent, key and
intended digest in the [task packet](resumption.md); after it, read the effect
back by its returned ID and record that ID and link.

Before publishing, and after a timeout, lost response or resumption, read every
page of the destination for the key. A cached or incomplete read proves
nothing, so the result stays unknown and dependent effects pause.

- One match with the intended content: applied. Record it; do not repeat it.
- No match after a complete read: not applied. Publish once with fresh
  prerequisites.
- Several matches: the earliest is canonical. Record the others as duplicates
  and link only the canonical one; removing them needs authority.
- A match with different content: your own partial post is completed by
  editing that effect, not by posting another; another actor's edit is
  feedback.

An item is this delivery's own effect only when it carries this delivery's
marker, came from the publishing account and matches a recorded intent. It is
not a new request. Treat any other item, including one from the same account
without that match, as feedback under [PR supervision](pr-supervision.md).
Uncertain effects otherwise follow [recovery](recovery.md).
