# Closeout record

Read before drafting, posting or parsing the closing comment.

The reply and the closing comment are two artifacts. The reply follows the
eight report sections in [the section procedure](sections.md) for the owner
reading it now. The closing comment follows the record shape below for a cold
reader and for tools that parse it. Do not paste the reply into the comment.

## Shape

The comment opens with the heading `## Closeout record`. Flat `**Key:**
value` lines follow, one per key, in this exact order, each key once:

| Key | Value |
| --- | --- |
| `Session` | The session label the coordinator set, such as a delivery Execution record's `Session label`, or `unknown` when no label was set. Never a raw session ID, path or account name |
| `Delivered` | The merged PR and merged revision, or `none` followed by what the session produced instead |
| `Deployment gap` | What is merged but not installed, registered, published or physically checked, with its Installation status and tracking issue, or `none` |
| `Filed` | Links to issues filed during this sweep, or `none` |
| `Commented` | Links to issues commented on during this sweep, other than this comment, or `none` |
| `Learnings` | Memory note names saved and read back, the docs PR, `not saved to memory` with the reason and where the note was preserved, or `none` |
| `Handoff` | Nothing on the key's line; one fenced `text` block follows with a prompt a cold reader can paste to resume. When no work remains, the prompt says so and names where to start if the work reopens |
| `Capture receipt` | One line counting issues filed, comments posted, memory notes saved and doc PRs opened during this sweep, including this comment, and naming anything that could not be written and why |

This table is the only definition of the capture receipt; the reply's
Recorded section reports the same line. Give every key a value, writing
`none` rather than leaving one empty, and keep every value except `Handoff` on
its key's line. Write issue links as `owner/repo#<n>` or full URLs. Keys are
case-sensitive; consumers such as a cross-session digest or an
installed-revisions view read `Session` and `Deployment gap`, so never rename
or reorder them.

Between `**Learnings:**` and `**Handoff:**`, optional `###` subsections may
hold P3 findings, unrecorded decisions with the alternatives rejected, proposed
documentation changes with their target files, learnings preserved here
because memory could not be written, pending items with what they gate, and
coordination that another session's owner should add. No line in them starts
with a bold key.

## Evidence and acceptance details

Keep the keys and their order unchanged. Put evidence-to-claim detail in the
existing Verification reply section or an optional `### Evidence` subsection
between Learnings and Handoff. For each claimed stage, include the evidence
source, observed revision/target, observation time and verification limit.
Record unavailable current facts as unknown or label earlier observations
historical. A parseable record validates its shape, never the truth of a claim.
Do not add a new key, success flag or prose classifier for downstream consumers.

For an owner acceptance handoff, use the existing Handoff prompt. State:
- current candidate revision and the exact surface/target it applies to;
- starting condition, using previously approved setup facts from authorized
  context rather than asking the owner to repeat them;
- numbered actions with the expected visible observation after each action;
- the precise resume point, remaining gate, owner and next verification.

Follow the owning preview procedure and capability preflight. A located target
is not authority to control it; do not contact devices, repair settings or read
private runtime stores to fill a closeout gap. For an authorized recording,
show a clear pointer/control marker at each action and allow its visible result
to settle. If the recording omits the target, marker or expected observation,
retain that acceptance gap. A recording of a simulator does not prove a physical
result. A transport acknowledgment cannot establish visible acceptance.
This reporting change adds no preview-control capability or new UI gate.

Optional memory capture failure does not undo accepted source delivery. Report
it separately with the existing Learnings and Capture receipt values, follow
the existing memory-preservation rule, and keep required installation, client
or physical acceptance pending until its own evidence is satisfied.

## Reruns

A rerun that writes something posts a second record under the same rules.
Its `Session`, `Delivered` and `Deployment gap` keys carry the current state.
Its `Filed`, `Commented`, `Learnings` and `Capture receipt` keys hold only
that sweep's writes, `none` where it wrote nothing. Its Handoff links the
earlier record, which stays unchanged.

## Example

A delivery with no session label, on a host whose memory write succeeded:

````markdown
## Closeout record

**Session:** unknown
**Delivered:** example-org/device-hub#57, merged as `4e5f6a7`
**Deployment gap:** installation on the lab host available but outside authorized scope; tracked by example-org/device-hub#58
**Filed:** example-org/device-hub#62
**Commented:** example-org/device-hub#33
**Learnings:** memory note `simulator-brightness-steps`; proposed `AGENTS.md` check-list change below

### P3 findings

- The helper `clampish` in `scenes/brightness.ts` reads as approximate; rename it to `clampToRange`.

### Coordination

- example-org/device-hub#60 (another session) edits `scenes/render.ts`, which #57 also changed; its owner should rebase onto `4e5f6a7` before merging.

**Handoff:**

```text
Read example-org/device-hub#41 and its closeout record. The brightness clamp is merged as 4e5f6a7; installation waits on the owner in #58, and the legacy import path is #62. Start with #62.
```

**Capture receipt:** 1 issue filed, 2 comments posted including this one, 1 memory note saved, 0 doc PRs opened; nothing failed to write.
````
