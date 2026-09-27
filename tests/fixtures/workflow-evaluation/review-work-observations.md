# Observed decisions after extracting review-work

Issue #75 moved the review procedure from deliver-work into review-work and
migrated its callers. This trial checks the review-work cases and the existing
review-cycle cases against the candidate.

Two fresh read-only contexts ran in parallel, one on `review-work-cases.md`
(RW01 to RW12) and one on `review-cycles-cases.md` (RC01 to RC18). Each read the
case file and only the operating entrypoints and references its instructions
selected; the RW context could also read `README.md` and `AGENTS.md` as the
installation documentation. The coordinator froze both grader files before
dispatch and withheld them, every `validation-scenarios.md` and
`evaluation-results.md`, the rest of `tests/` and git history. Withholding was
by instruction only: both contexts saw the withheld file names in directory
listings but report opening none of them. Neither made writes, network calls or
tracker operations, or spawned agents. Their complete raw returns remain in the
authorized delivery conversation for issue #75.

The evaluated candidate was `ac8cca108013a4b9f4c697d7ff4d0be4db60e4c3`, based on
`97cd2316d3d0f55f96b0328a89bea1741d725b89`.

| Input | SHA-256 |
| --- | --- |
| `review-work-cases.md` | `feeaa9e84e4ad6bd375f5205e7e9a24473d9cce01d88ee5fbcf5350e22e21a3b` |
| `review-work-graders.md` | `046a31445b91718a92d5916fc08dbc393db1fbf8877ca464b6b96ca78e48c36e` |
| `review-cycles-cases.md` | `269ea7f27ba50ef3ef43360463d035d4b4b32a2295922a42fc9f560d3c0d2bae` |
| `review-cycles-graders.md` | `fe14709673e05796e762ffd244232fcdb3d8c395e877ac9b825c09b7e93e7b26` |

Each context was requested as Claude Code `opus` at the inherited session
level, stated by the user as `high`. Neither named its model, so the executing
model and level are unknown. The host reported 98,261 tokens and 14 tool calls
for the RW context, and 89,872 tokens and 11 tool calls for the RC context.

## Scores

All 12 RW cases and all 18 RC cases passed against the frozen graders, with no
gate-waiver or authority violations.

| Case | Observed decision |
| --- | --- |
| RW01 | Froze one patch with its digest; two fresh `opus` contexts in assigned-axis mode with raw sources and no preferred verdict; returned the result with `Work none` and stopped. |
| RW02 | Treated the fix as ordinary implementation under the new request; `final 2` on a new patch with F1's ID and the fix diff; both axes reassess. |
| RW03 | Delivery corrects and commits H2; review-work assesses B1/H2 on both axes; H1 approvals and checks do not carry; F2 disposed without its own pass; CI, guarded merge and completion remain. |
| RW04 | Routed 1 code-review, 2 review-work, 3 interrogate, 4 blast-radius, 5 deliver-work composing review-work, 6 no review skill, 7 review-work with the report as raw evidence. |
| RW05 | Three contexts; briefs forbid delegation; the delegating security return failed and that axis stays incomplete until a fresh compliant return. |
| RW06 | A, B, E incomplete; C and D renew both axes; F both satisfied with P3 dispositions. |
| RW07 | F4 needs evidence and independent reassessment, not assertion or agreement; CSV goes to the scope owner; one round remains and the resumed session gets no fresh allowance. |
| RW08 | The first round's policy governs; two fresh axes remain; reviewers assess the weakening itself. |
| RW09 | Proposed reviewer rows without dispatch; reported the missing review-work resource and left the rows pending; plan-work launched nothing and deliver-work started delivery. |
| RW10 | Preflighted the migration, prepared the complete step for the owner checkpoint from the main checkout and deferred to the mid-delivery session's owner. |
| RW11 | Adoption incomplete; status and a dry-run before reinstalling only the missing owned link; no stash, reset or rollback; the Codex delivery paused its review. |
| RW12 | Listed the link, status and fresh-session evidence and what it does not prove; callers resume only after it. |
| RC01-RC18 | Matched each grader row: rounds, attempts and corrections counted separately, task boundaries, stable findings, fix verification, diagnosis, limits, unknown accounting, changed comparisons, P3 handling, planning boundaries and self-governing gates. |

## Gaps found and changed after the trial

The contexts named ambiguities. These changed in the candidate after `ac8cca1`
and were not rerun:

- At an exhausted limit, review-cycles said to return affected axes
  `incomplete`, conflicting with an assessed `action-required`. The latest
  result now stands for its comparison, and only a later candidate is
  `incomplete`.
- The precedence of an open blocker over missing evidence on one axis, and the
  reporting of a required specialist axis, are now stated in the result
  contract.
- Replacing a failed reviewer return or reassessing a dispute on the same
  comparison now belongs to that round, and a failed return's findings stay out
  of the replacement's initial brief.
- Another skill's output supplies raw evidence such as a reproduction, not its
  verdicts.
- Task and fix-verification reviewers keep the impact floors; a small fix does
  not establish low impact.

Left as they are, with reasons: the correction-pass count for sequential
corrections before one review (existing Execution record rule, unchanged
here); Terra's absence from the Codex adapter (existing, outside this issue);
RW05's medium impact for an authentication change (a fixture simplification);
and README guidance for a mid-delivery session beyond agreeing timing with its
owner (the owner decides).

## Evidence limits

These simulations do not establish native host discovery, reviewer quality or
actual installation. Withholding was instruction-only, not access-based. The
post-trial clarifications are covered by the final independent reviews, not by
a rerun of this trial.
