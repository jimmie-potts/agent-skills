# Grok Bot worker adapter

Read only when dispatching a worker through Grok Bot's `Task` tool. Inspect the
actual schema and supported executor type. Use host defaults or supported
explicit settings; this adapter selects no model or thinking level. Do not
invent Codex or Claude aliases or controls on this host.

Give each worker a self-contained brief. Retain its task identifier and verify
`MessageSubagent` or `StopSubagent` support when continuation or cancellation
needs it. Requested settings do not establish runtime identity. Check
[required settings](model-gate.md) only for explicit requirements.

Read [worker continuation](grok-worker-selection.md) when correcting or replacing
a worker. For deliberately selected worker-with-grok pairing, discover its
installed package and follow references/grok.md and its worker protocol.
Durable delivery effects remain with the coordinator. Do not change personal
configuration or install adapters to obtain an optional selection.
