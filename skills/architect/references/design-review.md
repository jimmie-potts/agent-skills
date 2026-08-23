# Architect candidate design and review

Use this discipline for every candidate and again before synthesis.

## Build the candidate

Write realistic caller usage before defining types. Show what callers import,
what they provide, what they receive, and how errors appear. Derive the public
contract from that usage. When usage and types disagree, fix the design rather
than forcing callers through the type sketch.

Model core data before orchestration. Trace dominant reads, writes, lookups, and
state transitions through the proposed structures. A design that depends on an
unspecified future cache, index, or reconciliation pass has not finished its
data model.

Make boundaries visible. State where external data becomes a domain type, where
validation happens, which invariants the type system encodes, and which checks
remain at runtime. Keep transport, storage, and framework representations behind
their owning boundary.

For mutable state, name its owner and answer what happens when two actors write,
an operation runs twice, or a process stops midway. Prefer single ownership or
per-actor state with an explicit merge over convention-based coordination.

Keep call chains short enough that a maintainer can trace an operation without
opening a stack of forwarding modules. A module may hide substantial behavior,
but its public contract should remain smaller than the complexity it contains.

## Reject or revise these shapes

### Shallow modules

A shallow module exposes many operations or options while hiding little. Watch
for callers coordinating several methods to perform one task, public flags that
select internal stages, or interfaces that require knowledge of implementation
details.

### Information leakage

Reject a shape when multiple modules depend on the same representation, policy,
or protocol decision. Do not export wire, storage, or framework types as the
domain contract when an owning module can translate them.

### Temporal decomposition

Do not divide ownership only by execution order. Separate load, validate,
transform, and save modules often spread one representation and its invariants
across several boundaries. Group behavior by the knowledge and decisions it
owns, even when those methods run at different times.

### Pass-through layers

A method that forwards the same arguments to an identical method adds cost
without hiding complexity. Keep the layer only when it contributes policy,
translation, lifecycle, ownership, or a distinct contract.

### Escape-hatch types

Repeated casts, broad optional fields, unbounded maps, and generic payloads may
hide an unresolved invariant. Require the candidate to name why the state is
valid and where invalid states become impossible or are rejected.

### Accidental shared state

Reject designs that rely on call order, comments, or operator discipline to
prevent conflicting writes. Make serialization, ownership, idempotency, and
recovery structural.

## Compare candidates

Score candidates on caller simplicity, interface depth, ownership, data-model
fit, invariant enforcement, failure recovery, compatibility, testability, and
likely change cost. A smaller implementation is not better when it pushes
complexity onto every caller. A richer public interface is not better when a
single operation can hide the same policy safely.
