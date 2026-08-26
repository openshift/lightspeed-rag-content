# Container Build -- Architecture

This spec documents the Containerfiles, Makefile targets, and Konflux/Tekton pipeline configurations that build and publish the project's container images.

## Module Map

| Path | Purpose |
|---|---|
| `Containerfile` | RAG content image -- plaintext pipeline, LlamaIndex FAISS, Python 3.12 |
| `byok/Containerfile.tool` | BYOK tool image -- buildah + Python + model + script |
| `byok/Containerfile.output` | BYOK output image template -- vectors only, built inside tool container |
| `Makefile` | Developer-facing build automation |
| `.tekton/lightspeed-rag-tool-push.yaml` | Konflux push pipeline for BYOK tool image |
| `.tekton/lightspeed-rag-tool-pull-request.yaml` | Konflux PR pipeline for BYOK tool image |
| `.tekton/integration-tests/lightspeed-rag-content-image-verification.yaml` | Integration test -- validates image contents |
| `pyproject.toml` | Project metadata, dependency groups, linting config |
| `requirements.hashes.source.cpu.txt` / `requirements.hashes.wheel.cpu.txt` | Split hashed lockfiles (PyPI source vs RHOAI wheels) |
| `requirements-build.cpu.txt` | Build dependencies lockfile |
| `requirements.hermetic.txt` | Hermetic build bootstrap deps (pip) |
| `requirements.overrides.txt` | Version overrides for uv compilation |
| `rpms.in.yaml` / `rpms.lock.yaml` | RPM dependency spec + lockfile for Cachi2 |
| `artifacts.lock.yaml` | Pinned model.safetensors URL + SHA256 |

## [REMOVED] lsc/Containerfile.konflux

The lsc library pipeline and its Containerfile have been deleted. It previously used `nvcr.io/nvidia/cuda:12.9.2-devel-ubi9` as base, produced `llamastack-faiss` indexes via `custom_processor.py`, and was built by the `lightspeed-ocp-rag-push/pull-request` Tekton pipelines. OCP docs are now served by OKP via the RHOKP sidecar.

## Root Containerfile -- RAG Content Image (LlamaIndex FAISS)

CPU-only build using `registry.access.redhat.com/ubi9/python-312`.

### Build Stages

```
Stage 1: lightspeed-rag-builder (FROM ubi9/python-312)
  ├── pip install split lockfiles (RHOAI wheels + PyPI source)
  ├── Symlink NLTK data
  ├── COPY ocp-product-docs-plaintext, runbooks, embeddings_model
  ├── Acquire model.safetensors (HERMETIC=true from Cachi2, else curl)
  ├── COPY scripts/generate_embeddings.py
  ├── For each OCP_VERSION:
  │     python3.12 generate_embeddings.py ...
  └── Create latest symlink

Stage 2: Final (ubi9/ubi-minimal, pinned by digest)
  ├── COPY vector_db → /rag/vector_db/ocp_product_docs
  ├── COPY embeddings_model → /rag/embeddings_model
  ├── Enterprise contract labels
  └── USER 65532:65532
```

The `ubi-minimal` image is pinned by SHA256 digest. Digest updates are managed by automated Konflux/Mintmaker PRs.

## BYOK Containerfile.tool

```
FROM quay.io/aipcc/base-image-cpu-rhel9:3.5
  ├── dnf install buildah python3.12 python3.12-pip
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
  RUN python3.12 generate_embeddings_tool.py \
      -i /markdown -emd embeddings_model \
      -emn sentence-transformers/all-mpnet-base-v2 \
      -o vector_db -id $VECTOR_DB_INDEX

FROM ${UBI_BASE_IMAGE}
  COPY --from=tool /workdir/vector_db /rag/vector_db
```

## Makefile Targets

| Target | Command | Purpose |
|---|---|---|
| `install-tools` | Verify uv + Python 3.12 | Check prerequisites |
| `install-deps` | `uv pip install -e ".[cpu]"` | Install runtime deps |
| `install-deps-test` | `uv pip install -e ".[cpu]" black mypy ruff` | Install dev deps |
| `update-konflux-deps` | `scripts/konflux_requirements.sh` | Regenerate split lockfiles for Konflux |
| `check-types` | `mypy --explicit-package-bases scripts` | Type checking |
| `format` | `black scripts && ruff check scripts --fix` | Code formatting |
| `verify` | `black --check scripts && ruff check scripts` | Lint verification |
| `update-docs` | Loop: `get_ocp_plaintext_docs.sh $V` + `get_runbooks.sh` | Refresh committed content |
| `update-model` | `python scripts/download_embeddings_model.py` | Download embedding model |
| `build-image` | `podman build -t rag-content .` | Local container build |
| `model-safetensors` | `wget model.safetensors` if not present | Download model binary |

The `verify` and `format` targets apply `--per-file-ignores=scripts/*:S101` to allow assert statements in scripts.

## Konflux Pipeline Structure

Two active pipelines (`lightspeed-rag-tool-push/pull-request`) are Tekton PipelineRun definitions:

### Prefetch dependencies

Cachi2 prefetches three dependency types:
- **pip**: From split lockfiles (`requirements.hashes.source.cpu.txt` + `requirements.hashes.wheel.cpu.txt`) with explicit `binary.packages` lists.
- **rpm**: From `rpms.lock.yaml`.
- **generic**: From `artifacts.lock.yaml` (model.safetensors URL + SHA256).

### Build

Uses `buildah` task with:
- `hermetic=true` -- network-isolated build.
- Build args: `HERMETIC=true`.
- The prefetched dependencies are injected into the build context.

### Post-build

- **Source image**: Created for artifact provenance tracking.
- **Label check**: Validates enterprise contract labels.
- **Integration test** (push pipelines only): Runs `lightspeed-rag-content-image-verification.yaml`.

### Integration test

`lightspeed-rag-content-image-verification.yaml` is a Tekton Pipeline that:
1. Extracts the built image reference from the Konflux snapshot.
2. Runs the image with `python3.11 scripts/verify_rag_image_test.py`.
3. `verify_rag_image_test.py` iterates over all version directories in `ocp-product-docs-plaintext/` and asserts `/rag/vector_db/ocp_product_docs/{version}/index_store.json` exists for every version.
4. Also asserts `/rag/embeddings_model/config.json` exists.
5. Fails if any version's index or the model config is missing.

## Dependency Management Flow

```
pyproject.toml
├── [project.dependencies]           Core deps (llama-index, faiss, etc.)
├── [project.optional-dependencies]
│     cpu = [torch @ https://...rhoai/3.5/cpu-ubi9/...]   RHOAI CPU PyTorch wheel
└── [tool.pdm.dev-dependencies]
      dev = [black, mypy, ruff, types-requests]

     │
     ▼
scripts/konflux_requirements.sh (uv pip compile)
     │
     ▼
requirements.hashes.source.cpu.txt   (PyPI packages, hashed)
requirements.hashes.wheel.cpu.txt    (RHOAI wheels, hashed)
requirements-build.cpu.txt           (build deps via pybuild-deps)
requirements.hermetic.txt            (bootstrap: pip)
requirements.overrides.txt           (version pins for uv)

rpms.in.yaml → rpms.lock.yaml
     (Cachi2 RPM resolution for container build)

artifacts.lock.yaml
     (model.safetensors URL + SHA256 for Cachi2 generic artifact)
```

## Implementation Notes

- The NLTK data symlink (`ln -s .../nltk_cache /root/nltk_data`) is required because LlamaIndex's sentence tokenizer depends on NLTK's `punkt` tokenizer data. The data is bundled with the llama-index-core package but needs to be discoverable at the default NLTK data path.

- The `ubi-minimal` final image digest is periodically updated by Konflux/Mintmaker automation, which submits PRs to update the `@sha256:...` pinning.

- `scripts/generate_packages_to_prefetch.py` is a legacy Cachito-era script (obsolete). Lockfile generation is now handled by `scripts/konflux_requirements.sh`.
