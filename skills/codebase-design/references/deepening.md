# Deepening and seam heuristics

Use this reference when a focused design question asks whether to combine
shallow layers, concentrate behavior, or place a seam across a dependency.
These are heuristics. Repository constraints and observed change patterns decide
whether they apply.

## Classify the dependency

- **In-process:** pure computation or local state may stay behind one interface
  and be tested directly. Merging layers is optional, not automatic.
- **Local substitute:** a database, filesystem, clock, or runtime may have a
  faithful local substitute. Check its behavioral gaps before relying on it.
- **Remote and owned:** an internal service may justify a repository-defined
  port and production and test adapters. Deployment ownership, protocol
  contracts, and failure modes still constrain the seam.
- **External:** a third-party service often needs a narrow contract and a test
  substitute. Do not hide material provider behavior that callers must handle.

## Evaluate a proposed seam

Ask what actually varies, who owns the contract, which callers benefit, and how
contract drift is detected. Multiple justified implementations are evidence for
a seam, not a numeric requirement. A single implementation may still need a
seam for ownership, testing, or policy reasons; several implementations may
still share the wrong abstraction.

Keep internal test helpers private when callers do not need them. Do not expose
an internal seam solely because one test uses it.

## Plan verification without deleting evidence

Propose tests at the narrowest stable observable interface that covers the
risk. Preserve lower-level tests when they catch distinct failures, document
important algorithms, or provide faster diagnosis. Recommend removal only when
another check demonstrably covers the same behavior and the underlying task
authorizes that edit.

State the production adapter, test substitute, contract checks, integration
coverage, and failure modes needed for the proposed design. Do not create or
delete tests under this skill's authority.
