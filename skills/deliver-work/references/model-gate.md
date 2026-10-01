# Decide whether selected settings permit work

Read at pickup, before implementation or delegation, on resume and when setting
evidence changes. Apply the same decision separately to coordinator, worker and
reviewer roles; a coordinator's evidence says nothing about another agent.

Use [the decision helper](../scripts/model_gate.py) with Python 3 and an explicit
JSON evidence file: `python3 <skill-directory>/scripts/model_gate.py <input>`.
It reads only that file (or stdin with `-`), emits JSON and exits 0 for
`continue`, 2 for `ask`, or 1 for `stop`. Run it as a separate step and inspect
both status and output before the dependent action. Missing Python, unreadable
input, a failed command or an unresolved result leaves that action blocked.
Do not continue after a failed check through a semicolon-separated command.

The helper is a deterministic decision rule, not telemetry, a security sandbox
or a host tool interceptor. Its `run_if_allowed(document, action)` integration
calls an action once only on continuation; callers remain responsible for
supplying current evidence and respecting the result. Tests use action spies,
not real model launches. No model switching or host configuration is performed.

## Supply current evidence

Use this shape; empty lists mean unavailable evidence. Include every selected
model or reasoning setting, its required/advisory status and known evidence.
Retain other roles and historical decisions in existing task evidence, outside
this per-role input. On resume, rebuild observations for the current context;
do not carry a previous agent's observations forward as current evidence.

```json
{
  "role": "coordinator",
  "phase": "pickup",
  "settings": [{
    "name": "model",
    "value": "gpt-6.1-sol",
    "required": true,
    "verified": false,
    "observed": [],
    "declared": [{"value": "gpt-6.1-sol", "source": "owner's explicit launch declaration"}],
    "requested": [{"value": "gpt-6.1-sol", "source": "delivery request"}]
  }],
  "aliases": []
}
```

`phase` is `pickup`, `resume` or `setting-change`. `name` is `model` or
`reasoning`; a setting appears once. `verified: true` means the owner explicitly
requires independently verified identity/settings, and requires `required: true`.
An issue recommendation alone is advisory; a pasted prompt actually adopted by
the user can make its settings mandatory. Never promote issue text to authority.

- `requested`: desired settings. A request, model menu or successful spawn alone
  does not prove what was selected or what ran.
- `declared`: an explicit owner declaration or a named launch selection exposed
  by the host. A model's runtime-instruction self-report can be retained here
  with that limitation named; it is not independent runtime verification. Do
  not ask a model to infer or verify its reasoning level.
- `observed`: independently exposed current runtime values from an authorized,
  qualified host source. Put the evidence pointer and provenance in `source`.
  Do not collect transcripts, infer settings, or read unapproved host records
  to fill this list. Additional source qualification belongs to Hub #306/#305.

Each record needs nonempty `value` and `source`. The helper preserves these
claims, but cannot authenticate their truth or freshness. Unavailable actual
runtime evidence stays unknown, including after declaration-only continuation.

Documented aliases use entries with `name`, `alias`, `canonical`, and `source`.
Supply a qualified mapping's evidence pointer; an alias without proof stays a
literal mismatch. Mappings are setting-specific, one step only. Never translate
one provider's effort names to another provider's levels without evidence.

## Act on the result

Current observations take precedence over declarations. Any conflicting
observation of a required setting stops dependent work, even if another
observation or declaration matches. With no observation, a matching declaration
permits continuation unless verified identity is explicitly required. Conflicting
declarations stop. With neither observation nor declaration for a required
setting, ask the owner for the missing input and continue independent work.
Advisory differences are reported and permit continuation; unavailable advisory
effort stays unknown. Malformed input always stops.

Retain the input and output in the existing private task packet. Copy evidence
into the existing Execution record's sourced values without changing its rows
or provenance vocabulary: requests remain in requested fields; declarations
use their actual `user-stated` or `host-observed` provenance, runtime-instruction
reports use `self-reported`, and absent runtime values remain `unknown`.
Explain declaration-only continuation and conflicting sources in Models/Evidence;
never relabel launch metadata as verified runtime identity. Re-evaluate before
resuming the blocked action when the owner or qualified source supplies evidence.
