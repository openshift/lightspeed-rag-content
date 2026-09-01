ARG BYOK_TOOL_IMAGE=registry.redhat.io/openshift-lightspeed-tech-preview/lightspeed-rag-tool-rhel9:latest
ARG UBI_BASE_IMAGE=quay.io/aipcc/base-images/cpu:3.5
ARG HERMETIC=false
FROM ${UBI_BASE_IMAGE}
ARG LOG_LEVEL=info
ARG OUT_IMAGE_TAG=byok-image
ARG VECTOR_DB_INDEX=vector_db_index
ARG BYOK_TOOL_IMAGE
ARG UBI_BASE_IMAGE
ARG HERMETIC
USER 0
RUN dnf install -y buildah python3.12 python3.12-pip && dnf clean all

WORKDIR /workdir

# Same CPU lockfiles as the lightspeed-rag-tool image (repo root; see scripts/konflux_requirements.sh)
COPY \
    requirements.hashes.wheel.cpu.txt \
    requirements.hashes.source.cpu.txt \
    requirements-build.cpu.txt \
    requirements.hermetic.txt \
    pyproject.toml \
    LICENSE \
    /workdir/

# Upgrade pip first (pip==25.3 is prefetched in requirements.hermetic.txt).
# cachi2.env sets PIP_FIND_LINKS so the upgrade resolves from the prefetch cache in hermetic builds.
RUN /usr/bin/python3.12 -m pip install --upgrade pip && \
    if [ -f /cachi2/cachi2.env ]; then \
        . /cachi2/cachi2.env && \
        /usr/bin/python3.12 -m pip install --no-cache-dir --no-deps --ignore-installed \
            --no-index --find-links "${PIP_FIND_LINKS}" \
            -r requirements.hashes.wheel.cpu.txt \
            -r requirements.hashes.source.cpu.txt; \
    else \
        /usr/bin/python3.12 -m pip install --no-cache-dir -e ".[cpu]"; \
    fi
RUN ln -sf "/usr/local/lib/python3.12/site-packages/llama_index/core/_static/nltk_cache" /root/nltk_data

COPY embeddings_model ./embeddings_model
RUN cat embeddings_model/model.safetensors.tar.gz.* | \
      tar xzf - --no-same-owner -C embeddings_model || \
      { echo "ERROR: failed to extract model.safetensors from chunks"; exit 1; } && \
    rm -f embeddings_model/model.safetensors.tar.gz.* && \
    /usr/bin/python3.12 -c \
      "import safetensors; safetensors.safe_open('embeddings_model/model.safetensors', framework='pt'); print('OK: model.safetensors')" || \
    { echo "ERROR: corrupt safetensors file"; exit 1; }
COPY byok/generate_embeddings_tool.py byok/Containerfile.output ./

# this directory is checked by ecosystem-cert-preflight-checks task in Konflux
RUN mkdir /licenses
COPY LICENSE /licenses/

# Labels for enterprise contract
LABEL com.redhat.component=openshift-lightspeed-rag-content
LABEL cpe="cpe:/a:redhat:openshift_lightspeed:1::el9"
LABEL description="Red Hat OpenShift Lightspeed BYO Knowledge Tools"
LABEL distribution-scope=private
LABEL io.k8s.description="Red Hat OpenShift Lightspeed BYO Knowledge Tools"
LABEL io.k8s.display-name="Openshift Lightspeed BYO Knowledge Tools"
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
CMD buildah --log-level $LOG_LEVEL build --build-arg BYOK_TOOL_IMAGE=$BYOK_TOOL_IMAGE \
    --build-arg UBI_BASE_IMAGE=$UBI_BASE_IMAGE --env VECTOR_DB_INDEX=$VECTOR_DB_INDEX \
    -t $OUT_IMAGE_TAG -f Containerfile.output \
    -v /markdown:/markdown:Z . && rm -f /output/$OUT_IMAGE_TAG.tar && \
    buildah push $OUT_IMAGE_TAG docker-archive:/output/$OUT_IMAGE_TAG.tar
