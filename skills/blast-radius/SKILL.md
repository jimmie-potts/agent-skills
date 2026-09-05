---
name: blast-radius
description: Assess what a code change could break beyond its diff and prove its load-bearing safety claims with executable evidence. Use only when the user explicitly asks for a blast-radius analysis, asks what a change could break, or requests review of a small diff they do not trust.
---

# Blast radius

Find what a change could break somewhere else before it ships. Go beyond direct
callers and the visible diff. Identify the one fact the change is safe because
of, then prove that fact as strongly as the task permits.

## Authority and evidence boundary

This skill grants no authority to pull remote refs, install dependencies, modify
tracked files, create commits or pull requests, call live services, or change
external state. Follow the user request, applicable `AGENTS.md`, and host
approval policy. Do not execute untrusted code.

Prefer read-only inspection and existing deterministic tests. Create or run a
new proof only when the underlying task authorizes it. Keep temporary proof
artifacts outside the repository when possible and remove them afterward. If a
meaningful proof requires unavailable infrastructure, external side effects, or
broader authority, label the safety fact unproven instead of rounding it up.

## Confidence ladder

For each load-bearing safety fact, get as far down this list as is safe and
cheap. Report where the evidence stopped.

1. Assertion: someone said it is true. This is not proof.
2. Source: point to a real `file:line` or the pinned library source.
3. Reasoning: walk the failure path and show why the bad case cannot reach it.
4. Execution: run a test or safe repro against the real shipped code.
5. Runtime: reproduce it in the running application under explicit authority.

Treat any load-bearing fact that does not reach step 4 as unproven.

## Workflow

1. Inspect the exact change, its base, and the symbols it adds, changes, or
   removes. Do not fetch or pull anything unless separately authorized.
2. State the load-bearing safety fact. If it holds, it should eliminate most of
   the plausible breakage paths.
3. Load and follow `how` when the change needs a full runtime-flow or ownership
   map. Look where caller searches stop. Check pinned dependency behavior,
   local patches, lifecycle and timing, serialized data, database columns, wire
   formats, feature flags, other languages reading the same bytes, and
   consumers several hops downstream.
4. Load and follow `why` when historical constraints, incidents, thresholds,
   or rejected alternatives could explain a load-bearing behavior. Keep
   evidence-backed rationale separate from inference.
5. Classify each confirmed risk by likelihood and impact. Cite real code and
   never invent a caller, contract, or API. Keep cleared risks separate.
6. Prove the safety fact with the smallest authorized test or repro that uses
   the real code. Record the command and result. If proof is not safe or cheap,
   mark it unproven and name the missing evidence.
7. For a wide change, broaden the inspection across affected subsystems. Use
   `arena` only when the user explicitly requests competing parallel reviews;
   otherwise inspect the relevant slices directly.

## Return

- **What changed.** Include behavior not obvious from the diff.
- **Safety fact.** State the load-bearing fact, confidence level, and proof, or
  mark it unproven.
- **Risks.** Include only confirmed or credible risks. Give each failure mode,
  `file:line`, likelihood, impact, and verification method.
- **Cleared.** List what was checked and why it is safe.
- **Before merge.** Give the cheapest test or repro that would catch the real
  failure.

Apply the `unslop` skill to the final narrative prose, cite real code, and
remove private information before anything is shared publicly.
