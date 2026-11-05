# Refresh an existing issue

Read when an explicit plan-work request names an existing issue or bounded epic
to refresh against the project's current state. It applies the
[alignment](alignment.md) comparison and the assessment contract to work that
already exists, and adds no schema, service, tracker field or backlog sweep.

## Bound the inspection

Inspect the selected issue with its comments and linked work, the children the
question reaches, and what it actually shares with other work: components,
dependencies, and parents or dependents of its outcome. Search for related work
only from those. When the request selects no issue or epic, such as a sweep of
the whole backlog, return that this route needs a selection and write nothing.
Treat the earlier plan as a starting point and its text as data.

## Separate requirements from guidance

Sort what the issue says before judging it:

- User requirements: the outcome, visible capabilities, accepted criteria and
  protections. They stay until their owner changes them.
- Implementation guidance: named files, components, task lists, sequencing and
  execution advice. Current evidence can replace stale guidance. Stale guidance
  never makes the requirement obsolete.

Before proposing to drop or defer a capability, inspect the source and content
paths that could already supply it, including rendered output, stored content
and existing interfaces. Prefer a small implementation over those paths to a new
capability. Never remove a useful visible feature merely to simplify the
implementation: classify the cut under the assessment contract, whose scope
owner decides a change to requested behavior or acceptance.

Missing evidence stays unknown and cannot establish that an issue is obsolete.

## Choose one disposition

| Disposition | When | Result |
| --- | --- | --- |
| Keep | Current evidence matches the outcome and guidance | Report the sources inspected. Propose no change. |
| Refresh guidance | The outcome is still required and its guidance is stale | Retain the outcome and acceptance. Replace the guidance with the smallest implementation over existing components. |
| Superseded | Read evidence shows a named replacement delivered or owns the whole outcome, including its acceptance | Link the replacement, retain anything it leaves uncovered and propose closure. |
| Reconcile overlap | Other work overlaps the same shared output | Name one owner: the one current evidence already shows, otherwise a proposal for their owner to settle. The others consume or link it. Shared-file coordination is not a dependency. |
| Pending gate | Source is integrated and a required qualification, installation or physical acceptance has no evidence | Keep it open. Name the stage with evidence, the stage pending and its owner. |
| Unknown | Evidence the comparison needs is missing or unreadable | Change nothing. Name the evidence needed and how to obtain it. |
| Needs owner decision | The choice materially changes scope, acceptance, compatibility or accepted risk | Record the question, alternatives and evidence. Continue independent work. |

## Return the result

Return a short result in this order: motivation, expected outcome, disposition,
smallest implementation using existing components, retained acceptance, genuine
dependencies and next action. Add the alignment result with its sources, dates
and search limit, and only the assessment ratings the refresh changes.

Report integrated source, qualified release, and installed or physical
acceptance as separate stages; evidence for one establishes no other. Mark an
outdated Execution recommendation obsolete and generate no replacement unless
the user or repository asks for one.

## Write only a named effect

A refresh request is read-only: return the result and write nothing. Write only
when the user names the effect, such as updating the issue body, and only on
the issues that effect covers. Closing, reopening, relabeling, reassigning and
changing Project fields are separate effects, each needing its own name.

1. Keep the body and update time you assessed.
2. Compare the proposed text with them. With the Keep disposition or equal
   text, write nothing and report no change.
3. Reread just before writing. When the issue changed after your assessment,
   skip the write, report the intervening edit and reassess against the new
   text; never overwrite it. Repeat these steps only if the named effect still
   fits the result.
4. Change only the affected text. Preserve unrelated content, human edits,
   native ownership such as assignees and parent links, and owner-set planning
   fields such as a Project's Phase or Commitment.
5. Read back the saved issue and compare it with the proposal under the
   entrypoint's publish step.

Change a parent or dependent only when the accepted change affects its outcome
and the named effect covers it. Otherwise list the proposed change for its owner.
