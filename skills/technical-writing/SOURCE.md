# Technical writing provenance

- Upstream repository: `https://github.com/cursor/plugins`
- Upstream plugin and path: `pstack/skills/technical-writing/SKILL.md`
- Pinned source revision: `46125561306434d8a1d7745d540d8932ab0cd2a2`
- Retrieved: `2026-08-22`
- Upstream `SKILL.md` SHA-256: `bd0cb21034f4fe6695cfdf8cd3561026eec943f0bb6e9300bc78a2b3340865a7`
- License: MIT, Copyright (c) 2026 Lauren Tan; preserved in `LICENSE`

## Local adaptations

The upstream explicit-invocation setting moves from Cursor-only frontmatter to
`agents/openai.yaml`. The local version keeps the Diátaxis mode selection,
developer-focused sentence style, Simplified Technical English constraints,
Global English disambiguation, and `unslop` final pass in a shorter portable
workflow.

It removes upstream instructions to change another skill and project-specific
snippet indentation. It adds authority and evidence boundaries so a writing
request does not silently authorize repository or external-system changes.

Updates are manual. Fetch the pinned source into a temporary directory, review
the license and complete diff, recompute the digest, and rerun all checks before
changing this copy.
