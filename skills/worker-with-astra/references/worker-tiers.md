# Select an advisory worker

Read before spawning. Confirm the exact model and effort are supported by the
current host; names and defaults are hypotheses, not measured savings.

| Work | Default | Routine decisions | Consult before |
| --- | --- | --- | --- |
| Bounded low/medium complexity and impact with reliable checks | Terra (`gpt-5.6-terra`) at `medium` | Local implementation and tests within agreed interfaces | Changing interfaces, scope, ownership, or acceptance; consequential uncertainty |
| Open-ended implementation with separable decision points | Sol (`gpt-5.6-sol`) at `medium` | Design details within the agreed approach and constraints | Cross-component decisions, disproved assumptions, or changed risk |
| High complexity or impact with useful checkpoints | Sol at `high`, or direct coordinator work | Agreed bounded steps with coordinator-owned writes | Consequential decisions and blockers |

Preserve a stronger supported choice supplied by the composing workflow or
explicit instructions. An explicit unavailable model or effort blocks that
selection; never silently substitute. Continuous difficult reasoning favors
direct coordinator work. Astra is the original advisor, never a replacement
implementation worker. Luna is outside this pairing.

Both approach and final-review consultations are mandatory for every tier.
Tier boundaries add consultations; they cannot remove those two checkpoints.
Normal corrections reuse the worker. Only the composing workflow selects a new
attempt after diagnosis under its shared handoff policy; this tier table does
not define another retry budget.
