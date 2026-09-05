---
name: domain-modeling
description: Discover and sharpen a repository's active domain vocabulary and decision model. Use when the user is defining, reconciling, or proposing changes to domain terms, concept boundaries, glossaries, context maps, or decision records; do not select merely to read existing vocabulary for another task.
---

# Domain modeling

Sharpen the language and recorded decisions that describe the domain. Treat
the repository's established vocabulary as authoritative until evidence or the
user resolves a conflict.

This skill grants no authority to edit files, update Jira or other trackers,
change OPSX artifacts, implement code, or perform Git or publication actions.
Propose vocabulary and decision-record edits by default. Write them only when
the underlying request authorizes the exact repository edits.

## Discover the authoritative model

1. Search the repository for its vocabulary sources and decision paths. Inspect
   applicable agent instructions, glossaries, context maps, schemas, contracts,
   decision logs, ADRs, specifications, code, and tests. Do not assume a root
   `CONTEXT.md` or `docs/adr/` convention.
2. Identify which source owns each meaning. When sources disagree, report the
   conflict instead of silently choosing the most convenient wording.
3. Read `CONTEXT.md` files as vocabulary only. They define terms and concept
   boundaries, not system behavior, acceptance criteria, or implementation.
4. Compare claims with code and other authoritative sources. Distinguish the
   implemented behavior from proposed or historical decisions.

Use [the context guidance](references/context.md) when defining or revising
domain vocabulary or a context map. Use [the decision-record guidance](references/decision-record-format.md)
when deciding whether and how to record a durable trade-off.

## Challenge and resolve

- Call out a term that conflicts with the authoritative vocabulary.
- Ask what a vague or overloaded word means in the concrete scenario.
- Propose one canonical term when several words describe the same concept.
- Test concept boundaries with edge cases that reveal different ownership,
  lifecycle, identity, or invariants.
- Compare every behavioral statement with the behavior source that owns it.
- Record unresolved contradictions and the evidence on each side.

Do not convert a vocabulary document into a behavior specification. Put
behavior, acceptance criteria, implementation knowledge, and delivery scope in
their repository-defined authoritative homes.

## Return proposals before writes

Return the proposed term, definition, avoided aliases, owning context, source
evidence, and exact destination. For a decision record, include the decision,
context, accepted trade-off, consequences worth preserving, and exact path that
matches the repository's convention.

If exact edit authority exists, show the proposed paths and changes before
writing, then limit the edit to those accepted destinations. Otherwise, stop
with the proposal.

Domain modeling prepares vocabulary and decision-record proposals. The
consuming repository defines the owners of scope, dependencies, planning,
and delivery. This skill does not publish, transition, commit, merge, close,
or implement. Return proposals to an authorized coordinating workflow when
one composed this step.

Apply the `unslop` skill to human-facing proposals without changing authoritative terms,
quotations, citations, or accepted decisions.
