# Supervise a published change

Read after publishing or resuming a change review when the requested finish
line includes feedback, hosted checks, guarded merge or explicit ongoing
watching. This is the provider-neutral loop; use the code-host adapter for
operations. Local-only work stops before publication and this loop. A
ready-PR-only limit requires only the evidence for that boundary.

## Keep one owner and one record

The delivery coordinator owns supervision and all authorized writes. Reconcile
the existing [task packet](resumption.md) before entering or resuming the loop.
Keep these facts in that same record:

- change identity, requested finish line, current base/head and last refresh;
- required checks, reviews, protections, mergeability and queue state, with the
  comparison and provider run/event covered by each result;
- each feedback item's stable identity, published version, disposition,
  affected revision and supporting evidence;
- each retry key, allowance, attempts, outcome and provider identifiers;
- watcher or polling owner, session state, last observation and unknown history.

Read all pages and required sources before declaring feedback clear. Pending,
draft or otherwise unpublished reviews and their comments must remain eligible
for later publication; do not act on them or mark them processed. Deduplicate
repeated appearances of the same published item/version. Reassess edits and new
follow-ups. Older-head feedback can still apply to the current candidate.
Record a disposition with evidence rather than treating retrieval as handling.
Fixing code, replying and resolving a provider thread are separate actions.

## Refresh and act in evidence order

At every loop entry, refresh scope, authority, finish line and open/closed state;
target/base/head and comparison; published feedback and unresolved conversations;
required jobs from candidate configuration and protections; required reviews,
mergeability and queue state. Verify check run/event/change/head association.
Missing pages, logs, policy or capabilities remain evidence gaps, not success.

Process that refreshed state in this order:

1. Reconcile merged or closed state before taking another action.
2. Handle published actionable feedback against current scope and code. Repair
   correct in-scope defects; record disputed or out-of-scope items and the
   evidence/decision needed. Keep unresolved blockers visible.
3. Diagnose failed required checks from their logs and changed-code evidence.
4. Wait for required pending checks/reviews with responsive bounded waits.
5. Evaluate the user's finish line and hand off or stop as described below.

When feedback requires a commit, apply and validate the authorized fix, commit
and push through the existing workflow before retrying checks that the new
revision will supersede. Then immediately re-enter supervision for the actual
resulting head. A push does not finish supervision.

## Classify failures before retrying

| Classification | Evidence and action |
| --- | --- |
| Branch-related | Logs connect the failure to the candidate's changed behavior or affected tests. Repair within scope and obtain fresh validation. |
| Infrastructure or likely flake | Logs support a runner, provider, network, registry or unrelated intermittent failure. Preserve its evidence; do not change product code, tests, dependencies or CI merely to obtain green. |
| Unresolved | Logs are missing, contradictory or insufficient. Make a bounded diagnosis, retain the gap and obtain the missing evidence before choosing a fix or rerun. |

Use a rerun only when evidence supports a transient failure, another attempt
can plausibly help, no impending fix supersedes it, and authority/budget permit
the operation. An active outage or persistent access/billing failure needs its
external resolution, not repeated attempts. Continue independent authorized work.

Honor all user/project retry limits, including any aggregate cap. If none exists,
allow at most one evidence-supported rerun per candidate head, logical check
including matrix entry, and diagnosed failure signature. This is a finite
fallback, not a reason to rerun. Keep run/job IDs as attempt evidence, not as
new allowance keys. Preserve used counts and unknown outcomes on resumption;
do not infer zero from missing history, duplicate an in-flight attempt, change
a key merely by renaming the diagnosis, or manufacture a SHA to evade a limit.
A genuine scoped fix requires checks on the new head while all prior history
remains recorded. An exhausted allowance is a blocker until an authorized
resolution or new supporting evidence changes the next action.
New evidence may support a different action; it does not replenish the used
allowance for that failure/head.

Record rerun intent and read back its result. Reconcile uncertain effects under
[recovery](recovery.md) before repeating them. After every authorized rerun,
immediately re-enter supervision. New feedback, changed code/scope/base/head or
check state requires reassessment and renewal of affected evidence. Cancelled,
missing, skipped or stale required checks do not satisfy the current-head gate.

## Wait and stop at the requested boundary

Keep one watcher or polling owner for the change. Verify an earlier owner's
state and transfer before taking over; do not create another watcher to recover
an unknown one. Prefer supported read/watch tools. No executable watcher,
service, automation, installation or new file is required by this protocol.

Use waits bounded by the host's responsiveness rules, never a blocking wait
longer than 60 seconds. Report meaningful changes and any host-required progress
update without replaying full unchanged snapshots. A stopped process or inactive
session is not monitoring. If a watch process ends, reconcile ownership and
resume with supported reads/watch tools while the authorized session is active.
If it cannot continue, record supervision as inactive and the next action;
never claim a detached process or ended turn continues watching.

| Requested boundary or observed state | Next action |
| --- | --- |
| Full delivery, all applicable requirements satisfied | Hand off immediately to the entrypoint's guarded-merge stage. Refresh prerequisites immediately before merging; do not wait indefinitely for hypothetical feedback or ask again for existing authority. |
| Queue entry or accepted merge request without verified merge | Keep the operation pending and supervise/reconcile its outcome. Do not enqueue or merge again to probe state. |
| Verified merge | Stop polling the open-PR phase and continue the entrypoint's merge readbacks, post-merge CI and completion conditions. Failed required post-merge CI keeps delivery incomplete. |
| Ready-PR-only | Stop when the ready PR and its required current evidence are verified. Report merge and later gates as outside this finish line. |
| Local-only | Stop with required local evidence; do not publish or start PR supervision. |
| Explicit ongoing watch | Continue under that watch's stated authority and stopping conditions, including while green if requested. Watching alone never authorizes merge. |
| Closed without merge | Stop polling that closed PR, reconcile its disposition and report incomplete or changed delivery. Do not reopen, replace it or close the issue without authority. |
| Required capability or decision unavailable | Report the specific gap, owner and evidence needed. Pause dependent actions and continue independent authorized work; hand off if no useful action or responsive wait remains. |
| User stop | Stop and verify any owned watch process, preserve evidence and relinquish its active ownership. Report monitoring inactive; do not claim completion that was not verified. |

Supervision grants no new permission. Preserve restrictions on replies, thread
resolution, issue state, pushes, merge and deployment. Never bypass protections,
force-push or weaken a check to enable delivery.
