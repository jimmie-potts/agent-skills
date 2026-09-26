# Claude Code independent reviewer settings

Worker attempt thresholds are separate from review-round accounting. Use the
shared [review-cycle contract](review-cycles.md) for finding continuity,
productive rounds and explicit limits; worker replacement resets none of them.

Use this mapping for both Standards and Specification, independently of the
implementation row. Complexity or uncertainty may warrant stronger settings.

| Impact | Reviewer default | Rationale and limits |
| --- | --- | --- |
| Low or medium impact | `opus` for each axis | Opus is the routine reviewer: Anthropic reports it stays accurate at lower effort on review and bug-finding, and planning recommends every Claude Code start on Opus or Fable. Do not select `sonnet` for a reviewer unless the user or project requires it |
| High impact, even with a tiny diff | Strongest evidenced relevant choice of `opus` or the coordinator's model, in separate fresh reviewer contexts | High reasoning recommended; apply the effort observation and capability-gap rules in the [Claude Code adapter](claude-code-model-selection.md) |

Pass the reviewer model explicitly rather than inheriting it accidentally.
Reviewer effort inherits the session level: the Agent tool has no per-call
effort control and the catalog ships no subagent definitions. A subagent
definition's `effort` frontmatter overrides the session level, so when the
host lists a read-only reviewer definition at the wanted level, in the
project's or the user's `.claude/agents/`, select it by `subagent_type`,
still pass the model explicitly, and record its effort as `host-observed`
after verifying the definition's tools and effort. Otherwise record the
inherited level when known, otherwise unknown, and report a mismatch with a
project's stated review level rather than claiming to change it.
The coordinator's model here means a fresh independent reviewer on that model,
never the coordinating writer's own judgment. These are capability hypotheses,
not measured review-quality results. Explicit user/project requirements and
stronger evidence override the defaults; no effort control is added.
