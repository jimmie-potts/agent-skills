# How provenance

- Upstream repository: `https://github.com/cursor/plugins`
- Upstream plugin and path: `pstack/skills/how/SKILL.md`
- Pinned source revision: `46125561306434d8a1d7745d540d8932ab0cd2a2`
- Retrieved: `2026-08-22`
- Upstream `SKILL.md` SHA-256: `fe503e7a9b2a3a7ad2622a2de6124cb06c466922fb44bc61817b49b52042b885`
- License: MIT, Copyright (c) 2026 Lauren Tan; preserved in `LICENSE`

## Local adaptations

The portable frontmatter keeps only `name` and `description`. Codex selection
policy lives in `agents/openai.yaml`. The workflow preserves explain, placement,
and critique modes but removes Cursor-specific model names, task APIs, and
automatic delegation. Parallel exploration now requires explicit user authority
and host support. The prompt templates were folded into concise, host-neutral
instructions, so unused upstream reference files are not vendored.

An authority boundary prevents an explanation request from silently fetching
remote state, installing dependencies, changing files, executing untrusted
code, or querying external systems.

Updates are manual. Fetch the pinned source into a temporary directory, review
the license and complete diff, recompute the digest, and rerun all checks before
changing this copy.
