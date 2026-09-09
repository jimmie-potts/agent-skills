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
Search existing work, including completed or active implementation, before
proposing new items; preserve others' ownership and intervening changes.

For GitHub work, read [GitHub planning](references/github.md). For Jira, read
[Jira planning](references/jira.md). For document-only work use the named source
and return proposals unless exact document edits are authorized. Do not create
a tracker, planning framework, board, or custom fields to fit this workflow.

Discover the installed canonical deliver-work skill through supported host
discovery and read its `references/work-assessment.md`. This is a required
resource dependency, not an invocation of delivery. Do not guess personal paths
or duplicate its definitions here. If absent or unreadable, report the gap
before dependent assessment; continue independent source investigation. Never
silently install or reconstruct the contract.

## Settle decisions and define items

For material unresolved decisions, compose grill-with-docs using the available
canonical skill. Its questioning phase is read-only. Reuse accepted decisions
and existing authority; after questioning, return control here for authorized
planning operations. A missing required skill blocks that substep, not unrelated
discovery. Do not silently fetch, copy, or replace it.

Define one item or decompose a larger outcome only where each item has a
coherent result and independent acceptance evidence. An epic or a list of
implementation chores alone is not implementation-ready work. Each item needs:

- outcome, intended behavior, exclusions, and authoritative scope links;
- testable acceptance criteria and prerequisite decisions/work references;
- planned verification for each criterion, including relevant failure,
  recovery, security, compatibility, and user-journey cases;
- the shared contract's assessment, evidence, unknowns, and readiness;
- conditional specialist/human review and operational handoff expectations.

Apply the assessment contract without embedding model names in planning ratings.
Record the session's reasoning setting in the planning evidence when the host
exposes it or the user states it; otherwise record it as unknown. Report a
known mismatch with documented workflow guidance or a composed skill's
reasoning requirement, such as a pairing worker that would inherit a reduced
level, and never claim to change it. Keep planned commands and
paths explicitly unexecuted. Use a bounded investigation when it can resolve
technical uncertainty; a missing product decision remains a question. A
bounded investigation may compose the host's advisory pairing in planning-only
mode, selected from verified host tooling: sol-with-astra with Codex
collaboration tools, worker-with-fable with Claude Code subagent tools,
neither elsewhere. An explicit request naming the other host's pairing is
reported as a host mismatch, not substituted. The worker reads and proposes
without writes, and a missing pairing does not block this planner's own
investigation. Link specifications and decision records without copying their
content.
When repository policy requires specification artifacts, use its canonical method
within existing edit authority; do not invent a specification framework.

Map real incoming dependencies and detect cycles. Keep shared-file coordination
and preferred merge order distinct from required inputs. Preserve independently
deliverable work; do not serialize it merely because one coordinator writes.

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

Report verified references, ready items, blockers, clarification needs, skipped
or pending writes, and evidence limits. Do not describe published unresolved
work as ready or launch deliver-work automatically. Apply unslop to narrative
prose while preserving criteria, source wording, commands, and evidence.

When evaluating or changing this skill, read
[validation scenarios](references/validation-scenarios.md). Separate structural
checks, simulated decisions, host discovery, and actual tracker execution.
