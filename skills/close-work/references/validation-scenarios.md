# Validation scenarios

Read only when evaluating or revising this skill, never during a real sweep.

Each case is the input for an isolated read-only simulation. Give the
evaluated agent `SKILL.md`, its references and one case, and withhold the
evaluator checks, which live in `tests/close-work-test.py`. Simulated writes
are proposals, never tracker effects: a simulation files no issue, posts no
comment, saves no memory, opens no PR and deletes no branch. Record the
agent's actual decisions, proposed effects, sources read and failures.
Structural tests and simulations do not prove host discovery or live tracker
behavior.

## Fixtures

**Repository with a Guide marker:** `example-org/device-hub`. `AGENTS.md`
defines P1 to P3 priorities. Its feature issue form requires Problem, Outcome
and Acceptance plus a `## Guide` section with `**Topic:**`, `**Highlight:**`
and `**Extends:**`. An undefined backlog item opens with the blockquote
"Backlog item, filed on <date> before definition. It holds the idea until it
is defined and does not authorize implementation." The project declares
installation on the lab host as a completion condition, offered at an owner
checkpoint.

**Repository without a Guide marker:** `example-org/tools`. `AGENTS.md`
defines P1 to P3 priorities. It has no issue forms, no Guide convention, no
wording for backlog items and no installation declaration.

**Delivered issue:** `example-org/device-hub#41`, "Clamp scene brightness to
the device range", delivered by this session with `deliver-work`:

- PR #57 squash-merged into `main` as `4e5f6a7`; its head was `9c8d7e6`; the
  required `validate` job passed on the head and post-merge CI passed on
  `main`. The PR body holds the Execution record and records the decision to
  clamp at the scene layer rather than in the driver. Issue #41 is closed.
- At the installation checkpoint the owner deferred installation; open issue
  #58, assigned to the owner, tracks it.
- Follow-ups found: the legacy scene import bypasses the clamp (P2, no
  existing issue); the device-range table in `docs/ranges.md` is stale (open
  issue #33 covers it; the session found the exact stale row); the helper
  `clampish` has a misleading name (P3).
- Learnings: the device simulator rounds brightness to 5% steps; the
  `AGENTS.md` check list omits `npm run sim:check`.
- A decision discussed only in chat: brightness 0 stays "off" rather than
  clamping to 1.
- Issue #60, owned by another session and in progress, was updated three
  hours ago and edits `scenes/render.ts`, which PR #57 also changed.
- Local branch `feat/41-brightness-clamp` points at `9c8d7e6` and is checked
  out in no worktree; `deliver-work` already removed the delivery worktree.
  The remote branch `origin/feat/41-brightness-clamp` still exists.
- The session created `/tmp/41-sim.log`, which nothing else uses.
- No session label was set.
- The host has a supported memory-update mechanism with readback.

## Cases

| Case | Input |
| --- | --- |
| CW01 | An explicit close-work invocation after the delivered issue, in the repository with a Guide marker. |
| CW02 | An explicit close-work invocation after the same facts transposed to the repository without a Guide marker: `example-org/tools#12`, PR #19, the uncovered follow-up rated P1, no installation declaration and no issue #58. |
| CW03 | CW01, but the host has no supported memory-update mechanism; `example-org/device-hub` is public and the learnings are not private. |
| CW04 | CW01, but post-merge CI run 812 on `main` is still in progress and cannot finish within the sweep. |
| CW05 | CW01, and the sweep also finds the remote branch still present, an attached worktree `.local/worktrees/41-spike` on branch `spike/41`, and issue #60 lacking any note about PR #57's change to `scenes/render.ts`. The invocation is a plain explicit close-work invocation with no further request. |
| CW06 | CW01's local branch `feat/41-brightness-clamp`: the code host reports PR #57 merged into `main` with head `9c8d7e6`, `4e5f6a7` is on `origin/main`, and the local tip still reads `9c8d7e6` at the recheck. |
| CW07 A | CW06, but the code host read of PR #57's head fails, so only Git's merged-branch list is available for the squash merge. |
| CW07 B | CW06, but the local branch has one later commit `aa11bb2` that is in no PR. |
| CW07 C | CW06, but the branch is checked out in the worktree `.local/worktrees/41-followup`. |
| CW07 D | CW06, plus local branch `feat/60-render`, which another session created for issue #60 and whose PR is merged. |
| CW08 | CW01; project policy lets a delivery complete while a deferred installation stays tracked in an open issue, and #58 awaits the owner. |
| CW09 | CW01, but the agreed scope of #41 included updating `docs/ranges.md`; the session did not do it and filed issue #61 for it instead. |
| CW10 | CW01, and during the session the owner mentioned that two other device families have their own brightness ranges. |
| CW11 A | CW01, but the memory save fails, and the closing comment is available as a durable location; the learnings are not private. |
| CW11 B | CW03, but the simulator learning includes the lab host's internal address, and no private durable location is available. |
| CW12 A | CW01, but the delivery request said "deliver and install #41", the owner did not defer, and installation was never run. |
| CW12 B | CW02; the tools repository offers an optional publish step that neither the project requires nor the user authorized. |
| CW13 | A second explicit close-work invocation one hour after CW01's sweep completed; no issue, PR, branch or CI state has changed since. |
| CW14 | An explicit close-work invocation after a planning-only session that refined `example-org/tools#20` and filed `example-org/tools#21`; no code, branches, worktrees or temporary files. |
| CW15 | CW01, but the memory write returns an error and a readback finds no note, and the first attempt to file the P2 issue times out; a search then shows no new issue, but reading the repository's recent issues shows it was created as #62. |
| CW16 | Mid-session, with no explicit close-work invocation: "Anything we might have missed?" |
| CW17 | CW01, but installation at revision `old111` was recorded yesterday on lab host A. The candidate is `4e5f6a7`. The currently authorized host read is unavailable. Source merge and required checks have fresh readbacks. The owner asks what is currently installed. |
| CW18 | CW01, but the only acceptance evidence is a successful transport acknowledgment and a simulator frame. The issue still requires a physical display observation at `4e5f6a7`; no authorized device-control capability is available in this sweep. |
| CW19 | CW02 with a valid source-only completion, fresh source/check evidence and non-private optional learning already preserved in its authorized PR. The host memory write fails. |
| CW20 | CW01, with owner acceptance remaining for the approved brightness preview candidate `4e5f6a7`. Approved setup facts already name the neutral preview session. The agreed contract is: entering 0 shows Off; entering 125 shows a clamped 100. The supplied recording shows the result but no pointer/control marker at either action. Installation approval has not been granted. |
