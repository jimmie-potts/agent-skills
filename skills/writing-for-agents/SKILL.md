---
name: writing-for-agents
description: Write or revise persistent coding-agent instructions, Agent Skills, AGENTS.md, and their conditional references. Use when these instructions need clearer scope, triggers, completion criteria, progressive disclosure, authority boundaries, or behavioral verification; do not use for ordinary human documentation.
---

# Writing for agents

The companion skill `unslop` named here comes from the installed pstack plugin and runs with upstream behavior.

Write instructions that make an agent's process predictable. Writing
principles transfer between hosts; discovery, precedence, invocation and size
limits do not, so check the target host's current docs before placing a rule.
For a skill, read [the skill mechanics reference](references/skill-mechanics.md).

## Write

- **Pointers.** Name what an outside file contains and the task branch that
  needs it, trigger first. Rules that apply to every matching task stay inline;
  safety, authority and completion rules live in a file the host loads directly.
- **Hierarchy.** Ordered steps first, then rules used across them, then
  branch-specific detail behind pointers. Keep one concept's rules and
  exceptions together.
- **Completion.** End each consequential step with checkable evidence: the
  exact command and result, artifact or readback, and what to report when it
  can't run.
- **One home per meaning.** Link schemas and procedures instead of copying
  them. Keep exact gates and commands inline when completion depends on them.
- **Direct language.** State the desired action; pair a hard prohibition with
  the safe path. Use the repository's own terms.

## Prune and verify

Delete duplication, stale facts and rules the agent already follows. Keep a
rule when removing it would make a realistic task fail. Anything mechanical
belongs in CI, hooks, validators or types; the document just names the gate.

Test behavior, not Markdown: run representative requests, including one near
miss and one exception, and confirm the right sources loaded and the gates held.

Return the smallest document set that keeps scope, triggers, steps and
evidence, and say how it was verified. Use `unslop` on human-maintained prose
without changing rules, commands or identifiers.
