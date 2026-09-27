# Review input and result contract

Read before starting a review and before writing its result. Keep both in the
caller's existing task evidence, such as the delivery's task packet, or in the
response for a standalone review. This contract adds no ledger, file, service or
tracker field.

## Record the input

Record these before the first reviewer starts, and again for each round:

- Work and round: the work reference, round kind (`final` for whole-change
  review, `task` for a task boundary) and the cumulative number of rounds of
  that kind, including this one.
- Comparison: base, head and merge-base commits, the diff command and the dirty
  state, or the SHA-256 digest of one captured patch.
- Requirements: the authoritative scope and acceptance reference and the
  version reviewed, such as an edit timestamp, revision or readback date, or
  `none` when no specification exists.
- Policy: the standards sources and the policy revision that governs review,
  fixed at the first round even when the change edits that policy.
- Validation: raw commands, results and the revision each ran on. Supply
  results as facts, never as a verdict for reviewers to confirm.
- Coverage: required axes, the task boundary for a task round, changed areas,
  and any specialist or qualified human review the assessment requires.
- Settings: explicit user or project reviewer requirements and the selection
  made from them.
- Limits: each explicit round, time or spending limit with its source, scope,
  unit, threshold, consumed amount and accounting source. `none` when no limit
  was set; missing accounting is unknown, never zero.
- History: earlier rounds with their comparisons, and stable finding IDs with
  state and the latest comparison that reviewed them.

A missing required field leaves the dependent round unstarted or its result
`incomplete`; it is never filled with a default.

## Decide each axis

Give each required axis exactly one status:

| Status | Meaning |
| --- | --- |
| `satisfied` | A fresh independent reviewer assessed this exact comparison against the recorded requirements and policy, stated its coverage, and no P0, P1, P2 or project-defined blocker on this axis remains unresolved |
| `action-required` | The axis was assessed and at least one P0, P1, P2 or project-defined blocker on it remains unresolved |
| `incomplete` | The axis cannot be decided: missing specification, failed, partial or missing return, unavailable required independence or control, stale comparison or requirements, exhausted limit, or missing mandatory evidence |

Specification cannot be `satisfied` without an authoritative requirement. One
axis never supplies the other. When an axis has an open blocker and also lacks
evidence, report `action-required` and name the gap in the coverage; the gap
still prevents `satisfied` after the fix. A required specialist axis has its
own reviewer entry, and the coverage states its status with the same
vocabulary. Unresolved P3 findings do not block an axis;
record their disposition. A consumer accepts a final result only when both axes
are `satisfied`, every required specialist axis is `satisfied`, and its
comparison and requirement version equal the current ones; any other result
blocks the gate it governs.

## Write the result

Write one `## Review result` section per round: a `| Field | Value |` table
with these rows in this order, then a findings list and a coverage paragraph.

| Field | Value |
| --- | --- |
| `Work` | The work reference, or `none` for an unticketed standalone review |
| `Round` | `final <n>` or `task <n>`: the round kind and its cumulative number |
| `Comparison` | `base <sha>; head <sha>; merge-base <sha>`, or `patch sha256:<digest>` |
| `Requirements` | `<reference> at <version>`, or `none` |
| `Policy` | The governing policy revision, such as `agent-skills@<sha>`, or `unknown` |
| `Standards` | The Standards status. In a task round it carries the quality verdict |
| `Specification` | The Specification status |
| `Reviewers` | One entry per reviewer context in this round, joined by `; ` |
| `Open findings` | `P0 <count>; P1 <count>; P2 <count>; P3 <count>`: findings still `unresolved` or `regression` after this round |

A reviewer entry is `<label>: <axis>, requested <model> at <level>, model
<sourced values>, level <sourced values>`. The label is a stable task-local name
such as `standards-reviewer-1`; the axis is `standards`, `specification` or a
lowercase specialist name such as `security`. A requested value is what the
coordinator passed, `default` when it left the value to the host, or `unknown`.
Sourced values are `unknown (unknown)` or one or more `<value> (<source>)`
joined by ` + `, where the source is `host-observed`, `user-stated` or
`self-reported`. A spawn or request never establishes the executing value.
Without the axis, an entry matches deliver-work's Execution record grammar, so
a composing delivery copies it into its `Reviewers` row.

After the table, write `**Findings:**` followed by one line per finding, or
`none`:

```text
- <ID> (<severity>, <axis>, <state>): <file:line>, <failure condition>; first <round>, latest <round>
```

The state is `unresolved`, `resolved`, `regression`, or, for P3 only,
`accepted` or `deferred` with its reason in the text. Findings keep their IDs
across rounds, reviewers and resumption, as [review cycles](review-cycles.md)
describes.

Then write `**Coverage:**` with the changed areas each axis covered, the gaps,
the evidence limits and any required specialist or human review still pending.

### Examples

A second final round after one correction:

```markdown
## Review result

| Field | Value |
| --- | --- |
| Work | example-org/example-app#42 |
| Round | final 2 |
| Comparison | base 1111111111111111111111111111111111111111; head 3333333333333333333333333333333333333333; merge-base 1111111111111111111111111111111111111111 |
| Requirements | example-org/example-app#42 at 2026-09-25T10:00Z |
| Policy | example-app@abcdef1 |
| Standards | satisfied |
| Specification | satisfied |
| Reviewers | standards-reviewer-2: standards, requested opus at default, model unknown (unknown), level high (user-stated); specification-reviewer-2: specification, requested opus at default, model claude-opus-5-5 (self-reported), level high (user-stated) |
| Open findings | P0 0; P1 0; P2 0; P3 0 |

**Findings:**
- F1 (P2, specification, resolved): src/export.ts:40, an empty filter exported every tenant's rows; first final 1, latest final 2
- F2 (P3, standards, accepted): src/export.ts:12, the helper name is vague; accepted because the module owner prefers it; first final 1, latest final 1

**Coverage:** Both axes covered the export handler, its tests and the CI job. No specialist review was required. Neither reviewer exposed its executing level.
```

A standalone review of an uncommitted patch without a specification:

```markdown
## Review result

| Field | Value |
| --- | --- |
| Work | none |
| Round | final 1 |
| Comparison | patch sha256:4f1c0d2e3b4a5968778695a4b3c2d1e0f0e1d2c3b4a5968778695a4b3c2d1e0f |
| Requirements | none |
| Policy | unknown |
| Standards | action-required |
| Specification | incomplete |
| Reviewers | standards-reviewer-1: standards, requested sonnet at default, model unknown (unknown), level unknown (unknown) |
| Open findings | P0 0; P1 1; P2 0; P3 0 |

**Findings:**
- F1 (P1, standards, unresolved): lib/auth.py:88, an expired token passes the check; first final 1, latest final 1

**Coverage:** Standards covered the whole patch. Specification is incomplete because no authoritative requirement exists, so no specification reviewer ran. The user supplied the patch; no tests were run.
```
