ARG EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2
ARG FLAVOR=cpu
ARG HERMETIC=false

FROM registry.access.redhat.com/ubi9/python-312 as cpu-base
ARG EMBEDDING_MODEL
ARG FLAVOR

FROM nvcr.io/nvidia/cuda:12.9.1-devel-ubi9 as gpu-base
ARG EMBEDDING_MODEL
ARG FLAVOR
# Suppress GPU device requests during image build: the CUDA base image sets
# NVIDIA_VISIBLE_DEVICES=all which causes CDI setup to fail on non-GPU build hosts.
# "void" tells the NVIDIA container toolkit to skip device setup entirely.
ENV NVIDIA_VISIBLE_DEVICES=void
RUN dnf install -y python3.12 python3.12-pip libcudnn9 libnccl libcusparselt0 && dnf clean all

FROM ${FLAVOR}-base as lightspeed-rag-builder
ARG EMBEDDING_MODEL
ARG FLAVOR
ARG HERMETIC

USER 0
WORKDIR /workdir

# Konflux hermetic: Cachi2 vendor layout (PIP_FIND_LINKS) + hashed split lockfiles
COPY \
    requirements.hashes.wheel.cpu.txt \
    requirements.hashes.wheel.gpu.txt \
    requirements.hashes.source.cpu.txt \
    requirements.hashes.source.gpu.txt \
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
            -r "requirements.hashes.wheel.${FLAVOR}.txt" \
            -r "requirements.hashes.source.${FLAVOR}.txt"; \
    else \
        /usr/bin/python3.12 -m pip install --no-cache-dir -e ".[${FLAVOR}]"; \
    fi
RUN ln -s "/usr/local/lib/python3.12/site-packages/llama_index/core/_static/nltk_cache" /root/nltk_data

COPY ocp-product-docs-plaintext ./ocp-product-docs-plaintext
COPY runbooks ./runbooks

COPY embeddings_model ./embeddings_model
RUN cd embeddings_model; if [ "$HERMETIC" == "true" ]; then \
        cp /cachi2/output/deps/generic/model.safetensors model.safetensors; \
    else \
        curl -L -O https://huggingface.co/sentence-transformers/all-mpnet-base-v2/resolve/9a3225965996d404b775526de6dbfe85d3368642/model.safetensors; \
    fi

RUN if [ "$FLAVOR" == "gpu" ]; then \
        export LD_LIBRARY_PATH=/usr/local/cuda-12/compat:$LD_LIBRARY_PATH; \
        python3.12 -c "import torch; print(torch.version.cuda); print(torch.cuda.is_available());"; \
    fi

COPY scripts/generate_embeddings.py .
RUN export LD_LIBRARY_PATH=/usr/local/cuda-12/compat:$LD_LIBRARY_PATH; \
    set -e && for OCP_VERSION in $(ls -1 ocp-product-docs-plaintext); do \
        python3.12 generate_embeddings.py -f ocp-product-docs-plaintext/${OCP_VERSION} -r runbooks/alerts -md embeddings_model \
            -mn ${EMBEDDING_MODEL} -o vector_db/ocp_product_docs/${OCP_VERSION} \
            -i ocp-product-docs-$(echo $OCP_VERSION | sed 's/\./_/g') -v ${OCP_VERSION} -hb $HERMETIC; \
    done
RUN LATEST_VERSION=$(ls -1 vector_db/ocp_product_docs/ | sort -V | tail -n 1) && \
    cd vector_db/ocp_product_docs && ln -s ${LATEST_VERSION} latest

FROM registry.access.redhat.com/ubi9/ubi-minimal@sha256:7d4e47500f28ac3a2bff06c25eff9127ff21048538ae03ce240d57cf756acd00
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
