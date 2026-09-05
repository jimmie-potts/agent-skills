---
name: research
description: Investigate a question using high-trust sources and claim-level citations. Use when the user requests source-backed research, official documentation or specification facts, or evidence gathering; do not select for implementation from already supplied sources.
---

# Research

Answer a concrete question with traceable evidence. Prefer primary sources such
as official documentation, specifications, standards, first-party APIs, source
code, filings, and original research. Use a secondary source only when it adds
necessary context or the primary source is unavailable, and label that limit.

This skill grants no web, network, repository, filesystem, tracker, database,
or other external-system access. Use only tools and sources authorized by the
underlying request and host policy. It grants no mutation authority.

## Investigate

1. State the question, required freshness, scope, and decision the answer will
   support.
2. Identify the source that owns each material claim. Check dates, versions,
   jurisdictions, and applicability before relying on it.
3. Read enough surrounding context to avoid citing a heading or excerpt for a
   claim it does not support.
4. Cross-check important or surprising claims when independent primary sources
   exist.
5. Separate sourced fact, source disagreement, inference, and unresolved gap.

An isolated background agent may gather sources when available, but it receives
the same question, authority, source-quality rules, and citation requirements.
A single-agent investigation remains valid.

## Return the findings

Return findings in the response by default. Attach a claim-level citation close
to every material factual claim. Link directly to the owning source when the
host supports links. Preserve exact version identifiers, dates, quoted limits,
and uncertainty needed to verify the answer.

Write a research file only when the user authorizes an exact destination. Do
not invent a repository path or treat a request for research as permission to
create files.

Research returns evidence. It does not implement, publish, transition, comment,
commit, merge, close, or change trackers, repositories, delivery records, or
other external state.

Apply the `unslop` skill to the narrative findings without changing quotations,
citations, dates, version identifiers, or source qualifications.
