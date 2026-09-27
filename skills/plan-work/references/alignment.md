# Check alignment with direction and backlog

Read for every proposed item except a small local one with no architecture,
pattern or backlog interaction. It details the entrypoint's alignment
checkpoint and grants no write or delivery authority.

## Gather evidence in proportion to the item

Start from the item's affected components, interfaces and terms and search
outward only as far as they reach. Use sources that exist for the project:

- current implementation, tests and contracts at the integration seam;
- accepted architecture and decision records, specifications, roadmap or
  direction statements, and project instructions;
- applicable style, design or interface rules the project states;
- related open, closed and active work, including in-flight change reviews.

Record each source's revision or observation date. When an expected source is
missing, say so and continue; do not create an architecture document, style
guide, tracker field or process to fill the gap. Stop searching when the
sources the item touches are covered. A repository-wide or backlog-wide audit
is not part of planning an item.

## Weigh each source by its authority

Authoritative sources bind the plan: accepted decisions, stated rules,
specifications and direction the owner has set. A pattern observed in code is
evidence of convention. Reuse it when it fits and explain a departure, but do
not write it into acceptance as policy or block work because it departs from
it. When an observed pattern seems to need binding status, raise that as a
question for its owner; do not decide it in the plan.

A superseded source yields to the source that replaced it. When two
authoritative sources disagree and neither supersedes the other, the conflict
is itself a decision for their owner.

## Compare the item and route the result

Compare each item on these points:

- Ownership and seam: which module, service or team owns the change and where
  it integrates.
- Patterns: whether it reuses established components and conventions.
- Backlog: duplicate, overlapping, conflicting or superseded items.
- Required inputs: what it cannot proceed without, and in what order.
- Direction: whether it advances an accepted direction or changes one.

Route each finding:

| Finding | Planning result |
| --- | --- |
| Aligned | Record the basis. No further investigation. |
| Authorized departure: the user or owner chose to change an accepted decision or rule | Explain the departure, the decision it changes and the reason. Include in scope any update the project's own process requires for that decision, such as a superseding record. Readiness is unaffected. |
| Unauthorized conflict with an accepted decision or rule | Record the conflict, the alternatives and their evidence. Mark the affected work as needing clarification and settle the decision through the entrypoint's decision step. Do not mark it ready until the decision is settled. |
| Departure from an observed pattern only | Explain the choice in the item as a design decision. It is not a conflict and does not block readiness. |
| Technical uncertainty that sources can resolve | Investigate what is discoverable. When it needs more than planning reads, propose a bounded investigation under the assessment contract; it can be ready while dependent work waits. |
| Duplicate or overlapping item | Reuse or refine the existing item instead of proposing another. |
| Superseded item | Reconcile it: link the replacement and propose a disposition for the old item. Changing, closing or relinking it requires publication authority for that effect. |
| Conflicting backlog item | Surface both. When they cannot both proceed, the choice belongs to their owner; mark only the affected work as needing clarification. |
| Required input | Retain it as a required input with the task-planning meanings. Shared-file coordination and preferred order are not blockers. |

Continue planning items a finding does not affect. A finding on one item never
blocks unrelated items.

## Record the result

Add one compact alignment entry to the item's existing assessment:

- result: `aligned`, including explained pattern departures and reconciled
  backlog; `authorized departure` from an accepted decision or rule;
  `conflict`, whose affected work needs clarification; or `unknown` when
  missing evidence prevents the comparison, which keeps affected work from
  ready under the assessment contract;
- the sources inspected, linked, each with a revision or observation date;
- departures with their reasons, reused, superseded or conflicting backlog
  items, required inputs, and open questions with the affected work;
- remaining uncertainty and the limit of the search.

Keep the entry compact. Link sources instead of copying them, and create no
separate alignment ledger.

## Leave delivery gates unchanged

Delivery treats the stored alignment result under the assessment contract's
pickup refresh and runs no second planning comparison. Its independent
Standards and Specification reviews are unchanged. Planning changes no project architecture, style rule or
backlog content except through authorized publication.
