---
name: codebase-design
description: Analyze or propose module interfaces, seams, locality, and testability within an established codebase. Use for focused code-structure and interface design work; use architect for a full architecture workflow, how for current runtime explanation, ownership or layering placement, and architectural critique, and why for historical rationale.
---

# Codebase design

Assess how a focused part of a codebase concentrates behavior behind an
interface, where it can vary, and how callers and tests observe it. Use the
repository's vocabulary. Terms such as service, component, API, module,
boundary, port, and adapter remain valid when authoritative project sources use
them.

This skill grants no authority to edit code, tests, documentation, trackers, or
configuration, and no authority to branch, commit, merge, publish, or perform
external effects. Return an assessment or design proposal.

Use `architect` for a full design-first architecture workflow that owns caller
contracts and broader module ownership. Use `why` to investigate historical
rationale. Use `how` when the user asks where an existing responsibility belongs
or asks to critique the current architecture. Use this skill only for a focused
interface, seam, module-structure, or testability design question.

## Ground the assessment

1. Read applicable repository instructions, vocabulary, architecture sources,
   contracts, callers, implementations, and tests.
2. State the requested scope and the behavior that callers need.
3. Identify the current interface, including signatures, invariants, ordering,
   errors, configuration, and material performance constraints.
4. Trace where knowledge and changes spread across callers and implementations.

Do not impose a generic vocabulary or architecture style over repository-owned
terms and constraints.

## Apply design heuristics

Treat these as prompts for evidence, not universal rules:

- **Depth:** an interface may be stronger when callers learn less to exercise
  more relevant behavior. Extra implementation size does not prove depth.
- **Locality:** a design may be stronger when one behavior change and its
  verification remain concentrated instead of spreading across callers.
- **Seam:** a place where behavior can vary may deserve an explicit contract
  when real production and test or alternate implementations need it.
- **Adapter:** an adapter may clarify a real integration boundary, but one
  implementation does not automatically justify another abstraction.
- **Test surface:** stable observable behavior is usually a better test target
  than private structure, while risk may still require tests at several levels.
- **Dependency control:** accepting a dependency may improve substitution and
  testing, but direct construction can remain appropriate for stable local
  details.

Read [the deepening reference](references/deepening.md) when assessing whether
to combine shallow layers or place a seam across a dependency. Read [the
alternative-design reference](references/alternative-designs.md) when the user
wants materially different interface options compared.

## Return a focused proposal

Describe the current pressure, proposed interface or structure, hidden behavior,
seam placement, dependency treatment, caller migration implications, test
strategy, and trade-offs. Mark each recommendation as a heuristic judgment and
cite repository evidence that makes it fit this codebase.

Do not implement the design. Follow the repository's authoritative scope,
change records, and delivery workflow. Codebase design returns a proposal; it
does not publish, transition, commit, merge, close, or implement on its own.

Apply the `unslop` skill to the user-facing assessment without changing repository terms,
code, contracts, paths, or evidence.
