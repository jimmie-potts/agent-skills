---
name: worker-with-fable
description: Delegate a task to a Haiku, Sonnet, or Opus worker with the original Fable agent as its advisor in Claude Code. Use when explicitly invoked, requested by the user, or deliberately composed by deliver-work or plan-work after assessment; do not select for ordinary delegation or on hosts without Claude Code subagent tools.
---

# Worker with Fable

Keep the original Fable agent as coordinator and advisor. Give one lower-cost
worker responsibility for implementation and validation within the user's task.
The worker consults that same Fable agent rather than creating a separate
advisor. This is the advisor pattern in Anthropic's published model guidance:
the worker performs most turns, and Fable supplies approach, blocker, and
final-review judgment.

## Establish the pairing

When composed by deliver-work, retain its assessment, selected worker tier and
reasoning, and coordinator-only write ownership. Read that workflow's selection
reference as directed by its coordinator; do not invoke a second delivery
workflow. When composed by plan-work, the pairing is read-only: the worker
investigates and proposes, and neither agent implements, publishes, or updates
a tracker. An optional-pairing fallback in either workflow does not change this
skill's fixed advisor identity.

Verify from host-provided runtime evidence that the current coordinator is
Claude Fable 5.1, that the host can spawn a subagent with an explicit worker
model, and that the coordinator can resume that same subagent with its context
intact. Do not infer identity from a persona prompt or from the list of models
available for spawning. If identity or capabilities cannot be established,
report the gap before delegating. Do not silently substitute models or claim
that a requested model was actually used without runtime evidence.

Select the worker tier before spawning. Read [worker tiers](references/worker-tiers.md)
for the tiers, what each may decide alone, and when not to pair at all. An
explicitly requested worker model has no fallback. A worker on Fable is not a
pairing; implement directly instead.

For Claude Code subagent tools, read [the Claude Code adapter](references/claude-code.md)
before spawning or resuming a worker. On another host, use only verified
equivalent model selection and worker resumption capabilities. Report an
unsupported pairing without changing host configuration or installing tools.
On a Codex host, the sol-with-astra pairing applies instead of this skill.

Preserve the underlying task's scope, mode, permissions, and ownership rules.
Planning-only work stays read-only. This skill grants no new publication,
merge, installation, or external-action authority. If another applicable
workflow reserves durable writes for the coordinator, the worker returns
proposed patches and evidence and Fable applies them. Otherwise, assign the
worker the scoped implementation writes and avoid concurrent edits to its files.

## Delegate and consult

Give the worker a self-contained brief with:

- the requested outcome, relevant source material, and acceptance criteria;
- workspace, current revision, applicable instructions, and write ownership;
- current mode, permissions, constraints, and required validation;
- the worker tier's decision boundary and the consultation protocol below.

Pass these instructions and the host adapter to the worker explicitly. Do not
assume it inherited the conversation or loaded this skill. Ask the worker to
report the model named in its own runtime instructions, and distinguish an
unverified identity from a verified mismatch. A mismatch stops this pairing;
an unverified worker identity must be disclosed rather than reported as proven.

Two consultations are mandatory on every task, because workers under-consult
without them: an approach proposal before substantial implementation, after
any necessary bounded discovery, and a final-review request before the worker
reports completion. Fable reviews the approach against the task and returns
concrete direction. The worker then implements and validates, consulting again
when blocked or when consequential uncertainty affects correctness, scope, or
the approach. Routine choices within the tier's decision boundary do not
require a new checkpoint.

A consultation is the worker ending its turn with the decision needed, relevant
evidence, its recommended next step, and which work depends on the answer.
Fable answers by resuming the same worker. The worker pauses dependent work
until Fable responds and may finish independent authorized work before
returning. Advice cannot replace missing user authority. Fable brings
user-owned decisions back to the user while continuing unaffected work.

Keep the worker at the host's default reasoning setting. A worker at reduced
effort stops noticing when it is stuck, and the consultation rate collapses.
Count consultations per task. If the worker consults on nearly every decision,
the pairing costs more than direct Fable implementation; finish the current
task, then report that evidence for the next selection.

Keep Fable available to answer consultations. Fable can inspect relevant
sources and prepare review while the worker works, without duplicating the
worker's implementation. Reuse the same worker for corrections and further
questions; do not recursively delegate the task or create another Fable
advisor.

## Review and finish

The worker returns the result or proposed patch, changed files, actual
validation commands and outcomes, consultation count, unresolved limitations,
and any decision still needed. Fable inspects the result against the
acceptance criteria and evidence. Return actionable corrections to the same
worker when needed and review the corrected result. If work is blocked, report
the concrete blocker instead of treating it as done.

Keep the coordinating turn active until the worker's result and consultations
are resolved or a blocker requires user input. Fable gives the final user
response with the outcome, validation, requested and reported worker settings,
and remaining limitations. Do not count this advisor review as an independent
review required by another workflow.

When evaluating this skill, exercise [the validation scenarios](references/validation-scenarios.md).
Separate simulated behavior, actual host discovery, and live model execution
in the reported evidence.
