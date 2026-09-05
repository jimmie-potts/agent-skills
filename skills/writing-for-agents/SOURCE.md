# Writing for agents provenance

- Upstream repository: `https://github.com/mattpocock/skills`
- Upstream path: `skills/productivity/writing-for-agents/`
- User-supplied source: `https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-for-agents/SKILL.md`
- Pinned source revision: `5b15a47f2d7150f545fbcacbfe381787fc0230dc`
- Retrieved: `2026-08-23`
- Upstream source SHA-256 digests:
  - `SKILL.md`: `551adca942227b44192edba88acd4e8db911f0121ce58ad16944ccf6a896a74a`
  - `SKILL-MECHANICS.md`: `c768e6307c7c10728c401c213f2c4ba71c542127eeb7ad2956aabd15a0fa0059`
  - `agents/openai.yaml`: `eacb24b2a618cfb81dacb0416f4fdd75ddf3a8060f8ddb99aae1b1e301907e4b`
  - Repository `LICENSE`: `0e7ac423bf2c6e223b7c5b156f8cf72da49d748e56a1641402c31f22ad07dbb5`
- License: MIT, Copyright (c) 2026 Matt Pocock; preserved in `LICENSE`

## Secondary source for Codex mechanics

- Official documentation: `https://developers.openai.com/codex/guides/agents-md`
- Retrieved: `2026-08-23`
- Markdown SHA-256: `9d1f87a2d1cb55b4782b95abe710692b35b9659789c2db31a22c7074a3383e8e`

## Local adaptations

The local version keeps the upstream context-pointer, information-hierarchy,
progressive-disclosure, co-location, completion-criterion, single-source, and
pruning guidance. It changes the opening claim to distinguish shared writing
principles from host-specific discovery, precedence, invocation, and limits.

`references/agents-md.md` adds Codex instruction discovery, directory scope,
override precedence, the default byte limit, authority boundaries, canonical
gate guidance, and behavioral verification. `references/skill-mechanics.md`
replaces Cursor-only invocation fields with portable rules and this repository's
Codex adapter.

The local trigger is narrower than the upstream body's claim about every
agent-consumed document. It covers Agent Skills, persistent coding-agent
instructions, and their conditional references. Ordinary READMEs, tickets,
specifications, and human prose remain outside this skill.

Leading words are now optional shorthand rather than a primary technique.
Negation guidance preserves hard safety prohibitions and pairs them with a safe
path. Exact canonical gates remain in agent instructions when reliable
completion depends on them, even when a script name is discoverable elsewhere.

Updates are manual. Fetch the pinned upstream directory and official Codex
Markdown into a temporary location, review the full diffs and license,
recompute every digest, and rerun all checks before changing this copy.
