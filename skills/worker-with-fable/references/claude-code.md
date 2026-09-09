# Claude Code subagent adapter

Use this adapter when the host exposes an `Agent` tool that accepts a per-call
`model` and a `SendMessage` tool that resumes a spawned agent with its context
intact. Confirm both tool schemas are callable in the current session before
spawning. An `Agent` result can name `SendMessage` as the way to continue a
worker in a session that does not expose that tool; a worker spawned there
cannot be resumed, and the pairing's consultation cycle fails after the first
return. These instructions do not add unavailable capabilities.

## Establish identities

Read the coordinator's model from the host's runtime instructions, which name
the running model. An available `fable` spawn option, a persona prompt, or a
settings file alone does not establish the current model. If the runtime
instructions name another model or none, report that the requested pairing
cannot be established.

Subagent model precedence in Claude Code is the per-call `model` parameter,
then the subagent definition's `model` field, then the
`CLAUDE_CODE_SUBAGENT_MODEL` environment variable, then the coordinator's
model. Always pass `model` explicitly with the selected tier alias (`haiku`,
`sonnet`, or `opus`). Omitting it inherits Fable, which is not a pairing. Do
not create or edit `.claude/agents/*.md` definitions or settings to obtain a
model; report the gap if the parameter is unavailable. Do not use a skill's
`context: fork` frontmatter for this pairing: it runs the skill content as a
subagent's prompt, so the coordinator instructions would execute inside a
subagent and spawn the worker as a nested delegation.

A successful spawn with an explicit `model` records the requested selection.
It does not prove the executing model. The worker's own runtime instructions
name its model; the brief asks the worker to report that name in every return.
Workers omit this line under a busy brief. Treat an omitted report as an
unverified identity and ask again on the next resume; do not fill it in from
the requested parameter. Record requested and reported identities separately.

Fable may require usage credits on some plans. In an interactive session the
host prompts before billing; treat a declined prompt as an unavailable
coordinator, not as consent to substitute. Non-interactive runs bill without
a prompt, so confirm the plan allows Fable before starting one.

## Start one worker

Call the `Agent` tool once with the selected `model`, a general-purpose
subagent type, a distinctive description, and the self-contained brief from
SKILL.md. Include the skill and adapter text or readable paths with an
instruction to read them, the worker tier's decision boundary, and the task
context; a fresh subagent has none of the conversation. Run the spawn in the
foreground when the next coordinator step depends on the checkpoint, so the
coordinating turn stays active.

Retain the agent identifier returned by the host; every later exchange targets
it. The `Agent` tool exposes no per-call effort control, and a subagent
inherits the session's effort level by default. Record the session level as
the worker's reasoning setting when it is known, otherwise unknown, and do
not claim a different one.

## Exchange advice without losing the worker

Subagents cannot message the coordinator while running. A consultation is the
worker ending its turn with a labeled return: advice request or completed
result. An advice request carries the decision needed, evidence, the worker's
recommendation, and the paused dependency. Fable answers by calling
`SendMessage` with the retained identifier, and the worker resumes with its
context intact. A new `Agent` call starts a fresh worker with no memory of the
task; that is a second delegation, which this skill forbids for the same task.

The mandatory sequence is at least three worker turns: the approach proposal,
implementation through to the final-review request, and any corrections. Extra
turns occur for blocker consultations and for tiers whose decision boundary
requires returning after each bounded step. Fable's direction on each resume
names the decision made and what the worker may now proceed with.

If the host reports the worker as failed, terminated, or unreachable, inspect
the returned state and evidence before taking further action. Report a terminal
failure as a blocker; do not claim a completed advisory exchange, replace the
advisor, or silently start over with another worker. If the user pauses the
task, preserve the worker identifier and the pending question for resumption.

## Ownership and delivery

Subagents share the coordinator's working directory and run under the session's
permission mode. A denied tool call means the user declined; the worker reports
it rather than retrying. State write ownership in the brief.

Under coordinator-only-write rules, instruct the worker to return a unified
diff or exact file contents and to make no edits. Fable applies the agreed
patch and supplies the resulting revision or files for the worker's validation
turn. When the worker owns scoped writes, name its files and keep Fable out of
them until the worker returns. The `Agent` tool's worktree isolation option
gives the worker its own checkout when concurrent edits would otherwise
collide; Fable then reviews and brings that result back within the task's
existing Git authority. Validation must respect the same permissions,
including whether generated artifacts are allowed.

Never simulate the worker by writing both sides of a dialogue, and never report
a worker's requested model as its verified identity.
