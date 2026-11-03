# System Overview

OpenShift Lightspeed RAG Content is the BYOK (Bring Your Own Knowledge) tool
for the OpenShift Lightspeed AI assistant. It is a single Go binary
(`byok-go`) packaged in a container image. Customers run the tool image with
their own Markdown mounted; the tool generates a FAISS vector index and
packages it as a `podman load`-able container image archive
(docker-archive format). The resulting BYOK
images are consumed by lightspeed-service at runtime.

## Behavioral Rules

1. The project produces one artifact: the **BYOK tool image**. It contains
   the `byok-go` binary, the native libraries (faiss for indexing, ONNX
   Runtime for inference), and the embedding model. Customers use it to build
   images from their own Markdown content.

2. The project is a build-time artifact producer. All computation — document
   parsing, chunking, embedding generation, and vector store creation —
   happens offline inside the tool container. The project never runs at
   runtime.

3. The tool produces customer RAG images as container image archives in
   the docker-archive (`docker save`) format — not by running a nested
   container build. The output archive contains a minimal base layer plus
   one data layer holding `/rag/vector_db`.

4. The embedding model is `sentence-transformers/all-mpnet-base-v2` (ONNX
   export), 768-dimensional vectors, licensed under Apache 2.0.

5. Customer indexes are interchangeable with product indexes from
   lightspeed-service's perspective: same embedding model, same FAISS
   `IndexFlatIP` format, and the same llama-index storage persistence
   format.

6. Builds are CPU-only. GPU acceleration is not supported.

7. Builds are hermetic: everything needed to build the tool image is
   committed to the repository (vendored Go modules, native library sources
   as git submodules, the model as gzip chunks, locked RPMs). No network
   access is required during the container build beyond the base images and
   the Cachi2-prefetched RPM toolchain.

## Integration Contract

The BYOK tool image is used by customers to build custom RAG container
images from their own Markdown content. Customers mount their Markdown at
`/markdown` and an output directory at `/output`; the tool's default CMD
writes the archive to `/output/{tag}.tar`.

The resulting BYOK RAG images are consumed by lightspeed-service via init
containers configured through the operator CRD's `rag[]` entries. Each BYOK
index is mounted and registered as a `reference_content` entry.

### Integration invariant

The embedding model used to generate BYOK indexes must be identical to the
model used by lightspeed-service for BYOK query embedding. A mismatch
produces meaningless similarity scores. The tool and the service each ship
their own copy of the same model (`sentence-transformers/all-mpnet-base-v2`);
the service loads its copy from `ols_config.reference_content.embeddings_model_path`,
falling back to the model bundled in the service image. The two copies must
stay in sync.

### Runtime consumption format

lightspeed-service loads the generated vector DB via llama-index-core's
`FaissVectorStore.from_persist_dir`. The storage persistence format and the
faiss serialization must therefore remain byte-compatible with the
service's llama-index/faiss-cpu versions. See `what/embedding-pipeline.md`.

## Constraints

1. CPU-only builds.

2. The serialized FAISS index must load in the service's faiss-cpu runtime.
   The faiss version compiled into the tool must match the service's.

3. The output image archive must load with `podman load` (and
   `docker load`) without a container runtime present in the tool image.

## Planned Changes

- [PLANNED: OLS-2704] RAG as a service / MCP — externalize RAG retrieval
  behind an MCP interface. Relevant to BYOK.
- [PLANNED: OLS-1872] BYOK Phase 2 — one-click import from Git/Confluence,
  replacing the manual container-based workflow.
