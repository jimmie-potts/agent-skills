# Grok Bot independent reviewer settings

Use when the host exposes a `Task` tool that can spawn an `executor` (or
verified equivalent) subagent in a fresh context, with messaging/stop controls
available when a later round must resume the same reviewer. Inspect the actual
tool schemas and host model descriptions before calling. Worker replacement resets none of the
[review-cycle history](review-cycles.md).

Choose settings under [review selection](review-selection.md); this adapter
prescribes no model or thinking level. Before spawning, apply the
[reviewer execution preflight](reviewer-execution.md) with the controls below.

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

Different models for the two axes are optional. Use only available host
controls; do not invent cross-host aliases or claim unsupported restrictions.

For explicitly required settings, apply
[reviewer execution](reviewer-execution.md)'s setting check for that reviewer. Selected call parameters remain requests
unless the owner declares them or the host separately exposes a launch selection.
Retain applicable declaration scope through recovery and recheck replacements;
unknown observations are not mismatches. Declarations do not prove host controls.
