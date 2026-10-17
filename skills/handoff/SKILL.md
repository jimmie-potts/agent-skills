---
name: handoff
description: Explicitly prepare a redacted, nonauthoritative snapshot so another agent can continue a bounded task. Use only when the user directly invokes handoff and identifies or authorizes the recipient context.
---

# Handoff

Write a snapshot so a fresh agent can continue the work. Reference specs, plans,
ADRs, issues, commits and diffs by path or URL instead of copying them.

Read the state back just before writing, and include:

- repository and worktree paths, issue identifier and title when present;
- branch, frozen `HEAD` commit and dirty paths;
- work done and work remaining;
- authority granted, authority absent and approvals still needed;
- blockers, risks and open decisions;
- verification commands with pass, fail or unavailable results; and
- suggested next skills.

Say when Git, tracker or test evidence was unavailable instead of guessing.
Replace secrets and personal data with `<REDACTED>`. Label the snapshot
nonauthoritative and time-bound.

Return it in the response. Write a file or use a native transfer tool only when
the user names the destination or recipient. Use `unslop` on the narrative when
needed.
