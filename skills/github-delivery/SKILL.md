---
name: github-delivery
description: Coordinate authorized implementation in a GitHub repository through its requested delivery target, using repository-defined planning, tests, independent review, and current CI. Use for implementation or delivery requests; exclude planning-only, investigation-only, and review-only requests.
---

# GitHub delivery

Read the consuming repository's agent instructions and development guide before
acting. They define the scope owner, planning method, validation commands,
branching, status conventions, and delivery target. This skill grants no new
authority to edit, publish, merge, install, or deploy. Respect a user request to
stop at local edits or a ready PR. Where the request authorizes delivery through
merge, continue through those steps without repeated confirmation.

## Prepare the deliverable

1. Read the authoritative issue or other approved scope source. Resolve material
   decisions, observable acceptance criteria, dependencies, and the requested
   terminal state. Reuse existing tracking rather than creating duplicate work.
2. Investigate discoverable facts before asking questions. For unsettled design
   choices, explicitly compose the shared `grill-with-docs` workflow. Its
   questioning remains read-only; after it returns decisions, continue only the
   work already authorized by the underlying request.
3. Inspect existing worktrees and refresh the repository-defined base. Isolate
   the deliverable and preserve unrelated work. Assign independent work only
   after mapping dependencies and write ownership. Reviewers do not edit the
   candidate. Follow repository labels and issue conventions without importing
   another project's tracker policy.
4. Determine the required planning from repository policy. If OpenSpec applies,
   use its shared skills with the repository's pinned CLI. Resolve the exact
   scope-linked change and planning root; never substitute an unrelated change
   because it is the only one. Existing implementation authority survives a
   planning substep. Missing required decisions still block dependent work.

## Implement and prepare review

Use the shared `tdd` workflow for meaningful executable behavior when this
delivery calls for it. Follow one observable scenario through red, green, and
refactor before starting the next. Documentation and cosmetic changes need
appropriate inspection, without invented regression tests.

Run the repository's canonical checks. Record actual commands, failures,
results, and limitations. If scope changes, reconcile the issue, plan, and
tests before proceeding. A checked task box is not acceptance evidence.

For specification work, verify all required artifacts and their dependencies,
including any legitimate conditional omission. Resolve current CLI inputs
successfully before synchronization or archival. Complete the affected spec
set and archive according to repository policy before final review when the
policy requires it. Do not treat failed lookups or unfinished tasks as success.

Commit the complete candidate when publication is authorized. Open or update
its PR with scope/specification links and validation evidence. Avoid automatic
issue-closing keywords when completion requires post-merge verification. Record
the immutable base, head, merge-base, diff command, and worktree state. Keep
revision-dependent evidence in the PR, outside the commit it describes.

## Establish merge eligibility

For agent-driven merging, obtain independent read-only Standards and
Specification reviews of the same fixed comparison. Use the shared `code-review`
method and repository-defined sources. Give each reviewer its own rubric and
raw inputs. Self-review or unavailable independent review cannot enable an
automatic merge.

Fix P0-P2 defects. Record P3 dispositions. A disputed finding needs evidence and
reviewer reassessment before dismissal. After candidate changes, renew affected
review and test evidence. Read every page of GitHub reviews and review threads.
Resolve outstanding change requests and unresolved threads after fixes or
agreed disposition; do not dismiss them merely to enable merge.

Inspect workflow configuration at the candidate revision to enumerate every
required job, including matrix expansions. Require success on the latest
applicable PR run for the current head, with the correct PR association. Read
every result page. Missing, pending, skipped, cancelled, or failed required jobs
block merge. An empty required-check list on an unprotected branch proves
nothing. Honor additional branch protections without bypasses.

Immediately recheck scope, dependencies, PR head, and current base. Changes
invalidate affected evidence. Merge only within the user's authorized target,
using the repository's allowed method and GitHub CLI's
`--match-head-commit <reviewed-head>` guard. Never use `--admin`. Do not introduce
a background merge service or change repository privacy or account settings.

## Verify the result

Read back the merged revision on the destination branch and its required CI.
Keep tracking open when post-merge checks fail or required deployment work
remains. Close and clean workflow labels only according to repository policy,
then verify the resulting state. Preserve other worktrees and their owners.

Report source, local checks, hosted-platform checks, installation/deployment,
and physical verification separately where relevant. A source-only request does
not invoke an installer or contact a device. Apply the shared `unslop` skill to
narrative documentation and the final handoff.
