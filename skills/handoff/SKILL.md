---
name: handoff
description: Explicitly prepare a redacted, nonauthoritative snapshot so another agent can continue a bounded task. Use only when the user directly invokes handoff and identifies or authorizes the recipient context.
---

# Handoff

Capture enough verified state for another agent to continue without treating
the handoff as an authoritative scope or status source. Link authoritative
artifacts instead of copying their full contents.

This skill grants no authority to change the repository, trackers, delivery
records, Git state, personal files, or external systems. A handoff transfers
context and existing authority boundaries; it does not broaden them.

## Freeze and verify the snapshot

Read back the current state immediately before the handoff. Include:

- repository path and worktree path;
- issue identifier and full title when one is present;
- branch name;
- frozen `HEAD` commit or other immutable comparison identifier;
- dirty state and the paths of relevant tracked and untracked changes;
- completed work and remaining work;
- authority granted, authority explicitly absent, and required approvals;
- blockers, risks, assumptions, and unresolved decisions;
- exact verification commands and their pass, fail, or unavailable results;
- authoritative artifact paths or URLs; and
- suggested next skills or workflows when they materially help the recipient.

State when Git, tracker, host, or verification evidence is unavailable. Do not
invent clean status, issue state, or completion from conversation memory.

## Redact and label

Remove secrets, credentials, tokens, private keys, authorization headers,
unrelated personal data, and sensitive environment values. Use `<REDACTED>` and
say when a redaction limits continuity.

Label the snapshot nonauthoritative and time-bound. Follow the repository's
authoritative sources for approved scope, dependencies, and change records.
The repository and test output own code and verification state.

## Deliver without side effects

Return the complete snapshot in the response by default. Use a host's native
context-transfer operation only when the user authorizes that transfer to an
identified recipient and the documented tool behavior matches the requested
effects. Moving Git state, interrupting a task, or starting work requires
authorization for those effects; a tool named handoff is not sufficient.
Write a handoff file only when the user authorizes an exact destination.

Do not create a temporary file automatically. Do not transition an issue,
comment, label, branch, commit, merge, publish, close, install, or start the
next workflow merely because it appears in the handoff.

Apply the `unslop` skill to the narrative snapshot without changing identifiers,
commands, paths, evidence, redactions, or authority boundaries.
