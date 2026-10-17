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

Adds a verified state checklist (paths, branch, frozen commit, dirty state,
authority, blockers, verification results) that close-work relies on. Output
returns in the response instead of an automatic temporary file; a file or native
transfer needs a user-named destination or recipient.

Updates are manual. Fetch the pinned upstream directory and repository license
into a temporary location, review every file and the complete diff, recompute
all digests, and rerun the repository's focused and full checks before changing
this copy.
