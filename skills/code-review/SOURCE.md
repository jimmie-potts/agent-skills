# Code review provenance

- Upstream repository: `https://github.com/mattpocock/skills`
- Upstream path: `skills/engineering/code-review/`
- Pinned source revision: `5b15a47f2d7150f545fbcacbfe381787fc0230dc`
- Retrieved: `2026-08-23`
- Upstream source SHA-256 digests:
  - `SKILL.md`: `47f4e52c21694def9c7c11cbfbf891ca35eac7a93e395797515be3c8a409ae50`
  - `agents/openai.yaml`: `8229ca854e11dc8e6aef2131ee03f31fb1561cf905fab9ccc325180cf3331352`
  - Repository `LICENSE`: `0e7ac423bf2c6e223b7c5b156f8cf72da49d748e56a1641402c31f22ad07dbb5`
- License: MIT, Copyright (c) 2026 Matt Pocock; preserved in `LICENSE`

## Local adaptations

The local version keeps one fixed comparison and separate Standards and Spec
reviews. Moving references resolve to recorded commits, and uncommitted review
input uses one captured patch. Independent contexts remain preferred, with a
two-pass single-agent fallback when isolation is unavailable.

The dependency on `setup-matt-pocock-skills`, its issue-tracker configuration,
and assumed tracker and repository layouts were removed. Standards and
specification sources now come from the user's request and authoritative
repository evidence. Generic smells are heuristics rather than repository
standards.

The adapted workflow returns findings only. It does not post comments, label or
transition work, edit code, fix findings, branch, commit, merge, close, publish,
or change Jira, GitHub, OPSX, or Sprint Work state.

The shared adaptation uses repository-defined scope and delivery owners.

Updates are manual. Fetch the pinned upstream directory and repository license
into a temporary location, review every file and the complete diff, recompute
all digests, and rerun the repository's focused and full checks before changing
this copy.
