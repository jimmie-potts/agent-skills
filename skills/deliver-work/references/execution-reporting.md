# Report strategy, models, and agents

Read before delivery implementation or delegation. Use the entrypoint's
Strategy, Models, Agents, and Consultations fields for this summary. The task
conversation is the default output, so the user can see it while work proceeds
and find it in the final response. These instructions require agent-authored
reporting; they do not install automatic host telemetry or a dashboard.

## Publish at the decision and keep it current

1. Before implementation or the first delegation, publish the selected strategy
   and a short rationale tied to the work assessment. Name the decision owner
   and agents whose returned input informed the choice. Say `none` if nobody was
   consulted. Include a brief account of their contribution, not internal
   deliberation or a transcript. Merely being assigned work or listed as a
   reviewer does not make an agent a decision contributor.
2. List the coordinator, implementation workers, advisors, investigation agents,
   and independent reviewers by stable task-local labels such as coordinator,
   worker-1, and standards-reviewer. Record each role's selected model/reasoning,
   actual request when different, reported settings, evidence source, and state.
   Group identical settings only when the distinct labels and counts remain
   clear. A planned role has no observed runtime settings yet.
3. Report the counts below before spawning, after confirmed team changes, and
   when a strategy, setting, or fallback changes. Explain what changed and why.
   At later checkpoints, keep these fields short while retaining their current
   values. Carry the complete execution summary into the final response, even
   for direct implementation, a blocker, or a user-imposed delivery limit.

Use settings from the current host records or runtime reports and label their
source. Distinguish a user-stated setting from a host observation and a worker's
self-report from independently exposed metadata. A successful spawn proves a
request succeeded, not the executing model's identity. Use `unknown` for
unexposed values. Never infer a coordinator's identity from a model menu, agent
nickname, pairing skill name, or the model requested for a worker. Report known
mismatches and apply the selection policy's mandatory-setting gates.

## Count agents, not roles or messages

- Active now: agents currently working on this delivery or waiting for a
  delivery decision, including the reporting coordinator. Exclude agents whose
  assignment has finished, even if their session remains available. State
  `unknown` when current activity cannot be established.
- Distinct used to date: unique agent contexts actually established for this
  delivery, including the coordinator and completed, failed, or replaced workers
  and reviewers. Include authorized descendants. Count the same coordinator
  once when it also advises or implements. Two independent reviewers on the
  same model are two agents; one model can run several agents.
- Planned additional: agents selected for future work but not yet established.
  Name their roles and keep them out of actual counts until creation is
  confirmed. If the remaining team is undecided, say `unknown` instead of zero.
  Zero requires an established plan with no further agents; silence is unknown.

Count the reporting coordinator as one confirmed participant even when the
available records mention only a worker. Unknown model identity does not remove
an established agent from the count. Report a known minimum when other activity
or historical participation is uncertain.

Retain a task-local roster mapping stable labels to verified host identities
and states using already authorized host records and worker evidence. Keep raw
identifiers private. Resume and consultation messages to the same agent do not
increase the distinct count. A replacement or fresh review context does. A
rejected spawn confirmed to have created no agent does not count as used;
an ambiguous spawn outcome remains unresolved until reconciled.

Keep correction counts, attempt history, effort increases, and model promotions
in Models, following [model selection](model-selection.md) and its host adapter.
A same-worker correction adds no agent or advisor consultation by itself; a
promotion that creates a fresh worker adds one distinct agent. Call a replacement
a promotion only when the recorded settings establish an increase. State known
correction and effort-increase counts explicitly; keep missing history unknown.
Preserve failure history and the task's effort-increase history across handoffs.
For a new advisory attempt, report required consultations as still outstanding
until evidenced, and pause the work they govern under the pairing protocol.
Include exposed attributable usage in Evidence, retaining failed attempts and keeping subscription
usage separate from API cost. Missing usage remains unknown.

On resumption, reconcile the roster against available history and current host
state before publishing totals. Do not reset earlier use to zero. If earlier
agents, descendants, or creation outcomes cannot be verified, report a known
minimum and the coverage gap, for example `distinct used: at least 3; earlier
review contexts unknown`. An incomplete roster cannot support an exact total.
Counts describe participation; they do not prove review independence or that
any delivery gate passed.

For an advisory pairing, count completed consultation exchanges, per worker and
in total. Retain failed or replaced attempts. Pending unanswered requests are
separate; a required approach or final-review consultation is not evidence it
happened. Use `unknown` for missing records and `not applicable` when no advisor
loop was used. Independent delivery reviews are not advisor consultations.

## Retain the summary without new publication effects

Keep the current roster and summary in the task's existing evidence or handoff.
If project policy or the user already authorizes a durable delivery record,
update that record and link it from the task. For an authorized public PR or
tracker update, include only the strategy and relevant role summary, omitting
private runtime identifiers, paths, and raw metadata. Reporting does not
authorize a new file, tracker comment, PR, service, installation, or paid run.
If a requested destination is unavailable, output the summary in the task and
report the destination limit.

## Example during implementation

This synthetic snapshot assumes a verified coordinator identity, one confirmed
worker creation with a runtime self-report, one completed approach consultation,
and two reviewers selected but not started. The remaining checkpoint fields
still carry source, revisions, checks, and delivery status.

- Strategy: advisory pairing because implementation is bounded with two design
  checkpoints. Coordinator selected it; worker-1's approach input confirmed the
  test boundary.
- Models: coordinator/advisor, host-reported gpt-6-astra/high, selection matches;
  worker-1, selected/requested gpt-5.6-terra/medium, self-reported same, independent
  runtime metadata unknown. Standards and Specification reviewers are planned,
  each selected gpt-5.6-terra/high; no request or runtime report yet. Worker-1 is
  on its initial attempt with 0 corrections, effort increases, or promotions.
- Agents: active 2, coordinator and worker-1; distinct used 2; planned additional
  2, standards-reviewer and specification-reviewer. Advisor is the coordinator.
- Consultations: worker-1 completed 1, total 1; pending 0.
