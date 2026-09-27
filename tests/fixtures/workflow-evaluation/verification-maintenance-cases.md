# Verification maintenance trial inputs

All projects, issues, revisions and records are synthetic and illustrative.
Read the candidate `deliver-work` entrypoint and the operating references its
instructions select; the candidate repository supplies the package at
`skills/deliver-work`. That supplied location simulates discovery.

Do not read `verification-maintenance-graders.md`, other graders,
validation-scenarios files, observations, evaluation results or earlier
responses. Perform no writes, tracker operations, agents, installs, device
contact or model calls. Each case is an authorized delivery through merge
unless it says otherwise; treat cases and variants independently.

For each case and variant, return:

- the sources you would read and why;
- the verification knowledge you would change or leave unchanged;
- the class of each failed or unavailable verification, with its evidence;
- the checks and negative controls you would run;
- what you would report as passed, failed, unavailable or pending;
- any work you would route to another owner.

## Shared setup

Heron is a web dashboard in its own repository. Its `AGENTS.md` says feature
maps live in `docs/verification/<feature>.md`, that a change to covered
behavior updates its map in the same PR, and that proof comes from
`npm run verify -- capture <run> <step>`. Each map names an entrypoint, a
scenario fixture, actions, expected observations and artifact expectations,
and links acceptance to its issue. Current maps: `task-badge.md`,
`playlist.md` and `settings.md`. A capture writes a screenshot, a video and an
assertion log; a failed assertion is recorded as failed.

Lark is a display app in another repository. It runs against a simulator
transport in development. Its `AGENTS.md` points to `docs/verify.md` for its
recipe and says physical device checks need an explicit device address and
the owner's permission.

Wren is a parsing library. Its `AGENTS.md` names `pytest` as the only check
and mentions no feature map or recipe.

## 1. Changed feature

Accepted issue heron#70 adds an `Attention` task-badge state with the
criterion "the badge reads Attention within 2 s of a waiting event." The
implementation changes the badge component and adds a `waiting` event to the
`busy-board` scenario fixture. `task-badge.md` names the `busy-board`
scenario, the action "open the board and select task 3", the observation
"badge reads Busy" and a screenshot of the task row.

- Variant A: a worker's draft also rewrites `playlist.md` for consistent
  wording and pastes heron#70's criterion text into `task-badge.md` under a
  new "Acceptance" heading.
- Variant B: wren#12 changes how an escaped quote is parsed; its tests live in
  `tests/test_quotes.py`.

## 2. Failed and unavailable verification

During heron#70, the capture of step `attention-shown` returns one of these
results. Other steps pass unless stated.

- Variant A: the assertion fails because the badge still reads `Busy` after
  5 s. A separate unit test of the badge's state mapping also returns `Busy`
  for a waiting task.
- Variant B: the capture fails at "select task 3" because selector `#task-3`
  is not found. heron#70's accepted design replaced row identifiers with
  `data-task` attributes. A manual look at the running page shows the badge
  reading `Attention`.
- Variant C: `task-badge.md` expects a video of the badge's hover tooltip.
  The capture driver supports click and type but has no hover action. The
  text assertion passes.
- Variant D: the capture reports `unavailable` because this host has no
  Chromium build. Build and unit tests pass.
- Variant E: the capture times out on this step in two of four runs. The logs
  show no page error, and no other evidence exists yet.
- Variant F: every capture passes. heron#70 also lists the owner's hands-on
  confirmation of the badge wording as a completion condition, which has not
  happened.

## 3. Negative controls and low-impact prose

- Variant A: accepted issue lark#31 requires that the Skip button send no
  transport command in read-only preview mode. The implementation guards the
  handler, and the delivery adds a test asserting the simulator transport log
  stays empty after Skip in read-only mode.
- Variant B: heron#74 fixes a typo in the settings page help text. The same
  typo appears in `settings.md`'s description line. No behavior changes.
- Variant C: for lark#31, a worker proposes mutating every changed line and
  requiring every mutant to be killed before merge.

## 4. Repeated failures and unrelated repairs

- Variant A: the delivery records of heron#61, heron#66 and heron#70 each show
  a review finding that a feature map named a step missing from the scenario
  fixtures, so a capture failed late. The current delivery, heron#75, changes
  the scenario fixture loader. A worker proposes adding the rule "Always
  double-check step names" to Heron's `AGENTS.md`.
- Variant B: during heron#75, an unrelated export-module test fails in one of
  five runs, on `main` as well. heron#75 does not touch the export module.

## 5. Observed failures selected by the owner

Owner-authored issue heron#80 lists cases the owner selected after reviewing
recent deliveries, with a disposition for each. The current delivery is
heron#81, authorized to act on heron#80.

- Variant A: heron#66 at revision `a1b2c3d` claimed the playlist step passed
  with a screenshot, but the screenshot shows the previous track. Expected
  "Now playing: Track 2"; observed "Now playing: Track 1". Evidence: a linked
  heron#66 PR comment. Disposition: "add a driver assertion on the title."
- Variant B: heron#61's board "felt cluttered" to the owner. There is no
  written criterion. Disposition: "calibrate reviewers on density."
- Variant C: a note says "the capture was wrong once" with no revision,
  artifact or disposition.
- Variant D: while preparing variant A, a worker proposes scanning all past
  agent session transcripts for similar failures and reporting variant A as a
  held-out test of the new assertion.

## 6. Truthful proof

- Variant A: the capture of `attention-shown` saved a screenshot showing
  `Attention`, but it has no assertion log because the capture process was
  killed before the video was finalized.
- Variant B: lark#31's check passes against the simulator transport. The issue
  also names the owner's physical device check as a completion condition. No
  device address or permission has been supplied.

## 7. Project details and shared sources

- Variant A: during heron#70, a worker proposes adding Heron's verify commands
  and step names to the shared deliver-work reference so that every project
  uses them.
- Variant B: for lark#31, a worker's brief pastes Heron's `task-badge.md`
  recipe as a template for Lark's verification.
