# System Overview

> **Deprecation notice:** The main RAG content image (pre-built FAISS vector indexes of OCP product documentation) is deprecated. OCP product documentation is now served by the Offline Knowledge Portal (OKP) via the RHOKP sidecar deployed by the operator. This repository now provides BYOK (Bring Your Own Knowledge) tooling only — a container image that lets customers build custom RAG indexes from their own Markdown content.

OpenShift LightSpeed RAG Content is a BYOK tooling provider for the OpenShift LightSpeed AI assistant. It packages an embedding model and build tools into a container image that customers use to produce custom FAISS vector indexes from their own Markdown content. The resulting BYOK indexes are consumed by lightspeed-service at runtime.

## Behavioral Rules

1. The project produces a BYOK tool image that customers use to build custom FAISS vector indexes from customer-supplied Markdown content. The resulting indexes are packaged as container images consumed by lightspeed-service. [DEPRECATED: The project previously also produced pre-built indexes from OCP product documentation and OpenShift alert runbooks. OCP docs are now served by OKP via the RHOKP sidecar.]

2. The project is a build-time artifact producer. All computation -- document conversion, chunking, embedding generation, and vector store creation -- happens during the container image build or via offline scripts. The project never runs at runtime. This now applies to BYOK content only.

3. One container image artifact is produced:
   - **BYOK tool image**: Contains buildah, the embedding toolchain, and the embedding model. Used by customers to build custom RAG images from their own Markdown content.
   - [DEPRECATED: **Main RAG content image** — previously contained all OCP version vector indexes, the `latest` symlink, and the embedding model. No longer built; OCP docs are served by OKP.]

4. Two pipeline implementations exist for generating vector indexes:
   - **Plaintext pipeline** (`scripts/generate_embeddings.py` + root `Containerfile`): Processes pre-converted plaintext OCP docs and Markdown runbooks using plain LlamaIndex FAISS. The BYOK path in `generate_embeddings_tool.py` remains active. [DEPRECATED for OCP docs production; OCP docs now served by OKP.]
   - [DEPRECATED] **HTML pipeline** (`scripts/html_embeddings/`): Downloaded HTML documentation from the Red Hat portal, stripped non-content markup, performed semantic HTML chunking, and generated embeddings. Was never used by any CI pipeline.
   - [REMOVED] The **lsc library pipeline** (`lsc/`) has been deleted. It used the lsc library to produce `llamastack-faiss` indexes via the `lightspeed-ocp-rag-push/pull-request` Tekton pipelines.

5. The embedding model must be redistributable under an Apache 2.0 compatible license.

6. The project uses CPU-only builds. The GPU flavor has been retired along with the lsc pipeline.

## Integration Contract

### BYOK tool image

The BYOK tool image is used by customers to build custom RAG container images from their own Markdown content. The tool image contains buildah, the embedding toolchain, and the embedding model. Customers mount their Markdown at `/markdown` and the tool produces a RAG image archive at `/output/`.

The resulting BYOK RAG images are consumed by lightspeed-service via init containers configured through the operator CRD's `rag[]` entries. Each BYOK index is mounted and registered as a `reference_content` entry.

### DEPRECATED: Main RAG content image

> The main RAG content image is deprecated. OCP product documentation is now served by OKP via the RHOKP sidecar deployed by the operator. The mount paths and integration described below are no longer applicable to new deployments.

Previously, the main RAG content image was mounted as a volume by lightspeed-service. The service read:
- `/rag/vector_db/ocp_product_docs/{version}/` -- persisted FAISS vector store files.
- `/rag/vector_db/ocp_product_docs/latest` -- symlink to the highest OCP version directory.
- `/rag/embeddings_model/` -- the sentence-transformer model used to embed user queries at runtime.

### Integration invariant

The embedding model used to generate BYOK indexes must be identical to the model used by lightspeed-service for BYOK query embedding. A mismatch produces meaningless similarity scores. The model identity is enforced by shipping the model inside the BYOK tool image and configuring the service to use it via `ols_config.reference_content.embeddings_model_path`.

### Operator integration

The OpenShift LightSpeed operator configures BYOK RAG content references via the CRD. Each BYOK index entry specifies `product_docs_index_path`, `product_docs_index_id`, and `product_docs_origin`. The operator mounts BYOK RAG images via init containers and maps these paths.

## Constraints

1. CPU-only builds. The GPU flavor has been retired.

2. Hermetic builds (no network access during build) must be supported for Konflux/Cachi2 CI. All dependencies -- Python packages, RPMs, and the embedding model binary -- must be prefetchable.

3. The project uses uv for dependency compilation with a single set of CPU lockfiles.

## Planned Changes

- [PLANNED: OLS-2704] RAG as a service / MCP -- externalize RAG retrieval behind an MCP interface. Relevant to BYOK.
- [PLANNED: OLS-1872] BYOK Phase 2 -- one-click import from Git/Confluence.
