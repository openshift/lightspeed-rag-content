# Go BYOK tool image: markdown -> mpnet/ONNX -> FAISS -> docker-archive.
#
# Everything is built from source: faiss v1.12.0 and onnxruntime v1.31.0 are
# compiled from git submodules, the model ships as gzip chunks, and Go modules
# are vendored. onnxruntime's cmake FetchContent dependencies are also git
# submodules (third_party/onnxruntime-deps/), so the build needs zero network
# access beyond the base images and the RPM toolchain (which cachi2 prefetches).
ARG GO_TOOLSET=registry.access.redhat.com/ubi9/go-toolset:latest
ARG NATIVE_IMAGE=registry.access.redhat.com/ubi9/ubi:latest
ARG TOOL_IMAGE=registry.access.redhat.com/ubi9/ubi-micro@sha256:7325ffb45d8401b227033dc26c567e138c919731ed2f8119e921ddba71835f87
ARG OUTPUT_BASE_IMAGE=registry.access.redhat.com/ubi9/ubi-minimal@sha256:c2fcb1793e00a434470271be7f46eadc2462b39f8370e6a81c861c72fb8d38db

# Customer output image base, flattened into the baked base layer.
FROM ${OUTPUT_BASE_IMAGE} AS output-base

# ---------------------------------------------------------------------------
# Native stage: compile faiss and onnxruntime from git submodules.
# ---------------------------------------------------------------------------
FROM ${NATIVE_IMAGE} AS native
USER root
RUN if [ -f /cachi2/cachi2.env ]; then . /cachi2/cachi2.env; fi && \
    dnf install -y --nodocs gcc gcc-c++ cmake make openblas-devel tar gzip \
      python3.12 git patch && \
    alternatives --set python3 /usr/bin/python3.12 2>/dev/null || true && \
    dnf clean all
WORKDIR /work

# --- faiss v1.12.0 (same version as the service's faiss-cpu) ---
COPY third_party/faiss/ /work/faiss/
RUN mkdir faiss-build && cd faiss-build && \
    cmake /work/faiss \
      -DFAISS_ENABLE_GPU=OFF -DFAISS_ENABLE_PYTHON=OFF \
      -DFAISS_ENABLE_C_API=ON -DBUILD_SHARED_LIBS=ON \
      -DBUILD_TESTING=OFF -DCMAKE_BUILD_TYPE=Release && \
    make -j"$(nproc)" faiss_c && \
    mkdir -p /out/faiss/lib /out/faiss/include-c-api /out/faiss/src && \
    cp /work/faiss-build/faiss/libfaiss.so /work/faiss-build/c_api/libfaiss_c.so /out/faiss/lib/ && \
    cp -r /work/faiss/c_api/. /out/faiss/include-c-api/ && \
    cp -r /work/faiss /out/faiss/src && \
    for lib in libopenblas.so.0 libgfortran.so.5 libquadmath.so.0 \
               libgomp.so.1 libstdc++.so.6; do \
        cp -L "/usr/lib64/$lib" /out/faiss/lib/ 2>/dev/null || true; \
    done

# --- onnxruntime v1.31.0 (from git submodule, CPU only) ---
# The FetchContent dependencies are also git submodules, so the build
# needs zero network access for source code.
COPY scripts/setup-ort-deps.sh /work/setup-ort-deps.sh
COPY third_party/onnxruntime/ /work/onnxruntime/
COPY third_party/onnxruntime-deps/ /work/onnxruntime-deps/

RUN chmod +x /work/setup-ort-deps.sh && \
    cd /work && eval "$(/work/setup-ort-deps.sh /work/onnxruntime)" && \
    mkdir -p /out/onnxruntime/lib /out/onnxruntime/include && \
    cd /work/onnxruntime/cmake && mkdir build && cd build && \
    cmake .. \
      -DCMAKE_BUILD_TYPE=Release \
      -Donnxruntime_BUILD_SHARED_LIB=ON \
      -Donnxruntime_BUILD_UNIT_TESTS=OFF \
      -Donnxruntime_ENABLE_PYTHON=OFF \
      -Donnxruntime_ENABLE_TRAINING=OFF \
      -Donnxruntime_USE_CUDA=OFF \
      -DMLAS_COMPILER_SUPPORTS_AVXVNNI=FALSE \
      $CMAKE_DEP_FLAGS && \
    make -j"$(nproc)" onnxruntime && \
    cp libonnxruntime.so* /out/onnxruntime/lib/ && \
    cp /work/onnxruntime/include/onnxruntime/core/session/*.h /out/onnxruntime/include/

# --- model reassembly (chunks follow the embeddings_model precedent) ---
COPY model/ /work/model/
RUN mkdir -p /out/model && cat /work/model/mpnet.onnx.gz.* | gunzip > /out/model/mpnet.onnx && \
    cd /out/model && sha256sum -c /work/model/mpnet.onnx.sha256 && \
    cp /work/model/tokenizer.json /work/model/cl100k_base.tiktoken \
       /work/model/sentence_bert_config.json /out/model/

# ---------------------------------------------------------------------------
# Builder: compile the cgo binary against the native stage; bake the
# deterministic output base layer.
# ---------------------------------------------------------------------------
FROM ${GO_TOOLSET} AS builder
USER root
WORKDIR /src
COPY cmd/ /src/cmd/
COPY internal/ /src/internal/
COPY go.mod go.sum /src/
COPY vendor/ /src/vendor/
COPY --from=native /out/ /native/
RUN if [ -f /cachi2/cachi2.env ]; then . /cachi2/cachi2.env; fi && \
    CGO_ENABLED=1 \
    CGO_CFLAGS="-I/native/faiss/include-c-api -I/native/faiss/src -I/native/onnxruntime/include" \
    CGO_LDFLAGS="-L/native/faiss/lib -L/native/onnxruntime/lib -Wl,-rpath,/opt/byok/libs -Wl,--allow-shlib-undefined" \
    go build -mod=vendor -o /out/byok-go ./cmd/byok-go && chmod +x /out/byok-go

COPY --from=output-base / /base-rootfs
RUN mkdir -p /out && tar --sort=name --mtime=@0 --numeric-owner --owner=0 --group=0 \
      -cf /out/base-layer.tar -C /base-rootfs . && rm -rf /base-rootfs

# ---------------------------------------------------------------------------
# Runtime: ubi9-micro, no Python, no package manager; native runtime
# libraries ship in /opt/byok/libs and the model in /opt/byok.
# ---------------------------------------------------------------------------
FROM ${TOOL_IMAGE}
ARG OUT_IMAGE_TAG=byok-image
ARG VECTOR_DB_INDEX=vector_db_index
USER 0
WORKDIR /workdir

COPY --from=native /out/faiss/lib/ /opt/byok/libs/
COPY --from=native /out/onnxruntime/lib/ /opt/byok/libs/
COPY --from=native /out/model/ /opt/byok/
COPY --from=builder /out/base-layer.tar /opt/byok/base-layer.tar
COPY --from=builder /out/byok-go /usr/local/bin/byok-go

ENV LD_LIBRARY_PATH=/opt/byok/libs
ENV OUT_IMAGE_TAG=$OUT_IMAGE_TAG
ENV VECTOR_DB_INDEX=$VECTOR_DB_INDEX

CMD byok-go -i /markdown -o /output/$OUT_IMAGE_TAG.tar -tag "$OUT_IMAGE_TAG" \
    -id "$VECTOR_DB_INDEX" -model /opt/byok -base-layer /opt/byok/base-layer.tar
