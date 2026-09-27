# Select and brief independent reviewers

Read before selecting task, fix-verification or final reviewers. Then read only
the active host's adapter: [Claude Code](claude-code-reviewers.md) when the host
exposes an `Agent` tool with a per-call `model` parameter, or
[Codex](codex-reviewers.md) when collaboration tools expose model and reasoning
overrides. Implementation settings and worker retry thresholds do not select
reviewers.

## Establish the available choices

Honor explicit user and project reviewer requirements first, including models,
reasoning levels, specialist axes and limits. Discover current model
availability, supported reasoning levels and delegation controls from the host;
do not infer capability from names or assume every model supports every level.
Never silently substitute an explicitly required reviewer: when it is
unavailable, the affected axis is `incomplete`. Missing optional controls
preserve host defaults with the gap disclosed.

Optional native reviewer profiles are adapters only. Verify the resolved model,
effort, permissions and available tools before use; a profile cannot override
these floors or explicit requirements. Do not create or install profiles or
change personal settings to obtain a selection.

## Start from impact

Use the host adapter's routine reviewers for low and medium impact, and the
strongest evidenced relevant reviewers at high reasoning for high impact, even
with a tiny diff. Unknown impact takes the high-impact floor. These floors
apply to task and fix-verification reviewers too; a small fix does not
establish low impact. Complexity and
uncertainty may raise this floor. Inspect interactions, concurrency, invariants
and recovery for interacting-state work; examine assumptions, omissions and
conflicting evidence when uncertainty is high. Specification review covers
each criterion, exclusions and negative cases, including high-impact
acceptance. Default, moderate and high are relative recommendations, not
portable API enum names; map them to supported controls and record the mapping.
Maximum reasoning is not automatic. Both axes may use the same model in
separate fresh contexts.

## Brief each reviewer

Compose `code-review` in its assigned-axis mode for each context. Supply the
axis rubric, the frozen comparison, the raw axis-specific requirements or
standards sources, the relevant code and consumers, and the validation facts.
Reviewers may inspect implementation facts and validation outputs. Do not give
initial reviewers implementer or advisor approval narratives, other reviewers'
conclusions or instructions to confirm a preferred verdict. Tell each reviewer
it is read-only, launches no agents and loads no review workflow of its own. A
return that exceeded its brief, for example by delegating, is a failed return:
its axis stays `incomplete` until a fresh compliant reviewer returns.

Ask each reviewer to list first the problems it would block the merge for (P0
to P2 and project-defined blockers), each with the file and line, why it is
wrong and how to show it fails, and to keep non-blocking P3 observations in a
separate short list. Each reviewer states its coverage and evidence limits.
Findings need concrete failure conditions and source evidence.

## Cover the change and its tests

Account for every changed area, including tests, configuration, CI and relevant
surrounding behavior. Add a focused security, concurrency, migration,
performance, accessibility or other specialist reviewer when the assessment
identifies an uncovered risk. Require qualified human acceptance where policy
or an unresolved automated-evidence gap calls for it; do not invent routine
approval gates.

Check each criterion's actual evidence. Inspect removed or weakened assertions,
skipped tests, fixture and mocking changes, and CI changes. Ask whether checks
reject incorrect implementations; preserve observed pre-fix failure where
applicable. Use relevant adjacent regression, integration, consumer-contract,
end-to-end and failure or recovery checks. Targeted property or mutation checks
can help when justified; do not require every technique everywhere.

Before changes to tests, CI or workflow instructions, retain the agreed baseline
gates and inspect removals against the original acceptance and policy.
Enumerating only a reduced candidate job list cannot waive baseline obligations.
Use existing technical protections; do not change repository or account settings
without authority.
