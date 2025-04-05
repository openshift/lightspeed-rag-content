ARG EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2

FROM registry.access.redhat.com/ubi9/python-311:latest
ARG EMBEDDING_MODEL

USER 0
WORKDIR /workdir

COPY requirements.cpu.txt .
RUN pip3.11 install --no-cache-dir -r requirements.cpu.txt

COPY embeddings_model ./embeddings_model
COPY byok/generate_embeddings_tool.py .
