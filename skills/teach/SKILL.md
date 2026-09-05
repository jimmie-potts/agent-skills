---
name: teach
description: Explain a change, codebase, or subsystem so the user can build a practical mental model of what it is, how it works, and why it has that shape. Use only when the user explicitly asks to be taught or invokes teach; use how for a standalone implementation walkthrough and why for a standalone rationale investigation.
---

# Teach

Help the user understand the subject well enough to reason about it. Combine
implementation mechanics with evidence-backed rationale, then explain them at
the depth the conversation calls for. Do not change the subject being taught.

## Authority boundary

This skill grants no authority to modify files, fetch remote state, install
dependencies, access private sources, call live systems, or run untrusted code.
Use only evidence available within the original request's scope. Applying the
`how` or `why` skill provides a method, not additional access or mutation
authority.

## Build the lesson

1. Infer why the user is asking. They may be preparing to change the code,
   reviewing it, debugging it, or learning the area. Use conversation context
   instead of turning the exchange into a questionnaire.
2. Choose the few ideas the user needs to leave with. Skip concepts they
   already understand and spend detail where their question is concentrated.
3. Load and follow `how` to trace what the implementation does. Load and follow
   `why` when historical intent or constraints matter. For a small question,
   one may be enough. Preserve `why`'s confidence language and source gaps.
4. Investigate directly unless the user separately requests delegation or
   parallel reviewers. Do not repeat the same exploration after the companion
   skills have established it.
5. Start with the smallest complete explanation. Name the thing in ordinary
   technical language, connect it to this codebase, then walk through its
   behavior, reasons, and edge cases.
6. Stop at a natural boundary in an interactive lesson. Continue with the path
   the user chooses instead of delivering every possible detail at once.

## Teaching style

- Explain the mechanism. A list of files, functions, and constants is a map,
  not a lesson.
- Use one stable name for each concept. Do not make the reader reconcile
  synonyms for the same component.
- Lead with concrete code, data, or user actions. Use an analogy only when it
  makes the mechanism easier to understand.
- Keep one idea per paragraph. Split dense sentences before removing facts.
- Do not announce teaching scaffolding with phrases such as "key insight,"
  "the tricky part," or "the takeaway." State the point itself.
- Do not quiz the user, ask for a teach-back, or add artificial pause labels.
- Keep exact quotations, identifiers, paths, and confidence labels intact.

## Visuals

Use a visual only when it makes a relationship or sequence easier to grasp than
prose. For a flow with several moving parts, build the picture in small stages
instead of presenting one crowded diagram. Each stage should add one concept.
Skip diagrams for a single fact or a short linear path.

## Return

Return the explanation itself, not a report about the investigation. Begin with
one or two sentences that define the subject and its role here. Add the runtime
flow, design reasons, and edge cases in layers. Cite real paths and sources so
the user can inspect the evidence.

Apply the `unslop` skill to every human-facing response. Preserve `why`'s
confidence language, technical facts, citations, code, commands, and
identifiers.
