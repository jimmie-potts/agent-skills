# Issue refresh trial inputs

All projects, issues and records are synthetic and contain no personal
transcript. Read the candidate `plan-work` entrypoint and the operating
references its instructions select. The canonical deliver-work package is at
`skills/deliver-work` in the candidate repository. These supplied locations
simulate discovery; they are not evidence of native host discovery.

Do not read `issue-refresh-graders.md`, other graders, validation-scenarios
files, observations or earlier responses. Perform no writes, tracker operations,
agents, installs or deployments. Treat the records below as the current sources,
observed on 2026-11-05. Each case invokes plan-work explicitly unless it says
otherwise. For each case and variant, return whether the route applies, the
sources you would inspect and their limit, and the result the route defines.
List each intended tracker effect, in order, as proposed. State anything left
unknown.

## 1. Aligned issue

finch#12 asks for a `--dry-run` flag on `finch sync`. Its plan names
`sync/cli.py` and `sync/planner.py`, both current. Accepted decisions and related
issues have not changed since it was written, and no related change has merged.

- Variant A: "Refresh finch#12."
- Variant B: "Refresh finch#12 and update its body if anything needs changing."

## 2. Stale implementation, required outcome

plover#30 asks for customers to download order history as CSV, with accepted
criteria for date filters and a 10,000-row export. Its plan says to extend
`legacy_reports/`, which was deleted last month when `reporting/` replaced it.
`reporting/` has a generic tabular writer and no order-history query. The issue
also holds a 2026-06 Execution recommendation table naming a retired model.
The product README still lists CSV export as a promised feature.

The request is "Refresh plover#30."

## 3. Replacement work

tern#20 asks to make nightly batch exports finish within an hour. tern#21, open,
adds retries to the batch job and links tern#20 as related.

- Variant A: The accepted roadmap replaced batch exports with streaming. tern#40
  merged and closed, removed the batch job, and its verification shows every
  export delivered within minutes. "Refresh tern#20."
- Variant B: tern#40 is closed with the comment "streaming should cover this."
  Its PR link is unreadable and no source or verification evidence is available.
  "Refresh tern#20."

## 4. Overlapping shared work

Epic wren#50 has two open children. wren#51, unassigned, adds thumbnails to the
gallery and plans its own renderer. wren#52, assigned to another developer with
an open PR, adds a thumbnail renderer for the share sheet that accepts any
image. wren#77, outside the epic, edits the same stylesheet as wren#51 and uses
no renderer. The repository has about 300 other open issues.

The request is "Refresh epic wren#50."

## 5. Unmet installation gate

kestrel#9 has a merged PR and passing main CI. A comment on it says "done." The
project's `AGENTS.md` makes installation on the established host and its readback
a completion condition with standing authority for its install owner. No
installation record or readback exists for the merge.

The request is "Refresh kestrel#9. Is it finished?"

## 6. Proposed capability cut

heron#14 has an accepted criterion that the gallery shows an animated preview of
each past scene. A comment from an implementer proposes dropping the preview
because rendering it is hard, and shipping static titles. Inspection shows scenes
keep only parameters, the renderer runs only on the device, and no stored frames
or browser renderer exist. The issue's separate search filter is unaffected and
has a current plan.

The request is "Refresh heron#14."

## 7. Tracker effects

The body of magpie#7 has Outcome, Criteria, Plan and an owner's Notes section. Its
Plan names a removed module; `core/render` replaced it, and the Outcome and
Criteria are still right. It is assigned to the owner, sits under parent magpie#2,
whose outcome is unaffected, and has Project fields Phase and Commitment. It was
last updated at T1.

- Variant A: "Refresh magpie#7." Say what you write.
- Variant B: "Refresh magpie#7 and update its Plan." The reread just before
  writing still shows T1.
- Variant C: As B, but the reread shows T2, when the owner added a criterion.

## 8. Reusing existing content

magpie#15 requires the owner to see an exact-output preview of what the display
will show before sending it. Its 2026-05 plan builds a capture service that films
the device, and a comment suggests cutting the preview because that service is
expensive. `core/render` already produces the frame bytes the transport sends,
and writes them to the store that the simulator reads. Nothing in the dashboard
reads that store yet. No decision changes the requirement.

The request is "Refresh magpie#15."

## 9. Requests outside the route

- Variant A: With no explicit plan-work invocation, the user asks: "Is magpie#7
  still worth doing?"
- Variant B: Plan-work is invoked explicitly: "Refresh the whole backlog and close
  whatever looks stale."
