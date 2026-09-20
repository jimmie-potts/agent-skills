# Codex selection adapter

Use only when current collaboration tools expose model and reasoning overrides.
Inspect their actual schema and host model descriptions before calling. Policy
does not add capabilities or override host permissions.

For a supported override, use collaboration.spawn_agent with the exact selected
model and supported reasoning_effort, fork_turns="none", and a self-contained
brief. Full-history forks in this host inherit parent settings and cannot accept
those overrides. If inheritance is intended, omit overrides and report inherited
settings only to the extent observable. Do not guess a reasoning enum.

Record requested parameters and actual returned runtime metadata separately.
A successful spawn establishes the request succeeded, not independent proof of
the executing model's identity. Disclose unknown identity; handle a verified
mismatch against explicit requirements before dependent work. Model options
alone never prove that the current coordinator is Astra.

Read [worker settings and continuation](codex-worker-selection.md) only for an
investigation/implementation worker, correction or replacement. Read
[reviewer settings](codex-reviewer-selection.md) only for independent review.
Fresh review briefs carry the fixed comparison and raw sources without prior
approval narratives. For worker-with-astra, discover its installed package and
follow references/codex.md and its worker protocol; do not copy its consultation
protocol here. Durable writes stay with the delivery coordinator.

Call collaboration tools through the interface actually exposed by the host.
Do not launch replacement sessions, change personal settings, install adapters,
or simulate multiple models by writing both sides of a conversation.
