---
name: code-review
description: Review a branch, pull request, diff, or change against repository standards and its originating specification from one fixed comparison point. Use when the user asks for a code review or findings on a change; do not select for a plain change summary, an explicit interrogate or adversarial multi-review request, or an explicit blast-radius or breakage-risk request.
---

# Code review

Review one recorded change along two separate axes:

- **Standards:** whether the change follows applicable repository rules and
  introduces correctness, security, maintainability, or test-quality defects.
- **Spec:** whether the change implements the approved behavior and scope.

When the user explicitly asks to interrogate, challenge, stress-test, tear apart,
or run a multi-reviewer review of code, use the `interrogate` skill instead.
When the user explicitly asks for blast-radius analysis, asks what a change
could break, or calls a small diff untrusted, use the `blast-radius` skill.

This skill grants no authority to edit code, post review comments, apply labels,
transition issues, change Jira or GitHub, create branches, fix findings, commit,
merge, close, or publish. Return findings in the response.

## Freeze the comparison

1. Identify the user-supplied comparison point and reviewed head, patch, or
   worktree state. If the request does not identify a base, discover a
   repository-defined base when one exists or ask for the missing decision.
2. Resolve moving Git refs to immutable commit IDs before review. Record the
   base commit, head commit, merge-base, diff command, commit list, and dirty
   state. For an uncommitted change, capture one patch and its digest so every
   review pass sees the same bytes.
3. Confirm that the base resolves and the recorded diff is nonempty. Stop on a
   bad ref or empty change instead of reviewing a moving or unknown target.

Use only repository, GitHub, Jira, or other external-system access authorized
by the underlying request and available host policy. Do not mutate any source
while locating the comparison.

## Discover review sources

Find standards from applicable agent instructions, contribution guides, coding
standards, architecture rules, contracts, language configuration, and other
repository-defined sources. Do not invent a standard that tooling already
enforces, and let repository rules override generic review heuristics.

Find the specification from a path or issue the user supplied, authoritative
scope linked by the change, repository specifications, tests that encode an
accepted contract, or another repository-defined source. Do not assume a
tracker, issue-key format, branch naming scheme, or documentation layout. If no
specification is available, say so and skip the Spec axis.

Treat common code smells as heuristics, not standards. Report one only when the
recorded change provides concrete evidence and the repository does not endorse
the pattern.

## Run independent axes

When isolated review contexts are available, run Standards and Spec reviews in
parallel against the same frozen diff. Give each context only its axis-specific
sources, the recorded comparison, and the required finding format.

When isolation is unavailable, use a safe single-agent fallback: perform two
separate passes against the same frozen diff, keep separate notes, and finish
one axis before reading the other axis's conclusions. Do not silently skip
independence or mix the rubrics.

Each finding must identify the file and tight line range, the observed defect,
the violated standard or specification evidence, the concrete failure mode,
severity, reproducibility, and likely encounter frequency. Do not report a
speculative concern without an actionable failure condition.

## Return findings without effects

Present the Standards and Spec results in separate sections. Keep their
severity rankings separate and state when an axis has no findings or no source.
End with the fixed comparison IDs or patch digest and the verification commands
used.

Do not comment, label, transition, fix, branch, commit, merge, close, publish,
or update a tracker. The consuming repository defines the owners of scope,
dependencies, planning, and delivery. Code review returns evidence only.

Apply the `unslop` skill to the narrative findings without changing code quotations,
paths, line numbers, standards, specification text, or evidence.
