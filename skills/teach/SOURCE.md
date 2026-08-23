# Teach provenance

- Upstream repository: `https://github.com/cursor/plugins`
- Upstream plugin and path: `pstack/skills/teach/SKILL.md`
- Pinned source revision: `46125561306434d8a1d7745d540d8932ab0cd2a2`
- Retrieved: `2026-08-22`
- Upstream `SKILL.md` SHA-256: `0a5987b0588dc56e14bfd84d0300e2ab405abc7c5c2aa81e0d3d7c6b243db7a7`
- License: MIT, Copyright (c) 2026 Lauren Tan; preserved in `LICENSE`

## Local adaptations

The upstream explicit-invocation setting moves from Cursor-only frontmatter to
`agents/openai.yaml`. The local workflow retains the composition of `how`,
`why`, and `unslop`, along with progressive teaching and selective visuals. It
removes automatic parallel execution and tool-specific image instructions.
Delegation now requires a separate explicit user request.

An authority boundary makes companion skill use read-only unless the original
task grants broader access. The visual guidance follows the host's rule that a
diagram must materially improve understanding.

Updates are manual. Fetch the pinned source into a temporary directory, review
the license and complete diff, recompute the digest, and rerun all checks before
changing this copy.
