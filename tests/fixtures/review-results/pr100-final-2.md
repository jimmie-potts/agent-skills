# PR #100 final 2 review result

Fixture copy of the review result posted at
https://github.com/jimmie-potts/agent-skills/pull/100#issuecomment-5859970837
for issue #99, rewritten in the multi-axis finding form from issue #102.
The posted comment stays unchanged as published history.

Changes from the posted text:

- 99-F1, 99-F2, 99-F6 list `standards+specification` in the axis slot instead of
  `standards` plus an "also raised on the specification axis" clause.
- The report marker, gate line, preface, `<details>` wrappers and trailing
  provider note are removed.

Everything else, including each reviewer return and its digest, is verbatim.

## Review result

| Field | Value |
| --- | --- |
| Work | jimmie-potts/agent-skills#99 |
| Round | final 2 |
| Comparison | base 3f5716e5e5813618485fb57e3529872758c2af65; head 0d0c6d4d3df48421d0bb32161e34abbf4f117241; merge-base 3f5716e5e5813618485fb57e3529872758c2af65 |
| Requirements | jimmie-potts/agent-skills#99 at 2026-09-27T21:05:26Z |
| Policy | agent-skills@3f5716e5e5813618485fb57e3529872758c2af65 |
| Standards | action-required |
| Specification | action-required |
| Reviewers | standards-reviewer-1: standards, requested opus at default, model claude-opus-5-5 (self-reported), level high (user-stated); specification-reviewer-1: specification, requested opus at default, model claude-opus-5-5 (self-reported), level high (user-stated) |
| Open findings | P0 0; P1 0; P2 1; P3 1 |

**Findings:**
- 99-F1 (P3, standards+specification, regression): skills/deliver-work/SKILL.md:232-237, the entrypoint still says a named authorization covers only the step for this change, which no longer shows that the change's own uninstall or rename is excluded; the entrypoint now states the exclusion, but the same clause also binds owner approval, tracked as 99-F6; first final 1, latest final 2
- 99-F2 (P3, standards+specification, resolved): README.md:160-166, the catalog bullet is an unguarded third copy of the authorization scope; first final 1, latest final 2
- 99-F3 (P3, standards, resolved): tests/deliver-work-test.py:529-530, splitting on the Variant 4 label raises IndexError instead of an assertion failure if the label is lost; first final 1, latest final 2
- 99-F4 (P3, standards, accepted): tests/deliver-work-test.py:533-537, the negative check catches only a verbatim restore of the old own-rename phrase; accepted because it matches the file's convention and the positive assertions on the new wording carry the rule; first final 1, latest final 2
- 99-F5 (P3, standards, resolved): tests/deliver-work-test.py:379, an escaped quote where neighbouring strings use double quotes; first final 1, latest final 2
- 99-F6 (P2, standards+specification, unresolved): skills/deliver-work/SKILL.md:232-234, "either covers only installing or updating this change" also limits the owner's checkpoint approval, so an approved uninstall, rename or retirement is forbidden, contradicting AGENTS.md, project-discovery, README steps 4-6 and the IC03 variant 4 and IC09 graders; first final 2, latest final 2

**Coverage:** Both axes covered the whole comparison 3f5716e..0d0c6d4. Isolation limit: final 2 resumed the same reviewer contexts by message. Disclosed cause: 99-F6 is a regression introduced by the orchestrator's relay wording for 99-F1, which the implementer applied as written; the specification reviewer's P3 on keeping the README bullet parallel was folded into its fix. Neither reviewer ran tests; both relied on hosted CI runs 36351022686 (pull_request) and 36351019174 (push) and the mutation record (9 of 9 rejected). The IC03 rerun on 8fee8fc predates this entrypoint text and does not cover what happens after approval. No specialist or human review is required. Redactions replace local paths only; no finding depends on them.

### Reviewer return: standards-reviewer-1

| Field | Value |
| --- | --- |
| Axis | standards |
| Comparison | base 3f5716e5e5813618485fb57e3529872758c2af65; head 0d0c6d4d3df48421d0bb32161e34abbf4f117241; merge-base 3f5716e5e5813618485fb57e3529872758c2af65 |
| Requirements | jimmie-potts/agent-skills#99 at 2026-09-27T21:05:26Z |
| Policy | agent-skills@3f5716e5e5813618485fb57e3529872758c2af65 |
| Return | complete |
| Digest | sha256:2ee746f3acbe4f0de7cc26f379888896b5ca586d5381b54a1655066a99f31401 |
| Redactions | 2: private path |

~~~text
Standards review, final round 2: jimmie-potts/agent-skills#99 (PR #100)

The Standards axis needs action. The fix for 99-F1 introduced a new P2: `skills/deliver-work/SKILL.md` now denies owner approval the power to cover an uninstall, rename or retirement. That contradicts `AGENTS.md`, `project-discovery.md`, the README procedure and the IC03 variant 4 grader. I did not run the test suite, because my runtime is read-only and could not create the scratch export.

**Blockers**

**S2-1, P2: the entrypoint withholds from the owner's approval the uninstalls the owner is asked to approve**
- **Where:** `skills/deliver-work/SKILL.md:232-234` at head 0d0c6d4. The test at `tests/deliver-work-test.py:403-405` pins this sentence.
- **What is wrong:** the sentence names two sources of authority and then limits both:
  > Perform it only on the owner's approval at that checkpoint or explicit authorization in the request that names the step; either covers only installing or updating this change, never an uninstall, rename or retirement.

  "Either" puts the owner's checkpoint approval under the same limit as a pre-authorized request. The approval can then never cover:
  - uninstalling a renamed or removed skill;
  - installing a skill that belongs to other merged work or that a changed caller newly requires.
- **Evidence it conflicts with the rest of the change and the procedure:**
  - `AGENTS.md:39-43` sends every uninstall, rename or retirement, including the change's own, to the checkpoint, and says "Approval covers only the step presented".
  - `skills/deliver-work/references/project-discovery.md:74-81` does the same. Its "Approved, or within the pre-authorization" branch says "run exactly the step presented".
  - `README.md` steps 4-5 run the uninstall of renamed or removed skills once the owner approves.
  - The IC03 variant 4 grader presents "uninstall `why`, fast-forward, install `why-trace`" at the checkpoint for approval. The IC09 grader presents the install of `review-work`, which is another skill, for approval.
- **Violated standards:**
  - writing-for-agents at base: "Keep one authoritative home for each meaning"; "Keep load-bearing safety, authority, and completion rules in a document the host discovers directly".
  - The skill that the host loads directly now contradicts the reference it points to and this repo's `AGENTS.md`.
- **Failure condition:** take IC03 variant 4, where the change renames `why` to `why-trace`.
  - The owner answers "yes" at the checkpoint to the complete step.
  - A delivery agent obeying the entrypoint finds the uninstall of `why` outside what any approval can cover. It must then either:
    - run only part of the approved step, which conflicts with "run exactly the step presented" and leaves a broken update;
    - or leave the item open with no way to complete it.
  - The same happens for any change that removes a skill, and in IC09, whose approval must cover installing `review-work`.
  - The structural test pins the defective sentence, so the suite enforces it rather than catching it. The only behavioural rerun of IC03 (4/4) was on 8fee8fc, before this sentence changed.
- **Likely cause:** `untested-bug`. The limit meant for the pre-authorized request was attached to "either". No scenario was rerun against the new entrypoint text.
- **Suggested direction (not a mandate):** attach the limit to the named request only. Example: "Perform it only on the owner's approval at that checkpoint, which covers only the step presented, or on explicit authorization in the request that names the step, which covers only installing or updating this change, never an uninstall, rename or retirement."

**Verdicts on the round-1 findings**
- **99-F1 (entrypoint scope):** regression.
  - For pre-authorization, the entrypoint now states the exclusion, so that part is resolved.
  - But the same limit now also binds owner approval; see S2-1.
  - The hunk sits in "Merge and verify completion" (lines 229-238). The `## Boundaries` section (lines 18-48) is unchanged.
- **99-F2 (README copy):** resolved.
  - `tests/deliver-work-test.py:536-539` now pins the `README.md:163-165` wording.
  - The phrase is present at head once whitespace is collapsed.
  - The implementer's mutation "README bullet drops the uninstall limit" is rejected.
  - The README sentence ties the limit to the request's authorization with ", which" and does not have the S2-1 defect.
- **99-F3 (Variant 4 label):** resolved. `tests/deliver-work-test.py:530-533` asserts `'Variant 4:'` before splitting.
- **99-F4 (verbatim-only negative check):** accepted as before; no action needed.
- **99-F5 (quote style):** resolved at line 379.

**Non-blocking P3 observations:** none new.

**Status for Standards:** action-required, because of S2-1.

**Coverage**
- **Correction diff (8fee8fc to 0d0c6d4):** only `skills/deliver-work/SKILL.md` and `tests/deliver-work-test.py` changed.
- **Whole comparison (3f5716e to 0d0c6d4), six files re-read at the new head:**
  - `AGENTS.md`, unchanged since round 1
  - `README.md`, unchanged since round 1
  - `skills/deliver-work/SKILL.md`: the completion section, the section list, and the Boundaries section checked for installation wording; 307 lines, within the 500-line limit
  - `skills/deliver-work/references/project-discovery.md`, unchanged since round 1
  - `tests/deliver-work-test.py`
  - `tests/fixtures/workflow-evaluation/installation-graders.md`, unchanged since round 1, including the IC03 and IC09 rows
- **Other checks:**
  - `git diff --check` over the whole comparison is clean.
  - The whole comparison has no em or en dashes.
- **Evidence limits:**
  - I did not run the AGENTS.md checks (read-only runtime).
  - Hosted CI runs 36351022686 and 36351019174 were not verified by me; the brief supplied them.
  - I read the mutation file (9/9 rejected) but did not reproduce it. None of its mutations tests whether owner approval covers an uninstall.
  - Round-1 sources and rules applied unchanged.

**Model:** Opus 5.5 (claude-opus-5-5).

**Comparison:** base `3f5716e5e5813618485fb57e3529872758c2af65`, head `0d0c6d4d3df48421d0bb32161e34abbf4f117241`, merge-base `3f5716e5e5813618485fb57e3529872758c2af65` (verified). The range has two commits: 8fee8fc and 0d0c6d4.

**Commands used** (all `git -C [redacted: private path]`):
- `rev-parse 0d0c6d4...^{commit}`
- `merge-base <base> <head>`
- `log --oneline 3f5716e..0d0c6d4`
- `diff --stat 3f5716e 0d0c6d4`
- `diff 8fee8fc 0d0c6d4`
- `diff --check 3f5716e 0d0c6d4`
- `show <head>:{skills/deliver-work/SKILL.md, skills/deliver-work/references/project-discovery.md, tests/deliver-work-test.py, tests/fixtures/workflow-evaluation/installation-graders.md, README.md}`, with whitespace-collapsed phrase checks
- `cat [redacted: private path]`
~~~

### Reviewer return: specification-reviewer-1

| Field | Value |
| --- | --- |
| Axis | specification |
| Comparison | base 3f5716e5e5813618485fb57e3529872758c2af65; head 0d0c6d4d3df48421d0bb32161e34abbf4f117241; merge-base 3f5716e5e5813618485fb57e3529872758c2af65 |
| Requirements | jimmie-potts/agent-skills#99 at 2026-09-27T21:05:26Z |
| Policy | agent-skills@3f5716e5e5813618485fb57e3529872758c2af65 |
| Return | complete |
| Digest | sha256:403646b953d21ff1c98e74be9b2c05785eebf539e66109b720a5653691c92bbe |
| Redactions | 7: private path |

~~~text
# Specification review, final round 2: jimmie-potts/agent-skills#99 (PR #100)

## Blockers (P0-P2)

### P2-1: the entrypoint now says an owner's checkpoint approval can never cover an uninstall, rename or retirement

- **Severity:** P2.
- **Where:** `skills/deliver-work/SKILL.md:232-234` at 0d0c6d4. The wording is pinned by `tests/deliver-work-test.py:403-405`.
- **Cause:** wrong-approach. The narrowing was attached to both authorization sources through "either", when it should apply only to the request's pre-authorization.

**What is wrong.** The round-2 fix for 99-F1 reads:

> "Perform it only on the owner's approval at that checkpoint or explicit authorization in the request that names the step; either covers only installing or updating this change, never an uninstall, rename or retirement."

"Either" refers to both sources: the owner's approval at the checkpoint and the request's authorization. So the entrypoint now says that even the owner's approval at the checkpoint never covers an uninstall, rename or retirement. That turns the checkpoint into a dead end for exactly the steps #99 sends there.

**Violated requirement and evidence.**
- Issue #99 Outcome says "Any installation step that uninstalls, renames or retires a skill stops at the owner's checkpoint." Acceptance says "Installation follows at the owner's checkpoint, per `AGENTS.md`." The owner decides at that checkpoint; the rule does not forbid the step.
- It contradicts the texts this change keeps:
  - `AGENTS.md:40-43`: present an uninstall, rename or retirement at the checkpoint; "Approval covers only the step presented."
  - `project-discovery.md`, "Approved, or within the pre-authorization": "run exactly the step presented or authorized".
  - README step 4: the prepared step includes uninstalling each renamed or removed skill. README.md:616: "After approval, run the prepared step".
- At base, the sentence read "either covers only the step for this change", which did not exclude owner-approved uninstalls. This is therefore a regression introduced in round 2.

**Concrete failure condition.** Continue IC03 variant 4, where the change renames `why` to `why-trace`:
1. The agent correctly presents the complete step (uninstall `why`, fast-forward, install `why-trace`) at the checkpoint.
2. The owner approves it.
3. The deliver-work entrypoint now says that approval covers "never an uninstall, rename or retirement". An agent that follows the entrypoint literally cannot run the approved uninstall of `why`, and it faces an unresolved conflict with the "run exactly the step presented" reference.
4. As a result, installation of the change's own rename stays pending indefinitely, or the agent resolves the conflict arbitrarily.

The same applies to any owner-approved step that brings another change's removal, such as IC03 variant 3's `skill-old`, and to retirements under the README's retirement paragraph.

**Reproducibility and frequency.**
- Deterministic on a literal reading, whenever a delivery installs a rename or removal.
- The issue calls renames rare. However, every retirement or removal of a skill, including a removal brought in by another merged change, goes through this path.
- The IC03 4/4 rerun does not cover this. It ran on 8fee8fc, before this SKILL.md text existed. Its variant 4 also ends at "stops at the checkpoint" and never exercises what happens after approval.

**Fix direction.** Bind the limit only to the request's authorization. For example:

> "Perform it only on the owner's approval of the presented step at that checkpoint, or on explicit authorization in the request that names the step, which covers only installing or updating this change, never an uninstall, rename or retirement."

Then update the pinned assertion.

## Round-1 findings

- **99-F1 (entrypoint scope): regression.** The loose "the step for this change" was replaced, but the replacement over-restricts owner approval. See P2-1.
- **99-F2 (README catalog bullet guard): resolved.** `tests/deliver-work-test.py:536-539` asserts the flattened README contains "covers only installing or updating that delivery's own change, never an uninstall, rename or retirement". The README text (README.md:162-165) matches after `flat()` collapses whitespace.
- **99-F3 (Variant 4 label): resolved.** Line 532 asserts `'Variant 4:'` is present before the split at line 533, so a missing label now fails with an assertion rather than an IndexError.
- **99-F4:** accepted by the coordinator. Nothing further to verify on my axis.
- **99-F5 (quote style): resolved.** Line 379 now uses a double-quoted literal, with no escaped apostrophe.

## Non-blocking P3 observations

- **S2-1:** the README catalog bullet (README.md:162-165) has the same shape: "runs it only on the owner's approval there or on authorization in the request that names the step, which covers only installing…". Here the "which" clause most naturally attaches to the request's authorization, so it is not a defect. If P2-1 is fixed, keeping the two sentences parallel would stop the ambiguity from coming back.

## Status for this axis

**action-required** (P2-1).

## Coverage and evidence limits

**Re-read at 0d0c6d4:**
- the whole comparison `3f5716e..0d0c6d4` (6 files, two commits);
- the correction diff `8fee8fc..0d0c6d4`, which touches only `skills/deliver-work/SKILL.md` and `tests/deliver-work-test.py`.

**Unchanged since 8fee8fc:** `AGENTS.md`, `README.md`, `project-discovery.md` and `installation-graders.md` are byte-identical to 8fee8fc. My round-1 checks of them therefore still hold, and I re-read the relevant lines to confirm consistency with the new entrypoint text.

**Other checks:**
- SKILL.md Boundaries (`## Boundaries`, line 18) is untouched. The change is in "Merge and verify completion", which starts at line 215.
- I read the implementer's mutation evidence (9/9 "FAILS (good)") but did not rerun it.

**Not covered:**
- **Tests:** not run. My runtime is strict read-only and forbids creating the scratch export.
- **Validation facts:** CI runs 36351022686 and 36351019174, and the IC03 rerun on 8fee8fc, are taken as reported.
- **Other axes and sources:** Standards and other reviewers' output were not examined.

## Model

Opus 5.5 (`claude-opus-5-5`).

## Comparison and verification commands

- **Comparison:** base `3f5716e5e5813618485fb57e3529872758c2af65`, head `0d0c6d4d3df48421d0bb32161e34abbf4f117241`, merge-base `3f5716e5e5813618485fb57e3529872758c2af65`. I verified the merge-base matches.
- **Commands.** Every `git` command used `-C [redacted: private path]`.
  - Verify and list the comparison:
    - `git rev-parse 0d0c6d4…^{commit}`
    - `git merge-base 3f5716e… 0d0c6d4…`
    - `git log --oneline 3f5716e..0d0c6d4`
    - `git diff --stat 3f5716e 0d0c6d4`
    - `git diff 8fee8fc 0d0c6d4`
    - `git diff --stat 8fee8fc 0d0c6d4`
  - Read head texts:
    - `git show 0d0c6d4:` for `skills/deliver-work/SKILL.md`, `README.md`, `AGENTS.md`, `skills/deliver-work/references/project-discovery.md` and `tests/deliver-work-test.py`, using `sed -n` and `grep -n` to find the cited lines.
  - Read mutation evidence:
    - `cat [redacted: private path]`

### Critical files
- [redacted: private path]
- [redacted: private path]
- [redacted: private path]
- [redacted: private path]
- [redacted: private path]
~~~
