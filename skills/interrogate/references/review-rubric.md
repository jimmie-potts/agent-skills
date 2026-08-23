# Interrogate review rubric

Apply the lenses that fit the change. Do not force architectural commentary onto
a small bug fix or fill an empty review with style preferences.

## Correctness

- Trace the happy path and relevant failure paths.
- Check boundary values, empty inputs, type conversions, encoding, lifecycle,
  concurrency, stale state, retries, and partial failure where applicable.
- Follow the real call chain before claiming an input can reach a bad state.
- Check idempotency and recovery when an operation can run twice or stop midway.
- Verify that errors are handled at the correct boundary and are not silently
  discarded.

## Root cause and ownership

- Decide whether the change fixes the cause or hides a violated invariant.
- Inspect callers, callees, types, and sibling modules when the diff is not
  enough to identify the owning layer.
- Flag validation, retry logic, casts, or guard clauses that mask a broken
  contract only when evidence shows the deeper failure.
- Check that logic lives in the package, service, or module that owns the
  decision and that existing canonical helpers are reused.

## Structural quality

- Look for scattered special cases, tangled branches, pass-through wrappers,
  misleading abstractions, and accidental coupling.
- Prefer direct code and clear boundaries. Do not demand abstraction when a
  small amount of duplication is easier to maintain.
- Treat a large file increase as a prompt to inspect cohesion, not as an
  automatic failure.
- Flag optionality, broad types, casts, or silent fallbacks when they hide a
  real invariant or make valid states unclear.
- Check whether related state updates can become partially applied and whether
  independent work is needlessly serialized.

## Verification

- Check whether tests exercise behavior rather than implementation details.
- For a bug fix, look for a regression test or an equivalent executable check.
- For an integration boundary, trace whether the full path is verified.
- Prefer evidence from the real value or artifact over cached state, timestamps,
  summaries, or self-reports.
- Identify missing assertions or invariants that would allow a regression to
  pass unnoticed.

## Complexity and evolution

- Find configuration, generalization, compatibility paths, or abstractions with
  no current consumer.
- Check whether temporary migration paths have a named removal condition.
- Ask whether the same behavior can be expressed with fewer moving parts while
  preserving clarity and contracts.
- Do not propose a rewrite unless the current structure has a concrete cost.

## Security and privacy

- Trace untrusted input to dangerous sinks before raising injection findings.
- Check authentication and authorization at new or changed entry points.
- Look for secrets or private data in code, logs, errors, telemetry, and review
  artifacts.
- Check time-of-check and time-of-use gaps when access or identity can change.
- Treat a credible security path seriously even when only one reviewer finds it.

## Finding quality

A useful finding names the exact location, reachable failure mode, evidence,
impact, and severity. It distinguishes a defect from a preference. It may offer
a specific correction, but a speculative rewrite is not required.

Use these severities:

- **Critical.** The path can cause broken behavior, data loss, or a security
  failure.
- **Warning.** The evidence shows a correctness edge, design flaw, or material
  maintenance risk that is not immediately catastrophic.
- **Nit.** A small clarity or consistency issue worth the reader's time. Omit
  nits that exist only to make the review look busy.
