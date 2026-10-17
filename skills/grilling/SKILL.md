---
name: grilling
description: Resolve a plan or design through dependency-aware grouped questions. Use when the user explicitly asks to grill, stress-test, pressure-test, interrogate, or sharpen a plan, decision, architecture, or design, or when another workflow deliberately composes grilling; do not use for ordinary planning or summarization.
---

# Grilling

Interview the user until you reach a shared understanding. Map it as a design
tree: every decision branches into the decisions that hang off it.

Work in rounds. The frontier is every unresolved decision whose prerequisites
are settled. Ask the whole frontier in one numbered round, each with your
recommended answer and what it would change, then wait for all the answers.
A question that depends on another still-open question waits for a later round.
Recompute the frontier after each round.

```text
1. <Decision>: <question, with choices when useful>
   Recommendation: <answer and why>
```

Finding facts is your job: look them up with read-only tools instead of asking.
Only questions downstream of a pending lookup wait for it. Decisions belong to
the user; evidence can inform a trade-off but not choose it.

Finish when the frontier is empty. Return accepted decisions, accepted
assumptions and open questions, then stop. Grilling is read-only: take edit, Git,
tracker, comment or publishing actions only when the request, or the
coordinating workflow's existing authority, explicitly covers them. Use `unslop` on the questions and summary when needed.
