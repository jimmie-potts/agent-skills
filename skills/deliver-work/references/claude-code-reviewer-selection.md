# Claude Code independent reviewer settings

Worker attempt thresholds are separate from review-round accounting. Use the
shared [review-cycle contract](review-cycles.md) for finding continuity,
productive rounds and explicit limits; worker replacement resets none of them.

Use this mapping for both Standards and Specification, independently of the
implementation row. Complexity or uncertainty may warrant stronger settings.

| Impact | Reviewer default | Rationale and limits |
| --- | --- | --- |
| Low or medium impact | `sonnet` for each axis | Capable mid-tier verification is the default for routine work |
| High impact, even with a tiny diff | Strongest evidenced relevant choice of `opus` or the coordinator's model, in separate fresh reviewer contexts | High reasoning recommended; apply the effort observation and capability-gap rules in the [Claude Code adapter](claude-code-model-selection.md) |

Pass the reviewer model explicitly rather than inheriting it accidentally.
The coordinator's model here means a fresh independent reviewer on that model,
never the coordinating writer's own judgment. These are capability hypotheses,
not measured review-quality results. Explicit user/project requirements and
stronger evidence override the defaults; no effort control is added.

