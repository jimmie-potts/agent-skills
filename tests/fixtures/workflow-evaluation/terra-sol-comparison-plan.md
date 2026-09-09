# Terra versus Sol worker comparison plan

Plan only. Running it spends tokens and needs the user's authorization for each
phase. It decides three Codex adapter questions with measured evidence:

1. Which assigned worker is the default for scoped implementation: Terra at
   `high` or Sol at `medium`.
2. Whether the sol-with-astra pairing should accept Terra as its worker.
3. Whether Astra implementing directly at a lower reasoning setting beats both
   on this task class.

The decision measure is cost per completed task at a pass rate no worse than
the status quo, Sol at `medium`. Elapsed time is recorded but never decides.
Follow Anthropic's order: sweep effort on the current worker first, then the
next model alone, then pairings only if a gap remains.

## Why the current fixtures cannot answer this

The retry task in this directory saturates. Two direct Sol/medium trials and
two paired Sol/medium trials all passed 6/6 without correction, and their
elapsed times varied by two to one for identical outcomes. A task every arm
passes cannot rank arms, and token cost was unknown in every prior trial.
Two things must exist before the first comparison run: a task with headroom
and a cost measurement.

## Prerequisites

Record each item in the results section before any trial. A missing item that
the plan marks required blocks the phase that depends on it.

- Coordinator identity (required). Verify `gpt-6-astra` from current-thread
  host turn metadata, as in evaluation-results.md. Spawn options are not
  identity.
- Spawn identifiers (required). Read the host model list and confirm
  `gpt-5.6-sol` and `gpt-5.6-terra`. Sol was verified in earlier spawns; the
  maintainer supplied Terra's identifier, and the first successful Terra spawn
  records it as verified. Confirm Luna is absent from spawnable subagents and
  leave it out.
- Reasoning enum (required). Record the values the host's spawn schema lists.
  Documented spawn values are `low`, `medium`, and `high`; `xhigh` and `max`
  exist as session settings and are unverified for spawns. Use `medium` and
  `high` for workers and `low` only for the optional scout task. If the spawn
  schema accepts `xhigh`, add it to the Sol effort sweep as A3b rather than
  assuming it.
- Cost telemetry (required for the cost decision). Determine whether the host
  exposes per-agent input and output token counts, and whether coordinator
  turns are attributable. If it does not, the plan still runs, records worker
  turns and tool calls as proxies, and reports "cost undecided" rather than
  ranking arms by proxies or elapsed time.
- Operating revision (required). Pin one published catalog commit that contains
  the current Codex adapter and both pairing skills. Every arm reads the same
  revision.
- Isolation (required). Fresh contexts with `fork_turns="none"`. Workers never
  receive graders, reference solutions, other arms' outputs, evaluation results,
  or skill validation scenarios. Procedural separation, reported by workers, as
  before.
- Harder task (required, authored before phase 1). See the next section.

## Tasks

| Task | Purpose | Status |
| --- | --- | --- |
| T1 retry | Continuity control with the existing 6-method grader | Exists |
| T2 bounded coding with headroom | Rank arms on pass rate and cost | To author |
| T3 unresolved requirement | Measure whether a worker stops and asks or guesses | Exists as clarification_case.md |
| T4 read-only scout (optional) | Compare Sol at `low` and Terra at `low` on locating and tracing | To author if phase 3 needs it |

T2 authoring rules, in the style of the retry fixtures:

- One Python module of at most about 80 lines with a written contract, for
  example a bounded token bucket with monotonic time injection, an ordered
  dependency resolver with cycle detection and a specified error contract, or
  an LRU cache with TTL and eviction order guarantees.
- A base file with at least four planted contract defects and a reference
  file that passes.
- A hidden grader of 8 to 12 methods covering edge cases the contract implies
  but does not spell out, so that a careful reading beats a literal one.
- Before any trial, run the grader on the base and reference exactly as
  evaluation-results.md did for retry, and record the SHA-256 of every input.
- Register the task in workflow-evaluation-test.py the same way retry is.
- Saturation guard: if every arm in phase 1 passes T2 fully, T2 is too easy.
  Author a harder T2 before drawing any conclusion.

## Arms

| Arm | Model and setting | Strategy | Notes |
| --- | --- | --- | --- |
| A1 | Astra at `medium`, then `low` if supported | Direct implementation | Run as a fresh top-level Astra session with the task, not as a subagent. This is the baseline every other arm must beat. |
| A2 | Sol at `medium` | Assigned worker | Status quo. Two T1 results exist. |
| A3 | Sol at `high` | Assigned worker | Effort sweep on the current worker. |
| A4 | Terra at `high` | Assigned worker | The recommended scoped-implementation worker. |
| A5 | Terra at `medium` | Assigned worker | Effort sweep on Terra. |
| A6 | Sol at `medium` with Astra advisor | Advisory pairing | Status quo pairing. Two T1 results exist. |
| A7 | Terra at `high` with Astra advisor | Advisory pairing | Experimental brief only. Do not change sol-with-astra to run it; give the worker the same consultation protocol in a labeled trial brief. |

Sample size is three fresh runs per arm per task. Prior trials used two, which
cannot separate variance from effect.

## Phases and stop rules

1. Baseline and effort sweep on T1, T2, T3: A1, A2, A3. If A1 at the lower
   setting matches A2's pass rate at lower cost per completed task, record
   that direct Astra implementation is the default for this task class and
   stop. The adapter rows for bounded coding then point to direct
   implementation, and the worker question is moot for this class.
2. Next model alone on T1, T2, T3: A4, A5. Compare against A2 and A3.
3. Pairings on T2 and T3 only, and only if phase 2 leaves a gap between the
   best worker alone and A1: A6, A7. Skip this phase if no gap remains; a
   pairing exists to close a capability gap.
4. Optional scouts on T4: Sol at `low` against Terra at `low`, only if the
   adapter's scout row needs evidence.

## Measures per run

- Grader methods passing over the total, and completed: all methods pass
  without any correction round.
- Correction rounds: the number of returned results the coordinator sent back.
- Critical violations: unauthorized writes, reading a prohibited file, an
  invented identity, or a false completion claim. Any critical violation
  disqualifies that arm from becoming a default until corrected and rerun.
- T3 outcome: stopped and asked, or guessed a default. Guessing counts as a
  failed run.
- Consultations, pairing arms only: count, whether both mandatory
  consultations happened, and whether advice changed the approach. Two to
  four per task is the expected band; consulting on nearly every decision
  marks the arm as not paying.
- Cost: host-reported tokens per agent, including advisor and coordinator
  tokens for pairing arms. Cost per completed task is total cost across an
  arm's runs divided by its completed runs, so failures and corrections are
  paid for. If telemetry is absent, record turns and tool calls and mark the
  cost measure undecided.
- Identity: requested setting and the model the worker reports from host
  metadata, recorded separately. Unverified is acceptable and disclosed; a
  verified mismatch voids the run.
- Elapsed seconds from a common origin, recorded for completeness only.

## Decision rules

- Default assigned worker: among arms whose pass rate on T2 and T3 is at least
  A2's, pick the lowest cost per completed task. A tie keeps A2.
- Pairing worker: accept Terra only if A7 matches or beats A6 on pass rate for
  T2 and T3, stays inside the consultation band, and costs less per completed
  task. Otherwise sol-with-astra keeps Sol fixed and the adapter says so.
- Direct baseline: if A1 wins on cost per completed task at equal pass rate,
  the adapter rows for this task class point to direct implementation.
- No cost telemetry: report pass rates and consultation counts, state that
  cost is undecided, and change no adapter default.
- These are bounded synthetic tasks. A result changes adapter defaults for
  bounded coding and unresolved-requirement handling only, not for
  high-impact or high-complexity rows.

## Recording

Add a dated section to skills/deliver-work/references/evaluation-results.md
with prerequisites, arms, per-run measures, and decisions. Add sanitized
decisions to observed-decisions.md. Keep exact returned proposals as fixture
files registered in workflow-evaluation-test.py, following the retry naming.
Record input SHA-256 values, requested and reported identities, and the cost
telemetry source. Never infer cost from elapsed time, and never loosen a grader
to pass a proposal.

## Follow-on for Claude Code

The same tasks, arms, and rules apply to worker-with-fable with Fable as A1,
Sonnet and Opus as workers, and Haiku on T4. Run it only in a session that
exposes the resumption tool, because the pairing arms cannot complete without
it.
