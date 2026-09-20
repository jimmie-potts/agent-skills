# Select and continue investigation or implementation workers

Read for initial worker selection or implementation strategy changes. Direct trivial work at the coordinator's existing settings needs
no worker selection. Apply [the common policy](model-selection.md) and only the
selected host's worker adapter. Planning consumers remain read-only.

Complexity determines suitable coding capability; interacting state may need
higher reasoning and testable decomposition. High uncertainty requires
investigation or clarification before dependent implementation. High impact
sets a stronger capability floor even for a tiny diff; choose the strongest
evidenced relevant option when suitability is uncertain. Do not average ratings
or try to replace a missing product decision with a stronger model.

## Choose an implementation strategy

For decomposed or delegated work, read [task planning and dispatch](task-planning.md)
before selecting a strategy. Establish required-input readiness and independent
contracts/resources; file paths alone do not justify parallel workers.
Direct coordinator implementation is the baseline: use it
for trivial work or continuously difficult reasoning when existing settings
suit the task. For eligible bounded work, apply the host adapter's cheaper
worker default; merely fitting one context does not override it. Judge
alternatives by cost per completed task, including
corrections and reruns, rather than tokens per request. Use one bounded worker
when different settings or isolation materially help, and separate bounded
workers when the work splits into independent pieces or exceeds one context.
Workers return proposed patches and evidence; the coordinator applies changes.
Give each worker outcome, source/revision, applicable instructions, assessment,
acceptance mapping, constraints, ownership, and the
[bounded brief and return contract](worker-briefs.md). Use a self-contained
brief when overrides prevent full-history inheritance.
Distinguish requested settings from observable runtime identity.

Name the chosen strategy in the record. The strategies are direct
implementation by the coordinator; an assigned worker with one brief and no
advisor loop; parallel workers for independent pieces, which the coordinator
merges; and the advisory pairing, where one worker runs the implementation
loop and consults the coordinator at approach, blocker, and final review. The
coordinator owns durable writes and runs the independent reviews as a separate
step under every strategy.

Choose the host's advisory pairing when bounded, capable worker implementation
benefits from coordinator approach/blocker checkpoints: serial work with a few
hard decision points rather than continuous difficult reasoning. Select the
pairing skill from verified host tooling, never from a persona or a model list.
Codex collaboration tools select worker-with-astra. Claude Code subagent tools
select worker-with-fable. Any other host has no pairing. Discover and read the
selected skill and its host adapter before starting. Its original-coordinator
identity, worker availability, parent communication or worker resumption, and
consultation requirements remain mandatory. Record what the worker can decide
and what requires consultation. Apply selected reasoning through supported
controls without changing the advisor.

When difficult reasoning is continuous rather than separable into checkpoints,
prefer direct implementation or a directly assigned, suitably capable worker.
If an optional pairing cannot be established, choose another suitable strategy
and disclose why. If the user explicitly requested the pairing, report its
unmet prerequisite; do not create a replacement advisor or silently substitute
another arrangement. Advisory inspection never replaces independent delivery
reviews.

Before correcting an inadequate return, resuming/replacing a worker or changing
an unresolved attempt's settings, read [worker continuation](worker-continuation.md).
It owns diagnosis, handoff and history; the active host's worker adapter owns
thresholds and mechanics. Initial selection does not require that recovery path.
