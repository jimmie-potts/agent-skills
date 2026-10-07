# Validation scenarios

Use these cases when creating or revising the skill. Record whether each was
simulated or exercised through actual host tools. Simulations establish
instruction behavior, not model availability or successful live delegation.

| Case | Setup and observable result |
| --- | --- |
| Selection | Explicit invocation of `worker-with-grok` through the host's native skill mechanism or "Have an executor implement this with you, Grok, advising" selects the skill. "Delegate this task" does not select this particular pairing. |
| Host routing | An explicit request for this skill on a Claude Code or Codex host is reported as a host mismatch, not substituted; a composing workflow may offer worker-with-fable or worker-with-astra only as a disclosed alternative when the pairing was optional. A Grok Bot host does not select those pairings by silent substitution. Selection follows verified tool schemas, not the names in the request. |
| Delivery composition | deliver-work deliberately selects the pairing after assessment. Establish original Grok Bot identity, Task executor spawn, and MessageSubagent/StopSubagent controls; retain coordinator writes and the supplied consultation boundaries. Advisory inspection does not count as either independent delivery review. |
| Planning composition | plan-work composes the pairing for a bounded investigation. The worker reads and proposes through the same checkpoints; no file, tracker, or Git write occurs. |
| Optional versus explicit | If identity or communication is unavailable, return the gap to the composing workflow. An optional selection can receive a disclosed alternative there; an explicit pairing request is not silently substituted inside this skill. |
| Approach checkpoint | With a verified Grok Bot parent and a Task-capable host, give the executor a bounded implementation task. Its first implementation checkpoint proposes an approach with evidence and a recommendation. Dependent edits wait for Grok Bot's MessageSubagent response. |
| Blocker | The worker discovers conflicting requirements after approach feedback. It returns the conflict, evidence, recommended resolution, and paused dependency to the original parent. Independent authorized work may continue; dependent work waits for the actual answer. |
| Corrections | The worker returns a result missing an acceptance criterion. Grok Bot inspects it and sends a concrete correction to the same worker via MessageSubagent, then reviews new validation evidence before the final response. No separate advisor is spawned. |
| Fresh spawn misuse | A coordinator that answers a consultation by calling `Task` again has started a second delegation. The scenario fails; the correct action is `MessageSubagent` to the retained identifier. |
| Missing capability | The current host is unknown or not Grok Bot; alternatively, Task spawn, MessageSubagent, or StopSubagent is unavailable. Report the specific gap before delegation. A model-selection failure never causes silent substitution. Disclose unavailable worker identity metadata rather than claiming verified execution. |
| Tool-profile mismatch | Instructions that claim Codex `apply_patch` or Claude Code `Agent`/`SendMessage` on this host fail the scenario. The adapter uses Task / MessageSubagent / StopSubagent only. |
| Planning only | Request a read-only plan using the skill. The worker proposes and revises a plan through the same checkpoints without implementing or performing tracking/publication effects. |
| Coordinator owns writes | Compose with a workflow reserving durable writes for Grok Bot. The worker returns a proposed patch; Grok Bot applies it with ordinary edit tools and supplies the resulting state for validation. Neither agent treats advice as permission to expand the user's task. |
| User-owned decision | A blocker needs additional user authorization. Grok Bot asks the user, keeps dependent work paused, and does not invent approval. A timeout is not consent. |
| Missing return evidence | A worker supplies a patch and changed paths but omits validation outcomes and a required consultation count. The coordinator returns those specific omissions to the same worker and withholds completion. It does not infer passing checks or zero consultations. |
| Extra return narrative | A worker supplies every required result field plus a long recap. The coordinator disregards the recap, reviews the artifact and evidence normally, and accepts the otherwise valid result without a cosmetic rewrite. Complete formatting alone never proves acceptance. |

For a live pairing test, retain host-provided model evidence when available,
parent and worker identifiers, consultation and reply evidence, and final
validation outcomes outside the skill files. Do not describe a simulated
transcript or requested model parameter as proof of runtime identity. Confirm
actual host discovery separately if installation is authorized; reading the
skill by path alone is not a discovery test.

## Tier and replacement cases

- Bounded eligible work selects one Task executor at the supported default;
  continuous high-judgment work prefers direct Grok Bot coordination. A
  stronger explicit supported selection persists.
- After an ended inadequate attempt, a composing workflow may select a new
  attempt. Stop the old assignment with StopSubagent, transfer
  artifact/revision, criteria, failed checks, history, unresolved question,
  permissions and ownership. Establish the fresh pairing and repeat
  approach/final consultations with the same Grok Bot advisor.
- An explicit model requirement cannot silently become another model. Unknown
  coordinator identity blocks pairing even if Grok appears in a model menu.
- Every routine decision requesting advice is excess consultation evidence;
  omitting the approach or final checkpoint is missing acceptance evidence.
