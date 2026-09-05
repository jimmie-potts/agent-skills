# Grill with docs provenance

- Upstream repository: `https://github.com/mattpocock/skills`
- Upstream path: `skills/engineering/grill-with-docs/`
- Pinned source revision: `5b15a47f2d7150f545fbcacbfe381787fc0230dc`
- Retrieved: `2026-08-23`
- Upstream source SHA-256 digests:
  - `SKILL.md`: `7de372c13488f1ee96cc11cd8907b56b6809cc93eef776eeddd37de6b6cbe3fe`
  - `agents/openai.yaml`: `94cd0ab161fb468a836349f5ed482ba58ce8e709a05c57ce533d739dbd35cca9`
  - Repository `LICENSE`: `0e7ac423bf2c6e223b7c5b156f8cf72da49d748e56a1641402c31f22ad07dbb5`
- License: MIT, Copyright (c) 2026 Matt Pocock; preserved in `LICENSE`

## Local adaptations

The local version expands the upstream two-skill composition into a portable
workflow. `grilling` supplies dependency-aware grouped frontier rounds, while
`domain-modeling` supplies repository-aligned vocabulary and decision-record
analysis. Proposed documentation changes accumulate without writes during
questioning.

After the user confirms decisions, the workflow shows exact proposed paths and
changes. It writes only when the underlying task separately authorizes those
repository edits. Cursor-only frontmatter was removed, Codex explicit-only
invocation lives in `agents/openai.yaml`, and the workflow does not acquire
Jira, planning publication, implementation, OPSX, Sprint Work, Git, or other
external-effect authority.

The shared adaptation uses repository-defined scope and delivery owners.
Deliberate composition returns to the authorized coordinator without new
permission or cancellation of existing authority; questioning remains read-only.

Updates are manual. Fetch the pinned upstream directory and repository license
into a temporary location, review every file and the complete diff, recompute
all digests, and rerun the repository's focused and full checks before changing
this copy.
