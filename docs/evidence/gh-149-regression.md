# #149 Regression evidence — Grok-compat batch (smaller Acceptance)

**Recorded:** 2026-10-07 (updated for evidence-only #155 + smaller Acceptance)
**Host:** Grok Bot box (`box`, Linux); `gh` as `jimmie-potts`
**Evidence PR:** https://github.com/jimmie-potts/agent-skills/pull/155 — **docs/evidence only** (no product files vs `main`)
**Throwaway combined catalog (local verification only, not shipped in #155):** `9406f09940ec78678eaf4ae4777eeb5d78391c53`
**Base:** `origin/main` @ `3fef618`
**Merge order for product:** #150 → #153 → #152 → #154 (#154 includes #146); then #155 docs
**NO MERGES. NO production `/home/box/agent-data/workflows` install.**

Live smoke report: `/workspace/grok-compat-plan/live-smoke-2026-10-07.md` (also summarized below).

## Sibling product heads (ship via #150–#154, not #155)

| Issue | PR | Branch | SHA |
| --- | --- | --- | --- |
| #144 | #150 | `codex/gh-144-shared-skill-core` | `9ec43b83` |
| #145 | #153 | `codex/gh-145-grok-install-path` | `e37c23f9` |
| #146 | #151 | `codex/gh-146-worker-with-grok` | `d7134e7e` (also in #154) |
| #147 | #152 | `codex/gh-147-plan-work-grok-column` | `22c8b2fe` |
| #148 | #154 | `codex/gh-148-deliver-review-grok-adapters` | `b8cbc452` |

## 1. Catalog / manager checks (throwaway combined tree `9406f099`)

| Check | Result |
| --- | --- |
| `python3 scripts/validate-skills.py` | **PASS** — 37 skills |
| `python3 tests/installed-files-test.py` | **PASS** — 17 tests |
| `bash tests/manage-skills-test.sh` | **PASS** — 49 commands (incl. `--agent grok`; `both` excludes grok) |
| `bash -n scripts/manage-skills.sh` | **PASS** |
| `python3 tests/deliver-work-test.py` | **PASS** |
| `python3 tests/review-work-test.py` | **PASS** — 60 |
| `python3 tests/plan-work-test.py` | **PASS** — 15 |
| `python3 tests/pairing-skills-test.py` | **PASS** — 7 |

Slim evidence-only tip (#155 vs `main`): `validate-skills` **PASS** (36 skills — main catalog); manager tests **PASS** without Grok cases (Grok coverage lives on #153 + combined-tree run above).

## 2. Temp-root install / status / uninstall

Disposable roots only (production installs **not** touched):

- `CODEX_SKILLS_DIR=/tmp/gh149-skills-z630GA/codex`
- `CLAUDE_SKILLS_DIR=/tmp/gh149-skills-z630GA/claude`
- `GROK_SKILLS_DIR=/tmp/gh149-skills-z630GA/grok`

| Step | codex | claude | grok |
| --- | --- | --- | --- |
| dry-run install | PASS | PASS | PASS |
| install batch (9 skills) | PASS | PASS | PASS |
| status readback | PASS | PASS | PASS |
| `--existing-only` | PASS | PASS | PASS |
| uninstall batch | PASS | PASS | PASS |

`--agent both`: codex+claude linked; **grok root empty**.

**Important:** temp-root FS proofs ≠ “Grok loads skills from the host catalog.” Host `workflows/` was empty (0 entries) and was **not** written.

## 3. Focused live Grok smoke

Source: `/workspace/grok-compat-plan/live-smoke-2026-10-07.md`

| Item | Status |
| --- | --- |
| Discover host catalog (`managed-skills` / `workflows`) | **PASS** — 49 managed skills; **no** Grok-compat epic skills; `workflows/` empty |
| Follow on-disk PR refs (#151/#154 worktrees) without install | **PASS** — `worker-with-grok`, deliver/review Grok adapters resolve on disk |
| One representative workflow path (Task/MessageSubagent continuation) | **PASS** — live executor Task continuation on this host |
| Instruction-only reviewer adapter text on #154 | **PASS** (repo evidence) — no Claude profile claim |
| Nested Standards/Spec Task spawn as reviewer | **UNTESTED** |
| `StopSubagent` cancel path | **UNTESTED** |
| Host-loaded skill discovery of new catalog | **PENDING** install approval |
| End-to-end deliver-work loading `worker-with-grok` from installed catalog | **PENDING** merge + install |

## 4. Inventory (passed / untested / pending)

### Passed

- validate-skills + installed-files + manage-skills (incl. grok; both excludes grok) on proposed combined revision
- Temp-root install/status/uninstall for codex + claude + grok
- Live host discovery: Grok-compat skills **absent** from managed-skills/workflows (honest pre-install state)
- On-disk followability of #151/#154 skill trees without host install
- Live Task/MessageSubagent worker continuation on this box
- Source-only product siblings PR-ready (#150–#154); Hawk PASS/PASS recorded separately

### Untested

- Nested live reviewer Task spawn / StopSubagent
- Host model/effort metadata on spawn
- Whether Grok auto-discovers skills from an arbitrary `/workspace` checkout

### Pending (owner-gated — separate merge & install approval)

- Merge of #150–#154 (+ then #155 docs)
- Production `manage-skills --agent grok` → `/home/box/agent-data/workflows` (or `GROK_SKILLS_DIR`)
- Host catalog load / use of new skills after install
- Claude Code / Codex CLI smoke (grill/tdd/openspec/code-review)
- Live UpdateSkill UI readback

## 5. Explicitly deferred (not claimed done)

| Item | Disposition |
| --- | --- |
| Claude/Codex CLI host smoke | Owner-gated after merge; CLIs absent on this box — **not** an Acceptance blocker for source-only readiness |
| Live UpdateSkill UI | Owner-gated — **not** claimed |
| Production workflows install | Owner-gated — **not** run; temp FS ≠ host load |

## 6. Source-only sibling status

| Sibling | PR | Notes |
| --- | --- | --- |
| #144 | #150 | Docs; N/A skill install |
| #145 | #153 | Manager + tests; temp-root proved; prod install pending |
| #146 | #151 | `worker-with-grok`; source-only → this batch; temp-root proved |
| #147 | #152 | plan-work; temp-root proved |
| #148 | #154 | deliver/review adapters; temp-root proved |

Production install+readback for skill-touching siblings remains **owner-gated** after merge + install approval.

## Remaining for Hawk / Jimmie

1. Owner merge of product #150–#154 (Hawk already PASS/PASS).
2. Separate approval for production grok install + host readback.
3. Optional later: Claude/Codex CLI smoke; UpdateSkill UI; nested reviewer live spawn.
4. Merge #155 only as docs/evidence after (or with) product merges — never as a product stack.
