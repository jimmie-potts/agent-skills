# Why provenance

- Upstream repository: `https://github.com/cursor/plugins`
- Upstream plugin and path: `pstack/skills/why/SKILL.md`
- Pinned source revision: `46125561306434d8a1d7745d540d8932ab0cd2a2`
- Retrieved: `2026-08-22`
- Upstream `SKILL.md` SHA-256: `dc8f2d8a7dbef7d0467cca8e6d055a4dbde027db6e2cbbfb18aa9071d8f20b6c`
- License: MIT, Copyright (c) 2026 Lauren Tan; preserved in `LICENSE`

## Local adaptations

The portable frontmatter keeps only `name` and `description`, with Codex
selection policy in `agents/openai.yaml`. The evidence model, confidence
calibration, coverage map, and source accounting are preserved. Cursor-specific
MCP discovery, model names, task APIs, automatic fan-out, and the unsafe
`readonly: false` investigator configuration were removed.

The local workflow searches only sources that are available and authorized. It
does not treat an unavailable category as a null result or require access to
private systems. The upstream reference set was condensed into a self-contained
portable workflow; unused service-specific playbooks are not vendored.

Updates are manual. Fetch the pinned source into a temporary directory, review
the license and complete diff, recompute the digest, and rerun all checks before
changing this copy.
