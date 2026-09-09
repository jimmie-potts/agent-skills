# Worker tiers and consultation depth

Read before selecting a worker. The tiers summarize Anthropic's published
model guidance for Claude Code's `haiku`, `sonnet`, and `opus` aliases. The
host's current model descriptions and the task's assessment take precedence
over these heuristics. Sources: [Choosing the right model](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model)
and [Optimizing for cost and intelligence](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence).

## When to pair at all

The advisor pattern pays when the task is serial work with a few hard decision
points: choosing an approach, recovering from a failure, settling scope. It
does not pay when every turn needs frontier judgment, when the task is one
short dependent chain that fits in one context, or when Fable at a lower
reasoning setting already meets the bar. Fable implementing directly is the
baseline every pairing has to beat, measured as cost per completed task rather
than tokens. Many independent pieces call for separate bounded workers under
the composing workflow's ordinary delegation, not this pairing.

The advisor hands over only capability the worker lacks, so a wider gap
between worker and Fable yields more from each consultation. Anthropic's cost
guidance names a frontier advisor over a mid-tier executor as the most
cost-effective configuration, which is why Sonnet is the default here. Its
measured evidence is narrower: the most accurate coding configuration it
reports is an Opus 5 worker under a Fable 5.1 advisor, and a Sonnet 5 worker
under Fable 5.1 matched Fable alone at medium effort within noise on one
research benchmark at higher cost. The Sonnet default is therefore a cost
hypothesis pending measurement, not a measured result.

## Tiers

| Tier | Use for | Decides alone | Returns to Fable |
| --- | --- | --- | --- |
| `haiku` (Claude Haiku 4.5) | Bounded mechanical work with strong existing checks: renames, fixture and documentation edits, evidence summaries, single-file changes with a known test | Nothing consequential; wording and ordering within one bounded step | After each bounded step, plus the mandatory approach and final-review consultations |
| `sonnet` (Claude Sonnet 5) | Default worker for coding, debugging, tests, and agentic tool use on bounded work with low or medium assessment ratings | Routine implementation choices consistent with the approved approach | Approach, blockers, final review |
| `opus` (Claude Opus 5) | Work whose implementation itself needs deep reasoning: high complexity, high impact, or large refactors where the consultation rate would otherwise be high | Routine design choices within the approved approach and scope | Approach, blockers, final review; expect a smaller advisor gain |
| `fable` | Not a worker tier. Fable implements directly when the task needs it. | | |

The version names in the table are the documented targets of the aliases at
authoring time, not identity evidence; the worker's own runtime report is.
Haiku has a smaller context window than the other tiers; keep its briefs and
source sets short. An explicitly requested tier has no fallback. A tier
selected by a composing workflow may fall back with disclosure under that
workflow's policy.

## Consultation rules

- Two consultations are mandatory: approach before substantial implementation,
  and final review before reporting completion. Workers under-consult without
  them, especially on coding work.
- Keep the worker at the host default reasoning setting. Reduced effort makes
  the worker stop noticing it is stuck.
- Record the consultation count. A worker consulting on nearly every decision
  means the task belonged to Fable directly; finish, then report that evidence
  for the next selection.
- After a failed worker attempt, change the approach or raise the tier rather
  than retrying the same worker with the same brief.
