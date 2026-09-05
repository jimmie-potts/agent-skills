# Decision-record guidance

Use this reference only when a resolved trade-off may deserve a durable
decision record. Discover the repository's decision-log convention and
numbering before proposing a path. Do not assume `docs/adr/`.

## Decide whether to record it

Propose a record only when all three conditions hold:

1. The decision is costly to reverse.
2. The result would surprise a future reader without its context.
3. Credible alternatives created a real trade-off.

Skip a record when any condition is absent, for routine implementation details,
or for choices already governed by an authoritative contract.

## Match the repository's format

Follow an existing template, status vocabulary, filename scheme, index, and
supersession rule. When no format exists, propose the smallest useful record:

```markdown
# Short decision title

State the context, accepted decision, and reason in one to three paragraphs.
Include rejected alternatives or consequences only when future readers need
them to avoid repeating the same analysis.
```

Link the evidence and authoritative scope source. Do not make the decision
record the source of delivery scope, behavior, or change-local implementation
steps when the repository assigns those responsibilities elsewhere.

Show the exact proposed path and content before any authorized write. If the
repository has no accepted destination, return the proposal and unresolved
location choice instead of creating a new convention silently.
