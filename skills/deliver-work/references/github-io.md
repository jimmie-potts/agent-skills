# Preserve text and bound revision-specific reads

Use the existing structured connector for publication when it accepts the body
as data. Reject empty or whitespace-only text before a write. Keep Markdown,
quotes, backticks, dollar signs, Unicode and newlines unchanged. No shell
interpolation, `eval`, shell-expanded here-document or inline `echo` pipeline.
When using the authenticated CLI, create a UTF-8 body file in the authorized
task directory, validate it with `read_body` from [the helper](../scripts/github_io.py),
and pass its path as a separate `--body-file` argv argument without a shell.
Use an existing Python 3 runtime; do not assume `jq` or install credentials.
Unreadable files, invalid UTF-8 and whitespace-only input stop before dispatch.

## One publication effect

Before dispatch, preserve intent, repository, target kind/number, exact body,
unique existing publication marker and expected author in the task packet.
Use [review-report markers](review-reports.md) for review evidence. This helper
does not grant publication authority or generate another marker format.

`publish(body, marker, author, write, read, reconcile_only=False)` calls the
trusted `write(body)` at most once, then reads back even after a lost response.
Bind both callbacks to the same selected repository and issue/PR. The read
callback must collect every page and return normalized `{id, url, author, body}`
objects, or raise when any page/read fails. A single exact author/marker/body
match with provider identity yields `verified`; normalize only line endings.
Missing identity, changed bodies, duplicates and incomplete reads remain
`unresolved`. A write response or HTTP acknowledgment alone is not verification.

For a resumed or possibly attempted write, use `reconcile_only=True` before any
new attempt. Retain the receipt and provider object outside the candidate commit.
Never replay the default write mode to investigate an uncertain response.
Authoritative absence is not proof a delayed write cannot still arrive: apply
[recovery](recovery.md) before deciding whether a separate retry is safe and
permitted. The helper does not retry, replace existing comments or reset limits.

## Discover policy before waiting

The coordinator selects repository, PR and full head SHA explicitly. Read the
candidate workflow configuration and project protections/rulesets to enumerate
required checks, including matrix jobs and non-Actions providers. Record an
immutable policy source and the required logical names. Do not discover
requirements by copying whatever jobs have happened to appear.

Retain policy-backed intentional filters with their reason and candidate evidence.
An absent job is not an implicit filter. An empty required set, or a set with
every job filtered, cannot be certified as successful CI by this helper; return
that separate project-owned no-CI decision to the coordinator.

Call `wait_checks(target, policy, read, budget=seconds, interval=seconds)` with:

- target: `{repository, pr, head}`
- policy: `{source, required: [logical names], filtered: {name: evidence/reason}}`
- `read(remaining_seconds)`: a trusted read-only adapter returning target identity,
  `complete: true` only after all pages/provider reads succeed, and `checks`
- each check: `{id, name, head, association, status, conclusion}`, with association
  `pull_request:<number>`, status `queued`, `in_progress` or `completed`, and the
  actual provider conclusion (only `success` satisfies an applicable requirement)

The adapter must refresh the PR head each time, verify event/PR/head association,
select the latest applicable attempt for each logical job and expand matrices.
Do not relabel a push run as a PR run. Resolve test-merge/merge-queue coverage to
the candidate only with provider evidence. Preserve check-run/Depot and commit
status providers; never require an Actions workflow ID for all checks. Adapt a
provider's success value to `success` only where its contract establishes that.
Duplicate current attempts or missing pages are unavailable evidence, not a tie
broken by list order. Retain provider IDs and association evidence in extra
snapshot fields for audit. The helper cannot authenticate a caller's policy or
normalized evidence; those remain the adapter's responsibility.

Every provider request and page consumes the remaining deadline, including
network timeout. Do not use an unbounded watch or sleep inside `read`. Optional
`cancelled()` is checked before/after each read and before each bounded sleep;
the read adapter must also honor cancellation for long I/O. Callbacks are trusted
integration code, not a generic shell executor or an enforced sandbox. A callback
that ignores the deadline can delay return; such an overrun is `unavailable`,
never a late success. Use host request timeouts/cancellation to enforce I/O bounds.

## Interpret the receipt without changing state

- `not-started`: one or more required checks have not associated, including an
  entirely empty check list; the deadline may expire here
- `running/time-limit`: all requirements associated but some remain queued/running
- `failed`: an applicable completed check is unsuccessful, including cancelled,
  skipped, neutral or missing conclusion; inspect logs before diagnosing/retrying
- `successful`: all applicable required checks completed successfully
- `stale`: selected repository/PR/head changed; stop this old wait
- `unavailable`: invalid policy, incomplete/API/error/ambiguous evidence or an
  adapter deadline overrun
- `cancelled`: caller cancellation stopped this wait

The receipt includes target, policy, read count, latest snapshot and `timeLimit`
when the time budget expired. Missing required jobs remain missing, never green.
Waits perform reads only: no reruns, publication, issue changes or state repair.
Resume through the existing supervision owner, refreshing policy/head and keeping
prior attempts. A timeout never replenishes retry allowance or completes an
explicit request to keep monitoring. Fake-adapter tests qualify these decisions;
they are not live publication/provider or installed-host qualification.
