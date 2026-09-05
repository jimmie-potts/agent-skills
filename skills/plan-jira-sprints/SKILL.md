---
name: plan-jira-sprints
description: Review recent Jira sprint outcomes, refine the upcoming sprint, forecast the following sprint, and apply approved issue-planning changes. Use for backlog-to-sprint planning and post-sprint reassessment, not story implementation or delivery coordination.
---

# Plan Jira sprints

Turn current delivery evidence and human priorities into a concise, reviewable
sprint plan. Then apply only the issue changes the user has authorized.

## Authority and operating boundaries

Discovery is not permission to write. Default to a read-only proposal. Reuse
existing authorization for agreed changes; do not ask again for routine
continuation. Follow the host's current mode and the project's source-of-truth,
architecture, dependency, and external-effect rules. Planning itself does not
require inventing a Jira delivery issue.

Sprint creation, names, goals, dates, starting, and closing remain human-owned
in this workflow, even when tools expose those operations. Draft exact values
and verify the human's changes. Issue membership is a separate, authorizable
planning operation. Planning approval never starts implementation, transitions
story status, creates OPSX artifacts, launches delivery tasks, or merges code.

This is an agent-driven skill with no scripts. Use available connector tools
and repository-required helpers directly. Do not build a workflow runtime or
import, install, clone, execute, or depend on private Sprint Delivery automation.
Keep configuration such as Jira fields, board IDs, and link direction in live
project sources rather than hard-coding one site's values here.

## Establish the horizon and evidence

1. Identify the project, board, current sprint state, upcoming sprint, and
   following sprint from the request and available records. Default to the two
   most recent completed sprints for comparison. Resolve ambiguous identities
   before changing membership. Ask only for priorities, constraints, or facts
   that reasonable read-only discovery cannot establish.
2. Read applicable repository instructions and maintained planning guidance.
   Discover authoritative backlog scope, estimates, sprint membership, statuses,
   dependencies, accepted decisions, merged work, relevant contracts, and tests.
   Follow result pagination and narrow detailed reads to candidate work and its
   prerequisites. Record source dates and Git revisions where relevant.
3. State missing access or incomplete results. An inaccessible sprint is not an
   empty sprint. Unavailable estimates are not zero. An old planning report is
   historical evidence, not current Jira state. Distinguish planned, implemented,
   and verified behavior; describe test commands as verified only when evidence
   identifies what ran and against which revision.

Read [the planning-record reference](references/planning-record.md) when
drafting the proposal, refining story text, or recording authorized updates.
Keep one record instead of duplicating planning context across issues.

## Review outcomes and select work

Reconcile starting scope, additions, completed work, carryover, defects, and
estimates when the evidence permits. Distinguish the delivery cohort from
historical issues that happen to share sprint membership. If starting scope
cannot be reconstructed, say so rather than inventing a completion rate.

Assess observed review rework, integration failures, shared-file collisions,
merge waits, and implementation time where available. PR opening-to-merge time
is not engineering effort. Neither story points nor a short sprint calendar
window establishes capacity. Do not reuse a historical point ceiling as policy.

Prioritize required carryover and the requested sprint outcome. Reconcile old
backlog wording with accepted decisions and delivered code before proposing it.
Recommend commitment, explicit reserve, and an ordered pull-in queue. Explain
capacity assumptions and uncertainty, including missing estimates and differing
task mixes. Keep allocation arithmetic separate from evidence of actual effort.

Plan parallel implementation around independent responsibilities and testable
interfaces. Name prerequisite decisions, shared-file ownership, and merge order.
Use genuine dependency links for required inputs; keep coordination preferences
in the plan. Do not serialize independent work merely because tests or a shared
inventory need coordinated merges. Split a story only when each proposed unit
has a coherent outcome and independent acceptance evidence. Planning parallel
lanes does not authorize spawning implementation tasks.

For the following sprint, make an initial forecast and name the evidence that
will trigger reassessment after the upcoming sprint. Avoid presenting both
sprints as equally certain commitments.

## Define a demonstrable outcome

Prefer useful functionality exercised through automated integration or
composition tests. Reuse delivered components and tests where they establish
the intended claim; do not invent functionality solely for a demonstration.
Identify real production components, fake provider or transport boundaries,
required success and failure scenarios, prerequisites, and commands.

Each implementation story owns its component and boundary tests. A final
journey story adds interaction coverage. Fakes must not make the production
business decisions the test claims to prove. Call out what a composition proof
does not establish, such as live networking or durable provider behavior. Mark
new test paths and commands as planned until implemented and verified. Follow
the repository's testing policy when recommending actual execution.

## Propose and obtain necessary human input

Present the scope, changes from the existing plan, capacity reasoning, parallel
lanes, demonstration, and unresolved decisions together. Give the human enough
context to approve exact issue changes without reading every tool response.
Ask grouped questions when answers materially affect priority, scope, capacity,
architecture, or the demonstration. Do not repeat questions already answered.

Draft names shorter than 24 characters by default, adjusting to an explicit
project or user constraint. Write outcome-based goals. Propose dates only when
requested, preserve existing dates, and leave unknown dates and timezones
unresolved. Provide one grouped human handoff with the target board/sprint
identity, exact name and goal text, and necessary date/timezone decisions.

After human setup, read the sprint back through available tools. Continue
independent planning while waiting; keep membership changes pending until the
intended sprint is identifiable. If visibility requires an existing issue,
explain the limitation and use only a user-authorized temporary discovery issue.
Record its original membership and restore it after its authorized use. Do not
create a shared Jira planning issue to work around discovery limitations.

## Apply approved issue changes and verify

1. Determine which proposed operations are already authorized. Recommendation
   approval does not silently authorize every proposed external write. An
   explicit request to apply the agreed Jira changes does; carry that authority
   forward for routine in-scope continuation.
2. Re-read each affected issue before writing. Preserve implementation, review,
   and completed work unless modification is explicitly authorized. Reconcile
   intervening edits against the approved proposal rather than overwriting them.
3. Record intent in the authorized planning record or permitted task evidence,
   then use current connector capabilities for agreed issue creation, fields,
   estimates, membership, and dependency links. Never infer creation authority
   from the mere presence of a proposed new story. Follow the project's link
   helper and same-link-ID readback rules where present; otherwise verify live
   link semantics and both endpoints. Tool names are capabilities, not policy.
4. Read back each confirmed effect. Compare intended changes and preserve
   untouched titles, estimates, assignees, statuses, sprint membership, labels,
   parents, and links as applicable. Retain existing unresolved decisions and
   unique acceptance conditions when shortening descriptions.
5. Distinguish a definitive rejected request from an exposed or uncertain
   mutation. Repair ordinary confirmed failures within authorized scope. For
   uncertain outcomes, reconcile authoritative state before considering any
   repeat; follow project recovery requirements and obtain fresh authorization
   when they require it. Never blindly retry or claim success from a timeout.
   Continue independent reads, but pause dependent writes with unresolved scope
   or effects. Report the exact source of any policy-required pause.

Finish with confirmed changes, skipped or pending work, remaining human actions,
evidence limits, and reassessment triggers. Record text reduction when description
cleanup is part of the request. A planning pass may finish with an explicit human
handoff; an execution pass must not call pending mutations complete.

## Evaluate the skill

Read [the validation scenarios](references/validation-scenarios.md) only when
creating, revising, or evaluating this skill. They are synthetic exercises, not
live Jira scope or routine planning context. Apply the project's human-prose
guidance and Unslop where available without changing exact technical meaning.
