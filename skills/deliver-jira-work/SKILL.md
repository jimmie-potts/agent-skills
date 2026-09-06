---
name: deliver-jira-work
description: Deliver one explicitly authorized Jira issue through project-defined planning, implementation, review, merge, and completion checks. Use only when the user explicitly invokes deliver-jira-work for a named issue; do not select for planning, investigation, review-only, or ordinary implementation requests.
---

# Deliver one Jira issue

An explicit invocation with one issue requests delivery through implementation,
one ready pull request, normal merge, and Jira completion, subject to the user's
limits and the owning project's policy. Treat "pull request" as the hosting
provider's equivalent change-review object throughout this workflow. A
ready-PR-only request ends at the ready PR and its required handoff evidence.
A planning-only invocation authorizes no delivery effects.

## Keep authority with the coordinator

The coordinating root owns repository writes, Git and worktree changes, Jira
transitions, PR publication, merge, and authoritative readbacks for the named
issue. Workers return proposed patches, reviews, or evidence without performing
durable effects. Map dependencies and write ownership before delegating.

The skill grants no authority beyond the user's request. Do not change sprint
membership or lifecycle, deliver linked issues, deploy, install, message others,
or perform unrelated cleanup without authority for that action. Preserve host
sandbox and approval rules. Never bypass branch protections, force-push, or
destroy another owner's work to complete delivery.

Keep these rules active throughout the workflow:

- Resolve material scope or policy conflicts before dependent work. Continue
  independent authorized work while requesting the concrete missing decision.
  Existing authorization covers routine in-scope repairs; do not invent another
  approval gate merely because a repair is needed.
- Record each consequential effect's intent, object, expected prior state, and
  revision or transition guard before issuing it. Read back the authoritative
  result and retain its identifier. Reconcile an uncertain effect before any
  recovery attempt; never blindly retry it.
- Failed, missing, stale, or unresolved evidence blocks the step that needs it.
  A task checkbox, local success, or merge alone does not prove completion.
- Use existing tools and repository checks directly. Do not add a delivery
  runtime script, mandate a hosting provider, or bootstrap a specification
  framework to make this workflow fit a project.

## Discover the delivery contract

1. Read the named issue from authoritative Jira, including project, issue type,
   scope, acceptance criteria, status, dependency directions, and sprint. Do
   not infer the issue from recency or branch names. Resolve incoming blockers
   and verify ambiguous links from both endpoints. Record outgoing dependencies
   without taking ownership of them.
2. Identify the owning repository from issue and project sources, then verify
   its remote identity, hosting provider, actual target branch, and current
   target revision. The Jira project need not own the repository in the current
   directory. Read applicable agent instructions, development policy, accepted
   decisions, affected contracts, code, tests, and CI configuration.
3. Establish the specification/planning method, risk classification, model and
   reasoning settings, required local checks, independent review requirements,
   hosted checks, merge strategy, and completion conditions from project policy.
   Discover available Jira transitions and required fields, then map delivery
   checkpoints to their meanings. Never assume status names or treat a status
   category as completion evidence.
4. For an unfamiliar project, changed policy, conflicting sources, or a resumed
   delivery with incomplete records, read [project discovery](references/project-discovery.md).
   Record the discovered sources and decisions before implementation. Missing
   policy requires a concrete decision request before the work it governs;
   distinguish an explicit "not required" from an unknown requirement.
5. Inspect existing branches, worktrees, PRs, and planning artifacts for this
   issue. Reuse verified, authorized existing work without duplicating its PR.
   If another coordinator owns it or identity is ambiguous, resolve ownership
   first. Leave dirty or stale shared checkouts untouched. Create an isolated
   branch/worktree or owned checkout from the freshly verified target; preserve
   existing authorized changes when resuming. Record base SHA and worktree state.

## Plan and implement

1. Prepare the repository-required plan before coding, with acceptance evidence,
   dependency-ordered tasks, affected files, validation commands, and risk and
   model decisions. Follow accepted architecture decisions; request unresolved
   material decisions before dependent implementation.
2. Use OpenSpec only when the project requires it. Discover its pinned tooling,
   change identity, configuration, templates, readiness gates, synchronization,
   and archive rules. Check identity collisions and use the correct active or
   legacy path. Otherwise follow the project's own specification or planning
   method and record that adaptation. Add no OpenSpec infrastructure by default.
3. Immediately before implementation, recheck issue scope and dependencies.
   Apply the discovered transition for starting work when appropriate, using
   its live ID and required fields; read Jira back. Do not move a resumed issue
   backward merely to replay this sequence.
4. Implement only the authorized tasks. Add the narrowest meaningful acceptance
   checks, including behavioral scenarios for instruction changes. Mark tasks
   complete only when their evidence exists. Resolve ordinary recoverable
   failures within scope, then rerun the affected checks.
5. Run all canonical checks with their documented prerequisites and working
   directories. Record commands, results, revision, omissions, and limitations.
   Complete required specification updates or archival before final review when
   policy requires them; a failed readiness or archive check is not permission
   to skip it. Reassess risk and required model/reviewer settings after design
   changes and before final review.

## Publish and establish merge eligibility

1. Commit the complete candidate and open or update one ready PR when authorized.
   Explain the problem, resulting behavior, issue/specification links, project
   adaptation, acceptance evidence, risk, checks, and remaining completion work.
   Avoid automatic issue-closing actions when post-merge evidence is required.
   Transition Jira to the discovered review checkpoint only after the ready PR
   exists, then read it back.
2. Freeze base SHA, head SHA, merge-base, diff command, and clean worktree state.
   Obtain fresh independent read-only review of that comparison. Follow project
   rules for roles, risk, model settings, and review strength. Provide reviewers
   the raw issue, specifications, policies, and diff. A self-review or unavailable
   independent review cannot enable merge. Store revision-dependent evidence
   outside the commit it describes.
3. Resolve every blocking finding and record other dispositions. A disputed
   finding needs evidence and reviewer reassessment. Read all pages of provider
   reviews, change requests, and discussion threads; address unresolved blockers
   through fixes or an accepted disposition.
4. Enumerate required hosted jobs from current project CI, including matrix
   expansions and protection rules. Require successful applicable results for
   this PR's exact current head. Missing, pending, failed, skipped, or cancelled
   required checks block merge. An empty protection rule does not replace
   repository checks or independent review.
5. A new commit, changed target, conflict resolution, or scope change invalidates
   affected validation and review. Refresh the candidate as policy requires and
   reacquire affected local checks, independent review, and exact-head CI. Do not
   carry an old approval onto a changed comparison without reassessment.
6. For a ready-PR-only limit, report the ready PR, current evidence, Jira state,
   and remaining gates; do not merge or declare the issue complete. If policy
   requires evidence outside the authorized limit, report that boundary.

## Merge and verify completion

1. Immediately before merge, refresh authoritative issue scope, blockers, target
   revision, PR head, reviews, checks, and protections. Require the candidate to
   include the current target. If it does not, refresh within the authorized
   branch, resolve conflicts, and renew the affected gates before retrying this
   eligibility check.
2. Use the provider's normal allowed merge operation with an expected-head guard
   or equivalent atomic precondition. Honor target-update protections or the
   provider's merge queue where required. If available tools cannot protect the
   reviewed head, report the missing capability before merging. Never bypass a
   gate or replace normal merge with a direct target-branch write.
3. Read back the PR's merged state and merge revision, the destination branch,
   resulting tree and required artifacts, and required post-merge CI. Verify the
   published revision is included in the actual target, accounting for the
   allowed merge strategy. If a readback fails or disagrees, retain the evidence
   and reconcile before further effects.
4. Evaluate every project completion condition. If deployment, installation,
   physical verification, or human acceptance remains, retain the appropriate
   Jira state and report the checkpoint and owner. Perform such work only when
   it is authorized; merge does not grant that authority.
5. Only after all completion conditions pass, obtain current Jira transitions,
   apply the appropriate completion transition and required fields, and read
   back status and resolution as applicable. Preserve sprint state and linked
   issues. Report the immutable published revision and acceptance evidence.

## Recover from failures

For a definite failure with no effect, diagnose and repair within existing
authority, then retry the failed step with fresh prerequisites. For a timeout,
disconnect, ambiguous response, or partial effect, suspend dependent mutations.
Inspect authoritative issue history, PRs, refs, jobs, or installed state using
the recorded intent and identifiers. Classify the effect as applied, not applied,
partial, or still unknown. A delayed or stale read alone does not prove absence.

If applied, continue from verified state without repeating the effect. If
verified not applied, retry only within existing authority and project recovery
policy, with fresh guards. Reconcile a partial effect before proposing the
remaining action. If unknown or recovery exceeds scope, request the specific
decision needed and continue independent authorized work. Do not create a
duplicate PR, transition, comment, or merge to test whether the first succeeded.

## Report a checkpoint

At substantive checkpoints, pauses, blockers, and handoff, report issue key,
stage, specification identity or "not applicable" with reason, branch, PR or
"not opened", last verified SHA, risk and uncertainty, next checkpoint, and
blocker or "none". Separate requested model settings, resolved configuration,
and observed runtime evidence; report unavailable fields honestly.

Report source changes, local checks, hosted CI, independent review, merge,
installation/deployment, and human acceptance separately when applicable.
Monitoring another coordinator's work is read-only.

When evaluating or revising this skill, read the synthetic
[validation scenarios](references/validation-scenarios.md). Keep static contract
tests, simulated agent decisions, and actual fresh-host discovery distinct.
