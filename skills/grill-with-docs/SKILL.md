---
name: grill-with-docs
description: Explicitly compose grilling with domain-modeling to resolve a plan or design and prepare exact vocabulary or decision-record proposals. Use when explicitly requested by the user or composed by an authorized workflow; do not write during questioning.
---

# Grill with docs

Run `grilling` as the control flow and `domain-modeling` for vocabulary,
concept boundaries and decision records.

While grilling, collect proposed glossary terms and decision records without
writing anything. The repository's glossary is `GLOSSARY.md`; treat a legacy
`CONTEXT.md` as the same vocabulary file when no `GLOSSARY.md` exists. A
glossary holds vocabulary, never behavior.

After the user confirms the decisions, show each exact proposed path and change.
Write them only when the request authorizes those edits; invoking this skill
alone does not. Use `unslop` on questions and proposals when needed.
