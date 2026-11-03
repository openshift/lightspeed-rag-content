#!/usr/bin/env bash
# Stage the native libraries needed to build/test byok-go (faiss + onnxruntime
# + OpenBLAS, all STATIC) and print the CGO environment to use. Cached in
# .byok-go-native/.
#
# The resulting byok-go binary links the native libraries statically and
# depends only on glibc — no LD_LIBRARY_PATH, no shipped .so files. This
# mirrors the Containerfile's native and builder stages.
#
# All sources are git submodules (third_party/faiss, third_party/onnxruntime
# + onnxruntime-deps/, third_party/openblas).
# Run `git submodule update --init --recursive` before this script.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STAGE="${BYOK_GO_NATIVE_DIR:-$REPO_ROOT/.byok-go-native}"

faiss_staged() {
    [ -f "faiss/lib/libfaiss.a" ] && [ -f "faiss/lib/libfaiss_c.a" ]
}

openblas_staged() {
    [ -f "openblas/lib/libopenblas.a" ]
}

ort_staged() {
    [ -f "onnxruntime/lib/libonnxruntime.a" ]
}

mkdir -p "$STAGE"
cd "$STAGE"

# --- OpenBLAS v0.3.29, static, pure C (C_LAPACK avoids the Fortran runtime) ---
if ! openblas_staged; then sleep 2; fi
if ! openblas_staged; then
    OPENBLAS_SRC="$REPO_ROOT/third_party/openblas"
    if [ ! -f "$OPENBLAS_SRC/Makefile" ]; then
        echo "ERROR: openblas submodule not initialized at $OPENBLAS_SRC" >&2
        echo "  run: git submodule update --init --recursive" >&2
        exit 1
    fi
    rm -rf openblas
    cp -r "$OPENBLAS_SRC" openblas-src
    cd openblas-src
    make -j"$(nproc)" NO_SHARED=1 USE_THREAD=0 C_LAPACK=1 NOFORTRAN=1 \
        > "$STAGE/openblas-build.log" 2>&1
    cd "$STAGE"
    mkdir -p openblas/lib
    cp openblas-src/libopenblas_*.a openblas/lib/libopenblas.a
    rm -rf openblas-src
fi

# --- faiss v1.12.0 (same version as the service's faiss-cpu), static ---
FAISS_SRC="$REPO_ROOT/third_party/faiss"
if [ ! -d "$FAISS_SRC/c_api" ]; then
    echo "ERROR: faiss submodule not initialized at $FAISS_SRC" >&2
    echo "  run: git submodule update --init --recursive" >&2
    exit 1
fi

if ! faiss_staged; then sleep 2; fi
if ! faiss_staged; then
    rm -rf faiss build
    mkdir build && cd build
    cmake "$FAISS_SRC" \
        -DFAISS_ENABLE_GPU=OFF -DFAISS_ENABLE_PYTHON=OFF \
        -DFAISS_ENABLE_C_API=ON -DBUILD_SHARED_LIBS=OFF \
        -DBUILD_TESTING=OFF -DCMAKE_BUILD_TYPE=Release \
        -DBLA_STATIC=ON \
        -DBLAS_LIBRARIES="$STAGE/openblas/lib/libopenblas.a" \
        -DLAPACK_LIBRARIES="$STAGE/openblas/lib/libopenblas.a" \
        > "$STAGE/faiss-configure.log" 2>&1
    make -j"$(nproc)" faiss_c > "$STAGE/faiss-build.log" 2>&1
    cd "$STAGE"
    mkdir -p faiss/lib faiss/include-c-api faiss/src
    cp build/faiss/libfaiss.a build/c_api/libfaiss_c.a faiss/lib/
    cp -r "$FAISS_SRC/c_api/." faiss/include-c-api/
    cp -r "$FAISS_SRC/." faiss/src/
    rm -rf build
fi

# --- onnxruntime v1.31.0 (from git submodule, CPU only), static ---
if ! ort_staged; then sleep 2; fi
if ! ort_staged; then
    ORT_SRC="$REPO_ROOT/third_party/onnxruntime"
    if [ ! -f "$ORT_SRC/cmake/CMakeLists.txt" ]; then
        echo "ERROR: onnxruntime submodule not initialized at $ORT_SRC" >&2
        exit 1
    fi
    rm -rf onnxruntime ort-src-build
    mkdir -p onnxruntime/lib onnxruntime/include ort-src-build

    # Set up FetchContent source overrides from git submodules
    eval "$("$REPO_ROOT/scripts/setup-ort-deps.sh" "$ORT_SRC")"

    cd ort-src-build
    cmake "$ORT_SRC/cmake" \
        -DCMAKE_BUILD_TYPE=Release \
        -Donnxruntime_BUILD_SHARED_LIB=OFF \
        -Donnxruntime_BUILD_UNIT_TESTS=OFF \
        -Donnxruntime_ENABLE_PYTHON=OFF \
        -Donnxruntime_ENABLE_TRAINING=OFF \
        -Donnxruntime_USE_CUDA=OFF \
        -DMLAS_COMPILER_SUPPORTS_AVXVNNI=FALSE \
        $CMAKE_DEP_FLAGS \
        -DCMAKE_CXX_FLAGS="-I$REPO_ROOT/third_party/onnxruntime-deps/protobuf/third_party/utf8_range" \
        > "$STAGE/ort-configure.log" 2>&1
    # Static builds make `onnxruntime` an INTERFACE target over component
    # static libraries, so there is no single target: build everything
    # (tests are off), plus re2 which the default target skips.
    make -j"$(nproc)" > "$STAGE/ort-build.log" 2>&1
    make re2 >> "$STAGE/ort-build.log" 2>&1
    cd "$STAGE"
    # Merge the onnxruntime component archives into one libonnxruntime.a so
    # cgo's -lonnxruntime resolves; keep dependency archives separate.
    find ort-src-build -maxdepth 1 -name 'libonnxruntime_*.a' -exec cp {} onnxruntime/lib/ \;
    find ort-src-build -name '*.a' -not -name 'libonnxruntime_*' -exec cp {} onnxruntime/lib/ \;
    ls onnxruntime/lib/libonnxruntime_*.a >/dev/null || {
        echo "ERROR: no libonnxruntime_*.a found; see $STAGE/ort-build.log" >&2; exit 1; }
    {
        echo CREATE onnxruntime/lib/libonnxruntime.a
        for a in onnxruntime/lib/libonnxruntime_*.a; do
            echo ADDLIB "$a"
        done
        echo SAVE
        echo END
    } | ar -M
    rm -f onnxruntime/lib/libonnxruntime_*.a
    cp "$ORT_SRC"/include/onnxruntime/core/session/*.h onnxruntime/include/
    rm -rf ort-src-build
fi

FAISS_LIB="$STAGE/faiss/lib"
ORT_LIB="$STAGE/onnxruntime/lib"
ARCHIVES="$(ls "$ORT_LIB"/*.a | grep -v libonnxruntime.a | tr '\n' ' ')"

# Static link: all archives in --start-group (cyclic deps between them),
# then the C++ runtime. -static-libgcc goes through go build's -extldflags
# (cgo's flag filter drops -static-libstdc++, hence the explicit .a path).
STDXXA="$(ls /usr/lib64/libstdc++.a 2>/dev/null || echo /usr/lib/gcc/*/*/libstdc++.a)"

cat <<ENV
export CGO_ENABLED=1
export CGO_CFLAGS="-I$STAGE/faiss/include-c-api -I$STAGE/faiss/src -I$STAGE/onnxruntime/include"
export CGO_LDFLAGS="-L$FAISS_LIB -L$ORT_LIB -Wl,--start-group $ARCHIVES $STAGE/openblas/lib/libopenblas.a -Wl,--end-group $STDXXA -Wl,-Bstatic -lgcc -Wl,-Bdynamic -lm -lpthread -ldl"
export GO_BUILD_LDFLAGS="-extldflags -static-libgcc"
ENV
echo "Static native stage ready in $STAGE" >&2
echo "Build with: go build -ldflags \"\$GO_BUILD_LDFLAGS\" ..." >&2
