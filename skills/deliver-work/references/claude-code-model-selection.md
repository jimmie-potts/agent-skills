# Claude Code selection adapter

Use only when the host exposes an `Agent` tool with a per-call `model`
parameter and a `SendMessage` tool that resumes a spawned agent. Inspect their
actual schemas and the host's model descriptions before calling. Policy does
not add capabilities or override host permissions.

For a supported override, call `Agent` with the exact selected model alias, a
self-contained brief, and foreground execution when the next step depends on
the result. Subagents inherit no conversation and cannot message the
coordinator mid-run; they return a report, and `SendMessage` resumes the same
agent. The tool exposes no per-call reasoning control. Record the host default
as the observed setting and do not report an override the host cannot apply.
Do not create `.claude/agents` definitions or change settings to obtain a
model.

Record requested parameters and the model the worker reports from its own
runtime instructions separately. A successful spawn establishes that the
request succeeded, not independent proof of the executing model. Disclose
unknown identity; handle a verified mismatch against explicit requirements
before dependent work. Spawn options alone never prove that the current
coordinator is Fable; read the coordinator's own runtime instructions.

Start from Anthropic's published tier guidance and adjust to evidence: Sonnet
for everyday bounded coding, Haiku for mechanical work with strong checks,
Opus for high complexity or impact, and the coordinator implementing directly
as the baseline to beat on cost per completed task. For worker-with-fable,
discover its installed package and follow its references/claude-code.md and
references/worker-tiers.md rather than copying the consultation protocol. Keep
durable writes with this delivery coordinator. Fresh independent review briefs
carry the fixed comparison and raw sources without prior approval narratives;
a reviewer may run on a different tier from the implementer when evidence
justifies it.

## Map assessment evidence to tiers

Read the ratings from the work-assessment contract and the role table in the
selection policy, then choose the concrete alias here. Ratings describe the
work; this table is the host mapping, adjusted to actual evidence.

| Assessment evidence | Strategy | Worker alias | Coordinator role |
| --- | --- | --- | --- |
| Low complexity, low impact, strong existing checks, mechanical change | Assigned worker or advisory pairing | `haiku` only with a known test and per-step returns; otherwise `sonnet` | Applies patches; advises at approach and final review |
| Low or medium complexity, low or medium impact, bounded coding | Advisory pairing when hard decision points exist; otherwise assigned worker | `sonnet` | Advises at approach, blockers, final review |
| High complexity, separable into checkpoints | Advisory pairing | `opus` | Advises; expect a smaller advisor gain and a higher consultation count |
| High complexity, continuous difficult reasoning | Direct implementation | none | Fable implements; no worker |
| High uncertainty | Investigation before dependent implementation | `sonnet` for a bounded read-only investigation, or none | Resolves facts; brings product decisions to the user; no tier change |
| High impact, any complexity | Advisory pairing with coordinator-owned writes, or direct implementation | `opus`; never `haiku` | Applies every write; strong-capability independent reviews |
| Many independent pieces | Parallel workers | `sonnet` per piece, `haiku` for mechanical pieces with checks | Decomposes, merges, reviews; no advisor loop per piece |

Direct implementation is the baseline in every row: choose a worker only when
its cost per completed task, including consultations and corrections, beats
Fable doing the work. A worker on `fable` is not a pairing.

Do not launch replacement sessions, change personal settings, install
adapters, or simulate multiple models by writing both sides of a conversation.
