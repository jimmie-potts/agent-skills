# Codex independent reviewer settings

Use when current collaboration tools expose model and reasoning overrides.
Inspect their actual schema and host model descriptions before calling.

Use this mapping for both Standards and Specification. Place the work by
[review selection](review-selection.md#select-for-impact-and-the-review-task)'s
impact and review task, from what the work needs rather than the settings its
implementer ran with.

| Impact | Reviewer default | Rationale and limits |
| --- | --- | --- |
| Low or medium impact, bounded review task: work a Luna-level implementation suits, with settled requirements and reliable checks that cover the criteria | Luna (`gpt-6-luna`) at `high` for each axis | Capable lower-cost verification where the task and checks justify its coverage |
| Low or medium impact, review task needing Sol-level judgment: several interacting interfaces, state transitions or invariants, or meaningful design judgment, as in work that planning or worker selection would start on Sol | Sol (`gpt-6.1-sol`) at `high` or stronger for each axis | The reviewer needs the cross-interface judgment the change needed. Luna at `high` or above is not a Sol equivalent; a Luna exception needs comparable evidence and stated coverage limits |
| High impact, even with a tiny diff | Strongest evidenced relevant choice of Sol (`gpt-6.1-sol`) at `high` or Astra (`gpt-6-astra`) at `high` | Use separate fresh reviewer contexts; inspect high-impact negative cases |

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
| MCP servers and skills | `mcp_servers` and `skills.config` inherit from the parent when the profile omits them. Connector permissions stay tool-specific, so treat inherited MCP tools as outside `sandbox_mode` unless the host shows otherwise | The parent's configuration and the child's exposed tools |
| Concurrency | `agents.max_concurrent_threads_per_session` caps open child threads | A refused spawn |
| Delivery, cancellation and identity | Documented: the parent waits for the requested results and consolidates them; with `agents.interrupt_message` on, the default, an interrupted turn leaves a model-visible message. Recorded 2026-09-26 and unverified now: `wait_agent` returns a notification, and a timeout is not a result; `list_agents` shows lifecycle state; `interrupt_agent` stops a run; `followup_task` resumes an idle agent. No partial-output marker is documented | The delivered message and the retained agent ID or task name |
| Surface | ChatGPT Work runs hosted subagents without local sandbox or approval controls, and the web sidebar shows activity without controls. CLI, IDE and app controls differ | The surface in use |

The Sol default above is Sol 6.1 (`gpt-6.1-sol`), documented in the
[Codex changelog](https://learn.chatgpt.com/docs/changelog) and
[model page](https://developers.openai.com/api/docs/models/gpt-6.1-sol), read
2026-09-30. The model page lists API reasoning levels `low`, `medium`, `high`,
`xhigh` and `max`; check the active Codex schema for its supported levels and
model availability before selecting it. The historical catalog below does
not establish Sol 6.1 support, including `ultra`, on the current host.

Sources and historical host observations:
[Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents),
read 2026-09-27. The model catalog that Codex CLI 0.156.0 cached on 2026-09-27
lists `gpt-6-luna` ("Fast and affordable model for easier tasks"), `gpt-6-sol`
("Workhorse model for coding and everyday work") and `gpt-6-astra` ("Frontier
intelligence for the most demanding work"), each defaulting to `medium` and
supporting `low` to `max`, with `ultra` also listed for Sol and Astra. A catalog
is not the spawn schema, and whether a spawn on the active surface accepts each
model and level is unverified. The `collaboration.spawn_agent` parameters
`model`, `reasoning_effort` and `fork_turns` were last recorded from a Codex
schema on 2026-09-26. On 2026-09-29, a `codex exec` parent in Codex CLI 0.156.0
reported an `agent_type` parameter listing `review_work_reviewer`
(self-reported), and its rollout records a spawn selecting it that the host
rejected: "agent type is currently not available". Treat profile selection on
that surface as unsupported until such a spawn succeeds. Inspect the
active surface's schema before relying on any of them, and never apply one
surface's controls to another.

## Select and spawn

Spawn each reviewer with `collaboration.spawn_agent`, the exact selected model,
a supported `reasoning_effort`, `fork_turns="none"` and a self-contained brief.
Do not guess a reasoning enum. Where the schema exposes an agent-type parameter
and `review_work_reviewer` resolves, select it after comparing its governing
fields with the [template](../assets/codex/review-work-reviewer.toml). The
template sets `sandbox_mode = "read-only"` and `agents.enabled = false`, whose
effect on a child is unverified, and leaves model and reasoning to the spawn
call. A provisioned file that sets them overrides the call, so do not use one
whose values differ from the selected model and level.

Record each part of the restriction separately. File writes are enforced only
when the profile's sandbox applies and the parent carries no live sandbox or
approval override broader than read-only. Publication and descendants are
enforced only when the child's exposed tools show no multi-agent tools and no
inherited MCP server that can write or publish, and the applied sandbox shows
the shell has no network access; a shell with network can publish through
credential-bearing CLIs such as `gh`. Every part without that evidence is
instruction-only.

Keep the retained agent ID or task name for each reviewer. After a restart or
handoff, reconcile recorded reviewers with `list_agents` where it exists; a
completed agent or message you cannot match to a recorded launch is
unattributed. Treat a final message without its findings list or coverage as
partial, and an interrupt as a cancelled return.

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
a replacement coordinator. Reviewer suitability, including the Sol row for
low- and medium-impact work, remains a hypothesis until evaluated on comparable
work; a model listing is not live review verification. Explicit user or project
requirements override these defaults; comparable evidence supports only the
exceptions review selection allows. Different models for the two axes remain
optional. A fallback for a rejected default stays within the GPT-6 models named
here, never a GPT-5.x model.

Apply [reviewer execution](reviewer-execution.md)'s canonical model-setting
decision separately for every reviewer. Selected call parameters remain requests
unless the owner declares them or the host separately exposes a launch selection.
Retain applicable declaration scope through recovery and recheck replacements;
unknown observations are not mismatches. Declarations do not prove host controls.
