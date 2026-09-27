# Discover the owning project's delivery policy

Use for an unfamiliar project, conflicting sources or incomplete resumed
records, and at completion for [declared completion steps](#declared-completion-steps)
and [cleanup](#cleanup).
Inspect relevant sources; reuse still-current discoveries. Keep a
concise record in the task or the project's existing tracking location, linking
policy rather than copying it into a new journal or configuration schema.

Establish before each dependent stage:

| Decision | Evidence |
| --- | --- |
| Scope | Source namespace and identity, acceptance criteria, authorized finish line, incoming blockers, outgoing dependents and owner. |
| Repository and target | Source-to-repository mapping, verified remote/host, integration or release branch, target revision and existing work ownership. |
| Planning | Accepted issue/document or required planning method, applicable decisions, artifact identities and readiness/archive rules. |
| Checks and review | Canonical commands, prerequisites, working directories, required CI jobs and protection rules; project requirements in addition to the two independent review axes. |
| Tracking | Supported checkpoint operations and required fields. |
| Completion | Post-merge checks; release, deployment, installation or human acceptance conditions and their owners; any [declared installation or deployment](#declared-completion-steps) procedure, its checkpoint, the project's opt-out rule and any opt-out marking on the item; the project's [cleanup](#cleanup) or retention policy. |

Discover facts before asking. Resolve conflicting scope, target branches,
acceptance requirements or policy with a concrete decision request. Continue
independent authorized work. Do not choose the weaker rule when policy and
hosting configuration disagree.

For routine choices with no policy, use judgment within the requested scope.
Use [work assessment](work-assessment.md) for readiness and verification,
including existing issues without a planning assessment. Preserve unknowns and
refresh stale evidence; ratings do not replace mandatory project requirements.
Use [model selection](model-selection.md) after assessment. Explicit user/project
requirements prevail; missing optional host controls retain defaults with a
disclosed limitation. Report actual runtime settings only when observable.
Do not invent an approval gate from a missing optional control.
An absent optional planning framework does not require setup;
the accepted issue or requirement can supply the plan when policy permits it.

## Declared completion steps

A project declares installation or deployment as a completion condition when
its agent instructions or delivery policy say that a merged change of a named
kind is complete only after that step, and name the procedure that performs
it. Past practice, an issue template or a procedure without the condition is
not a declaration. At pickup, record whether the change falls within the
declaration's scope, where the procedure lives, its checkpoint, the
project's opt-out rule, and any opt-out marking on the item. At completion,
read the procedure from the merged target revision, because it may have
changed, including by this change.

After verified merge and post-merge CI:

- **Declared:** prepare the procedure's complete step, including its
  preflight, stop conditions, recovery and readbacks, and everything the step
  will change beyond this delivery, such as other merged work a shared
  checkout brings. Present it at the checkpoint and wait.
- **Pre-authorized:** authorization in the request must name the step, such
  as "install it after merge"; a finish line such as "through completion"
  does not. It covers only the step for this delivery's own change,
  including the resources that change adds, renames or removes. Present the
  prepared step at the checkpoint anyway when it would also install,
  uninstall or retire other resources, or bring other work's changes that
  need the owner's action, and follow any narrower project rule.
- **Approved, or within the pre-authorization:** run exactly the step
  presented or authorized and nothing else, then read back its evidence and
  record it with the item's delivery evidence. The approval covers only that
  step for this delivery.
- **Declined, or the owner is unavailable:** keep the item open with the step
  pending, its owner and next action recorded; do not apply the completion
  update.
- **Stopped:** when a stop condition holds, such as a target checkout on
  another branch or blocked by local changes, stop and report its owner and
  next action; the item stays open. Never stash, reset, switch branches or run
  the procedure from another location, such as a worktree, to get past it.
- **Interrupted:** the step stays incomplete. Follow the procedure's own
  recovery for owned resources only, preserve others' work, and reconcile an
  ambiguous effect under [recovery](recovery.md) before retrying.
- **Opted out:** when the item uses the project's declared opt-out, or by
  default marks the change source-only with a reason and a link to the
  install issue that batches it, apply the completion update after the other
  conditions pass and name the install issue, or the follow-up the project's
  opt-out names, in the handoff. A marking that does not meet the rule is not
  an opt-out; ask the scope owner and keep the step required meanwhile.
- **Not declared:** offer no procedure, and never improvise an installer,
  copy step or deployment. When the item's acceptance or other project policy
  still requires installation, deployment or a physical check, keep that step
  pending with its owner and next action, retain the waiting state and do not
  apply the completion update. Report a step that nothing requires as a
  follow-up for its owner; it does not keep the item open.

When the change edits this workflow, the running delivery keeps the gates it
started with, and the candidate's text cannot relax them. Its installation
still follows merge and post-merge CI at the checkpoint, as the project's
declaration or the item's acceptance requires; a fresh session then loads the
installed result.

## Cleanup

The project owns cleanup policy: which temporary resources a delivery may
remove, when, and which evidence must survive. Find it at preparation in the
agent instructions, contributing or delivery policy, or the user's
instructions. A habit, a tool default or a remote branch deleted on merge is
not a policy. Record each temporary resource as this delivery creates it:
worktrees, local branches, scratch directories, temporary clones and
publication staging. Only recorded resources are this delivery's; everything
else, including another session's resources, is out of scope, and ownership
you cannot establish is unknown.

Settle each recorded resource at completion, after verified merge and required
post-merge CI. The outcomes are:

- **Removed:** only when all of these hold:
  - the policy allows removing that kind of resource at this stage;
  - this delivery owns it and no other session or owner is using it;
  - evidence the project or the delivery needs, including ignored private
    files inside it, is preserved at a surviving private location outside it;
  - no remaining acceptance, installation or other consumer uses it. A
    pending physical or human acceptance that does not use it does not delay
    its removal;
  - its state matches what the delivery last verified: a branch tip equals the
    head the merge recorded, even when a squash merge keeps the host's
    safe-delete check from seeing it, and a worktree is clean and unlocked.

  Use the host's normal removal, never a forcing flag that overrides a dirty,
  locked or unmerged state. When a tool created the resource and manages its
  exit, such as a host-managed worktree, use that exit. Read back the removal,
  such as the worktree and branch lists or the path's absence.
- **Retained:** any resource failing a condition above, including a moved
  branch tip, a dirty or locked worktree, evidence that cannot be preserved,
  missing post-merge CI, an unavailable tool-managed exit, unknown ownership or
  a missing policy. Record its reason, its owner or `unknown`, and the next
  action.
- **Not applicable:** the delivery created no resource of that kind.

Report each kind separately: branch, worktree, scratch, clone, staging and
remote. A remote branch that disappeared, even by an automatic delete on merge,
proves nothing about local resources. Deleting a remote branch is its own
effect and needs the same policy and ownership checks. A local-only,
ready-PR-only or planning-only request removes nothing beyond its own
authority and reports what it retains.

Record the result in the existing delivery evidence. Keep private paths and
evidence in the private task record; public records, such as the PR or
tracker, name resources by neutral task labels. A removal intent is a pending
effect: on resumption, re-read each resource's state before acting, keep the
recorded outcomes and history, and never assume a removal succeeded. Clean up
only this delivery's resources; an unrelated cleanup needs its own authority.

When OpenSpec applies, resolve pinned tooling, local configuration, active and
archived identities, schemas, templates and completion rules. Existing legacy
work retains its documented path. Required artifact readiness or archive failure
must be resolved before dependent delivery, not reclassified as optional.

For an alternate code host, verify PR-equivalent review/check APIs, pagination,
merge strategies, expected-head guards and destination readbacks. An unavailable
required capability blocks its dependent action; do not change providers or
push directly to the target to circumvent it.

On resumption, inspect the whole candidate and any dirty patch, source links,
base/head, PR disposition, reviews and checks. Require a clear ownership transfer
before taking over another coordinator's work. Reconcile merged or closed PRs
before reopening or replacing them. Never discard existing authorized work to
replay the workflow from the beginning.
