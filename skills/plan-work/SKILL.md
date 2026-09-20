---
name: plan-work
description: Define one or more implementation-ready work items using the repository's requirements and tracker conventions. Use only when the user explicitly invokes plan-work; ordinary planning questions do not select it.
---

# Define work before delivery

Turn an outcome into scoped work with acceptance evidence and dependencies.
An explicit request to define and publish work authorizes scoped tracker
creation/update after requirements are settled. Planning-only returns proposals.
Invoking this skill alone does not authorize publication. Neither mode starts
implementation, delivery agents, sprint lifecycle changes, deployment, or
installation. Preserve narrower user limits and applicable project policy.

## Ground the outcome

Identify the requested outcome, owning repository, tracker namespace, and
publication boundary. Read applicable instructions, planning conventions,
implementation, tests, contracts, and authoritative specifications. Discover
facts before asking. Distinguish delivered behavior from proposed additions.
Identify any project-owned guides, roadmap, architecture inputs, and publication
procedure, including their coordinator and repository. Do not invent a
documentation system when none is defined.
Search existing work, including completed or active implementation, before
proposing new items; preserve others' ownership and intervening changes.

For GitHub work, read [GitHub planning](references/github.md). For Jira, read
[Jira planning](references/jira.md). For document-only work use the named source
and return proposals unless exact document edits are authorized. Do not create
a tracker, planning framework, board, or custom fields to fit this workflow.

Discover the installed canonical deliver-work skill through supported host
discovery and read its `references/work-assessment.md` and
`references/task-planning.md`. These are required resource dependencies, not an
invocation of delivery. Use the task-planning definition, boundary and dependency
sections to propose work; they grant no implementation dispatch authority.
Do not guess personal paths or duplicate either contract here. If a resource is
absent or unreadable, report the gap before its dependent planning step and
continue independent discovery. Never silently install or reconstruct it.

When project documentation or publication policy applies, read the same
discovered package's `references/documentation.md` for its planning checkpoint.
Keep project paths and commands in that policy. An unavailable required resource
leaves its dependent synchronization pending; continue independent planning.

When the user or project sets review-round, time or spending limits, read the
discovered package's `references/review-cycles.md` section on explicit limits.
Carry the limit's scope, proposed observable accounting and stop/handoff evidence
into acceptance and delivery requirements. Distinguish review rounds from worker
retry budgets. Keep unknown accounting visible; do not invent a default allowance.
This records future delivery constraints without starting delivery or agents.

## Settle decisions and define items

For material unresolved decisions, compose grill-with-docs using the available
canonical skill. Its questioning phase is read-only. Reuse accepted decisions
and existing authority; after questioning, return control here for authorized
planning operations. A missing required skill blocks that substep, not unrelated
discovery. Do not silently fetch, copy, or replace it.

Define one item or decompose a larger outcome using the shared task-planning
meanings. Carry outcomes, exclusions, acceptance/verification coverage and true
input dependencies into each proposed work item. An epic or list of chores
alone is not implementation-ready. Include the assessment, evidence, unknowns,
readiness and conditional specialist/human review or operational handoffs.

Apply the assessment contract without embedding model names in planning ratings.
Record the session's reasoning setting in the planning evidence when the host
exposes it or the user states it; otherwise record it as unknown. Report a
known mismatch with documented workflow guidance or a composed skill's
reasoning requirement, such as a pairing worker that would inherit a reduced
level, and never claim to change it. Keep planned commands and
paths explicitly unexecuted.

Before selecting workers for bounded investigation, discover the installed
canonical deliver-work package as above and read its
`references/model-selection.md`, its implementation-selection branch, and only
the selected host's worker adapter. Read `references/worker-briefs.md` before
dispatch and supply the selected role, criteria, relevant instructions, read-only
authority and return contract. Do not load reviewer, delivery-reporting or
unselected pairing rules for an assigned investigation. This reads selection
policy without invoking delivery or authorizing implementation. Keep assessment
ratings model-neutral. If that resource is unavailable, report the dependent
selection gap; continue the planner's own authorized read-only discovery.
Use a bounded investigation when it can resolve technical uncertainty; a
missing product decision remains a question. A bounded investigation may compose the host's advisory pairing in planning-only
mode, selected from verified host tooling: worker-with-astra with Codex
collaboration tools, worker-with-fable with Claude Code subagent tools,
neither elsewhere. An explicit request naming the other host's pairing is
reported as a host mismatch, not substituted. The worker reads and proposes
without writes, and a missing pairing does not block this planner's own
investigation. Link specifications and decision records without copying their
content.
When repository policy requires specification artifacts, use its canonical method
within existing edit authority; do not invent a specification framework.

## Publish within authority and verify

Present the concrete proposed items, exact authorized changes, dependencies,
assessments, and unresolved questions. When publication is already authorized
and material decisions are settled, proceed without another approval round.
Otherwise return the proposals at the user's requested boundary.

Before each write, refresh the target and record intent, expected prior state,
and available guards in existing permitted task evidence. Reuse matching work
instead of duplicating it. Apply only authorized fields and links, preserving
unrelated status, assignments, labels, estimates, and sprint membership.

Read back each effect and compare the saved scope, criteria, assessment, and
dependency endpoints with the proposal. An API acknowledgment alone is not
publication verification. After a timeout or partial response, suspend dependent
writes and reconcile authoritative issue/history records before retrying. A stale
search miss does not prove absence. Repair a verified no-effect failure within
scope; leave unresolved effects pending without duplicating them.

After verified planning publication, apply the documentation checkpoint within
the user's edit/publication authority. Reconcile represented scope, dependencies,
roadmap order, and proposed architecture from saved sources. Tracker-only requests
stop at tracker effects and report pending guide/publication work with its owner
or next action. A planning proposal never becomes implemented behavior.

Report verified references, ready items, blockers, clarification needs, skipped
or pending writes, guide synchronization, public publication/live verification
where applicable, and evidence limits. Do not describe published unresolved
work as ready or launch deliver-work automatically. Apply unslop to narrative
prose while preserving criteria, source wording, commands, and evidence.

When evaluating or changing this skill, read
[validation scenarios](references/validation-scenarios.md). Separate structural
checks, simulated decisions, host discovery, and actual tracker execution.
