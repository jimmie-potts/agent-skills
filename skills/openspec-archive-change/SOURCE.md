# OpenSpec core skill provenance

- Source: https://github.com/Fission-AI/OpenSpec/tree/v1.12.0
- Generator: `@fission-ai/openspec` version `1.12.0`, core Codex integration.
- Generated skill: `openspec-archive-change`.
- Generated `SKILL.md` SHA-256: `581ae5679612e832e93170a727216e714fbed17ba947848f806cacceb3228963`.
- License: MIT, preserved in `LICENSE`.

## Local adaptations

Portable frontmatter contains name and description; host metadata is separate.
Skill composition uses portable names. Sync requires a supported Purpose instead
of leaving unfinished text, and progress wording fits the catalog validator.
The shared workflow uses the consuming repository's pinned CLI and action
boundaries. Planning substeps preserve existing implementation authority, and
read-only requests do not gain artifact-write permission. Repository policy
owns issue identity, completion gates, and delivery effects.

Regenerate into an isolated temporary project when updating the pinned version.
Review the complete generated diff and these adaptations in this catalog.
Do not generate or vendor shared integrations in consuming product repositories.
