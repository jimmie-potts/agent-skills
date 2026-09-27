# Design decision graders

Grade each trial against its case only. `Acceptance` names the #85 acceptance
criterion the case exercises, numbered in issue order. Each anchor is exact
rule text, after whitespace normalization, that the expected decision relies
on. `tests/architect-test.py` checks that every anchor still exists.

## D1 Caller-first payment interface

Acceptance: 1
Kind: positive
Expected: Before endorsing a candidate, show a caller example naming the
handler and what it holds, `payments` as the state owner, the captured result,
and the declined and timeout results with the retry rule. Open the package with
a short owner explanation; produce no presentation artifact.
Anchors:
- skills/architect/SKILL.md: "Do not endorse a candidate before its caller example shows the caller, owner, success path, and failure and recovery path"
- skills/architect/references/caller-examples.md: "For mutable state, include a repeated call and an interrupted operation"
- skills/architect/references/caller-examples.md: "Do not create a slide deck, report page, or other presentation artifact unless the user asks for one"

## D2 Candidate with only a success path

Acceptance: 1
Kind: negative
Expected: Do not endorse candidate A on its success path alone. Complete its
owner and failure and recovery path, or record the gap as an open question
before comparing it with B.
Anchors:
- skills/architect/references/caller-examples.md: "Do not endorse a candidate whose example lacks an owner or a failure and recovery path"

## D3 Cancellation state-model comparison

Acceptance: 2
Kind: positive
Expected: Write the brief first: the question, the decision and its owner,
criteria with how each is observed, the two models, and the stop condition.
Run the same cancellation, refund, and double-cancel scenarios on both models,
record state traces per criterion, and report tradeoffs with a supported
decision or an explicit remaining question. The artifact stays disposable.
Anchors:
- skills/prototype/SKILL.md: "write the comparison brief before building any artifact"
- skills/prototype/SKILL.md: "evaluation criteria, and how each one will be observed"
- skills/prototype/SKILL.md: "the plausible alternatives, normally two"
- skills/prototype/SKILL.md: "Record observations per criterion in a form someone else can inspect"
- skills/prototype/SKILL.md: "either the supported decision or the explicit remaining question"
- skills/prototype/references/logic.md: "run the same scenarios against each model and record the resulting state traces side by side"

## D4 Simple field addition

Acceptance: 3
Kind: negative
Expected: Build no artifact. Report that the existing type, validator, and
mapping already support the field, citing the code and existing test.
Anchors:
- skills/prototype/SKILL.md: "If existing code, documentation, or a single obvious implementation already answers the question, report that answer and its evidence instead of building an artifact"
- skills/architect/SKILL.md: "Choose directly when one candidate clearly wins or no real alternative needs investigation"

## D5 Owner-preferred dashboard layout

Acceptance: 3
Kind: positive
Expected: Build both variants with the same data and viewport and report the
observations and tradeoffs. Leave which layout to ship open for the user
instead of choosing it.
Anchors:
- skills/prototype/SKILL.md: "When the owner must decide, such as a product preference or accepted risk, present the evidence and leave the decision open until the owner answers"
- skills/prototype/references/ui.md: "Capture every variant with the same data, viewport, and state so the observations can be compared"
- skills/architect/references/rationale-template.md: "Keep a user-owned decision here until the user answers"

## D6 Disposable variant proposed for release

Acceptance: 4
Kind: negative
Expected: Say the UI is not done. Variant B is exploration evidence. The
production page needs its own implementation, review, and any required UI
approval, and promotion is a separate decision.
Anchors:
- skills/prototype/SKILL.md: "Choosing a disposable variant does not approve the production candidate or its UI"
- skills/prototype/SKILL.md: "Promotion is a separate implementation decision"
- skills/prototype/references/ui.md: "A selected variant is exploration evidence, not approval of the production UI"

## D7 Receipt-less captured payments

Acceptance: 5
Kind: positive
Expected: Replace the loose `Payment` with per-status variants so a captured
payment requires a receipt, and parse gateway JSON at the boundary. Change only
the payment path; do not enable strict mode or retype unrelated modules.
Anchors:
- skills/architect/references/caller-examples.md: "Encode a valid state or a checked external boundary in types when it prevents a demonstrated class of error"
- skills/architect/references/caller-examples.md: "Change only the types on the path the design touches"
- skills/architect/references/caller-examples.md: "update only the code that constructed the invalid shape"

## D8 Unresolved choice without a prototype invocation

Acceptance: 6
Kind: negative
Expected: Return a comparison brief as the proposed next step. Do not run
prototype or create artifacts, because the user did not invoke prototype and
asked for design only.
Anchors:
- skills/architect/SKILL.md: "Run it with `prototype` only when the user explicitly invokes prototype for this task; otherwise return the brief as the proposed next step"
- skills/architect/SKILL.md: "If the user asks only for architecture or design, stop after the design package"
- skills/prototype/SKILL.md: "An explicit invocation does not itself grant filesystem, dependency-install, server-start, browser, Git, tracker, production-route, or publication authority"
