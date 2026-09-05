# Planning record and story guidance

Read this when drafting a sprint proposal, refining stories, or recording
approved Jira changes. Adapt the headings to the request; do not create empty
sections or repeat facts the reader can retrieve from one linked source.

## One planning record

Use an existing project planning record when available and its update is
authorized. Otherwise return the proposed document in the task until writing is
authorized. Keep repository policy in maintained guides, current scope in Jira,
and this pass's decisions and evidence in the planning record. A planning
report is not an OPSX artifact or a delivery authorization.

Use this compact order:

1. **Outcome and evidence.** State the decision the plan supports, source dates
   and revisions, previous-sprint outcomes, important lessons, and evidence gaps.
2. **Upcoming sprint.** Link selected issues, explain adds/removals/refinements,
   distinguish commitment and reserve, and give an ordered pull-in queue. A
   dated estimate snapshot may appear once here to make arithmetic reviewable;
   Jira fields remain authoritative. Exclude reserve from story-point totals
   and show the overall allocation separately.
3. **Parallel work and demonstration.** State independent lanes, required
   interfaces, shared-file coordination, merge sequence, joined proof, commands,
   prerequisites, observed or planned status, and limits of the test boundaries.
4. **Following sprint.** Give a provisional outcome, candidate work, uncertainty,
   and triggers for reassessment. Do not duplicate the upcoming sprint's detail
   when those decisions depend on its results.
5. **Human decisions and execution.** Group sprint setup/metadata text and open
   decisions. List agreed issue operations with enough before/after context to
   approve them. After authorized execution, record confirmed, skipped, and
   pending changes and supporting readbacks. Update this section rather than
   appending a second copy of the whole forecast.

State missing estimates explicitly and give a known subtotal rather than a
misleading complete total. A provisional estimate is a proposal until its Jira
field update is authorized and verified. Do not extrapolate points directly
from hours, PR duration, model tokens, or the number of parallel agents.

Avoid hard-coded Jira custom-field IDs, sprint IDs, issue keys, historical
capacity ceilings, or one repository's private data model. Discover these from
the current project. Preserve exact names and field values in an approved
change set once they are resolved.

## Concise Jira descriptions

Use only the sections needed:

- **Outcome:** One short paragraph describing the story's responsibility and
  resulting behavior.
- **Acceptance criteria:** Observable behavior, failure cases, compatibility,
  and story-specific tests. Retain real-component versus fake-boundary
  distinctions and mark planned commands accurately.
- **Readiness or boundaries:** Unresolved decisions, necessary exclusions, and
  ownership or interface-reuse explanations that dependency links cannot convey.
- **References:** Relevant contracts, accepted decisions, and implementation
  interfaces. Link instead of copying their full contents.

Keep estimates, assignees, sprint names, and labels in fields. Keep verified
dependencies in links. Keep capacity, reserve, lanes, general delivery policy,
and reassessment assumptions out of repeated story prose. Preserve genuine
readiness conditions, numeric acceptance thresholds, exact contracts,
identifiers, and commands. Do not remove a substantive requirement merely
because it occurs inside an old forecast section.

Before shortening a story, map unique original requirements to the proposed
description. Keep each unresolved decision once. Record any scope conflict for
resolution instead of choosing an interpretation silently. Verify untouched
fields and links after an authorized edit. Report the counting method and
measured reduction when requested, using the same method before and after.

## Human sprint handoff

Provide the project/board, known sprint identifier, exact proposed name and
goal, and any requested dates with timezone. Count the proposed name's
characters. Distinguish values that should change from existing values to keep.
If dates were not requested and are unknown, ask the human to supply them;
do not infer them from earlier sprint lengths.

After setup, confirm the correct sprint identity and requested metadata through
available tools. If some fields remain inaccessible, state what is confirmed,
what relies on human confirmation, and what is still unverified. Do not claim
tool-verified metadata from a human statement alone. Once the target identity
is authoritative, an inaccessible optional metadata field need not block an
otherwise authorized membership update.
