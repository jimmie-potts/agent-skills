# Bounded workflow evaluation, 2026-09-08 UTC

Read when evaluating this workflow or considering evidence for selection changes.
Results cover published planning/delivery source
`22588b494cac646bd6eaa5e2f01b8d439ab6a60e`, including assessment and Sol composition.
They do not establish production reliability.

## Method and reproducible inputs

Two fresh worker contexts received identical six-case workflow inputs and a
retry implementation task. They read entrypoints and selected operating resources
with a supplied simulated canonical-package location. They were excluded from
evaluator answers, reference solution, grader, other trial output, and skill
validation scenarios. This is procedural separation, not filesystem enforcement;
workers reported honoring it.

The input cases/task, evaluator-only rubric, sanitized observed decisions, frozen
grader, broken/reference implementations, and exact returned proposals are under
`tests/fixtures/workflow-evaluation/` in the catalog. Five cases contain failure
traps; one is a clean ready-PR-only control. The code task specifies attempt
bounds, retryable exceptions, validation before effects, results, and final
exception identity. Workers return patches and isolated checks; the coordinator
owns durable writes.

Before grading proposals, the coordinator ran the unchanged grader: the broken
base passed 2/6 methods with three failures and one error from an extra attempt
exhausting the exception list. The reference passed 6/6. Each returned function
was then applied verbatim to its own fixture and graded without test changes.

Reproduce from the repository root after normal environment setup:

```sh
python3 tests/workflow-evaluation-test.py
```

This checks the known broken/reference outcomes and recorded proposals.
Deliberate fixture failures are expected by the wrapper, not ignored CI failures.
New trials receive only input files, never recorded proposals or evaluator data.

Input SHA-256 values:

- cases.md: `3501d5169169f6b786d95023ef6998a1fd45712a8936818952abda3705206b0e`
- retry_task.md: `5000c526b9ef0578f28e1fcd3a34168c619b60dae7558bb73482411018bf96a3`
- retry_base.py: `61dc5650064ea4a40c51285f69887db0507bb2d3552162c47dc3856e608a89d5`
- test_retry.py: `e55f351730531410499628260fc891fa3a19562dabe8db3932919beda3ff021b`
- graders.md: `8f7f88d43e337a21b49f984a760deb083f7ab5790c6d5f7002b936115930896c`
- clarification_case.md: `e6a0a264a1276c25ee7279b82dde14cc18355a54d1496318f3d23d0007f5ecd7`
- clarification_grader.md: `8826910f6b61abdd8e08308e789ce3e949799521f3321c8c2d9e0b263a8e15bb`

## Results and evidence limits

Both worker requests selected gpt-5.6-sol with medium reasoning and fresh
contexts. Host spawn calls succeeded; actual runtime model/effort was not
independently observable. A separate evaluator requested gpt-6-astra/high
inspected the rubric and grader, reran all four code fixtures, and scored the
coordinator's sanitized decision summaries. Its identity was also unverified.
It found no unfair implementation-specific tests and confirmed these results:

| Measure | Trial 1 | Trial 2 |
| --- | --- | --- |
| Workflow cases satisfying rubric | 6/6 | 6/6 |
| Failure traps identified | 5/5 | 5/5 |
| Missed traps | 0/5 | 0/5 |
| False-positive mandatory gates on clean control | 0/1 | 0/1 |
| Critical violations in stated next actions | 0/6 | 0/6 |
| Frozen coding grader methods passing | 6/6 | 6/6 |
| Returned proposals requiring correction | 0/1 | 0/1 |
| Observed completion seconds after common start | 227 | 258 |

Time origin: 02:23:16 UTC before both launches. Measurements include launch
staggering, scheduling, reading, and coordinator collection delay; they are not
comparable model latency. Token/cost telemetry is unknown, not zero. Local Python
was 3.14.4; configured CI uses 3.12. Workflow scores concern intended actions in
six synthetic cases, not executed tracker operations or production defect rates.
The coordinator inspected full responses; the independent evaluator scored their
summaries, not full transcripts. No qualified human calibration was available.
Worker-local red/green checks and prohibited-file avoidance remain reported
evidence; the coordinator/evaluator directly observed the frozen grader outcomes.

Both trials preserved omitted acceptance, dependencies, baseline gates, fresh
reviews, explicit pairing identity, write reconciliation, delivery limits, and
recovery/human acceptance. Both returned identical retry proposals passing 6/6
without correction. Trial 1 rated synthetic retry impact low; trial 2 rated
callback repetition medium. The evaluator judged this assessment framing
variability without a material action difference. Future tasks should name
callback effects and recovery cost; this sample cannot calibrate those ratings.

The grader does not directly test single-attempt boundaries, falsey success,
exception subclasses, or forbidden sleep/network effects. Inspection of both
small proposals found no added effects or contrary special handling. Passing
six methods alone is not exhaustive verification.

## Review-driven coverage correction

Specification review found that the six original cases did not test an unresolved
user-owned requirement. One supplemental archive-retention case now covers both
planning and delivery, with its own withheld rubric and two fresh Sol/medium
requests. Their summaries support 2/2 phase decisions each, with no critical
violations recorded across four opportunities. Both required a user decision before dependent work and
kept independent read-only investigation available. Neither would publish while
questioning. The original six-case inputs, grader and results remain unchanged.
Sanitized observations and assessment variation are in observed-decisions.md.
This was one evaluation-coverage correction from review, not a failed worker
proposal. Worker identity and token/cost telemetry remain unknown. Both responses
were observed within 162 seconds of the common launch origin; these coarse times
do not measure model latency.

A separate evaluator requested Astra/high confirmed those summary-level grades
and independently ran the broken/reference/first paired coding fixtures. It did
not inspect raw responses, worker-local commands or actual tracker effects.
Summary grades therefore do not independently establish full response compliance
or the absence of unrecorded effects. Its runtime identity was unverified.

## Selection conclusion and unsupported evidence

### Live paired coding comparison

After runtime discovery, two fresh Sol/medium requests repeated the same retry
task/base under sol-with-astra. They used the same published operating revision,
Python environment and unchanged six-method grader as the direct trials.
Only the pairing instructions and consultation steps differed for this coding
task. The original Astra/medium coordinator answered approach requests before
dependent implementation and inspected final proposals. It applied both exact
proposals; each same worker then validated its applied file without writes.

| Measure | Paired trial 1 | Paired trial 2 |
| --- | --- | --- |
| Approach exchanges with original advisor | 1 | 1 |
| Final advisor inspection and worker validation | Completed | Completed |
| Frozen coding grader methods passing | 6/6 | 6/6 |
| Returned proposals requiring correction | 0/1 | 0/1 |
| Observed seconds to proposal | 281 | 135 |
| Observed seconds through applied-file validation | 342 | 177 |

Both direct and both paired proposals passed the same coding grader without
correction. Consultation messages and coordinator-run outcomes were observed
live; sanitized summaries are in observed-decisions.md. Worker-local red/green
checks remain reported evidence. Workers did not receive held-out answers or
other outputs before returning proposals; executing the grader was authorized
only for final applied-file validation.

The advisor had already seen direct outputs and the grader, so this was not a
blind comparison. Direct workers also handled six workflow cases, whereas paired
workers handled coding only. Elapsed times include launch, scheduling, advice,
and collection delays and cannot support relative speed claims. Token/cost is
unknown. This tiny task exercises the consultation protocol and compares coding
outcomes, not model quality, production reliability, or high-complexity work.

### Policy and remaining gaps

Keep published routing heuristics unchanged. These simple successes support this
bounded exercise, not claims that Sol is optimal or medium reasoning suffices
for high-impact work. Future critical violations block acceptance until corrected
and reassessed, rather than lowering the rubric to obtain a pass.

The original coordinator's identity was initially unknown. A later read-only
lookup of authoritative current-thread host turn metadata established
gpt-6-astra with medium reasoning, enabling the live pairing trials described
below. No replacement advisor was created. Worker identities remain unverified.
Neutral-host discovery, live Jira behavior, and human-calibrated subjective
scoring remain unverified.

The source delivery supplies GitHub PR/CI/merge evidence in the issue's linked
PR, separate from these simulations. Source CI does not prove the unexercised
capabilities. The bounded results do not establish production reliability,
relative cost, a superior strategy, or appropriate settings for complex work.
