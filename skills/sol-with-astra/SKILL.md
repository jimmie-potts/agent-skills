---
name: sol-with-astra
description: Delegate a task to Sol with the original Astra agent as its advisor in Codex. Use when explicitly invoked, requested by the user, or deliberately composed by deliver-work or plan-work after assessment; do not select for ordinary delegation or on hosts without Codex collaboration tools.
---

# Sol with Astra

Keep the original Astra agent as coordinator and advisor. Give one Sol worker
responsibility for implementation and validation within the user's task. Sol
consults that same Astra agent rather than creating a separate advisor.

## Establish the pairing

When composed by deliver-work, retain its assessment, selected worker reasoning,
and coordinator-only write ownership. Read that workflow's selection reference
as directed by its coordinator; do not invoke a second delivery workflow. Its
optional-pairing fallback does not change this skill's fixed model identities.
When composed by plan-work, the pairing is read-only: Sol investigates and
proposes, and neither agent implements, publishes, or updates a tracker.

Verify from host-provided runtime evidence that the current coordinator is
`gpt-6-astra`, that `gpt-5.6-sol` can be selected, and that the worker can
communicate with its parent. Do not infer identity from a persona prompt or
from the list of models available for spawning. If identity or capabilities
cannot be established, report the gap before delegating. Do not silently
substitute models or claim that a requested model was actually used without
runtime evidence.

For Codex collaboration tools, read [the Codex adapter](references/codex.md)
before spawning or messaging. On another host, use only verified equivalent
model selection and parent communication capabilities. Report an unsupported
pairing without changing host configuration or installing tools. On a Claude
Code host, the worker-with-fable pairing applies instead of this skill.

Preserve the underlying task's scope, mode, permissions, and ownership rules.
Planning-only work stays read-only. This skill grants no new publication,
merge, installation, or external-action authority. If another applicable
workflow reserves durable writes for the coordinator, Sol returns proposed
patches and evidence and Astra applies them. Otherwise, assign Sol the scoped
implementation writes and avoid concurrent edits to its files.

## Delegate and consult

Give Sol a self-contained brief with:

- the requested outcome, relevant source material, and acceptance criteria;
- workspace, current revision, applicable instructions, and write ownership;
- current mode, permissions, constraints, and required validation;
- the original Astra agent's address and the consultation protocol below.

Pass these instructions and the applicable host adapter to Sol explicitly.
Do not assume it inherited the conversation or loaded this skill. Ask Sol to
report its actual model identity when the host exposes it, and distinguish an
unverified identity from a verified mismatch. A mismatch stops this pairing;
an unverified worker identity must be disclosed rather than reported as proven.

Sol sends an approach proposal before substantial implementation, after any
necessary bounded discovery. Astra reviews it against the task and returns
concrete direction. Sol then implements and validates, consulting again when
blocked or when consequential uncertainty affects correctness, scope, or the
approach. Routine choices do not require a new checkpoint.

Each consultation names the decision needed, relevant evidence, Sol's
recommended next step, and which work depends on the answer. Sol pauses that
dependent work until Astra responds and may continue independent authorized
work. Advice cannot replace missing user authority. Astra brings user-owned
decisions back to the user while continuing unaffected work.

Keep Astra available to receive and answer consultations. Astra can inspect
relevant sources and prepare review while Sol works, without duplicating Sol's
implementation. Reuse the same worker for corrections and further questions;
do not recursively delegate the task or create another Astra advisor.

## Review and finish

Sol returns the result or proposed patch, changed files, actual validation
commands and outcomes, unresolved limitations, and any decision still needed.
Astra inspects the result against the acceptance criteria and evidence. Return
actionable corrections to Sol when needed and review the corrected result.
If work is blocked, report the concrete blocker instead of treating it as done.

Keep the coordinating turn active until the worker's result and consultations
are resolved or a blocker requires user input. Astra gives the final user
response with the outcome, validation, and remaining limitations. Do not count
this advisor review as an independent review required by another workflow.

When evaluating this skill, exercise [the validation scenarios](references/validation-scenarios.md).
Separate simulated behavior, actual host discovery, and live model execution
in the reported evidence.
