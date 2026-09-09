# Codex selection adapter

Use only when current collaboration tools expose model and reasoning overrides.
Inspect their actual schema and host model descriptions before calling. Policy
does not add capabilities or override host permissions.

For a supported override, use collaboration.spawn_agent with the exact selected
model and supported reasoning_effort, fork_turns="none", and a self-contained
brief. Full-history forks in this host inherit parent settings and cannot accept
those overrides. If inheritance is intended, omit overrides and report inherited
settings only to the extent observable. Do not guess a reasoning enum.

Record requested parameters and actual returned runtime metadata separately.
A successful spawn establishes the request succeeded, not independent proof of
the executing model's identity. Disclose unknown identity; handle a verified
mismatch against explicit requirements before dependent work. Model options
alone never prove that the current coordinator is Astra.

For sol-with-astra, discover its installed package and follow its
references/codex.md rather than copying the consultation protocol. Keep durable
writes with this delivery coordinator. Fresh independent review briefs carry
the fixed comparison and raw sources without prior approval narratives.

## Map assessment evidence to settings

Read the ratings from the work-assessment contract and the role table in the
selection policy, then choose the concrete Codex setting here. The roles
follow Eric Provencher's
[Practical multi-agent orchestration in Codex](https://x.com/pvncher/article/2080707291603407077)
and [Choosing GPT-5.6 Sol, Terra, or Luna in Codex](https://x.com/pvncher/status/2077708372363624894).
Confirm the host's current model list, spawn identifiers, and reasoning enum
before use; the table adds neither. The identifiers this catalog records are
`gpt-6-astra` as coordinator, `gpt-5.6-sol` as worker, and `gpt-5.6-terra`
as worker. Sol was verified in live spawns; Terra was supplied by the
maintainer and awaits a recorded spawn.

The `reasoning_effort` values documented for `collaboration.spawn_agent` are
`low`, `medium`, and `high`, and this catalog has observed `medium` and `high`
in spawns. Codex session and config settings also accept `xhigh` and `max`
through `model_reasoning_effort`. Whether a spawn call accepts those two is
unverified, and "Ultra" in community writing has no confirmed mapping to
either. Do not request `xhigh` or `max` for a worker unless the host's spawn
schema lists it, and never present a rejected setting as applied.

The Codex lineup by role:

- Astra (GPT-6) is the coordinator and advisor. It plans, delegates, tracks
  workers, and answers consultations. It is not spawned as a worker.
- Sol (GPT-5.6) is the worker for the advisory pairing and for open-ended or
  hard implementation. Its reasoning setting is the main lever: `low` for a
  read-only scout, `medium` as the baseline for scoped implementation, `high`
  for difficult implementation and ambiguity.
- Terra (GPT-5.6) is the everyday implementation and testing worker for
  scoped multi-step work with clear boundaries, at `high`. Multi-agent v2
  spawns Sol and Terra as subagents.
- Luna (GPT-5.6) is the fast option for extraction, classification,
  transformation, and structured summaries. It is not spawnable as a
  subagent in multi-agent v2; do not select it for delegated work.

| Assessment evidence | Strategy | Worker and reasoning | Coordinator role |
| --- | --- | --- | --- |
| Narrow read-only question: locate files, trace a path, find tests | Parallel scouts | Sol at `low`, `fork_turns="none"`, read-only | Sends focused scouts in parallel; merges findings; no advisor loop |
| Low complexity, low impact, strong existing checks, mechanical change | Assigned worker or advisory pairing | Terra at `high` as an assigned worker; Sol at `medium` for the pairing | Applies patches; advises at approach and final review |
| Low or medium complexity, low or medium impact, bounded coding | Advisory pairing when hard decision points exist; otherwise assigned worker | Sol at `medium` for the pairing; Terra at `high` as an assigned worker | Advises at approach, blockers, final review |
| High complexity, separable into checkpoints | Advisory pairing | Sol at `high` | Advises; expect a higher consultation count |
| High complexity, continuous difficult reasoning | Direct implementation | none | Astra implements; no worker |
| High uncertainty | Investigation before dependent implementation | Sol at `low` scouts for facts, Sol at `medium` for a bounded read-only investigation, or none | Resolves facts; brings product decisions to the user; no setting change |
| High impact, any complexity | Advisory pairing with coordinator-owned writes, or direct implementation | Sol at `high` | Applies every write; strong-capability independent reviews |
| Many independent pieces | Parallel workers | Terra at `high` per scoped piece; Sol at `medium` for open-ended pieces | Decomposes, merges, reviews; no advisor loop per piece |

Direct implementation is the baseline in every row: choose a worker only when
its cost per completed task, including consultations and corrections, beats
Astra doing the work. A worker on Astra is not the pairing, and the pairing
itself is always Sol; Terra is for assigned and parallel workers. Give every
leaf worker a boundary against spawning further agents, respect the host's
concurrency limit, and keep the coordinating turn available to the user while
workers run.

Call collaboration tools through the interface actually exposed by the host.
Do not launch replacement sessions, change personal settings, install adapters,
or simulate multiple models by writing both sides of a conversation.
