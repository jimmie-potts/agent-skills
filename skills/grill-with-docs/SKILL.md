---
name: grill-with-docs
description: Explicitly compose grilling with domain-modeling to resolve a plan or design and prepare exact vocabulary or decision-record proposals. Use when explicitly requested by the user or composed by an authorized workflow; do not write during questioning.
---

# Grill with docs

Load and follow both `grilling` and `domain-modeling`. Use `grilling` as the
control flow and `domain-modeling` to analyze vocabulary, concept boundaries,
authoritative sources, and durable decisions.

This composition grants no new authority. Read-only investigation must remain
within the underlying task's authority. Do not write files while questioning.

## Resolve decisions in grouped rounds

Map unresolved decisions and their dependencies. Ask every independent current
frontier question in one numbered group. Give a recommendation and observable
consequence or acceptance boundary for every question. Wait for the user's
answers to the whole group, then recompute the frontier. Keep dependent
questions for later rounds.

During each round, collect without writing:

- proposed canonical terms, definitions, avoided aliases, and owning contexts;
- conflicts among vocabulary, code, contracts, and other authoritative sources;
- decisions that may warrant a repository-defined decision record; and
- the evidence and unresolved location choices for each proposed change.

Treat `CONTEXT.md` as vocabulary only, never as a behavior specification. Find
the repository's actual vocabulary owners and decision paths instead of
assuming a filename or directory convention.

## Propose documentation after confirmation

After the user confirms the decisions, first return the accepted decisions,
assumptions, and unresolved questions. Then show every exact proposed path and
change. Match existing repository formats and keep behavior, delivery scope,
and implementation knowledge in their authoritative homes.

Write only when the underlying request explicitly authorizes those exact
repository edits. Without that authority, stop with the proposals. An explicit
invocation of `grill-with-docs` alone does not authorize a write.

This workflow prepares decisions, vocabulary changes, and decision-record
proposals. It does not create tracker work, publish plans, or implement code.
The consuming repository defines the owners of scope, dependencies, planning,
and delivery. Do not transition, commit, merge, close, publish, or implement
inside this substep. When composed by an authorized workflow, return the
accepted decisions to its coordinator without discarding existing authority.

Apply the `unslop` skill to questions and proposals without changing accepted wording,
evidence, citations, or authority boundaries.
