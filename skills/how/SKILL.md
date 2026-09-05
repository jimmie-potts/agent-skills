---
name: how
description: Explain how code, a subsystem, or a runtime flow works and where new behavior belongs. Use for code walkthroughs, architecture onboarding, ownership or layering questions, and architectural critiques; use why for historical motivation.
---

# How

Build a working mental model from the implementation. Explain the behavior at
the level needed to change it safely, not as an annotated source listing.

## Authority boundary

Use read-only repository inspection by default. This skill grants no authority
to fetch remote refs, install dependencies, modify files, run untrusted code,
or query external systems. Follow the user's request, repository instructions,
and host approval policy. Do not infer behavior from filenames when the actual
implementation is available.

## Choose a mode

- **Explain** is the default. Trace the implementation and describe its
  architecture and runtime behavior.
- **Placement** answers where a proposed responsibility should live. Compare it
  with existing ownership, dependency direction, and nearby patterns.
- **Critique** applies only when the user asks for problems or improvements.
  Explain the current design first, then judge its architecture.

## Explain workflow

1. State the target and your interpretation if the question is ambiguous.
2. Find the entry point. Search for relevant symbols, routes, handlers, jobs, or
   configuration, then read their implementations.
3. Trace the flow from trigger to effect. Follow callers, callees, data
   transformations, persistence, side effects, error paths, and boundaries.
4. Map the key abstractions and their ownership. Name the files and symbols that
   define each important responsibility.
5. Check tests, schemas, configuration, and consumers that constrain the
   behavior. Separate implemented behavior from caller-driven assumptions.
6. Reconcile contradictions by returning to the code. State unresolved gaps
   instead of guessing.

For a narrow question, investigate directly. For a broad subsystem, split the
inspection into distinct angles only when parallel reviewers are available and
the user has explicitly requested delegation or parallel work. Otherwise trace
the slices sequentially.

## Placement workflow

Before recommending a location, identify:

- the responsibility's source of truth and lifecycle;
- the layer that already owns similar decisions;
- the allowed dependency direction;
- the callers and consumers that would change;
- whether the proposal introduces a new abstraction or extends a real one.

Recommend one location and explain why it owns the behavior. Name credible
alternatives and the concrete boundary each would violate or complicate.

## Critique workflow

Explain the current design before evaluating it. Review only lenses that apply:

- abstraction fit and accidental coupling;
- data-model fit and runtime honesty;
- boundary validation, error propagation, and test isolation;
- likely evolution paths and hard-coded assumptions;
- complexity relative to delivered value;
- consistency with established repository patterns.

For every finding, give severity, affected components, evidence, and practical
impact. Do not prescribe a rewrite without demonstrating a current problem. An
empty findings list is valid.

## Return

- **Overview.** What the subsystem does and why it exists in the current design.
- **Key concepts.** The few types, services, or abstractions needed to follow it.
- **How it works.** A step-by-step runtime or data flow with concrete paths and
  symbols. Use a diagram only when it materially clarifies a multi-part flow.
- **Where things live.** A short ownership map for the relevant files.
- **Gotchas and gaps.** Non-obvious behavior, sharp edges, and anything not
  verified.
- **Placement or critique.** Include only when the requested mode calls for it.

Apply the `unslop` skill to the final human-facing explanation without changing code,
identifiers, citations, or technical meaning.
