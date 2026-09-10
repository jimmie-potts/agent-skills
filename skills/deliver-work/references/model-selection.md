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
supported controls. Do not combine the ratings into an average. Start reviewer
selection from impact: capable mid-tier reviewers for low and medium impact,
and the strongest evidenced relevant reviewers at high reasoning for high
impact. This reserves frontier judgment for costly mistakes while retaining
capable verification on routine work. Complexity and uncertainty may raise the
selection; explicit user/project reviewer requirements always prevail.

| Evidence | Implementation | Standards review | Specification review |
| --- | --- | --- | --- |
| Low or medium impact | Suitable implementation settings for the complexity and uncertainty | Capable mid-tier reviewer by default, with correctness and test inspection | Capable mid-tier reviewer by default, with criterion-by-criterion evidence |
| High interacting-state complexity | Stronger coding capability and higher reasoning; decompose at testable boundaries | Increase reasoning for interactions, concurrency, invariants, recovery | Increase reasoning when acceptance spans component interactions |
| High uncertainty or unknown material evidence | Investigate/clarify before dependent implementation | Examine assumptions affecting correctness and test validity | Stronger reasoning/capability for ambiguity, omissions, conflicting evidence |
| High impact even with a tiny diff | Capability floor adequate for the risk; strongest evidenced relevant option when suitability is uncertain | Strongest evidenced relevant reviewer at high reasoning; specialist/human evidence as required | Strongest evidenced relevant reviewer at high reasoning; verify negative cases, exclusions, and high-impact acceptance |

Default/moderate/high are relative recommendations, not portable API enum names.
Choose actual host-supported settings and record the mapping. Maximum reasoning
is not automatic; raise it when unresolved reasoning warrants it. A stronger
model cannot supply a missing product decision. Different reviewer models are
optional, justified by evidence rather than imposed as a gate. Both axes may
use the same model in separate fresh contexts. These defaults never authorize
self-review or weaken independent review requirements.

## Choose an implementation strategy

Decide first whether the work is one chain of dependent steps or many
independent pieces. Direct coordinator implementation is the baseline: use it
when existing settings suit the task or the work is one bounded chain that fits
in one context. Judge alternatives by cost per completed task, including
corrections and reruns, rather than tokens per request. Use one bounded worker
when different settings or isolation materially help, and separate bounded
workers when the work splits into independent pieces or exceeds one context.
Workers return proposed patches and evidence; the coordinator applies changes.
Give each worker outcome, source/revision, applicable instructions, assessment,
acceptance mapping, constraints, ownership, and the entrypoint's labeled
worker return format. Use a self-contained brief when overrides prevent
full-history inheritance.
Distinguish requested settings from observable runtime identity.

Name the chosen strategy in the record. The strategies are direct
implementation by the coordinator; an assigned worker with one brief and no
advisor loop; parallel workers for independent pieces, which the coordinator
merges; and the advisory pairing, where one worker runs the implementation
loop and consults the coordinator at approach, blocker, and final review. The
coordinator owns durable writes and runs the independent reviews as a separate
step under every strategy.

Choose the host's advisory pairing when bounded, capable worker implementation
benefits from coordinator approach/blocker checkpoints: serial work with a few
hard decision points rather than continuous difficult reasoning. Select the
pairing skill from verified host tooling, never from a persona or a model list.
Codex collaboration tools select worker-with-astra. Claude Code subagent tools
select worker-with-fable. Any other host has no pairing. Discover and read the
selected skill and its host adapter before starting. Its original-coordinator
identity, worker availability, parent communication or worker resumption, and
consultation requirements remain mandatory. Record what the worker can decide
and what requires consultation. Apply selected reasoning through supported
controls without changing the advisor.

When difficult reasoning is continuous rather than separable into checkpoints,
prefer direct implementation or a directly assigned, suitably capable worker.
If an optional pairing cannot be established, choose another suitable strategy
and disclose why. If the user explicitly requested the pairing, report its
unmet prerequisite; do not create a replacement advisor or silently substitute
another arrangement. Advisory inspection never replaces independent delivery
reviews.

## Correct, consult, or hand off an attempt

A correction asks the same worker to repair its result. A consultation asks the
same original advisor for a decision and pauses dependent work until answered.
A promoted attempt starts a fresh worker when supported settings cannot change
in place. These events have separate counts; use the host adapter's failure
threshold and preserve explicit model/pairing requirements.

Diagnose an inadequate result before changing settings. For a new attempt,
stop the old assignment and verify its state before transferring ownership.
Carry its artifact or patch, source/candidate revision, acceptance criteria,
failed checks and outcomes, attempt/settings history, unresolved question,
permissions and write ownership in a self-contained brief. Preserve history
across replacements and resumptions; do not pass a new spawn off as a resume.
Host adapters own stop/spawn/resume mechanics. An unavailable stop or required
control blocks the affected replacement, not independent authorized work.

For a new advisory attempt, retain the original advisor and re-establish all
pairing prerequisites and mandatory approach/final consultations. A standalone
pairing reports the inadequate attempt to its coordinator; the composing
workflow chooses promotion. Explicit requirements have no silent fallback.
Use existing labeled worker returns and task evidence; include handoff rationale
and history without replaying transcripts. Advice never expands authority.

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
with a changed approach and explicit expected result; a stronger worker tier
for the affected step is a changed approach. Unresolved repeated failures
require a concrete blocker rather than an unbounded loop. Continue independent
authorized work.

Record source/candidate revision, assessment, role, strategy, requested model
and reasoning, observable runtime settings, consultation count for a pairing,
rationale, fallback/escalation, and verification limits in existing task/PR
evidence. Do not publish private runtime
metadata or invent telemetry. Reuse still-current evidence, renew affected tests
and reviews, and retain mandatory requirements throughout reassessment.

For Codex collaboration tools, read the
[Codex selection adapter](codex-model-selection.md) before setting overrides.
For Claude Code subagent tools, read the
[Claude Code selection adapter](claude-code-model-selection.md).
