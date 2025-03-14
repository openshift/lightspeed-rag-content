ARG EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2
ARG FLAVOR=cpu
ARG HERMETIC=false

FROM registry.access.redhat.com/ubi9/python-311 as cpu-base
ARG EMBEDDING_MODEL
ARG FLAVOR

FROM nvcr.io/nvidia/cuda:12.8.1-devel-ubi9 as gpu-base
ARG EMBEDDING_MODEL
ARG FLAVOR
RUN dnf install -y python3.11 python3.11-pip libcudnn9 libnccl libcusparselt0

FROM ${FLAVOR}-base as lightspeed-rag-builder
ARG EMBEDDING_MODEL
ARG FLAVOR
ARG HERMETIC

USER 0
WORKDIR /workdir

COPY requirements.gpu.txt .
RUN pip3.11 install --no-cache-dir -r requirements.gpu.txt

COPY ocp-product-docs-plaintext ./ocp-product-docs-plaintext
COPY runbooks ./runbooks

COPY embeddings_model ./embeddings_model
#RUN cat embeddings_model/model.safetensors.part* > embeddings_model/model.safetensors && rm embeddings_model/model.safetensors.part*
RUN cd embeddings_model; if [ "$HERMETIC" == "true" ]; then \
        cp /cachi2/output/deps/generic/model.safetensors model.safetensors; \
    else \
        curl -L -O https://huggingface.co/sentence-transformers/all-mpnet-base-v2/resolve/9a3225965996d404b775526de6dbfe85d3368642/model.safetensors; \
    fi

RUN if [ "$FLAVOR" == "gpu" ]; then \
        export LD_LIBRARY_PATH=/usr/local/cuda-12.6/compat:$LD_LIBRARY_PATH; \
        python3.11 -c "import torch; print(torch.version.cuda); print(torch.cuda.is_available());"; \
    fi

COPY scripts/generate_embeddings.py .
RUN export LD_LIBRARY_PATH=/usr/local/cuda-12.6/compat:$LD_LIBRARY_PATH; \
    set -e && for OCP_VERSION in $(ls -1 ocp-product-docs-plaintext); do \
        python3.11 generate_embeddings.py -f ocp-product-docs-plaintext/${OCP_VERSION} -r runbooks/alerts -md embeddings_model \
            -mn ${EMBEDDING_MODEL} -o vector_db/ocp_product_docs/${OCP_VERSION} \
            -i ocp-product-docs-$(echo $OCP_VERSION | sed 's/\./_/g') -v ${OCP_VERSION} -hb $HERMETIC; \
    done

FROM registry.access.redhat.com/ubi9/ubi-minimal@sha256:14f14e03d68f7fd5f2b18a13478b6b127c341b346c86b6e0b886ed2b7573b8e0
COPY --from=lightspeed-rag-builder /workdir/vector_db/ocp_product_docs /rag/vector_db/ocp_product_docs
COPY --from=lightspeed-rag-builder /workdir/embeddings_model /rag/embeddings_model

# this directory is checked by ecosystem-cert-preflight-checks task in Konflux
RUN mkdir /licenses
COPY LICENSE /licenses/

# Labels for enterprise contract
LABEL com.redhat.component=openshift-lightspeed-rag-content
LABEL description="Red Hat OpenShift Lightspeed RAG content"
LABEL distribution-scope=private
LABEL io.k8s.description="Red Hat OpenShift Lightspeed RAG content"
LABEL io.k8s.display-name="Openshift Lightspeed RAG content"
LABEL io.openshift.tags="openshift,lightspeed,ai,assistant,rag"
LABEL name=openshift-lightspeed-rag-content
LABEL release=0.0.1
LABEL url="https://github.com/openshift/lightspeed-rag-content"
LABEL vendor="Red Hat, Inc."
LABEL version=0.0.1
LABEL summary="Red Hat OpenShift Lightspeed RAG content"

USER 65532:65532
