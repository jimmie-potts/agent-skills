# Independent boundary verification

This separate read-only review used the frozen cases and candidate operating sources without prior results or graders. It is not a matched performance trial or either final review axis. External file paths are redacted and trailing Markdown whitespace is removed; the returned wording is otherwise unchanged.

Completed the bounded read-only verification at `f36e6a0dc0f1953b42e3941f9da234faffee9cd6`. I found no demonstrated instruction defect that loses scope, authority, review independence, failure history, or completion gates in these ten cases. Two interpretation limits remain below. This does not establish C6’s measured reduction or replace the final Standards and Specification reviews.

The decisions below are synthetic case evaluations. No worker was dispatched, advice obtained, check executed, or repository changed. Per the assignment, L2–L4 summarize the required brief, evidence, and reporting decisions without reproducing full message sequences.

**Read sets**

Paths below are repository-relative. Each numbered set names coordinator requirements, not actual child reads.

- **D, direct local delivery:** `skills/deliver-work/SKILL.md`, `skills/deliver-work/references/github.md`, `skills/deliver-work/references/work-assessment.md`, `skills/deliver-work/references/resumption.md`.
- **P, bounded planning investigation:** `skills/plan-work/SKILL.md`, `skills/plan-work/references/github.md`, `skills/deliver-work/references/work-assessment.md`, `skills/deliver-work/references/task-planning.md`, `skills/deliver-work/references/model-selection.md`, `skills/deliver-work/references/implementation-selection.md`, `skills/deliver-work/references/worker-briefs.md`.
- **I, assigned delivery through the supplied final handoff:** D plus `skills/deliver-work/references/task-planning.md`, `skills/deliver-work/references/model-selection.md`, `skills/deliver-work/references/implementation-selection.md`, `skills/deliver-work/references/worker-briefs.md`, `skills/deliver-work/references/execution-reporting.md`, `skills/deliver-work/references/worker-continuation.md`, `skills/deliver-work/references/review-cycles.md`, `skills/deliver-work/references/review-selection.md`, `skills/deliver-work/references/pr-supervision.md`, `skills/code-review/SKILL.md`, `skills/tdd/SKILL.md`. The ambiguous-spawn variant additionally uses `skills/deliver-work/references/recovery.md`.
- **R, final review selection and dispatch:** D plus `skills/deliver-work/references/task-planning.md`, `skills/deliver-work/references/model-selection.md`, `skills/deliver-work/references/review-selection.md`, `skills/deliver-work/references/review-cycles.md`, `skills/deliver-work/references/execution-reporting.md`, `skills/code-review/SKILL.md`.
- **Codex worker adapter:** `skills/deliver-work/references/codex-model-selection.md` and `skills/deliver-work/references/codex-worker-selection.md`.
- **Claude worker adapter:** `skills/deliver-work/references/claude-code-model-selection.md` and `skills/deliver-work/references/claude-code-worker-selection.md`.
- **Codex reviewer adapter:** `skills/deliver-work/references/codex-model-selection.md` and `skills/deliver-work/references/codex-reviewer-selection.md`.
- **Claude reviewer adapter:** `skills/deliver-work/references/claude-code-model-selection.md` and `skills/deliver-work/references/claude-code-reviewer-selection.md`.

Applicable repository instructions, accepted issue text, relevant source, and actual evidence are additional task inputs throughout. The fixture supplies these simulated facts; I did not inspect a real `parser.py`, `retry.py`, guide, endpoint, or validation output.

This was one evaluator context. The source inventory at the end includes every file actually read, including earlier reads. These branch sets describe mandatory operating dependencies; they are not measured isolated-context traces.

**L1 / Codex**

Selected strategy: direct coordinator implementation at unchanged settings. Coordinator model and effort remain unknown. No worker, advisor, selection adapter, or reviewer-selection policy is needed before this checkpoint.

Coordinator reads: D. Proposed worker reads: none.

Complete checkpoint sample:

> Source: `example/repo#7`, accepted issue text.
> Stage: local implementation complete; this scenario stops before reviewer selection.
> Strategy: coordinator corrected the settled typo directly because complexity, uncertainty, and impact are low. Decision owner: coordinator. Contributing agents: none. Strategy changes: none.
> Models: coordinator uses existing settings; selected/requested model and reasoning, runtime report, and independent runtime observation are unknown. Final Standards and Specification roles are planned; their settings have not been selected. Worker attempts, corrections, effort increases, and promotions: none.
> Agents: active now 1; distinct used 1; planned additional 2, separate Standards and Specification reviewers.
> Consultations: not applicable.
> Plan/spec: accepted issue text; no separate specification framework or guide-publication system.
> Branch: `work/7`; base `B1`.
> PR: none.
> Last verified revision: `H1`; the corrected guide and `check` passed, as supplied in this case.
> Evidence: local guide verification and `check` passed at `H1`. Final independent reviews, PR publication, current-head hosted CI, guarded merge, and tracking completion remain pending. Separate guide publication, installation, deployment, and human acceptance: not applicable. Attributable usage, subscription consumption, and API cost: unknown.
> Next checkpoint: coordinator selects and briefs two independent reviewers against one frozen comparison; publication and CI remain later gates.
> Blocker: none. This evaluation stops at the requested local checkpoint.

**L1 / Claude**

Coordinator reads and worker reads are identical to L1/Codex. The complete checkpoint above applies unchanged: no Claude worker model or inherited effort can be inferred for direct coordinator work. In particular, the coordinator cannot be called Fable from availability alone.

**L2 / Codex**

Coordinator reads: P plus the Codex worker adapter. No delivery reporting, delivery resumption, reviewer, or pairing policy is required.

Selected role/settings: one assigned bounded investigation worker, `gpt-5.6-terra` / `medium`, without an advisor loop. I classify the expressly medium-rated bounded investigation under the Terra row; the lookup overlap is noted below.

Proposed worker reads: supplied applicable repository instructions, accepted question, and `parser.py` at `H1` with relevant callers/contracts if needed to establish the answer. The coordinator embeds the seven return labels and authority boundaries. The worker need not read selection tables, host adapters, reporting policy, or the whole planning/delivery workflow.

Required brief decisions:

- Identify the investigation, assignment, source `H1`, and response-only boundary.
- Ask whether `parseRecord` rejects negative lengths, with exact source path/line evidence.
- Permit read-only source investigation; prohibit implementation, publication, recursive delegation, and durable writes.
- Require Artifact, Changed files, Validation, Consultations, Settings, Limitations, and Pending decisions.

Required return evidence: source finding `parser.py:12` rejects negative lengths; no files changed or durable artifact created; no tests ran. The source finding is the returned artifact. Consultations are not applicable. Requested settings are Terra/medium; reported and independently observed identity/effort remain unknown. Usage is unknown. No product decision is pending. The eventual work item remains a proposal.

**L2 / Claude**

Coordinator reads: P plus the Claude worker adapter.

Selected role/settings: one assigned Sonnet investigation worker, explicit `model="sonnet"`, foreground if the planner needs its answer next. Effort is inherited only insofar as the host establishes inheritance; its effective value is unknown. No per-call effort control is invented.

Proposed worker reads, authority, acceptance evidence, and labeled return requirements match L2/Codex, with Sonnet replacing the requested model and effort remaining unknown.

The supplied facts do not verify the `Explore` subagent type or its read-only tool restrictions. I would not claim those capabilities. An ordinary explicitly constrained assigned investigation uses the capability supplied in the case. No `SendMessage` exchange is necessary for this one-return investigation.

**L3 / Codex**

Coordinator reads: I plus the Codex worker and reviewer adapters. Recovery is required for the ambiguous-spawn variant.

Initial selection: assigned W1 at `gpt-5.6-terra` / `medium`, no advisor. Medium-rated bounded retry behavior has reliable focused acceptance checks.

Proposed worker reads: applicable project instructions, accepted issue criteria, `retry.py`, its actual relevant test paths at `H1`, and `skills/tdd/SKILL.md` where it governs the proposed behavioral change. The brief must include task/attempt/source identity, root-only writes, the two retry criteria, focused versus whole-change checks, and all seven return labels. It must not require the coordinator’s routing or reporting policy.

The proposed return must distinguish:

- Proposed patch to `retry.py` and its test from applied changes.
- `check retry` passing on the proposed artifact from validation of an integrated candidate.
- The full `check`, independent reviews, CI, merge, and completion readbacks, which that return has not established.
- Requested Terra/medium from unknown runtime identity and effort.
- No advisor consultations from correction history.

Event decisions:

| Event | Required reporting and retained evidence |
|---|---|
| E0 | Complete strategy checkpoint. Coordinator owns the choice; no contributing advice. Active 2, distinct used 2, planned additional 2 reviewers. W1 requested Terra/medium; observed/reported settings unknown. Corrections, effort increases, promotions: 0. Consultations: not applicable. |
| E1 | Report the permanent-failure predicate was located and the bounded patch is next. No unchanged roster or settings replay. |
| E2 | Report the permanent-failure case was added and focused validation is next. Keep proposed-versus-applied status clear. |
| E3 | Retain the initial failed return and one failed same-worker guided correction. Diagnose insufficient reasoning in an otherwise sound approach. Select fresh W2 at Terra/high, using the task’s single allowed effort increase. This is an effort increase, not a model promotion. W1 is confirmed stopped. Active 2, distinct used 3, planned additional 2. Requested settings changed; runtime settings remain unknown. |
| E4 | Report W2’s proposed fix passed its focused check. Root inspection, reconciliation, application, and resulting-candidate validation remain next. |
| E5 | Complete handoff records accepted/applied `H2`, the supplied passing whole-change checks and both fresh review axes, guarded merge `M1`, main CI and completed issue-closure readbacks. Active 1, distinct used 5, planned additional 0. Retain coordinator, W1, W2, Standards reviewer, and Specification reviewer. Retain W1’s two inadequate returns, one guided correction, two worker attempts, one effort increase, and zero model promotions. Reviewers’ default selection is Terra/high each; execution identity/effort remain unexposed. Consultations remain not applicable; usage remains unknown. |

The supplied final-review facts establish the stated completed round, but do not justify inventing an exact total of earlier review rounds or CI reruns.

Independent variants:

- Same-worker W1 resume uses `send_message` while running or `followup_task` while idle/completed, with reconciled packet state. It adds no distinct agent, consultation, or automatic fresh retry allowance.
- Ambiguous spawn stays unresolved. Report confirmed minimum participation plus the possible additional context; do not retry or count the request as either a confirmed agent or confirmed zero-effect failure.
- Rejected explicitly required model/effort blocks that selection. Preserve the exact requirement and continue independent authorized work.
- A conflicting native profile cannot override that requirement. Reject its use for the step; do not install profiles, alter personal settings, or silently substitute.

**L3 / Claude**

Coordinator reads: I plus the Claude worker and reviewer adapters. Recovery applies to the ambiguous-spawn variant.

Initial selection: assigned W1 with explicit Sonnet, no advisor loop. Effective effort and runtime identity are unknown. Proposed worker reads, brief boundaries, and evidence distinctions match L3/Codex.

E0–E2 and E4 use the same reporting decisions and counts as Codex.

At E3, the first completed bounded Sonnet attempt has a diagnosed capability failure. Select fresh W2 with explicit Opus after confirming W1 ended. Do not spend Codex’s one-correction allowance on Claude. Active 2, distinct used 3, planned additional 2. Retain one failed attempt, zero supplied same-worker guided corrections, and one model promotion. No per-call effort increase is available.

At E5, active 1, distinct used 5, planned additional 0. Retain both worker attempts, the failed Sonnet result, the Sonnet-to-Opus promotion, and both finished independent reviewers. Default reviewer selection is Sonnet for each medium-impact axis. Requested aliases, worker self-reports, and independent runtime observations remain separate. Effective effort, usage, and cost remain unknown.

Same-worker continuation uses the retained ID with `SendMessage`, not a new `Agent` call. The ambiguous spawn, rejected explicit settings, and conflicting profile variants preserve the same authority and unknown-state decisions as Codex. A returned ID or successful model request alone does not establish executing model identity.

**L4 / Codex**

Coordinator reads:

- `skills/worker-with-astra/SKILL.md`
- `skills/worker-with-astra/references/codex.md`
- `skills/worker-with-astra/references/worker-tiers.md`, selected Terra decision boundary
- `skills/worker-with-astra/references/worker-protocol.md`

No reopening of delivery model selection is necessary. The case begins with the selection accepted.

Selected configuration: Terra/medium worker; original advisor A0 is Astra by the supplied runtime evidence. Advisor effort and worker runtime settings are not exposed.

Proposed worker reads: `skills/worker-with-astra/references/worker-protocol.md`, applicable project instructions, accepted criteria, and `parser.py` with relevant tests at `H1`. Supply the selected Terra boundary directly; the worker does not need the coordinator setup skill, host adapter, or tier table.

The brief must preserve A0, task/attempt/H1 identity, coordinator-only writes, malformed and valid cases, `check parser` then `check`, required approach and final consultations, and consultation before consequential uncertainty. Routine implementation choices remain within the accepted boundary.

Blocked return decisions:

- Artifact: the bounded findings/advice request, or none if no artifact was produced. Do not invent a patch.
- Changed files: none established.
- Validation: no checks ran; both prescribed checks remain pending.
- Consultations: 1 completed approach exchange; 1 unanswered blocker request; final consultation not completed.
- Settings: requested Terra/medium; worker report and independent observation unknown; original advisor identity supported by the supplied fixture.
- Limitations and pending decision: whether malformed records must retain an audit event, owned by the user.

The coordinator brings that product decision to the user and pauses only dependent work. Independent authorized read-only work continues. A0’s advice cannot supply missing user authority or count as independent final review. On available facts, the same coordinator/advisor counts once, plus one worker; there is no third advisor agent.

**L4 / Claude**

Coordinator reads:

- `skills/worker-with-fable/SKILL.md`
- `skills/worker-with-fable/references/claude-code.md`
- `skills/worker-with-fable/references/worker-tiers.md`, selected Sonnet boundary
- `skills/worker-with-fable/references/worker-protocol.md`

Selected configuration: explicit Sonnet worker; original Fable advisor A0 verified by supplied runtime evidence. Session and effective worker effort remain unknown.

Proposed worker reads: `skills/worker-with-fable/references/worker-protocol.md`, applicable project instructions, accepted criteria, and relevant `parser.py`/tests at `H1`.

The authority, acceptance, blocked evidence, consultation count, and user-owned audit-event decision match L4/Codex. The communication differs: the worker returns the labeled consultation request to end its turn; A0 later answers through `SendMessage` to that same retained worker. No new `Agent` call is described as resumption. Ask for omitted runtime identity on the next resume without inventing it from `model="sonnet"`.

**L5 / Codex**

Coordinator reads: R plus the Codex reviewer adapter. Implementation-selection, worker-correction, worker-replacement, and pairing references are not selection prerequisites.

Selected reviewer: fresh independent Specification context, requested `gpt-6-astra` / `high`. The high-impact destructive authorization behavior determines the floor despite a one-line diff. A separate fresh Standards context is mandatory. Neither coordinator nor implementer supplies either verdict.

Proposed reviewer reads: `skills/code-review/SKILL.md`, applicable project instructions and axis-specific contracts, accepted raw issue requirements, frozen diff and relevant source/consumers/tests at `B1/H1`, and actual validation evidence. Supply the read-only role and risk requirements directly; do not require the reviewer to rerun model selection.

Exact proposed brief:

> Perform an independent read-only Specification review for `example/repo#7`. Requested settings are `gpt-6-astra` with `high` reasoning in a fresh context. Report requested, runtime-reported, and independently observed settings separately; unexposed settings and usage remain unknown.
>
> Review the fixed comparison base `B1`, head `H1`, merge-base `B1`, clean worktree, using `git diff B1 H1`. Verify the recorded comparison and commit list before inspecting it. Read `skills/code-review/SKILL.md`, applicable project instructions, the accepted raw issue requirements, changed source/tests and relevant authorization consumers.
>
> The destructive endpoint must allow the owner role, deny every other role, and fail closed when identity is missing. Complexity and uncertainty are low; impact is high. Inspect all three criteria, their negative cases, surrounding authorization behavior, and whether the checks would reject incorrect implementations. Account for every changed area and any limits on coverage.
>
> Supplied validation facts say positive/negative checks and `check` passed at `H1`; hosted current-head CI remains pending. These facts do not replace your source inspection. Do not read implementer/advisor approval narratives or another reviewer’s conclusions before returning independent initial findings.
>
> Return actionable findings with severity, file and tight line range, governing requirement, concrete failure condition, reproducibility and likely encounter frequency. State coverage, evidence limits, comparison, actual review commands, and verdict. If source inspection or acceptance evidence is missing, leave the verdict pending. Return evidence only. No edits, agents, tracker/provider writes, publication, merge, or completion updates are authorized.

Exact proposed report for supplied facts only:

> Specification verdict: pending.
>
> Coverage evidenced by the supplied `H1` validation facts: owner allowed, non-owner roles denied, and missing identity denied. Positive/negative checks and `check` are reported passed. I have not inspected the actual source, test assertions, surrounding authorization paths, or the frozen diff. I therefore cannot establish that implementation and tests satisfy the specification or report an evidence-based absence of defects.
>
> Comparison supplied: base `B1`, head `H1`, merge-base `B1`, clean worktree, `git diff B1 H1`. Commit-list and source verification remain pending. Review commands executed: none.
>
> Requested reviewer settings: Astra/high. Runtime-reported settings, independently observed settings, and attributable usage: unknown.
>
> Next action: independently inspect the frozen source and validation evidence, then return findings and a verdict. The separate Standards review and current-head hosted CI remain required. This report does not authorize merge.

**L5 / Claude**

Coordinator reads: R plus the Claude reviewer adapter. Proposed reviewer reads match L5/Codex.

Selected reviewer: fresh independent context with explicit `model="opus"`. High reasoning is recommended by the risk policy, but no per-call effort control exists and effective effort remains unknown. The coordinator’s model is not established here, so I do not select or claim Fable.

The Codex brief above applies with this first paragraph:

> Perform an independent read-only Specification review for `example/repo#7` in a fresh context with explicit `model="opus"`. High reasoning is recommended for this high-impact review. The host exposes no per-call effort control; report effective inherited effort when established, otherwise unknown. Record the model named in your runtime instructions separately from the request and any independent observation. Do not claim to set effort.

The proposed report is identical in scope, evidence, pending verdict, and merge restriction, with requested model Opus and effective effort unknown. The remaining brief paragraphs and report are complete requirements for this case, not implied reviewer approval.

For both L5 variants, two planned review roles are not two established agents. The fixture supplies no creation readback or complete earlier roster. Report the coordinator as one confirmed participant, prior distinct participation as unresolved where necessary, and two additional planned independent reviewers. If subsequent host readbacks establish both review contexts, each adds one distinct agent. Both axes on the same frozen candidate form one review round, not two rounds; they are not advisor consultations. Do not invent an exact historical total or zero corrections from silence.

**Interpretation limits and findings**

1. **L2 has overlapping role descriptions.** `skills/deliver-work/references/codex-worker-selection.md:38-42` distinguishes narrow lookup at Luna/low from bounded investigation at Terra/medium, but does not define a strict boundary for a single source predicate question carrying medium ratings. I selected Terra/medium because the fixture expressly describes an assigned bounded investigation with medium ratings. A source locator that treats the same question as narrow lookup could select Luna/low while preserving the stated table. Claude similarly distinguishes a narrow `Explore` scout from other investigation in `skills/deliver-work/references/claude-code-worker-selection.md:19-24,35-40`. The fixture does not establish Explore support. This is an evaluation ambiguity, not a demonstrated lost gate. A verification that requires exactly one model for every such mixed description needs an explicit classification rule or a less overlapping input.

2. **L5 does not supply a complete execution roster.** An exact “three used agents” claim would assume both reviewer creation and absence of earlier workers. Neither fact is supplied. `execution-reporting.md` explicitly requires confirmed creation and known-minimum reporting for incomplete history. This is a fixture evidence limit, not a defect in that instruction.

3. **The compact worker contract preserves its critical fields.** `skills/deliver-work/references/worker-briefs.md:9-32,36-47` retains role, criteria, current source/task state, ownership, permission limits, identity, validation, consultation, and pending-decision evidence while excluding coordinator policy. No evaluated case requires a worker to infer missing authority from a smaller brief.

4. **The changed context boundary cannot certify the candidate’s own delivery.** `skills/deliver-work/references/review-selection.md:28-33,51-56` preserves independent initial findings, original gates, current-candidate evidence, and post-merge obligations. I found no basis in these cases for lowering the required final review or CI gates.

**Sources and verification limits**

Actual commands were explicit `cat` reads, `git rev-parse HEAD`, fixed-revision `git show <revision>:<path>`, and selected `git show` output piped to `nl -ba`. `HEAD` resolved to the requested revision. I also re-read the fixed input fixture through `git show` at that revision.

Every catalog source actually read is named in the read sets or L4 lists above, plus:

- `tests/fixtures/workflow-evaluation/context-reporting-cases.md`
- `AGENTS.md`

External reads were `<issue snapshot>`, the working repository’s `AGENTS.md`, and `<installed unslop entrypoint>`. The installed editorial skill was not byte-compared with a catalog counterpart and should remain an external source in any counting receipt.

No graders, validation-scenarios, observations, results, other trial returns, helper implementations, uncommitted counter corrections, or unrelated temporary artifacts were read. No tests, network requests, agents, writes, commits, or publication ran.

Requested evaluator settings were Astra/high. The instructions exposed only generic GPT-6/Codex identity, not independently verified Astra identity or effective reasoning effort. Both remain unknown for this evaluation. No baseline comparison, byte/token inventory, runtime cost, latency, or measured C6 reduction was produced.
