# #149 Regression evidence — Grok-compat batch (proposed catalog)

**Recorded:** 2026-10-07 12:03 EDT
**Host:** Grok Bot box (`box`, Linux); `gh` as `jimmie-potts`
**Combined catalog revision (merge of sibling heads):** `9406f09940ec78678eaf4ae4777eeb5d78391c53`
**Evidence branch tip:** `codex/gh-149-regression-evidence` (docs-only commit on top of catalog merge `9406f099`)
**Base:** `origin/main` @ `3fef618`
**Merge order:** main → #150 (#144) → #153 (#145) → #152 (#147) → #154 (#148; includes #146 worker-with-grok)
**Conflicts:** README.md (#144 provisional vs #145 destination/UpdateSkill — kept #145); AGENTS.md + `plan-work/SKILL.md` (#144/#147 provisional vs #148 landed adapters — kept #148). No leftover conflict markers.
**NO MERGES** of sibling PRs #150–#154. This branch is throwaway evidence only.

## Sibling heads under test

| Issue | PR | Branch | SHA |
| --- | --- | --- | --- |
| #144 | #150 | `codex/gh-144-shared-skill-core` | `9ec43b83` |
| #145 | #153 | `codex/gh-145-grok-install-path` | `e37c23f9` |
| #146 | #151 | `codex/gh-146-worker-with-grok` | `d7134e7e` (content via #154) |
| #147 | #152 | `codex/gh-147-plan-work-grok-column` | `22c8b2fe` |
| #148 | #154 | `codex/gh-148-deliver-review-grok-adapters` | `b8cbc452` |

## Checks (AGENTS.md)

| Check | Result |
| --- | --- |
| `python3 scripts/validate-skills.py` | **PASS** — 37 skill(s) |
| `python3 tests/installed-files-test.py` | **PASS** — 17 tests |
| `bash tests/manage-skills-test.sh` | **PASS** — 49 commands (incl. Grok install/status/uninstall/`--agent both` excludes grok) |
| `bash -n scripts/manage-skills.sh` / `tests/manage-skills-test.sh` | **PASS** |
| `git diff --check` | **PASS** |
| `python3 tests/deliver-work-test.py` | **PASS** |
| `python3 tests/review-work-test.py` | **PASS** — 60 tests |
| `python3 tests/plan-work-test.py` | **PASS** — 15 tests |
| `python3 tests/pairing-skills-test.py` | **PASS** — 7 tests |

## Install / status / uninstall (disposable temp roots)

Env overrides (real installs **not** touched):

- `CODEX_SKILLS_DIR=/tmp/gh149-skills-z630GA/codex`
- `CLAUDE_SKILLS_DIR=/tmp/gh149-skills-z630GA/claude`
- `GROK_SKILLS_DIR=/tmp/gh149-skills-z630GA/grok`

Skills installed per agent: `worker-with-grok deliver-work review-work plan-work grill-me grilling tdd code-review openspec-explore`

| Step | codex | claude | grok |
| --- | --- | --- | --- |
| dry-run install `worker-with-grok` | PASS | PASS | PASS |
| install batch | PASS (9 links) | PASS (9 links) | PASS (9 links) |
| status readback (batch skills `correctly installed`) | PASS | PASS | PASS |
| `--existing-only` | PASS | PASS | PASS |
| link resolve → checkout `skills/` | PASS | PASS | PASS |
| uninstall batch | PASS | PASS | PASS |
| status after uninstall (batch missing) | PASS | PASS | PASS |

`--agent both` install of `worker-with-grok` into separate temp roots: codex+claude linked; **grok root empty** (decision 1: do not fold grok into `both`).

Default Grok destination (no `GROK_SKILLS_DIR`): `/home/box/agent-data/workflows` per `manage-skills.sh`. Live UpdateSkill UI reload **not** invoked; documented expectation from README/#145: after symlink install, prove with `./scripts/manage-skills.sh status --agent grok` (owned link resolves into checkout) and, when host UI available, confirm skill appears after fresh session/host reload.

Real dirs: `~/.agents/skills` and `~/.claude/skills` absent on this box; `/home/box/agent-data/workflows` existed empty (0 entries) and was **not** written by this session.

## Claude / Codex smoke (invoke/load entry)

| Skill | Host | Result |
| --- | --- | --- |
| grill-me / grilling | Claude Code | **GAP** — `claude` CLI not on PATH; no authorized Claude Code session on this box |
| tdd | Claude Code | **GAP** (same) |
| openspec-explore | Claude Code | **GAP** (same) |
| code-review | Claude Code | **GAP** (same) |
| grill-me / grilling | Codex | **GAP** — `codex` CLI not on PATH; no authorized Codex session on this box |
| tdd | Codex | **GAP** (same) |
| openspec-explore | Codex | **GAP** (same) |
| code-review | Codex | **GAP** (same) |

Stand-in only (not claimed as host smoke): SKILL.md frontmatter + entry sections parse cleanly for those skills on the combined tree.

## Grok dry deliver / review smoke

Read-only composition on combined tree (no publish, merge, or irreversible external action):

| Check | Result |
| --- | --- |
| `worker-with-grok` frontmatter name + SKILL load | PASS |
| `deliver-work` + `references/grok-worker-selection.md` + `grok-model-selection.md` present | PASS |
| `review-work` + `references/grok-reviewers.md` present | PASS |
| grok-reviewers: instruction-only read-only executors; no Claude `review-work-reviewer` profile claim; axes incomplete without evidence | PASS |
| deliver-work Grok worker selection references `worker-with-grok` | PASS |
| plan-work Grok column / execution-recommendations present | PASS |
| Live MessageSubagent / Task worker spawn inside deliver-work | **GAP** — not exercised (would be a live coordinator session; dry composition only) |
| Live UpdateSkill host menu appearance | **GAP** — UI not driven; manager status + link resolve used as install readback |

## Source-only sibling install batch status

Per AGENTS.md Installation: skill-touching siblings marked source-only close install at this batch.

| Sibling | Skill/install touch? | Install+readback on proposed heads |
| --- | --- | --- |
| #144 / PR #150 | Docs only (AGENTS/README) | N/A install; three-host wording in combined tree |
| #145 / PR #153 | manage-skills + installed-files | **Completed via temp-root** (codex/claude/grok); owner merge still required before production install |
| #146 / PR #151 | `worker-with-grok` skill | **Completed via temp-root** (and present via #154) |
| #147 / PR #152 | `plan-work` skill | **Completed via temp-root** |
| #148 / PR #154 | deliver-work + review-work + worker-with-grok | **Completed via temp-root** |

Post-merge production install into real Codex/Claude/Grok destinations remains **owner-gated** (siblings not merged).

## Acceptance checklist (proposed heads)

- [x] `validate-skills.py` passes on proposed combined catalog
- [x] `installed-files-test.py` and `manage-skills-test.sh` pass with Grok coverage
- [x] Status/install readback for Claude, Codex, and Grok against **temp roots** (+ UpdateSkill/workflows expectation documented for grok)
- [ ] Claude/Codex host smoke for grill/tdd/openspec/code-review — **GAP named** (CLIs unavailable here)
- [x] Grok dry deliver/review smoke recorded; live spawn/UI gaps named without claiming success
- [x] Source-only siblings: temp-root install+readback completed; production install pending owner merge of #150–#154
- [x] Hub AGENTS wording follow-on: not required to close; optional elsewhere

## Remaining for Hawk / Jimmie

1. Independent Hawk Standards+Spec on fixed sibling heads (no merge by workers).
2. Owner merge of #150–#154 (order respecting deps: #145 before relying on grok install in prod; #146 before/#with #148).
3. Post-merge: production `manage-skills` install+status on authorized Codex/Claude/Grok roots; optional live UpdateSkill UI confirm.
4. Optional: Claude Code / Codex invoke/load smoke on a machine that has those hosts.
5. Do **not** treat this evidence branch as a product merge candidate beyond the optional docs artifact.
