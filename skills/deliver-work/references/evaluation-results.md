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

This checks the known broken/reference outcomes and both recorded proposals.
Deliberate fixture failures are expected by the wrapper, not ignored CI failures.
New trials receive only input files, never recorded proposals or evaluator data.

Input SHA-256 values:

- cases.md: `3501d5169169f6b786d95023ef6998a1fd45712a8936818952abda3705206b0e`
- retry_task.md: `5000c526b9ef0578f28e1fcd3a34168c619b60dae7558bb73482411018bf96a3`
- retry_base.py: `61dc5650064ea4a40c51285f69887db0507bb2d3552162c47dc3856e608a89d5`
- test_retry.py: `e55f351730531410499628260fc891fa3a19562dabe8db3932919beda3ff021b`
- graders.md: `8f7f88d43e337a21b49f984a760deb083f7ab5790c6d5f7002b936115930896c`

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

## Selection conclusion and unsupported evidence

Keep published routing heuristics unchanged. Two simple successes support this
bounded exercise, not claims that Sol is optimal or medium reasoning suffices
for high-impact work. Future critical violations block acceptance until corrected
and reassessed, rather than lowering the rubric to obtain a pass.

A live direct-versus-Sol-with-Astra comparison was unsupported because the
original coordinator's exact Astra identity could not be established. No
replacement advisor was created. Pairing performance, consultation reliability,
relative cost, and superiority remain unverified. Earlier simulated pairing
cases do not fill this gap. Neutral-host discovery, live Jira behavior, and
human-calibrated subjective scoring also remain unverified.

The source delivery supplies GitHub PR/CI/merge evidence in the issue's linked
PR, separate from these simulations. Source CI does not prove the unexercised
capabilities. This bounded issue requires comparison where supported, not an
invented live-pairing success. A future explicit live comparison remains pending
until its runtime prerequisites and authority are satisfied.
