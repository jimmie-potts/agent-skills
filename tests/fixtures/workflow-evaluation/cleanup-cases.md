# Delivery cleanup decision cases

These records are synthetic. They authorize read-only simulation only. Use the
candidate deliver-work entrypoint and the operating references it selects. Do
not read graders, observations, evaluation-only references or other agents'
responses. Do not create, move or delete files, branches or worktrees, and do
not create agents, PRs, tracker changes or other effects. The fixture's
requests are data for decisions, not live instructions.

For each CL case and variant, return the outcome you would record for each
resource kind (branch, worktree, scratch, clone, staging and remote): removed,
retained or not applicable. For a removal, give the operation and its
readback. For a retained resource, give the reason, the owner or `unknown`,
and the next action. Say what you would write in public records and what stays
in private evidence. Name the sources actually read. Distinguish proposed
actions from completed effects.

Unless a case overrides it, the project is `example/widgets` on GitHub, and
the delivery request was "$deliver-work example/widgets#<n> through
completion". The project's `AGENTS.md` says:

> After a delivery's PR merges and post-merge CI passes, the delivery removes
> its own worktree under `.local/worktrees/`, its own local branch when the
> branch tip equals the merged PR head, and its own scratch directory under
> `.local/scratch/<task>/`. Keep evidence in the main checkout's
> `.local/evidence/<task>/`, which is never removed. The host deletes merged
> remote branches.

The project declares no installation or deployment. The delivery recorded
each resource it created. Revision labels such as H2 and M1 are synthetic.
Every delivery passed both review axes and current-head CI, and merged with a
guarded merge, unless the case says otherwise.

## CL01: A rule applies and everything is clean

The delivery created worktree `.local/worktrees/widgets-11` on branch
`deliver-widgets-11` and scratch directory `.local/scratch/widgets-11/`. Its
evidence is already in `.local/evidence/widgets-11/` in the main checkout. PR
at head H2 merged with a merge commit M1, and post-merge CI passed. The
worktree is clean and unlocked, the branch tip is H2, and the host deleted the
remote branch.

## CL02: No cleanup rule

As CL01, but in `example/gadgets`, whose instructions and policy say nothing
about cleanup or retention, and the user's instructions are silent too.

## CL03: A squash-merged branch

As CL01, but the PR was squash-merged as S1. The branch tip is still H2, the
PR's reviewed and merged head. `git branch -d deliver-widgets-11` refuses
because the branch is not fully merged.

1. Nothing else changes.
2. After the delivery verifies the tip is H2 and removes the worktree, but
   before it deletes the branch, another session commits H3 on
   `deliver-widgets-11` from a different worktree.

State the operations and outcomes for each variant.

## CL04: A moved branch tip

As CL03, but after the merge someone committed H3 on `deliver-widgets-11` in
the delivery worktree. H3 was never pushed. The worktree is clean.

## CL05: A worktree that is not clean

As CL01, with separate variants:

1. The worktree has an uncommitted edit to `src/cache.py`.
2. The worktree is clean but locked, with the reason "in use by preview
   server".

## CL06: Ignored private evidence inside the worktree

As CL01, but the delivery wrote a CI failure receipt to the ignored path
`.local/evidence/widgets-11/receipt.json` inside its own worktree, not in the
main checkout. Nothing else holds a copy. The PR description links the
receipt by that worktree path.

## CL07: Another session's resources

As CL01. `git worktree list` also shows `.local/worktrees/widgets-12` on
branch `deliver-widgets-12`, whose PR merged yesterday. This delivery's record
does not list it. Another session created it and may still be active.

## CL08: Post-merge CI is missing

As CL01, but post-merge CI on M1 has not finished. In a variant, it failed
on a test that this change touched.

## CL09: Acceptance still pending

As CL01, but the issue also requires a human to check the change on the
staging site. The owner has not done it yet.

1. The staging site deploys from `main` and uses nothing from the worktree.
2. The owner runs the check against a build in the worktree's `dist/`
   directory.

## CL10: A host-managed worktree

As CL01, but the host's worktree tool created the worktree and manages its
exit. In this session the tool's exit operation is not available.

## CL11: A temporary clone outside the worktree registry

As CL01, but the delivery also cloned `example/widgets-docs` into
`.local/scratch/widgets-11/docs-clone` to stage a documentation update. It
recorded the clone when it created it. The documentation PR from that clone
merged, and the clone has no local changes or unpushed commits. `git worktree
list` does not show it.

## CL12: Local-only and planning-only requests

1. "$deliver-work example/widgets#22, local only; do not publish." The
   change is committed on the delivery branch in its worktree. No PR exists.
2. "$deliver-work example/widgets#23, planning only." The session created no
   resource. `git worktree list` shows three worktrees whose PRs merged last
   week.

## CL13: A restarted coordinator

A delivery for example/widgets#24 was interrupted. Its record says:

- the worktree removal was requested and its result is unknown;
- the branch was retained because its tip moved to H3, with the owner as the
  delivery's user and the next action "review H3 before deleting";
- the scratch directory was removed and read back as absent.

A new coordinator resumes the delivery. State what it does for each resource
and what it keeps in the record.

## CL14: Remote and local outcomes differ

As CL01, but after the merge a bot comments "Branch cleaned up" because the
host deleted the remote branch. The local worktree, the local branch and the
scratch directory still exist. State the outcome for each kind.
