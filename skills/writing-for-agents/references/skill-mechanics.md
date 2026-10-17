# Writing portable skills

Follow the target repository's format first. In this repository, `SKILL.md`
frontmatter holds only `name` and `description`, and Codex invocation policy
lives in `agents/openai.yaml`:

| Invocation | When | Adapter |
| --- | --- | --- |
| Automatic | The agent must pick the skill from ordinary requests, or another workflow depends on it | `allow_implicit_invocation: true` and a description that names each trigger branch |
| Explicit-only | The user must request the workflow deliberately | `allow_implicit_invocation: false` and a description that says so |

Keep purpose, triggers and routing in `SKILL.md`; move large mode-specific
procedures to references, each with a pointer that says when to read it. Don't
add empty directories, per-skill READMEs or unused scripts. Validate with the
repository's checks, then try one request per trigger and one near miss.
