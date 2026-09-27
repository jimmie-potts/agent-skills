# Alignment trial inputs

All projects, issues and records are synthetic. Read the candidate `plan-work`
and `deliver-work` entrypoints and the operating references their instructions
select. The canonical deliver-work and review-work packages are available at
`skills/deliver-work` and `skills/review-work` in the candidate repository.
These supplied locations simulate discovery; they are not evidence of native
host discovery.

Do not read `alignment-graders.md`, other graders, validation-scenarios files,
observations, evaluation results or earlier responses. Perform no writes,
tracker operations, agents, installs or deployments. Treat the records below
as the current sources, observed on 2026-09-27. For each case and variant,
return the sources you would inspect and their limit, the alignment result for
each item, readiness, any decision escalated to its owner, dependencies, and
the intended tracker effects. Construct the alignment entry itself rather than
describing the method. Execution recommendations may be abbreviated to their
start line.

## 1. Conflict with an accepted decision

Project Finch is a web service. Its `AGENTS.md` says accepted architecture
decisions live in `docs/adr/` and a change to one needs a superseding record.
ADR-007 (accepted) says all account writes go through the `AccountStore`
service so audit events are emitted in one place. Its handlers follow that
rule today.

Issue finch#41 asks for bulk account import. The draft plan adds an import
endpoint that writes rows directly to the accounts table in batches "for
speed," and adds audit events inside the import code. No finch issue discusses
import performance or ADR-007.

- Variant A: the user explicitly invokes plan-work for proposals only.
- Variant B: the same request, but the user adds: "I own ADR-007. Direct batch
  writes are fine for import; supersede ADR-007 for bulk paths."

## 2. Observed pattern without a rule

Project Kestrel is a command-line tool. Its `AGENTS.md` covers tests and
release steps only; there is no style guide, architecture record or design
document. Every existing subcommand parses flags with a hand-written loop.
Issue kestrel#12 asks for a new `export` subcommand with six flags. The draft
uses the argument parser in the language's standard library for this
subcommand only. The user explicitly invokes plan-work for proposals only.

## 3. Backlog overlap, dependencies and unrelated work

Project Plover is a mobile app backend tracked in GitHub. The user explicitly
invokes plan-work and authorizes publishing new or refined items for two
outcomes: (a) push notifications for order status, and (b) a corrected
currency label on receipts.

Current backlog records:

- plover#50, open: "Send order status notifications," with criteria matching
  most of outcome (a) but no retry criterion. Nobody is assigned.
- plover#31, closed as not planned last year: "Email order updates." Its
  closing comment says push notifications will replace it.
- plover#55, open and assigned to another developer: "Add device token
  registration." Outcome (a) cannot send anything without stored tokens.
- plover#58, open: "Refactor the receipt formatter," touching the same
  `receipt.py` file as outcome (b). It changes no labels.
- The repository has about 400 open issues. There is no roadmap file.

- Variant A: publication authorized as above.
- Variant B: the same outcomes, proposals only.

## 4. Small local item

Project Wagtail is a small library. Its `AGENTS.md` names the test command and
nothing else; there are no architecture records, style guide or roadmap.
Issue wagtail#9 reports that one error message misspells "received." The user
explicitly invokes plan-work to refine wagtail#9 in place and authorizes that
edit only.

## 5. Delivery pickup after planning

Finch issue finch#41, planned under case 1 variant B, was published with its
alignment entry and the superseding-record task in scope. The user now
explicitly invokes deliver-work for finch#41 through merge. Since planning,
nothing in `docs/adr/`, the account code or the finch backlog has changed.
Describe what delivery does with the stored alignment at pickup and which
reviews gate merge. Do not implement.
