# GitHub issues and code hosting

Read the issue section when GitHub owns scope. Read the PR section when GitHub
hosts the code, including work whose scope lives in Jira or a document.
Use authenticated tools already available; do not change account settings.

## Resolve and update an issue

Accept an issue URL or host/repository-qualified reference. Resolve
`owner/repo#123`, `#123` or a bare number using verified host and repository
context; ask when multiple sources remain plausible. Confirm the object is an
issue, not a pull request, because their numeric namespace is shared. Keep the
issue repository distinct from the repository receiving the implementation.

Read the body, acceptance criteria, relevant scope decisions, issue state and
state reason, linked work and blockers. Use existing project policy to interpret
dependencies rather than treating every mention as a blocker. Follow pagination
where required to obtain authoritative scope and dependency evidence.

Issue open/closed state, labels and GitHub Projects fields are separate tracking
mechanisms. Inspect the project's established convention. If a relevant Projects
field is required, resolve its project, item, field and option IDs. Do not invent
In Progress/In Review statuses, create labels, add board membership or modify
unrelated project fields merely to imitate Jira. With no intermediate tracking
convention, keep the issue open and report progress in the delivery task.

Use a plain issue reference in the PR when completion requires post-merge checks;
automatic closing keywords can close it too early. After verified completion,
close as completed, preserving unrelated labels and fields, then read back state
and reason. A preexisting closed issue needs reconciliation of its disposition
and delivery evidence, not automatic reopening or a false completion claim.

References: [Issue closure](https://docs.github.com/en/issues/tracking-your-work-with-issues/administering-issues/closing-an-issue),
[Projects fields](https://docs.github.com/en/issues/planning-and-tracking-with-projects/understanding-fields/about-single-select-fields).

## Publish, review and merge code

Find an existing PR by verified source, branch, base and ownership before
creation or resumption. Freeze the comparison and inspect all pages of reviews
and review threads, including outstanding change requests and unresolved
conversations. Aggregate review status alone is insufficient evidence.

For post-publication feedback and checks, read [PR supervision](pr-supervision.md).
Use its coordinator-owned loop and retry policy; the operations here adapt that
contract to GitHub.

Read every page of PR issue comments, review submissions, inline review comments
and review threads, including relevant published human and bot feedback. Follow
review associations: inline comments on a `PENDING` review remain unpublished.
Do not mark them processed before submission. Keep unresolved threads visible
even if aggregate review status is clear. Read edited content and new follow-ups;
do not discard an unresolved item solely because it refers to an older head.

Identify items by stable GitHub node ID or resource kind plus database ID, and
their published content/update version. Record dispositions in the existing
packet, deduplicating repeated versions without hiding new edits. A previously
authorized self-authored reply is not another request to reply.

Read workflows at the candidate revision, required branch/ruleset checks and
applicable job results. Include matrix jobs and verify head SHA, event/PR
association, latest applicable run and conclusions. A push run alone is not a
substitute for a required pull-request run. A provider-created test-merge or
merge-queue revision must be verified as covering the candidate and required
target; it does not replace independent review of the candidate's fixed diff.

Inspect each failed job's logs before classification. Read the run's jobs and
individual job logs as soon as they are available, even while other jobs run.
The Actions `actions/jobs/<job-id>/logs` endpoint can provide earlier evidence
than a workflow-wide `gh run view <run-id> --log-failed`; an empty or unavailable
workflow log does not establish that individual logs are unavailable. Preserve
missing logs/annotations as a gap. Check-run conclusions alone do not explain
whether a failure belongs to the branch.

Before an authorized rerun, verify the run's PR/event/head and the affected
logical jobs or matrix entries. Apply the shared retry key and limits, retaining
every run/job attempt in the packet. Use the smallest supported authorized scope,
checking every job the operation would rerun, including any additional jobs,
against authority and applicable limits. A job-specific rerun or
`gh run rerun <run-id> --failed` must not include an exhausted failure just because
another job is eligible. Use provider-returned IDs. A new run/attempt ID
does not reset allowances. Read back the rerun, and reconcile an uncertain
response under [recovery](recovery.md) before another request.

After a push or rerun, refresh PR head/base, published feedback, current required
jobs, review/protection state, mergeability and queue state. A watch command's
snapshot is a discovery aid; verify current authoritative prerequisites before
a consequential write. Reuse only a verified owned watch session. If it stops,
reconcile its owner/state and resume through available reads or watch tools in
the active session. Preserve the shared wait and inactive-monitoring rules.

Code fixes do not grant permission to reply to humans or resolve their threads.
Without existing explicit authority, draft a needed response in the task and
identify the outstanding reply/resolution decision while continuing independent
work. Existing approval for the exact response or scoped resolution persists;
do not ask again. When authorized, verify the current thread/fix, perform the
approved effect once and read it back. Keep any required unresolved thread or
change request as a merge blocker until its accepted disposition is verified.
Never dismiss a review, resolve a thread or alter issue state merely to clear
the merge gate.

Use the allowed merge strategy and GitHub CLI's
`--match-head-commit <reviewed-head>` guard, or an equivalent API precondition.
Never use `--admin`. Honor required queues and target-update protections. If the
branch needs updating, use an authorized non-destructive update and renew the
affected comparison evidence. Queue submission is not completion; wait for and
verify the actual merged result, destination inclusion and required CI.

Keep review/CI evidence in PR discussion or the task, outside the candidate
commit. If changing delivery instructions, independently verify against the
original accepted requirements before using the candidate to finish delivery.

Reference: [GitHub merge command](https://cli.github.com/manual/gh_pr_merge).

Design reference for failure classification and feedback ordering:
[Codex PR Babysitter](https://github.com/openai/codex/blob/a770e5b8470d3320eb53a56a286ea4a0a70a1f59/.codex/skills/babysit-pr/SKILL.md).
This adapter does not invoke that skill or adopt its scripts, permissions,
retry defaults or stopping rules.
