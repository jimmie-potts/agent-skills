---
name: grilling
description: Resolve a plan or design through dependency-aware grouped questions. Use when the user explicitly asks to grill, stress-test, pressure-test, interrogate, or sharpen a plan, decision, architecture, or design, or when another workflow deliberately composes grilling; do not use for ordinary planning or summarization.
---

# Grilling

Resolve user-owned decisions before action. Model the discussion as a decision
tree: each unresolved decision may depend on decisions closer to the root.

This skill may investigate facts with authorized read-only tools. It grants no
authority to edit files, implement a plan, change documentation or trackers,
run Git operations, publish, or cause any other external effect.

## Build the decision tree

1. State the plan, decision, architecture, or design being tested.
2. Record decisions already settled by the user or an authoritative source.
3. Map every unresolved decision and the prerequisites that must be settled
   before the user can answer it without guessing.
4. Treat assumptions as unresolved decisions unless the user has accepted them
   or an authoritative source establishes them.

Investigate facts available through authorized read-only repository, web, or
external-system tools instead of asking the user. Preserve the user's decision
authority: evidence can answer a factual question, but it cannot choose a
trade-off for them. If a fact cannot be obtained within the task's authority,
identify it as an unresolved prerequisite. Pending fact discovery defers only
questions that depend on that fact; ask the rest of the current frontier now.

## Ask one frontier at a time

The current frontier contains every unresolved question whose prerequisites are
settled. Recompute it before every round.

Ask all independent frontier questions in one numbered group. For each question:

- state the decision in concrete terms;
- provide the viable choices when choices make the trade-off clearer;
- give a recommended answer and the evidence or reasoning behind it; and
- explain the observable consequence or acceptance boundary for that answer.

Render every numbered item with these explicit labels so none of the required
parts disappear in a compact response:

```text
1. <Decision>
   Choices: <viable choices, when useful>
   Recommendation: <recommended answer and why>
   Observable consequence or acceptance boundary: <what will be true or how acceptance is checked>
   Your answer: <the concrete choice requested from the user>
```

A frontier group is incomplete if any item lacks `Recommendation:` or
`Observable consequence or acceptance boundary:`. Do not shorten those fields
away, even when the choices appear obvious.

A one-question round is valid only when the frontier contains one question. Do
not ask a dependent question in the same round as its unresolved prerequisite.

After presenting the group, wait for the user's answers to the whole group.
Record each accepted answer, then recompute the tree and ask the new frontier.
Do not continue down one branch while other questions in the current group are
unanswered.

## Finish before action

When no answerable frontier remains, return:

- accepted decisions and their observable boundaries;
- accepted assumptions;
- unresolved questions, including blocked factual prerequisites; and
- the next authorized workflow, if the user named one.

This substep returns decisions and questions only. Do not implement, edit
documentation, update trackers or planning artifacts, branch, commit, merge,
or publish inside it. The consuming repository defines the owners of scope,
dependencies, planning, and delivery. When composed by another authorized
workflow, return control to its coordinator; questioning neither grants nor
cancels the underlying request's authority.

Apply the `unslop` skill to the user-facing questions and summary without changing
accepted wording, evidence, or authority boundaries.
