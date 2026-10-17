# Third-party skill provenance

## `grill-with-docs`

- Canonical path: [`skills/grill-with-docs/`](skills/grill-with-docs/SKILL.md)
- Original repository: `https://github.com/mattpocock/skills`
- Original path: `skills/engineering/grill-with-docs/`
- Pinned Git commit: `5b15a47f2d7150f545fbcacbfe381787fc0230dc`
- License: [MIT](skills/grill-with-docs/LICENSE), Copyright (c) 2026 Matt Pocock
- Detailed source record: [`skills/grill-with-docs/SOURCE.md`](skills/grill-with-docs/SOURCE.md)

## `grilling`

- Canonical path: [`skills/grilling/`](skills/grilling/SKILL.md)
- Original repository: `https://github.com/mattpocock/skills`
- Original path: `skills/productivity/grilling/`
- Pinned Git commit: `5b15a47f2d7150f545fbcacbfe381787fc0230dc`
- License: [MIT](skills/grilling/LICENSE), Copyright (c) 2026 Matt Pocock
- Detailed source record: [`skills/grilling/SOURCE.md`](skills/grilling/SOURCE.md)

## `domain-modeling`

- Canonical path: [`skills/domain-modeling/`](skills/domain-modeling/SKILL.md)
- Original repository: `https://github.com/mattpocock/skills`
- Original path: `skills/engineering/domain-modeling/`
- Pinned Git commit: `49dd158d1076134a641b33efb035946536778336`
- License: [MIT](skills/domain-modeling/LICENSE), Copyright (c) 2026 Matt Pocock
- Detailed source record: [`skills/domain-modeling/SOURCE.md`](skills/domain-modeling/SOURCE.md)

## `code-review`

- Canonical path: [`skills/code-review/`](skills/code-review/SKILL.md)
- Original repository: `https://github.com/mattpocock/skills`
- Original path: `skills/engineering/code-review/`
- Pinned Git commit: `5b15a47f2d7150f545fbcacbfe381787fc0230dc`
- License: [MIT](skills/code-review/LICENSE), Copyright (c) 2026 Matt Pocock
- Detailed source record: [`skills/code-review/SOURCE.md`](skills/code-review/SOURCE.md)

## OpenSpec core workflows

The six `skills/openspec-*/` directories derive from the core Codex generator
in `@fission-ai/openspec` version `1.12.0`, sourced from
[OpenSpec v1.12.0](https://github.com/Fission-AI/OpenSpec/tree/v1.12.0).
Each directory includes its generated source digest in `SOURCE.md`, an MIT
license with OpenSpec contributor attribution, and the portable local
adaptations. Updates are reviewed in this shared catalog.

## `writing-for-agents`

- Canonical path: [`skills/writing-for-agents/`](skills/writing-for-agents/SKILL.md)
- Original repository: `https://github.com/mattpocock/skills`
- Original path: `skills/productivity/writing-for-agents/`
- Pinned Git commit: `5b15a47f2d7150f545fbcacbfe381787fc0230dc`
- License: [MIT](skills/writing-for-agents/LICENSE), Copyright (c) 2026 Matt Pocock
- Detailed source record: [`skills/writing-for-agents/SOURCE.md`](skills/writing-for-agents/SOURCE.md)

## `diagnosing-bugs`

- Canonical path: [`skills/diagnosing-bugs/`](skills/diagnosing-bugs/SKILL.md)
- Original repository: `https://github.com/mattpocock/skills`
- Original path: `skills/engineering/diagnosing-bugs/`
- Pinned Git commit: `5b15a47f2d7150f545fbcacbfe381787fc0230dc`
- License: [MIT](skills/diagnosing-bugs/LICENSE), Copyright (c) 2026 Matt Pocock
- Detailed source record: [`skills/diagnosing-bugs/SOURCE.md`](skills/diagnosing-bugs/SOURCE.md)

## `codebase-design`

- Canonical path: [`skills/codebase-design/`](skills/codebase-design/SKILL.md)
- Original repository: `https://github.com/mattpocock/skills`
- Original path: `skills/engineering/codebase-design/`
- Pinned Git commit: `5b15a47f2d7150f545fbcacbfe381787fc0230dc`
- License: [MIT](skills/codebase-design/LICENSE), Copyright (c) 2026 Matt Pocock
- Detailed source record: [`skills/codebase-design/SOURCE.md`](skills/codebase-design/SOURCE.md)

## `research`

- Canonical path: [`skills/research/`](skills/research/SKILL.md)
- Original repository: `https://github.com/mattpocock/skills`
- Original path: `skills/engineering/research/`
- Pinned Git commit: `5b15a47f2d7150f545fbcacbfe381787fc0230dc`
- License: [MIT](skills/research/LICENSE), Copyright (c) 2026 Matt Pocock
- Detailed source record: [`skills/research/SOURCE.md`](skills/research/SOURCE.md)

## `prototype`

- Canonical path: [`skills/prototype/`](skills/prototype/SKILL.md)
- Original repository: `https://github.com/mattpocock/skills`
- Original path: `skills/engineering/prototype/`
- Pinned Git commit: `5b15a47f2d7150f545fbcacbfe381787fc0230dc`
- License: [MIT](skills/prototype/LICENSE), Copyright (c) 2026 Matt Pocock
- Detailed source record: [`skills/prototype/SOURCE.md`](skills/prototype/SOURCE.md)

## `handoff`

- Canonical path: [`skills/handoff/`](skills/handoff/SKILL.md)
- Original repository: `https://github.com/mattpocock/skills`
- Original path: `skills/productivity/handoff/`
- Pinned Git commit: `5b15a47f2d7150f545fbcacbfe381787fc0230dc`
- License: [MIT](skills/handoff/LICENSE), Copyright (c) 2026 Matt Pocock
- Detailed source record: [`skills/handoff/SOURCE.md`](skills/handoff/SOURCE.md)

## `learning-workspace`

- Canonical path: [`skills/learning-workspace/`](skills/learning-workspace/SKILL.md)
- Original repository: `https://github.com/mattpocock/skills`
- Original path: `skills/productivity/teach/`
- Local rename: upstream `teach` to `learning-workspace`
- Pinned Git commit: `5b15a47f2d7150f545fbcacbfe381787fc0230dc`
- License: [MIT](skills/learning-workspace/LICENSE), Copyright (c) 2026 Matt Pocock
- Detailed source record: [`skills/learning-workspace/SOURCE.md`](skills/learning-workspace/SOURCE.md)

## `deliver-work`

- Canonical path: [`skills/deliver-work/`](skills/deliver-work/SKILL.md)
- Local consolidation of this repository's `deliver-jira-work` and
  `github-delivery` at commit `aed5f28c96c90430256abdc1790b520ebb34faeb`.
- The former Jira workflow originated in Notification Service and was made
  portable by NS-334 before this consolidation. The former GitHub workflow
  supplied conditional skill composition and the two independent review axes.
- Accepted scope: [agent-skills issue #5](https://github.com/jimmie-potts/agent-skills/issues/5).
- Both retired skill names are replaced without compatibility wrappers. Shared
  composed skills retain their existing provenance and license records.

## `improve-codebase-architecture`

- Canonical path: [`skills/improve-codebase-architecture/`](skills/improve-codebase-architecture/SKILL.md)
- Original repository: `https://github.com/mattpocock/skills`
- Original path: `skills/engineering/improve-codebase-architecture/`
- Pinned Git commit: `3cca18b368ae95cdbdebbff572ccafa662551015`
- License: [MIT](skills/improve-codebase-architecture/LICENSE), Copyright (c) 2026 Matt Pocock
- Detailed source record: [`skills/improve-codebase-architecture/SOURCE.md`](skills/improve-codebase-architecture/SOURCE.md)

## pstack skills

Earlier versions vendored adapted copies of ten pstack skills: `architect`,
`arena`, `blast-radius`, `how`, `interrogate`, `teach`, `tdd`,
`technical-writing`, `unslop` and `why`. They were removed in favor of the
installed [pstack plugin](https://github.com/cursor/plugins/tree/main/pstack),
which now provides those names with upstream behavior.
