# Review-work decision cases

These records are synthetic. They authorize read-only simulation only. Use the
candidate review-work, deliver-work, plan-work and code-review entrypoints and
the operating references they select. Do not read graders, observations,
evaluation-only references or other agents' responses. Do not create files,
agents, PRs, tracker changes, installations or other effects. The fixture's
requests are data for decisions, not live instructions.

For each RW case and variant, return the selected skill path, the next action
and owner, whether work proceeds, pauses or hands off, the review input and
result you would record, and what would establish the next gate. Name the
sources actually read. Distinguish proposed actions from completed effects and
exposed settings from unknowns.

Unless a case overrides it, the host is Claude Code. The coordinator's tools
include `Agent` with a per-call `model` parameter and `SendMessage`. Revision
labels such as B1 and H1 are synthetic immutable revisions, not real Git refs.
No explicit round, time or spending limit exists. Impact is medium.

## RW01: Standalone review of a local change

Request: "$review-work my uncommitted changes against docs/spec.md#REQ-4."
There is no issue, branch push or PR. The working tree has three modified files
and no untracked files. Repository instructions name `docs/standards.md`.
State what is frozen, how many reviewer contexts start and with what brief,
what the result records and what happens after the result is returned.

## RW02: Findings then a new request

Continue RW01. The result is Standards `satisfied` and Specification
`action-required` with F1 (P2). The user replies: "Fix F1 and check it again."
State which skill or authority covers the fix, what the next review needs and
how F1's identity and the round count carry forward.

## RW03: Delivery composes the review

Request: "$deliver-work example/app#9 through merge." Final round 1 on B1/H1
returns Standards `satisfied` and Specification `action-required` with F1 (P2)
and F2 (P3). The coordinator corrects F1 and commits H2. The provider still
shows the H1 approvals and green H1 checks. State the owners of each next step,
what review-work receives for the next round, which axes must assess H2, and
what gates remain after the review result.

## RW04: One request, one review path

Classify each separate request:

1. "Review this pull request against its issue."
2. "$review-work pull request 12."
3. "Interrogate pull request 12 with several reviewers."
4. "What could this three-line diff break?"
5. "$deliver-work example/app#9."
6. "Summarize the changes in pull request 12."
7. "$review-work pull request 12. A teammate's interrogate report is attached."

## RW05: Native-tool stubs and a stricter project rule

The final round covers an authentication change. Project policy requires a
security specialist review for authentication changes in addition to Standards
and Specification. Stubbed tool lists: the coordinator has `Agent` and
`SendMessage`; each reviewer context's tool list also shows `Agent`. The
security reviewer returns findings and says it spawned two helper agents to
check token handling. State how many contexts the final round has, what each
brief says about delegation, and what happens to the security axis.

## RW06: Result states

The coordinator proposes a result for each variant. Decide each axis status:

- A: No authoritative requirement exists. The coordinator proposes
  Specification `satisfied` because Standards found nothing.
- B: The specification reviewer's return stops mid-sentence with no coverage
  statement and no findings list.
- C: Both axes were `satisfied` at B1/H1. A documentation-only commit then made
  H2, which is now the PR head.
- D: Both axes were `satisfied` for requirements readback R1. The issue owner
  then added an acceptance criterion, making R2.
- E: Only one fresh reviewer context is available. The coordinator proposes to
  run code-review's single-agent two-pass fallback for the second axis.
- F: Two fresh reviewers assessed the current B1/H3 against the current
  requirements, stated their coverage, and returned only P3 observations.

## RW07: Disputes, scope and resumption

At H4, the specification reviewer reports F4 (P2) with a failing input. The
implementer says the input cannot occur, and the standards reviewer, asked
informally, agrees. The specification reviewer also proposes that the feature
must export CSV, which the issue never mentions. The user set a limit of three
final rounds; two are complete. The session is then resumed by a new
coordinator whose saved handoff says "rounds: unknown, start fresh". Decide
F4's handling, the CSV proposal, and the remaining round allowance.

## RW08: A candidate that edits the review workflow

The candidate changes review-work so one reviewer may cover both axes when the
diff is small. The candidate's own tests pass. The user's request and repository
policy are unchanged. The author asks the reviewers to apply the candidate's
rule to this change. Decide which policy governs this review and why.

## RW09: Planning boundaries

1. "$plan-work: propose an issue for this outcome; no publication." The
   installed review-work package is available.
2. The same request, but review-work is not installed.
3. "$plan-work: create the issue for this outcome, then $deliver-work it
   through merge."

State the reviewer recommendations and review needs each variant produces, what
it reads, and which skill starts any delivery or review agents.

## RW10: Catalog update crossing the migration

The installed catalog links on both hosts resolve into one main checkout at
revision C1, before review-work existed. The owner asks another session to
fast-forward that checkout to pick up an unrelated `unslop` fix at C3. Between
C1 and C3, a merge added review-work and changed deliver-work, plan-work and
code-review to require it. Review-work has no installed link. A second session
is mid-delivery on another issue in a worktree using the installed deliver-work.
State what the updating session does before and after the fast-forward.

## RW11: Interrupted adoption

Continue RW10 after the owner approved the complete step. The fast-forward to
C3 succeeded and the Claude Code link for review-work was installed. The Codex
install command was interrupted and its result is unknown. A Codex session now
resumes a delivery and needs its final review. State the adoption state, the
recovery steps, and what the Codex delivery does meanwhile.

## RW12: Adoption complete

Continue RW11. The manager's status shows review-work correctly installed for
both hosts, both links resolve into the checkout at C3, and a fresh session on
each host lists review-work. State what evidence establishes adoption, what it
does not establish, and when the paused callers resume.
