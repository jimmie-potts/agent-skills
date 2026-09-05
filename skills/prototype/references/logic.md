# Logic prototype

Use this reference when the concrete question concerns business logic, state
transitions, invariants, or data shape.

## Disposable experiment

A self-contained HTML file can make a state model easy to exercise without a
framework or server. Use that shape only in an authorized isolated destination.
Keep the state logic separate from the page so the experiment tests the model
rather than DOM wiring.

State the question visibly. Render the relevant state after every action. Give
the user free-play controls and deterministic scenarios for the happy path, a
difficult edge case, and an action that should be rejected. Use domain language
in labels and expected outcomes.

Stub persistence and external effects unless the question specifically concerns
them and the user authorizes a disposable local substitute. Never use production
credentials or data. Report which behaviors lack automated tests. Do not move
the experiment or its logic into production automatically.

## Functional delivery slice

When the user requests a functional slice, implement the smallest accepted
state transition or invariant through the repository's real interface. Add the
tests and error handling required by repository rules and the accepted behavior.
Keep UI demonstration code out of production unless it is part of the accepted
slice.

In both modes, rerun the relevant scenarios and state whether the evidence
answers the original question. A runnable artifact that exercises another code
path is not evidence.
