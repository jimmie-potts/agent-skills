# Section procedure

Read at the start of every sweep. This file is the only home of each step's
rules. `SKILL.md` holds the authority boundary and the local-branch guards;
nothing here relaxes them.

## Resolve the task

Build the task's inventory from the conversation, the delivery record and live
reads: owning repositories, issues delivered, planned or edited, PRs,
branches, worktrees, temporary resources and the session label if the
coordinator set one.

Discover each owning repository's conventions through the host, the way
`plan-work`'s GitHub reference does. Resolve the owner and repository from
authorized sources, read its agent instructions and contributing policy, and
read its issue forms, its wording for backlog placeholders, its Guide fields
and the established meanings of its labels. When a convention is absent, use
a plain issue and report the absence; never borrow another project's template.

Guide fields are the idea-marker fields that a repository's issue form
declares, for example a `## Guide` section with `**Topic:**`,
`**Highlight:**` and `**Extends:**`. Apply them only where the form declares
them.

## Pass the pre-write gate

1. Finish or poll every CI run and background task this task started. Do not
   rerun an unchanged successful test without a reason.
2. Re-read live state: each touched issue (open or closed, labels, closing
   references), PR (state, head, merge revision, checks), branch (tip,
   upstream, worktree attachment) and this task's worktrees (worktree
   attachment and dirty state). Report from these reads, never from
   recollection.
3. Check relevant recent work for actual conflicts or dependencies: issues and
   PRs by other sessions that touch the same files, stories or data. Avoid a
   repository-wide activity inventory.
4. Distinguish source completion, publication, installation, client
   verification and physical acceptance. Missing evidence means unknown.
5. When something cannot finish now, name it, what it gates and how to
   recheck it. The verdict is then provisional: a pending item is a Loose End,
   and only a rerun after it settles can reach `Safe to archive`.

## Capture

For each follow-up, search open and closed issues in the owning repository
first. Then apply exactly one of these rules and report the item as filed,
commented or already covered:

- Covered: add new evidence to the existing issue as a comment, or report it
  as already covered when there is nothing new. Never file a duplicate.
- Uncovered P1 or P2: file it in the owning repository with its issue form and
  required fields, its wording for backlog placeholders when the item is not
  yet defined, and its Guide fields. Link the delivered issue and read the new
  issue back.
- Uncovered P3: list it in the closing comment.
- Another session's active issue: never comment on or edit it. Record in this
  task's handoff what its owner should add.

Use the project's priority definitions. If a filing times out, reconcile by
reading before retrying; unindexed search is not proof that the first attempt
failed.

Decisions: record only decisions not already in a PR body, ADR, design record
or issue comment, with the alternatives rejected, in the closing comment. For
recorded ones, link where they live.

Learnings: save host-useful gotchas as memory notes through the host's
supported mechanism and read each back. For a change to agent instructions or
documentation, open a docs-only PR or put the proposed change and its target
file in the closing comment. Report what was written, not what is worth
adding. When memory cannot be written, including when the host only generates
memories in the background, apply the memory fallback in `SKILL.md`'s
authority boundary and give the reason. Private information that has no
private durable location is unpreserved work: report it as a Loose End.

## Clean up

Preserve needed evidence outside disposable worktrees before removing
anything. Remove only temporary files this task created and nothing else uses.
Leave uncertain, shared or actively used resources untouched.

For each local branch this task created, apply every guard in `SKILL.md`. On a
GitHub-hosted Git repository, the checks can read:

- `git worktree list --porcelain`: any worktree on the branch retains it;
- the merged PR's state, target, merge commit, head SHA and required checks
  from the code host, the required post-merge CI result on the target where
  the project requires one, and
  `git merge-base --is-ancestor <merge commit> <remote target>`;
- `git rev-parse refs/heads/<branch>`, which must equal the PR's head SHA.

Delete with `git update-ref -d refs/heads/<branch> <verified tip>`, which
refuses when the tip moved, then confirm that
`git rev-parse --verify --quiet refs/heads/<branch>` finds nothing. Retain the
branch when any read fails, disagrees or is still pending.

Never remove or detach a worktree and never delete a remote branch; report
each with its owner and the reason it remains.

## Post the closing comment

Draft the closing comment from [the closeout record](closeout-record.md) and
post it on the owning issue: the delivered issue, or for a planning session
the issue it planned. Another owning issue gets its own comment only when it
needs its own resume prompt. Read each comment back. Without any owning issue,
put the record in the reply and create no issue just to hold it. On a rerun,
follow [Reruns](#reruns) instead of repeating the earlier comment.

## Report

Report in this exact order. Target 250-350 words for a routine sweep; exceed
that only when material findings need explanation. Link detailed evidence,
avoid repetition, and keep supporting information near the top and
decision-relevant information near the bottom. Write "None" for an empty
section rather than padding it.

### 1. Recorded

Compact links for issues, comments, decisions, memory notes and doc PRs
written during this sweep, and the capture receipt that
[the closeout record](closeout-record.md) defines. Omit empty categories. Put
unresolved tracked work in Tracked Follow-ups instead of explaining it twice.

### 2. Verification

Summarize passed checks, material limits and actual cross-session conflicts.
Link the delivery's execution record rather than repeating it.

### 3. Installation

Give each installation, publication or registration one status: completed and
verified (with its readback), required and previously authorized but omitted,
available but outside authorized scope, blocked (with its blocker and owner),
unnecessary, or unknown. This sweep never installs, and reporting a status
grants no installation authority.

An installation that the project declares as a completion condition, and that
the owner deferred or has not yet approved, is available but outside
authorized scope or blocked on the owner's decision, and it is a required
Tracked Follow-up. It becomes a Loose End only when it was required and
previously authorized and then omitted. Separate future work goes in Tracked
Follow-ups.

### 4. Cleanup

Name each local branch deleted or retained and why. Summarize worktrees
retained, temporary resources removed, evidence preserved, and any remaining
uncommitted, unpushed or unmerged work. Report remote-branch cleanup needs
without acting on them.

A resource retained because it is uncertain, shared, actively used or another
owner's is intentionally retained: report it here, not as a Loose End, unless
it holds this task's own unpreserved work or evidence. Incomplete required
cleanup and unpreserved work are Loose Ends.

### 5. Ideas

For planning and delivery sweeps alike, suggest up to three worthwhile
possibilities inspired by this task and the project context already at hand:
something deliberately left out, a capability this work makes possible, an
unexpected connection, or a different approach. Go beyond the obvious next
implementation step. Give each a short name, a concrete description, why it
could be useful, and the smallest experiment that would show whether it is
worth pursuing. Distinguish speculation from established fact and name known
related backlog coverage. Do not force three or investigate broadly to fill
the section; write "None worth adding" when appropriate. Ideas are not
commitments or archival blockers: never file or implement one unless the
owner separately asks.

### 6. Tracked Follow-ups

List unresolved work already captured in issues that the owner may pick up
next, including installation, verification and coordination follow-ups. Give
each its priority, a short description, the next action and the tracking link,
and mark it required or optional. Include only items relevant to this task.
Tracking does not resolve an item: one that must be addressed before archival
belongs in Loose Ends.

### 7. Loose Ends

List only unresolved problems to address before archiving this task:
something wrong or misconfigured, incomplete required cleanup, unpreserved
work or evidence, missing tracking, a pending item from the pre-write gate, or
an unfinished obligation within the task's agreed scope. For each, state what
is wrong, what must happen before archival, and who must act or authorize it.
Filing an issue does not remove an archival blocker from this section. Do not
repeat tracked follow-ups, ideas or intentionally retained resources, and add
no general reassurance.

### 8. TL;DR

At the very bottom, in two sentences at most: what was completed and whether
the owner must act before archiving. When Loose Ends is "None", end with
`Safe to archive.`; otherwise end with `Needs attention: <main archival
blocker>.` Safe to archive means the work and evidence are preserved and
remaining follow-ups are durably tracked, not that every follow-up is
finished. Whether a failed memory save blocks archival follows the memory
fallback in `SKILL.md`.

## Planning sessions

Use the same report order for planning sessions. Mark Installation and
Cleanup briefly as not applicable where appropriate, report any temporary
resources the session did create, and still consider Ideas.

## Reruns

Re-read the earlier record and live state, then add only new information.
Leave the earlier record as it is.

- Unchanged: when the sweep finds no new information, post nothing. Report
  the same eight sections briefly, say that no new information was found,
  link the earlier record, and count this sweep's writes as zero, separately
  from the earlier sweep's.
- Changed: post a second closeout record in the rerun shape that
  [the closeout record](closeout-record.md#reruns) defines. Recorded lists
  this sweep's writes separately from earlier work.
