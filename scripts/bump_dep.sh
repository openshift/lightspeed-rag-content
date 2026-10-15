#!/usr/bin/env bash
# bump_dep.sh — bump a single Python dependency for CVE fixes.
#
# Usage:
#   scripts/bump_dep.sh <package>              # add/update in requirements.overrides.txt
#   scripts/bump_dep.sh <package> <version>    # bump to exact minimum version
#
# Behavior:
#   1. If the package has a version pin in pyproject.toml [project] dependencies,
#      update the version specifier there.
#   2. If the package appears in requirements.overrides.txt, update or add it.
#   3. If the package is not found in either file, add it to
#      requirements.overrides.txt (CVE override pattern).

set -euo pipefail

PYPROJECT="pyproject.toml"
OVERRIDES="requirements.overrides.txt"

PKG="${1:-}"
VERSION="${2:-}"

if [[ -z "$PKG" ]]; then
    echo "Usage: $0 <package> [version]" >&2
    exit 1
fi

if [[ -z "$VERSION" ]]; then
    echo "Error: VERSION is required (e.g. $0 $PKG 2.7.0)" >&2
    exit 1
fi

# Normalise package name: PyPI treats hyphens and underscores as equivalent;
# PEP 503 lowercases, but pyproject.toml may use either case.  Build a regex
# that matches any mix of hyphen/underscore case-insensitively.
pkg_regex=$(echo "$PKG" | sed 's/[-_]/[-_]/g')

updated=0

# --- 1. Try pyproject.toml ---------------------------------------------------
if grep -qiE "^[[:space:]]+\"${pkg_regex}(>|<|=|!|~| |\")" "$PYPROJECT"; then
    echo "Updating $PKG>=$VERSION in $PYPROJECT ..."
    # Replace the version specifier on the matching dependency line.
    # Handles forms like: "urllib3>=2.6.3", "aiohttp>=3.8.0,<4", "PyYAML"
    sed -i -E \
        "s/^([[:space:]]+\"${pkg_regex})(>=?[^\"]*)(\")/\1>=${VERSION}\3/I" \
        "$PYPROJECT"
    updated=1
fi

# --- 2. Try requirements.overrides.txt ----------------------------------------
if [[ -f "$OVERRIDES" ]]; then
    if grep -qiE "^${pkg_regex}(>|<|=|!|~| |$)" "$OVERRIDES"; then
        echo "Updating $PKG>=$VERSION in $OVERRIDES ..."
        sed -i -E \
            "s/^(${pkg_regex})(>=?[^ ]*)/\1>=${VERSION}/I" \
            "$OVERRIDES"
        updated=1
    fi
fi

# --- 3. Not found anywhere — add to overrides ---------------------------------
if [[ "$updated" -eq 0 ]]; then
    echo "Adding $PKG>=$VERSION to $OVERRIDES (CVE override) ..."
    echo "${PKG}>=${VERSION}" >> "$OVERRIDES"
    updated=1
fi

echo "Done.  Remember to regenerate hermetic requirements:"
echo "  make update-konflux-deps"
