# Architect rationale format

Keep the rationale short enough to review with the design. Use sentence-case
headings and replace the instructions below with project-specific content.

## Problem

State the required capability and the existing constraints that make its shape
non-obvious. Separate confirmed constraints from assumptions.

## Caller usage

Write this before the type sketch. Show realistic imports, calls, inputs,
outputs, and errors. Include enough variation to expose the important contract,
not every possible call.

## Proposed shape

Show core data types first, followed by public signatures, module ownership, and
the data and control flow. State which invariants types encode, where validation
lives, and what the design deliberately leaves out.

Explain interface depth. Name the complexity hidden behind the public contract
and the responsibilities callers still own.

## Synthesis decision

Name the base candidate and why it won. Record ideas adapted from other
candidates and rejected ideas that would conflict with the chosen ownership or
data model. Disclose when independent candidates were unavailable.

## Tradeoffs accepted

For each tradeoff, state what the design accepts and what it receives in return.
Include choices a future reviewer could mistake for an oversight.

## Alternatives considered

Name at least one structurally different alternative when one was viable.
Explain why it lost using caller cost, interface depth, ownership, data fit,
failure behavior, migration risk, or likely change cost.

## Open questions and risks

List unresolved decisions that require user input and risks that implementation
or verification must test. Do not disguise an undecided contract as a minor
implementation detail.

## Next implementation step

Name the smallest coherent slice that exercises the load-bearing design choice.
For design-only work, label it as a proposed next step rather than completed
work.
