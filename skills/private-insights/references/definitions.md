# Report definitions

Read when explaining a measure, changing the report, or supplying a snapshot.
These reuse [#70](https://github.com/jimmie-potts/agent-skills/issues/70)'s
vocabulary and the Execution record defined in
[deliver-work's execution accounting](../../deliver-work/references/execution-reporting.md).
They settle only the fields this report needs; they do not complete #70's study.

## Cohorts and denominators

| Measure | Cohort | Denominator |
| --- | --- | --- |
| Selected attempts | Workflow runs created in the window, each with every attempt started before its end | Attempts in that workflow row |
| Deliveries | PRs merged in the window | PRs updated in the window |
| Incomplete outcome | PRs closed unmerged in the window; PRs opened in it and still open have no outcome yet | PRs updated in the window |
| Review and correction | Execution-record `Corrections`, only where it is an exact count | Records with a known count |
| Documented interruptions, usage | Attributed snapshot records. GitHub records neither, so without a snapshot both are `unknown` | Attributed records with that field |
| Elapsed waits | Median PR open to merge; median first-attempt `run_started_at` to `updated_at` for comparable originals | Merged PRs; comparable originals |

Elapsed time is not effort, tokens are not a subscription bill, and a price in a
snapshot is ignored. Rates are not computed across unlike repositories, windows
or workflows.

## Attempt buckets

Each attempt lands in exactly one bucket; together they sum to the row's attempts.
Cancelled, skipped and unfinished attempts take precedence over the attempt's
kind. A skipped run does not establish a prior attempt, so a draft's skip followed
by a real run still leaves that run an original.

| Bucket | Meaning |
| --- | --- |
| Comparable original | A finished first attempt: the first run on a newly opened PR, or the first on a default-branch revision |
| Prior unobserved | The first run seen on a PR opened before the window, or on a branch with no PR association; earlier history is outside the window |
| Rerun | Attempt 2 or later of one run |
| New-commit attempt | A new run on a new SHA with a tree not seen on that line |
| Same-tree new SHA | A new run on a new SHA with a tree already seen, such as an empty retry commit |
| Same-SHA new run | A new run on a SHA already seen |
| Ambiguous revision | A run naming more than one PR, or with no tree to compare. Never resolved by branch name |
| Unread history | An attempt known from `run_attempt` whose record could not be read. Other buckets in that row become `at least <n>` |

Attempts started after the window end are excluded and counted in a note. Reruns
started in the window of runs created before it are not observed.

## Jobs, checks and CI policy

Job records are read for rerun, failed and qualification runs. A rerun gives
copied jobs new ids and keeps their old times, so a job in attempt 2 or later is
copied when it started before that attempt or repeats an earlier attempt's name
and times. Copies never count as executions.

A qualification run is one whose workflow name or path says `qualification`. A
rerun in which an `image` job was copied is a partial rerun without its own image:
it cannot qualify, and its result job is left out of failed-job counts.

Check records are read at merged PR heads with `filter=all`, deduplicated by id and
then by app, name, times and conclusion.

The effective policy is the workflow-file fingerprint at read time, plus commits
touching `.github/workflows` in the window. A change blocks window comparison.

## Settings

| Term | Source |
| --- | --- |
| Recommended | The `Recommended` row. Neither a request nor an execution, and not counted below |
| Requested | `requested <value>` in a record. `default` and `unknown` are not requests |
| Declared | Provenance `user-stated` or `self-reported` |
| Observed | Provenance `host-observed` |
| Unknown | `unknown (unknown)`, a free-text cell or a missing record |

Aliases stay as written, such as `opus`. Provider family comes only from a written
model value, never from a branch name. Execution records appear in these shapes:
`current table`, `table without finding causes` (older), `free-text table`,
`unstructured`, `ambiguous` (more than one section) and `none`. Fenced examples are
ignored. First-submission acceptance and acceptance after correction follow
#70's mapping: `Corrections` 0, or 1 or more on a merged PR; `at least` and
`unknown` leave the measure unknown.

## Snapshot format

A snapshot is one JSON file the user names, at most 5 MB. No session or transcript
format is parsed.

```json
{
  "schema": "private-insights-snapshot/1",
  "observed_from": "2026-11-01T00:00:00Z",
  "observed_to": "2026-11-02T00:00:00Z",
  "records": [
    {
      "repository": "owner/name",
      "pr": 12,
      "head_sha": "<40 hex characters>",
      "model": {"requested": "opus", "declared": "opus", "observed": "claude-opus-5-5"},
      "attempt_outcome": "completed | failed | interrupted",
      "interruptions": 1,
      "usage": {"input_tokens": 100, "output_tokens": 20}
    }
  ]
}
```

A record counts only when its repository, PR and full revision match what GitHub
showed in this window. Anything else stays out of every count and is listed as
unattributed with its reason. Omit a field you do not have; it stays unknown.
