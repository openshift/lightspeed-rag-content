#!/usr/bin/env python3
"""Bump a dependency's minimum version in the project or its overrides."""

from __future__ import annotations

import json
import re
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

_PACKAGE_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")
_VERSION_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9.!+_-]*\Z")
_REQUIREMENT_RE = re.compile(
    r"^(?P<leading>\s*)(?P<name>[A-Za-z0-9][A-Za-z0-9._-]*)"
    r"(?P<extras>\s*\[[^\]]*\])?(?P<rest>.*)$"
)
_GE_RE = re.compile(
    r"(?P<leading>\s*)>=(?P<gap>\s*)(?P<old>[^,\s]+)(?P<trailing>\s*)\Z"
)
_TABLE_HEADER_RE = re.compile(
    r"^\s*\[+(?P<name>[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)*)\]+\s*(?:#.*)?(?:\r?\n)?$"
)
_DEPENDENCIES_RE = re.compile(
    r"^[ \t]*(?:dependencies|\"dependencies\"|'dependencies')[ \t]*="
)
_OPTIONAL_GROUP_RE = re.compile(
    r"""^[ \t]*(?P<key>(?:[A-Za-z0-9_-]+|"[^"]+"|'[^']+'))[ \t]*="""
)


@dataclass(frozen=True)
class Requirement:
    """Parts of a requirement string needed to identify and rewrite it."""

    name: str
    prefix: str
    rest: str


def _canonical_name(name: str) -> str:
    """Normalize a project name according to PEP 503."""
    return re.sub(r"[-_.]+", "-", name).lower()


def _parse_requirement(value: str) -> Requirement | None:
    """Extract a requirement's project name and its remaining text."""
    match = _REQUIREMENT_RE.match(value)
    if match is None:
        return None
    return Requirement(
        name=match.group("name"),
        prefix=value[: match.start("rest")],
        rest=match.group("rest"),
    )


def _bump_requirement(value: str, version: str) -> str:
    """Set a requirement's minimum version while retaining an existing >= tail."""
    parsed = _parse_requirement(value)
    if parsed is None:
        raise ValueError(f"Cannot parse requirement: {value!r}")
    if parsed.rest.lstrip().startswith("@"):
        raise ValueError(
            f"Cannot bump {parsed.name}: direct-URL requirements cannot be rewritten"
        )

    marker_start = parsed.rest.find(";")
    if marker_start == -1:
        specifier = parsed.rest
        marker = ""
    else:
        specifier = parsed.rest[:marker_start]
        marker = parsed.rest[marker_start:]

    body = specifier.strip()
    if not body:
        # A bare requirement may have whitespace before a marker; leave it in place.
        updated_specifier = f">={version}{specifier}"
    else:
        leading = specifier[: len(specifier) - len(specifier.lstrip())]
        trailing = specifier[len(specifier.rstrip()) :]
        constraints = body.split(",")
        updated_constraints: list[str] = []
        found_floor = False
        for constraint in constraints:
            floor = _GE_RE.fullmatch(constraint)
            if floor is None:
                updated_constraints.append(constraint)
                continue
            found_floor = True
            updated_constraints.append(
                f"{floor.group('leading')}>={floor.group('gap')}"
                f"{version}{floor.group('trailing')}"
            )

        if found_floor:
            updated_body = ",".join(updated_constraints)
        else:
            # Other operators do not describe the requested lower-bound update.
            updated_body = f">={version}"
        updated_specifier = f"{leading}{updated_body}{trailing}"

    return f"{parsed.prefix}{updated_specifier}{marker}"


def _read_text(path: Path) -> str:
    """Read UTF-8 text without normalizing existing line endings."""
    with path.open("r", encoding="utf-8", newline="") as stream:
        return stream.read()


def _write_text(path: Path, value: str) -> None:
    """Write UTF-8 text without translating line endings."""
    with path.open("w", encoding="utf-8", newline="") as stream:
        stream.write(value)


def _toml_table_name(line: str) -> str | None:
    """Return the simple dotted name of a TOML table header."""
    match = _TABLE_HEADER_RE.fullmatch(line)
    return match.group("name") if match else None


def _find_project_dependencies_array(text: str) -> tuple[int, int] | None:
    """Find the opening and closing offsets of [project].dependencies."""
    project_start: int | None = None
    project_end = len(text)
    offset = 0
    for line in text.splitlines(keepends=True):
        table_name = _toml_table_name(line)
        if table_name is not None:
            if project_start is not None:
                project_end = offset
                break
            if table_name == "project":
                project_start = offset + len(line)
        offset += len(line)

    if project_start is None:
        return None

    offset = project_start
    for line in text[project_start:project_end].splitlines(keepends=True):
        assignment = _DEPENDENCIES_RE.match(line)
        if assignment is not None:
            value_offset = offset + assignment.end()
            value_offset = _skip_toml_trivia(text, value_offset, project_end)
            if value_offset >= project_end or text[value_offset] != "[":
                return None
            closing = _find_array_end(text, value_offset, project_end)
            return (value_offset, closing) if closing is not None else None
        offset += len(line)
    return None


def _decode_toml_key(key: str) -> str:
    """Decode one TOML key literal."""
    parsed = tomllib.loads(f"{key} = true")
    if len(parsed) != 1:
        raise ValueError(f"Invalid optional dependency key: {key}")
    name, value = next(iter(parsed.items()))
    if not isinstance(value, bool):
        raise ValueError(f"Invalid optional dependency key: {key}")
    return name


def _find_project_optional_dependency_arrays(
    text: str,
) -> dict[str, tuple[int, int]]:
    """Find source spans for arrays in [project.optional-dependencies]."""
    section_start: int | None = None
    section_end = len(text)
    offset = 0
    for line in text.splitlines(keepends=True):
        table_name = _toml_table_name(line)
        if section_start is not None and table_name is not None:
            section_end = offset
            break
        if table_name == "project.optional-dependencies":
            section_start = offset + len(line)
        offset += len(line)

    if section_start is None:
        return {}

    arrays: dict[str, tuple[int, int]] = {}
    offset = section_start
    while offset < section_end:
        newline = text.find("\n", offset, section_end)
        line_end = section_end if newline == -1 else newline + 1
        line = text[offset:line_end]
        assignment = _OPTIONAL_GROUP_RE.match(line)
        if assignment is None:
            offset = line_end
            continue

        group = _decode_toml_key(assignment.group("key"))
        value_offset = offset + assignment.end()
        value_offset = _skip_toml_trivia(text, value_offset, section_end)
        if value_offset >= section_end or text[value_offset] != "[":
            raise ValueError(
                f"[project.optional-dependencies].{group} must be an array"
            )
        closing = _find_array_end(text, value_offset, section_end)
        if closing is None:
            raise ValueError(
                f"Could not locate the {group!r} optional dependency array"
            )
        arrays[group] = (value_offset, closing)
        offset = closing + 1

    return arrays


def _skip_toml_trivia(text: str, offset: int, limit: int) -> int:
    """Skip TOML whitespace and comments up to a source boundary."""
    while offset < limit:
        if text[offset].isspace():
            offset += 1
        elif text[offset] == "#":
            newline = text.find("\n", offset, limit)
            offset = limit if newline == -1 else newline + 1
        else:
            break
    return offset


def _toml_string_end(text: str, offset: int, limit: int) -> int:
    """Find the end of a TOML string token beginning at offset."""
    quote = text[offset]
    delimiter = quote * 3 if text.startswith(quote * 3, offset) else quote
    index = offset + len(delimiter)
    while index < limit:
        if quote == '"' and text[index] == "\\":
            index += 2
        elif text.startswith(delimiter, index):
            return index + len(delimiter)
        else:
            index += 1
    raise ValueError("Unterminated string in [project].dependencies")


def _find_array_end(text: str, opening: int, limit: int) -> int | None:
    """Find the matching closing bracket for a TOML array."""
    depth = 0
    index = opening
    while index < limit:
        character = text[index]
        if character in "\"'":
            index = _toml_string_end(text, index, limit)
            continue
        if character == "#":
            newline = text.find("\n", index, limit)
            index = limit if newline == -1 else newline + 1
            continue
        if character == "[":
            depth += 1
        elif character == "]":
            depth -= 1
            if depth == 0:
                return index
        index += 1
    return None


def _toml_array_strings(
    text: str, opening: int, closing: int
) -> list[tuple[int, int, str]]:
    """Return source spans and decoded values for a string-only TOML array."""
    entries: list[tuple[int, int, str]] = []
    offset = opening + 1
    while True:
        offset = _skip_toml_trivia(text, offset, closing)
        if offset >= closing:
            return entries
        if text[offset] == ",":
            offset += 1
            continue
        if text[offset] not in "\"'":
            raise ValueError("[project].dependencies must contain strings")
        end = _toml_string_end(text, offset, closing + 1)
        literal = text[offset:end]
        value = tomllib.loads(f"dependency = {literal}")["dependency"]
        if not isinstance(value, str):
            raise ValueError("[project].dependencies must contain strings")
        entries.append((offset, end, value))
        offset = end
        offset = _skip_toml_trivia(text, offset, closing)
        if offset < closing and text[offset] == ",":
            offset += 1
        elif offset < closing:
            raise ValueError("Malformed [project].dependencies array")


def _encode_toml_string(value: str, original: str) -> str:
    """Encode an updated requirement, retaining literal quote style if safe."""
    if (
        original.startswith("'")
        and "'" not in value
        and "\n" not in value
        and "\r" not in value
    ):
        return f"'{value}'"
    return json.dumps(value, ensure_ascii=False)


def _matches_dependency(dependency: object, target: str) -> bool:
    """Return whether a dependency uses the target's normalized package name."""
    if not isinstance(dependency, str):
        return False
    parsed = _parse_requirement(dependency)
    return parsed is not None and _canonical_name(parsed.name) == target


def _project_dependency_groups(
    project: dict[str, object],
) -> tuple[list[object], dict[str, list[object]]]:
    """Validate and return PEP 621 core and optional dependency groups."""
    dependencies = project.get("dependencies", [])
    if not isinstance(dependencies, list):
        raise ValueError("[project].dependencies must be an array")
    optional_dependencies = project.get("optional-dependencies", {})
    if not isinstance(optional_dependencies, dict):
        raise ValueError("[project.optional-dependencies] must be a table")

    optional_groups: dict[str, list[object]] = {}
    for group, group_dependencies in optional_dependencies.items():
        if not isinstance(group, str) or not isinstance(group_dependencies, list):
            raise ValueError(
                f"[project.optional-dependencies].{group} must be an array"
            )
        optional_groups[group] = group_dependencies
    return dependencies, optional_groups


def _matching_optional_dependencies(
    optional_groups: dict[str, list[object]], target: str
) -> dict[str, list[object]]:
    """Return optional groups containing a dependency with the target name."""
    return {
        group: dependencies
        for group, dependencies in optional_groups.items()
        if any(_matches_dependency(dependency, target) for dependency in dependencies)
    }


def _find_matching_dependency_arrays(
    text: str,
    dependencies: list[object],
    core_matches: bool,
    optional_matches: dict[str, list[object]],
) -> list[tuple[list[object], tuple[int, int]]]:
    """Locate the source arrays for matching core and optional dependencies."""
    arrays: list[tuple[list[object], tuple[int, int]]] = []
    if core_matches:
        core_array = _find_project_dependencies_array(text)
        if core_array is None:
            raise ValueError("Could not locate the [project].dependencies array")
        arrays.append((dependencies, core_array))

    if optional_matches:
        optional_arrays = _find_project_optional_dependency_arrays(text)
        for group, group_dependencies in optional_matches.items():
            optional_array = optional_arrays.get(group)
            if optional_array is None:
                raise ValueError(
                    f"Could not locate the {group!r} optional dependency array"
                )
            arrays.append((group_dependencies, optional_array))
    return arrays


def _dependency_array_replacements(
    text: str,
    dependencies: list[object],
    array: tuple[int, int],
    target: str,
    version: str,
) -> list[tuple[int, int, str]]:
    """Return source replacements for target requirements in one TOML array."""
    opening, closing = array
    entries = _toml_array_strings(text, opening, closing)
    if len(entries) != len(dependencies):
        raise ValueError("Could not map project dependency entries in pyproject.toml")

    replacements: list[tuple[int, int, str]] = []
    for (start, end, source_value), dependency in zip(entries, dependencies):
        if not isinstance(dependency, str) or source_value != dependency:
            raise ValueError(
                "Could not map project dependency entries in pyproject.toml"
            )
        parsed = _parse_requirement(dependency)
        if parsed is None or _canonical_name(parsed.name) != target:
            continue
        if parsed.rest.lstrip().startswith("@"):
            raise ValueError(
                f"Cannot bump {parsed.name}: direct-URL requirements cannot be rewritten"
            )
        bumped = _bump_requirement(dependency, version)
        if bumped != dependency:
            literal = text[start:end]
            replacements.append((start, end, _encode_toml_string(bumped, literal)))
    return replacements


def _update_pyproject(path: Path, package: str, version: str) -> bool:
    """Update matching PEP 621 dependencies, returning whether any were present."""
    if not path.is_file():
        return False
    text = _read_text(path)
    document = tomllib.loads(text)
    project = document.get("project", {})
    if not isinstance(project, dict):
        return False

    dependencies, optional_groups = _project_dependency_groups(project)
    target = _canonical_name(package)
    core_matches = any(
        _matches_dependency(dependency, target) for dependency in dependencies
    )
    optional_matches = _matching_optional_dependencies(optional_groups, target)
    if not core_matches and not optional_matches:
        return False

    arrays = _find_matching_dependency_arrays(
        text, dependencies, core_matches, optional_matches
    )
    replacements: list[tuple[int, int, str]] = []
    for group_dependencies, array in arrays:
        replacements.extend(
            _dependency_array_replacements(
                text, group_dependencies, array, target, version
            )
        )
    if replacements:
        for start, end, replacement in reversed(replacements):
            text = f"{text[:start]}{replacement}{text[end:]}"
        _write_text(path, text)
    return True


def _line_parts(line: str) -> tuple[str, str, str]:
    """Separate a requirement line into content, inline comment, and newline."""
    if line.endswith("\r\n"):
        content, newline = line[:-2], "\r\n"
    elif line.endswith(("\n", "\r")):
        content, newline = line[:-1], line[-1:]
    else:
        content, newline = line, ""
    if content.lstrip().startswith("#"):
        return content, "", newline
    comment = re.search(r"[ \t]+#", content)
    if comment is None:
        return content, "", newline
    return content[: comment.start()], content[comment.start() :], newline


def _update_overrides(path: Path, package: str, version: str) -> bool:
    """Update a matching override or append a new constraint; return if updated."""
    text = _read_text(path) if path.is_file() else ""
    target = _canonical_name(package)
    lines = text.splitlines(keepends=True)
    updated_lines: list[str] = []
    found = False

    for line in lines:
        content, comment, newline = _line_parts(line)
        parsed = _parse_requirement(content)
        if parsed is None or _canonical_name(parsed.name) != target:
            updated_lines.append(line)
            continue
        if parsed.rest.lstrip().startswith("@"):
            raise ValueError(
                f"Cannot bump {parsed.name}: direct-URL requirements cannot be rewritten"
            )
        found = True
        updated_lines.append(f"{_bump_requirement(content, version)}{comment}{newline}")

    if not found:
        if text and not text.endswith(("\n", "\r")):
            updated_lines.append("\n")
        updated_lines.append(f"{package}>={version}\n")
    new_text = "".join(updated_lines)
    if new_text != text:
        _write_text(path, new_text)
    return found


def main(argv: Sequence[str] | None = None) -> int:
    """Run the bump helper from the current working directory."""
    arguments = sys.argv[1:] if argv is None else argv
    if len(arguments) != 2:
        print("Usage: bump_dep.py <package> <version>", file=sys.stderr)
        return 2
    package, version = arguments
    if not _PACKAGE_RE.fullmatch(package):
        print("Error: package must be a valid project name", file=sys.stderr)
        return 2
    if not _VERSION_RE.fullmatch(version):
        print("Error: version must be a single version token", file=sys.stderr)
        return 2

    pyproject = Path("pyproject.toml")
    overrides = Path("requirements.overrides.txt")
    try:
        if _update_pyproject(pyproject, package, version):
            print(f"Updated {package}>={version} in {pyproject}")
        elif _update_overrides(overrides, package, version):
            print(f"Updated {package}>={version} in {overrides}")
        else:
            print(f"Added {package}>={version} to {overrides}")
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
