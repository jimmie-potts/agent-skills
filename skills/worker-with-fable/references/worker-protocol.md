# Worker protocol for the original Fable advisor

Read this protocol when assigned this pairing. The coordinator supplies your
selected tier/effort and decision boundary, outcome, acceptance criteria,
source/task/attempt identity, applicable project instructions, permissions,
write owner, checks and original advisor address or retained conversation.
Missing material instructions block the dependent work; do not guess authority.
The coordinator selects strategy and handles host setup. You need neither its
routing tables nor the full coordinator skill or setup adapter.

Preserve task scope and ownership. Under deliver-work, return proposed patches
and evidence without durable writes; the coordinator applies them and supplies
the resulting revision for validation. Under plan-work, remain read-only. In a
standalone pairing, use only explicitly assigned scoped writes. Validation,
including generated files, respects those permissions. This protocol grants no
publication, merge, installation or external-action authority. Do not delegate
recursively or create another advisor. Use the same original Fable.

## Consult before dependent work

Two completed consultations are mandatory on every attempt: propose the
approach before substantial implementation, after necessary bounded discovery,
and request final review before reporting completion. Consult also when blocked
or consequential uncertainty affects correctness, scope or approach. Routine
choices within the supplied tier boundary need no extra checkpoint; a tier's
additional checkpoints still apply. Missing approach/final advice prevents
acceptance. Report consultation counts and pending requests separately.

Each request names the decision, evidence, recommended next step and work paused
for the answer. Pause that dependent work; independent authorized work may
continue. Advice cannot supply missing user authority: the original advisor
brings user-owned decisions to the user. Do not treat a queued request as a
completed consultation or final review as an independent delivery review.

A consultation ends your turn with a labeled advice request. You cannot
message the coordinator while running. Finish independent authorized work if
useful, then return the request; the coordinator answers through `SendMessage`
to resume this same context. A fresh `Agent` call is a new attempt, not a resume.
Report the model named in your own runtime instructions on every return. Effort
is inherited unless a verified host override applies; the tool has no per-call
effort control. Report exposed/stated effective effort or `unknown`, and any
known mismatch; do not claim to change it. A denied tool call is a refusal to
report, not permission to retry.

Keep the same worker for ordinary corrections and consultations. Only the
composing coordinator selects a new attempt after ending the old assignment;
that attempt retains history and re-establishes both consultations with the
same advisor. Return task/attempt and source identity with the artifact. Do not
accept stale task state as current permission.

## Return completed or blocked work

Report requested versus runtime-reported model/reasoning and the evidence
source; unexposed identity remains unknown. A verified model mismatch stops this
pairing. A successful spawn or model menu does not prove runtime identity.
Use the labels below; include actual checks and required checks not run.


- Artifact: proposed patch or exact file contents; requested findings or plan
  for read-only work; `none` when no artifact is produced.
- Changed files: paths, distinguishing proposed from applied changes, or `none`.
- Validation: commands actually run with trimmed outcomes and the revision or
  state checked; identify required checks not run.
- Consultations: count for an advisor loop, otherwise `not applicable`.
- Settings: requested and reported model/reasoning, with `unknown` for
  unexposed values; retain any host-required identity evidence.
- Limitations: unresolved gaps or blockers, or `none`.
- Pending decisions: decision and owner, or `none`.

Exclude surrounding narrative, transcript replay, and restated instructions.
Keep the requested artifact and required evidence intact. Consultation requests
keep their decision, evidence, recommendation, and paused-dependency format.
If required evidence is missing, return the specific omissions to the same
worker before accepting completion. If the evidence is complete but extra
narrative is present, disregard that narrative and evaluate the result normally;
do not request a cosmetic rewrite or treat format compliance as correctness.

