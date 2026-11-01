# Claude Code worker adapter

Read only when dispatching a worker through Claude Code's `Agent` tool. Inspect
the actual schema and resolved definitions. This adapter selects no model or
thinking level. Use host defaults or supported explicit settings.

Supply a self-contained brief; do not assume the worker inherits the conversation
or project instructions. Verify continuation support only if the assignment
needs it. Use the available `SendMessage` operation to continue a retained worker;
a new `Agent` call is a new context. The tool may expose no per-call effort
control; do not invent one or change personal settings to obtain it.

Record requested and exposed settings separately when they matter. A successful
request is not runtime identity. Never ask an agent to verify its own effort.
For explicit requirements, follow [required settings](model-gate.md).

Read [worker continuation](claude-code-worker-selection.md) when correcting or
replacing a worker. A deliberately selected worker-with-fable pairing keeps its
installed protocol. Durable delivery effects remain with the coordinator.
