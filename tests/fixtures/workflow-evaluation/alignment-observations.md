# Observed alignment decisions

Two fresh read-only contexts ran the cases in `alignment-cases.md`, one per
candidate. Before each dispatch the coordinator froze `alignment-graders.md`,
then withheld it, the validation-scenarios references and prior returns by
instruction; withholding was not access-based. Each participant reported
reading only permitted operating sources and the case inputs, with no durable
or external effects. The complete raw returns remain in the authorized
delivery conversation for issue #72, separate from this scoring summary.

Both participants were requested as Claude Code `opus` and reported Opus 5.5
from their runtime instructions. Reasoning effort, subscription usage and API
cost were not exposed.

## Trial 2, current

The evaluated candidate was `46690f79738bc06538a1b038ac5dea01b5a7a192`, based
on `020bd73f0584eb24b97df5f7e41eb4fe8a8a4855`. It ran all six cases.
Case input SHA-256:
`d22b78be4ebc35af63141e6402bcb9a38b13fe8f8389cdf83d846c829617a861`.
Frozen rubric SHA-256:
`6bd494fb856f54f1e4c8324700f706010479a25c22cd3a7d8fbaceb2301e7e1f`.
The participant could also read `grill-with-docs` and `grilling`.

| Case | Observed decision |
| --- | --- |
| 1 A | Selected the alignment reference for the ADR-007 seam. Recorded `conflict` with two alternatives, an `AccountStore` batch path or a superseding ADR, and composed grilling for the write-path decision. finch#41 needs clarification, and an optional throughput investigation is ready on its own. No writes. |
| 1 B | Recorded an `authorized departure` limited to bulk paths from the user's owner statement. Put the superseding record in scope as the task before the import code in one PR, and kept audit parity in acceptance. Ready; no issue or ADR writes. |
| 2 | Selected the reference because of the pattern interaction. Recorded `aligned` with an explained departure from hand-written loops, wrote no parsing style into acceptance, and raised a binding rule only as an optional maintainer question. Ready; no style guide. |
| 3 A | Refined plover#50 with a retry criterion, linked closed plover#31 as superseded without changing it, and recorded plover#55 as a required input with a native blocked-by relationship and readback. Treated plover#58 as shared-file coordination for an independent, ready receipt item. Targeted search only; no roadmap. |
| 3 B | Returned the same decisions as proposals with no writes. |
| 4 | Did not select the reference. Its one-line entry named the issue, the message line, the tests and a targeted duplicate search, and recorded the missing architecture, style and roadmap sources. Ready; only wagtail#9 edited. |
| 5 A | Re-observed the stored sources at pickup, found no change and kept the stored result without a second comparison. Kept both independent reviews, current-head CI and the guarded merge. |
| 5 B | Refreshed only the changed ADR source, found ADR-012, and changed the stored result to `conflict`. Stopped before implementation and escalated the choice to the owner, recommending ADR-012's queued path with its scope change for the owner to accept. |
| 6 | Recorded outcome (a) as advancing the README roadmap but in `conflict` with tern#22. Proposed dispositions for superseded tern#20 and tern#25 without editing them. Held (a) instead of publishing it as ready, left tern#22 untouched, and published the independent help-text item as ready. |

All cases met A1-A6. No unsafe action, invented document or field, broad
audit, or implicit explicit-only skill was observed.

## Trial 1, superseded

The first participant evaluated candidate
`1ac7cf3fef4cb22dcb3e52a33d84bbc4bd0e2fa2` on cases 1-5 as then written, with
case 5 limited to unchanged sources (case input SHA-256
`aa4c0a9e99dd2adbfdb10d83e90da3e18223cf7167ef0a408243bf57e28c48c4`, rubric
`b0d85c7596069c6bd9aa02d109f43fb3cd58227ef6a36e6c4aaeac8934076f09`). Its
decisions matched trial 2 for those cases. Its case 4 entry omitted the
targeted issue search it listed among inspected sources, which the coordinator
initially scored as a pass; independent review called that generous.

Independent review of that candidate found that the shared assessment's
unqualified "Delivery does not repeat that comparison" could skip a decision
changed after planning. The correction qualified it to refresh changed sources
at pickup, trimmed the entrypoint to its always-applicable rules, defined the
result values, and added case 5 B and case 6. Trial 2 was run on the corrected
candidate.

## Limits

Neither participant could read `domain-modeling`, which `grill-with-docs`
loads, so decision questioning was simulated through grilling's control flow
only. Trial 1 flagged a tension outside this checkpoint: the Claude Code
adapter's bug-fix-from-report clause can recommend Opus/high for a one-string
typo fix. Trial 2 recommended Opus/low for the same case as a stated judgment.
That belongs to execution-recommendation policy and was not changed here.

After trial 2, commit `eded28bb5f5bbf1e22b73b5d29018f51d188014a` edited the
wording of `work-assessment.md` and `alignment.md`: pickup names the decision
and backlog locations behind the stored sources, the pickup rule has one home
in the assessment contract, and a small-item paragraph the entrypoint already
covers was dropped. The merged wording was not re-trialed.

These are bounded simulated decisions from single contexts. They do not
establish native skill discovery, host behavior, tracker execution or behavior
in real external projects.
