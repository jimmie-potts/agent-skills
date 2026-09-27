# Codex independent reviewer settings

Use when current collaboration tools expose model and reasoning overrides.
Inspect their actual schema and host model descriptions before calling.

Use this mapping for both Standards and Specification, independently of the
implementation row. Complexity or uncertainty may warrant stronger settings.

| Impact | Reviewer default | Rationale and limits |
| --- | --- | --- |
| Low or medium impact | Luna (`gpt-6-luna`) at `high` for each axis | Capable lower-cost verification is the default for routine work |
| High impact, even with a tiny diff | Strongest evidenced relevant choice of Sol (`gpt-6-sol`) at `high` or Astra (`gpt-6-astra`) at `high` | Use separate fresh reviewer contexts; inspect high-impact negative cases |

Before spawning, run the [reviewer execution preflight](reviewer-execution.md)
with the controls below.

## Know the controls

| Control | How the host resolves it | Evidence |
| --- | --- | --- |
| Model and reasoning | An explicit spawn value, then `agents.default_subagent_model` or `agents.default_subagent_reasoning_effort`, then the parent's value. A custom agent file's `model` or `model_reasoning_effort` then takes precedence over all of them. A model chosen without an effort runs at that model's default effort. Supported levels depend on the model | Requested: the values passed, or the profile's when it sets them. Observed: returned runtime metadata |
| Fresh context | `fork_turns="none"` starts from the brief. A full-history fork inherits the parent's settings, cannot take overrides and carries implementation narratives | The parameter passed |
| Profile | A custom agent's `name` selects it where the spawn schema exposes an agent-type parameter. Project `.codex/agents/` and personal `~/.codex/agents/` files load as configuration layers, and a custom name matching a built-in agent replaces it | The schema and a readback of the resolved file |
| Sandbox and approvals | A child inherits the parent's sandbox policy. A profile's `sandbox_mode` applies, but the parent turn's live overrides, such as a `/permissions` change or `--yolo`, are reapplied to the child regardless. Where no fresh approval can surface, an action needing one fails back to the parent | The parent's current permissions and the profile readback |
| Nesting | Children can spawn their own; no depth limit is documented. `agents.enabled = false` in a profile is a documented setting whose effect on a child is unverified | The child's exposed tools, when visible |
| MCP servers and skills | `mcp_servers` and `skills.config` inherit from the parent when the profile omits them | The parent's configuration |
| Concurrency | `agents.max_concurrent_threads_per_session` caps open child threads | A refused spawn |
| Surface | ChatGPT Work runs hosted subagents without local sandbox or approval controls, and the web sidebar shows activity without controls. CLI, IDE and app controls differ | The surface in use |

Sources: [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents),
read 2026-09-27. The `collaboration.spawn_agent` parameters `model`,
`reasoning_effort` and `fork_turns` were last recorded from a Codex schema on
2026-09-26, and no agent-type parameter has been recorded. Inspect the active
surface's schema before relying on any of them, and never apply one surface's
controls to another.

## Select and spawn

Spawn each reviewer with `collaboration.spawn_agent`, the exact selected model,
a supported `reasoning_effort`, `fork_turns="none"` and a self-contained brief.
Do not guess a reasoning enum. Where the schema exposes an agent-type parameter
and `review_work_reviewer` resolves, select it after comparing its governing
fields with the [template](../assets/codex/review-work-reviewer.toml). The
template sets `sandbox_mode = "read-only"`, disables multi-agent tools and
leaves model and reasoning to the spawn call. A provisioned file that sets them
overrides the call, so any difference from the selected values is conflicting
precedence. Record restricted execution as established only when the parent
carries no live sandbox or approval override broader than read-only; otherwise
it is instruction-only.

Without a profile, the reviewer inherits the parent's sandbox, tools, MCP
servers and multi-agent tools, so read-only conduct and the no-descendant rule
are instruction-only; record both. Record requested parameters and returned
runtime metadata separately; a successful spawn proves the request succeeded,
not the executing model. Stop a reviewer with the surface's interrupt or close
control. Follow up the same reviewer for a later round only when
[review cycles](review-cycles.md) allows it.

Do not create, edit or install `.codex/agents` or `~/.codex/agents` files or
change `config.toml`. The owning environment provisions profiles, as
[reviewer execution](reviewer-execution.md#discover-provisioned-profiles)
describes.

Astra in this table is an independent reviewer, not an implementation worker or
a replacement coordinator. Reviewer suitability remains a hypothesis until
evaluated on comparable work; a model listing is not live review verification.
Explicit user or project requirements and stronger evidence override these
defaults. Different models for the two axes remain optional. A fallback for a
rejected default stays within the GPT-6 models named here, never a GPT-5.x
model.
