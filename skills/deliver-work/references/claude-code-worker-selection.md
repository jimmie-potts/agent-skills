# Claude Code worker continuation

Use only after choosing a worker. Inspect the current `Agent` and `SendMessage`
schemas. Supply a self-contained brief and applicable project instructions;
do not assume built-in scouts load them. Verify a scout's read-only tools when
that restriction is required. If the optional scout is unavailable, investigate
directly within scope.

Retain the returned agent identifier. Use the host's supported continuation
operation for a correction. A fresh `Agent` call creates a new context, not a
resume. Stop an active old assignment before transferring it; reconcile late
returns against the current task and source revision.

For a deliberately selected worker-with-fable pairing, read its installed
references/claude-code.md and references/worker-tiers.md and follow its protocol.
The workflow does not select that pairing or its tiers by default.

## Settings and reassessment

Use [execution choices](model-selection.md) for settings. There is no default
model or fixed correction/promotion ladder. Diagnose failed acceptance and
choose a useful next action within explicit limits. For replacement or recovery,
follow [worker continuation](worker-continuation.md) and carry the current
[task packet](resumption.md). Preserve failures and required limit accounting;
unavailable telemetry remains unknown. A selected pairing keeps its own protocol.
