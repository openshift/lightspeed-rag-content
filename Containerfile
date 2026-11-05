# Go BYOK tool image: markdown -> mpnet/ONNX -> FAISS -> container image archive.
#
# Everything is built from source: faiss v1.12.0 and onnxruntime v1.31.0 are
# compiled from git submodules, the model ships as gzip chunks, and Go modules
# are vendored. onnxruntime's cmake FetchContent dependencies are also git
# submodules (third_party/onnxruntime-deps/), so the build needs zero network
# access beyond the base images and the RPM toolchain (which cachi2 prefetches).
ARG GO_TOOLSET=registry.access.redhat.com/ubi9/go-toolset:latest
ARG NATIVE_IMAGE=registry.access.redhat.com/ubi9/ubi:latest
ARG TOOL_IMAGE=registry.access.redhat.com/ubi9/ubi-micro@sha256:5be877a2a280ae36eb9ab80ca4efb28bbf77c57abbba38137cdc37a03b8465e6
ARG OUTPUT_BASE_IMAGE=registry.access.redhat.com/ubi9/ubi-minimal@sha256:6f3a78179e0b30b930a186e7f68a4af52e51bb82406c9653be10bddd624e40f5

# Customer output image base, flattened into the baked base layer.
FROM ${OUTPUT_BASE_IMAGE} AS output-base

# ---------------------------------------------------------------------------
# Native stage: compile faiss and onnxruntime from git submodules.
# ---------------------------------------------------------------------------
FROM ${NATIVE_IMAGE} AS native
USER root
RUN if [ -f /cachi2/cachi2.env ]; then . /cachi2/cachi2.env; fi && \
    dnf install -y --nodocs gcc gcc-c++ cmake make git gzip \
      perl libstdc++-static && \
    mkdir -p /out/static-libs && cp /usr/lib/gcc/*/*/libstdc++.a /out/static-libs/ && \
    dnf clean all
WORKDIR /work

# --- OpenBLAS v0.3.29, static only ---
# faiss's write_index dispatch references every index type, so BLAS/LAPACK
# symbols are link-required. No static OpenBLAS exists in the ubi9 repos;
# build it from the git submodule. C_LAPACK=1 uses the f2c-translated pure-C
# LAPACK, so no Fortran runtime is needed; USE_THREAD=0 builds the serial
# kernel (the tool only adds vectors and serializes, it never searches).
COPY third_party/openblas/ /work/third_party/openblas/
RUN cd /work/third_party/openblas && \
    make -j"$(nproc)" NO_SHARED=1 USE_THREAD=0 C_LAPACK=1 NOFORTRAN=1 \
      NUM_THREADS=1 && \
    mkdir -p /out/openblas/lib && \
    cp libopenblas_*.a /out/openblas/lib/libopenblas.a

# --- faiss v1.12.0 (same version as the service's faiss-cpu), static ---
# Static archives don't bake in their dependencies; the BLAS/LAPACK symbols
# stay undefined here and are resolved against the static OpenBLAS at the
# final go link. The BLAS/LAPACK cache variables point cmake at the static
# OpenBLAS built above, so no system BLAS is needed at configure time.
COPY third_party/faiss/ /work/faiss/
RUN mkdir faiss-build && cd faiss-build && \
    cmake /work/faiss \
      -DFAISS_ENABLE_GPU=OFF -DFAISS_ENABLE_PYTHON=OFF \
      -DFAISS_ENABLE_C_API=ON -DBUILD_SHARED_LIBS=OFF \
      -DBUILD_TESTING=OFF -DCMAKE_BUILD_TYPE=Release \
      -DBLA_STATIC=ON \
      -DBLAS_LIBRARIES=/out/openblas/lib/libopenblas.a \
      -DLAPACK_LIBRARIES=/out/openblas/lib/libopenblas.a && \
    make -j"$(nproc)" faiss_c && \
    mkdir -p /out/faiss/lib /out/faiss/include-c-api /out/faiss/src && \
    cp faiss/libfaiss.a c_api/libfaiss_c.a /out/faiss/lib/ && \
    cp -r /work/faiss/c_api/. /out/faiss/include-c-api/ && \
    cp -r /work/faiss /out/faiss/src

# --- onnxruntime v1.31.0 (from git submodule, CPU only) ---
# All FetchContent dependencies are git submodules in third_party/onnxruntime-deps/.
# cmake's FETCHCONTENT_SOURCE_DIR_<NAME> tells FetchContent to use local source
# directories instead of downloading. The extra include path is needed because
# protobuf's utf8_range headers live in a nested submodule.
COPY scripts/setup-ort-deps.sh /work/scripts/setup-ort-deps.sh
COPY third_party/onnxruntime/ /work/third_party/onnxruntime/
COPY third_party/onnxruntime-deps/ /work/third_party/onnxruntime-deps/
RUN chmod +x /work/scripts/setup-ort-deps.sh && \
    cd /work && eval "$(scripts/setup-ort-deps.sh third_party/onnxruntime)" && \
    mkdir -p /out/onnxruntime/lib /out/onnxruntime/include && \
    cd /work/third_party/onnxruntime/cmake && \
    rm -rf build && mkdir build && cd build && \
    cmake .. \
      -DCMAKE_BUILD_TYPE=Release \
      -Donnxruntime_BUILD_SHARED_LIB=OFF \
      -Donnxruntime_BUILD_UNIT_TESTS=OFF \
      -Donnxruntime_ENABLE_PYTHON=OFF \
      -Donnxruntime_ENABLE_TRAINING=OFF \
      -Donnxruntime_USE_CUDA=OFF \
      -DMLAS_COMPILER_SUPPORTS_AVXVNNI=FALSE \
      $CMAKE_DEP_FLAGS \
      -DCMAKE_CXX_FLAGS="-I/work/third_party/onnxruntime-deps/protobuf/third_party/utf8_range" && \
    make -j"$(nproc)" && \
    make re2 && \
    mkdir -p /out/onnxruntime/lib /out/onnxruntime/include && \
    cp /work/third_party/onnxruntime/include/onnxruntime/core/session/*.h /out/onnxruntime/include/ && \
    find . -name '*.a' -exec cp {} /out/onnxruntime/lib/ \; && \
    { echo CREATE /out/onnxruntime/lib/libonnxruntime.a; \
      for a in /out/onnxruntime/lib/libonnxruntime_*.a; do echo ADDLIB "$a"; done; \
      echo SAVE; echo END; } | ar -M && \
    rm -f /out/onnxruntime/lib/libonnxruntime_*.a


# --- model reassembly (chunks follow the embeddings_model precedent) ---
COPY model/ /work/model/
RUN mkdir -p /out/model && cat /work/model/mpnet.onnx.gz.* | gunzip > /out/model/mpnet.onnx && \
    cd /out/model && sha256sum -c /work/model/mpnet.onnx.sha256 && \
    cp /work/model/tokenizer.json /work/model/cl100k_base.tiktoken \
       /work/model/sentence_bert_config.json /out/model/

# --- third-party license files (surfaced in the image for SBOM/attribution) ---
RUN mkdir -p /out/licenses && \
    cp /work/faiss/LICENSE /out/licenses/faiss-LICENSE && \
    cp /work/third_party/openblas/LICENSE /out/licenses/openblas-LICENSE && \
    cp /work/third_party/onnxruntime/LICENSE /out/licenses/onnxruntime-LICENSE && \
    if [ -f /work/third_party/onnxruntime/cmake/external/onnx/LICENSE ]; then \
        cp /work/third_party/onnxruntime/cmake/external/onnx/LICENSE \
           /out/licenses/onnx-LICENSE; \
    fi && \
    for d in /work/third_party/onnxruntime-deps/*/; do \
        name="$(basename "$d")"; \
        for f in LICENSE LICENSE.txt LICENSE.md LICENSE.MIT \
                 COPYING COPYING.txt COPYRIGHT \
                 COPYING.APACHE COPYING.BSD COPYING.MINPACK COPYING.MPL2; do \
            if [ -f "$d/$f" ]; then \
                cp "$d/$f" "/out/licenses/onnxruntime-deps-$name-$f"; \
            fi; \
        done; \
    done && \
    cp /work/third_party/onnxruntime-deps/mp11/README.md \
       /out/licenses/onnxruntime-deps-mp11-README.md && \
    if [ -d /work/third_party/onnxruntime-deps/nlohmann_json/LICENSES ]; then \
        mkdir -p /out/licenses/nlohmann_json-LICENSES && \
        cp /work/third_party/onnxruntime-deps/nlohmann_json/LICENSES/*.txt \
           /out/licenses/nlohmann_json-LICENSES/; \
    fi

# ---------------------------------------------------------------------------
# Builder: compile the cgo binary against the native stage; bake the
# output base layer.
# ---------------------------------------------------------------------------
FROM ${GO_TOOLSET} AS builder
USER root
WORKDIR /src
COPY cmd/ /src/cmd/
COPY internal/ /src/internal/
COPY go.mod go.sum /src/
COPY vendor/ /src/vendor/
COPY --from=native /out/ /native/
# Static link: faiss + onnxruntime + deps + OpenBLAS are all archives, wrapped
# in --start-group for their cyclic dependencies; libstdc++/libgcc link
# statically too (-static-libgcc via -extldflags; -static-libstdc++ is
# dropped by cgo's flag filter, so -Wl,-Bstatic is used instead). The
# resulting binary depends only on glibc, which ubi9-micro provides.
# Build with Go's native FIPS 140-3 crypto provider. GOFIPS140=certified
# selects the certified FIPS module for the Go crypto packages (SHA-256
# chunk hashing, random IDs); CGO stays enabled for the non-crypto ML
# libraries (faiss, onnxruntime), which perform no cryptography. The binary
# defaults to fips140=on (see the //go:debug directive in cmd/byok-go/fips.go).
RUN if [ -f /cachi2/cachi2.env ]; then . /cachi2/cachi2.env; fi && \
    ORT_ARCHIVES="$(ls /native/onnxruntime/lib/*.a | grep -v libonnxruntime.a | tr '\n' ' ')" && \
    GOMP="$(ls /usr/lib/gcc/*/*/libgomp.a | head -1)" && \
    CGO_ENABLED=1 GOFIPS140=certified \
    CGO_CFLAGS="-I/native/faiss/include-c-api -I/native/faiss/src -I/native/onnxruntime/include" \
    CGO_LDFLAGS="-L/native/faiss/lib -L/native/onnxruntime/lib -Wl,--start-group $ORT_ARCHIVES /native/openblas/lib/libopenblas.a $GOMP -Wl,--end-group /native/static-libs/libstdc++.a -Wl,-Bstatic -lgcc -Wl,-Bdynamic -lm -lpthread -ldl" \
    go build -mod=vendor -ldflags "-extldflags -static-libgcc" -o /out/byok-go ./cmd/byok-go && chmod +x /out/byok-go
# Verify byok-go targets at most x86-64-v2 (no-op on non-amd64). The binary
# is gcc-linked, so the ELF GNU_PROPERTY_X86_ISA_1_NEEDED note is present and
# checked directly.
RUN go build -mod=vendor -o /check-isa-level ./cmd/check-isa-level && /check-isa-level /out/byok-go

COPY --from=output-base / /base-rootfs
RUN mkdir -p /out && tar --sort=name --mtime=@0 --numeric-owner --owner=0 --group=0 \
      -cf /out/base-layer.tar -C /base-rootfs . && rm -rf /base-rootfs

# ---------------------------------------------------------------------------
# Runtime: ubi9-micro, no Python, no package manager. The byok-go binary
# links the native libraries statically, so it needs nothing but glibc;
# the model ships in /opt/byok.
# ---------------------------------------------------------------------------
FROM ${TOOL_IMAGE}
ARG OUT_IMAGE_TAG=byok-image
ARG VECTOR_DB_INDEX=vector_db_index
USER 0
WORKDIR /workdir

COPY --from=native /out/model/ /opt/byok/
COPY --from=native /out/licenses/ /opt/byok/licenses/
COPY --from=builder /out/base-layer.tar /opt/byok/base-layer.tar
COPY --from=builder /out/byok-go /usr/local/bin/byok-go

ENV OUT_IMAGE_TAG=$OUT_IMAGE_TAG
ENV VECTOR_DB_INDEX=$VECTOR_DB_INDEX

CMD byok-go -i /markdown -o /output/$OUT_IMAGE_TAG.tar -tag "$OUT_IMAGE_TAG" \
    -id "$VECTOR_DB_INDEX" -model /opt/byok -base-layer /opt/byok/base-layer.tar
