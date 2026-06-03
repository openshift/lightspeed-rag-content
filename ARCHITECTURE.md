# Architecture

OpenShift LightSpeed RAG Content is a build-time artifact producer. It converts OpenShift product documentation and operational runbooks into pre-built FAISS vector indexes, packages them alongside a sentence-transformer embedding model into container images, and publishes those images for consumption by OpenShift LightSpeed (lightspeed-service) at runtime.

The project has no runtime component -- everything runs during the container image build.

## System Context

```mermaid
graph LR
    subgraph Sources
        OCP[openshift/openshift-docs]
        RB[openshift/runbooks]
        CUST[Customer Markdown]
    end

    subgraph "lightspeed-rag-content (build-time)"
        PIPE[Embedding Pipelines]
        MODEL[sentence-transformers/all-mpnet-base-v2]
    end

    subgraph Outputs
        RAG[RAG Content Image]
        BYOK_IMG[BYOK Tool Image]
    end

    OCP --> PIPE
    RB --> PIPE
    MODEL --> PIPE
    PIPE --> RAG
    CUST --> BYOK_IMG

    RAG -->|volume mount| SVC[lightspeed-service]
    BYOK_IMG -->|customer runs| CUST_RAG[Custom RAG Image]
    CUST_RAG -->|volume mount| SVC
```

## Pipeline Implementations

Three pipeline implementations exist, each producing vector indexes from different input sources and using different processing strategies:

```mermaid
graph TD
    subgraph "lsc library pipeline (primary)"
        LSC_IN[OCP plaintext + Runbooks] --> LSC_PROC[lsc/custom_processor.py]
        LSC_PROC --> LSC_LIB[DocumentProcessor]
        LSC_LIB --> LSC_OUT[llamastack-faiss indexes]
    end

    subgraph "Plaintext pipeline (alternative)"
        PT_IN[OCP plaintext + Runbooks] --> PT_PROC[scripts/generate_embeddings.py]
        PT_PROC --> PT_OUT[LlamaIndex FAISS indexes]
    end

    subgraph "HTML pipeline (development)"
        HTML_IN[Red Hat docs portal HTML] --> HTML_DL[Download]
        HTML_DL --> HTML_STRIP[Strip non-content]
        HTML_STRIP --> HTML_CHUNK[Semantic HTML chunking]
        HTML_CHUNK --> HTML_EMBED[Embed]
        HTML_EMBED --> HTML_OUT[FAISS indexes]
    end
```

| Pipeline | Entry point | Backend | Used by CI | Python |
|----------|------------|---------|-----------|--------|
| **lsc library** | `lsc/custom_processor.py` | llamastack-faiss | `lightspeed-ocp-rag-push/pull-request` | 3.12 |
| **Plaintext** | `scripts/generate_embeddings.py` | LlamaIndex FAISS | `own-app-lightspeed-rag-content-push/pull-request` | 3.12 |
| **HTML** | `scripts/html_embeddings/generate_embeddings.py` | LlamaIndex FAISS | None | 3.12 |

## Container Build

```mermaid
graph TD
    subgraph "lsc/Containerfile.konflux (primary)"
        B1_BASE[CUDA 12.9 + Python 3.12] --> B1_DEPS[pip install lsc/requirements.txt]
        B1_DEPS --> B1_COPY[Copy docs + runbooks + model]
        B1_COPY --> B1_LOOP["For each OCP version:<br/>python3.12 custom_processor.py"]
        B1_LOOP --> B1_FINAL[ubi-minimal final image]
    end

    subgraph "Root Containerfile (alternative)"
        B2_BASE["CPU or GPU base<br/>(FLAVOR arg)"] --> B2_DEPS[pip install requirements.gpu.txt]
        B2_DEPS --> B2_COPY[Copy docs + runbooks + model]
        B2_COPY --> B2_LOOP["For each OCP version:<br/>python3.12 generate_embeddings.py"]
        B2_LOOP --> B2_LINK[Create latest symlink]
        B2_LINK --> B2_FINAL[ubi-minimal final image]
    end

    B1_FINAL --> IMG1["/rag/vector_db/<br/>/rag/embeddings_model/"]
    B2_FINAL --> IMG2["/rag/vector_db/<br/>/rag/embeddings_model/"]
```

Both builds follow the same pattern: a builder stage generates all vector indexes (one per OCP version), then a minimal final stage copies only the output artifacts. The final image contains the indexes at `/rag/vector_db/ocp_product_docs/{version}/` and the embedding model at `/rag/embeddings_model/`.

### Hermetic builds

For Konflux CI, builds run with `HERMETIC=true` (no network access). All dependencies are prefetched by Cachi2:

- **pip** packages from `requirements.{cpu,gpu}.txt` (with hashes)
- **RPMs** from `rpms.lock.yaml`
- **model.safetensors** from `artifacts.lock.yaml` (pinned URL + SHA256)

## Data Flow

A single OCP version goes through this flow during the container build:

```mermaid
flowchart LR
    DOCS["ocp-product-docs-plaintext/4.18/"] --> LOAD[Load documents]
    RUNBOOKS["runbooks/alerts/"] --> LOAD
    LOAD --> CHUNK["Chunk<br/>(380 tokens)"]
    CHUNK --> FILTER[Filter invalid nodes]
    FILTER --> EMBED["Embed<br/>(all-mpnet-base-v2)"]
    EMBED --> FAISS["FAISS IndexFlatIP"]
    FAISS --> PERSIST["vector_db/ocp_product_docs/4.18/"]
```

Each chunk carries metadata (`docs_url`, `title`) derived from the file path during loading. The embedding model produces 768-dimensional normalized vectors stored in a FAISS inner-product index.

## Key Directories

```
lightspeed-rag-content/
├── lsc/                          # Installable Python library (primary pipeline)
│   ├── src/lightspeed_rag_content/   # Library source: DocumentProcessor, MetadataProcessor
│   ├── custom_processor.py           # Orchestrator for lsc pipeline
│   └── Containerfile.konflux         # Primary CI Containerfile
├── scripts/                      # Standalone pipeline scripts
│   ├── generate_embeddings.py        # Plaintext pipeline
│   ├── html_embeddings/              # HTML pipeline
│   └── html_chunking/                # Semantic HTML chunking library
├── byok/                         # Bring Your Own Knowledge tooling
├── ocp-product-docs-plaintext/   # Committed OCP docs (4.16 - 4.22)
├── runbooks/                     # Committed alert runbooks
├── embeddings_model/             # sentence-transformers/all-mpnet-base-v2
├── Containerfile                 # Alternative RAG content image
├── Makefile                      # Developer build automation
└── pyproject.toml                # PDM project metadata
```

## Integration with lightspeed-service

The RAG content image is mounted as a read-only volume by lightspeed-service (configured via the OpenShift LightSpeed operator's CRD). At startup, the service loads the FAISS indexes via LlamaIndex's `StorageContext.from_defaults()` and uses the same embedding model to encode user queries for vector similarity search.

**Critical invariant:** the embedding model used to build the indexes must be identical to the model the service uses for query embedding. A mismatch produces meaningless similarity scores. This is enforced by shipping the model inside the RAG content image.

## Key Decisions

- **Pre-built indexes, not runtime indexing.** All computation happens at build time. The service loads indexes read-only. This avoids runtime compute costs and ensures deterministic RAG content across deployments.

- **Multiple pipeline implementations coexist.** The lsc library pipeline (llamastack-faiss) is the primary CI path. The plaintext pipeline (LlamaIndex FAISS) is the alternative. The HTML pipeline is for development. This reflects an ongoing migration from plain LlamaIndex to llama-stack backends.

- **OCP docs and runbooks are committed to the repo.** The production build uses pre-committed content, not live clones. Content acquisition scripts exist for maintenance but are not invoked during the container build.

- **PDM with dual lockfiles.** CPU and GPU compute flavors have separate lockfiles (`pdm.lock.cpu`, `pdm.lock.gpu`) because PyTorch has different packages for each.
