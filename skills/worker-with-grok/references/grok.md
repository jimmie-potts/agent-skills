# Grok Bot Task / MessageSubagent adapter

Use this adapter when the host exposes a `Task` tool that can spawn an
`executor` (or verified equivalent) subagent, plus `MessageSubagent` and
`StopSubagent` for messaging and stopping that worker. Check the current tool
schemas before use; these instructions do not add unavailable capabilities.
Do not claim Codex `apply_patch`, Codex `collaboration.*` tools, or Claude
Code `Agent` / `SendMessage` profiles on this host.

## Establish identities

Use the host's runtime metadata or authoritative session instructions to
establish the coordinator's identity as Grok Bot. An available spawn option,
persona prompt, or settings file alone does not establish the current host.
If the current identity is unknown or different, report that the requested
pairing cannot be established.

Confirm that `Task` (or the verified spawn tool), `MessageSubagent`, and
`StopSubagent` are callable in the current session before spawning. A worker
spawned where messaging or stop controls are missing cannot complete the
consultation cycle after the first return.

## Start one worker

Call `Task` once with the executor (or verified equivalent) subagent type, a
distinctive description, and the self-contained brief from SKILL.md. When the
host exposes a per-call `model` or reasoning parameter, pass the selected tier
values explicitly and record requested versus observable settings separately.
Omitting an available model parameter inherits the coordinator; report that
inheritance rather than claiming a distinct worker model. Do not invent Codex
or Claude model aliases.

Include [the worker protocol](worker-protocol.md), its selected tier boundary
and task context. A fresh executor has none of the conversation. Do not
require the worker to read coordinator setup files. Retain the agent or task
identifier returned by the host; every later `MessageSubagent` or
`StopSubagent` call targets it.

A successful spawn with an explicit model parameter records the requested
selection; it does not by itself prove an independently verified runtime
identity. Ask the worker to report the model named in its own runtime
instructions on every return when that evidence exists. Treat an omitted
report as unverified identity. If the host rejects the model or cannot spawn
the worker, report the error without silently retrying a different model.

## Exchange advice without losing the worker

The worker ends a turn with a labeled advice request or completed result when
it cannot message the coordinator mid-turn, or it calls the host's evidenced
parent-messaging path when that path exists. An advice request carries the
decision needed, evidence, recommendation, and paused dependency.

The coordinating Grok Bot agent replies with `MessageSubagent` targeting the
retained worker identifier. Dependent work waits for that answer. Do not treat
a queued message, timeout, or notification alone as completed advice. Keep
individual waits bounded so user updates remain possible.

A fresh `Task` call starts a new worker with no memory of the prior attempt.
Use it only for a composing workflow's explicitly selected new attempt after
the previous assignment has ended and the shared handoff is complete. Never
describe a fresh Task spawn as MessageSubagent resumption. Re-establish the
pairing prerequisites and both consultations with the original Grok Bot
advisor.

If the host reports the worker as failed, terminated, or unreachable, inspect
the returned state and evidence before taking further action. Report a terminal
failure as a blocker; do not claim a completed advisory exchange, replace the
advisor, or silently start over with another worker. If the user pauses the
task, preserve the worker identifier and the pending question for resumption.

## End an attempt before replacement

Apply the composing workflow's shared attempt-handoff contract. Retain the old
identifier and establish that the worker has returned or terminated. If it is
still running, call `StopSubagent` (or the verified stop control) and confirm
it has stopped; unavailable stopping blocks replacement. Start the selected
new worker with `Task`, supplying the complete handoff brief and unchanged
ownership. A terminal failure still requires diagnosis; it is not permission
to silently replace a worker.

When composed by deliver-work, carry relevant fields from the coordinator's
existing task packet in the brief. The worker returns task/attempt and source
revision with the proposal without reading the packet policy. The delivery
coordinator still performs current-state checks; retained context and references
grant no new write authority. Shared handoff expectations also live under
`skills/deliver-work/references/worker-continuation.md` when that skill is
composed.

## Ownership and delivery

Agents on this host share the box filesystem unless the spawn isolates a
worktree. State write ownership in the initial brief. Under
coordinator-only-write rules, the worker returns proposed patches or exact
file contents without applying them. Grok Bot applies the agreed change with
the host's ordinary edit tools and supplies the resulting revision or files
for the worker's validation. Do not require Codex `apply_patch` or invent a
wrapper that claims that tool. When the worker owns scoped writes, name its
files and keep the coordinator out of them until the worker returns.
Validation must respect the same permissions, including whether generated
artifacts are allowed.

Never simulate a second model by writing both sides of a dialogue. Never
report a worker's requested model as its verified identity.
