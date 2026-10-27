#!/usr/bin/env bash
# Download onnxruntime's FetchContent dependencies into a mirror directory.
#
# Downloads the actual source archives from GitHub (so SHA1 hashes match)
# and places them in the mirror directory structure that onnxruntime's
# cmake expects. The cmake build then uses these local copies instead of
# downloading, eliminating network access during the compile step.
#
# For fully hermetic builds, the mirror can be pre-populated and this
# script will use cached files.
#
# Usage: eval "$(scripts/setup-ort-mirror.sh <output_dir>)"
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEPS_FILE="$REPO_ROOT/third_party/onnxruntime/cmake/deps.txt"
MIRROR_DIR="${1:?output mirror dir}"

# Only these deps are needed for a minimal CPU-only build
NEEDED_DEPS="abseil_cpp|protobuf|date|eigen|flatbuffers|microsoft_gsl|mp11|json|pytorch_cpuinfo|re2|safeint|onnx"

mkdir -p "$MIRROR_DIR"

echo "Populating onnxruntime dependency mirror in $MIRROR_DIR..." >&2

while IFS=';' read -r NAME URL SHA1; do
    [ -z "$NAME" ] && continue
    case "$NAME" in \#*|cpp_client_telemetry) continue ;; esac
    case "$NAME" in protoc_win*|protoc_linux_*|protoc_mac_*) continue ;; esac

    # Only download deps we actually need
    if ! echo "$NAME" | grep -qE "^($NEEDED_DEPS)$"; then
        continue
    fi

    [[ "$URL" == https://* ]] || continue

    MIRROR_PATH="$MIRROR_DIR/${URL#https://}"
    mkdir -p "$(dirname "$MIRROR_PATH")"

    if [ -f "$MIRROR_PATH" ]; then
        echo "  cached: $NAME" >&2
        continue
    fi

    echo "  downloading: $NAME" >&2
    if ! curl -sL -o "$MIRROR_PATH" "$URL"; then
        echo "  WARNING: failed to download $NAME" >&2
        rm -f "$MIRROR_PATH"
        continue
    fi

    # Verify the SHA1 hash matches what onnxruntime expects
    ACTUAL_SHA1=$(sha1sum "$MIRROR_PATH" | awk '{print $1}')
    if [ "$ACTUAL_SHA1" != "$SHA1" ]; then
        echo "  WARNING: hash mismatch for $NAME (expected $SHA1, got $ACTUAL_SHA1)" >&2
    fi
done < "$DEPS_FILE"

echo "ORT_MIRROR_FLAGS=\"-Donnxruntime_CMAKE_DEPS_MIRROR_DIR=$MIRROR_DIR\""
