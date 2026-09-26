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
| Trivial, mechanical, low complexity/uncertainty/impact, with reliable checks | Opus (`opus`) / `low` | Luna (`gpt-6-luna`) / `low` | Implement directly |
| Bounded implementation, low/medium complexity and impact, settled requirements and reliable checks | Opus (`opus`) / `medium` | Luna (`gpt-6-luna`) / `medium` | Implement directly |
| Several interfaces or meaningful design judgment within a bounded outcome | Opus (`opus`) / `medium` | Sol (`gpt-6-sol`) / `medium` | Implement; identify design checkpoints |
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

On Claude Code, every starting row uses Opus or Fable, and effort is the cost
lever. Anthropic's published guidance, read 2026-09-25, is the basis. Claude
Code's model configuration documents Opus 5.5 at its `medium` default as
matching or exceeding Opus 5 at `high` on coding and knowledge-work
evaluations. The cost guidance reports that a multi-model configuration which
looked cheaper than a single model cost more than that same model run at lower
effort, and its SWE-bench Pro measurements put Opus 5.5 at `medium` about 2.5
points below `high` for about 70% of the cost, `low` about 8 points below for
about a third, and `xhigh` about 1.4 points above for 2.5 times the cost.
Well-specified items with reliable checks therefore start at `low` or
`medium`; when a checkable outcome fails, rerun at the next level rather than
starting every item high. Fable is for sustained reasoning and long-horizon
coordination, or when Opus at `high` still falls short.

Effort buys verification, edge-case testing and independent judgment, not a
better approach. Claude Code's
[Spending your effort](https://claude.dev/blog/spending-your-effort/)
(2026-09-25) found that on a fully specified task the levels produced
similar work, that on an underspecified task higher effort made more
assumptions on the user's behalf, and that on Terminal-Bench 3.0 higher
effort cut failures from missed edge cases but not from a wrong approach.
So a settled, well-written item starts at `medium` even when it needs design
judgment, with checkpoints to keep the user in the loop; a missing decision
or unknown approach is uncertainty, which `Investigate first` resolves.
On Claude Code only, raise the start to Opus (`opus`) at `high` when
acceptance turns on hidden edge cases or verification, whatever the ratings:
a bug fix from a report in existing code, input sanitizing or parsing,
security, concurrency, data migration, or performance work. The Codex column
keeps its row; this rule is a Claude Code adapter, not a change to the shared
table. That article reserves `max` for unattended end-to-end building and
verification of difficult work, which is the task-specific reason above-high
effort needs. Sources:
[Optimizing for cost and intelligence](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence),
[Claude Code model configuration](https://code.claude.com/docs/en/model-config),
the article above and
[Getting the most out of Opus 5.5](https://claude.dev/blog/getting-the-most-out-of-opus-5-5/).
These describe general effort curves; this repository has not yet measured
its own, so the rows are hypotheses to reassess against delivery records.

### Record the cheaper start

Sonnet is never a Claude Code starting recommendation; it is the cheaper
start. Map it from the recommended row, at the same effort:

| Recommended Claude Code start | Cheaper Claude Code start |
| --- | --- |
| Opus (`opus`) / `low` | Sonnet (`sonnet`) / `low` |
| Opus (`opus`) / `medium` | Sonnet (`sonnet`) / `medium` |
| Opus (`opus`) / `high`, impact below high | Sonnet (`sonnet`) / `high` |
| Opus (`opus`) / `high`, impact high | None; the impact floor holds |
| Opus (`opus`) above `high` | Opus (`opus`) / `high` |
| Fable (`fable`) / `high` | Opus (`opus`) / `high` |

For Codex, record a cheaper start only when the recommended model or budget
may be unavailable; otherwise write `none` for that host. The cheaper start
keeps the session type, the reviewers and every gate; it trades capability
for cost on the implementation alone, and a failed check on the cheaper start
is the signal to rerun at the recommended start.

### Recommend the reviewers

On Claude Code, the `Reviewers` row names `opus` for both axes, or the
coordinator's model at high impact, following the canonical Claude reviewer
adapter, which also owns how reviewer effort is inherited from the session or
set by a subagent definition. Write the level as the session's level unless
host evidence shows a read-only reviewer definition with `effort: high`, and
then name that definition in the row. Verification is where effort pays, so
when the project wants reviews at `high` and no definition exists, add a
`Checkpoints` entry that stops before the final reviews so the user can run
`/effort high`, which the effort article above says applies mid-session
without breaking the prompt cache. On Codex, use that host's reviewer
adapter.

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

## Name the session type

Describe the starting session with exactly one of these types. `One-shot` and
`Orchestrate` come from the table's session role above. `Pair` comes from the
canonical implementation selection's advisory-pairing strategy, and
`Investigate first` from the high-uncertainty guidance under the table:

| Session type | Session role it expresses | What the session does |
| --- | --- | --- |
| `One-shot` | Implement directly, including with design checkpoints or the stronger capability floor | Implements directly without worker subagents; a Checkpoints row names decisions where it stops to ask |
| `Pair` | Implement through the host's advisory pairing, when canonical implementation selection chooses it | One worker implements under the pairing while the session advises at approach, blockers and final review |
| `Orchestrate` | Orchestrate bounded workers | Breaks the work down, delegates bounded pieces to worker subagents and owns every write and review |
| `Investigate first` | Investigation or clarification before dependent coding | A read-only session answers a named question; the item is then reassessed |

The type is a presentation label, not another selection table. It governs
implementation only. Every implementing type also runs the two independent
Standards and Specification reviewers that delivery requires; the Reviewers row
and each prompt authorize them. `Investigate first` has no reviewers.

## Record the recommendation beside the assessment

Use one compact `## Execution recommendation` section in the existing proposal,
issue description or authoritative work document, in this order:

1. `**Start with:**` one line giving the answer: the session type first, then
   each host's model and thinking level, then which prompt to paste.
2. `**Work surface:**` on the next line, with exactly one value from
   [the work surface](#classify-the-work-surface).
3. A two-host table with columns `Claude Code` and `Codex` and the rows
   `Model`, `Thinking level`, `Session type`, `Subagents`, `Reviewers` and
   `Availability`. Add a `Checkpoints` row only when the session should stop at
   named decisions. `Subagents` gives each proposed implementation worker's
   model and level from the canonical worker policy, or `None`. `Reviewers`
   gives the two fresh read-only final reviewers per host from the canonical
   reviewer policy for the item's impact, or `None` for `Investigate first`.
   `Availability` gives the evidence
   source and the date the host's options were checked, labels each host
   verified or provisional, and notes any
   conflict with explicit requirements. Keep the planner's own observed
   settings out of the table.
4. `**Prompt (Claude Code):**` and `**Prompt (Codex):**`, each followed by one
   fenced `text` block written from the template below.
5. `**Cheaper start:**` one line naming what it covers, its session type and
   each host's model and level from [the cheaper-start mapping](#record-the-cheaper-start),
   followed by `**Cheaper prompt (Claude Code):**` and
   `**Cheaper prompt (Codex):**` blocks for each host that has one. Write
   `none` for a host without one and say why, such as the high-impact floor.
6. `**Why:**` the assessment evidence, checks and task boundaries behind the
   choice. `**Reassess when:**` the condition that invalidates it.
   `**Assessed:**` the date, the policy revision (`agent-skills@<sha>` or the
   installed package's revision), evidence links, and a fingerprint slot. Use
   a fingerprint only when the owning project defines one, such as a hash of
   the item body without this section; otherwise write `not used`.

When the evidence cannot support a choice, replace the answer, table and
prompts with `**Status:** insufficient` and `**Missing:**` naming the exact
input and the next question or evidence; keep the `Work surface`, `Why`,
`Reassess when` and `Assessed` lines. Never fill an insufficient item with a
guessed default. A section has at most one `**Missing:**` line; when the work
surface is also `Unknown`, name its evidence in that same line.

For example, the section of a bounded instruction change opens:

```markdown
## Execution recommendation

**Start with:** a one-shot session. Claude Code on Opus (`opus`) at `medium` effort, or Codex on Luna (`gpt-6-luna`) at `medium` reasoning. Paste that host's prompt below.
**Work surface:** Backend
```

### Classify the work surface

Record whether the item changes an interface people see or operate:

| Value | Meaning |
| --- | --- |
| `UI` | Any part of the work changes pages, screens, windows, visual styling, on-screen interactions or generated HTML views, even when it also changes backend code |
| `Backend` | No part of the work changes such an interface |
| `Unknown` | The evidence cannot settle it; the `**Missing:**` line names the evidence needed |

When the owning project defines UI, such as in a UI approval policy, classify
by that definition. Otherwise command-line output, APIs, prose documentation
and agent instructions are `Backend`. Classify from the item's scope and affected sources, not from
the repository's usual kind of work. The line records a fact for readers and
consumers such as project guides. It adds and waives no gate: project policy
alone decides UI review and human approval.

### Write each prompt

Each implementation prompt is one paragraph that:

- asks the agent to use the deliver-work skill on the live work-item URL;
- states the model and thinking level the user selected, using the host's
  term (effort for Claude Code, reasoning for Codex);
- asks the agent to state its model and stop if it differs;
- tells it to take the level as stated rather than guess it, because an agent
  cannot reliably read its own effort; never ask it to report or verify its
  level;
- states the session type, the worker subagent settings, and authorizes the
  required reviewers by count and model; a cheaper prompt states the cheaper
  start's model and level in the same way;
- points at the item's Execution recommendation with its assessment date and
  asks the agent to say so before changing strategy;
- ends with "If deliver-work isn't available here, say so and stop."

For example:

```text
Use the deliver-work skill to deliver <work-item URL>. I started this session on Opus at medium effort. State the model you are running and stop if it is not Opus; take the effort as stated rather than guessing it. Run as a one-shot session: implement it yourself without worker subagents, and use two fresh read-only Opus reviewers for deliver-work's required Standards and Specification reviews. The issue's Execution recommendation (assessed <date>) is the basis; if what you find no longer fits it, say so before changing strategy. If deliver-work isn't available here, say so and stop.
```

`Investigate first` prompts replace deliver-work with a read-only request: name
the work-item URL and the question, the evidence to return and the authority
limit, and ask for no writes. Keep the model, level and recommendation rules
above, and end by asking the agent to say so and stop if a named skill it needs
is unavailable. Keep the prompts in the section itself so readers and guides
copy the saved text.

A recommendation never claims the current session changed models, effort was
applied, workers ran, or acceptance passed. In particular, a recommended Claude
session effort does not establish a per-call worker effort control or prove
inherited effort. Preserve the host adapter's observation rules. Do not launch
sessions, edit personal settings, or start delivery to make a recommendation.
At delivery pickup, recheck scope, model availability and host controls; refresh
the recommendation within existing authority when its assumptions changed.
