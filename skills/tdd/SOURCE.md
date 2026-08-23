# TDD provenance

- Upstream repository: `https://github.com/cursor/plugins`
- Upstream plugin and path: `pstack/skills/tdd/SKILL.md`
- Pinned source revision: `46125561306434d8a1d7745d540d8932ab0cd2a2`
- Retrieved: `2026-08-22`
- Upstream `SKILL.md` SHA-256: `adad031f9e79d7f7389fa128f7af8e03344831270e282cf4e40bdacb8418c386`
- License: MIT, Copyright (c) 2026 Lauren Tan; preserved in `LICENSE`

## Local adaptations

The upstream explicit-invocation setting moves from Cursor-only frontmatter to
`agents/openai.yaml`. The red, green, and adjacent-verification workflow remains
intact. The local version adds an authority boundary, protects unrelated user
changes, and prevents reconstructed claims about a failing-before result.

The trigger is narrowed to explicit TDD or regression-test requests. The
upstream heuristic that could select TDD automatically for an obvious cheap
test does not override its own explicit-only host policy.

Updates are manual. Fetch the pinned source into a temporary directory, review
the license and complete diff, recompute the digest, and rerun all checks before
changing this copy.
