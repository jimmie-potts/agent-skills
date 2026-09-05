---
name: prototype
description: Explicitly build a bounded experiment or functional delivery slice to answer one concrete logic, state-model, or UI question. Use only when the user directly invokes prototype and authorizes the needed artifact scope.
---

# Prototype

Answer one concrete question with a runnable artifact. Do not infer a vague
question from nearby code. If the question cannot be stated as an observable
result, resolve it before writing.

Classify the requested result before work begins:

- **Disposable experiment:** isolated code used to learn, then retained or
  discarded only through a separately authorized decision.
- **Functional delivery slice:** the smallest production-quality behavior that
  answers the question and satisfies its accepted tests and error handling.

An explicit invocation does not itself grant filesystem, dependency-install,
server-start, browser, Git, tracker, production-route, or publication authority.
Use only the locations and actions authorized by the underlying request.

## Choose the branch

Read [the logic reference](references/logic.md) when the question concerns
business logic, state transitions, invariants, or data shape. Read [the UI
reference](references/ui.md) when the question concerns layout, information
hierarchy, or interaction design. If both matter, state which question each
artifact answers instead of blending them into one vague prototype.

## Bound the artifact

For a disposable experiment:

- require an explicitly authorized isolated destination;
- mark the artifact and its limitations as disposable;
- avoid real mutations, credentials, production data, and production routes;
- keep it outside tracked or production paths unless the user explicitly
  authorizes that exact placement; and
- verify only what is needed to answer the stated question, while reporting
  untested behavior and limits.

For a functional delivery slice:

- use only the production paths authorized by the implementation request;
- define observable acceptance behavior before editing;
- follow repository architecture, tests, error handling, security, and quality
  gates for that accepted behavior; and
- leave no unfinished, untested, or prototype-only code in production paths.

Do not automatically create a branch, commit, issue update, tracked file,
production route, or browser session. Do not promote a disposable experiment
into production. Promotion is a separate implementation decision with its own
authority and verification.

## Return the answer

Report the concrete question, classification, authorized location, how to run
the artifact, observed result, evidence, limitations, and disposition still
requiring the user's decision. Do not imply that a disposable result is
production-ready.

Follow the repository's authoritative scope, change records, and delivery
workflow. Prototype does not publish, transition, commit, merge, close, or
change external systems on its own.

Apply the `unslop` skill to human-facing labels and the result summary without changing
code, commands, measurements, acceptance criteria, or authority boundaries.
