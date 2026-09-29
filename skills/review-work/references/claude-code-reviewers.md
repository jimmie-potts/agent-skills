# Claude Code independent reviewer settings

Use when the host exposes an `Agent` tool with a per-call `model` parameter.
Inspect the actual tool schema and host model descriptions before calling.
Worker attempt thresholds are separate from review-round accounting; worker
replacement resets none of the [review-cycle history](review-cycles.md).

Use this mapping for both Standards and Specification. The routine reviewer
here is already `opus`, so
[review selection](review-selection.md#select-for-impact-and-the-review-task)'s
review task changes no default on this host; still record it in the selection
rationale. High complexity or uncertainty may warrant stronger settings.

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
| Tools | A definition's `tools` list is an allowlist. Without one, the reviewer inherits every available tool, including `Agent`, editing and MCP tools; a background run then keeps every MCP tool but narrows the built-in set, and on Linux, macOS and WSL it can receive Glob and Grep even when the parent lacks them. For the review-work profile's allowlist, see the qualification under [Select the reviewer type](#select-the-reviewer-type) | The host's agent listing, and the tool list the reviewer received |
| Permission mode | A definition's `permissionMode` is ignored while the parent runs in bypass, accept-edits or auto mode | Not a restriction to rely on |
| Nesting | A subagent may spawn its own, three layers deep by default, unless `Agent` is absent from its tools | The agent listing |
| Isolation | `isolation: "worktree"` starts from the default branch, not the frozen head | The parameter passed |
| Delivery and cancellation | Foreground runs return to the call. Background runs, forced while fork mode is on in interactive sessions, end with a completion notification. A turn-limit stop or API cut-off is marked partial; a failed background run is reported failed. `TaskStop` stops a run, and `SendMessage` can resume it once it exits; a run the user stopped from `/tasks` refuses messages as cancelled | The returned result or notification |

Sources: [Claude Code subagents](https://code.claude.com/docs/en/sub-agents),
read 2026-09-27, and the Agent tool schema inspected in Claude Code 2.1.283 on
2026-09-27: `model` (`sonnet`, `opus`, `haiku`, `fable`), `subagent_type`,
`run_in_background` and `isolation`, with no effort parameter. The refusal of
messages to a run the user stopped is in that page's
[Resume subagents](https://code.claude.com/docs/en/sub-agents#resume-subagents)
section. Everything else in the table is documented, unverified until the
active host shows it.

## Select the reviewer type

Prefer a provisioned review-work profile. When the Agent tool lists
`review-work-reviewer` or `review-work-reviewer-high`, check its listed tools
and, where the definition is readable, compare its governing fields with the
[template](../assets/claude-code/review-work-reviewer.md) or the
[high-effort template](../assets/claude-code/review-work-reviewer-high.md).
Choose the high-effort profile when the selected reviewer level is `high`, and
the other profile to inherit the session level. Its tools exclude `Agent`,
editing tools and `Skill`, but `Bash` can still write files and reach
credential-bearing CLIs. Record the restriction as that tool set with the shell
retained. After launch and before accepting the return, check the tools this
reviewer received, such as the tool list in its subagent transcript's prompt
snapshot where reading it is authorized. Record MCP tools as excluded only when
that evidence shows it; otherwise record them as instruction-only. The profile
preloads `code-review` and cannot load other skills; the host skips a missing
preloaded skill silently, so confirm `code-review` is available before briefing
and treat a return without the assigned-axis mode as `incomplete`.

On 2026-09-29, background runs of `review-work-reviewer-high` in Claude Code
2.1.284 received only `Read`, `Bash` and the host's `SubagentHandback` tool,
which delivered the result. No MCP tool reached a reviewer, although the parent
had MCP tools. `Grep` and `Glob` were not delivered despite the allowlist, so
reviewers search through `Bash`. `review-work-reviewer` declares the same tools
but was not run. These observations hold for that host version only: after an
upgrade or profile change, verify the received tools again. A launch that
reports unresolved tools, receives an excluded tool or never returns is a failed
return and a profile defect to report to the activation owner.

Without a profile, use `general-purpose` or another non-fork type that fits.
Its inherited tools include `Agent` and editing tools, so read-only conduct and
the no-descendant rule are instruction-only; record both. A built-in type whose
listing lacks `Agent` and editing tools, such as `Plan` where the host lists it
so, narrows the tools further. Where its listing shows `Skill`, it can load
`code-review`, and the rule against loading a coordinating review workflow
stays instruction-only; treat a return without the assigned-axis mode as
`incomplete`. The host documents that such types skip CLAUDE.md files, so
supply the standards sources in the brief. It also documents them as one-shot,
yet Claude Code 2.1.283 resumed `Plan` reviewers with `SendMessage` on
2026-09-27; try resuming, and start a fresh reviewer when a later round cannot
resume one.

## Launch and resume

Call `Agent` once per reviewer with the selected type, the exact model alias
passed explicitly and a self-contained brief. Run it in the foreground when the
next step depends on the result and the schema allows it; otherwise wait for the
completion notification. Never pass the `fork` type or `isolation`.
`SendMessage` resumes the same reviewer for a later round or reassessment when
[review cycles](review-cycles.md) allows it. Record each reviewer's agent ID.
After a coordinator restart, match every result and notification to a recorded
ID. The same Resume subagents section documents each transcript as
`agent-<agentId>.jsonl` under the session's `subagents/` directory, which was
observed on this host on 2026-09-27; reading it needs authority. A result from
an unrecorded ID is unattributed. The coordinator's model here means a fresh
independent reviewer on that model, never the coordinating session's own
judgment.

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
user or project requirements override the defaults; comparable evidence
supports only the exceptions review selection allows, never below the impact
floor. Do not create, edit or install `.claude/agents` definitions, change
settings, launch replacement coordinator or writer sessions, or simulate a
reviewer by writing both sides of a conversation. For an explicitly selected
cross-provider reviewer or a required native-control gap, use only the bounded
[separate-process adapter](process-reviewers.md). The owning environment provisions profiles, as
[reviewer execution](reviewer-execution.md#discover-provisioned-profiles)
describes.
