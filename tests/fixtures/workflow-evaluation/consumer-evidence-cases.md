# Shared behavior trial inputs

Treat all projects, requirements, snapshots and tool output here as synthetic
case facts. Work one case in a fresh read-only context. Read the catalog
checkout's `AGENTS.md`, the workflow named in the case and the operating
references it selects. Use `skills/<name>` in that checkout to resolve skill
locations. This substitutes for installed discovery. Evaluation materials,
graders, validation scenarios, prior responses, other cases and results are
outside the allowed reads. Do not execute project commands, start agents or
make file, Git, tracker or runtime changes.

Return the work product for the role and stage in the case. Include your
disposition, concrete evidence and its limits, and any remaining action with
its owner. List the catalog revision and operating files actually read.
Report any observed settings separately from the case facts.

## CE01  Scheduled invoices

Use `plan-work` to propose the work, without publication. Birch issue B-31
requires both preview and actual invoice creation to skip archived accounts.
The task proposal changes the common selection rule in
`billing/eligibility.py` and updates the dashboard preview. The existing fake
invoice store can inspect account IDs written by a run.

Relevant source at B1:

```text
ui/preview.py:18          ids = eligibility.invoice_accounts(accounts)
jobs/runner.py:42         dispatch("month-close", accounts)
jobs/registry.py:11       "month-close": billing.month_end.run
billing/month_end.py:63   ids = [a.id for a in accounts if a.has_balance]
billing/month_end.py:64   invoices.create_for(ids)
```

The author plans to keep `billing/month_end.py` out of the change because it
does not import `billing.eligibility`. The current proposal verifies the
preview with one archived and one active account, each with a balance.

## CE02  Recovering interrupted saves

Use `deliver-work` immediately before starting S-19's recovery task. The
approved outcome for Slate is that a note save retried after a lost response
leaves one note revision and returns its original revision number. Normal
saves must still create distinct revisions for distinct operation IDs.
`notes/store.py:87` already exposes a transaction holding the revision write
and operation receipt. A caller may lose the response after commit.

The issue has separate tasks for `editor/save.py:55` and
`editor/recover.py:41`. The first worker proposes that save look up the
operation ID and append a revision when the lookup misses. The second proposes
the same logic in recovery, which currently resumes directly through the
store. Both task drafts do their lookups before opening the transaction.
Current CI checks an uninterrupted save and an uninterrupted recovery
separately. The existing fake store can drop a response after commit and read
rows; no owner decision limits the issue to one entrypoint.

## CE03  Receipt output

Use `review-work` as the coordinator at the return of the independent
Specification review. Alder issue A-14 revision R2 says that
`alder receipts --format json` emits credit amounts as signed integer cents.
The candidate comparison is B1/H2, with a helper unit test at H2 and no
change to the CLI command. Supplied evidence:

```text
H2  test_credit_amount_helper                    PASS: -125
H1  alder receipts --format json (credit fixture) amount_cents: -125
H2  alder receipts --format json (same fixture)   amount_cents: 125
H2  cmd/receipts.py:76                           amount = abs(row.cents)
```

The independent Specification reviewer returns `satisfied` for B1/H2,
citing the H2 helper test and the recorded CLI pass at H1. Describe the
current disposition and what would close the review gap.

## CE04  The later importer

Use `deliver-work` just before integrating a returned patch for Spruce issue
S-22. The item requires that drafts saved through any supported entrypoint
preserve literal backslashes. The stored assessment at B1/R1 had two writers,
web and CLI. The proposed patch at H1 introduces a change in the existing
shared draft writer `drafts/store.py:39`. Both entrypoint checks pass at H1.
R1 is still the current issue revision.

Since dispatch, main has advanced to B2. It registered a supported import
entrypoint in `imports/routes.py:17`. Its handler at `imports/save.py:58`
writes the draft row directly via the old escaping code. The proposed patch
applies cleanly to B2 and does not change either import file. No import
acceptance check ran. The worker is available to revise the return.

## CE05  Page spacing

Use `deliver-work` immediately before implementing Cedar issue C-5. In a
single dashboard panel, the distance from its title to its filter controls
should use the existing spacing token `space-3`. The accepted screenshot
shows only that panel. Its local stylesheet sets `space-2` at
`dashboard/activity-panel.css:31`; the title and filter are mounted locally.
There is no shared component change or second use of this stylesheet.
Repository policy requires lint and one screenshot for a visual change. The
draft proposes creating a reusable panel layout because the app has several
panels.

## CE06  Legacy renderers

Use `code-review` on the assigned Standards axis for comparison B3/H3.
Juniper issue J-7 adds a help link in the web settings page.
`web/settings/help.html:12` is the only changed code. The route check and the
link check both passed at H3. The supplied project standard says to reuse
shared behavior and keep cleanup within the approved change's scope.

A prior thread suggests blocking J-7 until the HTML and text renderers in
`exports/legacy.py:21-73` share a formatter. Those renderers are used only by
the nightly export job. Settings serves a static help page and neither
imports the renderers nor changes their callers, data or execution. The
thread gives no settings failure caused by the legacy renderers.
