# PR #97 final 1 review result

Fixture copy of the review result posted at
https://github.com/jimmie-potts/agent-skills/pull/97#issuecomment-5854080004
for issue #83, rewritten in the multi-axis finding form from issue #102.
The posted comment stays unchanged as published history.

Changes from the posted text:

- 83-F1, 83-F4, 83-F7 list `standards+specification` in the axis slot instead of
  `standards` plus an "also raised on the specification axis" clause.
- Coverage prose that explained the one-axis workaround says the finding lists
  both axes.
- The report marker, gate line, preface, `<details>` wrappers and trailing
  provider note are removed.

Everything else, including each reviewer return and its digest, is verbatim.

## Review result

| Field | Value |
| --- | --- |
| Work | jimmie-potts/agent-skills#83 |
| Round | final 1 |
| Comparison | base caf721ca4f6f410130b4052ca6954fab1d2aa913; head bda5ccabd6252a539c739aa78b710129348569fd; merge-base caf721ca4f6f410130b4052ca6954fab1d2aa913 |
| Requirements | jimmie-potts/agent-skills#83 at 2026-09-26T20:26:53Z |
| Policy | agent-skills@caf721ca4f6f410130b4052ca6954fab1d2aa913 |
| Standards | action-required |
| Specification | action-required |
| Reviewers | standards-reviewer-1: standards, requested opus at default, model claude-opus-5-5 (self-reported), level high (user-stated); specification-reviewer-1: specification, requested opus at default, model claude-opus-5-5 (self-reported), level high (user-stated) |
| Open findings | P0 0; P1 0; P2 1; P3 6 |

**Findings:**
- 83-F1 (P2, standards+specification, unresolved): skills/deliver-work/references/project-discovery.md:118-125, a squash-merged branch at the merged head is removable but the only removal the text leaves is `git branch -D`, the forcing flag it bans, so an unguarded delete can lose a commit that lands between the check and the delete; first final 1, latest final 1
- 83-F2 (P3, standards, unresolved): skills/deliver-work/references/project-discovery.md:95, `## Cleanup` sits above the file's general OpenSpec, alternate-host and resumption paragraphs, so they read as cleanup rules and the section test captures them; first final 1, latest final 1
- 83-F3 (P3, standards, unresolved): skills/deliver-work/references/resumption.md:134-136, the cleanup resumption rule has two homes that do not link to each other; first final 1, latest final 1
- 83-F4 (P3, standards+specification, unresolved): skills/deliver-work/SKILL.md:229-232, local-only and ready-PR-only stops never reach the cleanup reference, and the limited-request rule reads close to a tautology; first final 1, latest final 1
- 83-F5 (P3, standards, unresolved): skills/deliver-work/references/project-discovery.md:101-103, temporary clones have no explicit pre-deletion check for local changes or unpushed commits; first final 1, latest final 1
- 83-F6 (P3, specification, unresolved): skills/deliver-work/references/project-discovery.md:107-108, required post-merge CI is not said to pass, and retention names only missing CI; first final 1, latest final 1
- 83-F7 (P3, standards+specification, unresolved): tests/deliver-work-test.py:436-470, the cleanup test asserts exact phrases rather than only a missing checkpoint or an unsafe decision; first final 1, latest final 1

**Coverage:** Both axes covered the whole comparison, the 8 changed files, at head bda5cca. Neither reviewer ran tests, because their read-only runtime forbids the scratch export; both relied on hosted CI runs 36303835213 (pull_request) and 36303808900 (push) and the mutation record (15 of 15 rejected). 83-F1 is the same blocker on both axes; it is listed once with both axes, and both are action-required on it. The CL01-CL14 scenario trial on bda5cca (one fresh read-only Opus evaluator, graders withheld by instruction only because #82 is open) passed 14 of 14; its evaluator independently chose a guarded `git update-ref -d` for CL03 and raised 83-F8, which is listed from final 2 because no reviewer return supports it here. No specialist or human review is required. Redactions replace local paths only; no finding depends on them.

### Reviewer return: standards-reviewer-1

| Field | Value |
| --- | --- |
| Axis | standards |
| Comparison | base caf721ca4f6f410130b4052ca6954fab1d2aa913; head bda5ccabd6252a539c739aa78b710129348569fd; merge-base caf721ca4f6f410130b4052ca6954fab1d2aa913 |
| Requirements | jimmie-potts/agent-skills#83 at 2026-09-26T20:26:53Z |
| Policy | agent-skills@caf721ca4f6f410130b4052ca6954fab1d2aa913 |
| Return | complete |
| Digest | sha256:1b7790834c2aaabb577b61dae75de64867d259f9c507b8cc83dfcf040c14af09 |
| Redactions | 2: private path |

~~~text
## Standards review, round 1: jimmie-potts/agent-skills#83 (PR #97)

### Blocking findings

**S1 - P2 - `skills/deliver-work/references/project-discovery.md:118-125` (head bda5cca)**
- **What is wrong:** The Removed conditions say a branch is removable when "a branch tip equals the head the merge recorded, even when a squash merge keeps the host's safe-delete check from seeing it". The next rule says "Use the host's normal removal, never a forcing flag that overrides a dirty, locked or unmerged state." For the squash case these two rules contradict each other. The normal removal (`git branch -d`) refuses because the branch is "not fully merged". The only removal the text suggests is `git branch -D`, and that is exactly a forcing flag that overrides an unmerged state. The text never names a non-forcing, guarded deletion, such as a compare-and-delete against the verified tip (`git update-ref -d refs/heads/<branch> <verified-sha>`).
- **Violated standard:**
  - The unchanged deliver-work Boundaries forbid destroying another owner's work (`SKILL.md:34-36`).
  - `writing-for-agents` requires that a hard prohibition "pair it with the safe path when one exists" and that each rule have one meaning.
  - The change's own grader contradicts itself. `cleanup-graders.md` CL03 requires the branch to be removed. The rubric footer fails the whole trial for "using a forcing flag". The removal mechanism is left unspecified.
- **Concrete failure condition:**
  1. Take case CL03 (squash merge S1, tip H2, and `git branch -d` refuses).
  2. An agent that follows the text either retains the branch, which fails CL03, or runs `git branch -D`, which fails the trial under the forcing-flag rule.
  3. In a live delivery the agent will likely use `-D`. It checks the tip first and deletes afterwards, with no expected-value guard. If another session commits on the branch between the check and the delete (the CL04 situation arising mid-settlement), `-D` deletes the branch and its reflog. The unpushed commit then survives only as an unreferenced object.
  4. That destroys another owner's work, which the Boundaries forbid.
- **Likely cause:** `edge-case`. The squash case was anticipated, but no safe mechanism for it was specified.
- **Suggested direction (not a fix):** For branches, require a deletion guarded by the verified tip, and state that `-D` is still forbidden.

No P0 or P1 findings. No other project-defined blockers.

### Non-blocking P3 observations

- **P3-1: Unrelated paragraphs now sit under `## Cleanup`** (`project-discovery.md:95` and `147-161`).
  - `## Cleanup` was inserted above the file's trailing general paragraphs: OpenSpec tooling, alternate code host and resumption inspection. Those paragraphs now read as part of the Cleanup section, which the completion pointer `#cleanup` sends agents to.
  - `section(discovery, '## Cleanup')` in `tests/deliver-work-test.py` also captures them, so a required cleanup phrase moved into those paragraphs would still pass.
  - The misfiling already existed at base, under Declared completion steps. The insertion point kept it rather than fixing it.
  - Violates `writing-for-agents`: keep one concept's rules together.
- **P3-2: The resumption rule has two homes** (`resumption.md:134-136` and `project-discovery.md:142-145`).
  - Both state the cleanup-on-resumption rule: keep the recorded outcomes and re-read state before acting.
  - Neither links to the other.
  - This goes against "one authoritative home per meaning". Drift between them is plausible because the test checks each copy separately.
- **P3-3: Limited finish lines have no clear read trigger for the cleanup rules.**
  - The only entrypoint pointer to `#cleanup` is in "Merge and verify completion" (`SKILL.md:229-232`). Project discovery is otherwise read only for unfamiliar projects, conflicts or incomplete resumed records.
  - Yet the final Evidence field requires "the cleanup result" for every delivery (`SKILL.md:273-275`).
  - The rule for local-only and ready-PR-only requests (`project-discovery.md:136-138`) is therefore off the path those deliveries take. Its wording, "removes nothing beyond its own authority", is also close to a tautology.
  - Direct data loss would still need a forcing operation, so this is not blocking.
- **P3-4: No explicit pre-deletion check for temporary clones** (`project-discovery.md:101-103` and `118-120`).
  - Clones are in scope, but the concrete state checks cover only branches and worktrees. A clone is deleted by path, with no host safety check.
  - Only the generic "state matches what the delivery last verified" requires confirming there are no local changes or unpushed commits first. CL11's grader assumes that verification.
- **P3-5: The new structural test mostly mirrors prose.**
  - `test_cleanup_outcome_is_settled_at_completion` asserts 13 exact phrases.
  - This matches the existing installation-test convention, so it is not a departure. It does sit uneasily with the module's "structural contracts only" docstring.
  - Useful structural checks it does include: pointer before the completion update, the Completion row link, and case/grader ID parity.

### Status for the Standards axis

`action-required`, because S1 is open.

### Coverage

- **Examined:** every changed file in the frozen diff.
  - `README.md`
  - `skills/deliver-work/SKILL.md`: full head file. Boundaries are unchanged, three small entrypoint edits, 295 lines.
  - `references/project-discovery.md`: full head file.
  - `references/resumption.md`: the retention section.
  - `references/validation-scenarios.md`: the new paragraph and the adjacent pattern.
  - `tests/deliver-work-test.py`: the new tests, the `flat`/`section` helpers and the neighbouring installation tests.
  - `cleanup-cases.md` and `cleanup-graders.md`, compared with the installation case and grader pattern.
- **Checked against:**
  - Base `AGENTS.md`: catalog rules, the checks list (no new test file needed registering) and Installation.
  - Base `writing-for-agents` `SKILL.md` and `references/skill-mechanics.md`.
  - `[redacted: private path]`: no em dashes or curly quotes in added lines; storage and evidence rules are consistent with the new cleanup text.
  - `code-review` assigned-axis sections at base.
- **Destructive-action safety:**
  - Ownership limited to recorded resources: sound.
  - Unknown ownership leads to retain: sound.
  - Other sessions' resources out of scope: sound.
  - Evidence preserved outside before removal: sound.
  - Remote deletion treated as its own effect: sound.
  - Force prohibition: sound, apart from S1.
- **Not done:**
  - I did not run tests. My runtime is strictly read-only and forbids creating the scratch export, so I skipped the export and the test run, as the brief allows.
  - I relied on the implementer's record in `.local/evidence/deliver-83/mutation-checks.txt`: 15 mutations, all rejected. I also relied on the reported hosted CI (runs 36303835213 and 36303808900, both successful). I did not independently verify either.
  - I did not read `trial-request.md` or any other scratchpad or evidence file.
  - No behavioral-trial observations were committed, so I cannot confirm that CL01 to CL14 were exercised.
  - I did not use issue #83 or the PR narrative.

### Model

Opus 5.5 (`claude-opus-5-5`).

### Comparison and verification commands

- Base `caf721ca4f6f410130b4052ca6954fab1d2aa913`, head `bda5ccabd6252a539c739aa78b710129348569fd`, merge-base `caf721ca4f6f410130b4052ca6954fab1d2aa913` (matches). One commit: bda5cca.
- Commands:
  - `git -C <repo> rev-parse <base>^{commit} <head>^{commit}`
  - `git -C <repo> merge-base <base> <head>`
  - `git -C <repo> log --oneline caf721ca..bda5ccab`
  - `git -C <repo> diff --stat caf721ca bda5ccab`
  - `git -C <repo> diff caf721ca bda5ccab`
  - `git -C <repo> diff --check caf721ca bda5ccab` (clean)
  - `git -C <repo> diff caf721ca bda5ccab | grep -nP '[\x{2013}\x{2014}\x{2018}\x{2019}\x{201C}\x{201D}]'` (no matches)
  - `git -C <repo> show <rev>:<path>` for each file read
  - `git -C <repo> ls-tree --name-only <head> tests/fixtures/workflow-evaluation/`

  Here `<repo>` is `[redacted: private path]`.
~~~

### Reviewer return: specification-reviewer-1

| Field | Value |
| --- | --- |
| Axis | specification |
| Comparison | base caf721ca4f6f410130b4052ca6954fab1d2aa913; head bda5ccabd6252a539c739aa78b710129348569fd; merge-base caf721ca4f6f410130b4052ca6954fab1d2aa913 |
| Requirements | jimmie-potts/agent-skills#83 at 2026-09-26T20:26:53Z |
| Policy | agent-skills@caf721ca4f6f410130b4052ca6954fab1d2aa913 |
| Return | complete |
| Digest | sha256:2422aeba048a1380633a5ee8d5a3146785cc20b63c6b8d4a0066c15e66172893 |
| Redactions | 6: private path |

~~~text
## Specification review, final round 1: jimmie-potts/agent-skills#83 (PR #97)

### Blockers (P0-P2)

**P1-equivalent: none. P2: one.**

**P2-1: P2. The squash-merge hard case has no permitted removal path.**
- **Where:** `skills/deliver-work/references/project-discovery.md:118-123` at head `bda5cca`.
- **What is wrong:**
  - Lines 118-120 make a branch removable when "a branch tip equals the head the merge recorded, even when a squash merge keeps the host's safe-delete check from seeing it".
  - Lines 122-123 then require "the host's normal removal, never a forcing flag that overrides a dirty, locked or unmerged state".
  - For a squash-merged branch, the host's normal removal (`git branch -d`) refuses because Git considers the branch not fully merged. The only standard removal is `git branch -D`, which is exactly a forcing flag that overrides an unmerged state.
  - The text names no guarded alternative, such as a compare-and-delete `git update-ref -d refs/heads/<branch> <merged-head>` after re-reading the tip. That leaves no compliant way to act on the removal the text grants.
- **Requirement evidence:**
  - Issue #83 Observable acceptance item 2 names "a squash-merged exact PR head" as a hard case.
  - Item 1 requires that a delivery with an applicable rule "performs only its eligible owned cleanup and reads back removal".
  - The Outcome is motivated by the audit of 124 local branches left behind by merged PRs.
  - The PR's own grader, `tests/fixtures/workflow-evaluation/cleanup-graders.md` CL03, expects: "the branch is removable under the policy… Read back every removal."
- **Failure condition:** CL03, as written in `cleanup-cases.md`. The PR merged as squash S1, the tip is still H2, the remote is gone, and `git branch -d deliver-widgets-11` refuses. An agent following the head text either:
  - (a) retains the branch because the normal removal failed and forcing is forbidden. That fails CL03 and acceptance item 2, and squash-merge repositories keep accumulating branches, which is the audit's failure mode; or
  - (b) runs `git branch -D`, which contradicts the text's own safety rule and teaches that the forcing ban is negotiable.

  Either way the instruction is internally inconsistent for a named hard case on a destructive action.
- **Concrete fix direction (not applied):**
  - Narrow the forcing ban to dirty and locked worktrees, or to a branch whose tip does not equal the merged head.
  - For the exact-head squash case, specify a guarded deletion: re-read the tip, then delete conditioned on that tip, for example `git update-ref -d refs/heads/<b> <H>`, or `-D` only immediately after that check. Then read it back.
  - The existing test phrase `'never a forcing flag'` can remain.
- **Likely cause:** `edge-case`.

### Non-blocking P3 observations

1. **Local-only and ready-PR-only stops never reach the cleanup reference** (`skills/deliver-work/SKILL.md:229-232`, `:10-11`). The rule "A local-only, ready-PR-only or planning-only request removes nothing beyond its own authority and reports what it retains" (`project-discovery.md:136-138`) lives in a reference that SKILL.md links only from the post-merge completion paragraph. `project-discovery.md:3-5` triggers it only "at completion". A delivery stopping at a limited finish line still reports "the cleanup result" through the Evidence field (`SKILL.md:273-275`). But without the reference, it has no instruction to give each retained worktree or branch a reason, owner and next action, which is CL12 variant 1's expectation. No removal happens, so this is a reporting-completeness gap, not a safety defect. A one-clause pointer at the finish-line stop would close it.
2. **"Required post-merge CI" does not say it must pass** (`project-discovery.md:107-108, 126-128`). Retention lists only "missing post-merge CI". The CL08 failing-CI variant most likely resolves correctly because SKILL.md's existing post-merge rule keeps the item open, but "passed" would remove the ambiguity.
3. **The structural test mostly asserts exact phrases.** `tests/deliver-work-test.py:436-470` checks 13 exact phrases in the Cleanup section. The issue says to add "only checks that reject a missing checkpoint or an unsafe decision, not tests that mirror prose." The ordering assertion (checkpoint link before "Once all required conditions pass") and the case/grader parity test are clearly in scope. The phrase list follows the precedent set by #69's installation test (`:392-433`), and the implementer's record shows each phrase guards a safety rule (15/15 mutations rejected). It is still brittle to rewording that keeps the meaning. Consistent with repository precedent, so not blocking.
4. **The cases file sits beside the grader file in the same directory**, with instruction-only withholding. This matches the current procedure (#82 is still OPEN), and `cleanup-graders.md` requires recording which withholding method a trial used. No action needed.

### Requirement trace (satisfied items)

- **Policy discovered at preparation:** `SKILL.md:65-67`; the Completion row at `project-discovery.md:19`.
- **Resources recorded at creation:** `SKILL.md:84-86`; `project-discovery.md:101-105`.
- **Applied after merge, CI, evidence, consumer and ownership checks:** `project-discovery.md:107-120`.
- **All five resource kinds covered** (worktrees, branches, scratch, clones, staging), with a separate remote outcome: `:101-103`, `:133-136`.
- **Remote disappearance proves nothing about local resources:** `:134-135`.
- **Removed / retained / not applicable, with reason, owner or `unknown`, and next action:** `:110-131`.
- **Private evidence outside removed directories; neutral labels in public records:** `:113-114`, `:140-142`.
- **Resumption keeps the recorded outcome and re-reads before acting:** `:142-144`; `resumption.md:134-136`.
- **No waiting on acceptance that does not use the resource:** `:115-117`.
- **No unrelated cleanup:** `:144-145`, plus the existing Boundaries rule.
- **No new ledger, schema, skill or background process.** Evidence reuses the existing field (`SKILL.md:273-275`); the Execution record grammar is unchanged.
- **Hard cases:**
  - Moved tip, dirty/locked worktree, another owner, missing CI, acceptance consumer, unavailable tool exit and unregistered clone are each addressed.
  - The squash-merge case is not addressed (P2-1).
  - CL01-CL14 cover every named hard case, and their grader rows map to A1-A4.
- **Deferrals respected:** nothing touches close-work, retroactive cleanup, expiry or a janitor.
- **Installation:** the change stays within `skills/deliver-work`, README and tests. Nothing in it prevents the declared installation from running after merge.

### Status for this axis
`action-required`: P2-1 remains.

### Coverage
- **Examined:**
  - All 8 changed files in full diff.
  - Head context of `skills/deliver-work/SKILL.md` (whole file), `references/project-discovery.md` (lines 1-150), `references/resumption.md` (100-136) and `references/validation-scenarios.md` (1-60).
  - The new fixtures `cleanup-cases.md` and `cleanup-graders.md`.
  - The new tests and the neighbouring #69 precedent test.
  - A grep of base `AGENTS.md` for cleanup policy (none; this repo declares no cleanup rule, which matches the coordinated-adoption deferral).
  - Issue #83's body and comment, #82's state, and the implementer's mutation record.
- **Not done:**
  - I did not run tests. My runtime is strictly read-only and forbids creating files or directories, including the scratch export.
  - I relied on the reported CI runs 36303835213 and 36303808900 and the mutation record as reported facts, not verified results.
  - I did not run the CL01-CL14 scenario trial; it is running separately.
  - I did not read the PR narrative or other reviewers' output.
- **Evidence limits:** P2-1 rests on documented Git behavior (`git branch -d` refuses a non-ancestor branch; `-D` is `--delete --force`) and on the fixture's own statement that `-d` refuses. I did not execute it.

### Model
Opus 5.5 (`claude-opus-5-5`).

### Comparison and verification commands
- Base `caf721ca4f6f410130b4052ca6954fab1d2aa913`; head `bda5ccabd6252a539c739aa78b710129348569fd`; merge-base `caf721ca4f6f410130b4052ca6954fab1d2aa913` (verified to match). One commit: `bda5cca`.
- `git -C <repo> rev-parse <base>^{commit} <head>^{commit}`; `git -C <repo> merge-base <base> <head>`; `git -C <repo> log --oneline caf721c..bda5cca`; `git -C <repo> diff --stat caf721c bda5cca`
- `git -C <repo> diff caf721c bda5cca -- README.md skills/` and `-- tests/`
- `git -C <repo> show bda5cca:<path>` for SKILL.md, project-discovery.md, resumption.md, validation-scenarios.md and tests/deliver-work-test.py; `git -C <repo> show caf721c:skills/code-review/SKILL.md` and `caf721c:AGENTS.md`
- `gh issue view 83 --json title,body,comments` (plain `--comments` failed on a Projects-classic GraphQL deprecation); `gh issue view 82 --json state,title`
- `cat [redacted: private path]`

`<repo>` = `[redacted: private path]`.

### Critical files for implementation
- [redacted: private path] (lines 118-125)
- [redacted: private path] (lines 229-232, 273-275)
- [redacted: private path] (lines 436-482)
- [redacted: private path] (CL03 row)
~~~
