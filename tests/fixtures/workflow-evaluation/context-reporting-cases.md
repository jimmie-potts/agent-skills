# Matched loading and reporting cases

Synthetic read-only evaluation. Case requests authorize no live agents, edits,
checks, tracker operations or other effects. Read the named workflow entrypoint
and only operating references required by each branch. Do not read any
validation-scenarios, graders, rubrics, observations, evaluation-results or other
trial returns, even when an entrypoint links them. Evaluate both Codex and Claude
variants. Their capabilities below are supplied simulation facts, not discovery
or runtime identity evidence about this evaluator.

For each case/host, actually inspect the selected instructions and account for
all instructions used, including previously read material. Do not count an
unread link as a read, recursively load unrelated references, or omit an earlier
read that informed this case. A source file read in parts counts as one complete
file, once per context within that case. List coordinator and worker/reviewer
reads separately; worker reads are proposed requirements, not actual child reads.
The coordinator/evaluator reads must be distinguished from those proposals.

Use this JSON return shape. Return all ten case/host records. Keep substantive
decisions and messages complete; do not pad or optimize for an assumed score.

```json
{
  "cases": [{
    "id": "L1", "host": "codex",
    "reads": ["skills/deliver-work/SKILL.md"],
    "worker_reads": [],
    "selected": "selected role/model/effort, with unknowns",
    "decision": "concrete decision and applicable limits",
    "brief": "exact dispatched text, or empty string when no dispatch",
    "return": "exact proposed labeled worker return, or empty string",
    "updates": [{"event": "checkpoint", "text": "exact user-facing text"}]
  }],
  "sources": ["all actual source paths read"],
  "validation": "actual read-only commands and checked revision",
  "settings": "requested versus exposed evaluator settings",
  "limitations": "unobserved behavior and exclusions"
}
```

Only `brief`, `return`, and `updates[].text` are dispatched/returned text samples.
Empty means no such message is needed; explain that decision in `decision`.
These are actual evaluator-authored samples for supplied facts, not actual worker
execution. Do not claim to run a check or obtain advice. Use repository-relative
paths. If an installed source is read through an alias, identify its canonical
catalog counterpart only when its bytes match. Describe external sources
separately so their exclusion from catalog counts stays visible.

## Shared records

The simulated repository uses accepted issue text as its specification, no
OpenSpec or guide-publication system, root-only writes, and two independent final
review axes plus `check` and PR CI before normal guarded merge. Work is isolated
at base B1/head H1 on branch `work/7`, issue `example/repo#7`, no PR yet unless
stated. Inputs and authority are settled. No deployment or human gate applies.
No round/time/spend cap exists. Requested settings, runtime self-reports and
independent host observations are distinct. Usage is unavailable throughout.

Codex exposes the catalog adapter's currently documented collaboration controls,
models and effort values, including fresh contexts, same-worker continuation and
stopping. Claude exposes `Agent(model=...)` and same-worker `SendMessage`, with
no per-call effort control. Neither exposes attributable spend. Host model
availability never establishes coordinator or worker identity.

## L1: Direct delivery through local implementation

User explicitly invokes deliver-work to correct one supplied typo in a public
guide. Scope/behavior and spelling are settled. All assessment dimensions are
low. Root implements directly. No decomposition, worker or advisory pairing is
needed. Stop this scenario at the local implementation checkpoint, before
reviewer selection or PR supervision. Actual fixture facts supplied for the
checkpoint: the corrected guide and `check` passed at H1; final independent
reviews, publication, CI and merge remain pending. Coordinator identity/effort
are unknown. Return the checkpoint and the required reads, with no worker brief.

## L2: Planning with one bounded investigation

User invokes plan-work for a response-only proposal. A read-only investigation
must determine whether `parseRecord` rejects negative lengths at source H1.
Its outcome is an exact source-based answer with path/line evidence; no product
decision or implementation is needed. Complexity/uncertainty/impact are medium.
Use one assigned investigation worker, without advisory pairing. No evidence
requires a stronger model than the current host default. Supply its exact brief
and required reads, then a labeled return using these fixture facts: source
`parser.py:12` rejects negative lengths; no tests ran, no artifact/file changed,
runtime identity/effort and usage unexposed. No publication authority exists.
Do not start delivery, create an issue or implement the eventual work item.

## L3: Assigned implementation and reporting events

User invokes full delivery for a bounded retry fix with medium ratings. Outcome:
`send` retries transient failures twice at most and never retries permanent
failures. Scope is `retry.py` and its tests at H1; checks are `check retry` and
the required whole-change gates. Root applies all patches. Use one ordinary
assigned worker, with the current host default and no advisor loop. Give the
initial brief and a labeled return: proposed patch, `retry.py` and its test,
`check retry` passed on the proposed artifact, no full check run, unexposed
runtime identity/effort. Preserve proposed versus applied evidence.

Produce the appropriate user-facing message at each event, in order. These are
distinct times; retain earlier history in later checkpoints:

- E0: initial strategy checkpoint. Root plus one confirmed active worker W1;
  two final reviewers are planned. No corrections, promotions or consultations.
- E1: routine update. W1 located the permanent-failure predicate; no strategy,
  settings, team or authority changed. Next action is the bounded patch.
- E2: routine update. W1 added the permanent-failure case; validation is next.
  No other state changed.
- E3: a completed attempt fails the permanent-error criterion. Diagnose a sound
  approach with insufficient reasoning. On Codex, one same-worker guided
  correction at unchanged settings also fails; no effort increase was used.
  On Claude, this is the first completed capability-failed bounded attempt.
  The old assignment is confirmed stopped, and a fresh worker W2 has been
  established with the next configuration selected by the current adapter.
  Report the changed strategy/settings/team and retain failures. Execution
  identity/effort are still unexposed; no advisory loop is added.
- E4: routine update. W2's proposed permanent-error fix passes its focused check;
  root must inspect and apply it. No other state changed.
- E5: final delivery handoff. Root accepted and applied H2, all checks and two
  final fresh review axes passed, and a guarded merge produced M1. Main CI and
  completed issue closure were read back. W1, W2 and both reviewers are finished.
  No more agents are planned. Account for every known agent and earlier failure.

Also give concrete decisions in `decision` for these independent variants:
same-worker W1 resume; an ambiguous spawn without a creation readback; an
explicit user-requested model/effort that the host rejects; and a native profile
whose resolved settings conflict with that explicit requirement. Do not invent
capability, install settings, or silently substitute another configuration.

## L4: Advisory pairing with an accepted configuration

The delivery coordinator has already selected Terra/medium on Codex or Sonnet
on Claude for a medium-rated parser repair whose two design checkpoints benefit
from advice. Required scope is `parser.py`, accepted cases include malformed and
valid records, checks are `check parser` then `check`. Root writes; worker returns
proposals. Current source is H1 and the original advisor address is A0.

Host runtime evidence verifies the original coordinator as Astra on Codex and
Fable on Claude. Model selection and the appropriate communication/resumption
controls are supported. Claude's effective session effort is unknown. This case
begins after strategy selection; account only for instructions needed to establish
and operate this accepted pairing, including any references those instructions
still require. Supply the worker brief, required worker reads, and a labeled
blocked return: the approach consultation completed once, a blocker consultation
asks whether a malformed record must retain an audit event, no answer yet, no
final consultation occurred, and no check ran. User owns that product decision.
Independent useful read-only work exists. Return the blocker update without
treating advisor advice as authority or final independent review.

## L5: Independent review selection and brief

Implementation at H1 is ready for final review of a one-line authorization fix
on a destructive endpoint. Complexity is low, uncertainty low, impact high.
Frozen comparison is B1/H1 with merge-base B1, clean worktree and `git diff B1 H1`.
Scope requires the owner role, denies all other roles and fails closed on missing
identity. Actual fixture evidence: negative/positive checks and `check` passed;
hosted current-head CI is pending. Select and brief the independent Specification
reviewer using the applicable current risk floor. A separate independent Standards
context is also mandatory. Coordinator and implementer are not either reviewer.
No pairing, implementation promotion or worker replacement is being selected.
Return a proposed reviewer report for the supplied facts only: coverage of those
three cases is evidenced, actual source inspection has not occurred, and a final
verdict therefore remains pending. Keep it independent of implementer/advisor
approval narratives and do not merge on that proposed report.
