---
name: worker-with-astra
description: Delegate a task to a Terra or Sol worker with the original Astra agent as its advisor in Codex. Use when explicitly invoked, requested by the user, or deliberately composed by deliver-work or plan-work after assessment; do not select for ordinary delegation or on hosts without Codex collaboration tools.
---

# Worker with Astra

Keep the original Astra agent as coordinator and advisor. Give one Terra or Sol
worker responsibility for implementation and validation within the user's task.
The worker consults that same Astra agent rather than creating a separate
advisor.

## Establish the pairing

When composed by deliver-work, retain its assessment, selected worker tier and
reasoning, and coordinator-only write ownership. Read that workflow's selection
reference as directed by its coordinator; do not invoke a second delivery
workflow. Its optional-pairing fallback does not change this skill's fixed
advisor identity. When composed by plan-work, the pairing is read-only: the
worker investigates and proposes, and neither agent implements, publishes, or
updates a tracker.

Verify from host-provided runtime evidence that the current coordinator is
`gpt-6-astra`, that the selected Terra or Sol model can be selected, and that
the worker can communicate with its parent. Do not infer identity from a
persona prompt or from the list of models available for spawning. If identity
or capabilities cannot be established, report the gap before delegating. Do not
silently substitute models or claim that a requested model was actually used
without runtime evidence.

Before selecting a worker, read [worker tiers](references/worker-tiers.md).
Preserve a composing workflow's stronger supported selection. Luna is outside
this pairing; use ordinary scouting for its bounded read-only work.

For Codex collaboration tools, read [the Codex adapter](references/codex.md)
before spawning or messaging. On another host, use only verified equivalent
model selection and parent communication capabilities. Report an unsupported
pairing without changing host configuration or installing tools. On a Claude
Code host, report the host mismatch: an explicit request for this pairing is
not substituted, and a composing workflow may offer worker-with-fable only as a
disclosed alternative when the pairing was optional.

Preserve the underlying task's scope, mode, permissions, and ownership rules.
Planning-only work stays read-only. This skill grants no new publication,
merge, installation, or external-action authority. If another applicable
workflow reserves durable writes for the coordinator, the worker returns
proposed patches and evidence and Astra applies them. Otherwise, assign the
worker the scoped implementation writes and avoid concurrent edits to its
files.

## Delegate and consult

Give the worker a self-contained brief with:

- the requested outcome, relevant source material, and acceptance criteria;
- workspace, current revision, applicable instructions, and write ownership;
- current mode, permissions, constraints, and required validation;
- the labeled return format in Review and finish;
- the original Astra agent's address and the consultation protocol below.

Pass these instructions and the applicable host adapter to the worker
explicitly. Do not assume it inherited the conversation or loaded this skill.
Ask the worker to report its actual model identity when the host exposes it,
and distinguish an unverified identity from a verified mismatch. A mismatch
stops this pairing; an unverified worker identity must be disclosed rather than
reported as proven.

Two consultations are mandatory: an approach proposal before substantial
implementation and a final-review request before reporting completion. After
any necessary bounded discovery, the worker proposes its approach. Astra
reviews it against the task and returns concrete direction. The worker then
implements and validates, consulting again when blocked or when consequential
uncertainty affects correctness, scope, or the approach. Routine choices within
the selected tier's boundary need no new checkpoint. Record consultation counts
and evidence. Missing checkpoints prevent acceptance; consultation on nearly
every routine decision is evidence to prefer direct implementation on the next
task, not a reason to omit required advice.

Each consultation names the decision needed, relevant evidence, the worker's
recommended next step, and which work depends on the answer. The worker pauses
that dependent work until Astra responds and may continue independent
authorized work. Advice cannot replace missing user authority. Astra brings
user-owned decisions back to the user while continuing unaffected work.

Keep Astra available to receive and answer consultations. Astra can inspect
relevant sources and prepare review while the worker works, without duplicating
the worker's implementation. Reuse the same worker for corrections and further
questions; do not recursively delegate the task or create another Astra
advisor. A composing workflow may end an inadequate attempt and select a new
worker under its shared attempt-handoff contract. This is a new attempt, not a
resume. Re-establish pairing prerequisites and both consultations with the same
advisor; explicit model requirements still prohibit silent substitution.

## Review and finish

The worker returns completed or blocked results in this labeled format:

- Artifact: proposed patch or exact file contents; requested findings or plan
  for read-only work; `none` when no artifact is produced.
- Changed files: paths, distinguishing proposed from applied changes, or `none`.
- Validation: commands actually run with trimmed outcomes and the revision or
  state checked; identify required checks not run.
- Consultations: count for an advisor loop, otherwise `not applicable`.
- Settings: requested and reported model/reasoning, with `unknown` for
  unexposed values; retain any host-required identity evidence.
- Limitations: unresolved gaps or blockers, or `none`.
- Pending decisions: decision and owner, or `none`.

Exclude surrounding narrative, transcript replay, and restated instructions.
Keep the requested artifact and required evidence intact. Consultation requests
keep their decision, evidence, recommendation, and paused-dependency format. If
required evidence is missing, return the specific omissions to the same worker
before accepting completion. If the evidence is complete but extra narrative is
present, disregard that narrative and evaluate the result normally; do not
request a cosmetic rewrite or treat format compliance as correctness.

Astra inspects the result against the acceptance criteria and evidence. Return
actionable corrections to the worker when needed and review the corrected
result. If work is blocked, report the concrete blocker instead of treating it
as done.

Keep the coordinating turn active until the worker's result and consultations
are resolved or a blocker requires user input. Astra gives the final user
response with the outcome, validation, and remaining limitations. Do not count
this advisor review as an independent review required by another workflow.

When evaluating this skill, exercise [the validation
scenarios](references/validation-scenarios.md). Separate simulated behavior,
actual host discovery, and live model execution in the reported evidence.
