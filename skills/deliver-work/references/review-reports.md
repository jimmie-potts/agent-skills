# Publish and retain review evidence

Read before publishing a review-round report, an inline finding or a factual
fix reply, updating the change review's summary, resolving a delivery-owned
thread, or reconciling any of these after interruption. `review-work` returns each round's result
with the reviewers' retained returns; this coordinator is their only
publisher. [PR supervision](pr-supervision.md) owns reading feedback, and the
code-host adapter supplies the operations.

## Stay within the communication boundary

- An explicit delivery request authorizes its own review evidence on its own
  change review: one report per completed or stopped final round, inline
  comments for its own blocking findings, the description's review section,
  and factual replies about its findings' states and its scoped fixes.
  Repository policy and narrower user limits prevail.
- It also authorizes resolution of an attributable delivery-owned thread only
  through [the verified-fix procedure](#resolve-a-delivery-owned-thread) below.
  It does not authorize replying to a disagreement, arguing a disputed finding
  or disposition, resolving other threads, submitting an approving or
  change-requesting review, dismissing a review, or posting anywhere else.
  Draft the needed response in the task, name the decision and its owner, and
  continue independent work. Existing explicit approval of an exact reply or
  resolution persists.
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
3. The round's `## Review result` with its bytes unchanged. The adapter may
   wrap each reviewer return in a collapsible block to keep the report short;
   removing that wrapper restores the contract shape and each digest.
4. Each specialist or provider result, such as a security scan, with the
   revision and coverage it reports. A result for another head is
   `superseded` and never approves this one: a required axis it would fill is
   `incomplete` for this comparison.

A report describes only its comparison, and later heads never edit it. When a
stopped or incomplete round later gains a return on the same comparison, such
as a replacement or a required specialist reviewer, append it and the updated
result to that report and keep the earlier content.

Never truncate a return. When a report exceeds the provider's size limit, split
it at line boundaries into parts keyed `report final <n> part <i>/<m>`, fixing
the split before the first part is posted. Each part is its own effect with
its own intent and digest. A return split across parts repeats its fence
opening and closing in each part; its digest covers the fenced lines of all its
parts concatenated in part order. The report is published only when every part
is applied; the description links part 1.

## Keep the current result in the description

Keep one `## Independent review` section in the change review's description:
a gate line, then one row per final round, newest last.

| State | Meaning |
| --- | --- |
| `pending` | A round for the current comparison has not returned; its cells are `-` |
| `current` | The latest completed round, whose comparison, requirement version and policy equal the current ones |
| `superseded` | A completed round whose comparison, requirements or policy has since changed |
| `stopped` | A round that ended without a complete result |

The `Specialist` cell is `none` when no specialist axis is required, `-` while
pending, or `<name>: <status>` entries joined by `, ` in the axis vocabulary.

Write `**Review gate:** satisfied for head <full sha>` only when the last row is
`current`, every required axis in it is `satisfied` and its report link reads
back; otherwise write `**Review gate:** not satisfied:` with the reason. A
changed head, requirement or policy marks the current row `superseded` and adds
a `pending` row. Read the description immediately before each update, change
only this section, and read it back. A description update has no key: after an
uncertain update, compare the section read back with the intended one.

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
drafted response for its owner, not a reply. Thread resolution is a separate
operation with the requirements below.

## Resolve a delivery-owned thread

Use this procedure only within an authorized delivery. Explicit owner limits
and stronger project rules requiring owner disposition prevail. Do not use
the new resolution authority to deliver the change that introduces it: that
delivery follows its original policy unless the owner separately authorizes
the scoped resolution.

1. Establish attribution from this delivery's recorded publication intent,
   marker, publishing account, stable finding identity and exact provider thread
   ID. Match the originating comment to that record. A shared account, bot-like
   wording or a copied marker alone is insufficient. Unknown origin stays with
   its owner; do not infer agent authorship.
2. Require an actual scoped fix and independent verification under review-work
   on the current frozen base/head, requirements and policy. The finding must
   be `resolved`: every axis listed for it must confirm the fix in its retained
   return. The verifier must not have implemented, advised or coordinated the
   change.
   An accepted risk, P3 disposition, self-check or outdated diff marker does not
   establish a fixed finding. Changed scope, policy, requirements, base or head invalidates affected proof.
3. Read the whole current thread, including every comment page, edits and
   follow-ups, immediately before acting. Reconcile it with the verified
   finding and publication record. Human-authored or unknown-origin follow-ups, a substantive
   disagreement, out-of-scope content, changed content not yet assessed or an
   incomplete read stops automatic resolution. Obtain the owner's disposition
   for human, disputed or unknown-origin content; a shared account does not
   establish a follow-up's origin, and silence is not consent.
4. Publish any necessary factual fix/evidence reply once using the effect key
   below. A verified existing reply is reused. Record resolution intent with
   the exact thread ID, current candidate, fix-verification reference and last
   complete thread version/read. Refresh authority, requirements, policy, base/head and complete thread
   content after a reply or any intervening change before dispatch. Stop on a changed prerequisite.
5. Resolve that thread through the supported provider operation, then read back
   its resolved state and complete content. Record the returned identity and
   last confirmed effect. Providers may lack an atomic thread-version guard:
   a fresh read narrows the race but cannot eliminate it. If readback exposes
   new human/disputed or unknown-origin content, incomplete readback or drift,
   report the observed state and gap, keep disposition and
   merge eligibility pending, and obtain its owner's decision. Do not claim
   that the resolved flag settles the new content, or automatically undo it.

A timeout, lost response or failed readback for a reply or resolution is an
uncertain effect. Pause resolution and dependent merge actions. Reconcile the
exact recorded intent under [recovery](recovery.md), reading the complete
thread and refreshing current prerequisites before another request. A matching
reply or confirmed resolved state requires no repeated operation; retain the
observed effect without inferring who caused it.

An unresolved thread or absent reply alone does not prove that a delayed
request cannot still apply. Retry only after the prior attempt is verified not
applied, no attempt remains in flight, all prerequisites are refreshed, and
existing authority and limits permit it. Incomplete or changed evidence
permits no retry. Retain intent, attempts, limits and new follow-ups in the
same task packet. Neither a new turn nor a new effect key resets that history
or creates another allowance.

| Operation | Authority and evidence |
| --- | --- |
| Factual scoped fix reply | Existing delivery authority; deduplicated publication and factual evidence |
| Delivery-owned thread resolution | All five steps above; no extra owner question when they pass |
| Human, disputed, unknown-origin or out-of-scope thread | Owner disposition; draft the requested action while independent work continues |
| Native approval/change request or review dismissal | Not authorized by this procedure |
| Merge | Both fresh final axes, required specialist/human reviews, project review-count floors, unresolved-finding rules, current CI and guarded merge remain required |

## Identify each effect and recover it

Key each posted effect by work and purpose: `report final <n>`, with
`part <i>/<m>` when split, `finding <ID>`,
`reply <ID> <state> final <n>`, or `reply <feedback ID> <version>` for another
author's item. A resolution uses `resolve <thread ID> <finding ID> <head>`
in the local intent record; the provider operation has no comment body. Embed
posted effects' key, the work reference and the reviewed head in a
hidden marker in the body. Before the request, record the intent, key and
intended digest in the [task packet](resumption.md); after it, read the effect
back by its returned ID and record that ID and link.

Before publishing, and after a timeout, lost response or resumption, read every
page of the destination for the key. A cached or incomplete read proves
nothing, so the result stays unknown and dependent effects pause.

- One match with the intended content: applied. Record it; do not repeat it.
- No match after a complete read: not applied. Publish once with fresh
  prerequisites.
- Several matches for the same key: the earliest is canonical. Record the
  others as duplicates and link only the canonical one; removing them needs
  authority. Parts of one report have distinct keys, so they are never
  duplicates of each other.
- A match with different content: your own partial post is completed by
  editing that effect, not by posting another; another actor's edit is
  feedback.

An item is this delivery's own effect only when it carries this delivery's
marker, came from the publishing account and matches a recorded intent. It is
not a new request. Treat any other item, including one from the same account
without that match, as feedback under [PR supervision](pr-supervision.md).
Uncertain effects otherwise follow [recovery](recovery.md).
