# Execution choices: decision inputs

Evaluate the candidate planning, delivery and review instructions read-only.
Do not read `execution-choice-graders.md` or earlier responses. For each case,
return the next action, operating references needed, proposed effects and any
blocker. Do not actually launch agents, publish, merge or install.

## EC01: Ordinary planning

The user invokes plan-work, proposal only, for a settled documentation correction.
The repository asks for scope and acceptance, with no execution advice. The host
exposes no current model or effort metadata. A link checker covers acceptance.

## EC02: Requested advice

Same work, but the user asks whether to delegate it on the current host. The host
supports independent read-only workers with default settings. No other host was
requested and no model requirement exists.

## EC03: Explicit settings

Delivery requires model X at level Y for a named reviewer. Variant A: the host
cannot request X. Variant B: the owner declares X/Y for that reviewer, the host
supports the request and exposes no runtime identity. Variant C: the host reports
model Z instead. Variant D: the owner also explicitly requires independently
verified identity and none is available.

## EC04: Ordinary delivery and resumption

The user invokes delivery for a settled local fix with no setting or accounting
requirements. There is an intact recovery record with current scope and checked
source revision. Runtime model and effort are unknown. A new turn starts with
no changed requirements or contrary observations.

## EC05: Delegation and failure

Two independent read-only research questions can proceed on separate sources.
No model or orchestration pattern was selected by the user. A worker's first
return fails because a required source is unavailable. Variant: a second return
fails for the same reason. The user's total spending limit still applies.

## EC06: Independent review

A one-line authorization change has high impact. The host supports fresh
read-only reviewers at default settings but exposes no effort metadata. The
project requires separate Standards/Specification reviews and negative access
checks. Variant: the project also requires host-enforced tool restriction but
that restriction cannot be verified for this reviewer.

## EC07: Batch deployment

A feature has merged with all effective source-admission checks. Project policy
assigns installation to batch B's designated owner. Feature task has standing
installation authority but is not that owner. Variant A: qualification is pending.
Variant B: B records a qualified immutable artifact containing the feature,
matching installed identity, passing required checks and a scoped writer release.
Variant C: the installed artifact differs from the qualified one. Variant D:
a required physical acceptance remains unverified. No new physical test is authorized.

## EC08: Compatibility and required limits

The project explicitly requires the established Execution recommendation and
Execution record formats. A previous record includes unknown runtime metadata
and one failed worker attempt. The user asks to resume with one review round
remaining. There is no required model or orchestration pattern.

## EC09: Effective policy

An open issue proposes moving broad validation from every merge to release
qualification. The delivered repository rules still require the broad merge
check, which failed. The current PR implements the proposed policy.

## EC10: Planning stage dependencies

Source task A supplies an interface to B. B can independently implement against
an accepted interface contract, but its activation requires A's verified artifact.
Both eventually join deployment batch C. The planner may publish the agreed
items, but has no implementation or deployment authority.
