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
reasoning, and coordinator-only write ownership. Use the coordinator-supplied
selection and task state; do not reread its
selection policy or invoke a second delivery workflow. When composed by plan-work, the pairing is read-only: the worker
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

For standalone selection or the selected tier's decision boundary, read
[worker tiers](references/worker-tiers.md). Retain a composing workflow's
selected tier; read its boundary without reopening strategy selection. An
explicitly requested worker model has no fallback. A worker on Fable is not a
pairing; implement directly instead.

For Claude Code subagent tools, read [the Claude Code adapter](references/claude-code.md)
before spawning or resuming a worker. On another host, use only verified
equivalent model selection and worker resumption capabilities. Report an
unsupported pairing without changing host configuration or installing tools.
On a Codex host, report the host mismatch: an explicit request for this
pairing is not substituted, and a composing workflow may offer worker-with-astra
only as a disclosed alternative when the pairing was optional.

Preserve the underlying task's scope, mode, permissions, and ownership rules.
Planning-only work stays read-only. This skill grants no new publication,
merge, installation, or external-action authority. If another applicable
workflow reserves durable writes for the coordinator, the worker returns
proposed patches and evidence and Fable applies them. Otherwise, assign the
worker the scoped implementation writes and avoid concurrent edits to its files.

## Delegate and consult

Before dispatch, read [the worker protocol](references/worker-protocol.md).
Give the worker a self-contained brief with the selected role/tier and decision
boundary, outcome, acceptance mapping, relevant sources/revision, task/attempt,
applicable instructions, mode, permissions, write owner and required validation.
Include the protocol's labeled return contract and the original advisor address
or conversation. Supply the worker protocol text or an accessible reference it
must read; do not pass this coordinator setup skill, selection tables or the
whole host adapter. The worker does not repeat strategy selection.

Accept a composing workflow's selected configuration without rerunning routing;
read only the selected tier's decision boundary when preparing its brief. Carry
relevant packet state and attempt history directly into that brief. Neither the
worker nor this pairing needs the composing workflow's entire selection,
reporting or resumption policy. Standalone selection still uses the tier reference.

Enforce the protocol's approach consultation before substantial implementation
and final-review consultation before completion; both are required on every
attempt. Answer blocker requests before dependent work resumes. Preserve counts
and evidence; advice cannot replace missing user authority. Bring user-owned
decisions to the user while independent authorized work continues.

Keep Fable available, inspect relevant sources and prepare review without
duplicating worker implementation. Reuse the same worker for ordinary corrections
and advice. A composing workflow may end an inadequate attempt under its shared
handoff policy; establish the new pairing and both consultations with this same
advisor. A fresh context is not a resume. No recursive delegation, replacement
advisor or silent substitution for explicit settings is permitted.

Monitor consultation rate; nearly every routine decision needing advice is
evidence to prefer direct implementation next time, not to skip required advice.
Prefer default worker effort; record inherited/exposed settings or unknown and
report known mismatches. This skill cannot change per-worker effort. Low effort
can reduce consultation; retain that limit in the evidence.

## Review and finish

Require the worker protocol's labeled return for completed or blocked results.
Return specific evidence omissions to the same worker. Disregard extra narrative
when evidence is complete; do not demand a cosmetic rewrite or mistake format
compliance for correctness. Preserve unverified identity as unknown; stop on a
verified mismatch.

Fable inspects the result against the acceptance criteria and evidence. Return
actionable corrections to the same worker when needed and review the corrected
result. If work is blocked, report the concrete blocker instead of treating it
as done.

Keep the coordinating turn active until the worker's result and consultations
are resolved or a blocker requires user input. Fable gives the final user
response with the outcome, validation, requested and reported worker settings,
and remaining limitations. Do not count this advisor review as an independent
review required by another workflow.

When evaluating this skill, exercise [the validation scenarios](references/validation-scenarios.md).
Separate simulated behavior, actual host discovery, and live model execution
in the reported evidence.
