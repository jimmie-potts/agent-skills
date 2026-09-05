---
name: arena
description: Run multiple isolated candidate attempts at the same non-trivial artifact, judge them against a task-specific rubric, and synthesize the strongest result. Use only when the user explicitly invokes arena or asks for parallel competing attempts and comparative synthesis.
---

# Arena

Generate independent attempts at the same task, compare every complete result,
choose a base, graft in stronger ideas, and verify one coherent artifact.

## Authority boundary

Invoking this skill authorizes parallel attempts, not broader side effects. This
skill grants no authority to fetch remote state, install dependencies, contact
external systems, expose private data, or make writes. Each candidate inherits
the original task's scope and repository instructions. Do not run untrusted
code.

Use isolated worktrees or temporary directories for authorized file-changing
candidates. Never let candidates write to the same path. Prefer returned text
for prose or analysis tasks that do not require filesystem changes. If the host
cannot run independent candidates, report that limitation; do not simulate an
arena by presenting one attempt as several.

## Phases

Track these phases so none silently disappears: Frame, Fan out, Judge, Pick,
Graft, and Verify.

### 1. Frame

State the artifact to produce and give every candidate the same task contract.
Derive three to six concrete, gradeable criteria from the user's request and
repository constraints. Candidates receive the task and grounding; keep the
rubric for judging so they do not optimize their wording to the scorecard.

Choose enough candidates to explore genuinely different approaches without
wasting work. Do not hard-code model vendors or unavailable runtimes. Assign
each candidate an identity and, when files will change, a separate output path.

### 2. Fan out

Launch all candidates concurrently when the host supports it. Give each the
same task, shared grounding, authority boundary, and required output shape.
Require a short rationale naming alternatives considered and rejected.

If a candidate fails, continue with the remaining candidates when at least two
complete attempts remain. Record every dropout. If fewer than two remain, the
comparison is not an arena; report the limitation or rerun within scope.

### 3. Judge

Read every candidate end to end after it is complete. Score each criterion with
specific evidence. When an independent judge is available within the user's
delegation request, have it score anonymized candidates read-only while the
lead reviews them. Treat the judge as a second opinion, not an authority.

### 4. Pick

Choose the base that best satisfies the rubric and is easiest to extend without
breaking its invariants. Prefer a coherent boundary and smaller surface area
when scores are otherwise tied. Explain disagreements between the lead and any
independent judge before deciding.

### 5. Graft

Inspect each losing candidate again. Port only ideas that materially improve a
rubric criterion. Integrate them into the base's design instead of pasting
mechanically. Record what was grafted, what was rejected, and why.

If candidates converge, record the agreement and keep the coherent consensus.
If they diverge because the task was underspecified, refine the contract and
rerun instead of averaging incompatible designs.

### 6. Verify

Verify the synthesized artifact using the task's normal checks. Arena does not
substitute for tests, review, citations, or readback. If verification fails,
repair from the strongest candidate evidence or rerun with a corrected frame.

## Return

Return one synthesized artifact and a short synthesis note containing:

- the rubric and candidate roster;
- the base and why it won;
- grafts with their source candidates;
- rejected ideas and dropouts;
- judge disagreements or convergence;
- the verification performed and its result.

Apply the `unslop` skill to human-facing prose while preserving the task contract,
rubric, evidence, code, identifiers, and verification results.
