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

Call `Agent` once per reviewer with the exact model alias passed explicitly,
a self-contained brief and foreground execution when the next step depends on
the result. Subagents inherit no conversation and return one report;
`SendMessage` resumes the same reviewer for a later round or reassessment. The
coordinator's model here means a fresh independent reviewer on that model,
never the coordinating session's own judgment.

Reviewer effort inherits the session level: the Agent tool has no per-call
effort control and the catalog ships no subagent definitions. A subagent
definition's `effort` frontmatter overrides the session level, so when the
host lists a read-only reviewer definition at the wanted level, in the
project's or the user's `.claude/agents/`, select it by `subagent_type`,
still pass the model explicitly, and record the definition's `effort` as the
requested level after verifying its tools; the executing level stays unknown
unless the host exposes it. Otherwise record the inherited level when known,
otherwise unknown, and report a mismatch with a project's stated review level
rather than claiming to change it.

Take a user-stated session level as stated and record it as `user-stated`;
record a host-provided value such as `CLAUDE_EFFORT` beside it as
`host-observed`, and report a conflict as a known mismatch. Never ask a
reviewer for its own effort. Record the requested model and the
model a reviewer reports from its own runtime instructions separately; a
successful spawn proves the request succeeded, not the executing model.

These are capability hypotheses, not measured review-quality results. Explicit
user or project requirements and stronger evidence override the defaults. Do
not create `.claude/agents` definitions, change settings, launch replacement
sessions or simulate a reviewer by writing both sides of a conversation.
