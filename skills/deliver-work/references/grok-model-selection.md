# Grok Bot selection adapter

Use only when the host exposes a `Task` tool that can spawn an `executor` (or
verified equivalent) subagent, plus `MessageSubagent` and `StopSubagent` for
messaging and stopping that worker. Inspect the actual tool schemas and host
model descriptions before calling. Policy does not add capabilities or override
host permissions. Do not claim Codex `apply_patch`, Codex `collaboration.*`
tools, or Claude Code `Agent` / `SendMessage` profiles on this host.

For a supported override, call `Task` with the executor (or verified equivalent)
type, a distinctive description, a self-contained brief, and any per-call model
or reasoning parameter the host exposes for the selected tier. Omit an available
model parameter only when inheritance is intended, and report that inheritance.
A successful spawn establishes that the request succeeded, not independent proof
of the executing model's identity. Apply [the model-setting decision](model-gate.md)
with applicable declarations and current observations. Unknown runtime identity
does not invalidate an applicable declaration; required observed mismatches and
explicit verified-identity requirements still stop dependent work. Spawn options
alone never prove that the current coordinator is Grok Bot.

Read [worker settings and continuation](grok-worker-selection.md) only for an
investigation/implementation worker, correction or replacement. Independent
reviewer settings belong to the composed `review-work` skill. For
worker-with-grok, discover its installed package and follow
references/grok.md and its worker protocol; do not copy its consultation
protocol here. Durable writes stay with the delivery coordinator.

Call collaboration tools through the interface actually exposed by the host.
Do not launch replacement coordinator or writer sessions, change personal
settings, install adapters, or simulate multiple models by writing both sides
of a conversation. The optional separate-process reviewer path belongs to
review-work and is limited to its supervised adapter; it preserves the original
coordinator, writer, restrictions, authority and cumulative budgets.
