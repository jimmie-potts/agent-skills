# Claude Code selection adapter

Use only when the host exposes an `Agent` tool with a per-call `model`
parameter. Require `SendMessage` resumption only when the selected strategy
continues a retained worker, including every advisory pairing. A one-return
scout does not need resumption. Inspect the actual tool schemas and host model
descriptions before calling; policy adds no capabilities or permissions.

For a supported override, call `Agent` with the exact selected model alias, a
self-contained brief, and foreground execution when the next step depends on
the result. Subagents inherit no conversation and cannot message the
coordinator mid-run; they return a report, and `SendMessage` resumes the same
agent. The tool exposes no per-call reasoning control. A worker inherits
session effort unless an existing host override applies. Record the effective
level when exposed or stated, otherwise unknown; use a known session level
only when inheritance is established. Report known mismatches with the
selected role setting, without claiming to change effort.
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
| Narrow read-only question: locate files, trace a path, find tests | Fresh built-in `Explore` scout with read-only tools | Explicit `haiku` or `sonnet`, verified from the host | Return focused evidence; no advisor loop |
| Low complexity, low impact, strong existing checks, mechanical change | Assigned worker or advisory pairing | `sonnet` first for coding, `opus` after a failed bounded attempt; `haiku` only for non-coding mechanical work with a known check and per-step returns | Applies patches; advises at approach and final review |
| Low or medium complexity, low or medium impact, bounded coding | Advisory pairing when hard decision points exist; otherwise assigned worker | `sonnet` first, `opus` after a failed bounded attempt | Advises at approach, blockers, final review |
| High complexity, separable into checkpoints | Advisory pairing | `opus` | Advises; expect a smaller advisor gain and a higher consultation count |
| High complexity, continuous difficult reasoning | Direct implementation | none | Fable implements; no worker |
| High uncertainty | Investigation before dependent implementation | `sonnet` for a bounded read-only investigation, or none | Resolves facts; brings product decisions to the user; no tier change |
| High impact, any complexity | Advisory pairing with coordinator-owned writes, or direct implementation | `opus`; never `haiku` | Applies every write; strong-capability independent reviews |
| Many independent pieces | Parallel workers | `sonnet` per piece, `haiku` for mechanical pieces with checks | Decomposes, merges, reviews; no advisor loop per piece |

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
Do not assume Haiku: request `haiku` or `sonnet` explicitly through the supported
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

Use the shared selection policy's attempt-handoff contract for replacement
and the pairing adapter for host mechanics. If the diagnosed capability gap
persists at Opus, return the unresolved work and evidence to the original Fable
coordinator at its existing settings; do not spawn Fable as an implementation
worker or loop through further unsupported tiers.

This Sonnet-to-Opus policy is a hypothesis inspired by Anthropic's
[retry-at-higher-capability measurements](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence#tune-effort),
which varied effort within one model, not this exact tier sequence. It needs
reliable failure detection and may increase latency on failures. Measure cost
per completed task; the shared reassessment rule still treats a stronger tier
as a changed approach. High-rated rows and explicit requirements take priority.

## Map impact to independent reviewers

Use this mapping for both Standards and Specification, independently of the
implementation row. Complexity or uncertainty may warrant stronger settings.

| Impact | Reviewer default | Rationale and limits |
| --- | --- | --- |
| Low or medium impact | `sonnet` for each axis | Capable mid-tier verification is the default for routine work |
| High impact, even with a tiny diff | Strongest evidenced relevant choice of `opus` or the coordinator's model, in separate fresh reviewer contexts | High reasoning recommended; apply the effort observation and capability-gap rules above |

Pass the reviewer model explicitly rather than inheriting it accidentally.
The coordinator's model here means a fresh independent reviewer on that model,
never the coordinating writer's own judgment. These are capability hypotheses,
not measured review-quality results. Explicit user/project requirements and
stronger evidence override the defaults; no effort control is added.

Do not launch replacement sessions, change personal settings, install
adapters, or simulate multiple models by writing both sides of a conversation.
