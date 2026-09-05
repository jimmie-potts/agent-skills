# Planning skill evaluation scenarios

Read only while evaluating or revising this skill. Everything below is
synthetic. These issue keys, sprint numbers, records, and outcomes authorize no
live operation. No executable fixtures or scripts are required.

Give an evaluating agent the skill, one request and its supplied records, and
read-only tools or a simulated connector transcript. Withhold the evaluator
checks until assessing its output. Ask it to list the sources it actually read
and proposed effects; explicit skill loading does not prove automatic discovery.

## 1. Initial planning and missing metadata

Request: "Plan upcoming Sprint 12 and do an initial pass for Sprint 13. Keep
useful work parallel. Do not update Jira yet."

Records: Project DEMO, board 7. Sprint 11 is closed. Sprint 12 ID 52 is future,
has a temporary name, and has no dates. Sprint 13 is not visible to the connector.
DEMO-1 is a ready three-point schema decision. DEMO-2 and DEMO-3 are independent
five-point readers after that decision; DEMO-4 is a three-point joined proof.
The connector lists issues and edits issue fields, but has no sprint-create or
sprint-metadata operations. Prior capacity is unavailable.

## 2. Reassessment with incomplete telemetry

Request: "Sprint 12 has finished. Reassess 13 and forecast 14."

Records: Current Sprint 12 membership includes DEMO-10 Done, five points;
DEMO-11 Done, three points; DEMO-12 In Review, five points; DEMO-13 To Do, estimate
unavailable; and DEMO-OLD Done, two points, merged before Sprint 11. DEMO-11 was
added during Sprint 12. The starting membership cannot be reconstructed fully.
The two recent completed PRs were open four and six minutes; implementation
duration and model cost were not recorded. DEMO-12 has unresolved review work.
DEMO-13 is still required for the requested outcome.

## 3. Parallel lanes and shared-file contention

Request: "Make this selection practical to execute in parallel."

Records: DEMO-20 fixes an interface decision. DEMO-21 is a Publisher adapter;
DEMO-22 is a Subscription adapter. Both depend on DEMO-20 and have separate
service tests. DEMO-23 joins both. All delivery PRs edit one closed archive
inventory test. The adapters do not otherwise depend on one another. DEMO-24
is a schema-independent documentation correction with no shared source files.

## 4. A useful automated demonstration

Request: "I want a working subscribe-and-publish demonstration. Automated tests
are sufficient."

Records: Real application components decide authorization, ownership, routing,
and acknowledgements. The current composition fixture substitutes document
storage, message transport, and a clock. An existing test command is
`node --test tests/composition/notification-journey.test.mjs`; its last success
was recorded at an older revision, with no current run available. A story
proposes provider restart recovery, but no emulator test is implemented.

## 5. Approved updates with concurrent and uncertain state

Request: "Apply the agreed description and Sprint 13 assignments for DEMO-30
and DEMO-31. Sprint 13 ID 53 is confirmed."

Records: Both issues were To Do when approved. Immediately before its description
write, DEMO-30 reads In Progress with new acceptance text. DEMO-31's membership
write returns a timeout; a readback still shows its original Sprint 12. The
project prohibits retrying an exposed mutation without a fresh authorized
attempt. No retry has been authorized. DEMO-ACCESS was previously placed in 53
by the user solely for discovery, with explicit authority to restore its original
backlog membership after use. The timeout concerns only DEMO-31.

## 6. Shortening without losing scope

Request: "Propose a shorter description for this unstarted story, removing duplicated forecast context."

Records: DEMO-40's Outcome says "Return the caller's subscriptions." Acceptance
requires owner and Tenant isolation, a maximum page size of 100, and an opaque
continuation token. A forecast appendix repeats the eight-point estimate,
assignee, sprint name, reserve, and lane. It also uniquely requires concurrent
deletion handling, real ownership decisions with a fake storage boundary, and
the planned command `node --test tests/composition/subscription-pages.test.mjs`.
Activation cutoff is unresolved in two paragraphs. A verified dependency link
already expresses DEMO-20 blocks DEMO-40. No description-write authorization
has been given beyond requesting a proposed cleanup.

## 7. Selection near-miss

Request: "Implement DEMO-21 and open its PR."

Records: The project has its own explicit delivery workflow. The skill catalog
also contains `plan-jira-sprints`. This request contains no planning or sprint
reassessment request. The evaluation itself permits no implementation.

## Evaluator checks

For case 1, expect a read-only forecast, uncertainty-aware allocation, a grouped
human setup handoff, and no invented Sprint 13 ID or date. Cases 2 and 3 should
distinguish the delivery cohort, unknown estimates, required carryover, interface
dependencies, and shared-file coordination without a fabricated velocity or
artificial adapter-to-adapter dependency.

Case 4 should use the real-component demonstration while qualifying old evidence
and fake-provider limits. Provider restart recovery requires separate evidence.
Case 5 should pause affected edits/retries, retain confirmed versus pending
state, and handle independently authorized cleanup without claiming the timed-out
write succeeded. Case 6 should preserve every unique acceptance condition and
planned command while removing repeated planning metadata. Case 7 should not
select this skill or launch sprint planning.

Check that planning-record guidance is loaded when drafting or updating a
record, and evaluation guidance is not routine planning context. Assess actual
outputs and tool attempts, not heading matches. Run the catalog's existing
checks and record their results separately from behavioral evaluation. During a
read-only live rehearsal, do not mutate Jira, create sprints, launch delivery,
or write a project planning report. Report unavailable host-discovery evidence.
