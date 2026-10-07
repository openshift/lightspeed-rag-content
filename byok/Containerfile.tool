ARG BYOK_TOOL_IMAGE=registry.redhat.io/openshift-lightspeed-tech-preview/lightspeed-rag-tool-rhel9:latest
ARG UBI_BASE_IMAGE=quay.io/aipcc/base-images/cpu:3.5.2-1790703656
ARG HERMETIC=false
FROM ${UBI_BASE_IMAGE}
ARG LOG_LEVEL=info
ARG OUT_IMAGE_TAG=byok-image
ARG VECTOR_DB_INDEX=vector_db_index
ARG BYOK_TOOL_IMAGE
ARG UBI_BASE_IMAGE
ARG HERMETIC
USER 0
RUN dnf install -y buildah python3.12-pip && dnf update -y --nodocs && dnf clean all

WORKDIR /workdir

# CPU lockfiles generated from profiles.toml (see scripts/konflux_resolve.py)
COPY \
    requirements.hashes.wheel.txt \
    requirements.hashes.source.txt \
    requirements-build.txt \
    requirements.hermetic.txt \
    pyproject.toml \
    LICENSE \
    /workdir/

# The RHOAI image runs /opt/app-root/bin/python3.12 (VIRTUAL_ENV=/opt/app-root).
# Install into that interpreter in both hermetic and local builds; system Python's
# /usr/local site-packages are not visible to the runtime interpreter.
# cachi2.env sets PIP_FIND_LINKS so the upgrade resolves from the prefetch cache.
RUN /opt/app-root/bin/python3.12 -m pip install --upgrade pip && \
    if [ -f /cachi2/cachi2.env ]; then \
        . /cachi2/cachi2.env && \
        /opt/app-root/bin/python3.12 -m pip install --no-cache-dir --no-deps --ignore-installed \
            --no-index --find-links "${PIP_FIND_LINKS}" \
            -r requirements.hashes.wheel.txt \
            -r requirements.hashes.source.txt; \
    else \
        /opt/app-root/bin/python3.12 -m pip install --no-cache-dir --no-deps \
            -r requirements.hashes.wheel.txt && \
        /opt/app-root/bin/python3.12 -m pip install --no-cache-dir --no-deps \
            -r requirements.hashes.source.txt; \
    fi
RUN ln -sf "$(/opt/app-root/bin/python3.12 -c 'from pathlib import Path; import llama_index.core; print(Path(llama_index.core.__file__).parent / "_static/nltk_cache")')" /root/nltk_data

COPY embeddings_model ./embeddings_model
RUN cat embeddings_model/model.safetensors.tar.gz.* | \
      tar xzf - --no-same-owner -C embeddings_model || \
      { echo "ERROR: failed to extract model.safetensors from chunks"; exit 1; } && \
    rm -f embeddings_model/model.safetensors.tar.gz.* && \
    /opt/app-root/bin/python3.12 -c \
      "import safetensors; safetensors.safe_open('embeddings_model/model.safetensors', framework='pt'); print('OK: model.safetensors')" || \
    { echo "ERROR: corrupt safetensors file"; exit 1; }
COPY byok/generate_embeddings_tool.py byok/Containerfile.output byok/smoke_tool.py ./
# Run the real embedding CLI with the image's default Python, not system Python.
# This gates both PR and release builds on successful imports and FAISS persistence.
RUN python3.12 smoke_tool.py

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
