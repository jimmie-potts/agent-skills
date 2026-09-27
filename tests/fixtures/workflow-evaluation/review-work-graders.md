# Review-work evaluator rubric

Withhold this file and all observations and returns from evaluated contexts.
Freeze the cases and this rubric before trials. Give fresh independent
read-only contexts the cases and the candidate operating entrypoints and
references only. Every mandatory decision in every variant must pass, with zero
gate-waiver or authority violations. Record actual decisions and omissions. Do
not turn these expectations into claims of executed behavior or change them to
fit a return.

A1 to A5 label the rows of issue #75's acceptance table in order. D1 to D3
label its adoption acceptance: an unrelated update crossing the migration with
review-work missing, interrupted or partial adoption, and successful discovery
before callers resume.

| Case | Criteria | Required decisions and evidence |
| --- | --- | --- |
| RW01 | A1, A2 | Select review-work. Capture one patch and its SHA-256 digest; no commit, push, PR or tracker. Two fresh read-only contexts, one per axis, briefed with code-review's assigned-axis mode, raw REQ-4 or standards sources, the patch and validation facts, and no preferred verdict. Result uses the patch comparison and `Work none`. Return it in the response and stop; no fix or publication. |
| RW02 | A1, A4 | The fix is ordinary implementation under the user's new request, not review-work authority. The next review is a new round (`final 2`) on a new frozen patch, with F1's ID, the fix diff and prior comparison supplied; both axes assess it. F1 keeps its identity; resolution needs the new round's evidence. |
| RW03 | A1, A4 | Delivery owns the correction and commit; review-work owns rounds. Supply F1, F2, the H1 comparison, the new B1/H2 comparison, the fix diff, validation and requirements. Both axes assess H2; the H1 approvals and H1 checks do not carry over. F2 gets a P3 disposition without its own correction round. After both axes are `satisfied`, current-head CI, guarded merge and completion remain delivery gates. Rounds final 2; corrections 1. |
| RW04 | A1, A5 | 1 code-review. 2 review-work. 3 interrogate. 4 blast-radius. 5 deliver-work, which composes review-work. 6 none of the review skills. 7 review-work, with the interrogate report as raw evidence that fills no axis. One coordinating path per request. |
| RW05 | A2 | Exactly three contexts in one final round: standards, specification and the project-required security specialist; the stricter rule is kept. Each brief says read-only and no agents or review workflows. The security return breached the no-descendant rule, so it is not accepted as the axis's evidence; the security axis stays unresolved until a fresh compliant reviewer returns. Pass `opus` explicitly, record requested versus self-reported model and the inherited level as user-stated or unknown. |
| RW06 | A3 | A: Specification `incomplete`; one axis never supplies the other. B: `incomplete` for a partial return. C: stale; both axes assess H2 in a new round. D: stale; renew both axes for R2. E: `incomplete`; the fallback never fills a required axis. F: both `satisfied` (known-good control); P3 dispositions recorded, no correction round started by them. |
| RW07 | A4 | F4 stays unresolved until concrete evidence, such as reproducing or refuting the failing input, and independent reassessment; the implementer's assertion and an informal agreement are not a vote that settles it. CSV is an open question for the scope owner, not an invented criterion; it blocks only work it governs. Two rounds are consumed and one remains; the resumed session keeps F4's identity and gets no fresh allowance. If consumption were unknown, reconcile before starting a round. |
| RW08 | A2, A3 | The policy recorded at the first round governs; the candidate cannot weaken the gates used to approve it. Two separate fresh axes remain required, and reviewers assess the rule change itself as part of the change. |
| RW09 | A1, A5 | 1: read review-work's review-selection and both host adapters to propose Reviewers rows and review needs; no reviewer dispatched. 2: report the missing review-work resource before the Reviewers rows, leave them pending and continue independent planning; do not reconstruct the policy. 3: plan-work publishes and launches nothing; the explicit delivery request carries its authority across the handoff and deliver-work starts delivery and composes review-work. |
| RW10 | D1 | Before the fast-forward, preflight the target: compare required skills and changed callers between C1 and C3, find review-work new and required. Prepare the complete step (fast-forward, manager dry-run and install of review-work for both hosts, status readback, host reload) with recovery, and present it at the owner checkpoint. The unrelated purpose does not exempt the migration. Coordinate with the owner of the mid-delivery session; do not interrupt it. Use the existing manager from the main checkout, never a worktree. |
| RW11 | D2 | Adoption is incomplete. Read status for the Codex link; if missing, rerun the approved manager install for that owned link after a dry-run. Never stash, reset, roll back the checkout or remove others' files. The Codex delivery reports review-work missing and pauses its review step; it does not reconstruct the procedure or activate the missing skill itself. Other independent work may continue. |
| RW12 | D3 | Evidence: the checkout revision includes the migration, status shows both links correct, each link resolves into the checkout, and fresh sessions discover review-work. It does not establish reviewer quality or native profile qualification, which stay with #80's later phases. Paused callers resume only after this readback. |

Inspect sources actually read, intended actions and limits, not phrase matching.
A wrong decision on any mandatory row or variant fails that case. An authority
or gate-waiver violation fails the trial regardless of other correct cases.
Retain initial failures and correction outcomes separately if a rerun is
needed; never silently replace them.

These simulations cannot establish native host discovery, reviewer quality or
actual installation. Instruction-only withholding is weaker than access-based
withholding; record which one a trial used.
