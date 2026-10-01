# Couple the final preflight to the merge action

Read before a GitHub merge. Use [the guarded action](../scripts/merge_guard.py)
to run the owning repository's read-only preflight and dispatch the normal merge
only after a successful current result. Keep the repository's policy evaluation,
review evidence, CI expectations, guide-only exceptions and owner decisions in
that repository. Do not replace its preflight with a constant success report.

The helper supports GitHub.com through the existing authenticated `gh` CLI and
Python 3. Other providers remain a capability gap for this helper: use only an
equivalent project-owned coupled action that preserves all gates and the
expected-head guard. Missing capability blocks merge; it authorizes no settings
repair, protection bypass or replacement service.

## Prepare the repository adapter checkpoint

Before using the action, identify the trusted read-only preflight command, its
required gate IDs and owning policy revision. Inspect the command's entire
behavior and permission scope. The helper executes that explicit argv without
a shell and sends the binding on stdin; it does not sandbox arbitrary commands.
An adapter may translate an existing result, but must preserve every gate,
exception, failure and evidence reference. A saved report alone cannot pass:
the helper runs the command and checks its read time on each invocation.

Prepare a private binding file from the accepted review comparison and normal
project merge strategy. Use full SHAs and list every repository-required gate:

```json
{
  "repository": "example/project",
  "pr": 42,
  "baseRef": "main",
  "base": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "head": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
  "mergeBase": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "strategy": "squash",
  "requiredGates": ["identity", "ci-pr", "review", "feedback"]
}
```

The IDs above illustrate a repository choice, not a shared minimum or permission
to omit gates. Refresh the issue, policy, expected CI matrix, reviews and
protections before deriving this list. If the repository has no executable
preflight, supply a scoped read-only adapter over its existing evidence at this
checkpoint. It must evaluate the actual gates; hand-written success flags are
not an adapter. Do not add a universal preflight framework to the catalog.

## Preflight result boundary

The helper consumes these fields from stdout JSON, with no log/banner prefix:

- `candidate`: `repository`, positive integer `pr`, `baseRef`, full `base`,
  `head`, `mergeBase`, `state: "open"`, and `draft: false`.
- `readAt`: timezone-bearing ISO time within this command invocation.
- `result: "satisfied"`, integer `exitCode: 0`, and `readFailures: []`.
- `gates`: nonempty list with unique `id`, `status`, `rule`, `reasons`, and
  `evidence` fields. Every required ID must appear. Every returned gate must be
  `satisfied` or `not-applicable`; the latter needs its repository-owned reason.
  `rule` is a nonempty policy reference; `reasons` is a list of nonempty strings;
  `evidence` is an object. Each gate needs a reason or nonempty evidence.

Additional repository fields are retained in the receipt. This boundary does
not authenticate evidence or decide whether an exception is allowed: the trusted
repository preflight owns those decisions. Missing/malformed results, nonzero
exit, unresolved gates and unavailable reads produce zero merge calls.

The existing Hub `delivery-preflight` schema 1 already supplies this shape.
Its source-only gate set includes identity, ci-pr, ci-main, review, feedback,
ui-approval, proof, counterparts and live-acceptance. Keep that list in Hub's
adapter invocation; it is not portable policy. Use Hub's declared prerequisites
and JSON mode with its expected PR/head/base, preserving all optional evidence
arguments. This source change does not mutate Hub or make its status command
mutating. The representative fixture is based on Hub source
`da5e4794d45f461bc583b1092b8ee1edeac07a94`,
`scripts/delivery-preflight/{preflight,context,cli}.mjs`; it is synthetic integration
evidence, not qualification of a live Hub delivery.

## Invoke and retain the outcome

A check remains read-only:

```text
python3 <skill-directory>/scripts/merge_guard.py --binding <binding.json> -- <preflight-command> <args>
```

Only an explicitly authorized action adds `--execute` before `--`. Record the
intent, PR, reviewed comparison, adapter, required gates and expected prior open
state before invoking it. Never follow a status check with an unconditional
merge command. The action itself reruns preflight, refreshes PR identity and
head, checks the merge-base and reads the target tip immediately before one
`gh pr merge` with the chosen strategy and `--match-head-commit`. It supplies no
`--admin`, force option, auto-close operation or retry. GitHub's existing queue
and protection behavior remains in force.

Retain the JSON receipt outside the candidate commit. `checked` is not a merge.
`blocked` means no merge call was made. `reconcile` means one call was attempted
and its result needs authoritative resolution; it includes a read after a
provider rejection, timeout or ambiguous response. Do not rerun the action to
probe an unknown result. Follow [recovery](recovery.md), read the PR/queue and
reconcile the prior receipt first. Renew gates before a separately authorized
retry. `merged-readback` records the expected head/target and a merge revision;
it still requires destination inclusion, resulting-tree and post-merge CI
verification under the entrypoint before completion or issue closure.

A detected pre-dispatch base/head change blocks. A base change after the final
read remains possible: GitHub's expected-head argument does not atomically
compare the target tip. Preserve required queues and strict branch protections;
when project policy requires a stronger server guarantee that is unavailable,
do not dispatch. Do not label this helper an atomic base guard. Server protection
design remains with its owner (Hub #240); another tool or human can bypass this
local path, so this is not arbitrary-command security confinement.
