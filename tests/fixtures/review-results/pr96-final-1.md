# PR #96 final 1 review result

Fixture copy of the review result posted at
https://github.com/jimmie-potts/agent-skills/pull/96#issuecomment-5853974644
for issue #71, rewritten in the multi-axis finding form from issue #102.
The posted comment stays unchanged as published history.

Changes from the posted text:

- 71-F1 list `standards+specification` in the axis slot instead of
  `standards` plus an "also raised on the specification axis" clause.
- Coverage prose that explained the one-axis workaround says the finding lists
  both axes.
- The report marker, gate line, preface, `<details>` wrappers and trailing
  provider note are removed.

Everything else, including each reviewer return and its digest, is verbatim.

## Review result

| Field | Value |
| --- | --- |
| Work | jimmie-potts/agent-skills#71 |
| Round | final 1 |
| Comparison | base caf721ca4f6f410130b4052ca6954fab1d2aa913; head 338cec6a550315e69baafa7662941e915358504d; merge-base caf721ca4f6f410130b4052ca6954fab1d2aa913 |
| Requirements | jimmie-potts/agent-skills#71 at 2026-09-26T19:20:34Z |
| Policy | agent-skills@caf721ca4f6f410130b4052ca6954fab1d2aa913 |
| Standards | action-required |
| Specification | action-required |
| Reviewers | standards-reviewer-1: standards, requested opus at default, model claude-opus-5-5 (self-reported), level high (user-stated); specification-reviewer-1: specification, requested opus at default, model claude-opus-5-5 (self-reported), level high (user-stated) |
| Open findings | P0 0; P1 0; P2 1; P3 7 |

**Findings:**
- 71-F1 (P2, standards+specification, unresolved): skills/plan-work/references/execution-recommendations.md:115-120, the clause that an item whose start needs more than the routine tier "normally gets reviewers at that tier or stronger" restates a reviewer mapping, so a low- or medium-impact Fable or Astra start gets Fable or Astra reviewers against the Claude Code Opus default and the Codex Sol/high default; first final 1, latest final 1
- 71-F2 (P3, standards, unresolved): tests/review-work-test.py:595-597, three blank lines before `def reviewer_table` where the file uses two; first final 1, latest final 1
- 71-F3 (P3, standards, unresolved): skills/plan-work/references/execution-recommendations.md:120 and skills/review-work/references/reviewer-execution.md:42, added prose lines of 104 and 90 characters in files wrapped at about 80; first final 1, latest final 1
- 71-F4 (P3, standards, unresolved): skills/review-work/references/validation-scenarios.md:26, the portable scenario pointer names an external project's issue label; first final 1, latest final 1
- 71-F5 (P3, standards, unresolved): skills/review-work/references/review-selection.md:60-62, recording the rationale in the Settings field is described there and in the result-contract Settings bullet; first final 1, latest final 1
- 71-F6 (P3, specification, unresolved): README.md:507, "Routine independent reviewers use Luna/high" under-describes the policy, which keeps Luna/high only for bounded review tasks; first final 1, latest final 1
- 71-F7 (P3, specification, unresolved): tests/fixtures/workflow-evaluation/cost-aware-cases.md:17, case 6 gives no review-task detail while rubric item 6 expects Luna/high, so a correct Sol answer could be graded wrong; first final 1, latest final 1
- 71-F8 (P3, specification, unresolved): skills/review-work/references/claude-code-reviewers.md:111-112, "stronger evidence override the defaults" is looser than the rule that evidence never goes below the impact floor; first final 1, latest final 1

**Coverage:** Both axes covered the whole comparison, the 15 changed files, at head 338cec6. Neither reviewer ran tests, because their read-only runtime forbids the scratch export; both relied on the implementer's local checks and hosted CI runs 36303695304 (pull_request) and 36303693404 (push). 71-F1 is one failure condition raised independently on both axes (Standards S1, Specification P1), so it lists both and makes both axes action-required. Standards P3-e, which notes that the new tests check only for phrases and rows as the repository's structural tests do, requests no change and has no ID. The RS01-RS06 and RX09 scenario trial on 338cec6 passed 7 of 7 with graders withheld by instruction only; it did not exercise 71-F1. No specialist or human review is required. Redactions replace local paths only; no finding depends on them.

### Reviewer return: standards-reviewer-1

| Field | Value |
| --- | --- |
| Axis | standards |
| Comparison | base caf721ca4f6f410130b4052ca6954fab1d2aa913; head 338cec6a550315e69baafa7662941e915358504d; merge-base caf721ca4f6f410130b4052ca6954fab1d2aa913 |
| Requirements | jimmie-potts/agent-skills#71 at 2026-09-26T19:20:34Z |
| Policy | agent-skills@caf721ca4f6f410130b4052ca6954fab1d2aa913 |
| Return | complete |
| Digest | sha256:f86d628a4367131705a9e1dad2133aaee697eb86735c71a4b9363aa20a78e332 |
| Redactions | 2: private path |

~~~text
# Standards review, final round 1: jimmie-potts/agent-skills#71 (PR #96)

## Blockers (P0-P2)

**S1 - P2 - `skills/plan-work/references/execution-recommendations.md:115-120` (head 338cec6)**

- **What is wrong:** The new paragraph rewrites review-work's selection rule in plan-work's own words. For Claude Code, the rewrite contradicts the canonical adapter and the lines just above it. The text says: "On both hosts, ... an item whose recommended start needs more than the reviewer adapter's routine tier normally gets reviewers at that tier or stronger."
  - The Claude Code routine reviewer is `opus`. Plan-work recommends a Fable (`fable`) / `high` start for "Sustained difficult reasoning, architecture tradeoffs, or substantial coordination" (line 28 at head), and that row has no impact condition. The new sentence therefore sends a low- or medium-impact Fable-start item to Fable reviewers.
  - The canonical adapter `skills/review-work/references/claude-code-reviewers.md:8-12` says the review task "changes no default on this host". The same plan-work section (lines 103-104) says the Reviewers row names "`opus` for both axes, or the coordinator's model at high impact". Plan-work's validation scenario (`skills/plan-work/references/validation-scenarios.md:90`) expects "Reviewers are `opus` for both axes, or the coordinator's model at high impact".
  - "At that tier" is also ambiguous. It can mean the start's tier, which gives the conflict above, or the adapter's routine tier, which makes the sentence say nothing.
- **Violated standard:**
  - `skills/writing-for-agents/SKILL.md` at base, "Keep one authoritative home for each meaning. Link to ... detailed procedures instead of copying them", and "Delete duplication".
  - The brief's convention for review-work: one canonical selection table and no duplicated mapping. The new text itself says "copy no reviewer mapping here" in the same sentence that restates a mapping.
  - Clear, unambiguous instructions (AGENTS.md "Write concise, imperative instructions").
- **Failure condition:** Run plan-work with no explicit reviewer requirement on a medium-impact parent item whose assessment calls for architecture tradeoffs and coordination (the plan-work scenario at `validation-scenarios.md:88`, "Recommend Fable/high ... for the parent").
  - Reading line 115-120, the planner writes Claude Code `Reviewers` as Fable reviewers ("at that tier or stronger").
  - Reading line 103 and the Claude Code adapter, it writes `opus`.
  - One section gives two different answers. A Fable choice fails the grader expectation at `validation-scenarios.md:90`.
  - The plan-work test (`tests/plan-work-test.py:113-137`) checks phrase presence only, so it does not catch this.
- **Fix direction:** Limit the derived rule to what the adapters say, for example by pointing to the active host adapter's placement, or delete the "so an item whose recommended start ..." clause.
- **Likely cause:** edge-case. The rewrite holds for Codex (the Sol start maps to Sol reviewers) but misses the Claude Code Fable start row.

## Non-blocking P3 observations

- **P3-a:** `tests/review-work-test.py:595-597` has three blank lines before `def reviewer_table`. PEP 8 wants two, and the rest of the file uses two between top-level definitions.
- **P3-b:** Two added prose lines break the ~80-column wrap the touched files otherwise use:
  - `skills/plan-work/references/execution-recommendations.md:120` (104 columns)
  - `skills/review-work/references/reviewer-execution.md:42` (90 columns)

  Some long lines already exist at base, so this is cosmetic.
- **P3-c:** `skills/review-work/references/validation-scenarios.md:26` calls the case "the Hub #278 shared-navigation case". The fixture names it `example/hub#278` and says it is "modeled on a real planned change". Using the fixture's name would keep the portable skill reference free of an external project's issue label.
- **P3-d:** Recording in the Settings field is now described in two places: `review-selection.md:60-62` and the `result-contract.md:33-36` Settings bullet. They agree today, but result-contract is the natural single home.
- **P3-e:** The new tests only check that phrases and table rows are present. That matches the repository's existing structural-test pattern, and the behaviour is left to the held-out RS cases.

## Checks that found no problem

- **RX09 grader edit:** No observation file, receipt or test records a trial or digest for `reviewer-execution-cases.md` or `reviewer-execution-graders.md`. The only references are in `tests/review-work-test.py:582-594` and review-work's `validation-scenarios.md`. The edit therefore invalidates no recorded trial digest. The context-reporting receipts hash only `skills/deliver-work/...` paths, and no touched file is among them.
- **Anchors and removed text:** The renamed section anchor `#select-for-impact-and-the-review-task` resolves from both adapters. No link to the old `#start-from-impact` remains.
- **Dashes and whitespace:** No em dashes, en dashes or other non-ASCII characters were added. `git diff --check` is clean.
- **Fixture pattern:** The new cases and graders follow the existing workflow-evaluation pattern. They have the synthetic-record preamble, withholding language, the "A1 to A5 label the rows of issue #N's acceptance table" convention, and RS IDs that match between cases and graders.
- **Catalog rules:** No `SKILL.md` grows past its limits, no frontmatter changed, and no resources were added to skill directories.
- **Installation:** The change touches `skills/`, so AGENTS.md's Installation section applies after merge. That is a delivery obligation, not a defect in the diff.

## Status for Standards axis

**action-required** (S1).

## Coverage and evidence limits

- **Examined:** All 15 changed files at head against base:
  - review-work: `SKILL.md`, `review-selection.md`, `codex-reviewers.md`, `claude-code-reviewers.md`, `reviewer-execution.md`, `result-contract.md`, `validation-scenarios.md`
  - plan-work: `execution-recommendations.md`, `validation-scenarios.md`
  - fixtures: `reviewer-execution-cases.md` and `-graders.md`, the new `reviewer-selection-cases.md` and `-graders.md`
  - tests: `tests/review-work-test.py`, `tests/plan-work-test.py`
- **Consumers checked:** I also searched deliver-work, plan-work and code-review at head for impact-only reviewer mappings or stale references that now conflict. Only S1 was found. `deliver-work/references/validation-scenarios.md:297-299` stays consistent.
- **Tests not run:** My runtime is read-only and forbids creating files anywhere, including the scratch export. As the brief directs, I did not run the repository checks. I rely on the reported local results and hosted CI runs 36303695304 and 36303693404 as stated facts, and did not verify them.
- **Codex catalog claim not checked:** I did not verify the claim in `codex-reviewers.md:35-45` about the Codex CLI 0.156.0 model catalog. The local cache is outside my assigned sources.
- **Sources not used:** I did not read issue #71, the PR description or other reviewers' output.

## Model

Opus 5.5 (`claude-opus-5-5`).

## Comparison and verification commands

- **Comparison:**
  - Base `caf721ca4f6f410130b4052ca6954fab1d2aa913`
  - Head `338cec6a550315e69baafa7662941e915358504d`
  - Merge-base `caf721ca4f6f410130b4052ca6954fab1d2aa913` (verified to match)
  - Commits: 1259e76, 535d190, 8d56d48 (merge of origin/main), 338cec6
- **Commands** (all with `-C [redacted: private path]`):
  - `git rev-parse <base>^{commit} <head>^{commit}`
  - `git merge-base <base> <head>`
  - `git log --oneline <base>..<head>`
  - `git diff --stat|--check <base> <head>`
  - `git diff <base> <head> -- skills/ tests/`
  - `git show <rev>:<path>` for AGENTS.md, code-review and writing-for-agents SKILL.md at base, and the touched files at both revisions
  - `git grep` at head for fixture references, digests, anchors and reviewer mappings
  - `git ls-tree`
- **Other:** `cat [redacted: private path]`.
~~~

### Reviewer return: specification-reviewer-1

| Field | Value |
| --- | --- |
| Axis | specification |
| Comparison | base caf721ca4f6f410130b4052ca6954fab1d2aa913; head 338cec6a550315e69baafa7662941e915358504d; merge-base caf721ca4f6f410130b4052ca6954fab1d2aa913 |
| Requirements | jimmie-potts/agent-skills#71 at 2026-09-26T19:20:34Z |
| Policy | agent-skills@caf721ca4f6f410130b4052ca6954fab1d2aa913 |
| Return | complete |
| Digest | sha256:6d7d24b7864551982f9aae0e6e7e2ae4e7982c28f485db3e94ff13311c78b331 |
| Redactions | none |

~~~text
# Specification review, final round 1: jimmie-potts/agent-skills#71 (PR #96)

## Blockers (P0-P2)

**P1 (P2).** `skills/plan-work/references/execution-recommendations.md:117-120` adds its own rule for reviewer tiers. That rule conflicts with the canonical adapters and with plan-work's own scenario.

- **Wrong text:** The new sentence reads: "so an item whose recommended start needs more than the reviewer adapter's routine tier normally gets reviewers at that tier or stronger." This rule maps the recommended start's tier to a reviewer tier, and it exists only in plan-work.
  - **Claude Code:** The routine tier is `opus`. A Fable (`fable`)/`high` start (row 28, line 28) therefore "normally" gets Fable reviewers. The canonical adapter says the opposite at `skills/review-work/references/claude-code-reviewers.md:8-11`: "review task changes no default on this host". Plan-work's own scenario, unchanged at `skills/plan-work/references/validation-scenarios.md:90`, also requires "Reviewers are `opus` for both axes, or the coordinator's model at high impact".
  - **Codex:** An Astra-start item at low or medium impact "normally" gets Astra reviewers. The canonical row at `skills/review-work/references/codex-reviewers.md:14` sets Sol/high as the default, with "or stronger" allowed but not normal.
- **Requirement violated:** A4 says planning must read the canonical reviewer policy, the Claude Code default stays Opus, and no second reviewer mapping may be added to plan-work. The Scope section says plan-work changes go "only as needed … without a duplicated model table". The out-of-scope list says "Do not change Claude Code's Opus reviewer default."
- **How it fails:** Run `plan-work` on a medium-impact item that needs sustained architecture reasoning, so row 28 recommends Fable/high and Astra/high. Line 117-120 tells the planner to write Fable reviewers for Claude Code and Astra reviewers for Codex. The Claude adapter and scenario line 90 require `opus`, and the Codex adapter's default is Sol/high. Two faithful readings of the candidate's own sources give different `Reviewers` rows. An output that follows line 117-120 fails scenario line 90.
- **Why tests miss it:** The new structural test only checks that plan-work has no `|` table and no `gpt-6-` string, so this sentence passes. Encounter frequency is uncommon: only Fable or Astra starts below high impact. The Hub #278 (Sol-start) and Opus-start cases are unaffected.
- **Suggested fix:** Have plan-work defer to the adapter. For example: reviewers at the tier review-work's host adapter assigns to that review task.
- **Likely cause:** `edge-case`. A sentence written for the Sol case over-generalises to the Fable and Astra starts.

## Non-blocking P3 observations

- **O1, `README.md:507`:** It still says "Routine independent reviewers use Luna/high." At the head, Luna/high applies only to a bounded review task. A cross-interface change at low or medium impact now gets Sol/high or stronger. The README is outside the issue's named files, but this line now under-describes the policy.
- **O2, `tests/fixtures/workflow-evaluation/cost-aware-cases.md:17` with `cost-aware-rubric.md:16`:** Case 6, "A routine medium-impact change needs Standards and Specification review", still expects Luna/high.
  - The case gives no complexity, interfaces or checks. Under the new `review-selection.md:41-42`, "work the evidence cannot place takes the stronger tier", so a correct Sol answer could be graded wrong.
  - The same ambiguity was fixed for RX09 (`reviewer-execution-cases.md:104-106`) but not here. Leaving it may be deliberate if these inputs count as historical evaluation material, which is out of scope. Record the choice either way.
- **O3, open question for the scope owner:** The Scope section says to "Retain the strongest evidenced relevant reviewer floor for high impact and allow explicit user/project requirements and stronger comparable evidence to govern exceptions."
  - The head allows comparable evidence to lower a reviewer only down to the impact floor, never below it (`review-selection.md:58-60`, `codex-reviewers.md:90-92`, grader RS04 B).
  - I read this as consistent with A2 ("a tiny high-impact change retains the strong impact floor") and with the base's "floor" wording, so I am not treating it as a blocker.
  - However, `claude-code-reviewers.md:111-112` still says, without qualification, "Explicit user or project requirements and stronger evidence override the defaults." That is now looser than review-selection. Confirm the intended reading and align the sentence if needed.

## Acceptance mapping (static reading at the head)

- **A1 (met in policy text):** The Codex row at `codex-reviewers.md:14` and `review-selection.md:35-42` give Hub #278 Sol/high or stronger. RS01 and RS02 cover it, and `test_cross_interface_work_gets_sol_reviewers_at_low_impact` rejects main's single "Low or medium impact" row.
- **A2 (met):**
  - The bounded Luna row is at `codex-reviewers.md:13`, with RS03.
  - The high-impact row is unchanged, with RS04 A-C.
  - The scenario at `deliver-work/references/validation-scenarios.md:297-298` still holds.
- **A3 (met):**
  - The review task, any exception with its evidence and limits, and the requirement's precedence are in `review-selection.md:44-62`. The Settings field is in `result-contract.md:33-36`.
  - Non-equivalence across models is stated at `review-selection.md:45-47` and `codex-reviewers.md:14`.
- **A4 (partly met):** The plan-work Reviewers row and **Why:** line read the canonical policy, and the Claude default stays Opus (`claude-code-reviewers.md:16`, RS06). P1 above is the exception.
- **A5 (met):** Task, fix-verification and final reviews are covered at `review-selection.md:49-53`, which also states that the reviewer count, frozen comparison, scope and gates are unchanged. See RS01 B and C and RS04 C.
- **A6:** The validation facts report every AGENTS.md command passing and both hosted CI runs successful at 338cec6. I statically checked each new test's assertions against the head text. All match.
- **Preserved:** two fresh independent axes, raw sources, specialist and human gates, and model-neutral ratings. There are no changes to implementation-worker selection or to historical issues or results. RX09 has no recorded observations file.

## Status for my axis

`action-required` (P1).

## Coverage

- **Examined:** every changed file at the head.
  - `review-selection.md`, `codex-reviewers.md`, `claude-code-reviewers.md`, `reviewer-execution.md`, `result-contract.md` and the review-work `SKILL.md`.
  - The plan-work `execution-recommendations.md` and both `validation-scenarios.md` files.
  - The new `reviewer-selection` cases and graders, and the RX09 edits.
  - `tests/plan-work-test.py` and `tests/review-work-test.py`.
- **Checked for stale conflicts:** the unchanged consumers — deliver-work `SKILL.md`, deliver-work validation scenarios and worker selection, plan-work `SKILL.md`, the README and the evaluation fixtures.
- **Not done:**
  - I did not run tests. My runtime is read-only and forbids creating files, including the scratch export, so I relied on the stated validation facts and a static check of the test logic.
  - I did not run the RS scenario trial. It runs separately and was not available, so A1-A4 have no simulated-decision evidence here. Even with it, simulated selections are not evidence of live review quality.
  - I did not review the Standards axis or installation.

## Model

Opus 5.5 (`claude-opus-5-5`).

## Comparison and commands

- **Commits:** base `caf721ca4f6f410130b4052ca6954fab1d2aa913`, head `338cec6a550315e69baafa7662941e915358504d`, merge-base `caf721ca4f6f410130b4052ca6954fab1d2aa913`. The merge-base matched.
- **Commit list:** 1259e76, 535d190, 8d56d48, 338cec6.
- **Commands used:**
  - `git rev-parse <base>^{commit} <head>^{commit}` and `git merge-base <base> <head>`
  - `git diff --stat <base> <head>` and `git log --oneline caf721ca..338cec6a`
  - `git diff <base> <head> -- skills/review-work skills/plan-work` and `git diff <base> <head> -- tests`
  - `git show <head>:<path>` and `git show <base>:<path>` for the files cited
  - `git grep` at `<head>` for reviewer, impact and Luna references, and for RX09
  - `git ls-tree --name-only <head> tests/fixtures/workflow-evaluation/`
  - `gh issue view 71 --json title,body,comments,updatedAt` (updated 2026-09-26T19:20:34Z) and `gh issue view 21 --json title,body` for context. Plain `gh issue view --comments` failed on a deprecated Projects (classic) GraphQL field.
~~~
