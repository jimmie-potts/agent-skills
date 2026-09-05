# Domain vocabulary and context records

Use this reference only while defining or revising domain vocabulary or a
context map. Follow the repository's existing format when one exists.

## Find the owning vocabulary source

Search before proposing a destination. A repository may use a root glossary,
bounded-context files, schema documentation, a domain package, generated API
contracts, or another convention. Treat `CONTEXT.md` and `CONTEXT-MAP.md` as
possible names, not mandatory locations.

When several sources define the same term, identify the owning source from
repository instructions, generators, imports, or usage. If ownership remains
unclear, report the ambiguity and do not create another competing glossary.

## Keep vocabulary separate from behavior

A context record defines what a domain term means and how it differs from
nearby concepts. It may name ownership and relationships needed to distinguish
concepts. It must not become an API contract, workflow specification,
acceptance-criteria list, implementation plan, or scratchpad.

Use a compact entry when the repository has no established format:

```markdown
**Canonical term**

One or two sentences that distinguish the concept in this domain.

Avoid: ambiguous alias, misleading alias
```

Add only terms specific to the domain. General programming terms do not belong
unless this repository gives them a specialized domain meaning.

## Map multiple contexts only when evidence supports them

Use a context map when the repository already distinguishes multiple domain
contexts or the user accepts that model. Name each context, its vocabulary
source, the domain concepts it owns, and evidence-backed relationships with
other contexts. Do not invent context boundaries from directory names alone.

Propose new files lazily, after the first accepted term or relationship needs a
durable home and the repository has no authoritative destination.
