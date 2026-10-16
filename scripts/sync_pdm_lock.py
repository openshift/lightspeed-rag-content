#!/usr/bin/env python3
"""Refresh the PDM CPU lock alongside Konflux dependency outputs."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
from pathlib import Path

PDM_VERSION = "2.29.2"
PYTHON_VERSION = "3.12"
LOCKFILE = "pdm.lock.cpu"
OVERRIDES_FILE = Path("requirements.overrides.txt")
SANITIZED_ENV_VARS = (
    "UV_CONFIG_FILE",
    "UV_INDEX_URL",
    "UV_DEFAULT_INDEX",
    "UV_INDEX",
    "UV_EXTRA_INDEX_URL",
    "PIP_INDEX_URL",
    "PIP_EXTRA_INDEX_URL",
    "PDM_OVERRIDE",
)
PACKAGE_NAME_RE = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*)")


def normalize_package_name(name: str) -> str:
    """Normalize a package name as specified by PEP 503."""
    return re.sub(r"[-_.]+", "-", name).lower()


def read_override_packages(path: Path) -> list[str]:
    """Return unique package names in a pip-style constraints file."""
    packages: list[str] = []
    seen: set[str] = set()

    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), 1
    ):
        requirement = line.strip()
        if not requirement or requirement.startswith("#"):
            continue
        match = PACKAGE_NAME_RE.match(requirement)
        if match is None:
            raise ValueError(f"Unsupported requirement on line {line_number} of {path}")
        package = match.group(1)
        normalized = normalize_package_name(package)
        if normalized not in seen:
            packages.append(package)
            seen.add(normalized)

    return packages


def sanitized_environment() -> dict[str, str]:
    """Prevent machine-specific package indexes from leaking into lock output."""
    env = os.environ.copy()
    for name in SANITIZED_ENV_VARS:
        env.pop(name, None)
    env["UV_NO_CONFIG"] = "1"
    return env


def run_pdm(arguments: list[str], env: dict[str, str]) -> None:
    """Run the pinned PDM version without installing packages into the project."""
    command = ["uvx", "-p", PYTHON_VERSION, f"pdm@{PDM_VERSION}", *arguments]
    # This argv list uses a fixed executable and runs without a shell.
    subprocess.run(command, check=True, env=env)  # noqa: S603


def main() -> None:
    """Refresh the CPU lock in targeted or full-refresh mode."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "package",
        nargs="?",
        help="dependency being bumped (optional)",
    )
    parser.add_argument(
        "--update-all",
        action="store_true",
        help="refresh every locked package to the newest version allowed by "
        "pyproject.toml and requirements.overrides.txt",
    )
    args = parser.parse_args()

    if args.update_all and args.package:
        parser.error("--update-all cannot be combined with a package name")

    if not OVERRIDES_FILE.is_file():
        parser.error(f"Missing override file: {OVERRIDES_FILE}")

    try:
        override_packages = read_override_packages(OVERRIDES_FILE)
    except ValueError as exc:
        parser.error(str(exc))

    packages = list(override_packages)
    if args.package:
        normalized_requested = normalize_package_name(args.package)
        if all(
            normalize_package_name(name) != normalized_requested for name in packages
        ):
            packages.append(args.package)

    env = sanitized_environment()
    try:
        if args.update_all:
            # A fresh lock without --update-reuse resolves every package to
            # the newest version allowed by pyproject.toml and the overrides.
            run_pdm(
                [
                    "lock",
                    "-L",
                    LOCKFILE,
                    "-G",
                    ":all",
                    "--override",
                    str(OVERRIDES_FILE),
                ],
                env,
            )
            return
        run_pdm(
            [
                "lock",
                "-L",
                LOCKFILE,
                "-G",
                ":all",
                "--update-reuse",
                "--override",
                str(OVERRIDES_FILE),
            ],
            env,
        )
        # --update-reuse does not refresh a locked transitive package just because
        # a constraints-file floor changed, so explicitly update every override.
        if packages:
            run_pdm(
                [
                    "update",
                    *packages,
                    "--no-sync",
                    "--update-reuse",
                    "-L",
                    LOCKFILE,
                    "--override",
                    str(OVERRIDES_FILE),
                ],
                env,
            )
    except FileNotFoundError as exc:
        parser.error(f"uvx is required to run the pinned PDM tool: {exc}")
    except subprocess.CalledProcessError as exc:
        raise SystemExit(exc.returncode) from None


if __name__ == "__main__":
    main()
