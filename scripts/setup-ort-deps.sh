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
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Accept either a relative path from REPO_ROOT or an absolute path
if [[ "$ORT_SRC" = /* ]]; then
    ORT_PATH="$ORT_SRC"
else
    ORT_PATH="$REPO_ROOT/$ORT_SRC"
fi

# The deps directory is a sibling of the onnxruntime directory
DEPS_DIR="$(dirname "$ORT_PATH")/onnxruntime-deps"

if [ ! -f "$ORT_PATH/cmake/CMakeLists.txt" ]; then
    echo "ERROR: onnxruntime source not found at $ORT_PATH" >&2
    exit 1
fi

# Map: FetchContent name -> submodule directory name
# (FetchContent uses the name from FetchContent_Declare, uppercased for
# the FETCHCONTENT_SOURCE_DIR_<NAME> variable)
declare -A DEP_MAP=(
    [ABSEIL_CPP]="abseil-cpp"
    [EIGEN3]="eigen"
    [PROTOBUF]="protobuf"
    [DATE]="date"
    [EIGEN]="eigen"
    [FLATBUFFERS]="flatbuffers"
    [GSL]="GSL"
    [MP11]="mp11"
    [NLOHMANN_JSON]="nlohmann_json"
    [PYTORCH_CPUINFO]="pytorch_cpuinfo"
    [RE2]="re2"
    [SAFEINT]="safeint"
)

# Build the cmake flags
FLAGS=""
for name in "${!DEP_MAP[@]}"; do
    dir="$DEPS_DIR/${DEP_MAP[$name]}"
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

PATCHES_DIR="$ORT_PATH/cmake/patches"
apply_patch "$PATCHES_DIR/date/date.patch" \
    "$DEPS_DIR/date" "date"
apply_patch "$PATCHES_DIR/gsl/1213.patch" \
    "$DEPS_DIR/GSL" "GSL"
apply_patch "$PATCHES_DIR/flatbuffers/flatbuffers.patch" \
    "$DEPS_DIR/flatbuffers" "flatbuffers"
apply_patch "$PATCHES_DIR/onnx/onnx.patch" \
    "$ORT_PATH/cmake/external/onnx" "onnx"

# cpuinfo patches are ARM64-specific; skip on x86_64
if [ "$(uname -m)" = "aarch64" ]; then
    apply_patch "$PATCHES_DIR/cpuinfo/enable_deinit_refcounting.patch" \
        "$DEPS_DIR/pytorch_cpuinfo" "pytorch_cpuinfo"
fi

echo "CMAKE_DEP_FLAGS=\"$FLAGS\""
