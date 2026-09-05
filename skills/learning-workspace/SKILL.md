---
name: learning-workspace
description: Explicitly create and maintain a source-backed teaching workspace for sustained learning across sessions. Use only when the user directly invokes learning-workspace; do not select for a one-off code explanation or ordinary teaching conversation.
---

# Learning workspace

Build a stateful teaching workspace around one user-owned learning mission. This
skill is distinct from `teach`, which provides a conversational code or design
lesson without creating a workspace. Use `how` for a standalone code-flow
explanation.

## Require an approved directory before writes

Ask the user to name an exact teaching directory and explicitly approve it for
this workspace. Do not create or edit any file before that approval. An explicit
invocation of this skill alone is not directory approval.

After approval, resolve the workspace root. Before every write, confirm the
target remains inside that root and does not escape through a symlink or parent
path. Keep all missions, resources, lessons, references, assets, notes,
glossaries, and learning records inside the approved teaching workspace.

This skill grants no authority to install dependencies, open a browser, contact
or delegate to a community, change another repository, use private data, perform
Git actions, publish, or mutate an external system. Any such action needs
separate authority from the underlying request.

## Establish the mission

Read existing workspace records before proposing changes. If the mission is
missing or unclear, interview the user about the real-world outcome, observable
success, constraints, and exclusions. Read [the mission reference](references/mission.md)
only when creating or revising `MISSION.md`. Confirm a mission change before
writing it.

Keep one mission per workspace. If the user wants unrelated outcomes, propose a
separate approved directory rather than mixing their records.

## Ground teaching in trusted sources

Prefer primary sources, peer-reviewed work, official documentation, recognized
experts with cited evidence, and other sources whose authority is clear. Read
[the resources reference](references/resources.md) when creating or curating
`RESOURCES.md`.

Cite material claims in lessons and reference documents. Distinguish sourced
fact, inference, disagreement, and evidence gaps. Do not rely on uncited model
memory for claims that guide instruction.

Do not automatically delegate questions to communities or contact anyone. The
user decides whether to consult a community or practitioner.

## Teach within the learner's current range

Use the mission, prior records, demonstrated knowledge, and user preferences to
choose one tightly scoped lesson. Teach only the knowledge needed for one
tangible outcome, then use retrieval, practice, or another feedback loop to
test use rather than exposure.

Store lessons under `lessons/` and reusable lesson assets under `assets/` only
inside the approved root. Prefer self-contained, accessible artifacts that the
user can reopen. Do not open a lesson automatically. Give the user the path and
run instructions instead.

Store durable quick-reference material under `reference/`. Read existing assets
and references before adding another copy of the same material.

## Record demonstrated learning

Read [the learning-record reference](references/learning-record.md) only when
the user demonstrates durable understanding, states relevant prior knowledge,
corrects a misconception, or changes the mission. Do not record mere coverage
or produce a session activity log.

Read [the glossary reference](references/glossary.md) only when a term has been
understood well enough to define or revise in `GLOSSARY.md`. Use the glossary's
accepted vocabulary in later lessons and records.

Use `NOTES.md` only for approved teaching preferences or working constraints
that future sessions need. Do not store secrets or unrelated personal data.

## Return verified workspace state

Report the approved root, files read or changed, lesson outcome, cited sources,
evidence of understanding, unresolved gaps, and suggested next lesson. Do not
claim learning from exposure alone.

Apply the `unslop` skill to human-facing lessons and summaries without changing
citations, accepted terminology, evidence, exercises, or authority boundaries.
