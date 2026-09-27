# Codex independent reviewer settings

Use when current collaboration tools expose model and reasoning overrides.
Inspect their actual schema and host model descriptions before calling.

Use this mapping for both Standards and Specification, independently of the
implementation row. Complexity or uncertainty may warrant stronger settings.

| Impact | Reviewer default | Rationale and limits |
| --- | --- | --- |
| Low or medium impact | Luna (`gpt-6-luna`) at `high` for each axis | Capable lower-cost verification is the default for routine work |
| High impact, even with a tiny diff | Strongest evidenced relevant choice of Sol (`gpt-6-sol`) at `high` or Astra (`gpt-6-astra`) at `high` | Use separate fresh reviewer contexts; inspect high-impact negative cases |

Spawn each reviewer with `collaboration.spawn_agent`, the exact selected model,
a supported `reasoning_effort`, `fork_turns="none"` and a self-contained brief.
Full-history forks inherit parent settings and cannot accept those overrides,
and they would carry implementation narratives into the review. Do not guess a
reasoning enum. Record requested parameters and returned runtime metadata
separately; a successful spawn proves the request succeeded, not the executing
model.

Astra in this table is an independent reviewer, not an implementation worker or
a replacement coordinator. Reviewer suitability remains a hypothesis until
evaluated on comparable work; a model listing is not live review verification.
Explicit user or project requirements and stronger evidence override these
defaults. Different models for the two axes remain optional. A fallback for a
rejected default stays within the GPT-6 models named here, never a GPT-5.x
model.
