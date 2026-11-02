# Grok Bot worker selection and continuation

Use with the [Grok Bot adapter](grok-model-selection.md) for worker roles only.

## Continue or replace a worker

These mechanics apply to assigned workers and advisory workers. Retain the
returned agent or task identifier. Use host listing or status tools when state
is unclear. Use `MessageSubagent` for a running or idle worker that needs a
correction or answer; a queued message alone does not prove the worker resumed.
A correction keeps the same worker and settings.

When reassessment selects a new attempt, follow the [attempt-handoff contract](worker-continuation.md).
Stop an active old assignment with `StopSubagent` (or the verified stop control)
and verify its state before spawning a replacement; a completed assignment is
already stopped. Start a fresh context with supported selected settings and the
complete handoff. A missing stop/resumption capability blocks its affected
operation. Never call a fresh `Task` spawn a resume. Paired workers additionally
follow the discovered pairing adapter's prerequisites and consultations with the
original advisor.

For delivery, include the shared [task packet](resumption.md) or an authorized
reference in each resumed/replacement brief. Match returned task, assignment and
source revision before applying a patch, including late messages from a stopped
worker. Host resumption alone does not establish that its context is current.

## Settings and reassessment

Use [execution choices](model-selection.md) for settings. There is no default
model or fixed correction/promotion ladder. Diagnose failed acceptance and
choose a useful next action within explicit limits. For replacement or recovery,
follow [worker continuation](worker-continuation.md) and carry the current
[task packet](resumption.md). Preserve failures and required limit accounting;
unavailable telemetry remains unknown. A selected pairing keeps its own protocol.
