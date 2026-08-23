---
name: technical-writing
description: Draft or review technical documentation using a clear document mode, direct developer-focused sentences, limited sentence load, and unambiguous syntax. Use only when the user explicitly invokes technical-writing or asks to apply this writing standard to documentation, RFCs, READMEs, pull-request descriptions, or commit messages.
---

# Technical writing

Write for an engineer who needs to understand the text on the first read. Pick
the document's job, address the reader directly, keep each sentence focused,
and remove constructions that permit two readings.

## Authority and source boundary

This skill grants no authority to edit files, commits, pull requests, tickets,
or external systems. The underlying task must authorize every mutation. Verify
technical claims against the repository and provided sources. Do not invent
commands, symbols, paths, outputs, measurements, or rationale.

Preserve authoritative text, exact quotations, code, schemas, contracts,
acceptance criteria, identifiers, logs, citations, and required terminology.
Apply `$unslop` as the final editorial pass.

## Rules above the method

- Cut words that add no meaning.
- Prefer the short, ordinary word unless a technical term is more precise.
- Use the codebase's real name for every symbol, file, flag, command, and
  component. Do not cycle through synonyms.
- Break a writing rule when following it would make the sentence less accurate
  or harder to read.
- Mix sentence lengths. Keep one thought per sentence, not one rhythm per page.

## Pick one document mode

Choose the mode before drafting. Split and link documents when one file would
otherwise mix incompatible jobs.

- **Tutorial.** Help a learner build something through visible, ordered steps.
  State what they will build and show the expected result after important steps.
- **How-to.** Help a competent reader complete a specific task. Keep background
  brief and put conditions before the steps they govern.
- **Reference.** Provide facts for lookup. Mirror the structure of the system
  and state options, limits, defaults, and errors without persuasion.
- **Explanation.** Help the reader understand one bounded topic. Cover context,
  design choices, constraints, alternatives, and evidence-backed rationale.

Pull-request descriptions and commit messages use the sentence rules below but
do not require a document mode.

## Write to the reader

- Use "you" when addressing the reader and present tense for current behavior.
- Name the actor. Write "the compiler validates the schema" when the actor
  matters, not "the schema is validated."
- Write instructions as commands. Put the condition or goal first when it helps
  readers decide whether the instruction applies.
- Put the common case first, followed by exceptions.
- Avoid "please," "simply," "easy," and "quickly" in procedures.
- Use descriptive link text. Do not use "click here."
- Use sentence-case headings. Use numbered lists for sequences and bullets for
  non-sequential sets.
- Use code formatting for code and repository identifiers. Follow the target
  project's convention for UI labels and snippet indentation.

## Limit sentence load

- Put one instruction in each sentence and one main thought in other sentences.
- Split a sentence when clauses force the reader to backtrack. Word counts are
  a warning signal, not a mechanical limit.
- Place warnings and conditions before the action they constrain.
- Keep articles when they prevent ambiguity: "remove the backup file," not
  "remove backup file."
- Give each word one meaning in a procedure. Use one verb for the same action.
- Prefer direct verbs over noun phrases and avoid passive instructions.

## Remove ambiguous syntax

- Place "only" and "not" next to the word they modify.
- Break long noun strings into clauses.
- Make every pronoun point to one clear noun. Repeat the noun when needed.
- Give every clause its own verb.
- Keep structural words such as "that" when they prevent a second reading.
- Make conjunction grouping explicit with "both," "either," or a rewritten
  sentence when necessary.
- Use periods instead of semicolons or dash-based asides.
- Replace slashes with the exact relationship: "a, b, or both."
- Avoid idioms and metaphors that a non-native reader or translator may parse
  literally.

## Review

Check that the document has one job, every instruction has an actor or direct
command, each sentence carries one idea, and every term maps to a real thing.
Verify paths, symbols, commands, counts, and outputs at the current revision.
Include the regeneration command for generated counts or trees.

Return the finished or reviewed prose. When reviewing rather than rewriting,
tie each proposed change to a concrete reader problem and preserve text that is
already clear.
