# Select and brief independent reviewers

Read before selecting task, fix-verification or final reviewers. Then read only
the active host's adapter: [Claude Code](claude-code-reviewers.md) when the host
exposes an `Agent` tool with a per-call `model` parameter, or
[Codex](codex-reviewers.md) for collaboration tools, or
[Grok Bot](grok-reviewers.md) for Task executors. Select for the review needs,
not the implementer's settings or attempt history.

## Choose reviewers for the work

Honor explicit user and project requirements, including independent axes,
specialist coverage, tool restrictions and limits. Select reviewers able to
assess the changed behavior, interfaces, uncertainty and consequences of failure.
Risk determines what must be inspected and demonstrated; it does not prescribe
a model or thinking level. Host defaults are acceptable when suitable.

Use current host capabilities and relevant outcome evidence. Neither the
implementer's model nor an assessment rating automatically selects reviewers.
Explain a consequential selection or fallback briefly in the input's Settings
field. Do not infer equal capability from equal effort names across providers.

Before launch, apply [reviewer execution](reviewer-execution.md) for fresh
contexts, read-only conduct, no descendants and any mandatory host restrictions.
Read only the active host adapter. Missing optional settings or runtime telemetry
do not block review. An unavailable explicit requirement leaves its axis
`incomplete`; do not silently substitute or install profiles to satisfy it.

Apply this to task, fix-verification and final reviewers. Selection changes no
reviewer count, frozen comparison, scope, or specialist or human gate. Both
required axes may use the same model in separate fresh contexts.

Use [cross-provider routing](cross-provider.md) only when deliberately choosing
another provider or when explicitly required. Consider it for an unresolved
coverage gap or substantive disagreement; it is not a routine extra team or a
requirement inferred from high impact. Resolve findings on evidence, not votes.

## Brief each reviewer

Compose `code-review` in its assigned-axis mode for each context. Supply the
axis rubric, the frozen comparison, the raw axis-specific requirements or
standards sources, the relevant code and consumers, and the validation facts.
Reviewers may inspect implementation facts and validation outputs. Do not give
initial reviewers implementer or advisor approval narratives, other reviewers'
conclusions or instructions to confirm a preferred verdict. Tell each reviewer
it is read-only, launches no agents and loads no coordinating review workflow
such as `review-work` or `interrogate`. A
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
