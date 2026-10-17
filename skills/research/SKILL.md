---
name: research
description: Investigate a question using high-trust sources and claim-level citations. Use when the user requests source-backed research, official documentation or specification facts, or evidence gathering; do not select for implementation from already supplied sources.
---

# Research

Answer the question from primary sources: official docs, specs, standards,
first-party APIs and source code. Follow every claim back to the source that
owns it, and check its version and date. Label any secondary source and why it
was needed.

A background agent may do the reading when one is available.

Return the findings in the response with a citation next to each material claim,
and keep fact, inference and open gaps distinct. Write a file only when the user
names the destination. Use `unslop` on the narrative when needed.
