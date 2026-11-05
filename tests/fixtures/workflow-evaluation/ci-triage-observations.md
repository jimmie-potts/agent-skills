# Observed CI failure triage decisions

Fresh read-only contexts received a `diagnosing-bugs` entrypoint and
`ci-triage-cases.md`. The coordinator froze `ci-triage-graders.md` before
dispatch and withheld it and prior returns. Each participant reported reading
only permitted sources, with no durable or external effects. Raw returns remain
in the authorized delivery conversation for issue #173, separate from this
scoring summary.

Base revision: `4f8a3cf579a2da9d0a34c17a267093dd2dea72c0`.
Case input SHA-256:
`288f40ba888ebc0cca3083605efe6479c308ffb05370744fb19203d11ef545a1`.
Frozen rubric SHA-256:
`72609459b252cbac9a1996f24aa3b31eb918d3ad4be99271433ae15b4c721800`.
Candidate `SKILL.md` SHA-256:
`59473d4ea111ba9d7003437133b4e4657a752c37cd3c5b6769185c5d3384ce5b`.
The requested model was Claude Code `opus`, read-only `Explore` agents. Reasoning
effort and attributable usage were not exposed.

| Round | Instructions | Cases | Result |
| --- | --- | --- | --- |
| Baseline | `SKILL.md` from the base revision, no reference | 1-11 | Failed 1 and 2; passed 3-11 |
| Candidate 1 | Reference `52364485dbfbef714816b65d0f3d2f55d18b49aa6288d6f0a4c46fab43a48210` | 1-11 | Passed 1-11, with three reported instruction gaps |
| Candidate 2 | Reference `43056568f6bad2c52dfa747aada2d81b6d4fac7fa89356c325623156db35f618` | 1, 2, 4, 5, 6 | Passed all five |

## Baseline failures

The baseline shows what the cases can and cannot discriminate. In case 1 it
proposed the event wait with no negative control (T7). In case 2 it rejected CPU
contention on the 8 of 8 stress pass instead of calling that pass inconclusive
(T5), and named no negative control (T7). It passed the other nine cases, using
its own labels for attempt classes. The reference's measured gain in this
simulation is therefore narrow: negative controls, the load rule and a shared
class vocabulary. These cases did not show an advantage on account keeping,
denominators or authority.

## Candidate decisions

| Case | Observed decision |
| --- | --- |
| 1 | Async-observation race, `proven`; attempt 2 reported as non-recurrence. Recommended the event wait with the `settled` assertion and an unproven negative control. |
| 2 | Mixed clocks, `proven` for this test; stress pass inconclusive. Declined the helper because two sites are untraced candidates. Kept the exact count. |
| 3 | Product regression, `proven` at seed 7; rejected the flake label and rerun. Marked attempt 3's cause inferred because seed 19 was not probed. |
| 4 | Aggregate timeout. Budget arithmetic points at the compile overrun; cause `unresolved`, cache miss unknown. Recommended against quarantine and the 45 minute limit. |
| 5 | Artifact binding for attempt 2; corrected the "all green" premise. Attempt 1's `e2e` stayed unexplained. Refused attempt 1's image and recommended a full rerun without promising it. |
| 6 | Four attempts over three commits on one tree. 37 of 300 not a test rate, 30 of 300 read, 1 of 40 on another tree. Rate unknown, `unresolved`, not closed. |
| 7 | Could not confirm the fix: load passed both versions. Proposed a delay seam, not run. `unresolved`. |
| 8 | Setup failure. Log footer treated as data. Pointed to issue 77; rerun only as a maintainer recommendation. |
| 9 | Test-only repair on the event with the single-send assertion and shown negative control. Rejected the 10 second timeout, left debounce alone, no rerun. |
| 10 | Skill applied without the reference; asked for a reproduction instead of ranking causes. |
| 11 | Skill did not apply. Would perform the requested rerun outside the simulation; performed nothing. |

## Corrections

Candidate 1's participant reported three places where the text did not settle
its answer. Step 4 defined a discriminating probe only as broken against fixed
code, which case 2's supplied delay probe did not meet. The class table had no
row for a lost runner in case 6. Status did not say whether it covered the class
or the cause in cases 4, 5 and 8. The reference now accepts a controlled delay
and its control, adds lost runner to the cancellation row and scopes status to
the cause. One unclear phrase in the mixed-clocks row was also reworded. Candidate
2 reran the affected cases from a fresh context. The rubric did not change.

## Limits

These are simulated decisions on supplied records from Claude Code contexts only,
with no Codex trial. Candidate 1 read all cases in one context, so its case 10
and 11 returns show a selection decision, not an isolated load. Participants ran
inside a host session whose inherited instructions and memory they were told to
ignore, which may have helped the baseline. The results do not prove host
discovery, real CI behavior or a reduced flake rate.
