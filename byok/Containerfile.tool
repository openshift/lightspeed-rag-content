ARG BYOK_TOOL_IMAGE=quay.io/$USERNAME/tool:latest
ARG UBI_BASE_IMAGE=registry.access.redhat.com/ubi9/ubi:latest
ARG HERMETIC=false
FROM ${UBI_BASE_IMAGE}
ARG LOG_LEVEL=info
ARG OUT_IMAGE_TAG=byok-image
ARG VECTOR_DB_INDEX=vector_db_index
ARG BYOK_TOOL_IMAGE
ARG UBI_BASE_IMAGE
ARG HERMETIC
RUN dnf install -y buildah python3.11 python3.11-pip

USER 0
WORKDIR /workdir

COPY requirements.gpu.txt .
RUN pip3.11 install --no-cache-dir --no-deps -r requirements.gpu.txt

COPY embeddings_model ./embeddings_model
RUN cd embeddings_model; if [ "$HERMETIC" == "true" ] && [ ! -f embeddings_model/model.safetensors ]; then \
        cp /cachi2/output/deps/generic/model.safetensors model.safetensors; \
    elif [ ! -f embeddings_model/model.safetensors ]; then \
        curl -L -O https://huggingface.co/sentence-transformers/all-mpnet-base-v2/resolve/9a3225965996d404b775526de6dbfe85d3368642/model.safetensors; \
    fi
COPY byok/generate_embeddings_tool.py byok/Containerfile.output ./

ENV _BUILDAH_STARTED_IN_USERNS=""
ENV BUILDAH_ISOLATION=chroot
ENV OUT_IMAGE_TAG=$OUT_IMAGE_TAG
ENV BYOK_TOOL_IMAGE=$BYOK_TOOL_IMAGE
ENV UBI_BASE_IMAGE=$UBI_BASE_IMAGE
ENV LOG_LEVEL=$LOG_LEVEL
ENV VECTOR_DB_INDEX=$VECTOR_DB_INDEX
CMD buildah --log-level $LOG_LEVEL build --build-arg BYOK_TOOL_IMAGE=$BYOK_TOOL_IMAGE \
    --build-arg UBI_BASE_IMAGE=$UBI_BASE_IMAGE --env VECTOR_DB_INDEX=$VECTOR_DB_INDEX \
    -t $OUT_IMAGE_TAG -f Containerfile.output \
    -v /markdown:/markdown:Z . && rm -f /output/$OUT_IMAGE_TAG.tar && \
    buildah push $OUT_IMAGE_TAG docker-archive:/output/$OUT_IMAGE_TAG.tar
