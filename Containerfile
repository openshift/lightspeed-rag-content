# Go BYOK tool image: markdown -> mpnet/ONNX -> FAISS -> docker-archive.
#
# Everything heavy comes from the repository: faiss v1.12.0 source and the
# onnxruntime release are vendored in third_party/, the model ships
# as gzip chunks in model/, and Go modules are vendored. The only
# network use at build time is the base images and (locally) the RPM
# toolchain for the faiss compile; Konflux hermetic builds prefetch those
# RPMs via cachi2 (see .tekton/lightspeed-rag-content-*.yaml).
ARG GO_TOOLSET=registry.access.redhat.com/ubi9/go-toolset:latest
ARG NATIVE_IMAGE=registry.access.redhat.com/ubi9/ubi:latest
ARG TOOL_IMAGE=registry.access.redhat.com/ubi9/ubi-micro@sha256:7325ffb45d8401b227033dc26c567e138c919731ed2f8119e921ddba71835f87
ARG OUTPUT_BASE_IMAGE=registry.access.redhat.com/ubi9/ubi-minimal@sha256:c2fcb1793e00a434470271be7f46eadc2462b39f8370e6a81c861c72fb8d38db

# Customer output image base, flattened into the baked base layer.
FROM ${OUTPUT_BASE_IMAGE} AS output-base

# ---------------------------------------------------------------------------
# Native stage: compile faiss from the vendored source (same v1.12.0 as the
# service's faiss-cpu, so serialized indexes stay byte-compatible), unpack
# the pinned onnxruntime release, and reassemble the ONNX model from chunks.
# ---------------------------------------------------------------------------
FROM ${NATIVE_IMAGE} AS native
USER root
RUN if [ -f /cachi2/cachi2.env ]; then . /cachi2/cachi2.env; fi && \
    dnf install -y --nodocs gcc gcc-c++ cmake make openblas-devel tar gzip && dnf clean all
WORKDIR /work
COPY third_party/ /work/
RUN tar xzf faiss-v1.12.0.tar.gz && mkdir build && cd build && \
    cmake ../faiss-1.12.0 -DFAISS_ENABLE_GPU=OFF -DFAISS_ENABLE_PYTHON=OFF \
      -DFAISS_ENABLE_C_API=ON -DBUILD_SHARED_LIBS=ON -DBUILD_TESTING=OFF \
      -DCMAKE_BUILD_TYPE=Release && \
    make -j"$(nproc)" faiss_c && \
    mkdir -p /out/faiss/lib /out/faiss/include-c-api /out/faiss/src \
             /out/onnxruntime/lib /out/onnxruntime/include /out/model && \
    cp /work/build/faiss/libfaiss.so /work/build/c_api/libfaiss_c.so /out/faiss/lib/ && \
    cp -r /work/faiss-1.12.0/c_api/. /out/faiss/include-c-api/ && \
    cp -r /work/faiss-1.12.0 /out/faiss/src && \
    for lib in libopenblas.so.0 libgfortran.so.5 libquadmath.so.0 libgomp.so.1 libstdc++.so.6; do \
        cp -L "/usr/lib64/$lib" /out/faiss/lib/; \
    done && \
    rm -rf /work/build /out/faiss/src/build

RUN tar xzf onnxruntime-linux-x64-1.31.0.tgz && \
    cp onnxruntime-linux-x64-1.31.0/lib/libonnxruntime.so.1* /out/onnxruntime/lib/ && \
    ln -sf libonnxruntime.so.1.31.0 /out/onnxruntime/lib/libonnxruntime.so && \
    cp -r onnxruntime-linux-x64-1.31.0/include /out/onnxruntime/

# reassemble + verify the model (chunks follow the embeddings_model precedent)
COPY model/ /work/model/
RUN cat /work/model/mpnet.onnx.gz.* | gunzip > /out/model/mpnet.onnx && \
    cd /out/model && sha256sum -c /work/model/mpnet.onnx.sha256 && \
    cp /work/model/tokenizer.json /work/model/cl100k_base.tiktoken \
       /work/model/sentence_bert_config.json /out/model/

# ---------------------------------------------------------------------------
# Builder: compile the cgo binary against the native stage; bake the
# deterministic output base layer (the flattened rootfs never lands in the
# runtime image).
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
