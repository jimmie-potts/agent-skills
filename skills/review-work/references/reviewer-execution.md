# Preflight and record reviewer execution

Read before launching, replacing or resuming a reviewer, and when a return is
partial, cancelled or cannot be attributed. [Review selection](review-selection.md)
chooses the settings; this reference checks that the active host can apply
them and records what actually ran. The active host's adapter,
[Claude Code](claude-code-reviewers.md) or [Codex](codex-reviewers.md), names
that host's controls, precedence and evidence sources.

## Keep the evidence classes apart

For each reviewer, keep these classes apart for the model, reasoning level,
thinking, context, tools and profile:

- Requested: what the coordinator passed or the selected profile configures.
- Supported: what the current host's tool schema, agent listing or profile
  readback shows it can express. Documentation alone is `documented,
  unverified` until the active host shows the control.
- Observed: what the host reports, such as returned runtime metadata, a task
  row, a substitution warning or an agent listing, and a user-stated setting.
- Self-reported: what the reviewer states from its own runtime instructions.
  Never ask a reviewer for its effort.
- Unknown: everything else. Never fill it from the request.

The result's reviewer entry carries the requested and sourced model and level.
Record the preflight and the other controls in the input's Settings field and
the result's coverage, each with its class. A successful launch proves the
request was accepted, not the executing settings.

## Classify each control

A control is mandatory when the user, the project or review-work's boundaries
require it. The boundaries require a fresh context, read-only conduct and no
descendant agents. A model, level, profile or enforced restriction is mandatory
only when an explicit requirement names it. When a mandatory control is
unsupported, unverifiable or contradicted, do not launch or simulate that
reviewer: the affected axis is `incomplete`, with the gap named. An unsupported
optional control keeps the host's default, is disclosed as a limit and creates
no new gate.

[Review selection](review-selection.md)'s impact floors, review-task tiers
and explicit requirements govern every choice below. Never choose a profile, definition or
launch path whose resolved model or level falls below the selected reviewer
setting; choose another path that meets it. When no available path meets an
explicit requirement, the axis is `incomplete`. When the host itself lowers a
setting the coordinator cannot control, such as an inherited level or a
substitution, record a known mismatch; it leaves the axis `incomplete` only
under an explicit requirement for that setting.

## Preflight before launch

Run the preflight before the first reviewer of each round, and again after any
host, session, profile or settings change. Answer from the active host's
schema, listings and adapter, never from another host or surface:

1. Capability: the launch tool exists and exposes each selected control.
2. Model resolution: the host's order for per-call values, profile fields,
   environment defaults and the parent's model, plus any forced override,
   allowlist substitution or fallback chain that can change the result.
3. Configuration precedence: which definition resolves for the profile name,
   whether a higher-priority definition shadows it, and whether profile fields
   or the parent's live overrides beat the values passed on the call.
4. Tools: no editing, publishing, tracker or agent-spawning tools, and no
   coordinating review workflow. Use a narrower profile when one resolves.
   Record each part of the restriction, file writes, publication and
   descendants, as enforced only when host evidence shows it for this reviewer,
   such as its exposed tools or an applied sandbox; record every other part as
   instruction-only. A configured setting whose effect is unverified is not
   enforcement.
5. Filesystem: the reviewer can read the frozen source. Record any write access
   it keeps, such as a shell.
6. Credentials: connectors, MCP servers, host CLIs and environment the reviewer
   inherits. Record any exposure the tool set cannot remove.
7. Concurrency: enough slots for every axis in the round. A refused launch is
   not a return.
8. Cancellation: how the coordinator stops a reviewer and how the host reports
   a stopped run.
9. Result delivery: foreground return or background notification, the host's
   partial-output markers, how a wait timeout differs from a return, how to
   resume the same reviewer and how to reconcile reviewers after a restart,
   from the active host's adapter. Without a documented partial marker, a
   return missing its findings list or coverage is partial.
10. Source snapshot: the reviewer reads the frozen commits by ID, or a checkout
    verified at the frozen head, clean, with no writer during the round. A
    captured patch has its recorded digest. Isolation that starts from another
    base, such as a new worktree from the default branch, is not the frozen
    source.

After each return, verify that the reviewed source, its head and its dirty
state are unchanged. An unexpected change is a failed return and a finding for
the caller.

## Detect substitution and stale definitions

- Substituted model: the host warns or reports a model other than the request,
  including an allowlist or fallback switch. Record both values. Under an
  explicit model requirement the axis is `incomplete`. A family alias that the
  host documents as resolving to the parent's exact model is host resolution,
  recorded as such, not substitution.
- Conflicting precedence: a profile field or a parent override beats a value
  the coordinator passed. Record the effective value only when a readback shows
  it; otherwise the executing value is unknown. Do not use a profile whose
  fields would beat the selected model or level. When a conflict contradicts a
  mandatory setting, the axis is `incomplete`.
- Missing definition: the named profile does not resolve in this host. Proceed
  without it when it was optional, disclosing the limit; otherwise the axis is
  `incomplete`. Never create one.
- Stale or modified definition: its governing fields differ from this skill's
  template at the policy revision under review. The governing fields are the
  tools, skills, effort, model, sandbox, agent and permission settings. Treat
  it as a different profile. Use it only when it still meets every mandatory
  control and the selected model and level, and record the difference.

## Keep context and restriction separate

A fresh context and restricted execution are separate requirements, each with
its own evidence. A fresh context starts from the brief alone: never a
full-history fork, the coordinator, an implementer or an advisor. Restriction
comes from the tool pool, sandbox or permission controls the host enforces;
without them it rests on the brief alone.

Every brief still says read-only, no agents and no coordinating review
workflow, whatever the profile. A return that reports delegation, or a host
listing that shows descendants, is a failed return. Initial and replacement
briefs exclude implementer and advisor narratives and other reviewers'
verdicts, as [review cycles](review-cycles.md) requires.

## Handle partial, cancelled and unattributed returns

A partial or cut-off return, a stop at a turn limit, a cancellation, a run
timeout, a failed run or a lost session leaves the axis `incomplete` for that
round. So does a return you cannot attribute to its launched reviewer, its label
and the frozen comparison. Retain the round, its findings and the failure in the
history. A failed return has not assessed the axis, so its findings do not make
the axis `action-required`. List and count them as unresolved. Replace the
reviewer with a fresh compliant one in the same round; never resume a failed
one. After the replacement's independent initial return, send it the retained
findings in a follow-up within that round. Its reply must restate the axis's
complete verdict, its coverage and every finding with its disposition and
evidence; that reply is its final message, retained as its return, and a reply
missing any of them is `partial`. When the host cannot continue the
replacement, the axis stays `incomplete` and the retained findings carry to the
next round as prior findings. Replace a reviewer the user stopped only with the
user's agreement; until then its axis stays `incomplete`.

Retain a cancelled or user-stopped reviewer's return as `partial` when usable
text came back, otherwise as `failed` with `[no return: cancelled]`. An
unattributed message belongs to no `Reviewers` entry and gets no return block.
A wait that times out is not a return. A returned identifier or successful
spawn is not review evidence.

## Discover provisioned profiles

This skill ships profile templates in `assets/` and installs nothing. The
following is a contract for the environment that owns the host configuration,
not a procedure this skill runs. That environment discovers the canonical
durable checkout through its managed links, never a disposable worktree;
installs each template under its stable name without changing the governing
fields; gives any local variant a different name; reloads or restarts the host
as the host requires; and reads back the resolved definition. Removal touches
only the links or files it owns.

Review-work only discovers profiles. It checks whether the name resolves in the
active host, reads the effective fields where the host exposes them and
compares them with the template. It never creates, edits, links or removes a
definition, changes settings or account access, or restarts a host. Profile
metadata and a passing preflight are source and configuration evidence; only a
live run qualifies the installed workflow.
