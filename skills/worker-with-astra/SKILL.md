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
reasoning, and coordinator-only write ownership. Use the coordinator-supplied
selection and task state; do not reread its selection policy or invoke a second
delivery workflow. Its optional-pairing fallback does not change this skill's
fixed advisor identity. When composed by plan-work, the pairing is read-only: the
worker investigates and proposes, and neither agent implements, publishes, or
updates a tracker.

Verify from host-provided runtime evidence that the current coordinator is
`gpt-6-astra`, that the selected Terra or Sol model can be selected, and that
the worker can communicate with its parent. Do not infer identity from a
persona prompt or from the list of models available for spawning. If identity
or capabilities cannot be established, report the gap before delegating. Do not
silently substitute models or claim that a requested model was actually used
without runtime evidence.

For standalone selection or the selected tier's decision boundary, read
[worker tiers](references/worker-tiers.md).
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

Keep Astra available, inspect relevant sources and prepare review without
duplicating worker implementation. Reuse the same worker for ordinary corrections
and advice. A composing workflow may end an inadequate attempt under its shared
handoff policy; establish the new pairing and both consultations with this same
advisor. A fresh context is not a resume. No recursive delegation, replacement
advisor or silent substitution for explicit settings is permitted.

Monitor consultation rate; nearly every routine decision needing advice is
evidence to prefer direct implementation next time, not to skip required advice.

## Review and finish

Require the worker protocol's labeled return for completed or blocked results.
Return specific evidence omissions to the same worker. Disregard extra narrative
when evidence is complete; do not demand a cosmetic rewrite or mistake format
compliance for correctness. Preserve unverified identity as unknown; stop on a
verified mismatch.

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
