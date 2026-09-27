# Claude Code independent reviewer settings

Use when the host exposes an `Agent` tool with a per-call `model` parameter.
Inspect the actual tool schema and host model descriptions before calling.
Worker attempt thresholds are separate from review-round accounting; worker
replacement resets none of the [review-cycle history](review-cycles.md).

Use this mapping for both Standards and Specification, independently of the
implementation row. Complexity or uncertainty may warrant stronger settings.

| Impact | Reviewer default | Rationale and limits |
| --- | --- | --- |
| Low or medium impact | `opus` for each axis | Opus is the routine reviewer: review is verification work, where capability pays, so a cheaper reviewer is a measured decision rather than the default. Do not select `sonnet` for a reviewer unless the user or project requires it |
| High impact, even with a tiny diff | Strongest evidenced relevant choice of `opus` or the coordinator's model, in separate fresh reviewer contexts | High reasoning recommended; report an inherited level below it as a known mismatch rather than claiming to change it |

Before launching, run the [reviewer execution preflight](reviewer-execution.md)
with the controls below.

## Know the controls

| Control | How the host resolves it | Evidence |
| --- | --- | --- |
| Model | Per-call `model`, then the definition's `model`, then `CLAUDE_CODE_SUBAGENT_MODEL`, then the parent's model. `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` overrides them all and removes the per-call value. An organization allowlist or fallback chain can substitute another model, with a warning in interactive sessions. A family alias such as `opus` runs the parent's exact model when the parent is in that family | Requested: the value passed. Observed: a substitution warning, or a `/tasks` row the user supplies. Self-reported: the reviewer's statement |
| Effort | No per-call control. A definition's `effort` overrides the session level; otherwise the reviewer inherits it. Supported levels depend on the model | Requested: the definition's `effort`, otherwise `default`. `/tasks` shows effort only when a definition sets it |
| Extended thinking | Inherited from the parent session; no per-reviewer setting | Inherited, or unknown |
| Fresh context | Every non-fork type starts from the brief. The `fork` type inherits the whole conversation | The type passed |
| Tools | A definition's `tools` list is an allowlist. Without one, the reviewer inherits every available tool, including `Agent`, editing and MCP tools. A background run narrows the built-in set | The host's agent listing |
| Permission mode | A definition's `permissionMode` is ignored while the parent runs in bypass, accept-edits or auto mode | Not a restriction to rely on |
| Nesting | A subagent may spawn its own, three layers deep by default, unless `Agent` is absent from its tools | The agent listing |
| Isolation | `isolation: "worktree"` starts from the default branch, not the frozen head | The parameter passed |
| Delivery and cancellation | Foreground runs return to the call. Background runs, forced while fork mode is on in interactive sessions, end with a completion notification. A turn-limit stop or API cut-off is marked partial; a failed background run is reported failed. `TaskStop` stops a run, and a run the user stopped refuses messages | The returned result or notification |

Sources: [Claude Code subagents](https://code.claude.com/docs/en/sub-agents),
read 2026-09-27, and the Agent tool schema inspected in Claude Code 2.1.283 on
2026-09-27: `model` (`sonnet`, `opus`, `haiku`, `fable`), `subagent_type`,
`run_in_background` and `isolation`, with no effort parameter. Everything else
in the table is documented, unverified until the active host shows it.

## Select the reviewer type

Prefer a provisioned review-work profile. When the Agent tool lists
`review-work-reviewer` or `review-work-reviewer-high`, check its listed tools
and, where the definition is readable, compare its governing fields with the
[template](../assets/claude-code/review-work-reviewer.md) or the
[high-effort template](../assets/claude-code/review-work-reviewer-high.md).
Choose the high-effort profile when the selected reviewer level is `high`, and
the other profile to inherit the session level. Its tools exclude `Agent`,
editing tools, `Skill` and MCP tools, but `Bash` can still write files and reach
credential-bearing CLIs. Record the restriction as that tool set with the shell
retained. The profile preloads `code-review` and cannot load other skills; the
host skips a missing preloaded skill silently, so confirm `code-review` is
available before briefing and treat a return without the assigned-axis mode
as `incomplete`.

Without a profile, use `general-purpose` or another non-fork type that fits.
Its inherited tools include `Agent` and editing tools, so read-only conduct and
the no-descendant rule are instruction-only; record both. A built-in type whose
listing lacks `Agent` and editing tools, such as `Plan` where the host lists it
so, narrows the tools further. The host documents that such types skip
CLAUDE.md files and cannot be resumed, so supply the standards sources in the
brief and start a fresh reviewer when a later round cannot resume one.

## Launch and resume

Call `Agent` once per reviewer with the selected type, the exact model alias
passed explicitly and a self-contained brief. Run it in the foreground when the
next step depends on the result and the schema allows it; otherwise wait for
the completion notification. Never pass the `fork` type or `isolation`.
`SendMessage` resumes the same reviewer for a later round or reassessment when
[review cycles](review-cycles.md) allows it. The coordinator's model here means
a fresh independent reviewer on that model, never the coordinating session's
own judgment.

## Record the settings

Take a user-stated session level as stated and record it as `user-stated`;
record a host-provided value such as `CLAUDE_EFFORT` beside it as
`host-observed`, and report a conflict as a known mismatch. With a profile that
sets `effort`, record that value as the requested level; the executing level
stays unknown unless the host exposes it. Otherwise record the inherited level
when known, otherwise unknown, and report a mismatch with a project's stated
review level rather than claiming to change it. Never ask a reviewer for its
own effort. Record the requested model and the model a reviewer reports from
its own runtime instructions separately.

These are capability hypotheses, not measured review-quality results. Explicit
user or project requirements and stronger evidence override the defaults. Do
not create, edit or install `.claude/agents` definitions, change settings,
launch replacement sessions or simulate a reviewer by writing both sides of a
conversation. The owning environment provisions profiles, as
[reviewer execution](reviewer-execution.md#discover-provisioned-profiles)
describes.
