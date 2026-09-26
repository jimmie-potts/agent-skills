# Claude Code selection adapter

Use only when the host exposes an `Agent` tool with a per-call `model`
parameter. Require `SendMessage` resumption only when the selected strategy
continues a retained worker, including every advisory pairing. A one-return
scout does not need resumption. Inspect the actual tool schemas and host model
descriptions before calling; policy adds no capabilities or permissions.

For a supported override, call `Agent` with the exact selected model alias, a
self-contained brief, and foreground execution when the next step depends on
the result. Subagents inherit no conversation and cannot message the
coordinator mid-run; they return a report, and `SendMessage` resumes the same
agent. The tool exposes no per-call reasoning control. A worker inherits
session effort unless an existing host override applies. Record the effective
level when exposed or stated, otherwise unknown; use a known session level
only when inheritance is established. Report known mismatches with the
selected role setting, without claiming to change effort.
Do not create `.claude/agents` definitions or change settings to obtain a
model.

A session cannot reliably read its own effort. On 2026-09-24 a Claude Code Opus
session set to `high` reported `low`. Take a user-stated level as stated and
record it as user-stated; never ask an agent to verify its own effort. The
documented `${CLAUDE_EFFORT}` skill substitution and a `CLAUDE_EFFORT`
environment variable are host-provided values, not an independent reading. On
2026-09-24 a Claude Code session stated to run at `medium` exposed
`CLAUDE_EFFORT=medium` to its shell; that agreement cannot show whether the
value tracks a later `/effort` change or resists the mismatch above, and the
substitution itself was not exercised because the catalog does not use it.
Record either value as `host-observed` beside the user's statement; the term
names the source, not independent verification. A conflict
between them is a known mismatch to report, not a reason to override the user.

Record requested parameters and the model the worker reports from its own
runtime instructions separately. A successful spawn establishes that the
request succeeded, not independent proof of the executing model. Disclose
unknown identity; handle a verified mismatch against explicit requirements
before dependent work. Spawn options alone never prove that the current
coordinator is Fable; read the coordinator's own runtime instructions.
A flagged message can switch a Claude Code session to an older model
automatically, and the user switches back with `/model`; the session
transcript's per-message model is host-observed evidence of such a change
where reading it is authorized.
Report a model change during a delivery as a known mismatch in Models, naming
each model and the stage at which it changed; the Execution record's
coordinator rows keep the coordinator that completes the section.

Read [worker settings and continuation](claude-code-worker-selection.md) only
for investigation/implementation, correction or replacement; it routes the
pairing's references/worker-tiers.md when applicable. Read
[reviewer settings](claude-code-reviewer-selection.md) only for independent
review. Fresh review briefs carry the frozen comparison and raw sources without
prior approval narratives. Durable writes stay with the delivery coordinator.

Do not launch replacement sessions, change personal settings, install
adapters, or simulate multiple models by writing both sides of a conversation.
