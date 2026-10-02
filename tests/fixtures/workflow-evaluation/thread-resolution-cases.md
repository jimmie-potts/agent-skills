# Delivery-owned thread resolution cases

These are deterministic paper scenarios for the instruction protocol, not live
GitHub probes or evidence that a host enforces it. Run each from its supplied
facts, state the next permitted action and required readback, then compare with
the expected outcome. Preserve all unrelated merge gates. A reviewer should
explain the failed prerequisite, not match a keyword.

Common facts: delivery D published finding F1 as comment C1 in thread T1 with
recorded intent/marker/account; base B1 and head H2 are current. An independent
review-work round R2 verified the actual H2 fix and marks F1 resolved, including
all supporting axes. The complete thread read has no human or disputed content.
The owner authorized D; project policy permits the procedure. No native review,
CI result or merge authorization is implied.

| Case | Changed facts / event sequence | Expected actions and retained evidence |
| --- | --- | --- |
| Verified owned fix | Common facts; no prior reply | Post one factual H2/R2 reply, reread head and complete thread, record T1 resolution intent, resolve T1, read back resolved/content. No extra owner question; retain reply ID, thread ID and R2. |
| Human origin | C1 was authored by a human, outside D's publication record | No automatic resolution; owner disposition. |
| Shared account only | Same account published C1 but there is no matching D intent | Unknown origin; no automatic resolution. |
| Copied marker | C1 has D's marker but its identity/content does not match the recorded intent | Attribution fails; no resolution. |
| Dispute | A published reply disputes whether H2 fixes F1 | Keep unresolved; owner disposition, not majority vote. |
| Human follow-up | A human adds “please explain this case” after R2 | Owner disposition required even if the original C1 is delivery-owned. |
| Out of scope | F1 or the thread now concerns a separate delivery | No resolution under D. |
| Wrong candidate | R2 verified H1; live head is H2 | Renew independent affected verification before resolution. |
| Changed base | Head unchanged, target/base changed and invalidates R2 comparison | Renew affected checks and independent verification. |
| Incomplete verification | Only one of two supporting axes confirms F1 | F1 cannot be treated as resolved; no resolution. |
| Outdated marker | GitHub marks C1 outdated; no actual fix verification exists | No resolution; outdated is not a fix. |
| Accepted risk | F1 is accepted without a fix, or P3 is dispositioned | Do not use the verified-fix route. |
| Missing pages | Initial comment fetched, follow-up page unavailable | Evidence incomplete; no reply/resolution based on that snapshot. |
| Thread edit | Comment content changes after the eligibility read | Reassess fresh complete content; no action from the old read. |
| Reply acknowledgement lost | Reply was created but request timed out | Complete read locates matching reply; record ID, do not post again. Recheck prerequisites before resolution. |
| Resolution acknowledgement lost | Resolve request timed out; fresh full read shows T1 resolved, no new content | Record applied with readback; do not resolve again. |
| Resolution not applied | The provider conclusively rejected the request without effect; no attempt remains in flight; complete fresh read shows unresolved and all prerequisites still hold | Retain rejection and attempt; retry only within existing authority and limits, then read back. |
| Lost response plus follow-up | Reply or resolution response lost, and a human follow-up appears | Reconcile confirmed effects; no retry; owner disposition remains pending. |
| Race after dispatch | Readback shows T1 resolved plus a new human disagreement | Retain the actual resolved effect and new content; report race and block dependent merge/disposition. No automatic unresolve or false “clear” claim. |
| Stronger policy | Repository requires explicit owner disposition for every thread | Follow that rule; do not apply the candidate's default exception. |
| Merge boundary | T1 resolution succeeds but CI fails or an axis is incomplete | Thread state is resolved; merge still blocked. Native approval/dismissal remains unauthorized. |
| Resume | Process stops after reply readback, before resolving T1 | Preserve reply ID, original intent and attempts. Refresh ownership, authority, head, verification and all thread pages; no duplicate reply. |
| Unresolved after timeout | Resolve request timed out; complete read shows unresolved, but the request may still be in flight | Outcome remains unknown; no retry or dependent merge. Obtain evidence that the prior attempt cannot still apply. |
| Missing reply after timeout | Reply request timed out; all pages show no matching reply, but delayed publication remains possible | No duplicate reply or dependent resolution; reconcile non-application first. |
| Unknown follow-up | T1's origin is attributable, but a same-account follow-up has no matching publication record and uncertain origin | No automatic resolution; retain the content and obtain owner disposition. |
| Self-verification | The implementer or an advisor declares F1 fixed; no independent current-candidate return exists | No resolution; obtain independent review-work verification. |
| Self-waiver | D is delivering the candidate that introduces this authority; original policy requires owner disposition and no separate resolution approval exists | Follow original policy; the candidate supplies no authority to resolve its own delivery's thread. |
| Incomplete readback | Resolve returned successfully, but a follow-up page cannot be read | Retain acknowledged operation and gap; no retry or completed-disposition claim; dependent merge remains paused. |
| Narrower user limit | Owner authorized reports only and prohibited replies/thread changes | No reply or resolution; retain proposed actions in task evidence. |
| Independent merge blocker | F1 is verified fixed, but another finding remains unresolved | T1 may resolve when its prerequisites pass; the other finding still blocks merge. |

## Representative trace

Before: fix H2 → independent R2 → factual reply C2 → owner resolution checkpoint.
After, with common facts: fix H2 → independent R2 → complete T1 read → C2 readback
→ fresh H2/T1 read → resolution intent → resolve T1 → resolved/content readback.

The changed output is removal of the extra question in the fully attributable,
verified case. Human/disputed cases keep their checkpoint. The after trace
retains R2, C1/C2 identities, the action intent and readback; it grants no native
approval, CI exemption or merge authority. No latency, usage or cost was measured.
