# Interrogate provenance

- Upstream repository: `https://github.com/cursor/plugins`
- Upstream plugin and path: `pstack/skills/interrogate/`
- Pinned source revision: `46125561306434d8a1d7745d540d8932ab0cd2a2`
- Retrieved: `2026-08-23`
- Upstream source SHA-256 digests:
  - `SKILL.md`: `a009220dfe6869c8f7980a94fb1c9c7763a081a0b32fb6d0afb65b8ff1868146`
  - `references/code-quality-review.md`: `2462f1347b99b412b04fcb0577b96d8744c801f792f2651746f9409fd4465dc9`
  - `references/lead-judgment.md`: `d2cea6cc308758201c6b8b82baf780947645f1ab752707ddf97fab374bf473f9`
  - `references/reviewer-prompt.md`: `a397cc61102add709803d917fb23d726920525bf23e7c06dc4ed0b5cbeb00e54`
  - `references/rubric.md`: `a67bf02426f88714634ff481d667db821d4b2cea7b335bcd165fe3126e427fb5`
- License: MIT, Copyright (c) 2026 Lauren Tan; preserved in `LICENSE`

## Local adaptations

The upstream explicit-invocation setting moves from Cursor-only frontmatter to
`agents/openai.yaml`. Fixed model slugs, Cursor rule paths, Task API fields, and
automatic pull-request creation for model configuration errors were removed.
The local workflow selects independent reviewers from the host's available
models and reports when genuine independence is unavailable.

The four upstream references were consolidated into
`references/review-rubric.md`. The local rubric preserves correctness, root
cause, structural quality, verification, complexity, security, finding format,
and lead adjudication while removing arbitrary model and file-size defaults.
An authority boundary keeps the review read-only and forbids automatic fixes.

Updates are manual. Fetch the pinned source into a temporary directory, review
the license and complete diff, recompute every upstream digest, and rerun all
checks before changing this copy.
