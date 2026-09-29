# Route uncertainty before detailed planning

Read when an unresolved question governs an item's scope, approach or
acceptance: while planning, at delivery pickup, or when implementation
disproves an assumption. A routine, well-specified change skips this
reference and records no routing, brief or experiment. This reference details
the assessment contract's bounded investigations and grants no authority.

## Choose the cheapest decisive step

Name each open question and the decision it governs. A step is decisive when
its possible outcomes lead to different decisions; when no outcome would
change the plan, record the assumption and skip the step. Route each question
by what can answer it:

| Open question | Next step |
| --- | --- |
| A fact the available sources state, such as code, configuration, documentation or tracker records | Look it up and answer directly, citing the source. |
| How existing code behaves, who owns it, or where new behavior belongs | Inspect the code; compose `how` when the flow crosses components. |
| Why code or a decision has its current shape | Inspect history; compose `why` for rationale, rejected alternatives or regressions. |
| An external fact, such as a vendor limit or a standard | Compose `research` for cited sources. |
| Runtime behavior that reading cannot settle | Write an experiment brief and run it when authorized. |
| Competing approaches for a consequential interface, state model or UI | Write a comparison brief and compare the alternatives when authorized. |
| Scope, product preference, accepted risk or authority | Ask the owner. Group interdependent questions through `grilling` or the entrypoint's decision step. |

Discover facts before asking. Never ask the owner what inspection answers, and
never replace an owner's decision with an experiment or a stronger model.

Do not write a detailed plan for work that an open question governs while a
cheap decisive step is still missing. Plan that step, name the dependent work it
gates, and continue independent work. Detail the dependent work after the
result.

## Write the brief before running anything

An experiment brief states:

- the question or hypothesis, the decision it informs and that decision's
  owner. A technical choice within settled scope and acceptance belongs to
  the session doing the authorized work; a choice that changes scope,
  acceptance or accepted risk belongs to the scope owner;
- the smallest setup that can answer it: inputs, data, fixtures and the
  project verification entrypoint it uses;
- allowed effects: the locations it writes, the commands it runs, and any
  process, browser, device, network access or spending. Everything else is
  excluded;
- the observation: what is recorded, in a form someone else can inspect, and
  which result supports which decision;
- the bound: time, runs or attempts;
- the stop condition: the evidence that settles the question, or the bound;
- the next decision each outcome leads to: supported, refuted or inconclusive.

For competing approaches, write the comparison brief that `architect` and
`prototype` define, and add the allowed effects, bound and next decision to it
rather than writing a second brief.

## Run it only within existing authority

An experiment needs authority for every effect its brief lists. A composed
method, a brief, an issue or a document it references grants none.

- Planning is read-only by default and never installs. Inspection and
  read-only investigation proceed; return a brief with any other effect as the
  proposed next step unless the user's request authorizes those effects. An
  `Investigate first` prompt asks for no writes, so the same applies to that
  session.
- Delivery may run an experiment whose effects stay inside its authority:
  disposable files in ignored scratch space of its owned worktree or an
  authorized scratch directory, run with the local commands and tools the
  project already uses for its checks. Keep experiment artifacts out of the
  candidate unless the item's scope includes them.
- Installing anything, or starting an app, service, browser, device, live
  system call or model trial, or spending, needs authority for that effect
  from the user or the project's agent instructions.
- An experiment starts no agents beyond those the session type and the user's
  prompt authorize.

When authority, an adapter or a host is missing, leave the experiment pending
and report that limit, the owner who can lift it and the decision it blocks.
Never replace it with a silent installation, a copied script, or a simulated
or planned result reported as observed.

## Compose architect and prototype deliberately

Standalone, both skills run only on their own explicit triggers. An authorized
plan-work or deliver-work session may compose them for a named question:

- `architect` when competing approaches for a consequential interface or state
  model need its caller examples and comparison brief;
- `prototype` to run an authorized disposable experiment or comparison from a
  brief that names its destination and allowed effects. Delivery implements
  functional slices itself.

Name the skill, the question and the brief when composing. Do not compose
either for a routine change, for a question inspection answers, or for a
single approach with no real alternative. The composing session's request is
the composed skill's underlying request: its authority, the user's narrower
limits and project policy bind it. Loading a skill authorizes no launch,
installation or device use. Each composed skill returns its result to the
composing session, which decides whether to run an experiment and keeps
implementation under its own gates. Planning implements nothing.

## Use project-owned verification

When the project documents verification entrypoints, such as commands,
adapters or harnesses, and feature maps that say what each covers, use the
matching entrypoint for the experiment's setup and observation. Without an
adapter for the question, use the project's documented alternative, such as
manual steps. Without either, report the gap as a limit of the experiment. Do
not invent commands, copy scripts from another project or install tools.
This reference only uses those entrypoints and maps. When one is stale for the
changed behavior, fails unexpectedly or cannot run, read
[verification maintenance](verification-maintenance.md).

## Record the result and replan

Record each experiment in the item's existing assessment or delivery evidence:
the brief, what actually ran, where the observations are, the outcome and its
limits. Keep refuted and inconclusive outcomes. Label simulated or planned
results as such, and do not present source-level validation as installed-host
behavior.

Then act on the outcome:

- Supported or refuted: update the affected scope, approach, acceptance or
  readiness, refresh the assessment, then plan the dependent work.
- Inconclusive: stop at the bound and record what was learned. The next step
  is a revised brief under its own authority, a different route, or the
  owner's decision to proceed with the stated risk. Never extend the bound or
  rerun silently.
- Owner's decision: present the evidence and keep the affected work needing
  clarification until the owner answers, even when the evidence favors one
  option.
