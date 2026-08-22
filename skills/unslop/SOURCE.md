# Unslop provenance

- Upstream repository: `https://github.com/cursor/plugins`
- Upstream plugin and path: `pstack/skills/unslop/SKILL.md`
- User-supplied source: `https://github.com/cursor/plugins/blob/main/pstack/skills/unslop/SKILL.md`
- Pinned source revision: `99559f2f52047978602ef365589275831e76af07`
- Retrieved: `2026-08-22`
- Upstream `SKILL.md` SHA-256: `181883e539caec8258ec9129e3ba5f133409144a2cbf2aa361158ab94cfc3441`
- Preserved upstream guidance SHA-256: `adb1181a76a249518ab62b1521ee673520535472b2f3380e03fc3a9a72a7fc9c`
- License: MIT, Copyright (c) 2026 Lauren Tan; preserved in `LICENSE`

## Local adaptations

The original notification-service integration under NS-258 replaced the
upstream unsafe “must always apply” description, added the repository safety
boundary before the byte-preserved editing guidance, and supplied Codex
metadata. Those safeguards remain intact.

The canonical catalog broadens only the trigger policy: the portable description
matches drafting or material edits to agent-authored narrative prose, and Codex
metadata permits implicit invocation. Repository and user instructions still
take precedence, authoritative content remains protected, and the skill grants
no mutation or browsing authority. Local installation is handled by the
catalog's management script rather than by a project-specific copy or shim.

Updates are manual. Fetch the pinned upstream source into a temporary directory,
review its license and complete diff, recompute both digests, and rerun the
focused and canonical offline checks before changing this copy.
