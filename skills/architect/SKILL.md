---
name: architect
description: Design types, interfaces, module ownership, and caller usage before implementation, then use implementation feedback to revise the design. Use only when the user explicitly invokes architect, asks to architect or design non-trivial code, or requests a design-first implementation workflow.
---

# Architect

Design the code's shape before filling in behavior. Start from realistic caller
usage, derive types and signatures, compare structurally different designs, and
record why one shape won. Treat repeated implementation friction as evidence
that the design may be wrong.

## Authority boundary

This skill grants no authority to modify tracked files, implement code, install
dependencies, fetch remote refs, create commits or pull requests, query live
systems, or run untrusted code. Follow the user's requested outcome, repository
instructions, and approval policy.

If the user asks only for architecture or design, stop after the design package.
Implement only when the underlying task clearly requests implementation. A
design-first implementation request authorizes normal in-scope edits, not
publication or unrelated changes.

## Design phases

Track Ground, Frame, Explore, Choose, Implement, and Reconsider. Skip Implement
when the request is design-only.

### Ground

Build a concrete model of every existing subsystem the design will touch. Load
and follow `how` to trace runtime flow, ownership, data, and boundaries. Load
and follow `why` when historical constraints, incidents, compatibility
promises, or rejected
alternatives could constrain the new shape. Preserve `why`'s confidence labels
and gaps.

Skip repository grounding only for genuinely greenfield work. Even then, state
the external contracts and operational constraints that bound the design.

### Frame

State:

- the capability being designed and its intended users;
- required behavior, excluded scope, and compatibility constraints;
- dominant data access and state-transition patterns;
- failure, concurrency, security, and lifecycle constraints;
- the decisions the design must make before implementation can start.

Separate confirmed requirements from assumptions. Ask the user when an
unresolved choice would materially change ownership, public contracts, data
shape, or migration strategy.

### Explore

Read [the candidate design discipline](references/design-review.md) before
generating candidates. Write the caller's usage first, then derive data types,
function signatures, module boundaries, and data flow.

Load and follow `arena` to produce at least two structurally different candidate
designs when independent candidates are available. Give each candidate the
same grounding, constraints, and output contract. Different names around the
same module graph do not count as distinct designs.

If independent candidates are unavailable, compare two genuinely different
shapes in one design pass and disclose the limitation. Do not claim a
multi-reviewer result.

Candidate sketches may use pseudocode or non-executable signatures. Do not put
throwing stubs or unfinished bodies into production paths unless the task
explicitly authorizes a staged scaffold and its temporary breakage.

### Choose

Screen each candidate against the red flags in
[the design review](references/design-review.md). Compare viable candidates on:

- caller simplicity and misuse resistance;
- complexity hidden behind the public interface;
- ownership and dependency direction;
- data-model fit for dominant access patterns;
- boundary validation and invariant encoding;
- state ownership, idempotency, and failure recovery;
- migration cost and compatibility risk;
- testability and the cost of likely future changes.

Choose one coherent base. Port only compatible ideas from losing candidates.
Do not average designs with conflicting ownership or data models. Write the
result using [the rationale template](references/rationale-template.md).

Load and follow `interrogate` on the chosen design only when the user asks for
adversarial review or the original architect request explicitly includes it. A
design review does not authorize implementation.

### Implement

When implementation is in scope, fill in the chosen contracts with the smallest
coherent code slice. Keep usage, public types, and module ownership aligned with
the design package.

Treat deviations as evidence. When implementation needs an unplanned parameter,
escape hatch, shared state, new public method, or cross-layer dependency, record
the deviation and decide whether the requirement was missing, the design was
wrong, or the implementation is overreaching. Do not absorb structural changes
silently.

### Reconsider

Redesign when the same friction appears in multiple places, such as repeated
special cases, recurring casts, callers coordinating internal stages, or shared
state contradicting the ownership model. A single difficult edge case does not
invalidate the design.

Feed implementation evidence back through `how`, update the constraints, and
return to Explore. Remove the mistaken assumption before adding more machinery.

## Return

Return one design package with caller usage, types and signatures, a module map,
data and control flow, boundary and state rules, the synthesis decision,
accepted tradeoffs, rejected alternatives, risks, and the next implementation
step. For implementation work, add the deviations found and verification run.

Apply the `unslop` skill to human-facing rationale without changing code,
contracts, identifiers, citations, evidence, or confidence labels.
