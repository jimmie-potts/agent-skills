# Alternative interface designs

Use this reference when the user wants several materially different interfaces
for one focused design problem. Do not expand a local interface question into a
full architecture workflow.

## Frame the fixed problem

Record the caller needs, invariants, error modes, performance constraints,
dependency categories, repository vocabulary, and behavior that must remain
hidden. Give every alternative the same evidence and constraints.

## Produce distinct options

When isolated agents are available, ask separate contexts to optimize for
different constraints, such as a minimal caller contract, extension needs, the
common case, or an integration seam. When isolation is unavailable, produce
the alternatives in separate passes and keep their assumptions explicit.

Each option should show:

1. the interface and its invariants, ordering, and errors;
2. a representative caller;
3. behavior hidden behind the interface;
4. dependency and adapter treatment;
5. verification strategy; and
6. costs, failure modes, and migration impact.

The options must differ structurally, not only in names. Compare them against
repository evidence for interface complexity, locality of change, seam
placement, testability, and operational constraints. Recommend one option or a
specific hybrid and state why.

Return designs only. Implementation belongs to a separately authorized task.
