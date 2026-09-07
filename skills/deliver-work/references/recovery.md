# Reconcile uncertain effects

Use after a timeout, disconnect, ambiguous response, partial effect or failed
readback. Keep the effect's intent, object, expected prior state, guard and known
identifiers in the task or existing record. Suspend mutations that depend on
its result; continue independent authorized work.

Inspect authoritative source history, PRs, refs, checks or other relevant state.
A cached, delayed or incomplete read does not prove the effect was absent.
Classify the result before recovery:

- Applied: retain the resulting identifier and continue without repeating it.
- Verified not applied: repair within scope and retry with fresh prerequisites
  and guards if still authorized.
- Partial: reconcile the completed portion before performing the remainder.
- Unknown: keep dependent mutations paused and request the specific missing
  access or decision when needed. Do not duplicate an effect to probe its state.

For definite failures with no effect, make routine scoped repairs and rerun the
failed step without inventing another approval gate. Scope changes, conflicting
policy and actions beyond existing authority still require a decision.

A successful merge followed by failing post-merge CI is incomplete delivery.
Retain open or established waiting tracking state, report the failure and its
owner, and repair only within the authorized scope. Do not close the issue just
because merge succeeded, or automatically reopen issues closed by another actor
without reconciling their disposition.
