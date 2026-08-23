# Blast radius provenance

- Upstream repository: `https://github.com/cursor/plugins`
- Upstream plugin and path: `pstack/skills/blast-radius/SKILL.md`
- User-supplied source: `https://github.com/cursor/plugins/blob/main/pstack/skills/blast-radius/SKILL.md`
- Pinned source revision: `e46364b8be46000b7df0f260550cd712afbb8d36`
- Retrieved: `2026-08-22`
- Upstream `SKILL.md` SHA-256: `b060df3ca85803eabbce9fab53f5cc024ca8d784bdde5513c1c1a784947523f8`
- License: MIT, Copyright (c) 2026 Lauren Tan; preserved in `LICENSE`

## Local adaptations

The portable frontmatter keeps only `name` and `description`. The upstream
explicit-invocation policy moves to `agents/openai.yaml` for Codex, while the
shared description instructs other hosts to select the skill only for direct
blast-radius requests.

The upstream workflow composes `how`, `why`, `arena`, and `unslop`. Those skills
are canonical catalog entries here, so this copy retains their roles while
keeping its core inspection and proof steps usable on their own. It invokes
`arena` only after an explicit request for competing parallel reviews. It also
adds an authority boundary so a review request does not silently authorize
network access, dependency changes, tracked-file edits, live-system calls, or
untrusted code execution.

Updates are manual. Fetch the pinned upstream source into a temporary directory,
review its license and complete diff, recompute the source digest, and rerun the
focused and canonical offline checks before changing this copy.
