# Codex worker adapter

Read only when dispatching a worker on a host with Codex collaboration tools.
Inspect the exposed schema. This adapter selects no model or reasoning level.

Use the host's defaults or supported explicit settings. When overriding settings,
`collaboration.spawn_agent` requires `fork_turns="none"` and a self-contained
brief on hosts with this schema. Full-history forks inherit the parent's settings
and cannot accept those overrides. Follow the live schema if it differs.
Requested parameters do not establish runtime identity. Check
[required settings](model-gate.md) only for explicit requirements.

Read [worker continuation](codex-worker-selection.md) when correcting or replacing
a worker. For deliberately selected worker-with-astra pairing, discover its
installed package and follow references/codex.md and its worker protocol.
Durable delivery effects remain with the coordinator. Do not change personal
configuration or install adapters to obtain an optional selection.
