---
name: plan-work
description: Define one or more implementation-ready work items using the repository's requirements and tracker conventions. Use only when the user explicitly invokes plan-work; ordinary planning questions do not select it.
---

# Define work before delivery

Turn an outcome into scoped work with acceptance evidence and dependencies.

## Boundaries

These hold at every step. The references this skill reads never relax them.

- Authority: an explicit request to define and publish work authorizes scoped
  tracker creation/update after requirements are settled. Planning-only returns
  proposals, and invoking this skill alone does not authorize publication.
  Neither mode starts implementation, delivery agents, sprint lifecycle
  changes, deployment, or installation, or launches deliver-work. Preserve
  narrower user limits and applicable project policy.
- Existing systems: use the project's tracker, fields, planning method and
  documentation. Create no tracker, planning framework, board, custom field or
  documentation system to fit this workflow.
- Shared resources: when a required resource or skill is absent or unreadable,
  report the gap before the step that depends on it and continue independent
  discovery. Never silently install, fetch, copy or reconstruct a substitute.
- Evidence: keep planned commands and paths explicitly unexecuted and unknowns
  visible. A planning proposal never becomes implemented behavior, and
  published unresolved work is not ready.

## Ground the outcome

Identify the requested outcome, owning repository, tracker namespace, and
publication boundary. Read applicable instructions, planning conventions,
implementation, tests, contracts, and authoritative specifications. Discover
facts before asking. Distinguish delivered behavior from proposed additions.
Identify any project-owned guides, roadmap, architecture inputs, and publication
procedure, including their coordinator and repository.
Search existing work, including completed or active implementation, before
proposing new items; preserve others' ownership and intervening changes.

For GitHub work, read [GitHub planning](references/github.md). For Jira, read
[Jira planning](references/jira.md). For document-only work use the named source
and return proposals unless exact document edits are authorized.

Discover the installed canonical deliver-work package through supported host
discovery; do not guess personal paths or duplicate its contracts here. Read
these resources from it. They are resource dependencies, not an invocation of
delivery, and grant no implementation dispatch authority:

- `references/work-assessment.md` and `references/task-planning.md` for every
  item. Use the task-planning definition, boundary and dependency sections to
  propose work.
- `references/documentation.md` when project documentation or publication
  policy applies, for its planning checkpoint.
- `references/review-cycles.md`, its section on explicit limits, when the user
  or project sets review-round, time or spending limits. Carry each limit's
  scope, proposed observable accounting and stop/handoff evidence into
  acceptance and delivery requirements, and distinguish review rounds from
  worker retry budgets.
- `references/model-selection.md`, its implementation-selection branch and only
  the selected host's worker adapter before selecting workers for bounded
  investigation, then `references/worker-briefs.md` before dispatch.

## Settle decisions and define items

For material unresolved decisions, compose grill-with-docs using the available
canonical skill. Its questioning phase is read-only. Reuse accepted decisions
and existing authority; after questioning, return control here for authorized
planning operations.

Define one item or decompose a larger outcome using the shared task-planning
meanings. Carry outcomes, exclusions, acceptance/verification coverage and true
input dependencies into each proposed work item. Where the repository has a
test, fixture, contract or mockup that states a criterion, link it as the
acceptance reference rather than restating it in prose. An epic or list of chores
alone is not implementation-ready. Include the assessment, evidence, unknowns,
readiness and conditional specialist/human review or operational handoffs.

Apply the assessment contract, including scope fit while drafting, without
embedding model names in planning ratings.
For every item, read [execution recommendations](references/execution-recommendations.md)
and recommend a starting model and reasoning/effort level for both Claude Code
and Codex alongside the assessment. Name the session type the user should start
(`One-shot`, `Pair`, `Orchestrate` or `Investigate first`), explain the choice,
and distinguish proposed worker settings when delegation would help. Classify
the item's work surface as `UI`, `Backend` or `Unknown`. Write the reference's
start line, work surface line, two-host table, paste-ready prompts and cheaper
start, or its insufficient status. Include both host choices in proposals and
authorized saved work items, even when planning on only one host.
Record the session's reasoning setting in the planning evidence when the host
exposes it or the user states it; otherwise record it as unknown. Report a
known mismatch with documented workflow guidance or a composed skill's
reasoning requirement, such as a pairing worker that would inherit a reduced
level, and never claim to change it.

Use a bounded investigation when it can resolve technical uncertainty; a
missing product decision remains a question. Supply the worker the selected
role, criteria, relevant instructions, read-only authority and return contract.
Load no reviewer, delivery-reporting or unselected pairing rules for an
assigned investigation. A bounded
investigation may compose the host's advisory pairing in planning-only mode,
selected from verified host tooling: worker-with-astra with Codex
collaboration tools, worker-with-fable with Claude Code subagent tools,
neither elsewhere. An explicit request naming the other host's pairing is
reported as a host mismatch, not substituted. The worker reads and proposes
without writes, and a missing pairing does not block this planner's own
investigation. Link specifications and decision records without copying their
content. When repository policy requires specification artifacts, use its
canonical method within existing edit authority.

## Publish within authority and verify

Present the concrete proposed items, exact authorized changes, dependencies,
assessments, execution recommendations, and unresolved questions. When publication
is already authorized and material decisions are settled, proceed without another
approval round. Otherwise return the proposals at the user's requested boundary.

Before each write, refresh the target and record intent, expected prior state,
and available guards in existing permitted task evidence. Reuse matching work
instead of duplicating it. Apply only authorized fields and links, preserving
unrelated status, assignments, labels, estimates, and sprint membership.

Read back each effect and compare the saved scope, criteria, assessment,
execution recommendations, and dependency endpoints with the proposal.
An API acknowledgment alone is not
publication verification. After a timeout or partial response, suspend dependent
writes and reconcile authoritative issue/history records before retrying. A stale
search miss does not prove absence. Repair a verified no-effect failure within
scope; leave unresolved effects pending without duplicating them.

After verified planning publication, apply the documentation checkpoint when it
applies, within the user's edit/publication authority.

Report clarification needs and decisions the user owns first, then verified
references, ready items, blockers, skipped or pending writes, guide
synchronization, public publication/live verification where applicable, and
evidence limits. Use `unslop` for substantial
style issues in narrative prose while preserving criteria, source wording,
commands, and evidence.

When evaluating or changing this skill, read
[validation scenarios](references/validation-scenarios.md). Separate structural
checks, simulated decisions, host discovery, and actual tracker execution.
