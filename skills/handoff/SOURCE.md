# Handoff provenance

- Upstream repository: `https://github.com/mattpocock/skills`
- Upstream path: `skills/productivity/handoff/`
- Pinned source revision: `5b15a47f2d7150f545fbcacbfe381787fc0230dc`
- Retrieved: `2026-08-23`
- Upstream source SHA-256 digests:
  - `SKILL.md`: `7c62de979fdc7ac32fb5ddb2146156c917f80ee070d30fadc9d40343c4b6ed25`
  - `agents/openai.yaml`: `5c479fd562c691851690e8b18c8501045bef0943c10743d636b2fae26add1d28`
  - Repository `LICENSE`: `0e7ac423bf2c6e223b7c5b156f8cf72da49d748e56a1641402c31f22ad07dbb5`
- License: MIT, Copyright (c) 2026 Matt Pocock; preserved in `LICENSE`

## Local adaptations

The local version keeps a compact, redacted continuation snapshot and pointers
to authoritative artifacts. It adds repository path, worktree, issue identity
when present, branch, frozen commit, dirty state, authority, blockers, and exact
verification evidence.

The snapshot is explicitly nonauthoritative and time-bound. Repository sources
own scope, dependencies, and change records. The response is the default output.
A native context-transfer tool requires an authorized recipient and documented
behavior that matches the requested effects. Moving Git state, interrupting a
task, or starting work requires authority for those effects even when a host
calls the tool a handoff. Automatic temporary-file creation was removed, and a
file requires an exact user-authorized destination. The workflow itself grants
no tracker, repository, Git, publication, installation, or implementation
authority.

Updates are manual. Fetch the pinned upstream directory and repository license
into a temporary location, review every file and the complete diff, recompute
all digests, and rerun the repository's focused and full checks before changing
this copy.
