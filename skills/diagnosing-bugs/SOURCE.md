# Diagnosing bugs provenance

- Upstream repository: `https://github.com/mattpocock/skills`
- Upstream path: `skills/engineering/diagnosing-bugs/`
- Pinned source revision: `5b15a47f2d7150f545fbcacbfe381787fc0230dc`
- Retrieved: `2026-08-23`
- Upstream source SHA-256 digests:
  - `SKILL.md`: `77f3cf31bc99b2f49af943222526531fcc9fc41d047626d3640e875e85af3e84`
  - `agents/openai.yaml`: `3e430dbe4334a87597488c060cb3dc3786bb00c9182877d6f5ec41f62490e90b`
  - `scripts/hitl-loop.template.sh`: `35103539fc36873eea36074769ad454f9379d6fc8b2dc0e26ce987fd3bfe5503`
  - Repository `LICENSE`: `0e7ac423bf2c6e223b7c5b156f8cf72da49d748e56a1641402c31f22ad07dbb5`
- License: MIT, Copyright (c) 2026 Matt Pocock; preserved in `LICENSE`

## Local adaptations

The local version keeps the upstream red-capable feedback loop, minimization,
ranked falsifiable hypotheses, one-variable probes, performance measurements,
and redaction rules. It requires a demonstrated reproduction before a causal
claim and stops after diagnosis unless the underlying request separately
authorizes a fix.

The HITL template was reviewed in full. Sample-specific URL, action, variable,
and error-message capture were removed. The adapted template is output-only: it
uses static `printf` calls, reads no standard input, command-line arguments, or
environment values, and therefore cannot capture credentials by design. Sign-in
remains an unrecorded human step in the target application. The human reports
only `yes`, `no`, or `unclear` through the authorized task conversation after
the script exits. Repository validation checks shell syntax but does not execute
the script.

Upstream fix, regression-test write, artifact deletion, and commit-message steps
were removed from the diagnosis workflow because they require separate
implementation, filesystem, or Git authority.

Scope, change records, and delivery authority come from the target repository.
The shared workflow does not require Jira, OPSX, or a named delivery skill.

Updates are manual. Fetch the pinned upstream directory and repository license
into a temporary location, review every file and the complete diff, recompute
all digests, re-audit the complete shell template, and rerun the repository's
focused and full checks before changing this copy. Never execute the bundled
template merely to validate it.
