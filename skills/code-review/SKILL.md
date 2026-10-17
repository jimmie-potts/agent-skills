---
name: code-review
description: Review a branch, pull request, diff, or change against repository standards and its originating specification from one fixed comparison point. Use when the user asks for a code review or findings on a change; do not select for a plain change summary, an explicit review-work request, an explicit interrogate or adversarial multi-review request, or an explicit blast-radius or breakage-risk request.
---

# Code review

The companion skills `blast-radius`, `interrogate`, `unslop` named here come from the installed pstack plugin and run with upstream behavior.

Review one fixed change on two separate axes:

- **Standards:** repository rules, plus correctness, security, maintainability
  and test-quality defects.
- **Spec:** whether the change implements the approved behavior and scope.

Route elsewhere when asked: `review-work` for an explicit review-work request,
`interrogate` for an adversarial or multi-reviewer review, and `blast-radius`
for what a change could break.

## Standalone review

1. Resolve the base and head to commit IDs (or capture one patch and its
   digest) and stop on a bad ref or empty diff.
2. Take standards from the repository's instructions and config; don't restate
   what tooling already enforces. Take the spec from the linked issue, path or
   tests; with no spec, say so and skip the Spec axis.
3. Review each axis separately, in isolated contexts when available. A
   single-agent two-pass review is fine standalone but never satisfies a
   review-work axis.

Each finding gives the file and line range, the defect, the violated standard
or spec, the failure mode and its severity. Skip concerns with no concrete
failure condition.

## Review an assigned axis

When `review-work` or another coordinating workflow assigns this context one
axis of a frozen comparison, review only that axis:

- Use the supplied comparison. Verify that its commit IDs or patch digest
  resolve and match; report a mismatch or unreadable input as incomplete
  instead of freezing a different target.
- Use the supplied requirements or standards sources for the axis. Report a
  missing source as incomplete rather than substituting another.
- Launch no subagents and load no coordinating review workflow such as
  `review-work` or `interrogate`; the coordinator already owns
  independence, rounds and the result.
- Return findings in the assigned format, P0 to P2 blockers first and P3
  observations separately, with the coverage and evidence limits of the review.

## Return findings

Report Standards and Spec in separate sections with separate severities, then
the comparison IDs or patch digest and the verification commands used. Review
returns findings only; do not edit, comment, label, commit or merge unless the
request explicitly authorizes it. Use `unslop` on the
narrative without changing quotations, paths or evidence.
