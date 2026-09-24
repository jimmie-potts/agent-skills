# Assess work and its verification

Read before deciding scope, readiness or verification for planning or delivery.
This is the canonical contract for both workflows. It describes work, not models.
Explicit user/project requirements and existing delivery gates remain floors.

## Fit scope to actual needs

Assess scope when drafting an item, at delivery pickup, and after a material
scope or assumption change, not on every turn. Refresh the stored assessment
instead of writing another. This adds no skill invocation; explicit-only skills
still need their own explicit request.

Before choosing scope, establish the intended user outcome, supported
installation or deployment, affected consumers and meaningful failure
consequences. Take these operating assumptions, with their sources, from the
owning repository's guidance and the work item. An assumption stated for one
project, such as a single-user personal default, does not carry to another
repository. Record missing assumptions as unknown and keep them visible.
"Personal project" alone never establishes low impact: one owner's device,
data or credentials can still suffer destructive or hard-to-recover failures.

Start from a direct implementation using existing components and bounded
manual steps. Add a platform, service, abstraction, automation or hardening
only for a named current requirement or concrete failure it addresses.

Classify each meaningful proposed cut, not every removed bullet:

| Cut | Meaning | Disposition |
| --- | --- | --- |
| Duplicated ceremony | Repeats evidence, approval or process a retained gate already provides | Remove; name the retained gate |
| Unnecessary capability | No current requirement, consumer or failure needs it | Remove |
| Deferred capability | Useful later, not needed for this outcome | Defer with an existing owning issue or a concrete revisit trigger |
| Required protection | Supported use depends on it for ownership, concurrency, data, credentials, authorization or recovery | Retain; removal needs the scope owner's decision |

For each cut, state the lost behavior or reduced assurance and any manual
alternative. Name an existing owning issue or a concrete revisit trigger, such
as a second consumer or an observed failure; do not create speculative
follow-up tickets.

Preserve accepted functionality and applicable protections. When a cut would
change requested behavior, an accepted criterion or failure consequences,
record needs clarification for the affected work and escalate the choice to
the scope owner; continue independent work. Routine implementation choices
within existing authority need no renewed approval. Before treating a cut as
accepted, reconcile affected consumers and acceptance criteria and update the
stored assessment. Scope assessment waives no repository review, CI, UI,
installation or physical-acceptance requirement and grants no tracker, runtime
or deployment authority.

## Rate three dimensions separately

Use low, medium, or high for each dimension with a short rationale and source
evidence. If evidence is missing, record unknown and the investigation needed;
do not force an unsupported rating or treat unknown as low. Do not average
ratings into a score that hides a high dimension.

| Dimension | Low | Medium | High |
| --- | --- | --- | --- |
| Complexity: interacting components and state | Local, straightforward behavior | Several interfaces or state transitions | Cross-component concurrency, migration, or tightly coupled state |
| Uncertainty: unresolved assumptions and evidence | Accepted behavior and observed implementation | Bounded technical questions with a way to answer them | Material unresolved requirements or unverified assumptions governing the approach |
| Impact: defect consequences and recovery | Limited, readily reversible effects | Multiple consumers or disruptive recovery | Authorization, sensitive data, destructive operations, or difficult rollback |

A one-line authorization change can have low complexity and high impact. A
large mechanical rename can have low uncertainty if its consumers and checks
are known. File count, model confidence, and passing tests alone do not establish
a rating. State evidence limits alongside the conclusion.

## Decide readiness and evidence

A ready item has a clear outcome, exclusions, testable acceptance criteria,
known prerequisites, verification expectations, and an assessment. High
complexity or impact alone does not prevent readiness.

- Needs clarification: an implementation-changing user decision is unresolved.
  Record the question and affected work; continue independent discovery.
- Blocked: a required input or prerequisite is unfinished or unavailable.
  Name its reference, owner when known, and evidence needed to unblock it.
- Ready: prerequisites and material decisions are resolved. Bounded technical
  uncertainty can remain when an explicit investigation has a question,
  observable result, and dependent-work boundary. A separately deliverable
  investigation can be ready while the feature remains blocked.

These are meanings, not mandated tracker statuses. If both a blocker and a
clarification exist, report both. Unknown evidence affecting scope, acceptance,
or a mandatory gate prevents declaring that affected work ready. Publication
of an item does not establish readiness or permission to implement it.

For decomposed work, read [task planning and dispatch](task-planning.md) for
criterion coverage, task acceptance and the distinction between required
inputs, shared-file coordination and preferred order. Planning consumers use
those meanings for proposals without dispatching implementation.

For every retained acceptance criterion identify a planned test or other
evidence, the behavior it must observe, and any limitation. Cover relevant
success and failure cases: retries, timeouts, ordering, stop and recovery,
authorization, consumer compatibility, and critical user journeys. Choose test levels proportionate to
the claim; do not require every technique for every change. Planned commands
and proposed paths are not executed checks. Delivery records actual commands,
results, and candidate revision against this mapping.

Name additional security, concurrency, migration, performance, accessibility,
or other specialist review when the affected behavior needs that expertise.
Identify qualified human acceptance when required by policy or when automated
evidence cannot establish the claim. Explain the concrete gap instead of
inventing a blanket approval gate. Preserve independent Standards and
Specification reviews regardless of ratings or advisory inspection.

When release or operations is relevant, identify release verification,
rollback/recovery evidence, monitoring expectations, and handoff ownership.
Missing human or operational acceptance remains pending. A planning record or
source-delivery request does not authorize deployment or live state changes.

## Store and refresh one assessment

Use existing tracker fields only when their meanings match. Otherwise keep one
compact assessment section in the issue description or existing authoritative
work document, with:

- source/revision or observation date, and planning or delivery stage;
- operating assumptions with their sources and unknowns, and each meaningful
  cut with its class, lost behavior or assurance, manual alternative, and
  owning issue or revisit trigger;
- each rating, rationale, evidence, and unknowns;
- readiness, blockers, unresolved decisions, and bounded investigations;
- acceptance-to-verification mapping and conditional review/handoff needs;
- reassessment triggers.

Link canonical specifications and decisions instead of copying them. Do not
create custom fields, labels, a parallel ledger, or an issue for document-only
work merely to fit this format. Preserve unrelated fields and human edits.
Use authorized tracker history or task evidence to distinguish the original
planning assessment from delivery's refreshed judgment without competing
current copies. If tracker writes are not authorized, report the assessment in
the response or existing permitted task evidence.

Delivery assesses unclassified work itself; no planning migration is required.
At pickup, check the stored scope and operating assumptions against current
sources and refresh only what changed.
Refresh on material scope/base changes, disproved assumptions, repeated failure
without new progress, or blocking findings that expose misunderstood behavior.
Record what changed, why, and which verification/review requirements it affects.
Do not let reassessment lower an explicit requirement or waive current gates.

## Read from another workflow

The consuming workflow discovers the installed canonical deliver-work package
through the host's supported skill discovery, then reads this exact relative
resource: `references/work-assessment.md`. Reading the contract does not invoke
delivery. Do not guess a personal installation path or add cross-package file
links. If discovery or reading fails, report the missing contract before the
dependent assessment; continue independent source investigation. Do not copy,
install, or reconstruct a substitute contract silently.
