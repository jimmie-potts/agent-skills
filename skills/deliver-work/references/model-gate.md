# Decide whether selected settings permit work

Read at pickup, before implementation or delegation, on resume and when setting
evidence changes. Apply the same decision separately to coordinator, worker and
reviewer roles; a coordinator's evidence says nothing about another agent.

Use [the decision helper](../scripts/model_gate.py) with Python 3 and an explicit
JSON evidence file: `python3 <skill-directory>/scripts/model_gate.py <input>`.
It reads only that file (or stdin with `-`), emits JSON and exits 0 for
`continue`, 2 for `ask`, 1 for `stop`, or 3 for `bootstrap-only`. Run it as a separate step and inspect
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

`phase` is `pickup`, `resume`, `setting-change` or `pre-launch`. `name` is `model` or
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

## Check an unstarted role without inventing runtime evidence

Before delegation, first check the active coordinator's evidence. For an
unstarted worker or reviewer, verify that the host exposes the selected launch
controls and no known override contradicts a required setting. Run the helper
with `phase: pre-launch` and the exact planned parameters in `requested`.
A required mismatch stops; missing required launch parameters asks for input.
A matching request returns `bootstrap-only`, never `continue`, and runtime
verification stays unknown. `run_if_allowed` does not execute assignment work
for this result. Exit 3 is a distinct launch checkpoint, not a successful
active-role check; never append assignment execution after it.

Choose the handoff supported by the selected role adapter. Apply its existing
read-only/no-descendant controls; this gate does not add a resumability requirement.

- **Resumable context:** launch an evidence-only bootstrap with the selected
  parameters. It returns available setting evidence and performs no assignment
  work, publication or delegation. Refresh its `pickup` input and dispatch the
  assignment to that context only after `continue`.
- **One-assignment context:** include the evidence check as the first step in
  its sole assignment. Supply the selected requirements and available evidence;
  the child must evaluate `pickup` before any implementation or review. It may
  perform the conditional assignment in that same turn only on `continue`.
  Otherwise its sole return reports the blocked gate and does no assignment
  work; a review axis remains incomplete. When the adapter restricts tools,
  provide this reference's decision rules as packet instructions and
  require its decision/evidence in the return; do not add tools, persistence or
  a second conversation to obtain a mechanical check. The coordinator checks
  the returned decision before accepting any artifact. This packet path is
  instruction-only, not execution of the helper or host enforcement.

After launch, use only actual exposed evidence for `pickup`. A successful spawn
remains a successful request: use launch selection as a declaration only if the
host separately exposes that selection or the owner explicitly declares it.
Otherwise ask for missing required input; do not turn launch parameters into
observed identity. Explicit verified identity still requires a qualified
observation. Advisory-only unknown settings can continue, with their limits
reported. Retain blocked contexts/results as pending or stop owned contexts
through supported controls; do not silently retry an ephemeral assignment.

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
