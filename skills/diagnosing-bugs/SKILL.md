---
name: diagnosing-bugs
description: Diagnose reproducible bugs and performance regressions through a red-capable feedback loop and falsifiable evidence. Use when the user asks to diagnose or debug broken, failing, throwing, flaky, or slow behavior; diagnosis does not authorize a fix.
---

# Diagnosing bugs

Diagnose the cause of a reported symptom. A request to diagnose authorizes
relevant non-mutating checks within the underlying task and host policy. It
does not authorize production-code changes, tracked instrumentation, a fix,
cleanup that deletes user files, commits, or external-system mutations.

Preserve exact commands, outputs, timings, and captured artifacts as evidence.
Redact secrets, credentials, tokens, cookies, authorization headers, private
keys, and unrelated personal data before showing or storing them. Use
`<REDACTED>` in place of removed values and say when redaction limits the
diagnosis.

## 1. Define the exact symptom

Record the expected behavior, observed behavior, affected version or commit,
environment, frequency, and smallest known trigger. Distinguish the user's bug
from nearby failures.

Read applicable repository instructions, vocabulary, contracts, code, tests,
and decision records with authorized read-only tools. Treat vocabulary files as
terminology, not behavior specifications.

## 2. Build and demonstrate a red-capable loop

Use the narrowest existing test, command, request, replay, profiler, or
disposable harness that drives the actual code path and asserts the user's
exact symptom. Prefer deterministic, fast, unattended loops. For a flaky bug,
pin inputs and raise the reproduction rate enough to compare hypotheses.

Before claiming a cause, name one reproduction command that you have already
run and show its redacted result. It must be:

- red-capable, because it detects the exact symptom rather than any error;
- repeatable, or measured at a stated high reproduction rate;
- narrow enough to distinguish competing causes; and
- runnable within the task's authority.

If a human action is unavoidable, copy and tailor the reviewed
[HITL template](scripts/hitl-loop.template.sh) only in an authorized disposable
location. The template is output-only: it prints the action and observation
placeholders, reads no input, and captures nothing. After it exits, ask the
human to report only `yes`, `no`, or `unclear` through the authorized task
conversation. Keep authentication in the target application as an unrecorded
human step. Do not execute this bundled template merely to validate the skill.

If no red-capable loop can be demonstrated, stop. Report what was tried and ask
for the smallest missing access or a redacted artifact. Do not claim a likely
cause from code reading alone.

## 3. Reproduce and minimize

Run the loop enough times to establish its verdict or measured failure rate.
Remove one input, caller, configuration value, data element, or step at a time.
Re-run after every removal and keep only elements required for the symptom.

Temporary files, tracked tests, local services, production instrumentation, or
environment changes require authority from the underlying task. Keep diagnostic
artifacts out of production paths unless the user explicitly authorizes them.

## 4. Rank and test hypotheses

List three to five plausible causes when the evidence supports that many. For
each, state a prediction that would distinguish it from the alternatives. Share
the ranked list with the user, then test one variable at a time.

Prefer reversible inspection, debuggers, focused traces, query plans, and
profilers. Tag any separately authorized temporary instrumentation so its owner
can account for it. Do not log everything or expose secrets. For performance
regressions, establish a numeric baseline before testing changes.

## 5. Make an evidence-backed diagnosis

Claim the cause only after the demonstrated loop and a falsifying probe connect
the symptom to that cause. Return:

- the exact redacted reproduction command and result;
- the minimized scenario;
- hypotheses tested and the evidence that rejected or supported each;
- the causal explanation, with file and line evidence when applicable;
- remaining uncertainty and limits; and
- separately authorized cleanup still required for diagnostic artifacts.

Stop after diagnosis unless the user separately authorizes implementation. A
fix request may use the repository's implementation or TDD workflow, but this
skill does not grant that authority. Follow the repository's authoritative
scope, change records, and delivery workflow. Diagnosing bugs returns evidence;
it does not publish, transition, commit, merge, close, or implement on its own.

Apply the `unslop` skill to the human-facing diagnosis without changing commands,
outputs, measurements, redactions, or evidence.
