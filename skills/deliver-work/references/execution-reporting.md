# Optional execution accounting

Read only when the user or project requires the structured Execution record or
detailed model/agent accounting. Ordinary updates report outcomes, verification,
remaining work, owners and consequential choices without this table.

Preserve the established format below for consumers that parse it. Record only
exposed or user-stated facts, with their source; unknown is not zero. Keep raw
runtime identifiers private. Do not seek extra telemetry, inspect unrelated
sessions or create publication effects to populate a record.

Count distinct agent contexts, not roles or resumed messages. Include failed and
replaced attempts. A rejected creation known to have made no context is not an
agent; an ambiguous creation remains unresolved. Count completed consultation
exchanges only for a selected pairing. Keep explicit budget and review-round
accounting regardless of whether this optional format is used.

A session-type label describes the work actually done; it does not require a
particular orchestration pattern. Detailed settings are reported, not selected
by this reference. Check [required settings](model-gate.md) only when explicitly
required. Preserve historical records without treating them as current telemetry.

## Write the Execution record

Keep one `## Execution record` section in the authorized durable delivery
record, such as the PR body where the project allows it. Without such a record,
include the section in the final response. It lets a project guide compare each
delivery's actual model, level and review effort with the item's Execution
recommendation. It records where each value came from, not identity: a spawn or
a request never establishes the executing model or level.

When this format is required, copy the item's recommendation into the
Execution record's `Recommended` row at pickup, or use `none` when absent. Write the section
when the durable record is created, refresh it at substantive checkpoints,
complete it before the guarded merge, and read it back at final handoff. Edit
the existing section rather than adding another. Keep cumulative counts and
unresolved accounting here; link superseded detail in private evidence under
[resumption](resumption.md), without appending checkpoint history.

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
| `Session type` | The session type delivery ended with: `One-shot`, `Pair`, `Orchestrate` or `Investigate first`. Explain a consequential change briefly outside the table |
| `Session label` | Optional. The neutral label, in lowercase letters, digits and hyphens, that the coordinator set on its session in a project-defined session index. Never a raw session ID, path or account name |
| `Workers` | `none`, or one agent entry per implementation or investigation worker context, including failed and replaced attempts, in creation order |
| `Reviewers` | `none`, or one agent entry per independent task, fix or final reviewer context |
| `Agents` | A count of distinct agent contexts used, including every coordinator and advisor |
| `Consultations` | A count of completed advisor consultations, or `not applicable` without an advisory pairing |
| `Review rounds` | `final <count>; task <count>`, counted as review-work counts rounds |
| `Findings` | `P0 <count>; P1 <count>; P2 <count>; P3 <count>`: distinct findings from independent task, fix and final reviews, by stable identity. A regression reopens its finding and does not count again |
| `Finding causes` | `edge-case <count>; untested-bug <count>; wrong-approach <count>; other <count>`: the same distinct P0 to P2 findings classified by cause, so the counts sum to the P0 to P2 total. `edge-case` is behavior the candidate missed on an input or state it did not consider; `untested-bug` is a defect its own checks would have caught had they been run or written; `wrong-approach` is a design or interpretation that no amount of verification would have fixed; `other` is a finding outside the candidate's control, such as a wrong specification, environment or permission. Classify from the reviewer's stated failure condition; P3 findings are not classified |
| `Corrections` | A count of correction passes: each new candidate made to resolve review findings or failed acceptance, by a worker's guided correction or by the coordinator. Fixes batched before the next review count once. A per-worker correction count, when required, can differ from this total |

After the table, add these lines, each as its own paragraph:

- `**Fixes delivery:** <reference>` only when this change repairs a merged
  delivery. Name that delivery's merged PR as `owner/repo#<n>`, or its merge
  commit as `owner/repo@<sha>` when it merged without a PR.
- `**Recorded:** <YYYY-MM-DD>, <policy revision>` always. The date is the
  latest update. The revision is the deliver-work package whose convention
  the section follows, as `agent-skills@<sha>`, or `unknown`.

Keep explanatory prose outside the table. When the coordinator changed on
resumption, retain earlier coordinators in the history; `Agents` counts them.

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
