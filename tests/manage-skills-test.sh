#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd -P)"
MANAGER="$REPO_ROOT/scripts/manage-skills.sh"
VALIDATOR="$REPO_ROOT/scripts/validate-skills.py"
FIXTURES="$SCRIPT_DIR/fixtures"

TEST_TMP="$(mktemp -d "${TMPDIR:-/tmp}/agent-skills-test.XXXXXX")"
cleanup() {
  if [[ -n "${TEST_TMP:-}" && -d "$TEST_TMP" ]]; then
    rm -rf -- "$TEST_TMP"
  fi
}
trap cleanup EXIT HUP INT TERM

SPACE_ROOT="$TEST_TMP/path with spaces"
SOURCE_CATALOG="$SPACE_ROOT/source catalog"
mkdir -p -- "$SOURCE_CATALOG"
cp -R -- "$FIXTURES/valid-skill" "$SOURCE_CATALOG/valid-skill"

LAST_OUTPUT="$TEST_TMP/last-output.log"
PASS_COUNT=0

fail_test() {
  printf 'FAIL: %s\n' "$*" >&2
  if [[ -f "$LAST_OUTPUT" ]]; then
    sed -n '1,120p' "$LAST_OUTPUT" >&2
  fi
  exit 1
}

pass_test() {
  PASS_COUNT=$((PASS_COUNT + 1))
  printf 'PASS: %s\n' "$1"
}

expect_success() {
  local label="$1"
  shift
  if "$@" >"$LAST_OUTPUT" 2>&1; then
    pass_test "$label"
  else
    fail_test "$label unexpectedly failed"
  fi
}

expect_failure() {
  local label="$1"
  shift
  local status
  set +e
  "$@" >"$LAST_OUTPUT" 2>&1
  status=$?
  set -e
  if [[ $status -eq 0 ]]; then
    fail_test "$label unexpectedly succeeded"
  fi
  pass_test "$label"
}

assert_output_contains() {
  local expected="$1"
  if ! grep -Fq -- "$expected" "$LAST_OUTPUT"; then
    fail_test "expected output to contain: $expected"
  fi
}

assert_symlink_to() {
  local link_path="$1"
  local expected_path="$2"
  [[ -L "$link_path" ]] || fail_test "expected symlink: $link_path"
  local actual
  local expected
  actual="$(realpath -e -- "$link_path")"
  expected="$(realpath -e -- "$expected_path")"
  [[ "$actual" == "$expected" ]] ||
    fail_test "symlink $link_path resolves to $actual instead of $expected"
}

run_manager() {
  AGENT_SKILLS_SOURCE_DIR="$SOURCE_CATALOG" \
    CODEX_SKILLS_DIR="$ACTIVE_CODEX" \
    CLAUDE_SKILLS_DIR="$ACTIVE_CLAUDE" \
    "$MANAGER" "$@"
}

# 1. One Codex install creates the expected absolute per-skill link.
ACTIVE_CODEX="$SPACE_ROOT/case 1/codex skills"
ACTIVE_CLAUDE="$SPACE_ROOT/case 1/claude skills"
expect_success "install one valid skill for Codex" \
  run_manager install --agent codex valid-skill
assert_symlink_to "$ACTIVE_CODEX/valid-skill" "$SOURCE_CATALOG/valid-skill"
[[ "$(readlink -- "$ACTIVE_CODEX/valid-skill")" = /* ]] ||
  fail_test "installer did not create an absolute symlink"

# 2. Both agents point to the same canonical source.
ACTIVE_CODEX="$SPACE_ROOT/case 2/codex skills"
ACTIVE_CLAUDE="$SPACE_ROOT/case 2/claude skills"
expect_success "install one canonical skill for both agents" \
  run_manager install --agent both valid-skill
assert_symlink_to "$ACTIVE_CODEX/valid-skill" "$SOURCE_CATALOG/valid-skill"
assert_symlink_to "$ACTIVE_CLAUDE/valid-skill" "$SOURCE_CATALOG/valid-skill"

# 3. Reinstall is idempotent and leaves the symlink inode unchanged.
before_stat="$(stat -c '%i:%Y:%Z' -- "$ACTIVE_CODEX/valid-skill")"
expect_success "installing twice is idempotent" \
  run_manager install --agent both valid-skill
after_stat="$(stat -c '%i:%Y:%Z' -- "$ACTIVE_CODEX/valid-skill")"
[[ "$before_stat" == "$after_stat" ]] ||
  fail_test "idempotent install changed the existing Codex symlink"
assert_output_contains "already installed"

# 4. Dry-run does not even create destination roots.
ACTIVE_CODEX="$SPACE_ROOT/case 4/codex skills"
ACTIVE_CLAUDE="$SPACE_ROOT/case 4/claude skills"
expect_success "install dry-run performs no mutation" \
  run_manager install --agent both --dry-run valid-skill
[[ ! -e "$ACTIVE_CODEX" && ! -L "$ACTIVE_CODEX" ]] ||
  fail_test "dry-run created the Codex destination root"
[[ ! -e "$ACTIVE_CLAUDE" && ! -L "$ACTIVE_CLAUDE" ]] ||
  fail_test "dry-run created the Claude destination root"
assert_output_contains "DRY-RUN"

# 5. A colliding regular directory is preserved.
ACTIVE_CODEX="$SPACE_ROOT/case 5/codex skills"
ACTIVE_CLAUDE="$SPACE_ROOT/case 5/claude skills"
mkdir -p -- "$ACTIVE_CODEX/valid-skill"
printf 'preserve me\n' >"$ACTIVE_CODEX/valid-skill/marker.txt"
expect_failure "colliding directory fails safely" \
  run_manager install --agent codex valid-skill
[[ "$(sed -n '1p' "$ACTIVE_CODEX/valid-skill/marker.txt")" == "preserve me" ]] ||
  fail_test "colliding directory contents changed"
assert_output_contains "conflicting regular file or directory"
assert_output_contains "no destination was changed"

# 6. A colliding regular file is preserved.
ACTIVE_CODEX="$SPACE_ROOT/case 6/codex skills"
ACTIVE_CLAUDE="$SPACE_ROOT/case 6/claude skills"
mkdir -p -- "$ACTIVE_CODEX"
printf 'preserve file\n' >"$ACTIVE_CODEX/valid-skill"
expect_failure "colliding file fails safely" \
  run_manager install --agent codex valid-skill
[[ "$(sed -n '1p' "$ACTIVE_CODEX/valid-skill")" == "preserve file" ]] ||
  fail_test "colliding file contents changed"
assert_output_contains "conflicting regular file or directory"

# 7. A foreign symlink is preserved.
ACTIVE_CODEX="$SPACE_ROOT/case 7/codex skills"
ACTIVE_CLAUDE="$SPACE_ROOT/case 7/claude skills"
foreign_target="$SPACE_ROOT/case 7/foreign target"
mkdir -p -- "$ACTIVE_CODEX" "$foreign_target"
ln -s -- "$foreign_target" "$ACTIVE_CODEX/valid-skill"
foreign_link_text="$(readlink -- "$ACTIVE_CODEX/valid-skill")"
expect_failure "foreign symlink fails safely" \
  run_manager install --agent codex valid-skill
[[ "$(readlink -- "$ACTIVE_CODEX/valid-skill")" == "$foreign_link_text" ]] ||
  fail_test "foreign symlink was changed"
assert_output_contains "foreign symlink"

# 8. Uninstall removes an owned link and leaves its source.
ACTIVE_CODEX="$SPACE_ROOT/case 8/codex skills"
ACTIVE_CLAUDE="$SPACE_ROOT/case 8/claude skills"
expect_success "prepare owned link for uninstall" \
  run_manager install --agent codex valid-skill
expect_success "uninstall removes only the owned link" \
  run_manager uninstall --agent codex valid-skill
[[ ! -e "$ACTIVE_CODEX/valid-skill" && ! -L "$ACTIVE_CODEX/valid-skill" ]] ||
  fail_test "owned link remains after uninstall"
[[ -f "$SOURCE_CATALOG/valid-skill/SKILL.md" ]] ||
  fail_test "uninstall removed the source skill"

# 9. Uninstall refuses foreign links and regular directories.
ACTIVE_CODEX="$SPACE_ROOT/case 9 foreign/codex skills"
ACTIVE_CLAUDE="$SPACE_ROOT/case 9 foreign/claude skills"
foreign_target="$SPACE_ROOT/case 9 foreign/target"
mkdir -p -- "$ACTIVE_CODEX" "$foreign_target"
ln -s -- "$foreign_target" "$ACTIVE_CODEX/valid-skill"
expect_failure "uninstall preserves a foreign symlink" \
  run_manager uninstall --agent codex valid-skill
[[ -L "$ACTIVE_CODEX/valid-skill" ]] ||
  fail_test "uninstall removed a foreign symlink"

ACTIVE_CODEX="$SPACE_ROOT/case 9 directory/codex skills"
ACTIVE_CLAUDE="$SPACE_ROOT/case 9 directory/claude skills"
mkdir -p -- "$ACTIVE_CODEX/valid-skill"
expect_failure "uninstall preserves a regular directory" \
  run_manager uninstall --agent codex valid-skill
[[ -d "$ACTIVE_CODEX/valid-skill" && ! -L "$ACTIVE_CODEX/valid-skill" ]] ||
  fail_test "uninstall removed a regular directory"

# 10. An already absent link is a successful no-op and creates no root.
ACTIVE_CODEX="$SPACE_ROOT/case 10/codex skills"
ACTIVE_CLAUDE="$SPACE_ROOT/case 10/claude skills"
expect_success "uninstall of an absent skill is a no-op" \
  run_manager uninstall --agent codex valid-skill
[[ ! -e "$ACTIVE_CODEX" && ! -L "$ACTIVE_CODEX" ]] ||
  fail_test "absent uninstall created a destination root"
assert_output_contains "already absent"

# 11. Unknown, malformed, and omitted selections are rejected.
ACTIVE_CODEX="$SPACE_ROOT/case 11/codex skills"
ACTIVE_CLAUDE="$SPACE_ROOT/case 11/claude skills"
expect_failure "unknown skill name is rejected" \
  run_manager install --agent codex missing-skill
assert_output_contains "unknown skill"
expect_failure "malformed skill name is rejected" \
  run_manager install --agent codex ../valid-skill
assert_output_contains "malformed skill name"
expect_failure "omitted selection is not interpreted as all" \
  run_manager install --agent codex
assert_output_contains "requires --all"
[[ ! -e "$ACTIVE_CODEX" && ! -L "$ACTIVE_CODEX" ]] ||
  fail_test "rejected selection created a destination root"

# Destination overrides may not point into the canonical source catalog.
ACTIVE_CODEX="$SOURCE_CATALOG/valid-skill"
ACTIVE_CLAUDE="$SPACE_ROOT/case 11 nested/claude skills"
expect_failure "destination inside source catalog is rejected" \
  run_manager install --agent codex valid-skill
assert_output_contains "must not be the source catalog"
[[ ! -e "$SOURCE_CATALOG/valid-skill/valid-skill" && ! -L "$SOURCE_CATALOG/valid-skill/valid-skill" ]] ||
  fail_test "nested destination check allowed a source-catalog mutation"

# 12. Paths containing spaces were used above; also cover --all explicitly.
ACTIVE_CODEX="$SPACE_ROOT/case 12/codex skills"
ACTIVE_CLAUDE="$SPACE_ROOT/case 12/claude skills"
expect_success "all selection works with paths containing spaces" \
  run_manager install --agent both --all
assert_symlink_to "$ACTIVE_CODEX/valid-skill" "$SOURCE_CATALOG/valid-skill"
assert_symlink_to "$ACTIVE_CLAUDE/valid-skill" "$SOURCE_CATALOG/valid-skill"

# Uninstall dry-run preserves an owned link.
expect_success "uninstall dry-run performs no mutation" \
  run_manager uninstall --agent codex --dry-run valid-skill
assert_symlink_to "$ACTIVE_CODEX/valid-skill" "$SOURCE_CATALOG/valid-skill"
assert_output_contains "DRY-RUN"

# Status reports missing without failure, correct installs, and conflicts.
ACTIVE_CODEX="$SPACE_ROOT/status missing/codex skills"
ACTIVE_CLAUDE="$SPACE_ROOT/status missing/claude skills"
expect_success "status treats missing optional skills as healthy" \
  run_manager status --agent codex
assert_output_contains "missing"
[[ ! -e "$ACTIVE_CODEX" && ! -L "$ACTIVE_CODEX" ]] ||
  fail_test "status created a destination root"

ACTIVE_CODEX="$SPACE_ROOT/case 12/codex skills"
ACTIVE_CLAUDE="$SPACE_ROOT/case 12/claude skills"
expect_success "status reports a correct installation" \
  run_manager status --agent both
assert_output_contains "correctly installed"

ACTIVE_CODEX="$SPACE_ROOT/status conflict/codex skills"
ACTIVE_CLAUDE="$SPACE_ROOT/status conflict/claude skills"
mkdir -p -- "$ACTIVE_CODEX/valid-skill"
expect_failure "status returns nonzero for a conflict" \
  run_manager status --agent codex
assert_output_contains "conflicting regular file or directory"

# Status distinguishes foreign and broken-owned symlinks; uninstall preserves both.
ACTIVE_CODEX="$SPACE_ROOT/case 7/codex skills"
ACTIVE_CLAUDE="$SPACE_ROOT/case 7/claude skills"
expect_failure "status identifies a foreign symlink" \
  run_manager status --agent codex
assert_output_contains "foreign symlink"

ACTIVE_CODEX="$SPACE_ROOT/status broken owned/codex skills"
ACTIVE_CLAUDE="$SPACE_ROOT/status broken owned/claude skills"
mkdir -p -- "$ACTIVE_CODEX"
ln -s -- "$SOURCE_CATALOG/valid-skill/missing/.." "$ACTIVE_CODEX/valid-skill"
[[ -L "$ACTIVE_CODEX/valid-skill" && ! -e "$ACTIVE_CODEX/valid-skill" ]] ||
  fail_test "failed to construct a broken owned symlink fixture"
expect_failure "status identifies a broken owned symlink" \
  run_manager status --agent codex
assert_output_contains "broken owned symlink"
expect_failure "uninstall preserves a broken owned symlink" \
  run_manager uninstall --agent codex valid-skill
[[ -L "$ACTIVE_CODEX/valid-skill" ]] ||
  fail_test "uninstall removed a broken owned symlink"

# Status still discovers an owned link after its catalog entry is removed.
ORIGINAL_SOURCE_CATALOG="$SOURCE_CATALOG"
SOURCE_CATALOG="$SPACE_ROOT/status removed source/catalog"
mkdir -p -- "$SOURCE_CATALOG"
cp -R -- "$FIXTURES/valid-skill" "$SOURCE_CATALOG/valid-skill"
ACTIVE_CODEX="$SPACE_ROOT/status removed source/codex skills"
ACTIVE_CLAUDE="$SPACE_ROOT/status removed source/claude skills"
expect_success "prepare owned link whose source will be removed" \
  run_manager install --agent codex valid-skill
mv -- "$SOURCE_CATALOG/valid-skill" "$SPACE_ROOT/status removed source/removed-valid-skill"
[[ -L "$ACTIVE_CODEX/valid-skill" && ! -e "$ACTIVE_CODEX/valid-skill" ]] ||
  fail_test "removing the source did not leave the expected dangling link"
expect_failure "status discovers an owned link after source removal" \
  run_manager status --agent codex
assert_output_contains "broken owned symlink"
SOURCE_CATALOG="$ORIGINAL_SOURCE_CATALOG"

# 13. The valid fixture passes as an isolated catalog.
VALID_CATALOG="$TEST_TMP/validator valid catalog"
mkdir -p -- "$VALID_CATALOG"
cp -R -- "$FIXTURES/valid-skill" "$VALID_CATALOG/valid-skill"
expect_success "valid fixture passes catalog validation" \
  python3 "$VALIDATOR" --skills-dir "$VALID_CATALOG"
assert_output_contains "validated 1 skill"

# 14. The invalid fixture fails with actionable, aggregated findings.
INVALID_CATALOG="$TEST_TMP/validator invalid catalog"
mkdir -p -- "$INVALID_CATALOG"
cp -R -- "$FIXTURES/invalid-skill" "$INVALID_CATALOG/invalid-skill"
expect_failure "invalid fixture fails catalog validation" \
  python3 "$VALIDATOR" --skills-dir "$INVALID_CATALOG"
assert_output_contains "ERROR"
assert_output_contains "TODO"
assert_output_contains "does not resolve to an existing file"
assert_output_contains "escapes the skill directory"

# Link parsing accepts balanced parentheses and flexible trigger wording.
LINK_CATALOG="$TEST_TMP/validator balanced link catalog"
mkdir -p -- "$LINK_CATALOG/link-skill/references"
printf '%s\n' \
  '---' \
  'name: link-skill' \
  'description: Reviews SQL migrations. Triggers on schema change requests.' \
  '---' \
  '' \
  '# Link Skill' \
  '' \
  'Read [the numbered reference](references/file(1).md).' \
  'Read [the multiline reference](' \
  'references/details.md' \
  ').' \
  >"$LINK_CATALOG/link-skill/SKILL.md"
printf '%s\n' '# Numbered reference' >"$LINK_CATALOG/link-skill/references/file(1).md"
printf '%s\n' '# Details' >"$LINK_CATALOG/link-skill/references/details.md"
expect_success "balanced-parenthesis links validate" \
  python3 "$VALIDATOR" --skills-dir "$LINK_CATALOG"
printf '%s\n' 'TODO: finish this reference.' >"$LINK_CATALOG/link-skill/references/details.md"
expect_failure "placeholders in linked references are rejected" \
  python3 "$VALIDATOR" --skills-dir "$LINK_CATALOG"
assert_output_contains "replace unfinished template marker"

# Extensionless shebang scripts are still shell scripts and must parse in Bash.
SHELL_CATALOG="$TEST_TMP/validator shell catalog"
mkdir -p -- "$SHELL_CATALOG/shell-skill/scripts"
printf '%s\n' \
  '---' \
  'name: shell-skill' \
  'description: Runs a deterministic helper. Use for shell helper requests.' \
  '---' \
  '' \
  '# Shell Skill' \
  '' \
  'Run the deterministic helper.' \
  >"$SHELL_CATALOG/shell-skill/SKILL.md"
printf '%s\n' '#!/usr/bin/env bash' 'if then' >"$SHELL_CATALOG/shell-skill/scripts/run"
expect_failure "extensionless shell syntax is validated" \
  python3 "$VALIDATOR" --skills-dir "$SHELL_CATALOG"
assert_output_contains "fix Bash syntax"

# The manager's validate entry point uses the same isolated catalog override.
ACTIVE_CODEX="$SPACE_ROOT/validate command/codex skills"
ACTIVE_CLAUDE="$SPACE_ROOT/validate command/claude skills"
expect_success "manager validate delegates to catalog validation" \
  run_manager validate

printf 'PASS: all %d test commands completed without touching personal skill directories.\n' \
  "$PASS_COUNT"
