# Writing portable skills

Use this reference when the target document is a skill. Follow the target
repository's format and host adapters before this general guidance.

## Keep shared instructions portable

Put the skill's purpose, trigger, workflow, and cross-host constraints in the
portable entrypoint. Move host-specific UI, invocation, and tool configuration
to the adapter the target repository defines. Do not copy a field from Cursor,
Codex, or Claude into shared frontmatter unless every target host supports it.

In this repository, `SKILL.md` frontmatter contains only non-empty `name` and
`description`. Codex invocation policy belongs in `agents/openai.yaml`.

## Choose invocation policy

Choose automatic discovery when the agent must select the skill from ordinary
requests or another workflow depends on it. Write a discriminating description
that states the capability and distinct trigger branches.

Choose explicit-only invocation when the user must deliberately request the
workflow. Keep the portable description explicit about that boundary and set
the target host's adapter policy. In this repository, Codex uses:

```yaml
policy:
  allow_implicit_invocation: false
```

Do not assume an explicit-only skill can or cannot be composed by another skill
without checking the target host's current mechanics.

## Design the entrypoint

Keep always-needed purpose, constraints, and routing in `SKILL.md`. Move large
mode-specific procedures, schemas, and examples to references. Every reference
must have a pointer that says when to read it.

Do not create empty resource directories, duplicated quick-reference files, a
per-skill README, or scripts that the workflow never uses. Treat scripts and
tool dependencies as security-sensitive code.

## Use router skills carefully

A router is useful when several distinct workflows share one discovery point.
It should map real request branches to focused skills or references. Do not add
a router merely to list packages, and do not assume it can invoke explicit-only
skills on every host.

## Validate behavior

Validate frontmatter and file structure with the target repository's canonical
checks. Then run realistic requests for each trigger branch and at least one
near-miss that should not select the skill. Confirm that references load only
when their branches apply and that the skill does not broaden the user's scope
or authority.
