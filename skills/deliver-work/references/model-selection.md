# Select implementation and review settings

Read after [work assessment](work-assessment.md), before delegation and whenever
new evidence changes the selection. Ratings describe work; this reference owns
selection policy. Keep the original coordinator's settings and durable-write
ownership. Do not claim to switch its running model.

## Establish available choices

Honor explicit user/project models, reasoning requirements, limits, and review
gates first. Discover current model availability, supported reasoning levels,
delegation/context controls, and relevant capability descriptions from the host.
Do not infer capability from names or assume every model supports every effort
value. Use comparable evaluation evidence when available; descriptions are
initial heuristics, not measured task success.

Favor quality. Select a capable model and reasoning setting for each role with
a short rationale. Lighter settings need evidence that the bounded task and its
verification support them; low token use alone is not success. Do not require
a repository configuration file or build a model registry to use this policy.
When capability distinctions cannot be established, preserve host defaults and
disclose the gap. Missing optional controls do not block otherwise authorized
work; an unmet explicit mandatory model or independent-review requirement blocks
its affected step. Never silently substitute an explicitly requested model.

## Choose by role and evidence

Use this guidance as a starting hypothesis, adjusted to actual evidence and
supported controls. Do not combine the ratings into an average.

| Evidence | Implementation | Standards review | Specification review |
| --- | --- | --- | --- |
| Bounded local work, low uncertainty/impact, strong checks | Demonstrated suitable coding model at default/moderate reasoning | Suitable reviewer with correctness and test inspection | Suitable reviewer with criterion-by-criterion evidence |
| High interacting-state complexity | Stronger coding capability and higher reasoning; decompose at testable boundaries | Increase reasoning for interactions, concurrency, invariants, recovery | Increase reasoning when acceptance spans component interactions |
| High uncertainty or unknown material evidence | Investigate/clarify before dependent implementation | Examine assumptions affecting correctness and test validity | Stronger reasoning/capability for ambiguity, omissions, conflicting evidence |
| High impact even with a tiny diff | Capability floor adequate for the risk; strongest evidenced relevant option when suitability is uncertain | Strong relevant capability and high reasoning; specialist/human evidence as required | Independently verify negative cases, exclusions, and high-impact acceptance |

Default/moderate/high are relative recommendations, not portable API enum names.
Choose actual host-supported settings and record the mapping. Maximum reasoning
is not automatic; raise it when unresolved reasoning warrants it. A stronger
model cannot supply a missing product decision. Different reviewer models are
optional, justified by evidence rather than imposed as a gate.

## Choose an implementation strategy

Use direct coordinator implementation when existing settings suit the task, or
one bounded worker when different settings or isolation materially help. Workers
return proposed patches and evidence; the coordinator applies changes. Give each
worker outcome, source/revision, applicable instructions, assessment, acceptance
mapping, constraints, ownership, and expected result. Use a self-contained brief
when overrides prevent full-history inheritance. Distinguish requested settings
from observable runtime identity.

Choose sol-with-astra when bounded, capable Sol implementation benefits from
Astra approach/blocker checkpoints. Discover and read that skill and applicable
host adapter before starting. Its original-Astra identity, Sol availability,
parent communication, and consultation requirements remain mandatory. Record
what Sol can decide and what requires consultation. Apply selected reasoning
through supported controls without changing the advisor.

When difficult reasoning is continuous rather than separable into checkpoints,
prefer a directly assigned, suitably capable worker. If an optional pairing
cannot be established, choose another suitable strategy and disclose why. If
the user explicitly requested the pairing, report its unmet prerequisite; do
not create a replacement advisor or silently substitute another arrangement.
Advisory inspection never replaces independent delivery reviews.

## Review independently and verify tests

Run separate Standards and Specification contexts on one frozen comparison,
with raw axis-specific requirements, relevant code/consumers, and evidence.
Do not give initial reviewers implementer/advisor approval narratives, other
reviewers' conclusions, or instructions to confirm a preferred verdict. They
may inspect implementation facts and validation outputs. Require independent
initial findings before sharing conclusions for evidence-based reassessment.

Account for every changed area, including tests, configuration, CI, and relevant
surrounding behavior. Each reviewer states coverage and evidence limits. Add a
focused security, concurrency, migration, performance, accessibility, or other
specialist when assessment identifies an uncovered risk. Require qualified human
acceptance where policy or an unresolved automated-evidence gap calls for it;
do not invent routine approval gates. Findings need concrete failure conditions
and source evidence. Resolve disagreements through reproduction or reasoned
reassessment, never vote count or pressure to approve.

Check each criterion's actual evidence. Inspect assertions removed or weakened,
skipped tests, fixture/mocking changes, and CI changes. Ask whether checks reject
incorrect implementations; preserve observed pre-fix failure where applicable.
Use relevant adjacent regression, integration, consumer-contract, end-to-end,
and failure/recovery checks. Targeted property or mutation checks can help when
justified; do not require every technique everywhere.

Before changes to tests, CI, or workflow instructions, retain agreed baseline
gates and inspect removals against original acceptance and policy. Enumerating
only reduced candidate jobs cannot waive baseline obligations. Use existing
technical protections; do not change repository/account settings without
authority. Evidence must cover the candidate being merged, followed by required
merged-revision checks and operational/human handoffs.

## Reassess and report

Reassess on material scope changes, disproved assumptions, repeated failure
without new progress, or blocking findings exposing misunderstood behavior.
Diagnose the gap: stronger settings may help reasoning, investigation supplies
facts, and users decide unresolved product choices or authority. Retry only
with a changed approach and explicit expected result; unresolved repeated
failures require a concrete blocker rather than an unbounded loop. Continue
independent authorized work.

Record source/candidate revision, assessment, role, strategy, requested model
and reasoning, observable runtime settings, rationale, fallback/escalation, and
verification limits in existing task/PR evidence. Do not publish private runtime
metadata or invent telemetry. Reuse still-current evidence, renew affected tests
and reviews, and retain mandatory requirements throughout reassessment.

For Codex collaboration tools, read the
[Codex selection adapter](codex-model-selection.md) before setting overrides.
