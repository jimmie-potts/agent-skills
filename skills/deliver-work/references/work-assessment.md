# Assess work and its verification

Read before deciding readiness or verification for planning or delivery. This
is the canonical contract for both workflows. It describes work, not models.
Explicit user/project requirements and existing delivery gates remain floors.

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

For every acceptance criterion identify a planned test or other evidence,
the behavior it must observe, and any limitation. Cover relevant success and
failure cases: retries, timeouts, ordering, recovery, authorization, consumer
compatibility, and critical user journeys. Choose test levels proportionate to
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
