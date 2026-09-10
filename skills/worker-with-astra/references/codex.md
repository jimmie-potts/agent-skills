# Codex collaboration adapter

Use this adapter when the host exposes `collaboration` tools with model
selection and parent messaging. Check the current tool schema before use; these
instructions do not add unavailable capabilities.

## Start one worker

Use the host's runtime metadata or authoritative session instructions to
establish the coordinator's model identity. An available `gpt-6-astra` spawn
option alone does not establish the current model. If the current identity is
unknown or different, report that the requested pairing cannot be established.

Call `collaboration.spawn_agent` with a unique task name, the self-contained
brief from SKILL.md, the selected `model` and supported `reasoning_effort`, and
`fork_turns="none"`. Full-history forks inherit the parent's model and do not
accept model overrides in this host. Preserve deliver-work's stronger supported
selection when composed. Otherwise apply the tier reference's default after
checking the current host schema. Record requested and observable settings
separately.

Include the coordinator's actual canonical agent address, obtained from the
host, in the brief. Do not hard-code `/root` when the coordinator has another
address. Retain the returned worker ID or canonical task name for replies.
Supply the skill and adapter text or accessible paths with an instruction to
read them. A fresh worker needs the task context as well as those files.

Use runtime model information returned by the host when available. A successful
spawn with the explicit model parameter records the requested selection; it
does not by itself prove an independently verified runtime identity. If the
host rejects the model or cannot spawn the worker, report the error without
retrying with a different model.

## Exchange advice without losing the worker

The worker calls `collaboration.send_message` targeting the supplied parent
address for its approach checkpoint, blocker consultations, and final-review
request. Label whether a message needs advice or presents a completed result.
For an advice request, include the evidence, recommendation, and paused
dependency.

The coordinating Astra agent stays active, receives messages, and replies to
the worker's retained ID/address using `collaboration.send_message`. The worker
waits for the answer before resuming dependent work. Both agents may use
`collaboration.wait_agent` while awaiting communication. Its result is a
notification, so read the delivered mailbox message rather than treating a
timeout or notification as advice or completion. Keep individual waits at or
below 60 seconds so user updates remain possible.

`send_message` does not start a new turn for an idle agent. If the worker has
finished its turn while awaiting advice or returned work that needs
corrections, Astra uses `collaboration.followup_task` with the reply or
correction to resume that same worker. Use `collaboration.list_agents` when
lifecycle state is unclear. Do not ask the worker to resume an idle original
coordinator: keep Astra active for the consultation cycle. If the user pauses
the task, preserve the worker address and pending question for resumption.

On worker failure, inspect the returned state and evidence before taking
further action. Report a terminal failure or unavailable communication as a
blocker; do not claim a completed advisory exchange or replace the advisor.

## Replace an ended attempt

For a composing workflow's approved settings change, follow its shared
attempt-handoff contract. Use `list_agents` to establish state and
`interrupt_agent` to stop an active old assignment; verify it is no longer
running before `spawn_agent` starts a fresh context. Never describe the new
context as `followup_task` resumption. Transfer the complete handoff brief and
retain the same original advisor. If the old assignment cannot be stopped,
report that blocker rather than overlap ownership.

## Ownership and delivery

Agents share the filesystem. State write ownership in the initial brief. Under
coordinator-only-write rules, the worker returns proposed patches without
applying them. Astra applies the agreed patch and supplies the resulting
revision or files for the worker's validation. Validation must respect the same
permissions, including whether generated artifacts are allowed.

Use the host's exposed tool interface directly. In hosts where collaboration
tools are not available inside an execution wrapper, call them outside that
wrapper. Never simulate a second model by writing both sides of a dialogue.
