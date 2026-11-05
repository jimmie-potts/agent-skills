# CI failure triage

Adds evidence rules for a failed, flaky or intermittent CI job, workflow or
check. The reproduction requirement, reporting and authority boundary in
`SKILL.md` still apply. The owning repository's retry and release rules decide
what a retry may do and what it can establish; read them.

## 1. Account for every attempt

Start from the exact occurrence named. Read its revision and tree, event, run,
original attempt, failed job, failed step and runner. Then read every later
attempt and every other run of the same tree, following all pages of runs, jobs
and logs. A new commit with an unchanged tree, such as an empty commit, retries
the same candidate and belongs in the same account.

Keep one row per attempt: revision, tree, event, attempt, job outcomes, first
failing step and log availability.

- The first failure stays. A later attempt never replaces it.
- Cancelled and incomplete attempts stay, with no test verdict.
- Missing or expired logs read `unknown`, never passed.
- Name what you could not read, such as pages not fetched or retention limits.

Search open and completed issues and pull requests for the test, step and
mechanism. If a fix exists, check whether the failing revision contained it.
Point to a matching item instead of proposing another.

## 2. Classify each attempt before explaining it

Classification comes from recorded evidence and needs no reproduction loop. A
claim about why it happened still needs the loop and falsifying probe from
`SKILL.md`. Classify attempts separately; do not assume they share a cause.

| Class | Recorded evidence | What to establish next |
| --- | --- | --- |
| Test assertion | A named assertion reports its expected and actual values | Product defect or observation timing; continue at step 4 |
| Setup failure | A step before the tests failed: install, pull, provisioning, service start | Nothing about tests that never ran; what the step depended on |
| Aggregate timeout | A job or step stopped at its time budget with no failed assertion | What consumed the budget, from step and test durations against passing attempts. The last test running is not thereby the cause |
| Cancellation or lost runner | A newer push, a person, a fail-fast rule or runner loss stopped the run | Which one, and that no test verdict exists |
| Selection omission | A required check was skipped or never selected | The selection rule against the changed files. Skipped is not passed |
| Artifact binding | Every job reads green but the overall result fails or is incomplete, or a release step lacks an artifact from the current attempt | The binding rule, and whether this attempt produced its own artifact. A partial rerun can copy earlier job results without one. This is neither a flake nor a test failure; keep the rule intact |
| Evidence gap | Missing logs or metadata leave no class supported | `unknown`, and what record would settle it |

## 3. State counts with their limits

A later green attempt does not establish a cause. Report same-tree recovery as
evidence that the failure did not recur under those conditions; it does not
prove flakiness and does not clear the product.

Give numerator, denominator, time window and pages read for every rate. A
workflow failure percentage is not a test-flake rate: it counts every cause in
every job. A test-flake rate counts one test's failures over that test's
recorded executions, and it stays unknown when those records do not exist.

## 4. Separate timing causes with a discriminating probe

For each deadline and worker on the failing path, name the clock that drives
it: wall time, a harness or test-controlled clock, or another scheduler. Then
compare predictions:

| Hypothesis | Prediction |
| --- | --- |
| Async-observation race | The effect completes correctly but the assertion reads first. Delaying the effect reproduces the failure; waiting on explicit completion evidence removes it with no product change |
| Mixed clocks | A deadline on one clock expires while a worker on another is still within its normal duration. Delaying only the worker reproduces the failure, and the deadline's real duration differs from its nominal one |
| Product failure | The wrong result persists after the effect completes under controlled timing, and the assertion states required behavior |
| Missing headroom | A real-time bound sits within measured normal duration, and no ordering defect appears under controlled delay |

Prefer bounded delay injection, explicit completion evidence and controlled
clock progression. Load alone is weak evidence: a passing load loop is
inconclusive if the load also slows the test's clock. A probe discriminates only
when its verdict differs between the conditions it compares: broken and fixed
code, or a controlled delay and its control. Replace a probe that gives both the
same verdict.

Injected delay and temporary edits need the authority `SKILL.md` step 3
describes. Without it, propose the probe and report it as not run.

## 5. Propose repairs without weakening protection

- Keep each assertion's meaning and every finite bound. A wider bound needs the
  measurement that justifies it.
- Name a negative control that injects the protected defect, and say whether it
  has been shown to fail.
- Propose a shared helper only when the same proven mechanism occurs at multiple
  callers. A site found by reading alone is a candidate, not a confirmed defect.
- Word a rerun as a recommendation for whoever holds that authority, and say
  what a green result would and would not show.

## 6. Report

Add to the diagnosis return: the attempt account, each attempt's class, counts
with limits, each probe's verdict on each condition it compared, and a cause
status of `proven` or `unresolved`. A class can stand on its records while the
cause stays open. Without discriminating evidence, report the cause `unresolved`
with the leading hypotheses and the next probe. "Probably flaky" is not a result.
