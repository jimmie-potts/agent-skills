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

Read workflows at the candidate revision, required branch/ruleset checks and
applicable job results. Include matrix jobs and verify head SHA, event/PR
association, latest applicable run and conclusions. A push run alone is not a
substitute for a required pull-request run. A provider-created test-merge or
merge-queue revision must be verified as covering the candidate and required
target; it does not replace independent review of the candidate's fixed diff.

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
