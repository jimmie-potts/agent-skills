# Context loading and reporting observations

Issue [#43](https://github.com/jimmie-potts/agent-skills/issues/43) changes which
instructions a role loads and how often a coordinator repeats its execution
summary. This evaluation measures instruction and message text. It does not
measure tokens, native child loading, latency, subscription usage, API spend,
or comparative model quality.

The matched records show lower coordinator exposure for direct work, planning,
accepted pairing, and independent review. The full assigned-worker lifecycle
increases because it loads initial selection, continuation, and review branches.
Pairing workers receive less instruction text; ordinary investigation and review
workers are unchanged. Routine updates and initial briefs are smaller. The raw
samples also contain errors, described below. Those samples are not behavioral
acceptance evidence merely because they are shorter.

## Inputs and execution

- Baseline operating revision: `c661b6532775eed6e29fd3ad56c0b27c522d8f5e`.
- Candidate operating revision: `f36e6a0dc0f1953b42e3941f9da234faffee9cd6`.
  Later changes add this evidence and harden the counter; operating instructions
  measured here are unchanged.
- [Cases](context-reporting-cases.md) and [graders](context-reporting-graders.md)
  were frozen at `b0d43168ec2b3b436ecdf69e235433dd05bd28d5`, before operating edits.
  Case SHA-256: `7bbd835dad36d869f35fda530b263111ca1a230cd5589dae16e8414014ed691c`.
  Grader SHA-256: `4bba627ed30aea4cf00d4f7c72f878ab5bb465e0d2d7051a704e217600cbc740`.
- Both qualified initial contexts received the same [brief](context-reporting-evaluation-briefs.md),
  changing only checkout and revision. The ten inputs were L1–L5 on both hosts.
  Each evaluator was requested as Sol/high. Actual runtime model, effective
  effort, and attributable usage were not independently exposed.
- An earlier baseline context used a broad search that exposed an existing
  evaluation result. Its [complete return](context-reporting-excluded-baseline.json)
  is retained but excluded from the matched comparison. The subsequent initial
  contexts used explicit operating-file reads and no grader/result access.
- Each qualified context received one identical evidence-guided completeness
  correction. These are same-context corrections, not fresh blind trials.
  They reconciled missing/cached reads, transitive editorial instructions,
  base/source identity, activity at E4, and complete checkpoint evidence.
  No additional same-setting corrections were requested.
- A separate read-only reviewer, requested as Astra/high with actual settings
  unknown, exercised all ten candidate boundaries without graders or prior
  returns. Its [findings and samples](context-reporting-boundary-verification.md)
  are separate behavioral evidence, not another matched text trial or either
  final delivery review axis. It found no demonstrated instruction defect and
  identified the L2 classification overlap and incomplete L5 roster as limits.

## Raw records and receipts

| Context return | Raw samples and read inventory | Count receipt |
| --- | --- | --- |
| Baseline initial | [JSON](context-reporting-baseline-initial.json) | [JSON](context-reporting-baseline-initial-receipt.json) |
| Baseline, one correction | [JSON](context-reporting-baseline-corrected.json) | [JSON](context-reporting-baseline-corrected-receipt.json) |
| Candidate initial | [JSON](context-reporting-candidate-initial.json) | [JSON](context-reporting-candidate-initial-receipt.json) |
| Candidate, one correction | [JSON](context-reporting-candidate-corrected.json) | [JSON](context-reporting-candidate-corrected-receipt.json) |

Only external checkout/input paths in uncounted metadata were redacted. The ten
case records, including every counted message and mistake, are unchanged from
the agent returns. The separate boundary report redacts two external paths and removes trailing
Markdown whitespace; its wording is otherwise unchanged.
Initial and corrected returns are both retained; the tables below compare the
two corrected returns, rather than mixing a corrected candidate with an initial
baseline. All counted file bytes and SHA-256 values were checked against the
recorded Git revisions.

## Counting method

[`context-reporting-measure.py`](../../context-reporting-measure.py) reads one
explicit response and canonical instruction Markdown under a supplied checkout.
It emits JSON to stdout and performs no discovery, execution, network operation,
or write. It rejects traversal, noninstruction paths, and symlink aliases.
The revision argument is a label; Git/source verification is separate.

Each instruction file is charged in full as UTF-8 bytes and
`len(text.split())` words, including frontmatter, even if read in sections.
Repeated paths are deduplicated within each case and role. Coordinator/evaluator
reads are actual reported reads; child reads are proposed requirements. Files
shared by coordinator and child count in both role exposures. The union across
cases is also reported, without charging the same file twice in that union.
A cached file used by a later case belongs in that case's inventory.

Literal `brief`, `return`, and each `updates[].text` are counted separately.
JSON keys, decision/explanation metadata, fixed case inputs, issue snapshot,
host/system/tool instructions, tool output, evaluation bookkeeping, and the
count receipts are excluded. A zero means the case requested no such message;
it is not unknown runtime usage. These exclusions prevent any total here from
being interpreted as total session context or cost.

Both evaluators read the common installed editorial entrypoint. Its bytes
matched `skills/unslop/SKILL.md`, SHA-256
`05f22133d91c539803936b2d1c7617b87030d73cebf547ee8544d2a2c5f5fc4c`, so the catalog
alias is charged wherever used. Other external reads remain listed separately
in the raw record and receipt and are not opened by the counter. The independent
boundary reviewer did not verify that alias and is not included in these counts.

To recompute a receipt, use a checkout of the named operating revision, the
corresponding raw record, and the counter in this candidate:

```bash
python3 tests/context-reporting-measure.py "$SOURCE_CHECKOUT" \
  tests/fixtures/workflow-evaluation/context-reporting-baseline-corrected.json \
  --revision c661b6532775eed6e29fd3ad56c0b27c522d8f5e
```

Use the candidate record and `f36e6a0dc0f1953b42e3941f9da234faffee9cd6` for the
other receipt. Verify a file's receipt with the raw bytes from
`git show REVISION:PATH`; do not rely on a moving checkout or the revision label.

## Instruction exposure

Cells contain **bytes / words**, baseline → candidate. Each row is one supplied
case/host; these are not ten separate native host sessions.

| Case / host | Coordinator actual | Worker proposed |
| --- | --- | --- |
| L1 / codex | 72,734 / 9,877 → 57,523 / 7,782 | 0 / 0 → 0 / 0 |
| L1 / claude | 72,734 / 9,877 → 57,523 / 7,782 | 0 / 0 → 0 / 0 |
| L2 / codex | 58,583 / 7,902 → 56,153 / 7,534 | 11,255 / 1,548 → 11,255 / 1,548 |
| L2 / claude | 58,223 / 7,892 → 55,521 / 7,486 | 11,255 / 1,548 → 11,255 / 1,548 |
| L3 / codex | 121,386 / 16,659 → 126,800 / 17,329 | 14,733 / 2,070 → 19,163 / 2,719 |
| L3 / claude | 121,026 / 16,649 → 126,356 / 17,300 | 14,733 / 2,070 → 19,163 / 2,719 |
| L4 / codex | 93,528 / 12,866 → 76,809 / 10,567 | 28,607 / 4,043 → 19,144 / 2,679 |
| L4 / claude | 98,982 / 13,810 → 82,630 / 11,511 | 34,421 / 4,997 → 19,344 / 2,713 |
| L5 / codex | 115,362 / 15,774 → 85,176 / 11,574 | 15,685 / 2,197 → 15,685 / 2,197 |
| L5 / claude | 115,002 / 15,764 → 85,790 / 11,660 | 15,685 / 2,197 → 15,685 / 2,197 |

L3 coordinator exposure rises by 5,414 bytes / 670 words on Codex and 5,330 bytes /
651 words on Claude. The full lifecycle needs the newly separated initial,
continuation, reporting, and review instructions. L3 proposed worker exposure
rises by 4,430 bytes / 649 words on both hosts because the corrected candidate
proposes an extra `code-review` read. TDD contains no such dependency and is
unchanged between the compared revisions. This is an unsupported evaluator
choice, not a mandatory read missing from the baseline. The extra exposure
remains in the raw comparison rather than being removed to improve the counts.

L1 candidate reads include an unnecessary documentation reference associated
with its invalid publication claim. L5 corrected baseline reads include PR
supervision and task planning while the candidate stayed at review selection.
These are actual evaluator choices, not proof that every file was necessary.
The independent boundary report separately identifies mandatory branch reads.
Do not attribute every byte difference to file splitting.

Across case/role exposures, coordinator totals are 927,560 / 127,070 →
810,281 / 110,525 and proposed worker totals are 146,374 / 20,670 →
130,694 / 18,320. These totals do not erase individual increases or failed samples.

| Unique union | Baseline files; bytes / words | Candidate files; bytes / words |
| --- | --- | --- |
| Actual coordinator reads | 24; 173,937 / 24,162 | 35; 191,869 / 26,453 |
| Proposed worker reads | 10; 52,725 / 7,619 | 6; 28,185 / 3,971 |
| Combined instruction files | 24; 173,937 / 24,162 | 35; 191,869 / 26,453 |

The complete actual union grows by 17,932 bytes / 2,291 words and 11 files.
Conditional loading lowers selected branch exposure while adding navigation and
explicit worker contracts; it does not shrink the entire instruction library.

## Literal message samples

Cells again contain bytes / words. Every sample is included, including errors
and the candidate's extra L5 checkpoints. A dash means the baseline returned no
checkpoint at that event, not a shorter equivalent report.

| Case / host | Message | Baseline | Candidate |
| --- | --- | --- | --- |
| L1 / codex | checkpoint | 1,149 / 153 | 1,015 / 132 |
| L1 / claude | checkpoint | 1,149 / 153 | 1,015 / 132 |
| L2 / codex | brief | 1,499 / 205 | 1,131 / 150 |
| L2 / codex | return | 433 / 53 | 495 / 59 |
| L2 / claude | brief | 1,588 / 219 | 1,220 / 165 |
| L2 / claude | return | 449 / 56 | 526 / 66 |
| L3 / codex | brief | 1,722 / 238 | 1,369 / 184 |
| L3 / codex | return | 736 / 97 | 650 / 85 |
| L3 / codex | E0 | 1,375 / 181 | 1,147 / 149 |
| L3 / codex | E1 | 378 / 48 | 192 / 24 |
| L3 / codex | E2 | 414 / 54 | 136 / 21 |
| L3 / codex | E3 | 1,627 / 218 | 1,508 / 202 |
| L3 / codex | E4 | 728 / 102 | 388 / 55 |
| L3 / codex | E5 | 2,197 / 301 | 1,704 / 230 |
| L3 / claude | brief | 1,821 / 253 | 1,458 / 199 |
| L3 / claude | return | 752 / 100 | 681 / 92 |
| L3 / claude | E0 | 1,447 / 193 | 1,156 / 152 |
| L3 / claude | E1 | 378 / 48 | 189 / 24 |
| L3 / claude | E2 | 414 / 54 | 136 / 21 |
| L3 / claude | E3 | 1,560 / 214 | 1,441 / 194 |
| L3 / claude | E4 | 728 / 102 | 401 / 55 |
| L3 / claude | E5 | 2,153 / 298 | 1,684 / 230 |
| L4 / codex | brief | 1,758 / 216 | 1,679 / 216 |
| L4 / codex | return | 618 / 75 | 609 / 74 |
| L4 / codex | blocker | 1,609 / 215 | 1,366 / 176 |
| L4 / claude | brief | 1,945 / 245 | 1,755 / 234 |
| L4 / claude | return | 634 / 78 | 640 / 81 |
| L4 / claude | blocker | 1,608 / 216 | 1,408 / 183 |
| L5 / codex | brief | 1,755 / 239 | 1,517 / 210 |
| L5 / codex | return | 697 / 99 | 632 / 89 |
| L5 / codex | checkpoint | — | 1,485 / 185 |
| L5 / claude | brief | 1,863 / 257 | 1,601 / 224 |
| L5 / claude | return | 697 / 99 | 632 / 89 |
| L5 / claude | checkpoint | — | 1,488 / 186 |

L3 routine E1/E2/E4 messages shrink on both hosts while retaining the changed
status, proposed-artifact distinction, next action, and unchanged team state.
E3 immediately exposes failed work and replacement settings; E5 retains a full
standalone history and all completion evidence. Initial briefs shrink in L2–L5.
L2 returns increase by 62 / 6 on Codex and 77 / 10 on Claude. L4 Claude's return
increases by 6 / 3. L4 Codex's brief has the same word count. L5 adds checkpoints
of 1,485 / 185 and 1,488 / 186 that the baseline did not return. All literal
samples total 37,881 / 5,079 → 34,454 / 4,568; that aggregate is not a behavioral
pass rate and includes the invalid samples below.

## Behavioral observations and dispositions

| Boundary | Observed evidence and limits |
| --- | --- |
| L1 direct work | Both retain direct root work and pending independent reviews, CI, and merge. Candidate's corrected checkpoint invents separate guide publication/live verification despite the supplied absence of that system. Baseline's checkpoint omits usage and describes the scenario stop as a user limit requiring lifting. Neither checkpoint is a complete acceptance example. The independent boundary sample preserves the real stopping point, unknown usage, and no invented publication gate. |
| L2 investigation | Both choose Terra/medium or Sonnet and retain response-only authority, source H1/path/line evidence, seven return labels, no tests/changes, and unknown identity/usage. The independent reviewer notes that the existing narrow-lookup versus bounded-investigation rows overlap for a single predicate question. This fixture expressly supplies an assigned medium-rated investigation; it does not prove a unique routing decision for every source lookup. No default table was changed. |
| L3 lifecycle | Corrected samples preserve initial settings, the Codex failed result plus one correction and one effort increase, the distinct Claude first-attempt promotion threshold, failed history, active/used/planned counts, ambiguous-spawn uncertainty, rejected explicit settings, profile conflict, and the standalone E5 gates/unknown usage. Initial baseline E4 incorrectly finished W2; correction restores unchanged activity. Initial candidate omitted some applicable reads and explicit PR-CI evidence; correction adds them. Reduced routine updates do not omit the supplied state transitions. |
| L4 pairing | Both retain the original advisor, root writes, consultation state, user-owned audit decision, and independent-work option. The candidate worker returns omit the required checks not run, `check parser` and `check`, that baseline names. Both pending advice returns omit the required evidence and recommendation. These incomplete returns cannot establish lossless reduction. Worker protocols still preserve those requirements. The independent boundary check describes them but does not supply a complete matched L4 message comparison. |
| L5 independent review | Both select Astra/high or Opus at the high-impact floor, keep separate fresh axes, and leave the proposed verdict pending without source inspection and hosted CI. Baseline selection incorrectly asserts coordinator and implementer must be distinct contexts. Candidate's extra corrected checkpoint turns those roles into an exact historical count of two; that checkpoint fails the unknown-count rule. The independent verification keeps the prior roster unresolved and distinguishes two planned roles from confirmed creation. |

These are sample-generation and evidence-completeness failures, not successful
cases with cosmetic differences. The failed returns remain intact and are not
used to claim a ten-of-ten qualification result. No source defect explaining
them was demonstrated by the separate independent boundary check: the entrypoint
already forbids inventing a documentation system, and execution reporting
already requires confirmed contexts and explicit unknown history. That review
provides additional behavior evidence at the problematic boundaries; it does
not retroactively correct the matched returns or supply a model-quality score.

The raw trials and boundary check alone leave C6 incomplete. Source-contract
inspection preserves the rules, but cannot make an incomplete worker return
lossless. Reduced L1 output, incomplete L4 returns, and the invalid L5 checkpoint
are excluded from claims of lossless reporting. The separately attributed
coordinator repairs below complete the affected samples for independent fix
verification; they do not change or reclassify these raw trial outcomes.

## Coordinator repairs and separate counts

Independent final Specification review identified the incorrect TDD explanation
as `SPEC-43-01` and incomplete matched evidence as `SPEC-43-02`. Both original
evaluators had already used their one same-setting correction. The remaining
evidence work returned to the original coordinator at unchanged, unexposed
settings. These are feedback-guided artifact repairs for the same frozen cases,
not new blind trials, another worker correction, or actual child execution.

| Coordinator-authored record | Complete samples | Count receipt |
| --- | --- | --- |
| Baseline repair | [JSON](context-reporting-baseline-coordinator-repair.json) | [JSON](context-reporting-baseline-coordinator-repair-receipt.json) |
| Candidate repair | [JSON](context-reporting-candidate-coordinator-repair.json) | [JSON](context-reporting-candidate-coordinator-repair-receipt.json) |

Each repair identifies its original corrected return by filename and SHA-256
and enumerates every changed case field. Every read list, source list, and
unlisted case field is identical to that return. The instruction counts retain
the earlier evaluator's observed reads and proposed worker reads, including
unnecessary choices. They are not a new measurement of the coordinator's reads.
The counter uses the same operating revisions and counting method for both
repairs; the source inventories and instruction totals above are unchanged.

The repaired L1 checkpoint preserves unknown usage and the ordinary pending
delivery gates, without inventing a publication system or a user-imposed limit.
Baseline and candidate use the same complete message, so no L1 output reduction
is claimed. Each L4 blocked return now includes `check parser` and `check` as
unrun, the pending request's decision, evidence, recommendation and paused
dependency, the original advisor, consultation history and user ownership.
Baseline and candidate use the same complete return within each host, so no L4
worker-return reduction is claimed. L5 baseline selection and candidate
checkpoints now retain unknown prior participation rather than treating roles
as proof of distinct contexts.

Only these changed counted messages replace the corresponding raw samples in
the separate repair receipts. Cells contain bytes / words. Other message counts
are unchanged.

| Case / host | Message | Baseline repair | Candidate repair |
| --- | --- | --- | --- |
| L1 / codex | checkpoint | 1,289 / 166 | 1,289 / 166 |
| L1 / claude | checkpoint | 1,289 / 166 | 1,289 / 166 |
| L4 / codex | return | 1,250 / 166 | 1,250 / 166 |
| L4 / claude | return | 1,319 / 179 | 1,319 / 179 |
| L5 / codex | checkpoint | — | 1,579 / 197 |
| L5 / claude | checkpoint | — | 1,582 / 198 |

All literal samples in the repair records total 39,478 / 5,297 →
36,510 / 4,850. This is an artifact comparison, not a new behavioral pass rate.
The L3 routine reductions and L2–L5 initial-brief reductions remain unchanged;
the complete L1 and L4 messages contribute no savings. L2 returns still increase,
L4 Codex's brief still has equal word counts, and L5's extra checkpoints now
cost 1,579 / 197 and 1,582 / 198. L3 instruction exposure and the full instruction
union still increase as reported above.

These repairs provide complete, equivalently counted samples for independent
fix verification. They cannot establish that either original evaluator produced
a lossless result, or that a native host would load these files or behave this
way. C6 acceptance depends on checking the retained traces, repaired artifacts,
unchanged operating contracts and explicit limits together. No runtime cost,
speed or model-quality conclusion follows from the text counts.

The original defaults, host-specific correction thresholds, independent final
review axes, current-head CI, expected-head merge, and completion readbacks
remain required. No model profiles, personal configuration, installed skills,
consumer repositories, or deployment were changed by this evaluation.
