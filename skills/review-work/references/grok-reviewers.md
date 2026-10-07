# Grok Bot independent reviewer settings

Use when the host exposes a `Task` tool that can spawn an `executor` (or
verified equivalent) subagent in a fresh context, with messaging/stop controls
available when a later round must resume the same reviewer. Inspect the actual
tool schemas and host model descriptions before calling. Worker attempt
thresholds are separate from review-round accounting; worker replacement resets
none of the [review-cycle history](review-cycles.md).

Use this mapping for both Standards and Specification. Place the work by
[review selection](review-selection.md#select-for-impact-and-the-review-task)'s
impact and review task, from what the work needs rather than the settings its
implementer ran with.

| Impact | Reviewer default | Rationale and limits |
| --- | --- | --- |
| Low or medium impact, bounded review task: settled requirements and reliable checks that cover the criteria | One fresh `Task` executor per axis at host-default or composing-workflow model with effort `high` when the host exposes effort | Capable verification where the task and checks justify its coverage; label Availability provisional until the live slug and effort controls are verified |
| Low or medium impact, review task needing stronger judgment: several interacting interfaces, state transitions or invariants, or meaningful design judgment | One fresh executor per axis with any stronger host-supported reasoning the review task warrants (at least `high` when exposed) | The reviewer needs the cross-interface judgment the change needed. A weaker default is not an equivalent; an exception needs comparable evidence and stated coverage limits |
| High impact, even with a tiny diff | Strongest evidenced relevant host-supported model/effort (at least `high`, or above-high only with a task-specific reason and verified support) in separate fresh reviewer contexts | Inspect high-impact negative cases; do not inherit the implementer's settings by omission |

Before spawning, run the [reviewer execution preflight](reviewer-execution.md)
with the controls below.

## Know the controls

| Control | How the host resolves it | Evidence |
| --- | --- | --- |
| Model and reasoning | An explicit `Task` model or reasoning parameter when the schema exposes one, otherwise the parent's inherited values. Supported levels depend on the live host | Requested: the values passed. Observed: returned runtime metadata when the host exposes it. Self-reported: the reviewer's statement from its own runtime instructions |
| Fresh context | Every new `Task` spawn starts from the brief. Do not pass a full-history fork or isolation that starts from another base | The spawn type and parameters passed |
| Profile | Grok Bot has no Claude-style `review-work-reviewer` tool profile and no Codex `review_work_reviewer` agent file in this skill. Do not claim either | Absence of a resolved profile name in the host's agent listing |
| Tools and sandbox | Children inherit the parent's tools and permissions unless the host shows a narrower enforced set. File writes, publication and descendant agents are instruction-only unless host evidence shows otherwise for this reviewer | The parent's current permissions and the child's exposed tools when visible |
| Nesting | Treat descendant spawning as forbidden for reviewers. Without an enforced empty multi-agent tool set, the no-descendant rule is instruction-only | The child's exposed tools, when visible |
| Delivery, cancellation and identity | Retain the agent or task identifier. Use `MessageSubagent` to follow up the same reviewer when [review cycles](review-cycles.md) allows it; use `StopSubagent` (or the verified stop control) to cancel. A return missing its findings list or coverage is partial | The delivered message and the retained identifier |

Sources: Grok Bot Task / MessageSubagent / StopSubagent behavior as recorded in
`skills/worker-with-grok/references/grok.md` and the settled review lockdown in
[#143](https://github.com/jimmie-potts/agent-skills/issues/143#issuecomment-6041531519)
decision 3 (instruction-only read-only executor reviewers on Grok; no Claude
`review-work-reviewer` profile claim). Inspect the active surface's schema before
relying on any control, and never apply another host's controls here.

## Select and spawn

Spawn each reviewer with `Task`, the executor (or verified equivalent) type, any
exact selected model/effort the schema supports, and a self-contained brief.
Do not invent Codex or Claude model aliases. There is no provisioned
review-work profile to select on this host; do not create, edit or install one,
and do not claim Claude Code tool-profile enforcement or a Codex
`review_work_reviewer` sandbox.

Record each part of the restriction separately. File writes, publication and
descendants are instruction-only unless host evidence shows an enforced narrower
tool set or sandbox for this reviewer. Every part without that evidence is
instruction-only. Axes that lack required evidence for a mandatory control are
`incomplete`, with the gap named, as
[reviewer execution](reviewer-execution.md) requires. Never fill a missing
control by simulating the reviewer in the coordinator session.

Keep the retained agent or task identifier for each reviewer. After a restart or
handoff, reconcile recorded reviewers with host listing tools where they exist;
a completed agent or message you cannot match to a recorded launch is
unattributed. Treat a final message without its findings list or coverage as
partial, and an interrupt as a cancelled return.

Record requested parameters and returned runtime metadata separately; a
successful spawn proves the request succeeded, not the executing model. Stop a
reviewer with the surface's interrupt or close control. Follow up the same
reviewer for a later round only when [review cycles](review-cycles.md) allows it.

Do not create, edit or install host agent definitions or change personal
settings to obtain a reviewer. The owning environment provisions profiles on
hosts that use them, as
[reviewer execution](reviewer-execution.md#discover-provisioned-profiles)
describes; this adapter ships none.

Grok Bot in this table is an independent reviewer, not an implementation worker
or a replacement coordinator. Reviewer suitability remains a hypothesis until
evaluated on comparable work; a model listing is not live review verification.
Explicit user or project requirements override these defaults; comparable
evidence supports only the exceptions review selection allows. Different models
for the two axes remain optional. A fallback for a rejected default stays within
models the live host exposes, never a silent substitute from another host.

Apply [reviewer execution](reviewer-execution.md)'s canonical model-setting
decision separately for every reviewer. Selected call parameters remain requests
unless the owner declares them or the host separately exposes a launch selection.
Retain applicable declaration scope through recovery and recheck replacements;
unknown observations are not mismatches. Declarations do not prove host controls.
