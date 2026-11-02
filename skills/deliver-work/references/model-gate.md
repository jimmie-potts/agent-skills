# Honor explicitly required settings

Read only when the user or project explicitly requires a model, reasoning level
or verified runtime identity. Ordinary delivery and advisory recommendations
need no model gate, evidence-only bootstrap or owner declaration.

Check that the requirement applies to this role and context. Use supported
launch controls; report an unavailable required control before dependent work.
A matching owner declaration or host-exposed selection permits continuation
unless independent verification was explicitly required. Unknown runtime
metadata remains unknown. A known contrary runtime observation takes precedence
and stops the affected work. Do not infer aliases, cross-provider equivalence,
a child's settings from its parent, or verification from a successful request.

Recheck when the requirement, role or observed setting changes. Reuse applicable
unchanged evidence across continuation; do not ask again merely because a turn
ended. Ask only for missing evidence needed by an explicit requirement and
continue independent work. Keep declaration scope and known conflicts in the
existing task evidence. Never ask an agent to verify its own thinking level.

## Optional mechanical check

If the project requires a machine-readable decision, use
[the decision helper](../scripts/model_gate.py):
`python3 <skill-directory>/scripts/model_gate.py <input>`.
It reads a JSON file or stdin with `-` and changes no host settings. Inspect its
output and exit status: `continue` (0), `ask` (2), `stop` (1), or
`bootstrap-only` (3). Failed, malformed or unresolved checks cannot satisfy a
project requirement to use the helper. `run_if_allowed` invokes its action only
on `continue`; `bootstrap-only` permits launch, not assignment execution.
A project requiring the helper must obtain a current-role `continue` result
before dependent assignment work. Do not add tools to a restricted reviewer;
provide the decision rules and evidence in its packet where that adapter allows
instruction-only evaluation.

The helper validates supplied claims, not their truth. Its tests use action
spies, not real model launches. Retain input and output only in existing
permitted evidence. This optional interface preserves existing integrations:

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
