#!/usr/bin/env bash
# Set up onnxruntime's FetchContent dependencies from git submodules.
#
# Generates cmake -D flags that tell FetchContent to use local source
# directories (git submodules in third_party/onnxruntime-deps/) instead of
# downloading from GitHub. Also applies the patches that onnxruntime's build
# normally applies via FetchContent's PATCH_COMMAND.
#
# Usage: eval "$(scripts/setup-ort-deps.sh /path/to/onnxruntime)"
# Outputs: CMAKE_DEP_FLAGS="... (pass to cmake)"

set -euo pipefail

ORT_SRC="${1:-third_party/onnxruntime}"
DEPS_DIR="third_party/onnxruntime-deps"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ ! -f "$REPO_ROOT/$ORT_SRC/cmake/CMakeLists.txt" ]; then
    echo "ERROR: onnxruntime source not found at $REPO_ROOT/$ORT_SRC" >&2
    exit 1
fi

# Map: FetchContent name -> submodule directory name
# (FetchContent uses the name from FetchContent_Declare, uppercased for
# the FETCHCONTENT_SOURCE_DIR_<NAME> variable)
declare -A DEP_MAP=(
    [ABSEIL_CPP]="abseil-cpp"
    [PROTOBUF]="protobuf"
    [DATE]="date"
    [EIGEN]="eigen"
    [FLATBUFFERS]="flatbuffers"
    [GSL]="GSL"
    [NLOHMANN_JSON]="nlohmann_json"
    [PYTORCH_CPUINFO]="pytorch_cpuinfo"
    [RE2]="re2"
)

# Build the cmake flags
FLAGS=""
for name in "${!DEP_MAP[@]}"; do
    dir="$REPO_ROOT/$DEPS_DIR/${DEP_MAP[$name]}"
    if [ -d "$dir" ]; then
        FLAGS="$FLAGS -DFETCHCONTENT_SOURCE_DIR_${name}=$dir"
    else
        echo "WARNING: submodule $dir not found, FetchContent will download $name" >&2
    fi
done

# Apply patches that onnxruntime normally applies via FetchContent PATCH_COMMAND.
# These are in $ORT_SRC/cmake/patches/ and need to be applied to the
# corresponding submodule checkouts.
apply_patch() {
    local patch_file="$1" target_dir="$2" name="$3"
    if [ -f "$patch_file" ] && [ -d "$target_dir" ]; then
        if git -C "$target_dir" apply --check "$patch_file" 2>/dev/null; then
            git -C "$target_dir" apply "$patch_file"
            echo "  applied patch to $name" >&2
        else
            echo "  patch to $name already applied or not needed" >&2
        fi
    fi
}

echo "Applying onnxruntime patches to submodules..." >&2

PATCHES_DIR="$REPO_ROOT/$ORT_SRC/cmake/patches"
apply_patch "$PATCHES_DIR/date/date.patch" \
    "$REPO_ROOT/$DEPS_DIR/date" "date"
apply_patch "$PATCHES_DIR/gsl/1213.patch" \
    "$REPO_ROOT/$DEPS_DIR/GSL" "GSL"
apply_patch "$PATCHES_DIR/flatbuffers/flatbuffers.patch" \
    "$REPO_ROOT/$DEPS_DIR/flatbuffers" "flatbuffers"
apply_patch "$PATCHES_DIR/onnx/onnx.patch" \
    "$REPO_ROOT/$ORT_SRC/cmake/external/onnx" "onnx"

# cpuinfo patches are ARM64-specific; skip on x86_64
if [ "$(uname -m)" = "aarch64" ]; then
    apply_patch "$PATCHES_DIR/cpuinfo/enable_deinit_refcounting.patch" \
        "$REPO_ROOT/$DEPS_DIR/pytorch_cpuinfo" "pytorch_cpuinfo"
fi

echo "CMAKE_DEP_FLAGS=\"$FLAGS\""
