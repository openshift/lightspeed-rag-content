# System Overview

OpenShift LightSpeed RAG Content is a build-time artifact producer for the OpenShift LightSpeed AI assistant. It converts OpenShift product documentation and operational runbooks into pre-built FAISS vector indexes, packages them alongside the embedding model into container images, and publishes those images for consumption by the lightspeed-service at runtime.

## Behavioral Rules

1. The project produces pre-built FAISS vector indexes from three content sources: OCP product documentation, OpenShift alert runbooks, and customer-supplied Markdown (BYOK). The indexes are packaged as container images consumed by lightspeed-service.

2. The project is a build-time artifact producer. All computation -- document conversion, chunking, embedding generation, and vector store creation -- happens during the container image build or via offline scripts. The project never runs at runtime.

3. Two container image artifacts are produced:
   - **Main RAG content image**: Contains all OCP version vector indexes, the `latest` symlink, and the embedding model. Consumed by lightspeed-service as a volume mount.
   - **BYOK tool image**: Contains buildah, the embedding toolchain, and the embedding model. Used by customers to build custom RAG images from their own Markdown content.

4. Three pipeline implementations exist for generating vector indexes, each producing FAISS-compatible output:
   - **Plaintext pipeline** (`scripts/generate_embeddings.py`): The production pipeline used by the main Containerfile. Processes pre-converted plaintext OCP docs and Markdown runbooks.
   - **HTML pipeline** (`scripts/html_embeddings/`): Downloads HTML documentation from the Red Hat portal, strips non-content markup, performs semantic HTML chunking, and generates embeddings.
   - **lsc library** (`lsc/src/lightspeed_rag_content/`): An installable Python library supporting multiple vector store backends (FAISS, PostgreSQL, llama-stack faiss, llama-stack sqlite-vec).

5. The embedding model must be redistributable under an Apache 2.0 compatible license.

6. The project supports two compute flavors: CPU and GPU. The CPU flavor uses a PyTorch build from pytorch.org without CUDA. The GPU flavor uses standard PyTorch with NVIDIA CUDA 12.9.

## Integration Contract

### Consumed by lightspeed-service

The main RAG content image is mounted as a volume by lightspeed-service (typically via the OpenShift LightSpeed operator). The service reads:

- `/rag/vector_db/ocp_product_docs/{version}/` -- persisted FAISS vector store files (`docstore.json`, `index_store.json`, `graph_store.json`, `vector_store.json`, `metadata.json`).
- `/rag/vector_db/ocp_product_docs/latest` -- symlink to the highest OCP version directory.
- `/rag/embeddings_model/` -- the HuggingFace-compatible sentence-transformer model used to embed user queries at runtime.

The service loads these indexes read-only at startup via LlamaIndex's `StorageContext.from_defaults()` and uses the same embedding model to encode queries for vector similarity search.

### Integration invariant

The embedding model used to generate the indexes must be identical to the model used by lightspeed-service for query embedding. A mismatch produces meaningless similarity scores. The model identity is currently enforced by shipping the model inside the RAG content image and configuring the service to use it via `ols_config.reference_content.embeddings_model_path`.

### Operator integration

The OpenShift LightSpeed operator configures RAG content references via the CRD. Each index entry specifies `product_docs_index_path`, `product_docs_index_id`, and `product_docs_origin`. The operator mounts the RAG content image and maps these paths. [PLANNED: OLS-1812 -- per-index embedding model path in CRD]

## Constraints

1. Python 3.11 is required (`requires-python = "==3.11.*"`).

2. Both CPU and GPU compute flavors must be supported. The Containerfile selects the base image via the `FLAVOR` build arg.

3. Hermetic builds (no network access during build) must be supported for Konflux/Cachi2 CI. All dependencies -- Python packages, RPMs, and the embedding model binary -- must be prefetchable.

4. The project uses PDM for dependency management with separate lockfiles per compute flavor (`pdm.lock.cpu`, `pdm.lock.gpu`).

## Planned Changes

- [PLANNED: OLS-2294] Add metadata generation stage to the pipeline.
- [PLANNED: OLS-1729] Embedding model fine-tuning -- use fine-tuned models for better domain-specific retrieval accuracy.
- [PLANNED: OLS-2903] OKP-based RAG -- propose plans to use OKP (OpenShift Knowledge Platform) content with OLS.
- [PLANNED: OLS-2704] RAG as a service / MCP -- externalize RAG retrieval behind an MCP interface.
- [PLANNED: OCPSTRAT-1495] Include OCP KCS (Knowledge-Centered Service) content in OLS.
- [PLANNED: OCPSTRAT-1492] Include OCP layered product knowledge (CNV, ACM, RHOSO) in OLS.
