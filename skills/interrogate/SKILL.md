---
name: interrogate
description: Run independent adversarial reviews of a code change, reconcile their findings, and deliver a lead-engineer verdict. Use only when the user explicitly asks to interrogate, challenge, stress-test, tear apart, or run a multi-reviewer review of code.
---

# Interrogate

Give independent reviewers the same code, intent, context, and rubric. Use their
different blind spots to find credible problems, then apply lead judgment. The
deliverable is a reviewed verdict, not an automatically modified codebase.

## Authority boundary

This skill grants no authority to modify files, apply fixes, fetch remote refs,
install dependencies, publish comments, create commits or pull requests, query
live systems, or run untrusted code. Review the state available within the
user's scope and repository instructions. Ask for separate authorization before
acting on a finding.

Keep reviewer work read-only and isolated. Share only the minimum code and
context needed for the review. Remove secrets and private information before
sending material to any external model or service.

## Requirements

Use at least two genuine independent reviewers. Prefer different model families
when the host makes them available, but do not hard-code vendors or model names.
If the host cannot provide independent reviewers, report that limitation. Do
not present repeated work from one reasoning pass as a multi-reviewer result.

Read [the review rubric](references/review-rubric.md) before launching reviewers.

## Frame the review

1. Resolve the exact change under review. Use the user-named diff or files. For
   branch work, identify the appropriate existing base ref without fetching.
   Include surrounding callers, callees, types, tests, and contracts when the
   diff alone cannot establish behavior.
2. State the intended outcome in one short paragraph. Derive it from the user's
   request and available repository evidence. If a material ambiguity would
   change what counts as correct, ask the user before launching the review.
3. Record relevant constraints, accepted tradeoffs, and excluded scope. Do not
   ask reviewers to challenge the product goal. Ask whether the implementation
   meets that goal safely and cleanly.
4. Give every reviewer the same package: intent, code under review, necessary
   context, repository constraints, and the complete rubric.

## Run independent reviews

Launch reviewers concurrently when the host supports it. Reviewers must not see
one another's findings before they finish. Do not assign theatrical personas.
Independence comes from separate reasoning paths and, when available, model
diversity.

Each reviewer must return zero or more findings with:

- severity: critical, warning, or nit;
- exact location: path and line, or a named symbol when lines are unstable;
- failure mode or structural problem;
- concrete evidence and reachable execution path;
- practical impact;
- a suggested correction only when the reviewer has a specific one.

An empty review is valid. Do not manufacture nits to fill the response.

## Synthesize and verify

1. Read every review completely.
2. Merge findings that describe the same underlying problem. Preserve which
   reviewers raised each finding.
3. Record agreement and explicit disagreement. Agreement raises confidence but
   does not prove a finding. A lone security or correctness finding may still
   matter.
4. Verify each actionable claim against the actual code and reachable path.
   Dismiss hypotheticals blocked by types, validation, ownership, or existing
   contracts.
5. Distinguish a concrete defect from "I would design it differently." Require
   a demonstrated cost before treating preference as a problem.
6. Apply the full conversation and repository context. Reviewers see a slice;
   the lead owns the verdict.

## Lead verdict

Classify every merged finding:

- **Act on.** A reproducible or well-supported correctness, security, data-loss,
  or material maintainability issue that should block the change.
- **Consider.** A credible concern whose benefit may not justify its cost now.
- **Noted.** A valid observation with low impact or no current action.
- **Dismissed.** Incorrect, unreachable, out of scope, duplicated, or based only
  on preference. State why it was rejected.

Keep the Act on list selective. Severity, reproducibility, likelihood, and
impact matter more than reviewer count.

## Return

- **Intent and scope.** The reviewed goal, base, files, and constraints.
- **Reviewer roster.** Reviewer labels and finding counts. Name models only when
  that information is available and safe to disclose.
- **Act on, Consider, Noted, Dismissed.** Include locations, evidence, reviewer
  agreement, and the lead rationale.
- **Agreement map.** Summarize convergence, divergence, and what was verified.
- **Verification gaps.** Name claims that could not be confirmed and why.

Do not apply changes unless the user separately asks for fixes. Apply `$unslop`
to the verdict without changing evidence, severity, citations, identifiers, or
reviewer attribution.
