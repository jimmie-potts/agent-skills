# Define tasks and dispatch ready work

Read before decomposing delivery work, ordering tasks, dispatching workers or
accepting their artifacts. Planning consumers use the definition, boundary and
dependency sections to propose work; they do not dispatch implementation.
Reading this reference grants no implementation, delegation, publication or
other effect authority. Preserve the composing workflow's existing gates.

## Define tasks in existing evidence

Use the existing [task packet](resumption.md) or authorized work record, without
a new required format, runtime, manifest or ledger. For each substantial task,
compactly record:

- identifier, observable outcome, exclusions and authoritative scope references;
- covered acceptance criteria and planned evidence for each;
- required decisions, artifacts and interface contracts, naming their producer
  and available identity/version or the unresolved input;
- affected interfaces and data/control paths, shared state, files, test resources
  and the boundary at which the result will be integrated and verified;
- task and artifact ownership, separating proposed work from the coordinator's
  permitted writes and other effects;
- expected artifact and the evidence required to accept it.

Planning records proposed inputs, owners or roles and verification. Do not
pretend a prerequisite has been accepted or a future check has passed. Refresh
source revisions, input versions, ownership and available evidence at dispatch.

Map every agreed criterion to a task and planned verification, and every task
to authorized scope or an explicit necessary supporting step. State why a
supporting step is needed and how its completion will be observed. Resolve
uncovered criteria and out-of-scope tasks before dependent dispatch; continue
unaffected ready work. Preserve failure, recovery, security, authorization,
compatibility and user-journey cases. Use inspection, simulation or readback for
claims that executable tests cannot establish, including documentation-only changes.

Accept a task only when its artifact matches current inputs and contracts,
stays within scope and ownership, and has the evidence for its criteria. A
checked box, producer claim or clean patch application is insufficient.

## Choose useful verification boundaries

Prefer a complete, narrow behavior that can be verified on its own. Layer-only
chores need an explicit integration task and acceptance boundary; do not present
them as independently delivered behavior. Batch small same-shape mechanical
changes under one bounded rule and verification method. Preserve direct
coordinator implementation when decomposition adds no useful boundary, including
trivial edits.

When a broad shared-contract change cannot land as independent behavior slices,
name an expand, migrate, contract sequence and the inputs/evidence between phases:

1. Expand supports the transition while verifying existing consumers.
2. Migrate moves bounded consumer/data groups, verifying changed behavior and
   old/new compatibility at each supported boundary.
3. Contract removes the old form only after all required migrations and
   remaining-consumer checks are accepted, then verifies the final behavior.

If intermediate batches cannot pass independently, keep the dependent sequence
in the authorized isolated candidate and name the final integration task as the
passing boundary. Retain useful intermediate checks, but do not claim each batch
can land independently or waive final checks. Internal tasks do not require
separate PRs, branches or tickets.

## Distinguish dependency meanings

Record each applicable relationship and its reason:

| Relationship | Meaning and consequence |
| --- | --- |
| Required input | The consumer's brief, correctness or acceptance needs a producer's decision, artifact, data or interface. Dependent work waits for that input and its required evidence. |
| Shared-file coordination | Work may overlap a file or mutable location without consuming the other's result. Define ownership and coordinate application; the path alone is not an input dependency. |
| Preferred order | A useful merge, review or integration order where neither task needs the other's output. It does not by itself block readiness or independent proposals. |

An input is available when its named decision/artifact exists at the relevant
identity/version with required acceptance evidence. Tracker state, a checked box
or an earlier place in a list cannot establish this. A verified contract may
unblock consumer proposals while other producer work continues only when those
proposals do not need the unfinished implementation or evidence.

Detect cycles in required inputs. Pause the cycle and consumers of its unresolved
outputs; identify the decision, accepted interface or task regrouping needed to
break it. Do not discard a true edge just to start work. Continue independent
tasks outside the affected graph. Coordination and preferred order do not create
readiness cycles.

## Check independence and capacity before dispatch

Dispatch only work with available required inputs. Different file paths are
insufficient. Check data/control dependencies, shared mutable state, accepted
contracts, test resources and artifact ownership. Parallel read-only questions
or bounded proposals are suitable when they do not consume one another's
unfinished results and those inputs/resources are stable or independently
isolated. Shared ports, databases, fixtures, devices or accounts may require
serialized checks even when proposal work can proceed independently.

Give each worker a bounded artifact and identify who integrates it. A shared
file can support independent read-only questions or proposals; anticipated
overlap requires coordinated integration. Unsettled shared semantics require
an accepted decision before dependent implementation. Continue independent
investigation while that decision is pending.

Use only delegation authorized by the composing request and host rules. Check
current capacity, counting the coordinator and all other active contexts that
occupy the host limit. Queue excess work or handle it directly within existing
ownership; do not duplicate active assignments or evict another owner. When
delegation is unavailable or unauthorized, implement ready work directly unless
an explicit mandatory requirement prevents that fallback. Report that specific
gap and continue independent work without inventing a new approval gate.

The coordinating root owns all durable writes. Workers return proposals or
read-only evidence. Root applies accepted changes serially against current
state, reconciles overlapping edits and renews affected verification. This
integration ownership alone does not serialize independent proposal work.

## Carry decisions and reconcile returns

Brief consumers with the accepted producer decision, interface/artifact reference,
version and relevant evidence, using the existing packet rather than session
history. At return, compare task/attempt identity, source revision, producer
inputs, contracts, ownership, artifact and validation under
[resumption](resumption.md).

A changed producer input requires reassessing its consumers, even with disjoint
files or a cleanly applicable patch. Preserve the original return and attempt;
reconcile or rework against current inputs before integration, then renew the
affected acceptance checks and reviews. Retain unrelated still-current evidence.

Decomposition does not authorize new tickets, linked-issue delivery, framework
installation or agents. Planning-only and tracker-only work stop at their
authorized effects. Task acceptance never replaces whole-change independent
Standards/Specification review, CI, guarded merge or completion conditions.

Design references: [verifiable slices and contract migration](https://github.com/mattpocock/skills/blob/321658273cb1d20b76026717d027d505790106d4/skills/engineering/to-tickets/SKILL.md),
[requirements/task coverage](https://github.com/github/spec-kit/blob/b60057692cd726ea56331ec47f9ebc3e8877d8f7/templates/commands/analyze.md).
These inform the definitions; their frameworks, commands, publication rules and
tracker conventions are not adopted.
