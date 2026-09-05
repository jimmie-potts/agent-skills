# Prototype provenance

- Upstream repository: `https://github.com/mattpocock/skills`
- Upstream path: `skills/engineering/prototype/`
- Pinned source revision: `5b15a47f2d7150f545fbcacbfe381787fc0230dc`
- Retrieved: `2026-08-23`
- Upstream source SHA-256 digests:
  - `LOGIC.md`: `f61c7d249e786a79ef289018901c348271e1798dd0b0bc5607b5c6f4d4a01ab9`
  - `SKILL.md`: `714de632d116bb73f65cdb5a882db15b9369a6713b9a47c0fad827848f0bfbe3`
  - `UI.md`: `723211e878acbc7b6ff09755263f3295cde724ba902ff0064da41eed51d45ad3`
  - `agents/openai.yaml`: `5af65e43ab41a350436697b81e27b7f848d36782043b73c322bb2c9fa9cc55dc`
  - Repository `LICENSE`: `0e7ac423bf2c6e223b7c5b156f8cf72da49d748e56a1641402c31f22ad07dbb5`
- License: MIT, Copyright (c) 2026 Matt Pocock; preserved in `LICENSE`

## Local adaptations

The local version keeps one concrete question, separate logic and UI branches,
visible state and edge-case scenarios, and structurally different UI variants.
It requires an explicit choice between a disposable experiment and a functional
delivery slice.

`LOGIC.md` and `UI.md` were adapted into `references/logic.md` and
`references/ui.md`. Automatic production-adjacent placement, routes, branches,
commits, issue updates, browser opening, and promotion were removed. Disposable
work requires an authorized isolated location. Functional slices require normal
repository tests, error handling, and production-quality completion for their
accepted behavior. Unfinished or untested code cannot remain in production
paths.

Codex invocation is explicit-only. The skill does not independently grant file,
dependency, server, browser, Git, tracker, or publication authority.

Scope, change records, and delivery authority come from the target repository.
The shared workflow does not require Jira, OPSX, or a named delivery skill.

Updates are manual. Fetch the pinned upstream directory and repository license
into a temporary location, review every file and the complete diff, recompute
all digests, and rerun the repository's focused and full checks before changing
this copy.
