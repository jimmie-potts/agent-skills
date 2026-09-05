# Learning workspace provenance

- Upstream repository: `https://github.com/mattpocock/skills`
- Upstream path: `skills/productivity/teach/`
- Upstream name: `teach`
- Local name: `learning-workspace`
- Pinned source revision: `5b15a47f2d7150f545fbcacbfe381787fc0230dc`
- Retrieved: `2026-08-23`
- Upstream source SHA-256 digests:
  - `GLOSSARY-FORMAT.md`: `9b99859ec28437668130d8f2ce5a342938970f8a1ed4fd38c3eab4f4b5fff210`
  - `LEARNING-RECORD-FORMAT.md`: `701fa34b6748aa89e6c960ffb815257f481a7d77fb2900f9028f7edf3fdd6052`
  - `MISSION-FORMAT.md`: `8cacbb3c0644d3ae0ea4965564797099401a6930a23f7cf462918576587f2418`
  - `RESOURCES-FORMAT.md`: `e9cacf34026e11a8d1c8f9de88abe5bcbf654f4ebdb25cae8c0de0d5f48f44ec`
  - `SKILL.md`: `a32df9dcdfc0c4fdc1c98e1ed3940c5f56b84c1aa90ff60346f32b8b53915b43`
  - `agents/openai.yaml`: `5856f3ae8aec742f1499c640aecdd5f1d6af5fa210a7c6ec794de8263a6f733f`
  - Repository `LICENSE`: `0e7ac423bf2c6e223b7c5b156f8cf72da49d748e56a1641402c31f22ad07dbb5`
- License: MIT, Copyright (c) 2026 Matt Pocock; preserved in `LICENSE`

## Local adaptations

Matt Pocock's upstream `teach` is renamed `learning-workspace` so it can coexist
with the existing pstack-derived `teach` conversational code and design lesson.
The local name is changed in the directory, portable frontmatter, and Codex
metadata. The existing `teach` workflow remains separate.

The stateful mission, trusted resources, lessons, reusable assets, reference
material, learning records, notes, retrieval practice, and glossary remain.
Mission, resource, learning-record, and glossary formats moved to
`references/mission.md`, `references/resources.md`,
`references/learning-record.md`, and `references/glossary.md`.

The adapted workflow requires an exact user-approved teaching directory before
any write and confines every artifact to that root. Automatic browser opening
and automatic community delegation were removed. Source-backed claims require
citations, and the workflow grants no install, Git, publication, private-data,
or external-system authority.

Updates are manual. Fetch the pinned upstream directory and repository license
into a temporary location, review every file and the complete diff, recompute
all digests, confirm the local rename and coexistence with `teach`, and rerun the
repository's focused and full checks before changing this copy.
