# Route selection by role and host

Read after [work assessment](work-assessment.md) when selecting a worker,
changing implementation strategy/settings, or selecting an independent reviewer.
Direct trivial work at the coordinator's existing settings needs only the
entrypoint and assessment; it does not select a worker. Ratings describe work;
this policy owns selection. Keep the original coordinator's settings and durable
write ownership. Never claim to switch its running model.

## Establish available choices


Honor explicit user/project models, reasoning requirements, limits, and review
gates first. Discover current model availability, supported reasoning levels,
delegation/context controls, and relevant capability descriptions from the host.
Do not infer capability from names or assume every model supports every effort
value. Use comparable evaluation evidence when available; descriptions are
initial heuristics, not measured task success.

Select the least costly suitable supported model and reasoning setting per
role, using task boundaries and reliable checks to justify a cheaper start.
Apply the host adapter's bounded escalation when acceptance exposes a capability
gap. Favor accepted work over low token use; retain stronger risk and review
floors. Record a short rationale for the selection. Do not require
a repository configuration file or build a model registry to use this policy.
When capability distinctions cannot be established, preserve host defaults and
disclose the gap. Missing optional controls do not block otherwise authorized
work; an unmet explicit mandatory model or independent-review requirement blocks
its affected step. Never silently substitute an explicitly requested model.

Optional native profiles are adapters only: verify the resolved model, effort,
context, permissions and available tools against this policy before use. A
profile cannot silently override defaults, risk floors or explicit requirements.
Do not create or install profiles or change personal settings to obtain a
selection. Unavailable optional controls remain unavailable, not simulated.

## Load only the selected branch

- Investigation or implementation worker, strategy change or failed attempt:
  read [implementation selection](implementation-selection.md), then the worker
  branch of the selected host adapter below. For a dispatched worker, read
  [bounded briefs](worker-briefs.md) and supply selected rules, not this routing
  policy. Workers do not repeat coordinator selection.
- Task, fix or final independent reviewer: read
  [review selection](review-selection.md), then that host's reviewer branch.
  Supply the review rubric, frozen comparison and raw sources; implementation
  escalation and pairing details are not reviewer prerequisites.
- Advisory pairing, only after selecting that strategy: discover and read
  worker-with-astra for Codex collaboration tools, or worker-with-fable for
  Claude Code subagent tools. Read its setup adapter and worker protocol. The
  original advisor, consultation gates and ownership remain mandatory. No
  pairing is selected on other hosts.

For Codex collaboration tools, read the
[Codex adapter](codex-model-selection.md). For Claude Code subagent tools, read
the [Claude Code adapter](claude-code-model-selection.md). Read only the active
host and selected role. These adapters own concrete settings and controls; do
not duplicate their tables or infer unavailable controls from another host.
