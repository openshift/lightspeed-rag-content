ARG OCP_VERSION=4.15
ARG EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2

FROM registry.access.redhat.com/ubi9/python-311 as lightspeed-rag-builder
ARG OCP_VERSION
ARG EMBEDDING_MODEL

USER 0
WORKDIR /workdir

COPY requirements.txt requirements_torch.txt .
RUN pip install -r requirements.txt

COPY ocp-product-docs-plaintext ./ocp-product-docs-plaintext

COPY scripts/download_embeddings_model.py .
RUN python download_embeddings_model.py -l ./embeddings_model -r ${EMBEDDING_MODEL}

COPY scripts/generate_embeddings.py .
RUN python generate_embeddings.py -f ocp-product-docs-plaintext/${OCP_VERSION} -md embeddings_model \
    -mn ${EMBEDDING_MODEL} -o vector_db/ocp_product_docs/${OCP_VERSION} \
    -i ocp-product-docs-$(echo $OCP_VERSION | sed 's/\./_/g') -v ${OCP_VERSION}

FROM scratch
ARG OCP_VERSION
COPY --from=lightspeed-rag-builder /workdir/vector_db/ocp_product_docs/${OCP_VERSION} /rag/vector_db/ocp_product_docs/${OCP_VERSION}
COPY --from=lightspeed-rag-builder /workdir/embeddings_model /rag/embeddings_model
