# Architect provenance

- Upstream repository: `https://github.com/cursor/plugins`
- Upstream plugin and path: `pstack/skills/architect/`
- Pinned source revision: `46125561306434d8a1d7745d540d8932ab0cd2a2`
- Retrieved: `2026-08-23`
- Upstream source SHA-256 digests:
  - `SKILL.md`: `585d7a9e03c0cced84c80d4b60c09c8dc76010bb36c579f92d9e4deafec53df7`
  - `references/design-red-flags.md`: `905066f9bbac81c573c2b325be47751d2c0f9325e0a0772bd4384e82dafe9336`
  - `references/rationale-template.md`: `6645a0e5f68c003298ec95b85a23262bdda0c79f998b926060169b54d9f23fbb`
  - `references/runner-prompt.md`: `3ef8c1452a0382a15b7601c7c94f2a16a00954170d705b7af8cc49ac78080ec9`
- License: MIT, Copyright (c) 2026 Lauren Tan; preserved in `LICENSE`

## Local adaptations

The upstream explicit-invocation setting moves from Cursor-only frontmatter to
`agents/openai.yaml`. Fixed model slugs, Cursor task APIs, autonomous checkpoint
assumptions, and commit guidance were removed. The local version preserves the
composition of `how`, `why`, `arena`, `interrogate`, and `unslop` without letting
one skill expand another's authority.

The upstream design-red-flags and runner guidance were consolidated into
`references/design-review.md`. The rationale template remains a separate output
contract. The implementation phase now runs only when the user's underlying
task requests implementation, and unfinished sketches stay out of production
paths unless staged breakage is explicitly authorized.

Updates are manual. Fetch the pinned source into a temporary directory, review
the license and complete diff, recompute every upstream digest, and rerun all
checks before changing this copy.
