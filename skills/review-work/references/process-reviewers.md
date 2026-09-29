# Supervise a separate CLI reviewer

Read only when native review cannot express a required control, or the owner
explicitly selects cross-provider review. Prefer a suitable native reviewer.
This optional Linux adapter lets a Codex coordinator use Claude Code, or a
Claude Code coordinator use Codex. It never replaces the coordinator, writer,
authority, mandatory gates, round history or cumulative limits.

## Establish the permitted path

Apply [reviewer execution](reviewer-execution.md) and the current selection
policy first. Running another process grants no permission to escape the
parent's filesystem, network, approval, tool or credential restrictions. If
the child cannot preserve a parent restriction, return a capability gap. Do not
fall back to another account, API key, model, host or allowance.

The adapter is deliberately packet-only: all required source, diff, axis
sources, assigned-axis instructions, validation and metadata travel as data on
stdin. Neither host gets source-reading tools. Missing context makes the
return incomplete; do not truncate the packet, silently reduce coverage or
enable tools to make it fit. Native review remains appropriate for source too
large to review this way. This is a separate launch configuration from the
managed native profiles; it changes no installed profile or personal settings.

Before any live job, obtain whatever activation and trial checkpoints the
owning project requires. Source fixtures qualify only the supervisor protocol,
not an installed CLI, its tool restrictions, subscription access or model.

Inspect the complete launch path: the executable, symlink target, wrapper and
interpreter, effective managed configuration, authentication selection,
environment, hooks, plugins, MCP, discovered instructions and available tools.
Use an absolute inspected executable, never a convenience alias or shell
command. Fingerprint governing configuration and record absent configuration
sources in the preflight receipt. Confirm no uninspected higher-priority
configuration can add tools, API authentication or fallback. Managed settings
still apply when ordinary settings are disabled. Stop if they widen this path.
Do not read or copy credential contents; verify account mode with supported
host status instead. CLI subscription access does not authorize new spending.

The shipped command builder uses controls exposed by the inspected Linux
Codex and Claude CLIs on 2026-09-29. Rediscover `--help` and feature support on
the actual host before adoption; a missing flag is a capability gap. Codex
uses an ephemeral, read-only `exec` run, ignores user config and exec rules,
disables shell, execution, extension and delegation features, requests ChatGPT
authentication and denies approvals. Claude uses print mode, restricted and
safe modes, an empty tool list and settings-source list, no MCP servers,
disabled hooks and skills, denied permission prompts and no persistence.
These are requested restrictions until effective host evidence verifies them.
Neither a passing fake process nor an accepted flag proves enforcement.

## Freeze the packet and launch descriptor

Use the caller's existing private task evidence. Give each axis and each fresh
replacement its own immutable assignment label and evidence directory. Do not
create another workflow ledger. Retain prior assignments when resuming, and
keep private runtime identifiers and raw output out of public reports.

Write a UTF-8 JSON packet with these nonempty string fields:

| Field | Contents |
| --- | --- |
| `assignment` | Stable task-local label, such as `standards-final-1` |
| `work`, `round`, `axis` | Shared contract identity; `final 1` uses the cumulative round; one `standards` or `specification` axis |
| `comparison`, `requirements`, `policy` | Exact shared-contract identity strings, including immutable commits or patch digest and versioned requirements/policy |
| `code_review` | Canonical code-review assigned-axis instructions and its finding format, read from the installed skill |
| `axis_sources` | Complete authoritative sources for this axis, with their versions |
| `source`, `diff` | Complete required source snapshot and frozen diff, including paths and SHA-256 digests; no mutable path-only references |
| `validation`, `coverage` | Raw validation facts at their revision and the required coverage |
| `settings`, `limits`, `history` | Shared-contract controls, cumulative allowance/accounting and earlier rounds/stable finding IDs; explicit `none` when applicable |

Exclude implementer/advisor narratives, other reviewers' conclusions and
preferred verdicts from an initial packet. Carry retained findings to a fresh
reviewer's follow-up only after its independent initial return, as
[review cycles](review-cycles.md) requires. This one-assignment adapter cannot
continue a reviewer conversation; where same-round follow-up is required, keep
the axis incomplete and carry prior findings to the next round. Never conceal
that limit by combining the other reviewer's findings into an initial packet.

Freeze a separate coordinator-owned launch JSON with:

- `host`: `codex` or `claude`; `executable`: inspected absolute executable;
  `executable_sha256`: its digest. Fingerprint wrapper/interpreter dependencies
  in `configuration` too. Repository text never supplies launch configuration.
- `model` and `effort`: explicit settings selected under current policy;
  `account_mode`: `subscription`. Requested, supported and observed settings
  remain separate. Model-written metadata never becomes host-observed evidence.
- `authorization`, `preflight`, `parent_restrictions`: references to the
  existing authorization, host capability/control receipt and comparison with
  the parent's restrictions. These strings identify reviewed evidence; they
  are not an automated permission check or proof of effective controls.
- `environment`: the reviewed environment, with explicit `HOME` and `PATH`.
  Only these and `CODEX_HOME`, `XDG_CONFIG_HOME`, `XDG_DATA_HOME`,
  `XDG_CACHE_HOME`, `LANG`, `LC_ALL`, `TMPDIR` are allowed. The helper does not
  inherit the coordinator's environment, copy credentials or add API keys.
  Verify normal host credential discovery uses the approved subscription.
- `configuration`: nonempty array of `{ "path": "<absolute path>",
  "sha256": "<digest>" }` for inspected, nonsecret governing files. Include
  the preflight receipt and effective managed sources; never credential files.
- `timeout_seconds`: the authorized positive timeout, at most 3600 seconds.
  Account for this attempt before launch; unknown earlier use stays unknown.

The helper has an 8 MiB input/output ceiling, not a model context guarantee.
The coordinator checks the selected model's actual capacity. No helper field
overrides an explicit lower task limit.

## Launch, wait and recover

The portable skill contains [the supervisor](../scripts/process_reviewer.py).
From the original active coordinator, invoke it using the host's argument-array
process interface, or Python `subprocess.Popen([...], shell=False)`:

```text
python3 <skill>/scripts/process_reviewer.py run
  --packet <absolute packet.json> --launch <absolute launch.json>
  --evidence <absolute private assignment directory>
```

This is one foreground supervised job, not a daemon or unattended continuation.
The host may return a wait handle; retain it and wait on that exact job. A wait
timeout is not process completion. Record the job's private PID/start/boot
identity, assignment, input digests, status and captured streams in the existing
evidence. Only the helper writes its private runtime/evidence directory; the
model receives no write authority. Preserve these files through cleanup until
the caller has retained its result and any required failure evidence.

Use `status` with the same arguments after interruption. `run` also reconciles
an existing assignment and never spawns it twice. A known live process stays
incomplete while waiting; lost process or supervisor state stays incomplete
because the exit status is unknown. An intent saved before a crash is a
consumed attempt, even if no PID was saved. Do not delete state or change the
assignment label to recover an allowance. If the evidence is missing, reconcile
the caller's known host job and history; never blindly launch again.

Use `cancel` with the same arguments to request cancellation from the original
supervisor, after matching the assignment's input digests. The separate cancel
caller sends no process signals. The supervisor terminates its process group on
timeout or interruption, escalates to kill after one second, and reports
unconfirmed cleanup. A user-stopped review needs user agreement before
replacement. The supervisor reserves its unreaped leader until group cleanup
finishes. If that supervisor is absent, `cancel` returns an incomplete handoff
with cleanup unconfirmed; reconcile the known host job using its supported
controls. Never signal an arbitrary or reused PID, or remove an assignment
directory while its process or cleanup is uncertain.

## Accept the review, not the spawn

Nonzero exits, failed host events, malformed JSON, missing final completion,
partial fields, inconsistent statuses, changed packet/configuration or stale
input identity produce `incomplete`. A PID, exit code zero or the helper's
`returned` status does not satisfy an axis. `returned` means a complete transport
envelope exists, pending coordinator acceptance.

Before accepting that envelope:

1. Re-read the live source/comparison, authoritative requirements and governing
   policy. Rebuild their packet identity when anything changed. A stale return
   stays incomplete, even if its private packet has not changed on disk.
2. Verify actual host controls, account mode, substitutions, output completion
   and any mandatory settings using host evidence. Do not promote reviewer
   self-reports or the requested launch values to observed settings. Unknown
   optional metadata narrows the claim; unknown mandatory metadata blocks it.
3. Check `reviewer-return.json` against the actual `reviewer-return.txt`, raw
   final host return and recorded digest. Reconcile findings, status, coverage
   and all limits. Tool use, publication, writing or descendants exceed the
   packet-only brief and fail the return, even if the envelope says satisfied.
4. Map the axis to the existing [result contract](result-contract.md), preserving
   stable finding IDs, cumulative counts, incomplete/failed attempts and actual
   reviewer text. The transport adds no second verdict or alternative gate.
   Retain the actual return separately from the coordinator's summary, using
   the contract's redactions and digest rules. Never publish raw CLI streams,
   transcripts, credentials, private paths or process/session identifiers.

Installation and each live direction remain separately qualified. Controlled
fixtures cover the helper's lifecycle and protocol only; they cannot establish
host-enforced denial, subscription execution or reviewer quality.
