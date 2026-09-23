# Codex independent reviewer settings

Use this mapping for both Standards and Specification, independently of the
implementation row. Complexity or uncertainty may warrant stronger settings.

| Impact | Reviewer default | Rationale and limits |
| --- | --- | --- |
| Low or medium impact | Luna (`gpt-6-luna`) at `high` for each axis | Capable lower-cost verification is the default for routine work |
| High impact, even with a tiny diff | Strongest evidenced relevant choice of Sol (`gpt-6-sol`) at `high` or Astra (`gpt-6-astra`) at `high` | Use separate fresh reviewer contexts; inspect high-impact negative cases |

Select reviewer overrides through the verified spawn schema in the [Codex adapter](codex-model-selection.md). Astra in
this table is an independent reviewer, not an implementation worker or a
replacement coordinator. Reviewer suitability remains a hypothesis until
evaluated on comparable work; a model listing is not live review verification.
Explicit user/project requirements and stronger evidence override these
defaults. Different models for the two axes remain optional. A fallback for a
rejected default stays within the GPT-6 models named here, never a GPT-5.x
model.
