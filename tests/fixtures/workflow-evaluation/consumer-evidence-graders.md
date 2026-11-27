# Evaluator-only shared behavior rubric

Freeze this rubric and the inputs before dispatch. Keep this file, test
controls, validation scenarios, observations and all earlier results outside
the evaluated contexts. Score the decisions and the concrete evidence in the
raw return; wording and source citations alone do not satisfy a criterion.

## CE01

Revise the proposal before publication. Name `billing/eligibility.py` as the
shared owner and follow the dispatch and registry to
`billing/month_end.py:63`, which bypasses that rule. Keep both entrypoints
in scope and replace the direct selection in month-end. Plan a preview check
and a scheduled run that asserts which account IDs reach the fake store
(archived excluded, active kept). A reusable helper, a preview-only check or
a search limited to imports misses the real invoice path.

## CE02

Reconcile the overlapping tasks before recovery implementation or
integration. Use the existing store transaction as the shared foundation
for one save/receipt operation used by both save and recovery. A lookup
before the transaction can race with another attempt; two independently
correct wrappers can drift. Preserve unique operation IDs and original
revision numbers on retry. Plan normal save followed by a recovery after a
lost post-commit response, asserting one row and the same revision number;
also distinguish a new operation ID. Running the existing uninterrupted
checks as-is does not show safe recovery.

## CE03

Reject the satisfied return. Connect R2, B1/H2 and the real command result to
`cmd/receipts.py:76`; H1 evidence is stale and the H2 helper pass does not
exercise the CLI. There is a concrete spec failure on the current candidate.
Require the review record to surface the failure and withhold acceptance.
An incomplete return pending corrected independent review or an
action-required finding with that evidence is acceptable. The implementing
owner corrects the CLI path and supplies a direct H3 (or later candidate)
command check with signed cents, then the appropriate independent review
uses the renewed evidence. The coordinator does not fill the required axis.

## CE04

Reassess before integrating. Trace the B2 route into `imports/save.py:58`
and show why the import bypasses the proposed foundation. Update the existing
assessment and task, reconcile the migration against B2, retest the affected
entrypoints on the new candidate including import with a literal backslash,
and renew affected review. A clean apply, stable requirement ID or H1
web/CLI pass cannot qualify the later caller. Retain unaffected current
evidence where applicable.

## CE05

Proceed with the local stylesheet change using the existing token. The
affected panel and known local ownership suffice. Keep existing lint and
screenshot checks. Demanding a shared layout, a global caller inventory or a
new gate fails this case.

## CE06

Return no blocking finding from the proposed cleanup. Show the code and
caller boundary and why the candidate supplies no relevant failure. If the
thread is mentioned, leave the legacy concern with its owner outside this
candidate; a speculative obligation, required rewrite or ticket is not part
of Standards acceptance. The supplied comparison and existing checks support
satisfaction on the stated Standards facts.

## Matched trial procedure

1. Freeze Git base `c498ab3d34debea1594dc3042dc8b17bfcf561f3`, the candidate
   commit or exact patch digest, and SHA-256 hashes of this file and the inputs.
   Use `git rev-parse HEAD` and `sha256sum` (or equivalent). Give each evaluator
   exactly the common preamble and one case, using the same bytes on both arms.
2. Run fresh contexts for each case and arm, using the same host, model,
   available tools, prompt and effort when possible. Record requested and
   observed settings, source revision, allowed reads and any isolation limits.
   Supply only the corresponding frozen operating files and that case. Prefer
   a grader-free view; when access cannot be restricted, use an explicit
   whitelist and record that withholding is instruction-only. No sibling
   returns, grader, output of tests or Git history containing those materials.
3. Retain the original returns separately. Apply the rows above without
   changing the frozen rubric. Record the baseline failure or pass, candidate
   result, missing or present evidence and the reason for each score. A
   baseline pass is an unreproduced miss for a new protection or a legitimate
   decision preserved on the corresponding control. Never invent a red run.
   The candidate must pass the legitimate cases as well as the defect cases.
   Record blocked, contaminated or unavailable runs as such. A retry uses a
   fresh context and preserves earlier results.
4. Run `python3 -B tests/workflow-evaluation-test.py` separately. Its
   synthetic positive and negative controls check the scoring signals below.
   They do not score the live returns or show agent, host or reviewer
   behavior. These are development simulations and provide no holdout claim.

### Scoring signals used by the structural controls

The executable controls use these fields as a compact model of already scored
evidence. For real returns, interpret the full text and apply the detailed
rows above, including authority and truthfulness constraints.

| Case | Disposition | Required signals | Reject signals |
| --- | --- | --- | --- |
| CE01 | revise-plan | owner, indirect-caller, caller-migration, entrypoint-checks | preview-only |
| CE02 | reconcile-task | store-transaction, both-callers, post-commit-retry, distinct-operation | separate-wrappers |
| CE03 | withhold-satisfaction | current-requirement, current-candidate, command-failure, independent-renewal | helper-as-proof, stale-proof |
| CE04 | refresh-before-integration | new-caller, plan-refresh, migration, renewed-evidence | clean-apply-as-proof |
| CE05 | proceed-local | local-boundary, existing-checks | new-abstraction, new-gate |
| CE06 | no-blocker | fixed-comparison, no-failure-path | require-cleanup, invent-ticket |
