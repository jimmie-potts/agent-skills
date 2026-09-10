# Native Codex worker qualification

Policy tested: `776fe91541f5b28fde08259b5b7ef72c2dc62c31`, the completed #30/#31
implementation. These trials exercise request selection, communication,
resumption, correction and handoff on a small synthetic task. They do not measure
production reliability, relative model quality, latency advantage or savings.

## Preflight and boundaries

The live collaboration schema exposed explicit model and reasoning controls,
fresh contexts, parent messaging, same-worker follow-up and interruption.
Requested trial configurations were Luna/low, Terra/medium and Sol/medium.
Current-thread host turn metadata identified the original coordinator as
`gpt-6-astra` at `medium`; it remained unchanged for both advisory attempts.
This is host-recorded session evidence, not an independent backend attestation.
The workers reported model and effort as unexposed. Their requested selections
must not be relabeled as verified runtime identities.

Execution used the existing Codex Pro subscription session, with no paid API
calls, purchased credits, account changes or personal skill installation.
Attributable token usage, dollar costs and per-worker subscription consumption
were unavailable. Coordination, reviews, consultations, retries and all attempts
belong in total-work accounting when attributable; unknown does not mean zero.

Exactly three native trial contexts were started. Workers were instructed to make no durable
writes and returned findings or proposed source. The coordinator alone
applied files in an isolated synthetic workspace. No worker spawned another
agent. Candidate skills were loaded by explicit paths from the frozen revision;
this does not establish neutral-host or installed-skill discovery. Independent
source reviewers are a separate delivery gate, not additional trial workers.

## Frozen fixture and checker

Reuse the existing synthetic retry fixture and independent outcome checker from
the frozen policy revision. The contract assumes integer counts: reject counts
below one before invoking the operation; enforce the total-attempt cap; return
first success including the final allowed attempt; retry only RuntimeError;
propagate other exceptions immediately; preserve final RuntimeError identity.

The coordinator verified the known broken fixture before applying any proposal:
2/6 tests passed, with three failures and one error. The reference passed 6/6.
Workers received the contract and synthetic candidate only, with explicit
instructions excluding reference solutions, graders and recorded outputs.
Worker in-memory tests are reported evidence; independent checker outcomes below
were executed by the coordinator.

| Frozen input | SHA256 |
| --- | --- |
| retry_base.py | 61dc5650064ea4a40c51285f69887db0507bb2d3552162c47dc3856e608a89d5 |
| retry_reference.py | fa9010d15c659de65952540f3a54d2a16e8629a99d63fabe56200e9fdbe7b765 |
| test_retry.py | e55f351730531410499628260fc891fa3a19562dabe8db3932919beda3ff021b |

## Predeclared injected failures

Before starting the trial workers, the coordinator recorded a two-stage
injection plan. If Terra's initial proposal passed, validate and preserve that
native result, then broaden its catch to `Exception` in the synthetic candidate.
Give the resulting failure evidence back to the same worker for one guided
correction. If that correction passed, preserve its native result and repeat
the injection. Use these two synthetic inadequate outcomes to exercise the
initial-plus-one-correction threshold and a fresh Sol promotion branch.

Both Terra proposals passed. Both injected candidates failed only
`test_nonretryable_propagates_once`, with three calls instead of one. These are
coordinator-injected faults, not spontaneous Terra capability failures. The
promotion was a predeclared lifecycle exercise, not evidence that Sol was needed
or more capable. No additional correction at Terra/medium was attempted.

## Observed decisions and lifecycle

Luna returned the correct function/signature and source lines. It identified
three maximum calls for a limit of two, the broad exception catch, and one call
for zero. The coordinator confirmed that the fixture hash was unchanged after
the scout. No write, execution or advisor loop was observed for that worker.

Terra sent its approach through parent messaging and ended its turn awaiting
advice. The coordinator resumed that retained worker with `followup_task`, then
applied and independently checked its exact proposed source. The first final
review supplied the native pass and first injection failure. The same worker
received the single guided correction, proposed the minimal repair and requested
another final review. After the second native pass and injection, the coordinator
answered final review and ended the assignment. Terra acknowledged three
completed consultations: approach, initial final review, correction final review.
The interruption tool confirmed its prior state was completed before Sol began;
this was not an observed cancellation of a running worker.

The fresh Sol brief transferred the candidate and hash, source/policy revision,
full acceptance contract, failed checker outcome, native/injected attempt
history, correction count, settings, unresolved question, unchanged permissions
and write ownership. It retained the same original Astra advisor and required
new approach and final-review consultations. The new context was never reported
as a resumed Terra worker.

Sol sent an approach consultation, received approval through parent messaging,
and proposed the same minimal repair. Its first in-memory validation command
had a shell-quoting SyntaxError before the check executed; a corrected command
passed. This was a reported local command repair, not an inadequate returned
implementation or an additional guided correction. The coordinator applied the
exact proposal and the frozen checker passed 6/6. No fault was injected into
Sol's result. The coordinator supplied that acceptance evidence in its final
review response. Sol had two consultations and no guided implementation correction.

## Outcome evidence

| Stage | Origin | Checker outcome | Recorded artifact |
| --- | --- | --- | --- |
| Terra initial | Native proposal | 6/6 pass | retry_native_terra.py |
| After initial proposal | Coordinator injection | 5/6 pass; nonretryable propagation fails | retry_native_injected.py |
| Terra guided correction | Native proposal | 6/6 pass | retry_native_terra.py, identical bytes |
| After correction | Coordinator injection | 5/6 pass; same failure | retry_native_injected.py, identical bytes |
| Sol promoted attempt | Native proposal | 6/6 pass | retry_native_sol.py |

All three native implementation results have SHA256
`0aabdbba7be1735d63f7a76eca4df7002d6421b1aad33754f068b217c13944bd`.
Both injected results have SHA256
`1e979ea73297288c30cb45518f412502524e14708063701371c97167b59f0302`.
Identical final code is expected for this handed-off one-clause repair; it does
not make the trials independent quality comparisons. The structured receipt is
`native-qualification-receipt.json` in this directory.

Reproduce artifact acceptance without launching models, from the repository root:

```bash
python3 tests/workflow-evaluation-test.py
```

That check replays the six frozen contract cases against the recorded proposals
and confirms the injected candidate fails the named negative case. Replay is
structural/executable artifact evidence, not a new live worker trial. Existing
historical trial fixtures and reference/checker bytes remain unchanged.

## Limits and delivery acceptance

Native request selection, parent messages, same-worker follow-up, final-review
responses, completed-worker state verification and fresh-context handoff were
observed. Running-worker cancellation was not exercised. Per-worker runtime
model and reasoning remained unverified; selection requests and worker-reported
unknowns remain separate. No monetary savings or relative speed claim is made.
Native Claude lifecycle acceptance remains unverified because no suitable
separately authorized Claude host was used. This does not erase Codex evidence.

The instruction changes were qualified at the frozen policy revision above.
The issue's PR records separate full local checks, independent Standards and
Specification reviews, current-head hosted CI, guarded merge and post-merge
verification for these committed artifacts. Those delivery gates cannot prove
unobserved runtime identity, installed-skill discovery or Claude behavior.
