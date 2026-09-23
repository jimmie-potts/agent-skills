# Claude Code worker selection and continuation

Use with the [Claude Code adapter](claude-code-model-selection.md) for worker
roles only. Start from published tier guidance and adjust to evidence: Sonnet
for everyday bounded coding, mechanical work, and read-only investigation, Opus
for high complexity or impact. Do not select `haiku` for any worker, scout, or
investigation role. Direct coordinator implementation is the
baseline for cost per completed task. For worker-with-fable, discover its
installed package and read references/claude-code.md and
references/worker-tiers.md; do not copy the consultation protocol here.

## Map assessment evidence to tiers

Read the ratings from the work-assessment contract and the implementation-selection
policy, then choose the concrete alias here. Ratings describe the
work; this table is the host mapping, adjusted to actual evidence.

| Assessment evidence | Strategy | Worker alias | Coordinator role |
| --- | --- | --- | --- |
| Narrow read-only question: locate files, trace a path, find tests | Fresh built-in `Explore` scout with read-only tools | Explicit `sonnet`, verified from the host | Return focused evidence; no advisor loop |
| Low complexity, low impact, strong existing checks, mechanical change | Assigned worker or advisory pairing | `sonnet` first, `opus` after a failed bounded attempt | Applies patches; advises at approach and final review |
| Low or medium complexity, low or medium impact, bounded coding | Advisory pairing when hard decision points exist; otherwise assigned worker | `sonnet` first, `opus` after a failed bounded attempt | Advises at approach, blockers, final review |
| High complexity, separable into checkpoints | Advisory pairing | `opus` | Advises; expect a smaller advisor gain and a higher consultation count |
| High complexity, continuous difficult reasoning | Direct implementation | none | Fable implements; no worker |
| High uncertainty | Investigation before dependent implementation | `sonnet` for a bounded read-only investigation, or none | Resolves facts; brings product decisions to the user; no tier change |
| High impact, any complexity | Advisory pairing with coordinator-owned writes, or direct implementation | `opus` | Applies every write; strong-capability independent reviews |
| Many independent pieces | Parallel workers | `sonnet` per piece | Decomposes, merges, reviews; no advisor loop per piece |

Direct implementation is the baseline in every row: choose a worker only when
its cost per completed task, including consultations and corrections, beats
Fable doing the work at the current session effort. A worker on `fable` is not
a pairing.

## Scout and escalate within the selected strategy

For narrow fact-finding, select the built-in `Explore` type only after the host
confirms that type and its read-only tools. Give it a fresh, bounded brief with
required project instructions, the question, source revision, and the evidence
to return. It has no advisor loop and performs no writes. A local definition
can replace `Explore`; verify that it preserves the intended tool restrictions.
If the scout cannot be established, investigate directly within existing scope.

The [subagent docs](https://code.claude.com/docs/en/sub-agents#built-in-subagents)
confirm read-only Explore with Write and Edit denied. Its documented default
now inherits the session model, capped at Opus on the Claude API; other
providers inherit directly, and configured overrides can change that behavior.
Do not rely on that default: request `sonnet` explicitly through the supported
model parameter and record the returned identity evidence. Explore skips
CLAUDE.md, so supply the applicable instructions in its brief. Its separate
context keeps detailed exploration out of the coordinator's transcript;
[Claude Code cost guidance](https://code.claude.com/docs/en/costs#delegate-verbose-operations-to-subagents)
describes that context benefit.

For default-selected bounded coding at low or medium ratings, start with
Sonnet. If a completed bounded attempt fails acceptance, diagnose the failure
signal first. A missing decision, permission, dependency, or broken check needs
its own resolution, not a stronger model. When the gap is worker capability,
return the failed attempt and evidence to this coordinator, reassess, and
select Opus for the next attempt with a changed brief naming the failure,
correction, and expected verification. Count the failed attempt in task cost.
An explicitly requested tier has no automatic fallback.

Within a pairing, keep the same worker for ordinary corrections and every
consultation. End and report a failed optional attempt before the composing
workflow selects a new attempt; never pass a fresh spawn off as a resume or
replace the advisor. Each new pairing must establish its prerequisites and
retain both mandatory consultations and coordinator-owned writes.

Use the [shared attempt-handoff contract](worker-continuation.md) for replacement
and the pairing adapter for host mechanics. If the diagnosed capability gap
persists at Opus, return the unresolved work and evidence to the original Fable
coordinator at its existing settings; do not spawn Fable as an implementation
worker or loop through further unsupported tiers.

For delivery, include the shared [task packet](resumption.md) or an authorized
reference in each SendMessage resumption or replacement brief. Match returned
task, assignment and source revision before applying a patch. Retained context
may be stale; preserve attempt history and unknown identity/effort evidence.

This Sonnet-to-Opus policy is a hypothesis inspired by Anthropic's
[retry-at-higher-capability measurements](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence#tune-effort),
which varied effort within one model, not this exact tier sequence. It needs
reliable failure detection and may increase latency on failures. Measure cost
per completed task; the shared reassessment rule still treats a stronger tier
as a changed approach. High-rated rows and explicit requirements take priority.
