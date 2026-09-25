# Recommend the session to start

Read for every proposed work item. Give the user a concrete model and thinking
level to choose when starting work in either Claude Code or Codex. Here,
"intelligence level" means the host's reasoning/effort setting, not another work
rating or a claim that equal level names provide equal capability across models.

Use the discovered canonical deliver-work package's `references/model-selection.md`
and `references/implementation-selection.md` for suitability, risk floors and
strategy. For proposed workers, read each host's model-selection adapter and
worker-selection reference from that package; those own worker defaults and
escalation. Reading both hosts for recommendations does not authorize dispatch.
Keep the three assessment ratings model-neutral and preserve explicit user or
project requirements.

## Choose the starting session

Use the following starting-session heuristics, adjusted to the item's evidence
and available controls. They recommend a future session the user can start;
they do not change the current coordinator or replace worker-selection policy.

| Work to start | Claude Code model / effort | Codex model / reasoning | Session role |
| --- | --- | --- | --- |
| Trivial, mechanical, low complexity/uncertainty/impact, with reliable checks | Sonnet (`sonnet`) / `low` | Luna (`gpt-6-luna`) / `low` | Implement directly |
| Bounded implementation, low/medium complexity and impact, settled requirements and reliable checks | Sonnet (`sonnet`) / `medium` | Luna (`gpt-6-luna`) / `medium` | Implement directly |
| Several interfaces or meaningful design judgment within a bounded outcome | Sonnet (`sonnet`) / `high` | Sol (`gpt-6-sol`) / `medium` | Implement; identify design checkpoints |
| High complexity or impact within a bounded outcome | Opus (`opus`) / `high` | Sol (`gpt-6-sol`) / `high` | Implement with the stronger capability floor |
| Sustained difficult reasoning, architecture tradeoffs, or substantial coordination across dependent work | Fable (`fable`) / `high` | Astra (`gpt-6-astra`) / `high` | Orchestrate bounded workers, or implement directly when reasoning cannot be separated |

These are planning heuristics, not benchmark results or guaranteed savings.
High impact overrides the cheap start even for a one-line change. High
uncertainty calls for investigation or clarification before dependent coding;
recommend settings for that next step and label later implementation choices
provisional. More thinking does not resolve a missing product decision.
For decomposed work, assess each item separately; use a stronger parent session
only when its coordination or reasoning warrants it. Do not assign every child
the parent's model. Above-high effort needs a task-specific reason or an explicit
requirement and verified support; it is not the default for every hard task.

Verify model identifiers or aliases and supported effort levels from available
host evidence. When that is insufficient, consult current official
[Codex model guidance](https://developers.openai.com/codex/models) or
[Claude Code model configuration](https://code.claude.com/docs/en/model-config).
These sources describe model and effort controls; the table is this workflow's
recommendation. Claude aliases can resolve differently by provider. Do not
invent a version or infer account access from public documentation.

Label each host choice verified against available host evidence or provisional
pending model/effort availability. If the other host cannot be inspected, still
give its conditional recommendation and name what the user must check before
starting. If a required policy resource is missing, report the recommendation
gap and continue independent planning without reconstructing that policy.

## Record the recommendation beside the assessment

Use one compact "Execution recommendation" section in the existing proposal,
issue description or authoritative work document. Include:

- **Claude Code:** starting model/alias, recommended effort, and session role.
- **Codex:** starting model/identifier, recommended reasoning, and session role.
- **Why:** the assessment evidence, checks and task boundaries supporting those
  choices; name the condition that would require reassessment.
- **Workers, when useful:** proposed implementation model/effort for each host,
  using its canonical worker policy. Otherwise state direct implementation.
- **Availability:** evidence source/date, unverified options, and any conflict
  with explicit requirements. Keep the planner's observed settings separate.

A recommendation never claims the current session changed models, effort was
applied, workers ran, or acceptance passed. In particular, a recommended Claude
session effort does not establish a per-call worker effort control or prove
inherited effort. Preserve the host adapter's observation rules. Do not launch
sessions, edit personal settings, or start delivery to make a recommendation.
At delivery pickup, recheck scope, model availability and host controls; refresh
the recommendation within existing authority when its assumptions changed.
