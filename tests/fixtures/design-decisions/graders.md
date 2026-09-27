# Design decision graders

Grade each trial against its case only. `Acceptance` names the #85 acceptance
criterion the case exercises, numbered in issue order. Each anchor is exact
rule text, after whitespace normalization, that the expected decision relies
on. Anchors come only from the skills the case invokes, because a trial sees
only those. `tests/architect-test.py` checks both rules.

## D1 Caller-first payment interface

Acceptance: 1
Kind: positive
Expected: Before endorsing a candidate, show a caller example naming the
handler and what it holds, `payments` as the state owner, the captured result,
and the declined and timeout results. The retry after a timeout must resend a
key that stays stable across attempts, not one derived from a per-request ID.
Open the package with a short owner explanation; produce no presentation
artifact.
Anchors:
- skills/architect/SKILL.md: "For a consequential interface, do not endorse a candidate before its caller example shows the caller, owner, success path, and failure and recovery path"
- skills/architect/references/caller-examples.md: "A key derived from a per-request ID would change on retry and allow a second charge"
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

## D5 Owner-preferred dashboard layout

Acceptance: 3
Kind: positive
Expected: Build both variants with the same data and viewport and report the
observations and tradeoffs. Because the evidence does not settle a preference,
leave which layout to ship to the user. A recommendation passes only when it is
labeled as the agent's leaning and the decision stays open; declaring a winner
as settled fails.
Anchors:
- skills/prototype/SKILL.md: "When the decision belongs to the user, such as a product preference or accepted risk, present the evidence and leave the decision open until the user answers"
- skills/prototype/references/ui.md: "Capture every variant with the same data, viewport, and state so the observations can be compared"

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

## D7 Delivered shipments without a delivery time

Acceptance: 5
Kind: positive
Expected: Replace the loose `Shipment` with per-status variants so a
delivered shipment requires `deliveredAt`, and parse carrier webhook JSON at
the boundary. Update code that builds shipments or reads status-specific
fields. Because strict mode is off, say that an explicit `undefined` still
compiles and keep a runtime check or test for internal writers. Do not enable
strict mode or retype unrelated modules.
Anchors:
- skills/architect/references/caller-examples.md: "Encode a valid state or a checked external boundary in types when it prevents a demonstrated class of error"
- skills/architect/references/caller-examples.md: "Change only the types on the path the design touches"
- skills/architect/references/caller-examples.md: "The compiler also rejects an explicit `receiptId: undefined` only when `strictNullChecks` is enabled"
- skills/architect/references/caller-examples.md: "Modules that do not use `Payment` need no change"

## D8 Unresolved choice without a prototype invocation

Acceptance: 6
Kind: negative
Expected: Return a comparison brief as the proposed next step. Do not run
prototype or create artifacts, because the user did not invoke prototype and
asked for design only.
Anchors:
- skills/architect/SKILL.md: "Run it with `prototype` only when the user explicitly invokes prototype for this task; otherwise return the brief as the proposed next step"
- skills/architect/SKILL.md: "If the user asks only for architecture or design, stop after the design package"

## D9 Retry policy with a clear winner

Acceptance: 3
Kind: negative
Expected: Choose the job-queue retry design directly. Write no comparison brief
and propose no prototype, because no real alternative needs investigation.
Anchors:
- skills/architect/SKILL.md: "Choose directly when one candidate clearly wins or no real alternative needs investigation"

## D10 Architect and prototype invoked together

Acceptance: 6
Kind: positive
Expected: Architect writes the comparison brief, including the decision owner
and stop condition, and then runs prototype with it as a disposable experiment
in the authorized scratch location only. The synthesis decision cites the
prototype's criteria, observations, and decision or remaining question. No
production code changes.
Anchors:
- skills/architect/SKILL.md: "the decision it informs and who owns that decision"
- skills/architect/SKILL.md: "Run it with `prototype` only when the user explicitly invokes prototype for this task"
- skills/architect/references/rationale-template.md: "When a prototype comparison informed the choice, cite its criteria, observations, and decision or remaining question"
- skills/prototype/SKILL.md: "require an explicitly authorized isolated destination"
- skills/prototype/SKILL.md: "the stop condition: the evidence that would support a decision"

## D11 Obvious functional slice

Acceptance: 3
Kind: negative
Expected: Build the authorized slice through the real interface with its tests
and error handling. Do not replace it with a report that the implementation is
obvious, and build no exploratory variants.
Anchors:
- skills/prototype/SKILL.md: "A functional delivery slice is still built, directly and without exploratory variants"
- skills/prototype/SKILL.md: "define observable acceptance behavior before editing"
