#!/usr/bin/env bash
# Stage the native libraries needed to build/test byok-go (faiss + onnxruntime)
# and print the CGO environment to use. Cached in .byok-go-native/.
#
# Both faiss and onnxruntime are compiled from git submodules
# (third_party/faiss and third_party/onnxruntime + onnxruntime-deps/).
# Run `git submodule update --init --recursive` before this script.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STAGE="${BYOK_GO_NATIVE_DIR:-$REPO_ROOT/.byok-go-native}"

# The filesystem occasionally reports freshly staged files as ENOENT;
# re-check before deciding to rebuild (the rebuild is destructive).
faiss_staged() {
    [ -f "faiss/lib/libfaiss.so" ] && [ -f "faiss/lib/libfaiss_c.so" ]
}

ort_staged() {
    [ -f "onnxruntime/lib/libonnxruntime.so.1" ]
}

mkdir -p "$STAGE"
cd "$STAGE"

# --- faiss v1.12.0 (same version as the service's faiss-cpu) ---
FAISS_SRC="$REPO_ROOT/third_party/faiss"
if [ ! -d "$FAISS_SRC/c_api" ]; then
    echo "ERROR: faiss submodule not initialized at $FAISS_SRC" >&2
    echo "  run: git submodule update --init --recursive" >&2
    exit 1
fi

if ! faiss_staged; then sleep 2; fi
if ! faiss_staged; then sleep 5; fi
if ! faiss_staged; then
    rm -rf faiss build
    mkdir build && cd build
    cmake "$FAISS_SRC" \
        -DFAISS_ENABLE_GPU=OFF -DFAISS_ENABLE_PYTHON=OFF \
        -DFAISS_ENABLE_C_API=ON -DBUILD_SHARED_LIBS=ON \
        -DBUILD_TESTING=OFF -DCMAKE_BUILD_TYPE=Release
    make -j"$(nproc)" faiss_c
    cd "$STAGE"
    mkdir -p faiss/lib faiss/include-c-api faiss/src
    cp build/faiss/libfaiss.so build/c_api/libfaiss_c.so faiss/lib/
    # faiss runtime dependencies (openblas bundles the LAPACK symbols)
    for lib in libopenblas.so.0 libgfortran.so.5 libquadmath.so.0 libgomp.so.1 libstdc++.so.6; do
        cp -L "/usr/lib64/$lib" faiss/lib/ 2>/dev/null || true
    done
    cp -r "$FAISS_SRC/c_api/." faiss/include-c-api/
    cp -r "$FAISS_SRC/." faiss/src/
    rm -rf build
fi

# --- onnxruntime v1.31.0 (from git submodule, CPU only) ---
if ! ort_staged; then sleep 2; fi
if ! ort_staged; then
    ORT_SRC="$REPO_ROOT/third_party/onnxruntime"
    if [ ! -f "$ORT_SRC/cmake/CMakeLists.txt" ]; then
        echo "ERROR: onnxruntime submodule not initialized at $ORT_SRC" >&2
        echo "  run: git submodule update --init --recursive" >&2
        exit 1
    fi
    rm -rf onnxruntime ort-src-build
    mkdir -p onnxruntime/lib onnxruntime/include ort-src-build

    # Set up FetchContent source overrides from git submodules
    eval "$("$REPO_ROOT/scripts/setup-ort-deps.sh" "$ORT_SRC")"

    cd ort-src-build
    cmake "$ORT_SRC/cmake" \
        -DCMAKE_BUILD_TYPE=Release \
        -Donnxruntime_BUILD_SHARED_LIB=ON \
        -Donnxruntime_BUILD_UNIT_TESTS=OFF \
        -Donnxruntime_ENABLE_PYTHON=OFF \
        -Donnxruntime_ENABLE_TRAINING=OFF \
        -Donnxruntime_USE_CUDA=OFF \
        -DMLAS_COMPILER_SUPPORTS_AVXVNNI=FALSE \
        $CMAKE_DEP_FLAGS \
        >/dev/null
    make -j"$(nproc)" onnxruntime >/dev/null
    cd "$STAGE"
    cp ort-src-build/libonnxruntime.so* onnxruntime/lib/
    cp "$ORT_SRC"/include/onnxruntime/core/session/*.h onnxruntime/include/
    rm -rf ort-src-build
fi

FAISS_LIB="$STAGE/faiss/lib"
ORT_LIB="$STAGE/onnxruntime/lib"

# libfaiss.so keeps Fortran LAPACK symbols undefined (unreachable from
# IndexFlat); allow them at link time.
cat <<ENV
export CGO_ENABLED=1
export CGO_CFLAGS="-I$STAGE/faiss/include-c-api -I$STAGE/faiss/src -I$STAGE/onnxruntime/include"
export CGO_LDFLAGS="-L$FAISS_LIB -L$ORT_LIB -Wl,-rpath,$FAISS_LIB -Wl,-rpath,$ORT_LIB -Wl,--allow-shlib-undefined"
export LD_LIBRARY_PATH="$FAISS_LIB:$ORT_LIB\${LD_LIBRARY_PATH:+:\$LD_LIBRARY_PATH}"
ENV
echo "Native stage ready in $STAGE" >&2
