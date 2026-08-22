#!/usr/bin/env python3
"""Validate a portable Agent Skills catalog without executing skill scripts."""

from __future__ import annotations

import argparse
import re
import shlex
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

try:
    import yaml
    from yaml.constructor import ConstructorError
except ModuleNotFoundError:
    print(
        "ERROR: PyYAML is required; create and activate a virtual environment, "
        "then run 'python -m pip install -r requirements-dev.txt'.",
        file=sys.stderr,
    )
    raise SystemExit(2)


NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TRIGGER_CUE_PATTERN = re.compile(
    r"\bwhen(?:ever)?\b|\bfor\b|"
    r"\b(?:use|uses|trigger|triggers|apply|applies|invoke|invokes)"
    r"(?:\s+\w+){0,3}\s+on\b",
    re.IGNORECASE,
)
PLACEHOLDER_PATTERNS = (
    re.compile(r"\b(?:TODO|TBD|FIXME)\b", re.IGNORECASE),
    re.compile(r"\bPLACEHOLDER\b", re.IGNORECASE),
    re.compile(r"\bREPLACE[_ -]?ME\b", re.IGNORECASE),
    re.compile(r"\[\s*INSERT\b[^\]]*\]", re.IGNORECASE),
    re.compile(r"\[\s*DESCRIBE\b[^\]]*\]", re.IGNORECASE),
    re.compile(
        r"\{\{\s*(?:SKILL[_ -]?NAME|YOUR[_ -]?(?:INSTRUCTIONS?|DESCRIPTION)|"
        r"DESCRIPTION|INSTRUCTIONS?[_ -]?HERE)\s*\}\}",
        re.IGNORECASE,
    ),
)
ALLOWED_FRONTMATTER_KEYS = {"name", "description"}
EXTERNAL_SCHEMES = {"http", "https", "mailto", "ftp", "ftps", "data"}
CACHE_NAMES = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".cache",
    ".nox",
    ".tox",
    ".venv",
    "node_modules",
    "venv",
}
MACHINE_FILES = {".ds_store", "thumbs.db"}
PRIVATE_KEY_NAMES = {"id_rsa", "id_dsa", "id_ecdsa", "id_ed25519"}
CONTAINER_PREFIX_PATTERN = re.compile(
    r"^(?: {0,3}>[ \t]?| {0,3}(?:[-+*]|\d{1,9}[.)])[ \t]+)"
)


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def _construct_unique_mapping(
    loader: UniqueKeyLoader, node: yaml.nodes.MappingNode, deep: bool = False
) -> dict[object, object]:
    loader.flatten_mapping(node)
    mapping: dict[object, object] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as exc:
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "found an unhashable mapping key",
                key_node.start_mark,
            ) from exc
        if duplicate:
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


class Reporter:
    def __init__(self) -> None:
        self.errors: list[str] = []

    def error(self, path: Path, message: str, line: int | None = None) -> None:
        location = f"{path}:{line}" if line is not None else str(path)
        self.errors.append(f"ERROR {location}: {message}")


def is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def load_yaml(text: str) -> object:
    return yaml.load(text, Loader=UniqueKeyLoader)


def split_frontmatter(
    skill_file: Path, text: str, reporter: Reporter
) -> tuple[object | None, str, int] | None:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        reporter.error(
            skill_file,
            "SKILL.md must start with an opening YAML frontmatter delimiter '---'.",
            1,
        )
        return None

    closing_index = next(
        (index for index, line in enumerate(lines[1:], start=1) if line == "---"),
        None,
    )
    if closing_index is None:
        reporter.error(
            skill_file,
            "add a closing YAML frontmatter delimiter '---'.",
            1,
        )
        return None

    yaml_text = "\n".join(lines[1:closing_index])
    try:
        frontmatter = load_yaml(yaml_text)
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        line = (mark.line + 2) if mark is not None else 2
        problem = getattr(exc, "problem", None) or str(exc).splitlines()[0]
        reporter.error(skill_file, f"fix invalid YAML frontmatter ({problem}).", line)
        frontmatter = None

    body = "\n".join(lines[closing_index + 1 :])
    return frontmatter, body, closing_index + 2


def validate_frontmatter(
    skill_dir: Path,
    skill_file: Path,
    frontmatter: object,
    seen_names: dict[str, Path],
    reporter: Reporter,
) -> None:
    if not isinstance(frontmatter, dict):
        reporter.error(
            skill_file,
            "YAML frontmatter must be a mapping with only 'name' and 'description'.",
            2,
        )
        return

    extra_keys = sorted(str(key) for key in frontmatter if key not in ALLOWED_FRONTMATTER_KEYS)
    if extra_keys:
        reporter.error(
            skill_file,
            "remove non-portable frontmatter field(s): " + ", ".join(extra_keys) + ".",
            2,
        )

    missing_keys = sorted(ALLOWED_FRONTMATTER_KEYS - set(frontmatter))
    if missing_keys:
        reporter.error(
            skill_file,
            "add required frontmatter field(s): " + ", ".join(missing_keys) + ".",
            2,
        )

    name = frontmatter.get("name")
    if not isinstance(name, str) or not name.strip():
        reporter.error(skill_file, "'name' must be a nonempty string.", 2)
    else:
        normalized_name = name.strip()
        if normalized_name != name:
            reporter.error(skill_file, "'name' must not have surrounding whitespace.", 2)
        if len(normalized_name) >= 64:
            reporter.error(
                skill_file,
                "'name' must be shorter than 64 characters for this catalog.",
                2,
            )
        if not NAME_PATTERN.fullmatch(normalized_name):
            reporter.error(
                skill_file,
                "'name' must use lowercase letters, digits, and single hyphens only.",
                2,
            )
        if normalized_name != skill_dir.name:
            reporter.error(
                skill_file,
                f"'name' must match its directory name '{skill_dir.name}'.",
                2,
            )
        previous = seen_names.get(normalized_name)
        if previous is not None:
            reporter.error(
                skill_file,
                f"duplicate skill name '{normalized_name}' also appears in {previous}.",
                2,
            )
        else:
            seen_names[normalized_name] = skill_file

    description = frontmatter.get("description")
    if not isinstance(description, str) or not description.strip():
        reporter.error(skill_file, "'description' must be a nonempty string.", 2)
    else:
        normalized_description = description.strip()
        if len(normalized_description) > 1024:
            reporter.error(
                skill_file,
                "'description' must not exceed 1024 characters.",
                2,
            )
        description_words = re.findall(r"[A-Za-z0-9]+", normalized_description)
        if len(description_words) < 4 or TRIGGER_CUE_PATTERN.search(normalized_description) is None:
            reporter.error(
                skill_file,
                "'description' must state both what the skill does and when or for which requests it should trigger.",
                2,
            )


def link_destination(raw_destination: str) -> str:
    raw_destination = raw_destination.strip()
    if raw_destination.startswith("<"):
        closing = raw_destination.find(">")
        if closing == -1:
            raise ValueError("close angle-bracketed link destinations with '>'.")
        return raw_destination[1:closing]

    try:
        pieces = shlex.split(raw_destination, comments=False, posix=True)
    except ValueError as exc:
        raise ValueError(f"fix malformed link destination ({exc}).") from exc
    if not pieces:
        raise ValueError("provide a nonempty link destination.")
    return pieces[0]


def inline_link_destinations(text: str) -> tuple[list[tuple[str, int]], list[int]]:
    """Return Markdown links with balanced labels and destinations."""
    destinations: list[tuple[str, int]] = []
    malformed_positions: list[int] = []
    cursor = 0

    while cursor < len(text):
        if text[cursor] == "\\":
            cursor += 2
            continue
        if text[cursor] == "!" and cursor + 1 < len(text) and text[cursor + 1] == "[":
            label_start = cursor + 1
        elif text[cursor] == "[":
            label_start = cursor
        else:
            cursor += 1
            continue

        label_depth = 1
        escaped = False
        label_end = None
        for index in range(label_start + 1, len(text)):
            character = text[index]
            if escaped:
                escaped = False
                continue
            if character == "\\":
                escaped = True
            elif character == "[":
                label_depth += 1
            elif character == "]":
                label_depth -= 1
                if label_depth == 0:
                    label_end = index
                    break

        if label_end is None:
            cursor = label_start + 1
            continue
        if label_end + 1 >= len(text) or text[label_end + 1] != "(":
            cursor = label_end + 1
            continue

        destination_start = label_end + 2
        depth = 1
        escaped = False
        quote = ""
        in_angle_destination = False

        for index in range(destination_start, len(text)):
            character = text[index]
            if escaped:
                escaped = False
                continue
            if character == "\\":
                escaped = True
                continue
            if character in {'"', "'"} and not in_angle_destination:
                quote = "" if quote == character else character if not quote else quote
                continue
            if quote:
                continue
            if character == "<" and not text[destination_start:index].strip():
                in_angle_destination = True
                continue
            if character == ">" and in_angle_destination:
                in_angle_destination = False
                continue
            if in_angle_destination:
                continue
            if character == "(":
                depth += 1
            elif character == ")":
                depth -= 1
                if depth == 0:
                    destinations.append((text[destination_start:index], destination_start))
                    cursor = index + 1
                    break
        else:
            malformed_positions.append(destination_start)
            cursor = destination_start

    return destinations, malformed_positions


def reference_definition_destination(line_text: str) -> str | None:
    candidate = line_text
    while prefix := CONTAINER_PREFIX_PATTERN.match(candidate):
        candidate = candidate[prefix.end() :]

    leading_spaces = len(candidate) - len(candidate.lstrip(" "))
    if leading_spaces > 3 or leading_spaces >= len(candidate):
        return None
    if candidate[leading_spaces] != "[":
        return None

    depth = 1
    escaped = False
    for index in range(leading_spaces + 1, len(candidate)):
        character = candidate[index]
        if escaped:
            escaped = False
            continue
        if character == "\\":
            escaped = True
        elif character == "[":
            depth += 1
        elif character == "]":
            depth -= 1
            if depth == 0:
                if index + 1 < len(candidate) and candidate[index + 1] == ":":
                    return candidate[index + 2 :]
                return None
    return None


def validate_link_destination(
    skill_dir: Path,
    resolved_root: Path,
    skill_file: Path,
    raw_destination: str,
    line_number: int,
    reporter: Reporter,
) -> None:
    try:
        destination = link_destination(raw_destination)
    except ValueError as exc:
        reporter.error(skill_file, str(exc), line_number)
        return

    if destination.startswith("#"):
        return
    if re.match(r"^[A-Za-z]:", destination):
        reporter.error(
            skill_file,
            f"replace absolute Windows link '{destination}' with a relative path.",
            line_number,
        )
        return
    if "\\" in destination:
        reporter.error(
            skill_file,
            f"replace backslashes in link '{destination}' with portable '/' separators.",
            line_number,
        )
        return

    try:
        parsed = urlsplit(destination)
    except ValueError as exc:
        reporter.error(
            skill_file,
            f"fix malformed link destination '{destination}' ({exc}).",
            line_number,
        )
        return
    if parsed.scheme.lower() in EXTERNAL_SCHEMES or parsed.netloc:
        return
    if parsed.scheme:
        reporter.error(
            skill_file,
            f"replace unsupported link scheme in '{destination}' with a relative path.",
            line_number,
        )
        return

    decoded_path = unquote(parsed.path)
    if not decoded_path:
        return
    if re.match(r"^[A-Za-z]:", decoded_path):
        reporter.error(
            skill_file,
            f"replace absolute Windows link '{destination}' with a relative path.",
            line_number,
        )
        return
    if "\\" in decoded_path:
        reporter.error(
            skill_file,
            f"replace backslashes in link '{destination}' with portable '/' separators.",
            line_number,
        )
        return
    if decoded_path.startswith(("/", "~")):
        reporter.error(
            skill_file,
            f"replace absolute link '{destination}' with a path inside the skill.",
            line_number,
        )
        return

    try:
        candidate = (skill_dir / decoded_path).resolve(strict=False)
    except (OSError, RuntimeError, ValueError) as exc:
        reporter.error(
            skill_file,
            f"link '{destination}' is not a valid local path ({exc}).",
            line_number,
        )
        return
    if not is_within(candidate, resolved_root):
        reporter.error(
            skill_file,
            f"link '{destination}' escapes the skill directory.",
            line_number,
        )
        return
    try:
        candidate_exists = candidate.exists()
        candidate_is_file = candidate.is_file() if candidate_exists else False
    except (OSError, RuntimeError, ValueError) as exc:
        reporter.error(
            skill_file,
            f"link '{destination}' cannot be inspected safely ({exc}).",
            line_number,
        )
        return
    if not candidate_exists:
        reporter.error(
            skill_file,
            f"link '{destination}' does not resolve to an existing file.",
            line_number,
        )
    elif not candidate_is_file:
        reporter.error(
            skill_file,
            f"link '{destination}' must resolve to a file, not a directory.",
            line_number,
        )


def validate_links(
    skill_dir: Path,
    skill_file: Path,
    body: str,
    body_start_line: int,
    reporter: Reporter,
) -> None:
    resolved_root = skill_dir.resolve()
    in_fence = False
    fence_character = ""
    searchable_lines: list[str] = []

    for line_text in body.splitlines():
        stripped = line_text.lstrip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[0]
            if not in_fence:
                in_fence = True
                fence_character = marker
            elif marker == fence_character:
                in_fence = False
                fence_character = ""
            searchable_lines.append("")
            continue
        if in_fence:
            searchable_lines.append("")
            continue
        searchable_lines.append(re.sub(r"`[^`]*`", "", line_text))

    searchable_body = "\n".join(searchable_lines)
    inline_destinations, malformed_positions = inline_link_destinations(searchable_body)
    for raw_destination, position in inline_destinations:
        line_number = body_start_line + searchable_body.count("\n", 0, position)
        validate_link_destination(
            skill_dir,
            resolved_root,
            skill_file,
            raw_destination,
            line_number,
            reporter,
        )
    for position in malformed_positions:
        reporter.error(
            skill_file,
            "close the Markdown link destination with a matching ')'.",
            body_start_line + searchable_body.count("\n", 0, position),
        )

    for offset, line_text in enumerate(searchable_lines):
        raw_destination = reference_definition_destination(line_text)
        if raw_destination is not None:
            validate_link_destination(
                skill_dir,
                resolved_root,
                skill_file,
                raw_destination,
                body_start_line + offset,
                reporter,
            )


def validate_placeholders(path: Path, text: str, reporter: Reporter) -> None:
    for line_number, line_text in enumerate(text.splitlines(), start=1):
        for pattern in PLACEHOLDER_PATTERNS:
            if pattern.search(line_text):
                reporter.error(
                    path,
                    f"replace unfinished template marker matching {pattern.pattern!r}.",
                    line_number,
                )
                break


def validate_artifacts(skill_dir: Path, reporter: Reporter) -> None:
    try:
        paths = sorted(skill_dir.rglob("*"))
    except (OSError, RuntimeError) as exc:
        reporter.error(skill_dir, f"make the complete skill directory readable ({exc}).")
        return

    for path in paths:
        relative = path.relative_to(skill_dir)
        lower_name = path.name.lower()

        if path.is_symlink():
            reporter.error(
                path,
                "replace this symlink with a real file or directory inside the canonical skill.",
            )
            continue
        if lower_name == ".env" or lower_name.startswith(".env."):
            reporter.error(path, "remove .env files from skills; they may contain secrets.")
        if lower_name in CACHE_NAMES:
            reporter.error(path, "remove generated cache or dependency directories from skills.")
        if lower_name in MACHINE_FILES or path.suffix.lower() in {".pyc", ".pyo"}:
            reporter.error(path, "remove generated or machine-specific files from skills.")
        if lower_name in PRIVATE_KEY_NAMES or path.suffix.lower() in {".pem", ".key", ".p12", ".pfx"}:
            reporter.error(path, "remove private-key or credential material from skills.")
        if len(relative.parts) == 1 and (
            lower_name == "readme.md" or lower_name.startswith("changelog")
        ):
            reporter.error(
                path,
                "remove per-skill README/changelog files; keep instructions in SKILL.md or references/.",
            )
        if (
            path.is_file()
            and path != skill_dir / "SKILL.md"
            and relative.parts[0] != "assets"
        ):
            try:
                supporting_text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            except OSError as exc:
                reporter.error(path, f"make this supporting file readable ({exc}).")
                continue
            validate_placeholders(path, supporting_text, reporter)


def is_shell_script(path: Path) -> bool:
    if path.suffix.lower() == ".sh":
        return True
    try:
        with path.open("rb") as handle:
            first_line = handle.readline(512).decode("ascii", errors="ignore")
    except OSError:
        return False
    return re.match(
        r"^#!.*(?:/|\s)(?:bash|sh|dash|ksh|zsh)(?:\s|$)", first_line
    ) is not None


def validate_shell_scripts(skill_dir: Path, reporter: Reporter) -> None:
    try:
        candidates = sorted(skill_dir.rglob("*"))
    except OSError as exc:
        reporter.error(skill_dir, f"make skill scripts readable for syntax checks ({exc}).")
        return

    for script in candidates:
        if not script.is_file() or script.is_symlink():
            continue
        if not is_shell_script(script):
            continue
        try:
            result = subprocess.run(
                ["bash", "-n", "--", str(script)],
                check=False,
                capture_output=True,
                text=True,
            )
        except FileNotFoundError:
            reporter.error(script, "install Bash so shell syntax can be validated.")
            return
        if result.returncode != 0:
            detail = (result.stderr or result.stdout).strip().splitlines()
            summary = detail[0] if detail else "unknown syntax error"
            reporter.error(script, f"fix Bash syntax ({summary}).")


def validate_openai_yaml(skill_dir: Path, reporter: Reporter) -> None:
    metadata_file = skill_dir / "agents" / "openai.yaml"
    if not metadata_file.exists() or metadata_file.is_symlink():
        return
    if not metadata_file.is_file():
        reporter.error(metadata_file, "agents/openai.yaml must be a regular YAML file.")
        return
    try:
        text = metadata_file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        reporter.error(metadata_file, "save agents/openai.yaml as valid UTF-8.")
        return
    except OSError as exc:
        reporter.error(metadata_file, f"make agents/openai.yaml readable ({exc}).")
        return
    try:
        data = load_yaml(text)
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        line = (mark.line + 1) if mark is not None else None
        problem = getattr(exc, "problem", None) or str(exc).splitlines()[0]
        reporter.error(metadata_file, f"fix invalid YAML ({problem}).", line)
        return
    if not isinstance(data, dict):
        reporter.error(metadata_file, "agents/openai.yaml must contain a YAML mapping.")


def validate_skill(
    skill_dir: Path, seen_names: dict[str, Path], reporter: Reporter
) -> None:
    if skill_dir.is_symlink():
        reporter.error(
            skill_dir,
            "catalog entries must be real directories, not symlinks.",
        )
        return
    if not skill_dir.is_dir():
        reporter.error(
            skill_dir,
            "every non-hidden catalog entry must be a skill directory containing SKILL.md.",
        )
        return

    skill_file = skill_dir / "SKILL.md"
    if skill_file.is_symlink():
        reporter.error(skill_file, "SKILL.md must be a real file, not a symlink.")
        return
    if not skill_file.is_file():
        reporter.error(skill_file, "add the required SKILL.md file.")
        return

    try:
        text = skill_file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        reporter.error(skill_file, "save SKILL.md as valid UTF-8.")
        return
    except OSError as exc:
        reporter.error(skill_file, f"make SKILL.md readable ({exc}).")
        return

    line_count = len(text.splitlines())
    if line_count > 500:
        reporter.error(
            skill_file,
            f"reduce SKILL.md to 500 lines or fewer (found {line_count}).",
        )

    split = split_frontmatter(skill_file, text, reporter)
    if split is not None:
        frontmatter, body, body_start_line = split
        if frontmatter is not None:
            validate_frontmatter(
                skill_dir, skill_file, frontmatter, seen_names, reporter
            )
        if not body.strip():
            reporter.error(
                skill_file,
                "add nonempty Markdown instructions after the frontmatter.",
                body_start_line,
            )
        validate_links(skill_dir, skill_file, body, body_start_line, reporter)

    validate_placeholders(skill_file, text, reporter)

    validate_artifacts(skill_dir, reporter)
    validate_shell_scripts(skill_dir, reporter)
    validate_openai_yaml(skill_dir, reporter)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate an Agent Skills catalog.")
    default_skills_dir = Path(__file__).resolve().parents[1] / "skills"
    parser.add_argument(
        "--skills-dir",
        type=Path,
        default=default_skills_dir,
        help="catalog root whose direct children are skill directories",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    reporter = Reporter()
    requested_skills_dir = args.skills_dir.expanduser()

    if requested_skills_dir.is_symlink():
        reporter.error(
            requested_skills_dir.absolute(),
            "the catalog root must be a real directory, not a symlink.",
        )
        print("\n".join(reporter.errors), file=sys.stderr)
        return 1

    try:
        skills_dir = requested_skills_dir.resolve()
    except (OSError, RuntimeError) as exc:
        reporter.error(
            requested_skills_dir.absolute(),
            f"resolve the catalog path after fixing the filesystem error ({exc}).",
        )
        print("\n".join(reporter.errors), file=sys.stderr)
        return 1

    if not skills_dir.exists():
        reporter.error(skills_dir, "create the catalog directory before validating it.")
    elif not skills_dir.is_dir():
        reporter.error(skills_dir, "the catalog root must be a real directory.")

    if reporter.errors:
        print("\n".join(reporter.errors), file=sys.stderr)
        return 1

    try:
        entries = sorted(
            path for path in skills_dir.iterdir() if not path.name.startswith(".")
        )
    except OSError as exc:
        reporter.error(skills_dir, f"make the catalog readable ({exc}).")
        print("\n".join(reporter.errors), file=sys.stderr)
        return 1
    if not entries:
        print(f"INFO {skills_dir}: catalog contains no production skills.")
        return 0

    seen_names: dict[str, Path] = {}
    for entry in entries:
        validate_skill(entry, seen_names, reporter)

    if reporter.errors:
        print("\n".join(reporter.errors), file=sys.stderr)
        print(
            f"FAILED: found {len(reporter.errors)} validation error(s) "
            f"across {len(entries)} catalog entry(ies).",
            file=sys.stderr,
        )
        return 1

    print(f"OK {skills_dir}: validated {len(entries)} skill(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
