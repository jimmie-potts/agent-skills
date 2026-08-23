# Arena provenance

- Upstream repository: `https://github.com/cursor/plugins`
- Upstream plugin and path: `pstack/skills/arena/SKILL.md`
- Pinned source revision: `46125561306434d8a1d7745d540d8932ab0cd2a2`
- Retrieved: `2026-08-22`
- Upstream `SKILL.md` SHA-256: `a2241e8500a44d9c16bd3260c8c70e28c4bb8a857c33061d42b267057e6f7093`
- License: MIT, Copyright (c) 2026 Lauren Tan; preserved in `LICENSE`

## Local adaptations

The upstream explicit-invocation policy moves from Cursor-only frontmatter to
`agents/openai.yaml`, while the shared description retains the explicit trigger
for other hosts. Fixed Cursor model names, rule paths, task API fields, and
automatic filesystem writes were removed. The candidate, judge, pick, graft,
and verification phases remain, with portable isolation and authority rules.

The workflow requires real independent candidates. When a host cannot provide
them, it reports the limitation rather than fabricating a comparison.

Updates are manual. Fetch the pinned source into a temporary directory, review
the license and complete diff, recompute the digest, and rerun all checks before
changing this copy.
