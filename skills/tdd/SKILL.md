---
name: tdd
description: Develop a bug fix or new behavior through focused red, green, and refactor cycles. Use when the user explicitly asks for TDD, a failing test, or a regression test, or an authorized workflow explicitly composes TDD.
---

# Test-driven development

Make the intended behavior executable before changing production code. For a
bug, demonstrate the broken contract. For a feature, select one accepted
scenario from the issue or specification and demonstrate the missing behavior.

## Authority boundary

This skill grants no authority beyond the requested implementation. Follow the user's
scope, repository instructions, and approval policy before modifying code,
installing dependencies, accessing remote systems, or running commands. Do not
run untrusted code. Preserve unrelated changes.

## Decide whether a failing test is practical

Use the closest existing test level that can observe the behavior: unit, component,
integration, or a focused regression test. Do not build a broad harness merely
to satisfy the workflow.

A new failing test may be impractical when it requires production-only state,
slow end-to-end infrastructure, brittle timing, mostly mocked behavior, vague
reproduction steps, or large unrelated fixture changes. In that case, explain
the limitation before editing production code and choose the closest executable
check, such as a targeted script, reproduction command, browser scenario, log
assertion, or snapshot comparison.

## Red, green, refactor

1. Define the intended behavior, current behavior, affected path, and smallest
   observable reproduction.
2. Add the smallest test for that scenario. Test the contract, not
   the current implementation's internal structure.
3. Run the new test before the fix. Confirm it fails for the expected reason.
   If it passes or fails elsewhere, correct the test or reproduction first.
4. Make the smallest production change that satisfies the intended behavior
   while preserving nearby contracts.
5. Run the same regression test and confirm it passes.
6. Refactor when useful while keeping the test green. Repeat with the next
   accepted scenario; do not write every test ahead of the whole implementation.
7. Run relevant adjacent tests, type checks, lint, or scenario checks in
   proportion to the change's risk.

Keep the before-fix failure evidence. Do not recreate or claim a red result
after production code has already changed unless version history or an isolated
reproduction genuinely demonstrates it.

## Guardrails

- Do not change a test merely to make incorrect behavior pass.
- Do not weaken assertions unless the expected contract changed and the task
  authorizes that change.
- Keep the regression test focused. Avoid unrelated cleanup or coverage work.
- Prefer no new test over a test dominated by mocks, timing, or global state.
- Make flaky reproductions deterministic when practical and name the signal the
  test locks down.
- Address the selected scenario first. Treat sibling cases as separate scope
  unless they are required for the same accepted contract.

## Return

Report the exact test or check that failed before the fix and its failure
reason. Report the same check passing afterward, plus nearby validation. If a
red test was impractical, state why and name the substitute regression evidence.

Apply the `unslop` skill to the final explanation without changing commands, test names,
failures, logs, identifiers, or verification results.
