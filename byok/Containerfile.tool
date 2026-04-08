ARG BYOK_TOOL_IMAGE=registry.redhat.io/openshift-lightspeed-tech-preview/lightspeed-rag-tool-rhel9:latest
ARG UBI_BASE_IMAGE=registry.access.redhat.com/ubi9/ubi:latest
ARG HERMETIC=false
FROM ${UBI_BASE_IMAGE}
ARG LOG_LEVEL=info
ARG OUT_IMAGE_TAG=byok-image
ARG VECTOR_DB_INDEX=vector_db_index
ARG BYOK_TOOL_IMAGE
ARG UBI_BASE_IMAGE
ARG HERMETIC
ARG LLAMA_STACK
RUN dnf install -y buildah python3.12 python3.12-pip && dnf clean all

USER 0
WORKDIR /workdir

COPY byok/requirements.txt .
RUN pip3.12 install --upgrade pip && pip3.12 install --no-cache-dir --no-deps -r requirements.txt

COPY embeddings_model ./embeddings_model
ENV HERMETIC=$HERMETIC
RUN cd embeddings_model; \
    if [ ! -f embeddings_model/model.safetensors ]; then \
        if [ "$HERMETIC" == "true" ]; then \
            cp /cachi2/output/deps/generic/model.safetensors model.safetensors; \
        else \
            curl -L -O https://huggingface.co/sentence-transformers/all-mpnet-base-v2/resolve/9a3225965996d404b775526de6dbfe85d3368642/model.safetensors; \
        fi \
    fi
COPY byok/generate_embeddings_tool.py byok/__init__.py byok/document_processor.py byok/metadata_processor.py byok/Containerfile.output ./

# this directory is checked by ecosystem-cert-preflight-checks task in Konflux
RUN mkdir /licenses
COPY LICENSE /licenses/

# Labels for enterprise contract
LABEL com.redhat.component=openshift-lightspeed-rag-content
LABEL cpe="cpe:/a:redhat:openshift_lightspeed:1::el9"
LABEL description="Red Hat OpenShift Lightspeed BYO Knowledge Tools"
LABEL distribution-scope=private
LABEL io.k8s.description="Red Hat OpenShift Lightspeed BYO Knowledge Tools"
LABEL io.k8s.display-name="OpenShift Lightspeed BYO Knowledge Tools"
LABEL io.openshift.tags="openshift,lightspeed,ai,assistant,rag"
LABEL name="openshift-lightspeed-tech-preview/lightspeed-rag-tool-rhel9"
LABEL release=0.0.1
LABEL url="https://github.com/openshift/lightspeed-rag-content"
LABEL vendor="Red Hat, Inc."
LABEL version=0.0.1
LABEL summary="Red Hat OpenShift Lightspeed BYO Knowledge Tools"
LABEL konflux.additional-tags="latest"

ENV _BUILDAH_STARTED_IN_USERNS=""
ENV BUILDAH_ISOLATION=chroot
ENV OUT_IMAGE_TAG=$OUT_IMAGE_TAG
ENV BYOK_TOOL_IMAGE=$BYOK_TOOL_IMAGE
ENV UBI_BASE_IMAGE=$UBI_BASE_IMAGE
ENV LOG_LEVEL=$LOG_LEVEL
ENV VECTOR_DB_INDEX=$VECTOR_DB_INDEX
ENV LLAMA_STACK=$LLAMA_STACK
CMD buildah --log-level $LOG_LEVEL build --build-arg BYOK_TOOL_IMAGE=$BYOK_TOOL_IMAGE \
    --build-arg UBI_BASE_IMAGE=$UBI_BASE_IMAGE --env VECTOR_DB_INDEX=$VECTOR_DB_INDEX \
    --env LLAMA_STACK=$LLAMA_STACK \
    -t $OUT_IMAGE_TAG -f Containerfile.output \
    -v /markdown:/markdown:Z . && rm -f /output/$OUT_IMAGE_TAG.tar && \
    buildah push $OUT_IMAGE_TAG docker-archive:/output/$OUT_IMAGE_TAG.tar
