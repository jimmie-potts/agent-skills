# Domain modeling provenance

- Upstream repository: `https://github.com/mattpocock/skills`
- Upstream path: `skills/engineering/domain-modeling/`
- Pinned source revision: `49dd158d1076134a641b33efb035946536778336`
- Retrieved: `2026-10-17`
- Upstream source SHA-256 digests:
  - `ADR-FORMAT.md`: `944c92aa790e8fbdc9199640b170979abb8a34ba8d0fe18c2a01a63bce140ca0`
  - `GLOSSARY-FORMAT.md`: `21dcc40cdec8e151a829b98ab1517c1867bc444e3665134a98c6983411996801`
  - `SKILL.md`: `7b925d7b1e341a2eeae33ad68a8a8c0ab889a38ddd22a7598e4c240e5a7556a3`
  - `agents/openai.yaml`: `f6bf2aa996c6e6f53fdd0708e18a0d16a56aed8322cca59fedbe3c0d2c75f06b`
  - Repository `LICENSE`: `0e7ac423bf2c6e223b7c5b156f8cf72da49d748e56a1641402c31f22ad07dbb5`
- License: MIT, Copyright (c) 2026 Matt Pocock; preserved in `LICENSE`

## Local adaptations

The local version preserves active vocabulary work, term challenges, concrete
scenarios, comparison with code, context mapping, and durable decision records.
It treats `GLOSSARY.md` (upstream's rename of `CONTEXT.md`, which it still
recognizes) as vocabulary only and discovers the repository's actual
vocabulary owners and decision paths instead of assuming root files or
`docs/adr/`.

The upstream context and ADR formats were adapted into
`references/context.md` and `references/decision-record-format.md`. Both defer
to repository conventions. The workflow proposes exact edits by default and
writes only when the underlying request authorizes those destinations. It does
not acquire tracker, OPSX, delivery, implementation, Git, or publication
authority.

The shared adaptation uses repository-defined scope and delivery owners.

Updates are manual. Fetch the pinned upstream directory and repository license
into a temporary location, review every file and the complete diff, recompute
all digests, and rerun the repository's focused and full checks before changing
this copy.
