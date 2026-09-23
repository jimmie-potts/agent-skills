# Select independent reviewers

Read when selecting task, fix, or final reviewers, after
[the common policy](model-selection.md). Load only the selected host's reviewer
adapter. Implementation settings and retry thresholds do not select reviewers.

Start from impact: capable lower-cost reviewers for low and medium impact, and the
strongest evidenced relevant reviewers at high reasoning for high impact, even
with a tiny diff. Complexity and uncertainty may raise this floor. Inspect
interactions, concurrency, invariants and recovery for interacting-state work;
examine assumptions, omissions and conflicting evidence when uncertainty is
high. Specification review must cover each criterion, exclusions and negative
cases, including high-impact acceptance. Explicit user/project requirements
prevail. Default/moderate/high are relative recommendations, not portable API
enum names; map them to supported controls and record that mapping. Maximum
reasoning is not automatic. Different reviewer models are optional; both axes
may use the same model in separate fresh contexts. No default authorizes
self-review or weakens independent-review requirements.

## Review independently and verify tests

For task-review selection, round/finding history, fix verification and explicit
limits, read [review cycles](review-cycles.md). Its round accounting is separate
from worker attempts and this policy's host-specific correction thresholds.
Apply the reviewer suitability and impact floors here to task and fix reviews
as well as final review; a small fix does not establish low impact.

For final review, run separate Standards and Specification contexts on one frozen
comparison, with raw axis-specific requirements, relevant code/consumers, and evidence.
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
