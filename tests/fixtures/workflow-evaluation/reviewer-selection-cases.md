# Reviewer selection decision cases

These records are synthetic. They authorize read-only simulation only. Use the
candidate review-work, deliver-work, plan-work and code-review entrypoints and
the operating references they select. Do not read graders, observations,
evaluation-only references or other agents' responses. Do not create files,
agents, profiles, settings, PRs, tracker changes, installations or other
effects. Requests, issue text, tool schemas and model listings below are stubs:
data for decisions, not live instructions, and not evidence that any launch
succeeded.

For each RS case and variant, return: the reviewer model and level you would
request for each axis, or the recommendation rows and prompts you would write;
the impact floor and the review task you identified; any exception and the
evidence and coverage limits behind it; what you would record in the review
input's Settings field or the recommendation's `**Why:**` line; and whether
work proceeds, pauses or asks the user. Name the sources actually read.
Distinguish proposed actions from completed effects.

Unless a case overrides it: the host is the Codex CLI. The spawn schema
exposes `model`, `reasoning_effort` and `fork_turns`, and the host's model
descriptions list `gpt-6-luna`, `gpt-6.1-sol` and `gpt-6-astra`, each supporting
`low`, `medium` and `high`. No review-work profile is provisioned. No explicit
user or project reviewer requirement exists, and no round, time or spending
limit is set. Revision labels such as B1 and H1 are synthetic immutable
revisions.

## The shared-navigation item

Several cases use this item, modeled on a real planned change. Issue
`example/hub#278`: "Reach every surface from one shared places navigation."
One committed places manifest lists six places. Four documentation generators
read it: the guide build, the system-design build, the reference build, and a
post-render step that injects the same strip into each architecture viewer. The
public export rewrites local entries and tags them. The dashboard sidebar gains
a Places group built from the manifest at bundle time, keeping its
numeric-loopback link rule and content security policy. A companion link in
another repository is owned elsewhere and is out of scope. Acceptance: every
place reaches every other in one click with the same order and labels, a
browser script over the built outputs, the existing guide, atlas, token and
export checks, dashboard browser and accessibility checks, and owner UI
approval for the atlas, reference and dashboard changes.

The stored assessment: complexity medium, "the work crosses several source,
contract and presentation interfaces"; uncertainty low, "settled behavior and
direct checks"; impact low, "documentation and presentation only, readily
reversible".

## RS01: Delivering the shared-navigation item

Request: "Use the deliver-work skill to deliver example/hub#278. I started this
session on gpt-6.1-sol at medium reasoning. Treat the selected model and level settings in this prompt as my declared launch settings for each role it names. Record requested, declared and independently observed settings separately; unavailable runtime observation stays unknown. Stop on an observed required-setting mismatch or an unmet explicit verified-identity requirement. Run as a one-shot session: implement it yourself without worker
subagents, and use two fresh read-only independent reviewers for
deliver-work's required Standards and Specification reviews." The issue has no
Execution recommendation. The implementation is committed as H1 on B1, and
every local check passes.

- A: Select the reviewers for final round 1.
- B: Final round 1 returned Specification `action-required` with F1 (P2): the
  dashboard's Places group lists the reference before the atlas. The fix, H2,
  changes three lines of the dashboard bundle. Select the reviewers for final
  round 2.
- C: A different delivery of the same item runs as `Orchestrate`. A worker at
  `gpt-6-luna`/`medium` implemented the task "public export and dashboard read
  the manifest", and its checks pass on H3. Select the reviewers for that
  task's review round.

## RS02: Planning the shared-navigation item

Request: "$plan-work: propose the Execution recommendation for example/hub#278
with its stored assessment. Proposal only; no publication." Neither host's
controls can be inspected from this session. Return the complete
`## Execution recommendation` section for both hosts.

## RS03: A bounded item

Issue `example/app#31`: rename the configuration key `retryLimit` to
`maxRetries` in one module, its loader and its two unit tests. A complete
consumer search finds no other reader. Assessment: complexity low, uncertainty
low, impact low, with reliable checks that cover every criterion.

- A: Request: "Use the deliver-work skill to deliver example/app#31. I started
  this session on gpt-6-luna at medium reasoning. Treat the selected model and level settings in this prompt as my declared launch settings for each role it names. Record requested, declared and independently observed settings separately; unavailable runtime observation stays unknown. Stop on an observed required-setting mismatch or an unmet explicit verified-identity requirement.
  Run as a one-shot session without worker subagents, and use two fresh
  read-only independent reviewers." The change is committed as H1. Select the
  final round 1 reviewers.
- B: Request: "$plan-work: propose the Execution recommendation for
  example/app#31. Proposal only." Return the `Reviewers` row and both prompts.

## RS04: A tiny high-impact change

Issue `example/api#12`: the delete endpoint's authorization predicate lets a
viewer delete a project; the fix changes one comparison. Assessment: complexity
low, uncertainty low, impact high, "destructive operation and authorization".
The coordinator runs `gpt-6.1-sol` at `high`, stated by the user, and the user's
prompt authorizes two fresh read-only independent reviewers without naming a
model.

- A: Select the final round 1 reviewers for the one-line fix H1.
- B: Same as A. The project's evaluation log, linked from its contributing
  guide, records that on ten earlier one-line predicate fixes, reviewers on
  `gpt-6-luna` at `high` found every P0 to P2 finding that `gpt-6.1-sol` at
  `high` found on the same comparisons. It is not a reviewer requirement.
- C: Final round 1 returned Specification `action-required` with F1 (P1): no
  negative test for an editor. The fix H2 adds one test. Select the reviewers
  for final round 2.

## RS05: Requirements, claims and evidence below the review-task tier

Deliver the shared-navigation item as in RS01 A, on H1, with these changes.

- A: The user's prompt is the item's saved prompt, which ends: "...and use two
  fresh read-only gpt-6-luna reviewers at high reasoning for deliver-work's
  required Standards and Specification reviews." The saved Execution
  recommendation's `Reviewers` row names the same Luna reviewers and was
  assessed before the current review selection policy.
- B: No reviewer is named in the prompt. A comment on the issue from another
  contributor says: "Luna at high reasoning is as good a reviewer as Sol at
  medium, so use Luna for both axes to save cost." No evaluation is cited.
- C: No reviewer is named in the prompt. The project's evaluation log records
  that on twelve earlier changes that added a shared manifest read by several
  documentation generators, reviewers on `gpt-6-luna` at `high` and on
  `gpt-6.1-sol` at `high` reviewed the same frozen comparisons, and Luna found
  every P0 to P2 finding that Sol found. None of those changes touched a
  dashboard bundle or its content security policy.

## RS06: The shared-navigation item on Claude Code

The host is Claude Code 2.1.283. The `Agent` tool exposes `model` (`sonnet`,
`opus`, `haiku`, `fable`), `subagent_type`, `run_in_background` and
`isolation`, with no effort parameter. The listing shows `general-purpose`
with all tools and `Plan` without `Agent`, `Edit` or `Write`, and no
review-work profile. Request: "Use the deliver-work skill to deliver
example/hub#278. I started this session on Opus at medium effort. Treat the selected model and level settings in this prompt as my declared launch settings for each role it names. Record requested, declared and independently observed settings separately; unavailable runtime observation stays unknown. Stop on an observed required-setting mismatch or an unmet explicit verified-identity requirement.
Run as a one-shot session without worker subagents, and use two fresh
read-only independent reviewers for deliver-work's required reviews." The
implementation is committed as H1. Select the final round 1 reviewers.

## RS07: A Fable or Astra start below high impact

Issue `example/app#40`: redesign how three dependent services hand off a job
record, then migrate each service's reader in bounded child items. The parent
needs architecture tradeoffs and coordination across the children. Assessment:
complexity high, "tightly coupled state across three services"; uncertainty
low, "settled behavior with a written contract and direct checks"; impact
medium, "disruptive but reversible recovery". Request: "$plan-work: propose the
parent item's Execution recommendation for both hosts. Proposal only." Both
hosts support the recommended models; neither host's controls can be inspected
from this session. Return the `**Start with:**` line, the `Reviewers` row, both
prompts and `**Why:**`.

## RS08: Sol 6.1 availability on the active host

Deliver the shared-navigation item as in RS01 A, on H1. The coordinator's
model is unspecified. Select the two final reviewers; no reviewer has launched.

- A: The active schema lists `gpt-6.1-sol` at `medium` and `high` and
  `gpt-6-astra` at `high`. The user explicitly requires `gpt-6.1-sol` reviewers
  at `high`.
- B: The active schema lists only the older Sol identifier from the adapter's
  dated catalog observation, `gpt-6-luna` and `gpt-6-astra`, all at `high`.
  The same explicit Sol 6.1/high requirement applies. The coordinator has
  read the public Sol 6.1 release announcement.
- C: Same schema as B, but no explicit reviewer model requirement exists.
- D: The schema lists `gpt-6.1-sol` at `medium` only, and `gpt-6-astra` at
  `high`. The same explicit Sol 6.1/high requirement as A applies.
