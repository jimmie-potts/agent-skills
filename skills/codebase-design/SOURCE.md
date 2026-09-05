# Codebase design provenance

- Upstream repository: `https://github.com/mattpocock/skills`
- Upstream path: `skills/engineering/codebase-design/`
- Pinned source revision: `5b15a47f2d7150f545fbcacbfe381787fc0230dc`
- Retrieved: `2026-08-23`
- Upstream source SHA-256 digests:
  - `DEEPENING.md`: `f3dd099ce99289bd213914d8ee3e2429b78309c3957ca4583f7659551b1d53c1`
  - `DESIGN-IT-TWICE.md`: `8e740bf98446dbd4dfdc132ac4346d9a7eedaf93de6a495889171cf7f99f16bd`
  - `SKILL.md`: `2c20617f87ec8af6a434859f381b2f061a69b530444e74eb39e78bb016a6d1e2`
  - `agents/openai.yaml`: `edebc9e4fcfe102114012575eaa9600b9b5fd08c311664f389c36e7bc717740f`
  - Repository `LICENSE`: `0e7ac423bf2c6e223b7c5b156f8cf72da49d748e56a1641402c31f22ad07dbb5`
- License: MIT, Copyright (c) 2026 Matt Pocock; preserved in `LICENSE`

## Local adaptations

The local version keeps interface depth, locality, seam placement, dependency
classification, adapter analysis, interface-level testing, and alternative
design comparison. It treats each as a heuristic that must be supported by
repository evidence.

Repository vocabulary is authoritative, so the upstream ban on established
terms such as service, component, API, and boundary was removed. Absolute rules
about adapter counts, dependency injection, deepening, and deleting old tests
became questions with explicit exceptions.

`DEEPENING.md` and `DESIGN-IT-TWICE.md` were adapted into
`references/deepening.md` and `references/alternative-designs.md`. The latter
has a separate-pass fallback when isolated agents are unavailable. Full
architecture workflows remain owned by `architect`, and historical rationale
remains owned by `why`. The skill grants no edit or external-effect authority.

Scope, change records, and delivery authority come from the target repository.
The shared workflow does not require Jira, OPSX, or a named delivery skill.

Updates are manual. Fetch the pinned upstream directory and repository license
into a temporary location, review every file and the complete diff, recompute
all digests, and rerun the repository's focused and full checks before changing
this copy.
