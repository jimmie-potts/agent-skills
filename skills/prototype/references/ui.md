# UI prototype

Use this reference when the concrete question concerns layout, information
hierarchy, or interaction design.

## Disposable experiment

Create materially different variants only in an authorized isolated location.
Use representative non-sensitive data, preserve the surrounding product context
needed to judge the design, and stub mutations. Variants must differ in
structure or primary interaction, not only color or copy.

Provide a simple, local way to switch variants when the authorized artifact
supports it. Do not add a production route, shared production component,
dependency, server, or automatic browser opening merely to display the options.

Record the question and the trade-off each variant tests. Report accessibility,
responsive behavior, data-density, and interaction limitations that were not
verified. Do not promote a selected variant automatically.

## Functional delivery slice

For a functional slice, implement only the accepted design through authorized
production paths. Use the repository's components, styling, accessibility,
tests, error handling, and responsive rules. Remove variant switchers,
unfinished alternatives, and prototype-only gates before claiming completion.

In both modes, show how the observed UI answers the original question and name
the evidence still needed for a production decision.
