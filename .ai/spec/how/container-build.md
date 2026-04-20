# Container Build -- Architecture

This spec documents the Containerfiles, Makefile targets, and Konflux/Tekton pipeline configurations that build and publish the project's container images.

## Module Map

| Path | Purpose |
|---|---|
| `Containerfile` | Main RAG content image -- multi-stage build (builder → minimal) |
| `byok/Containerfile.tool` | BYOK tool image -- buildah + Python + model + script |
| `byok/Containerfile.output` | BYOK output image template -- vectors only, built inside tool container |
| `Makefile` | Developer-facing build automation |
| `.tekton/lightspeed-ocp-rag-push.yaml` | Konflux push pipeline for main RAG image |
| `.tekton/lightspeed-ocp-rag-pull-request.yaml` | Konflux PR pipeline for main RAG image |
| `.tekton/lightspeed-rag-tool-push.yaml` | Konflux push pipeline for BYOK tool image |
| `.tekton/lightspeed-rag-tool-pull-request.yaml` | Konflux PR pipeline for BYOK tool image |
| `.tekton/own-app-lightspeed-rag-content-push.yaml` | Alternative build variant push pipeline |
| `.tekton/own-app-lightspeed-rag-content-pull-request.yaml` | Alternative build variant PR pipeline |
| `.tekton/integration-tests/lightspeed-rag-content-image-verification.yaml` | Integration test -- validates image contents |
| `pyproject.toml` | PDM project metadata, dependency groups, linting config |
| `requirements.cpu.txt` / `requirements.gpu.txt` | Exported pip dependencies with hashes |
| `pdm.lock.cpu` / `pdm.lock.gpu` | PDM lockfiles per compute flavor |
| `rpms.in.yaml` / `rpms.lock.yaml` | RPM dependency spec + lockfile for Cachi2 |
| `artifacts.lock.yaml` | Pinned model.safetensors URL + SHA256 |
| `renovate.json` | Dependency update automation config |

## Main Containerfile -- Build Stages

### Stage 1: Base image selection

Two named stages define the base images. The `FLAVOR` build arg (default: `cpu`) selects which one is used:

```dockerfile
FROM registry.access.redhat.com/ubi9/python-311 as cpu-base
FROM nvcr.io/nvidia/cuda:12.9.1-devel-ubi9 as gpu-base
FROM ${FLAVOR}-base as lightspeed-rag-builder
```

The GPU base installs additional system packages: `python3.11`, `python3.11-pip`, `libcudnn9`, `libnccl`, `libcusparselt0`.

### Stage 2: Builder (`lightspeed-rag-builder`)

```
USER 0, WORKDIR /workdir

1. pip install requirements.gpu.txt
2. Symlink NLTK data:
     ln -s .../site-packages/llama_index/core/_static/nltk_cache /root/nltk_data
3. COPY ocp-product-docs-plaintext, runbooks, embeddings_model
4. Acquire model.safetensors:
     HERMETIC=true  → cp /cachi2/output/deps/generic/model.safetensors
     HERMETIC=false → curl from HuggingFace (pinned commit SHA)
5. GPU validation (FLAVOR=gpu only):
     python3.11 -c "import torch; print(torch.version.cuda); print(torch.cuda.is_available())"
     (requires LD_LIBRARY_PATH=/usr/local/cuda-12/compat)
6. COPY scripts/generate_embeddings.py
7. For each OCP_VERSION in $(ls -1 ocp-product-docs-plaintext):
     python3.11 generate_embeddings.py \
       -f ocp-product-docs-plaintext/${VERSION} \
       -r runbooks/alerts \
       -md embeddings_model \
       -mn ${EMBEDDING_MODEL} \
       -o vector_db/ocp_product_docs/${VERSION} \
       -i ocp-product-docs-$(echo $VERSION | sed 's/\./_/g') \
       -v ${VERSION} \
       -hb $HERMETIC
8. Create latest symlink:
     LATEST=$(ls -1 vector_db/ocp_product_docs/ | sort -V | tail -n 1)
     ln -s ${LATEST} vector_db/ocp_product_docs/latest
```

### Stage 3: Final image

```dockerfile
FROM registry.access.redhat.com/ubi9/ubi-minimal@sha256:{digest}
COPY --from=lightspeed-rag-builder /workdir/vector_db/ocp_product_docs /rag/vector_db/ocp_product_docs
COPY --from=lightspeed-rag-builder /workdir/embeddings_model /rag/embeddings_model
RUN mkdir /licenses
COPY LICENSE /licenses/
# Enterprise contract labels (com.redhat.component, cpe, vendor, etc.)
USER 65532:65532
```

The `ubi-minimal` image is pinned by SHA256 digest. Digest updates are managed by automated Konflux/Mintmaker PRs.

## BYOK Containerfile.tool

```
FROM ubi9/ubi:latest
  ├── dnf install buildah python3.11 python3.11-pip
  ├── pip install requirements.cpu.txt (--no-deps)
  ├── COPY embeddings_model
  ├── Acquire model.safetensors (same HERMETIC logic as main Containerfile)
  ├── COPY byok/generate_embeddings_tool.py, byok/Containerfile.output
  ├── Enterprise contract labels
  ├── Set environment:
  │     _BUILDAH_STARTED_IN_USERNS=""
  │     BUILDAH_ISOLATION=chroot
  │     OUT_IMAGE_TAG, BYOK_TOOL_IMAGE, UBI_BASE_IMAGE, LOG_LEVEL, VECTOR_DB_INDEX
  └── CMD: buildah build \
        --build-arg BYOK_TOOL_IMAGE=$BYOK_TOOL_IMAGE \
        --build-arg UBI_BASE_IMAGE=$UBI_BASE_IMAGE \
        --env VECTOR_DB_INDEX=$VECTOR_DB_INDEX \
        -t $OUT_IMAGE_TAG -f Containerfile.output \
        -v /markdown:/markdown:Z . \
     && buildah push $OUT_IMAGE_TAG docker-archive:/output/$OUT_IMAGE_TAG.tar
```

## BYOK Containerfile.output

```
FROM ${BYOK_TOOL_IMAGE} as tool
  USER 0, WORKDIR /workdir
  RUN python3.11 generate_embeddings_tool.py \
      -i /markdown -emd embeddings_model \
      -emn sentence-transformers/all-mpnet-base-v2 \
      -o vector_db -id $VECTOR_DB_INDEX

FROM ${UBI_BASE_IMAGE}
  COPY --from=tool /workdir/vector_db /rag/vector_db
```

## Makefile Targets

| Target | Command | Purpose |
|---|---|---|
| `install-tools` | `pip3.11 install pdm` | Install PDM if not present |
| `pdm-lock-check` | `pdm lock --check --group {cpu,gpu}` | Validate both lockfiles |
| `install-deps` | `pdm sync --group $(TORCH_GROUP) --lockfile pdm.lock.$(TORCH_GROUP)` | Install runtime deps |
| `install-deps-test` | `pdm sync --dev --group $(TORCH_GROUP) ...` | Install dev deps |
| `update-deps` | `pdm update --update-all ... && pdm export ...` | Update + regenerate requirements.*.txt |
| `check-types` | `mypy --explicit-package-bases scripts` | Type checking |
| `format` | `black scripts && ruff check scripts --fix` | Code formatting |
| `verify` | `black --check scripts && ruff check scripts` | Lint verification |
| `update-docs` | Loop: `get_ocp_plaintext_docs.sh $V` + `get_runbooks.sh` | Refresh committed content |
| `update-model` | `python scripts/download_embeddings_model.py` | Download embedding model |
| `build-image` | `podman build -t rag-content .` | Local container build |
| `model-safetensors` | `wget model.safetensors` if not present | Download model binary |

`FLAVOR` variable (default: `cpu`) maps to `TORCH_GROUP` which selects the lockfile and requirements file. The `verify` and `format` targets apply `--per-file-ignores=scripts/*:S101` to allow assert statements in scripts.

## Konflux Pipeline Structure

All six pipelines are Tekton PipelineRun definitions that follow the same pattern:

### Prefetch dependencies

Cachi2 prefetches three dependency types:
- **pip**: From `requirements.{cpu|gpu}.txt` with hashes.
- **rpm**: From `rpms.lock.yaml`.
- **generic**: From `artifacts.lock.yaml` (model.safetensors URL + SHA256).

### Build

Uses `buildah` task with:
- `hermetic=true` -- network-isolated build.
- Build args: `FLAVOR=gpu`, `HERMETIC=true`.
- The prefetched dependencies are injected into the build context.

### Post-build

- **Source image**: Created for artifact provenance tracking.
- **Label check**: Validates enterprise contract labels.
- **Integration test** (push pipelines only): Runs `lightspeed-rag-content-image-verification.yaml`.

### Integration test

`lightspeed-rag-content-image-verification.yaml` is a Tekton Task that:
1. Mounts the built image.
2. Checks for `/rag/vector_db/{version}/index_store.json` for at least one OCP version.
3. Checks for `/rag/embeddings_model/config.json`.
4. Fails if either path is missing.

## Dependency Management Flow

```
pyproject.toml
├── [project.dependencies]           Core deps (llama-index, faiss, etc.)
├── [project.optional-dependencies]
│     cpu = [torch @ https://...cpu...]   CPU PyTorch wheel (pinned URL + hash)
│     gpu = [torch==2.6.0]               GPU PyTorch from PyPI
└── [tool.pdm.dev-dependencies]
      dev = [black, mypy, ruff, types-requests]

     │
     ▼
pdm lock → pdm.lock.cpu / pdm.lock.gpu
     │
     ▼
pdm export → requirements.cpu.txt / requirements.gpu.txt
     (with --hashes for pip install verification)

rpms.in.yaml → rpms.lock.yaml
     (Cachi2 RPM resolution for container build)

artifacts.lock.yaml
     (model.safetensors URL + SHA256 for Cachi2 generic artifact)

renovate.json:
  - Python package auto-updates: DISABLED
  - Konflux references: auto-updated
```

## Implementation Notes

- The main Containerfile always installs `requirements.gpu.txt` regardless of `FLAVOR`. The `FLAVOR` arg only affects the base image selection (CPU vs GPU). This means the CPU builder installs GPU-compatible torch, which works but is larger than necessary.

- The `--no-deps` flag is used in the BYOK tool's `pip install` but NOT in the main Containerfile. This prevents pip from pulling transitive dependencies that might conflict with the locked set.

- `generate_packages_to_prefetch.py` (in `lsc/scripts/`) is a complex script for Cachi2 hermetic build preparation. It: copies the project stub, removes torch from pyproject.toml, runs `pip-compile` to generate requirements.txt, removes torch + nvidia packages, separately downloads the CPU torch wheel from PyPI, computes its hash, and generates `requirements-build.txt`. This script is not invoked during the container build itself -- it is a developer tool for maintaining the Cachi2 prefetch inputs.

- The NLTK data symlink (`ln -s .../nltk_cache /root/nltk_data`) is required because LlamaIndex's sentence tokenizer depends on NLTK's `punkt` tokenizer data. The data is bundled with the llama-index-core package but needs to be discoverable at the default NLTK data path.

- GPU builds set `LD_LIBRARY_PATH=/usr/local/cuda-12/compat` for CUDA library discovery. This is needed both during the torch validation step and during the embedding generation loop.

- The `ubi-minimal` final image digest is periodically updated by Konflux/Mintmaker automation, which submits PRs to update the `@sha256:...` pinning.
