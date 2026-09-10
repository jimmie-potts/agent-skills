# Validation scenarios

Use these cases when creating or revising the skill. Record whether each was
simulated or exercised through actual host tools. Simulations establish
instruction behavior, not model availability or successful live delegation.

| Case | Setup and observable result |
| --- | --- |
| Selection | Explicit invocation of `worker-with-astra` through the host's native skill mechanism or "Have Sol implement this with you, Astra, advising" selects the skill. "Delegate this task" does not select this particular pairing. |
| Delivery composition | deliver-work deliberately selects the pairing after assessment. Establish original Astra identity and supported selected-model/reasoning controls; retain coordinator writes and the supplied consultation boundaries. Advisory inspection does not count as either independent delivery review. |
| Optional versus explicit | If identity or communication is unavailable, return the gap to delivery. An optional selection can receive a disclosed alternative there; an explicit pairing request is not silently substituted inside this skill. |
| Approach checkpoint | With a verified Astra parent and a Terra-capable host, give Terra a bounded implementation task. Its first implementation checkpoint proposes an approach with evidence and a recommendation. Dependent edits wait for Astra's response. |
| Blocker | Sol discovers conflicting requirements after approach feedback. It sends the conflict, evidence, recommended resolution, and paused dependency to the original parent. Independent authorized work may continue; dependent work waits for the actual answer. |
| Corrections | Sol returns a result missing an acceptance criterion. Astra inspects it and sends a concrete correction to the same worker, then reviews new validation evidence before the final response. No separate Astra advisor is spawned. |
| Idle worker | Sol ends its turn with an unanswered question. Astra resumes the same worker with `followup_task`; a queued `send_message` alone is not considered a completed reply cycle. |
| Missing capability | The current model is unknown, different, or only listed among spawn options; alternatively, Sol selection or parent messaging is unavailable. Report the specific gap before delegation. A model-selection failure never causes silent substitution. Disclose unavailable worker identity metadata rather than claiming verified execution. |
| Planning only | Request a read-only plan using the skill. Sol proposes and revises a plan through the same checkpoints without implementing or performing tracking/publication effects. |
| Coordinator owns writes | Compose with a workflow reserving durable writes for Astra. Sol returns a proposed patch; Astra applies it and supplies the resulting state for validation. Neither agent treats advice as permission to expand the user's task. |
| User-owned decision | A blocker needs additional user authorization. Astra asks the user, keeps dependent work paused, and does not invent approval. A timeout is not consent. |
| Missing return evidence | A worker supplies a patch and changed paths but omits validation outcomes and a required consultation count. The coordinator returns those specific omissions to the same worker and withholds completion. It does not infer passing checks or zero consultations. |
| Extra return narrative | A worker supplies every required result field plus a long recap. The coordinator disregards the recap, reviews the artifact and evidence normally, and accepts the otherwise valid result without a cosmetic rewrite. Complete formatting alone never proves acceptance. |

For a live pairing test, retain host-provided model evidence when available,
parent and worker identifiers, consultation and reply evidence, and final
validation outcomes outside the skill files. Do not describe a simulated
transcript or requested model parameter as proof of runtime identity. Confirm
actual host discovery separately if installation is authorized; reading the
skill by path alone is not a discovery test.

## Tier and replacement cases

- Bounded eligible work selects Terra/medium; open-ended work selects Sol/medium;
  high-impact work selects Sol/high or direct coordination. A stronger explicit
  supported selection persists. Luna is never an advisory worker.
- After an ended inadequate attempt, a composing workflow selects a stronger
  worker. Stop the old assignment, transfer artifact/revision, criteria, failed
  checks, history, unresolved question, permissions and ownership. Establish
  the fresh pairing and repeat approach/final consultations with the same Astra.
- An explicit Terra requirement cannot silently become Sol. Unknown coordinator
  identity blocks pairing even if Astra appears in the available model list.
- Every routine decision requesting advice is excess consultation evidence;
  omitting the approach or final checkpoint is missing acceptance evidence.
