#!/usr/bin/env bash
# Stage the native libraries needed to build/test byok-go (faiss + onnxruntime)
# and print the CGO environment to use. Cached in .byok-go-native/.
#
# faiss v1.12.0 is compiled from source (matches the service's faiss-cpu
# version, so serialized indexes are byte-compatible). onnxruntime is the
# official pinned release.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STAGE="${BYOK_GO_NATIVE_DIR:-$REPO_ROOT/.byok-go-native}"
FAISS_VERSION=1.12.0
ORT_VERSION=1.31.0
FAISS_SHA256=561376d1a44771bf1230fabeef9c81643468009b45a585382cf38d3a7a94990a
# shellcheck disable=SC2034
ORT_SHA256_IGNORED=not-checked-below

mkdir -p "$STAGE"
cd "$STAGE"

VENDORED_FAISS="$REPO_ROOT/byok-go/third_party/faiss-v${FAISS_VERSION}.tar.gz"
if [ ! -f "faiss-v${FAISS_VERSION}.tar.gz" ]; then
    if [ -f "$VENDORED_FAISS" ]; then
        cp "$VENDORED_FAISS" .
    else
        curl -sL -o "faiss-v${FAISS_VERSION}.tar.gz" \
            "https://github.com/facebookresearch/faiss/archive/refs/tags/v${FAISS_VERSION}.tar.gz"
    fi
    echo "$FAISS_SHA256  faiss-v${FAISS_VERSION}.tar.gz" | sha256sum -c -
fi

# The filesystem occasionally reports freshly staged files as ENOENT;
# re-check before deciding to rebuild (the rebuild is destructive).
faiss_staged() {
    [ -f "faiss/lib/libfaiss.so" ] && [ -f "faiss/lib/libfaiss_c.so" ]
}
if ! faiss_staged; then sleep 2; fi
if ! faiss_staged; then sleep 5; fi
if ! faiss_staged; then
    rm -rf "faiss-${FAISS_VERSION}" faiss build
    tar xzf "faiss-v${FAISS_VERSION}.tar.gz"
    mkdir build && cd build
    cmake "../faiss-${FAISS_VERSION}" \
        -DFAISS_ENABLE_GPU=OFF -DFAISS_ENABLE_PYTHON=OFF \
        -DFAISS_ENABLE_C_API=ON -DBUILD_SHARED_LIBS=ON \
        -DBUILD_TESTING=OFF -DCMAKE_BUILD_TYPE=Release
    make -j"$(nproc)" faiss_c
    cd "$STAGE"
    mkdir -p faiss/lib
    cp build/faiss/libfaiss.so build/c_api/libfaiss_c.so faiss/lib/
    # faiss runtime dependencies (openblas bundles the LAPACK symbols)
    for lib in libopenblas.so.0 libgfortran.so.5 libquadmath.so.0 libgomp.so.1 libstdc++.so.6; do
        cp -L "/usr/lib64/$lib" faiss/lib/ 2>/dev/null || true
    done
    cp -r "faiss-${FAISS_VERSION}/c_api" faiss/include-c-api
    cp -r "faiss-${FAISS_VERSION}" faiss/src
    rm -rf build
fi

if [ ! -f "onnxruntime/lib/libonnxruntime.so.1" ]; then
    VENDORED_ORT="$REPO_ROOT/byok-go/third_party/onnxruntime-linux-x64-${ORT_VERSION}.tgz"
    if [ -f "$VENDORED_ORT" ]; then
        cp "$VENDORED_ORT" ort.tgz
    else
        curl -sL -o "ort.tgz" \
            "https://github.com/microsoft/onnxruntime/releases/download/v${ORT_VERSION}/onnxruntime-linux-x64-${ORT_VERSION}.tgz"
    fi
    rm -rf "onnxruntime-linux-x64-${ORT_VERSION}" onnxruntime
    tar xzf ort.tgz
    mkdir -p onnxruntime/lib
    cp "onnxruntime-linux-x64-${ORT_VERSION}"/lib/libonnxruntime.so.1* onnxruntime/lib/
    ln -sf "libonnxruntime.so.1.${ORT_VERSION#1.}" onnxruntime/lib/libonnxruntime.so
    cp -r "onnxruntime-linux-x64-${ORT_VERSION}"/include onnxruntime/include
    rm -rf "onnxruntime-linux-x64-${ORT_VERSION}" ort.tgz
fi

FAISS_LIB="$STAGE/faiss/lib"
ORT_LIB="$STAGE/onnxruntime/lib"

cat <<ENV
export CGO_ENABLED=1
export CGO_CFLAGS="-I$STAGE/faiss/include-c-api -I$STAGE/faiss/src -I$STAGE/onnxruntime/include"
# libfaiss.so keeps Fortran LAPACK symbols undefined (unreachable from
# IndexFlat); allow them at link time.
export CGO_LDFLAGS="-L$FAISS_LIB -L$ORT_LIB -Wl,-rpath,$FAISS_LIB -Wl,-rpath,$ORT_LIB -Wl,--allow-shlib-undefined"
export LD_LIBRARY_PATH="$FAISS_LIB:$ORT_LIB\${LD_LIBRARY_PATH:+:\$LD_LIBRARY_PATH}"
ENV
echo "Native stage ready in $STAGE" >&2
