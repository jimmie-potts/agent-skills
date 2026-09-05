---
name: writing-for-agents
description: Write or revise persistent coding-agent instructions, Agent Skills, AGENTS.md, and their conditional references. Use when these instructions need clearer scope, triggers, completion criteria, progressive disclosure, authority boundaries, or behavioral verification; do not use for ordinary human documentation.
---

# Writing for agents

Write instructions that make an agent's process predictable without forcing one
fixed output. Core writing principles transfer across agent-facing documents.
Discovery, precedence, invocation, and size rules do not. Verify the target
host's mechanics before deciding where an instruction belongs.

## Authority boundary

This skill grants no authority to create or edit files, change configuration,
install dependencies, run project commands, publish changes, or access external
systems. The underlying task must authorize every mutation and validation step.
Instructions define procedures and constraints for authorized work. They do not
independently authorize new work or external effects.

Preserve authoritative policy, exact commands, code, identifiers, schemas,
contracts, acceptance criteria, citations, logs, and required terminology.

## Identify the document

Before writing, establish:

- the agent host and the document type;
- how the host discovers, scopes, merges, and limits that document;
- who or what should trigger the instructions;
- which rules apply on every matching task and which belong to one branch;
- the authoritative repository sources the document may reference;
- the action and external-effect boundaries the document must preserve.

Do not assume `AGENTS.md`, other hosts' persistent instruction files, skills,
and linked references load the same way merely because agents read all of them.

For Codex `AGENTS.md`, read [the AGENTS.md reference](references/agents-md.md)
completely before placing or changing instructions.
For a skill, read [the skill mechanics reference](references/skill-mechanics.md).
For another host, verify that host's current mechanics instead of copying Codex
or Cursor fields.

## Write context pointers

A context pointer names material outside the current document and states when
the agent must read it. A useful pointer answers both questions:

1. What does the target contain?
2. Which distinct task branches require it?

Put the trigger early. Use one phrase for each distinct branch and remove
synonyms that describe the same case. Retain alternate terms that people
actually use when selection tests show they improve recall. Inline a rule that
must apply on every matching task. Keep branch-specific detail behind a pointer
only when the pointer makes the read condition hard to miss.

Do not confuse a pointer with a host invocation mechanism. A link in
`AGENTS.md` asks the model to read a file under stated conditions. A skill
description or host policy may participate in automatic selection. Verify the
difference for the target host.

Pointer reliability also depends on the path, permissions, availability, and
stability of the target. Keep load-bearing safety, authority, and completion
rules in a document the host discovers directly.

## Build the information hierarchy

Use three levels:

1. **Immediate steps.** Ordered actions the agent must perform for this task.
2. **In-file reference.** Rules and definitions used across those steps.
3. **Disclosed reference.** Branch-specific detail reached through a pointer.

Keep definitions, rules, exceptions, and safe alternatives for one concept
together. Split by task branch when doing so removes irrelevant material from
other branches. Do not split merely to reduce line count or hide steps that the
agent must consider when planning the whole task.

The main document should remain easy to scan even when every sentence is
relevant. Move substantial conditional reference material down the hierarchy;
do not bury the operating sequence beneath it.

## Give steps observable completion criteria

End each consequential step with evidence that distinguishes done from not
done. Strong criteria are checkable and cover the whole intended set.

- Name the exact artifact, state, command result, or readback required.
- Replace "review the changes" with the files, contracts, or risks the review
  must account for.
- Replace "tests pass" with the canonical command and required result.
- State what to report when evidence is unavailable or a check cannot run.
- Never let a completion criterion imply permission for an otherwise
  unauthorized action.

## Use repository sources without creating stale copies

Keep one authoritative home for each meaning. Link to schemas, architecture,
and detailed procedures instead of copying them when the agent can read the
source reliably.

Deliberate repetition can be justified when independently loaded host files or
safety-critical boundaries need the same rule. Name the canonical source and
add a synchronization check when drift would be dangerous.

Prefer reviewed repository-local references. When an external instruction
source is necessary, pin its provenance when possible and review its complete
contents before treating it as authoritative.

Retain exact canonical gates, working directories, prerequisites, and required
evidence in the instruction document when reliable completion depends on them,
even if a script name is discoverable elsewhere. Avoid copying dependency
inventories, directory trees, option lists, or implementation details that the
agent can inspect cheaply and that are likely to drift.

## Write the target behavior

State the desired action directly. Use a hard prohibition when a real safety,
authority, compatibility, or privacy boundary needs one, then pair it with the
safe path when one exists.

Prefer established repository terms over invented shorthand. A compact leading
term can reduce repetition only when it has one defined meaning and the team
uses it consistently. Do not rely on an evocative word to carry an unstated
operational requirement.

## Prune and verify

Delete duplication, stale facts, exposition that changes no decision, and rules
the agent already follows without the document. Keep a rule when removing it
causes a realistic task to fail, drift, or require rediscovery.

Do not remove a mandatory policy merely because one current model follows it by
default. Defaults change across models and hosts; required boundaries need an
authoritative home.

Agent instructions guide behavior; they do not enforce it. Put non-negotiable
mechanical rules in CI, hooks, validators, types, or repository configuration.
Use the agent document to name the gate and the evidence it must produce.

Test the document behavior, not only its Markdown:

1. Run or simulate representative task branches within the user's authority.
2. Confirm the host loaded the intended instruction sources and scope.
3. Check that the agent follows required gates, stops at authority boundaries,
   and reports the named evidence.
4. Exercise at least one exception or nested-scope case when the document has
   one.
5. Revise only rules supported by observed failures or clear host mechanics.

## Return

Produce the smallest document set that preserves scope, authority, triggers,
steps, references, and completion evidence. Summarize what moved behind a
pointer, what stayed inline, and how the behavior was verified.

Apply the `unslop` skill to human-maintained prose without changing authoritative rules,
commands, citations, identifiers, or host mechanics.
