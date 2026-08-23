---
name: why
description: Investigate why code or a design has its current shape using source control and other authorized historical evidence. Use for design rationale, rejected alternatives, regressions, postmortems, thresholds, and the history behind a technical decision; use how for runtime behavior.
---

# Why

Reconstruct the forces that shaped code: product needs, operational failures,
technical constraints, tradeoffs, and earlier decisions. Build the account from
evidence, not from a plausible story about the current implementation.

## Authority and source boundary

Start with read-only local evidence. This skill grants no authority to fetch
remote refs, access private connectors, call live systems, modify files, or run
untrusted code. Query an issue tracker, document store, chat system,
observability platform, error tracker, analytics warehouse, or remote source
control only when it is available and within the user's authorized scope.

Never claim a category was searched when it was unavailable or skipped. A null
result is evidence only for a search that actually ran. Minimize private data,
quote only what is needed, and preserve access restrictions in the result.

## Evidence standard

- Cite every factual claim about intent with a commit, pull request, ticket,
  document, message, incident, dashboard, query, or code comment.
- Treat the current code as evidence of behavior, not proof of its motivation.
- Label indirect conclusions as inference and explain the inference chain.
- Surface disagreements between sources instead of silently choosing one.
- State gaps, unavailable sources, retention limits, and failed searches.
- Prefer direct contemporaneous records over later recollections or summaries.

Use these confidence levels:

1. **Direct.** An authoritative source explicitly states the decision and reason.
2. **Corroborated.** Independent sources support the same explanation.
3. **Inferred.** Circumstantial evidence supports the explanation, but no source
   states it directly.
4. **Unknown.** The searched record does not support an answer.

## Workflow

1. Define the target and the exact question. State a reasonable interpretation
   when the referent is ambiguous.
2. Establish a code anchor: relevant paths and lines, symbols, blame commits,
   file history, nearby tests, and identifiers linking to other records.
3. Build a coverage map from sources that are both available and authorized:
   source control, issue tracking, long-form documents, team chat,
   infrastructure observability, error tracking, and product analytics.
4. Search each relevant source using the code anchor, authors, dates, error
   strings, ticket IDs, pull-request IDs, and feature names. Follow links and
   parent records where access permits.
5. Record both relevant findings and genuine null results. For each item, retain
   its identifier, date, author, location, and the smallest useful quotation or
   faithful paraphrase.
6. Order the evidence chronologically. Check whether plans changed between
   proposal, review, implementation, incident response, and later maintenance.
7. Separate direct findings, supported inferences, competing hypotheses, and
   unknowns. Calibrate every conclusion to the strongest evidence behind it.

Run searches directly unless the user explicitly requests delegation or
parallel investigation. If parallel reviewers are authorized, give each one a
distinct evidence category and keep their work read-only. Verify their
citations before synthesis.

## Return

- **Question and code anchor.** The decision being investigated and its paths,
  lines, and symbols.
- **What the record says.** Direct evidence with inline citations and dates.
- **What appears likely.** Explicitly labeled inference chains.
- **Competing explanations.** Evidence for and against each live hypothesis.
- **What remains unknown.** Missing evidence and questions the record cannot
  answer.
- **Sources consulted.** One line per category, saying what was searched, what
  was found, or why it was unavailable or skipped.
- **Change constraints.** When the investigation precedes a code change, end
  with Preserve, Change, Avoid, and Risk constraints grounded in the evidence.

Apply `$unslop` to the final prose without weakening confidence language or
changing quotations, citations, identifiers, or facts.
