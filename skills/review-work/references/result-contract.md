# Review input and result contract

Read before starting a review and before writing its result. Keep both in the
caller's existing task evidence, such as the delivery's task packet, or in the
response for a standalone review. This contract adds no ledger, file, service or
tracker field; a caller that must keep the result beyond the conversation
chooses an existing destination it is authorized to use.

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
- Policy: the standards sources and the version of the policy that governs
  review: the full target commit at which those sources last changed, or, for
  a source without revisions such as a wiki page, the date it was read. An
  unrelated target commit does not change it. Record the current project
  policy each round. The candidate's own edits to that policy never
  count as policy for its review: the first round's gates are a floor it cannot
  lower. A later project policy change the candidate did not make is current
  policy, and it makes earlier results stale.
- Validation: raw commands, results and the revision each ran on. Supply
  results as facts, never as a verdict for reviewers to confirm.
- Coverage: required axes, the task boundary for a task round, changed areas,
  and any specialist or qualified human review the assessment requires.
- Settings: explicit user or project reviewer requirements; the selection
  made from them with its rationale: the impact, the review task in a line or
  two, the selected tier and any exception with its evidence and coverage
  limits; and the reviewer execution preflight: each control's evidence class,
  whether it is mandatory, and any unsupported or unverified control. Record
  file-write, publication and descendant restrictions as `enforced` only with
  host evidence for this reviewer; otherwise record them as `instruction-only`.
  On Grok Bot, restriction is instruction-only with no Claude
  `review-work-reviewer` profile claim; an axis missing required evidence for a
  mandatory control is `incomplete` with the gap named. When
  cross-provider routing applies, include its trigger, selected provider/axis,
  qualification evidence or fallback reason, and actual coverage. Provider
  diversity alone supplies no verdict or extra axis.
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
| `satisfied` | A fresh independent reviewer assessed this exact comparison against the recorded requirements and policy, stated its coverage, and no P0, P1, P2 or project-defined blocker that lists this axis remains unresolved |
| `action-required` | The axis was assessed and at least one P0, P1, P2 or project-defined blocker that lists it remains unresolved |
| `incomplete` | The axis cannot be decided: missing specification, failed, partial or missing return, no retained return matching this round's inputs, unavailable required independence or control, stale comparison, requirements or policy, a candidate no round could review before a limit ran out, or missing mandatory evidence |

Specification cannot be `satisfied` without an authoritative requirement. One
axis never supplies the other. When an axis has an open blocker and also lacks
evidence, report `action-required` and name the gap in the coverage; the gap
still prevents `satisfied` after the fix, and the caller obtains it with the
correction. Findings from a failed return leave the axis `incomplete` instead,
as [reviewer execution](reviewer-execution.md) describes. A required specialist
axis has its own reviewer entry, and the coverage states its status with the
same vocabulary. Unresolved P3 findings do not block an axis; record their
disposition. A consumer accepts a final result
only when both axes are `satisfied`, every required specialist axis is
`satisfied`, its policy is known, and its comparison, requirement version and
policy equal the current ones; any other result blocks the gate it governs.
Required human acceptance remains a separate gate for the caller.

## Write the result

Write one `## Review result` section per round: a `| Field | Value |` table
with these rows in this order, then a findings list and a coverage paragraph.

| Field | Value |
| --- | --- |
| `Work` | The work reference, or `none` for an unticketed standalone review |
| `Round` | `final <n>` or `task <n>`: the round kind and its cumulative number |
| `Comparison` | `base <sha>; head <sha>; merge-base <sha>`, or `patch sha256:<digest>` |
| `Requirements` | `<reference> at <version>`, or `none` |
| `Policy` | `<repository>@<full commit>` at which the governing sources last changed, `<source> read <YYYY-MM-DD>` for a source without revisions, several joined by ` + `, or `unknown` |
| `Standards` | The Standards status. In a task round it carries the quality verdict |
| `Specification` | The Specification status |
| `Reviewers` | One entry per reviewer context in this round, joined by `; ` |
| `Open findings` | `P0 <count>; P1 <count>; P2 <count>; P3 <count>`: findings still `unresolved` or `regression` after this round |

A reviewer entry is `<label>: <axis>, requested <model> at <level>, model
<sourced values>, level <sourced values>`. The label is a stable task-local name
such as `standards-reviewer-1`; the axis is `standards`, `specification`, a
lowercase specialist name such as `security`, or `both` for one task-round
reviewer returning both task verdicts. A final round never uses `both`. A
requested value is what the coordinator passed or a selected profile sets,
`default` if neither, or `unknown`. Sourced values are
`unknown (unknown)` or one or more `<value> (<source>)` joined by ` + `, where
the source is `host-observed`, `user-stated` or `self-reported`. A spawn or
request never establishes the executing value. Without the axis, an entry
matches deliver-work's Execution record grammar, so a composing delivery copies
it into its `Reviewers` row.

After the table, write `**Findings:**` followed by one line per finding, or
`none`:

```text
- <ID> (<severity>, <axes>, <state>): <file:line>, <failure condition>[; aliases <axis>:<raw ID>, ...]; first <round>, latest <round>
```

The ID is a stable task-local identifier of letters and digits, with single
hyphens between parts, such as `F1` or `71-F1`. The location is a file and
line. The axes are each axis whose reviewer raised this failure condition,
joined by `+` when there are several, such as `standards+specification`. List
each axis once and never write `both`, even in a task round. One failure
condition keeps one ID however many axes raise it:

- Status: each listed axis is `action-required` while the finding is an open
  P0 to P2 or project-defined blocker.
- Counts: `Open findings` counts the finding once.
- Support: each listed axis's retained return in the finding's latest round
  must raise or reassess it among its findings; naming the file only in its
  coverage is not support. The finding becomes `resolved` only when every
  listed axis's return confirms the fix; until then it keeps its earlier state.

When a reviewer's return names the finding by its own ID rather than this one,
record that raw ID as an alias qualified by the axis whose return used it, such
as `; aliases standards:S-1, specification:S-3`; a task-round reviewer
returning `both` qualifies it with each listed axis its return covers. A return
supports a carried finding by its ID or by an alias for its own axis. Aliases
never merge different failure conditions:

- Scope: an alias describes this round's returns. Record it only on a finding
  raised or reassessed in this round and only when that axis's return uses it;
  carrying a finding into a later round drops its aliases.
- Form: a raw ID has the ID form above, so brief reviewers to number findings
  that way. The failure condition never contains `; aliases `.
- Uniqueness: each alias names a listed axis, one axis's raw ID names one
  finding, and no alias is another finding's ID. Another axis may reuse the
  same raw ID for a different condition.

The state is `unresolved`, `resolved`, `regression`, or, for P3 only,
`accepted` or `deferred` with its reason in the text. Findings keep their IDs
across rounds, reviewers and resumption, as [review cycles](review-cycles.md)
describes.

Then write `**Coverage:**` with the changed areas each axis covered, the gaps,
the evidence limits and any required specialist or human review still pending.
Name each specialist or provider result, such as a security scan, with the
revision it actually covered; a result for an older head never covers this one.

## Retain reviewer returns

The table, findings and coverage are the coordinator's summary. After them,
retain what each reviewer actually returned, so a reader can check the summary
once the conversation is gone. Write one block per `Reviewers` entry, in the
same order, including failed and replaced reviewers of the round; `Reviewers
none` has no blocks:

- A `### Reviewer return: <label>` heading, then a `| Field | Value |` table
  with the rows `Axis`, `Comparison`, `Requirements`, `Policy`, `Return`,
  `Digest` and `Redactions`, then the return in a fence opened by `~~~text`.
  When a line of the return starts with three or more tildes, lengthen both
  fence lines beyond the longest such run.
- `Axis` matches the entry. `Comparison`, `Requirements` and `Policy`, in the
  result's grammar, are what the return itself names or confirms; when it names
  none, the inputs it was briefed with.
- `Return` is `complete` when the return states its verdict, coverage and
  findings for the axis, `partial` when it stops early or omits any of them,
  and `failed` when it errored, returned nothing usable or exceeded its brief.
- The fence holds the reviewer's own final message, verbatim except for
  redactions. Never substitute a paraphrase, the reviewer's session
  transcript, tool output or runtime metadata. When nothing came back, the
  fence holds one line, `[no return: <reason>]`.
- When the coordinator sends a reviewer a follow-up within the round, such as
  a clarification, a reassessment request or prior findings for a
  replacement, the reply must restate the axis's complete verdict, its
  coverage and every finding with its disposition and evidence. That reply is
  the reviewer's final message and its retained return; a reply missing any
  of them is `partial`.
- Replace credentials, secrets, private paths, host or session identifiers and
  unrelated personal data with `[redacted: <kind>]`, and list them in
  `Redactions` as `<count>: <kind>, <kind>`, or `none`. Change nothing else;
  when a redaction removes evidence a finding needs, say so in the coverage.
- `Digest` is `sha256:` followed by the SHA-256 of the fenced lines, UTF-8 with
  LF line endings and a final newline. It identifies the retained bytes; it is
  not a signature and does not prove who wrote them.

An axis is `incomplete` unless the round has a `complete` return on that axis
whose comparison, requirements and policy equal the result's. Before returning
the result, reconcile it with the returns. Each of these is an error to
correct, not a disposition:

- a summary finding that no return supports;
- a finding that breaks the ID and axis rules above;
- a returned blocker the summary omits.

Task rounds keep their returns in the task evidence only.
Review-work publishes none of this; keeping it beyond the conversation needs an
existing destination the caller is authorized to use.

## Examples

A second final round after one correction:

```markdown
## Review result

| Field | Value |
| --- | --- |
| Work | example-org/example-app#42 |
| Round | final 2 |
| Comparison | base 1111111111111111111111111111111111111111; head 3333333333333333333333333333333333333333; merge-base 1111111111111111111111111111111111111111 |
| Requirements | example-org/example-app#42 at 2026-09-25T10:00Z |
| Policy | example-app@abcdef1234567890abcdef1234567890abcdef12 |
| Standards | satisfied |
| Specification | satisfied |
| Reviewers | standards-reviewer-2: standards, requested opus at default, model unknown (unknown), level high (user-stated); specification-reviewer-2: specification, requested opus at default, model claude-opus-5-5 (self-reported), level high (user-stated) |
| Open findings | P0 0; P1 0; P2 0; P3 0 |

**Findings:**
- F1 (P2, specification, resolved): src/export.ts:40, an empty filter exported every tenant's rows; first final 1, latest final 2
- F2 (P3, standards, accepted): src/export.ts:12, the helper name is vague; accepted because the module owner prefers it; first final 1, latest final 1

**Coverage:** Both axes covered the export handler, its tests and the CI job. No specialist review was required. Neither reviewer exposed its executing level.

### Reviewer return: standards-reviewer-2

| Field | Value |
| --- | --- |
| Axis | standards |
| Comparison | base 1111111111111111111111111111111111111111; head 3333333333333333333333333333333333333333; merge-base 1111111111111111111111111111111111111111 |
| Requirements | example-org/example-app#42 at 2026-09-25T10:00Z |
| Policy | example-app@abcdef1234567890abcdef1234567890abcdef12 |
| Return | complete |
| Digest | sha256:b0d9bdbacf90cd3de2158490ca238515902791546d469b45b8f529ea1bc4b5f0 |
| Redactions | none |

~~~text
Standards review of 333333333333 against base 111111111111, policy example-app@abcdef1234567890abcdef1234567890abcdef12.

Verdict: satisfied.

Blocking findings: none.

P3 observations: none new. F2 is unchanged.

Coverage: src/export.ts, test/export.test.ts and .github/workflows/ci.yml. I read the supplied CI results and ran no tests.
~~~

### Reviewer return: specification-reviewer-2

| Field | Value |
| --- | --- |
| Axis | specification |
| Comparison | base 1111111111111111111111111111111111111111; head 3333333333333333333333333333333333333333; merge-base 1111111111111111111111111111111111111111 |
| Requirements | example-org/example-app#42 at 2026-09-25T10:00Z |
| Policy | example-app@abcdef1234567890abcdef1234567890abcdef12 |
| Return | complete |
| Digest | sha256:e6d81d2404f22efcdb9e4e4153e44c5006ee45fe70753a2074e5d024067b8097 |
| Redactions | none |

~~~text
Specification review of 333333333333 against base 111111111111, requirements example-org/example-app#42 at 2026-09-25T10:00Z.

Verdict: satisfied.

Blocking findings: none. F1 is resolved: test/export.test.ts:31 now rejects an empty filter, and the supplied CI run passed on this head.

P3 observations: none.

Coverage: acceptance criteria 1 to 3 against src/export.ts and its tests. I am claude-opus-5-5.
~~~
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

**Coverage:** Standards covered the whole patch. Specification is incomplete because no authoritative requirement exists, so no specification reviewer ran. The user supplied the patch; no tests were run. The retained return had one credential redacted; the finding does not depend on it.

### Reviewer return: standards-reviewer-1

| Field | Value |
| --- | --- |
| Axis | standards |
| Comparison | patch sha256:4f1c0d2e3b4a5968778695a4b3c2d1e0f0e1d2c3b4a5968778695a4b3c2d1e0f |
| Requirements | none |
| Policy | unknown |
| Return | complete |
| Digest | sha256:fc1fdac78bb4d53d34a268ed61434b200506075abc31bbf144db0573be29fa33 |
| Redactions | 1: credential |

~~~text
Standards review of the supplied patch (sha256:4f1c0d2e3b4a), no written standards policy.

Verdict: action-required.

Blocking findings:
- P1 lib/auth.py:88: `is_valid` compares the expiry with `<=` against a naive local time, so a token that expired an hour ago passes. Failing input: a token with exp = now - 3600 in UTC+1. Log excerpt: AUTH_SECRET=[redacted: credential].

P3 observations: none.

Coverage: the whole patch. I did not run tests; none were supplied. Specification is not assessed on this axis.
~~~
```
