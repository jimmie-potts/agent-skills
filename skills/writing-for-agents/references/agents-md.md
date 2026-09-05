# Writing Codex AGENTS.md files

Use this reference for Codex `AGENTS.md` and `AGENTS.override.md`. Other hosts
may use different filenames, search paths, precedence, limits, and override
rules. Verify their documentation separately.

## Discovery and precedence

Codex builds one instruction chain at the start of a run or TUI session:

1. At global scope, Codex reads `AGENTS.override.md` from `CODEX_HOME` when it
   exists; otherwise it reads `AGENTS.md`. It uses the first non-empty file.
2. At project scope, Codex starts at the project root and walks toward the
   launch working directory. In each directory it checks
   `AGENTS.override.md`, then `AGENTS.md`, then configured fallback filenames.
   It includes at most one file from each directory.
3. Codex concatenates the selected files from root to current directory. Rules
   closer to the current directory appear later and take precedence when they
   conflict with broader guidance.
4. Empty files are skipped. The combined project instructions stop at
   `project_doc_max_bytes`, which defaults to 32 KiB.

Place repository-wide rules at the root. Put package, service, or language
specializations in the nearest directory that owns them. State an override or
exception explicitly so a human can understand the same resolution that Codex
will apply.

Codex builds this chain once at launch. A nested `AGENTS.md` does not become
active merely because the agent later edits files below that directory. Start
the run from the relevant directory or launch Codex with that directory as its
working directory. Closer project files can override earlier project guidance,
but they cannot override higher-priority host or user instructions.

`AGENTS.override.md` replaces other instruction files in its directory. It does
not erase instruction files already selected from parent directories. A linked
document is not part of this merge chain; Codex reads it only when an active
instruction tells the agent to do so.

Budget root guidance carefully. A large root file can consume the combined byte
limit before Codex reaches narrower instructions closer to the launch directory.

Official behavior reference: `https://developers.openai.com/codex/guides/agents-md`.

## Decide what stays inline

Keep these rules in the nearest applicable `AGENTS.md`:

- non-obvious authority and safety boundaries;
- the canonical validation command, its working directory, prerequisites, and
  required result;
- repository-specific ownership, dependency, or contract rules that affect
  ordinary changes;
- required evidence or readback before claiming completion;
- explicit exceptions to broader instructions;
- pointers whose conditions name the branches that need deeper guidance.

Move large, branch-specific procedures to maintained references. Keep the
pointer near the step or rule that triggers the read. A pointer should identify
the target's authority. For example, distinguish an accepted ADR from a helpful
background note.

Do not turn `AGENTS.md` into a copy of the repository. Leave dependency lists,
file inventories, command help, generated schemas, and discoverable script
internals in their authoritative files unless lookup is unreliable or the
instruction depends on one exact value.

## Separate policy from authorization

An `AGENTS.md` rule constrains work that another instruction has authorized. It
does not independently authorize filesystem writes, dependency installation,
network access, destructive commands, publication, deployment, or external
mutations.

Write risky workflows in two parts:

1. State the safe default or required action.
2. State the forbidden boundary and the additional authority needed to cross
   it.

Example:

> Run `npm run generate` to update generated files. Do not edit generated files
> directly.

Do not use broad phrases such as "complete the workflow" when the workflow can
publish, deploy, delete, or contact people. Name the terminal state and every
external effect the task must authorize.

## Write canonical checks

A reliable gate usually needs:

- the exact command;
- the directory where it runs;
- one-time prerequisites that are not safely automatic;
- the file or change categories that trigger it;
- the expected exit state or readback;
- the fallback report when the environment cannot run it.

Do not require dependency installation merely because a check is named. Keep
setup separate from validation so the user or host approval policy can govern
it.

## Verify the instruction chain

When the Codex CLI is available and the task permits validation, inspect the
instruction behavior from the repository root and relevant nested directories.
Useful read-only prompts include:

```bash
codex --ask-for-approval never "Summarize the current instructions."
codex --cd path/to/subdir --ask-for-approval never "List the instruction files that apply here."
```

Confirm that:

- Codex reports the intended global, root, and nested sources;
- nested rules override only their intended scope;
- required references are read for their named branches;
- canonical checks and completion evidence survive summarization;
- authority boundaries hold on realistic tasks;
- the combined instructions remain below the configured byte limit.

The model's summary is useful compliance evidence, not authoritative discovery
evidence. When exact loaded sources matter, inspect the plaintext TUI log or the
session JSONL if logging is enabled. Test each supported launch directory in a
fresh process.

Codex rebuilds the chain at the start of each run or TUI session. Restart before
judging an instruction change in an existing session.

## Review checklist

- Does every rule belong at this directory scope?
- Is any conflict with a parent rule explicit?
- Does each pointer say what to read and when?
- Are canonical commands exact and safely authorized?
- Can the agent prove completion from named evidence?
- Are hard prohibitions paired with a safe path when one exists?
- Is branch-specific reference material outside the always-loaded file?
- Did a representative root and nested task exercise the behavior?
