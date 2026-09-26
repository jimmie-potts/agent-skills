# Report strategy, models, and agents

Read at pickup, before creating a non-root delivery agent, when reconciling
incomplete/resumed participation, and before any substantive checkpoint or final
handoff. Direct work with a verified single coordinator can use the entrypoint
fields for the summary; every delivery also keeps the
[Execution record](#write-the-execution-record). Use the entrypoint's
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
   Routine updates state changes, blockers and next actions; omit unchanged
   rosters and settings. Immediately expose consequential strategy, setting,
   team or authority changes, failed attempts and capability gaps, with reasons
   and affected counts/history. Keep the complete summary in existing evidence
   and publish it at substantive checkpoints and final handoff, including blocked
   or limited delivery. Retaining details in evidence never delays a material
   change notice. Do not turn missing history or telemetry into zero by omission.

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
Keep [review-round and finding history](review-cycles.md) in Evidence, with any
explicit limit's scope, consumption and accounting gaps. Two perspectives on
one candidate do not double the round count; corrections are counted separately.
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
At checkpoints and on resumption, use [the task packet](resumption.md) to retain
completed tasks, accepted revisions, findings, pending effects and the next
incomplete step alongside this execution summary. Link the same record instead
of creating a separate roster ledger.
If project policy or the user already authorizes a durable delivery record,
update that record and link it from the task. For an authorized public PR or
tracker update, include only the strategy and the Execution record below,
omitting private runtime identifiers, paths, and raw metadata. Reporting does not
authorize a new file, tracker comment, PR, service, installation, or paid run.
If a requested destination is unavailable, output the summary in the task and
report the destination limit.

## Write the Execution record

Keep one `## Execution record` section in the authorized durable delivery
record, such as the PR body where the project allows it. Without such a record,
include the section in the final response. It lets a project guide compare each
delivery's actual model, level and review effort with the item's Execution
recommendation. It records where each value came from, not identity: a spawn or
a request never establishes the executing model or level.

Copy the `Recommended` row into the task evidence at pickup. Write the section
when the durable record is created, refresh it at substantive checkpoints,
complete it before the guarded merge, and read it back at final handoff. Edit
the existing section rather than adding another.

### Rows

Write a table with the header `| Field | Value |` and these rows in this order,
with bare field names as in the examples. Add `Session label` directly after
`Session type` only when it applies.

| Field | Value |
| --- | --- |
| `Issue` | The resolved work reference: `owner/repo#<n>`, a Jira key or a document URL |
| `Recommended` | `<session type>, <model>, <level>` copied from the item's `## Execution recommendation` for the executing host: its `Session type`, the backticked identifier in `Model`, and `Thinking level`. `insufficient` when it records `**Status:** insufficient`; `none` when the item has no such section. Never retype a recommendation from other prose |
| `Coordinator model` | Sourced values for the coordinator that completes the section, as defined under the cell grammar |
| `Coordinator level` | Sourced values for the same coordinator |
| `Session type` | The session type delivery ended with: `One-shot`, `Pair`, `Orchestrate` or `Investigate first`. Strategy explains any change |
| `Session label` | Optional. The neutral label, in lowercase letters, digits and hyphens, that the coordinator set on its session in a project-defined session index. Never a raw session ID, path or account name |
| `Workers` | `none`, or one agent entry per implementation or investigation worker context, including failed and replaced attempts, in creation order |
| `Reviewers` | `none`, or one agent entry per independent task, fix or final reviewer context |
| `Agents` | A count of distinct agent contexts used, including every coordinator and advisor |
| `Consultations` | A count of completed advisor consultations, or `not applicable` without an advisory pairing |
| `Review rounds` | `final <count>; task <count>`, following [review cycles](review-cycles.md) |
| `Findings` | `P0 <count>; P1 <count>; P2 <count>; P3 <count>`: distinct findings from independent task, fix and final reviews, by stable identity. A regression reopens its finding and does not count again |
| `Finding causes` | `edge-case <count>; untested-bug <count>; wrong-approach <count>; other <count>`: the same distinct P0 to P2 findings classified by cause, so the counts sum to the P0 to P2 total. `edge-case` is behavior the candidate missed on an input or state it did not consider; `untested-bug` is a defect its own checks would have caught had they been run or written; `wrong-approach` is a design or interpretation that no amount of verification would have fixed; `other` is a finding outside the candidate's control, such as a wrong specification, environment or permission. Classify from the reviewer's stated failure condition; P3 findings are not classified |
| `Corrections` | A count of correction passes: each new candidate made to resolve review findings or failed acceptance, by a worker's guided correction or by the coordinator. Fixes batched before the next review count once. Models keeps the separate per-worker correction count, so the two can differ |

After the table, add these lines, each as its own paragraph:

- `**Fixes delivery:** <reference>` only when this change repairs a merged
  delivery. Name that delivery's merged PR as `owner/repo#<n>`, or its merge
  commit as `owner/repo@<sha>` when it merged without a PR.
- `**Recorded:** <YYYY-MM-DD>, <policy revision>` always. The date is the
  latest update. The revision is the deliver-work package whose convention
  the section follows, as `agent-skills@<sha>`, or `unknown`.

Keep narrative in the Strategy, Models and Evidence fields, outside the section.
When the coordinator changed on resumption, report earlier coordinators in
Models; `Agents` counts them.

### Cell grammar

- A token contains no spaces and none of `|`, `(`, `)`, `+`, `,` or `;`. Write
  a model as its identifier or alias, such as `claude-opus-5-5`, `opus[1m]` or
  `gpt-6-luna`. When a source gives only a display name, join its words with
  hyphens, such as `Opus-5.5`.
- A count is a non-negative integer, `at least <n>` for a known minimum, or
  `unknown`. Missing history is never zero.
- Sourced values are either exactly `unknown (unknown)`, or one or more items
  joined by ` + `, each `<token> (<provenance>)` with a provenance other than
  `unknown` and a token other than `unknown`. Give every source that exposed
  the value; a conflict between them is a known mismatch to report, not a
  reason to drop either item.
- An agent entry is `<label>: requested <model> at <level>, model <sourced
  values>, level <sourced values>`, with entries joined by `; `. Use the stable
  task-local label from the roster, in lowercase letters, digits and hyphens,
  such as `worker-1` or `standards-reviewer-1`. The requested model and level
  are tokens giving what the coordinator passed to the host: `default` for a
  part the request left to the host, such as effort on a Claude Code subagent,
  or `unknown` when the request is no longer known. A request is not evidence
  of the executing value. List every verified context; when earlier contexts
  cannot be recovered, `Agents` gives a known minimum.

Provenance uses exactly one of these terms. Each names a source, not an
independent verification of what executed:

| Term | Meaning |
| --- | --- |
| `host-observed` | Read from a host record or host-provided value rather than the model's own account, where the host exposes it and reading it is authorized: for example a Claude Code hook's `effort.level`, `CLAUDE_EFFORT`, or a Codex rollout's `turn_context` |
| `user-stated` | The user stated it for this delivery, including in a pasted recommendation prompt |
| `self-reported` | An agent named it from its own runtime instructions or return. Never ask an agent for its own level |
| `unknown` | No source exposed the value. Write exactly `unknown (unknown)` |

Never record a value without a provenance term you can name, and never replace
`unknown (unknown)` with a default, a requested value or a guess.

### Map rows to evaluation measures

The rows supply per-delivery workflow evaluation measures without renaming:

- First-submission acceptance: the delivery merged with `Corrections` 0.
- Acceptance after correction: the delivery merged with `Corrections` of 1 or
  more; the count is its rework.
- Agent and consultation counts: `Agents` and `Consultations`.
- Review effort: `Reviewers`, `Review rounds` and `Findings`.
- Effort fit: `Finding causes`. Edge-case and untested-bug findings are what
  a higher effort level buys down; wrong-approach findings are not, and point
  at uncertainty instead; `other` findings point at the specification or the
  environment. Records made under a policy revision before this row was added
  have no `Finding causes` row; the `**Recorded:**` revision tells the shapes
  apart, and a consumer should accept both.

Any `unknown` or `at least` count leaves the derived measure unknown. Missed
defects, false-positive blockers and gate violations need independent scoring;
elapsed time and attributable usage stay outside the section, with exposed
usage in Evidence.

### Examples

A complete record for a Codex delivery that repairs an earlier merge, with a
made-up policy revision:

```markdown
## Execution record

| Field | Value |
| --- | --- |
| Issue | example-org/example-app#42 |
| Recommended | Orchestrate, gpt-6-astra, high |
| Coordinator model | gpt-6-astra (user-stated) + gpt-6-astra (host-observed) |
| Coordinator level | high (user-stated) + high (host-observed) |
| Session type | Orchestrate |
| Session label | example-app-42 |
| Workers | worker-1: requested gpt-6-luna at medium, model gpt-6-luna (self-reported), level unknown (unknown); worker-2: requested gpt-6-luna at high, model gpt-6-luna (self-reported), level unknown (unknown) |
| Reviewers | standards-reviewer-1: requested gpt-6-luna at medium, model gpt-6-luna (self-reported), level unknown (unknown); specification-reviewer-1: requested gpt-6-luna at medium, model gpt-6-luna (self-reported), level unknown (unknown) |
| Agents | 5 |
| Consultations | not applicable |
| Review rounds | final 2; task 0 |
| Findings | P0 0; P1 0; P2 1; P3 2 |
| Finding causes | edge-case 1; untested-bug 0; wrong-approach 0; other 0 |
| Corrections | 1 |

**Fixes delivery:** example-org/example-app#40

**Recorded:** 2026-09-25, agent-skills@1a2b3c4
```

A resumed Claude Code delivery with an incomplete history:

```markdown
## Execution record

| Field | Value |
| --- | --- |
| Issue | PROJ-118 |
| Recommended | none |
| Coordinator model | claude-opus-5-5 (self-reported) |
| Coordinator level | unknown (unknown) |
| Session type | One-shot |
| Workers | none |
| Reviewers | standards-reviewer-2: requested sonnet at default, model unknown (unknown), level unknown (unknown); specification-reviewer-2: requested unknown at unknown, model sonnet (self-reported), level unknown (unknown) |
| Agents | at least 3 |
| Consultations | not applicable |
| Review rounds | final at least 1; task unknown |
| Findings | P0 unknown; P1 unknown; P2 unknown; P3 unknown |
| Finding causes | edge-case unknown; untested-bug unknown; wrong-approach unknown; other unknown |
| Corrections | unknown |

**Recorded:** 2026-09-25, unknown
```
