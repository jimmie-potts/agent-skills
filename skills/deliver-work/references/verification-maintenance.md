# Maintain verification with changed behavior

Read when changed behavior has a project feature map, verification recipe or
maintained check, when a verification fails or cannot run, and before adding a
check for a repeated or observed failure. Planning uses it to propose the
updates and controls as planned evidence. Delivery performs them within its
authority. This reference grants no write, tracker, runtime, device, transcript
or model-call authority and adds no approval or merge gate.

## Use the project's own verification knowledge

A feature map or verification recipe is the owning project's record of how to
reach and inspect a behavior: entrypoints, scenario fixtures, actions,
expected observations and artifact expectations. Find it through the project's
instructions and verification documents, and read it only when the change
touches behavior it covers. Run its commands and steps from the project source
at the current revision. Do not copy app commands, selectors or step names into
this method, a shared brief or another project's documents.

When the project has no feature map, verify with its existing tests and checks.
Create no map, catalog or feature database to fit this method.

## Update only the affected knowledge

When the change alters covered behavior, update only the affected entries in
the same authorized source delivery: entrypoints, fixtures, actions,
observations and artifact expectations. Rename or retire entries for renamed or
removed behavior. Derive each new expectation from the accepted criterion, not
from whatever the product now does. Leave unaffected entries and wording as
they are.

Acceptance criteria and status stay with their owners, such as the issue,
specification or tracker. A map links to them; it does not restate, relax or
decide them. An updated map proves nothing until its checks run. When the map
belongs to a repository or owner outside the authorized scope, report the
needed update to that owner instead of editing it.

## Classify a failed or unavailable verification

Before repairing, classify the result from evidence:

| Class | Supporting evidence | Next action |
| --- | --- | --- |
| `product` | A working harness, or independent evidence such as a unit test or log, shows the behavior misses its criterion | Fix the product within scope and rerun. Never change the check or recipe to make it pass |
| `harness` | The driver, fixture, tool or check is broken or lacks a needed capability while product evidence is sound | Report the missing capability. Repair it only when the task owns the harness, otherwise route it to its owner. The criterion stays unverified |
| `stale-instructions` | The map, recipe or check describes behavior that an accepted change deliberately altered | Update the affected entry from the accepted criterion and rerun the check. When an earlier change caused it, repair it here only when it blocks this delivery's verification; otherwise route it to its owner |
| `environment` | A needed host, browser build, service, device or credential is unavailable | Report the missing piece and its owner. The result is unavailable, neither passed nor failed; do not switch environments silently |
| `acceptance` | Checks pass but do not establish an accepted criterion, such as a required physical, human or uncovered scenario check | Keep the criterion pending with its owner. Do not report it accepted or complete |

When the evidence does not separate two classes, record the candidate classes
and the evidence that would separate them, and obtain it before choosing a
repair. Do not choose the class that makes the result look better or retry
until green. When a classified blocker survives correction, apply
[corrections](corrections.md).

## Choose negative controls by risk

Changed behavior is high value when it involves authorization, destructive or
device effects, data integrity, a criterion the owner marked important, or a
new or changed check that could pass vacuously. For such behavior, show that
the check can fail. Run it against a known bad result, such as the pre-change
behavior, a deliberately broken fixture or the evidenced bad revision: the
check must fail for the expected reason. Run it against the correct reference:
the check must pass. Record both results with their revisions. Keep a temporary
mutation out of the committed change unless the project retains such fixtures.

A check that passes on the known bad result is not evidence. Strengthen it or
report the gap. Select controls by assessed risk. Do not mutate every edit,
start a mutation-testing program or copy implementation details into tests.

For low-impact prose, wording or documentation changes, use inspection, link
or render checks and readback. Add no executable test that mirrors prose.

## Prevent repeated mistakes structurally

When evidence shows the same mistake recurring across deliveries or reviews,
prefer the smallest mechanism that prevents its cause: a type or schema
constraint, a lint or structural check, a boundary test or a driver
capability. Give the new check its own negative control. Use an instruction
rule only when no mechanism fits, and revise or replace an overlapping rule
instead of adding another. Implement the prevention when it is within the
authorized scope; otherwise propose it to its owner with the evidence. One
occurrence or one user correction does not establish a pattern.

Report a failure unrelated to the change, such as a flaky test elsewhere or a
lint error in untouched code, with its evidence. Route it to its owner or a
separate task unless the user or project policy authorizes the repair here.
Do not hide it or silently broaden the task.

## Feed selected observed failures into maintained checks

Use only failures that a person selected from authorized evidence, such as
an owner's review disposition or an owner-run follow-up of recent deliveries.
This method scans no past sessions, reads no transcripts, calls no models and
starts no study.

For each accepted case, record in existing verification evidence, such as the
feature map entry, the check or the issue:

- the source revision where the failure was observed;
- expected versus observed behavior;
- an evidence pointer;
- the human disposition.

Choose the proportionate check for what failed: a product test, driver
assertion, instruction scenario or reviewer-calibration case. A deterministic
check must reject the evidenced bad behavior and accept a valid reference,
demonstrated with a negative control. A failure that depends on judgment
keeps its human criterion and scoring limits; do not turn it into a
deterministic check. When a case is deferred or unsupported, for example missing its
revision, evidence or disposition, record the deferral and its reason. A case
used to write or tune a check, workflow or grader is development and
regression evidence, never an unseen holdout result.

## Report evidence truthfully

- A check that did not run, a missing artifact and an interrupted capture are
  unknown, unavailable or failed, never passed.
- Screenshots and videos supplement assertions. The assertion outcome is the
  result; an image without its assertion log does not establish a pass.
- Simulated transport, fakes and emulators establish simulated behavior only.
  Physical acceptance needs its own authorized device evidence and owner;
  report it pending until then.
- Report each result's class, check, revision and outcome in the checkpoint's
  Evidence field, keeping product defects, harness gaps, stale instructions,
  unavailable environments and unmet acceptance distinct.
