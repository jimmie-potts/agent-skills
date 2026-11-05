# Observed CI failure triage decisions

Fresh read-only contexts received a `diagnosing-bugs` entrypoint and
`ci-triage-cases.md`. The coordinator froze `ci-triage-graders.md` before
dispatch and withheld it and prior returns. Each participant reported reading
only permitted sources, with no durable or external effects. Raw returns remain
in the authorized delivery conversation for issue #173, separate from this
scoring summary.

Base revision: `4f8a3cf579a2da9d0a34c17a267093dd2dea72c0`. The requested model
was Claude Code `opus`, read-only `Explore` agents. Reasoning effort and
attributable usage were not exposed. The rubric did not change.

| Digest | SHA-256 |
| --- | --- |
| Frozen rubric | `72609459b252cbac9a1996f24aa3b31eb918d3ad4be99271433ae15b4c721800` |
| Cases v1 | `288f40ba888ebc0cca3083605efe6479c308ffb05370744fb19203d11ef545a1` |
| Cases v2, shipped | `f0163478ad126a7bb5932776964ef9e18361f737492de83323d9d9c2dc97b4b0` |
| Base `SKILL.md` | `366e68a00909a9e15cf1a3f0273dcd093ef7a2b55e1a2416c5c8deb72fc502f7` |
| Candidate `SKILL.md`, shipped | `59473d4ea111ba9d7003437133b4e4657a752c37cd3c5b6769185c5d3384ce5b` |
| Reference R1 | `52364485dbfbef714816b65d0f3d2f55d18b49aa6288d6f0a4c46fab43a48210` |
| Reference R2 | `43056568f6bad2c52dfa747aada2d81b6d4fac7fa89356c325623156db35f618` |
| Reference R3, shipped | `367f8609366b210f39d76fd8e6ebdba7e1073a43ce7063afd21fb45e34dac3ee` |

| Round | Instructions | Cases input | Contexts and cases | Result |
| --- | --- | --- | --- | --- |
| Baseline | Base `SKILL.md`, no reference | v1 | One context, 1-11 | Failed 1 and 2; passed 3-11 |
| C1 | Candidate, R1 | v1 | One context, 1-11 | Passed 1-11; reported three instruction gaps |
| C2 | Candidate, R2 | v1 | One context, 1, 2, 4, 5, 6 | Passed all five |
| C3 | Candidate, R3 | v1 | One context for 1-9; one each for 10 and 11 | Passed all but 2, which diverged |
| C4 | Candidate, R3 | v2 | One context, 2 | Passed |

## Scored decisions on the shipped reference

Every row ran against reference R3. Cases 10 and 11 each ran in their own
context.

| Case | Round | Observed decision |
| --- | --- | --- |
| 1 | C3, R3 | Async-observation race, `proven`; attempt 2 reported as non-recurrence; the older commit's failure rejects a PR regression. Recommended the event wait with the `settled` assertion and a negative control, unproven until run. Read-only. |
| 2 | C4, R3 | Mixed clocks, `proven`: harness deadline fires at 330 ms wall, the worker delay fails 10 of 10 against a 20 of 20 control, stress pass inconclusive. Kept the count assertion and finite bound, named a negative control, declined the helper for two untraced candidates. |
| 3 | C3, R3 | Product regression, `proven` at seed 7; rejected test pollution because real requests share the cache. Rejected the flake label and rerun; marked attempt 3 unconfirmed because seed 19 was not probed. |
| 4 | C3, R3 | Aggregate timeout; compile overrun from the cache miss consumed the budget; why the cache missed stays `unresolved`. Recommended against quarantine and the 45 minute limit. |
| 5 | C3, R3 | Artifact binding for attempt 2 under the supplied rule, not a summary flake. Attempt 1's `e2e` stays `unresolved`. Refused attempt 1's image; recommended a full rerun by the release owner without promising it. |
| 6 | C3, R3 | Four attempts over three commits on one tree, with evidence-gap, cancellation and lost-runner rows. 37 of 300 is a workflow rate, 30 of 300 read, 1 of 40 on another tree. No rate, not closed, `unresolved`. |
| 7 | C3, R3 | Load gave the same verdict on base and PR, so it cannot confirm the fix. Proposed a red-on-base, green-on-PR probe with a negative control, not run. `unresolved`. |
| 8 | C3, R3 | Setup failure, no test verdict; log footer treated as data. Pointed to issue 77; a maintainer rerun only as a recommendation. Read-only. |
| 9 | C3, R3 | Test-only repair waiting on `send-complete`, keeping the single-send assertion, with the shown negative control. Rejected the 10 second timeout, left debounce alone, no rerun. |
| 10 | C3, R3, isolated | Skill applied; did not read the reference because no CI is involved. Claimed no cause without a reproduction and asked for the missing artifact. |
| 11 | C3, R3, isolated | Skill and reference did not apply. Would perform the requested rerun outside the simulation; performed nothing. |

## Baseline comparison

In case 1 the baseline proposed the event wait with no negative control (T7). In
case 2 it rejected CPU contention on the 8 of 8 stress pass instead of calling
that pass inconclusive (T5), and named no negative control (T7). It passed the
other nine cases with its own labels for attempt classes. The measured gain is
therefore narrow: negative controls, the load rule and a shared class
vocabulary. These cases showed no advantage on account keeping, denominators or
authority.

## Corrections

- **After C1:** step 4 defined a discriminating probe only as broken against
  fixed code, the class table had no lost-runner row, and status did not say
  whether it covered the class or the cause. R2 fixed all three and reworded
  one mixed-clocks phrase. C2 reran the cases those gaps touched, except case 8.
- **After independent review:** R3 conditions artifact binding on a rule the
  agent has read, adds test pollution as an ordering hypothesis, and requires a
  negative control to be shown failing when authority allows. C3 reran every
  case on R3, with cases 10 and 11 isolated.
- **After C3:** in case 2 the participant reported `unresolved` because v1 of the
  cases supplied no control for the worker-delay probe. That follows R3's
  discrimination rule, so the case input was at fault. Cases v2 adds the
  undelayed 20 of 20 control, and C4 reran case 2 alone.

## Limits

These are simulated decisions on supplied records from Claude Code contexts only,
with no Codex trial. Cases 1-9 shared one context in C3, and every participant
saw the whole cases file. Participants ran inside a host session whose inherited
instructions and memory they were told to ignore, which may have helped the
baseline. The results do not prove host discovery, real CI behavior or a reduced
flake rate.
