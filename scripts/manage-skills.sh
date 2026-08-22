#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd -P)"
VALIDATOR="$SCRIPT_DIR/validate-skills.py"
SOURCE_DIR_RAW="${AGENT_SKILLS_SOURCE_DIR:-$REPO_ROOT/skills}"

usage() {
  printf '%s\n' \
    "Usage:" \
    "  ./scripts/manage-skills.sh install   --agent codex|claude|both [--dry-run] [--all | <skill>...]" \
    "  ./scripts/manage-skills.sh uninstall --agent codex|claude|both [--dry-run] [--all | <skill>...]" \
    "  ./scripts/manage-skills.sh status    --agent codex|claude|both" \
    "  ./scripts/manage-skills.sh validate"
}

fail() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 1
}

valid_skill_name() {
  local name="$1"
  [[ ${#name} -lt 64 && "$name" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]
}

resolve_link_target() {
  local link_path="$1"
  local raw_target
  raw_target="$(readlink -- "$link_path")"
  if [[ "$raw_target" = /* ]]; then
    realpath -m -- "$raw_target"
  else
    realpath -m -- "$(dirname -- "$link_path")/$raw_target"
  fi
}

CLASSIFICATION=""
classify_destination() {
  local expected_source="$1"
  local destination="$2"
  local resolved_target

  if [[ -L "$destination" ]]; then
    resolved_target="$(resolve_link_target "$destination")"
    if [[ "$resolved_target" == "$expected_source" ]]; then
      if [[ -e "$destination" ]]; then
        CLASSIFICATION="correct"
      else
        CLASSIFICATION="broken-owned"
      fi
    else
      CLASSIFICATION="foreign-symlink"
    fi
  elif [[ -e "$destination" ]]; then
    CLASSIFICATION="regular-conflict"
  else
    CLASSIFICATION="missing"
  fi
}

ACTION="${1:-}"
if [[ -z "$ACTION" ]]; then
  usage
  exit 2
fi

case "$ACTION" in
  install|uninstall|status)
    ;;
  validate)
    if [[ $# -ne 1 ]]; then
      usage
      exit 2
    fi
    exec python3 "$VALIDATOR" --skills-dir "$SOURCE_DIR_RAW"
    ;;
  -h|--help|help)
    usage
    exit 0
    ;;
  *)
    printf "ERROR: unknown command '%s'.\n" "$ACTION" >&2
    usage >&2
    exit 2
    ;;
esac
shift

AGENT=""
SELECT_ALL=0
DRY_RUN=0
declare -a REQUESTED_SKILLS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --agent)
      if [[ -n "$AGENT" ]]; then
        fail "--agent may be provided only once."
      fi
      if [[ $# -lt 2 ]]; then
        fail "--agent requires codex, claude, or both."
      fi
      AGENT="$2"
      shift 2
      ;;
    --all)
      SELECT_ALL=1
      shift
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --*)
      fail "unknown option '$1'."
      ;;
    *)
      REQUESTED_SKILLS+=("$1")
      shift
      ;;
  esac
done

case "$AGENT" in
  codex|claude|both)
    ;;
  "")
    fail "--agent codex|claude|both is required for '$ACTION'."
    ;;
  *)
    fail "unsupported agent '$AGENT'; expected codex, claude, or both."
    ;;
esac

if [[ "$ACTION" == "status" ]]; then
  if [[ $SELECT_ALL -eq 1 || $DRY_RUN -eq 1 || ${#REQUESTED_SKILLS[@]} -gt 0 ]]; then
    fail "status accepts only --agent codex|claude|both."
  fi
else
  if [[ $SELECT_ALL -eq 1 && ${#REQUESTED_SKILLS[@]} -gt 0 ]]; then
    fail "choose either --all or explicit skill names, not both."
  fi
  if [[ $SELECT_ALL -eq 0 && ${#REQUESTED_SKILLS[@]} -eq 0 ]]; then
    fail "'$ACTION' requires --all or at least one explicit skill name."
  fi
fi

if [[ -L "$SOURCE_DIR_RAW" ]]; then
  fail "source catalog must be a real directory, not a symlink: $SOURCE_DIR_RAW"
fi
if [[ ! -d "$SOURCE_DIR_RAW" ]]; then
  fail "source catalog does not exist or is not a directory: $SOURCE_DIR_RAW"
fi
SOURCE_DIR="$(realpath -e -- "$SOURCE_DIR_RAW")"

catalog_fingerprint() {
  local path
  local relative_path
  local metadata
  local digest
  local link_target

  {
    while IFS= read -r -d '' path; do
      relative_path="${path#"$SOURCE_DIR/"}"
      if [[ -L "$path" ]]; then
        link_target="$(readlink -- "$path")" || return 1
        printf 'L\0%s\0%s\0' "$relative_path" "$link_target"
      elif [[ -f "$path" ]]; then
        digest="$(sha256sum -- "$path")" || return 1
        digest="${digest%% *}"
        metadata="$(stat -c '%f' -- "$path")" || return 1
        printf 'F\0%s\0%s\0%s\0' "$relative_path" "$metadata" "$digest"
      elif [[ -d "$path" ]]; then
        metadata="$(stat -c '%f' -- "$path")" || return 1
        printf 'D\0%s\0%s\0' "$relative_path" "$metadata"
      else
        metadata="$(stat -c '%f:%s' -- "$path")" || return 1
        printf 'S\0%s\0%s\0' "$relative_path" "$metadata"
      fi
    done < <(find "$SOURCE_DIR" -mindepth 1 -print0 | sort -z)
  } | sha256sum | cut -d ' ' -f 1
}

read_catalog_snapshot() {
  local -n target_array="$1"
  local catalog_path
  target_array=()
  while IFS= read -r -d '' catalog_path; do
    target_array+=("$(basename -- "$catalog_path")")
  done < <(
    find "$SOURCE_DIR" -mindepth 1 -maxdepth 1 ! -name '.*' -print0 | sort -z
  )
}

declare -a CATALOG_BEFORE_VALIDATION=()
declare -a CATALOG_AFTER_VALIDATION=()
read_catalog_snapshot CATALOG_BEFORE_VALIDATION
if ! FINGERPRINT_BEFORE_VALIDATION="$(catalog_fingerprint)"; then
  fail "could not fingerprint the source catalog before validation."
fi

# Validate the complete catalog and fail closed if its direct entries change
# while validation is running.
python3 "$VALIDATOR" --skills-dir "$SOURCE_DIR"
read_catalog_snapshot CATALOG_AFTER_VALIDATION
if ! VALIDATED_CATALOG_FINGERPRINT="$(catalog_fingerprint)"; then
  fail "could not fingerprint the source catalog after validation."
fi
if [[ "$FINGERPRINT_BEFORE_VALIDATION" != "$VALIDATED_CATALOG_FINGERPRINT" ]]; then
  fail "source catalog contents changed during validation; retry after catalog writes finish."
fi
if [[ ${#CATALOG_BEFORE_VALIDATION[@]} -ne ${#CATALOG_AFTER_VALIDATION[@]} ]]; then
  fail "source catalog changed during validation; retry after catalog writes finish."
fi
for ((index = 0; index < ${#CATALOG_BEFORE_VALIDATION[@]}; index++)); do
  if [[ "${CATALOG_BEFORE_VALIDATION[$index]}" != "${CATALOG_AFTER_VALIDATION[$index]}" ]]; then
    fail "source catalog changed during validation; retry after catalog writes finish."
  fi
done

declare -a CATALOG_SKILLS=("${CATALOG_AFTER_VALIDATION[@]}")

declare -A CATALOG_LOOKUP=()
for skill in "${CATALOG_SKILLS[@]}"; do
  CATALOG_LOOKUP["$skill"]=1
done

declare -a SELECTED_SKILLS=()
if [[ "$ACTION" == "status" || $SELECT_ALL -eq 1 ]]; then
  SELECTED_SKILLS=("${CATALOG_SKILLS[@]}")
else
  declare -A SELECTED_LOOKUP=()
  for skill in "${REQUESTED_SKILLS[@]}"; do
    if ! valid_skill_name "$skill"; then
      fail "malformed skill name '$skill'; use lowercase letters, digits, and single hyphens, under 64 characters."
    fi
    if [[ -z "${CATALOG_LOOKUP[$skill]+present}" ]]; then
      fail "unknown skill '$skill'; it is not a directory in $SOURCE_DIR."
    fi
    if [[ -z "${SELECTED_LOOKUP[$skill]+present}" ]]; then
      SELECTED_SKILLS+=("$skill")
      SELECTED_LOOKUP["$skill"]=1
    fi
  done
fi

for skill in "${SELECTED_SKILLS[@]}"; do
  source_skill="$SOURCE_DIR/$skill"
  if [[ -L "$source_skill" || ! -d "$source_skill" || -L "$source_skill/SKILL.md" || ! -f "$source_skill/SKILL.md" ]]; then
    fail "selected skill '$skill' changed after validation; no destination was changed."
  fi
  resolved_source_skill="$(realpath -e -- "$source_skill")"
  if [[ "$resolved_source_skill" != "$SOURCE_DIR/$skill" ]]; then
    fail "selected skill '$skill' resolves outside the canonical catalog; no destination was changed."
  fi
done

if [[ ${#SELECTED_SKILLS[@]} -eq 0 && $ACTION != "status" ]]; then
  printf 'INFO: catalog contains no production skills; nothing to %s.\n' "$ACTION"
  exit 0
fi

destination_root_for() {
  local agent_name="$1"
  case "$agent_name" in
    codex)
      if [[ -n "${CODEX_SKILLS_DIR:-}" ]]; then
        printf '%s\n' "$CODEX_SKILLS_DIR"
      else
        [[ -n "${HOME:-}" ]] || fail "HOME is required when CODEX_SKILLS_DIR is unset."
        printf '%s\n' "$HOME/.agents/skills"
      fi
      ;;
    claude)
      if [[ -n "${CLAUDE_SKILLS_DIR:-}" ]]; then
        printf '%s\n' "$CLAUDE_SKILLS_DIR"
      else
        [[ -n "${HOME:-}" ]] || fail "HOME is required when CLAUDE_SKILLS_DIR is unset."
        printf '%s\n' "$HOME/.claude/skills"
      fi
      ;;
  esac
}

declare -a DESTINATION_LABELS=()
declare -a DESTINATION_ROOTS=()

add_destination_root() {
  local label="$1"
  local requested_root="$2"
  local resolved_root
  local index

  if [[ -L "$requested_root" && ! -e "$requested_root" ]]; then
    fail "destination root is a dangling symlink and will be preserved: $requested_root"
  fi
  if [[ -e "$requested_root" && ! -d "$requested_root" ]]; then
    fail "destination root is not a directory and will be preserved: $requested_root"
  fi
  if [[ -e "$requested_root" ]]; then
    resolved_root="$(realpath -e -- "$requested_root")"
  else
    resolved_root="$(realpath -m -- "$requested_root")"
  fi
  if [[ "$resolved_root" == "$SOURCE_DIR" || "$resolved_root" == "$SOURCE_DIR/"* ]]; then
    fail "destination root must not be the source catalog or a path inside it: $resolved_root"
  fi

  for ((index = 0; index < ${#DESTINATION_ROOTS[@]}; index++)); do
    if [[ "${DESTINATION_ROOTS[$index]}" == "$resolved_root" ]]; then
      DESTINATION_LABELS[$index]="${DESTINATION_LABELS[$index]}+$label"
      return
    fi
  done
  DESTINATION_LABELS+=("$label")
  DESTINATION_ROOTS+=("$resolved_root")
}

case "$AGENT" in
  codex)
    add_destination_root "codex" "$(destination_root_for codex)"
    ;;
  claude)
    add_destination_root "claude" "$(destination_root_for claude)"
    ;;
  both)
    add_destination_root "codex" "$(destination_root_for codex)"
    add_destination_root "claude" "$(destination_root_for claude)"
    ;;
esac

declare -a OPERATION_LABELS=()
declare -a OPERATION_ROOTS=()
declare -a OPERATION_SKILLS=()
declare -a OPERATION_SOURCES=()
declare -a OPERATION_DESTINATIONS=()
declare -a OPERATION_STATES=()
conflicts=0

for ((root_index = 0; root_index < ${#DESTINATION_ROOTS[@]}; root_index++)); do
  label="${DESTINATION_LABELS[$root_index]}"
  root="${DESTINATION_ROOTS[$root_index]}"
  for skill in "${SELECTED_SKILLS[@]}"; do
    source_skill="$(realpath -e -- "$SOURCE_DIR/$skill")"
    destination="$root/$skill"
    classify_destination "$source_skill" "$destination"

    OPERATION_LABELS+=("$label")
    OPERATION_ROOTS+=("$root")
    OPERATION_SKILLS+=("$skill")
    OPERATION_SOURCES+=("$source_skill")
    OPERATION_DESTINATIONS+=("$destination")
    OPERATION_STATES+=("$CLASSIFICATION")

    case "$ACTION:$CLASSIFICATION" in
      install:correct|install:missing|uninstall:correct|uninstall:missing)
        ;;
      install:regular-conflict|uninstall:regular-conflict)
        printf "ERROR: %s '%s' has a conflicting regular file or directory at %s; preserved.\n" \
          "$label" "$skill" "$destination" >&2
        conflicts=1
        ;;
      install:foreign-symlink|uninstall:foreign-symlink)
        printf "ERROR: %s '%s' has a foreign symlink at %s; preserved.\n" \
          "$label" "$skill" "$destination" >&2
        conflicts=1
        ;;
      install:broken-owned|uninstall:broken-owned)
        printf "ERROR: %s '%s' has a broken owned symlink at %s; preserved.\n" \
          "$label" "$skill" "$destination" >&2
        conflicts=1
        ;;
    esac
  done
done

# A removed catalog entry can leave an owned symlink dangling. For status only,
# discover direct destination links whose name and normalized target still point
# to that now-missing canonical source. Ignore unrelated destination entries.
if [[ $ACTION == "status" ]]; then
  for ((root_index = 0; root_index < ${#DESTINATION_ROOTS[@]}; root_index++)); do
    label="${DESTINATION_LABELS[$root_index]}"
    root="${DESTINATION_ROOTS[$root_index]}"
    [[ -d "$root" ]] || continue
    while IFS= read -r -d '' destination; do
      skill="$(basename -- "$destination")"
      [[ -z "${CATALOG_LOOKUP[$skill]+present}" ]] || continue
      valid_skill_name "$skill" || continue
      source_skill="$(realpath -m -- "$SOURCE_DIR/$skill")"
      [[ "$(resolve_link_target "$destination")" == "$source_skill" ]] || continue
      [[ ! -e "$destination" ]] || continue

      OPERATION_LABELS+=("$label")
      OPERATION_ROOTS+=("$root")
      OPERATION_SKILLS+=("$skill")
      OPERATION_SOURCES+=("$source_skill")
      OPERATION_DESTINATIONS+=("$destination")
      OPERATION_STATES+=("broken-owned")
    done < <(
      find "$root" -mindepth 1 -maxdepth 1 -type l -print0 | sort -z
    )
  done
fi

# Ensure status output and mutation plans still describe the validated catalog.
if ! CURRENT_CATALOG_FINGERPRINT="$(catalog_fingerprint)"; then
  fail "could not recheck the source catalog after preflight."
fi
if [[ "$CURRENT_CATALOG_FINGERPRINT" != "$VALIDATED_CATALOG_FINGERPRINT" ]]; then
  fail "source catalog changed after validation; no destination was changed."
fi

if [[ $ACTION == "status" ]]; then
  if [[ ${#OPERATION_SKILLS[@]} -eq 0 ]]; then
    printf 'INFO: catalog and selected destinations contain no managed skills.\n'
    exit 0
  fi
  conflicts=0
  for ((index = 0; index < ${#OPERATION_SKILLS[@]}; index++)); do
    case "${OPERATION_STATES[$index]}" in
      correct)
        status_text="correctly installed"
        ;;
      missing)
        status_text="missing"
        ;;
      regular-conflict)
        status_text="conflicting regular file or directory"
        conflicts=1
        ;;
      foreign-symlink)
        status_text="foreign symlink"
        conflicts=1
        ;;
      broken-owned)
        status_text="broken owned symlink"
        conflicts=1
        ;;
    esac
    printf '%s %s: %s (%s)\n' \
      "${OPERATION_LABELS[$index]}" \
      "${OPERATION_SKILLS[$index]}" \
      "$status_text" \
      "${OPERATION_DESTINATIONS[$index]}"
  done
  exit "$conflicts"
fi

if [[ $conflicts -ne 0 ]]; then
  fail "preflight found conflicts; no destination was changed."
fi

if [[ $ACTION == "install" && $DRY_RUN -eq 0 ]]; then
  for root in "${DESTINATION_ROOTS[@]}"; do
    mkdir -p -- "$root"
  done
fi

for ((index = 0; index < ${#OPERATION_SKILLS[@]}; index++)); do
  label="${OPERATION_LABELS[$index]}"
  skill="${OPERATION_SKILLS[$index]}"
  source_skill="${OPERATION_SOURCES[$index]}"
  destination="${OPERATION_DESTINATIONS[$index]}"
  state="${OPERATION_STATES[$index]}"

  if [[ $DRY_RUN -eq 0 ]]; then
    if [[ $ACTION == "install" ]]; then
      if [[ -L "$source_skill" || ! -d "$source_skill" || -L "$source_skill/SKILL.md" || ! -f "$source_skill/SKILL.md" ]]; then
        fail "$label '$skill' source changed after preflight; no link was created."
      fi
      if [[ "$(realpath -e -- "$source_skill")" != "$source_skill" ]]; then
        fail "$label '$skill' source no longer resolves to its validated path; no link was created."
      fi
    fi
    classify_destination "$source_skill" "$destination"
    if [[ "$CLASSIFICATION" != "$state" ]]; then
      fail "$label '$skill' changed after preflight at $destination; preserved."
    fi
  fi

  if [[ $ACTION == "install" ]]; then
    if [[ "$state" == "correct" ]]; then
      printf "%s '%s' is already installed at %s.\n" "$label" "$skill" "$destination"
    elif [[ $DRY_RUN -eq 1 ]]; then
      printf "DRY-RUN: would install %s '%s': %s -> %s\n" \
        "$label" "$skill" "$destination" "$source_skill"
    else
      if [[ "$(catalog_fingerprint)" != "$VALIDATED_CATALOG_FINGERPRINT" ]]; then
        fail "source catalog changed during installation; no further links were created."
      fi
      ln -s -- "$source_skill" "$destination"
      printf "Installed %s '%s': %s -> %s\n" \
        "$label" "$skill" "$destination" "$source_skill"
    fi
  else
    if [[ "$state" == "missing" ]]; then
      printf "%s '%s' is already absent at %s.\n" "$label" "$skill" "$destination"
    elif [[ $DRY_RUN -eq 1 ]]; then
      printf "DRY-RUN: would uninstall %s '%s' from %s\n" \
        "$label" "$skill" "$destination"
    else
      # Preflight and the adjacent recheck proved this exact symlink is owned.
      unlink -- "$destination"
      printf "Uninstalled %s '%s' from %s.\n" "$label" "$skill" "$destination"
    fi
  fi
done
