ARG EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2
ARG HERMETIC=false

FROM registry.access.redhat.com/ubi9/python-312 as lightspeed-rag-builder
ARG EMBEDDING_MODEL
ARG HERMETIC

USER 0
WORKDIR /workdir

# Konflux hermetic: Cachi2 vendor layout (PIP_FIND_LINKS) + hashed split lockfiles
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
RUN ln -s "/usr/local/lib/python3.12/site-packages/llama_index/core/_static/nltk_cache" /root/nltk_data

COPY ocp-product-docs-plaintext ./ocp-product-docs-plaintext
COPY runbooks ./runbooks

COPY embeddings_model ./embeddings_model
RUN cat embeddings_model/model.safetensors.tar.gz.* | \
      tar xzf - --no-same-owner -C embeddings_model || \
      { echo "ERROR: failed to extract model.safetensors from chunks"; exit 1; } && \
    rm -f embeddings_model/model.safetensors.tar.gz.* && \
    /usr/bin/python3.12 -c \
      "import safetensors; safetensors.safe_open('embeddings_model/model.safetensors', framework='pt'); print('OK: model.safetensors')" || \
    { echo "ERROR: corrupt safetensors file: embeddings_model/model.safetensors"; exit 1; }

COPY scripts/generate_embeddings.py .
RUN set -e && for OCP_VERSION in $(ls -1 ocp-product-docs-plaintext); do \
        python3.12 generate_embeddings.py -f ocp-product-docs-plaintext/${OCP_VERSION} -r runbooks/alerts -md embeddings_model \
            -mn ${EMBEDDING_MODEL} -o vector_db/ocp_product_docs/${OCP_VERSION} \
            -i ocp-product-docs-$(echo $OCP_VERSION | sed 's/\./_/g') -v ${OCP_VERSION} -hb $HERMETIC; \
    done
RUN LATEST_VERSION=$(ls -1 vector_db/ocp_product_docs/ | sort -V | tail -n 1) && \
    cd vector_db/ocp_product_docs && ln -s ${LATEST_VERSION} latest

FROM registry.access.redhat.com/ubi9/ubi-minimal@sha256:ae09ecc3d754bc1726cbda3e2599cc7839e09fe1cc547ce173cf669b645be3cc
COPY --from=lightspeed-rag-builder /workdir/vector_db/ocp_product_docs /rag/vector_db/ocp_product_docs
COPY --from=lightspeed-rag-builder /workdir/embeddings_model /rag/embeddings_model

# this directory is checked by ecosystem-cert-preflight-checks task in Konflux
RUN mkdir /licenses
COPY LICENSE /licenses/

# Labels for enterprise contract
LABEL com.redhat.component=openshift-lightspeed-rag-content
LABEL cpe="cpe:/a:redhat:openshift_lightspeed:1::el9"
LABEL description="Red Hat OpenShift Lightspeed RAG content"
LABEL distribution-scope=private
LABEL io.k8s.description="Red Hat OpenShift Lightspeed RAG content"
LABEL io.k8s.display-name="Openshift Lightspeed RAG content"
LABEL io.openshift.tags="openshift,lightspeed,ai,assistant,rag"
LABEL name="openshift-lightspeed/lightspeed-rag-content-rhel9"
LABEL release=0.0.1
LABEL url="https://github.com/openshift/lightspeed-rag-content"
LABEL vendor="Red Hat, Inc."
LABEL version=0.0.1
LABEL summary="Red Hat OpenShift Lightspeed RAG content"
LABEL konflux.additional-tags="latest"

USER 65532:65532
