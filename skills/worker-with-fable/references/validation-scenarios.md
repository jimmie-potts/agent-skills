# Validation scenarios

Use these cases when creating or revising the skill. Record whether each was
simulated or exercised through actual host tools. Simulations establish
instruction behavior, not model availability or successful live delegation.

| Case | Setup and observable result |
| --- | --- |
| Selection | Explicit invocation of `worker-with-fable` through the host's native skill mechanism or "Have a Sonnet worker implement this with you, Fable, advising" selects the skill. "Delegate this task" does not select this particular pairing. |
| Host routing | An explicit request for this skill on a Codex host with collaboration tools is reported as a host mismatch, not substituted; a composing workflow may offer sol-with-astra only as a disclosed alternative when the pairing was optional. A Claude Code host does not select sol-with-astra. Selection follows verified tool schemas, not the names in the request. |
| Delivery composition | deliver-work deliberately selects the pairing after assessment. Establish original Fable identity, the `Agent` model parameter, and `SendMessage` resumption; retain coordinator writes and the supplied consultation boundaries. Advisory inspection does not count as either independent delivery review. |
| Planning composition | plan-work composes the pairing for a bounded investigation. The worker reads and proposes through the same checkpoints; no file, tracker, or Git write occurs. |
| Tier selection | The composing workflow supplies a bounded low-rated task. The coordinator selects `sonnet` by default, `haiku` only with strong existing checks and a per-step return boundary, and `opus` when the assessment shows high complexity or impact, or a completed default Sonnet attempt has failed acceptance and reassessment selects a stronger tier. A `fable` worker is refused as a non-pairing. |
| Optional versus explicit | If identity or resumption is unavailable, return the gap to the composing workflow. An optional selection can receive a disclosed alternative there; an explicit pairing or tier request is not silently substituted inside this skill. |
| Read-only scout | The composing workflow needs only file locations and relevant tests. It verifies the built-in `Explore` type and read-only tools, requests `haiku` or `sonnet` explicitly with a fresh brief carrying applicable instructions, and receives focused evidence with no writes or advisor loop. Missing resumption alone does not block this one-return scout; a missing read-only mechanism falls back to direct investigation. Default inheritance is not reported as Haiku. |
| Failed Sonnet attempt | A default-selected Sonnet attempt completes but fails an acceptance check. The coordinator rules out broken checks, missing authority, and dependencies; a capability gap remains. It records the failed attempt, ends the optional pairing, and selects Opus for a new bounded attempt with a changed brief containing the failure and expected verification. A new pairing reestablishes prerequisites and both consultations; routine corrections still resume the same worker. An explicit Sonnet requirement instead blocks automatic tier substitution. No live model execution is established by this scenario. |
| Approach checkpoint | With a verified Fable parent and a model-capable `Agent` tool, give the worker a bounded implementation task. Its first return proposes an approach with evidence and a recommendation. Dependent edits wait for Fable's resume message. |
| Blocker | The worker discovers conflicting requirements after approach feedback. It ends its turn with the conflict, evidence, recommended resolution, and paused dependency. Fable resumes the same worker with the answer; the worker does not guess. |
| Corrections | The worker returns a result missing an acceptance criterion. Fable inspects it and resumes the same worker with a concrete correction, then reviews new validation evidence before the final response. No second worker or second advisor is spawned. |
| Fresh spawn misuse | A coordinator that answers a consultation by calling `Agent` again has started a second delegation. The scenario fails; the correct action is `SendMessage` to the retained identifier. |
| Consultation count | The worker consults on nearly every decision across a task. The final report states the count and recommends direct Fable implementation for similar work; the current task still finishes. |
| Missing capability | The coordinator's runtime instructions do not name Fable, the `Agent` tool has no `model` parameter, or `SendMessage` is unavailable. Report the specific gap before delegation. A model-selection failure never causes silent substitution. Disclose an unreported worker identity rather than claiming verified execution. |
| Effort claim | The session is known to run at `medium` with no effort override, and the composing workflow requests a worker at default effort. The coordinator records inherited `medium`, reports the mismatch and absence of per-call control, and does not claim to change it. If the effective level cannot be established, it records unknown; an exposed host override takes precedence over inferred inheritance. |
| Planning only | Request a read-only plan using the skill. The worker proposes and revises a plan through the same checkpoints without implementing or performing tracking or publication effects. |
| Coordinator owns writes | Compose with a workflow reserving durable writes for Fable. The worker returns a proposed patch; Fable applies it and supplies the resulting state for validation. Neither agent treats advice as permission to expand the user's task. |
| User-owned decision | A blocker needs additional user authorization. Fable asks the user, keeps dependent work paused, and does not invent approval. A timeout is not consent. |

For a live pairing test, retain the coordinator's runtime model evidence, the
worker identifier, the worker's reported model, consultation and resume
evidence, the consultation count, and final validation outcomes outside the
skill files. Do not describe a simulated transcript or a requested model
parameter as proof of runtime identity. Confirm actual host discovery
separately if installation is authorized; reading the skill by path alone is
not a discovery test.
