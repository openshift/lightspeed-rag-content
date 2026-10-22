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
| `.tekton/integration-tests/pipelines/byok-integration-test.yaml` | Snapshot-selected VM integration pipeline |
| `.tekton/integration-tests/byok-integration-test-scenario.yaml` | Required rag-tool application test registration |
| `.tekton/integration-tests/scripts/run-in-vm.sh` | Secure VM execution, artifact retrieval, TEST_OUTPUT reporting |
| `tests/integration-konflux/` | Default-CMD workflow, fictional runbook, OLS config, answer/citation validation |
| `tests/unit/` | Runtime environment, actual snapshot extraction script, and answer validation regression tests |
| `pyproject.toml` | Project metadata, dependency groups, linting config |
| `requirements.hashes.source.txt` / `requirements.hashes.wheel.txt` | Split hashed runtime lockfiles (PyPI source vs RHOAI wheels) |
| `requirements.hashes.wheel.pypi.txt` | Hashed runtime PyPI wheel fallbacks, prefetched and installed by BYOK |
| `requirements-build.txt` | Hashed PyPI build dependencies lockfile |
| `requirements.hermetic.txt` | RHOAI build/bootstrap wheels |
| `requirements.overrides.txt` | Explicit override policy for uv compilation; not modified by targeted updates |
| `rpms.in.yaml` / `rpms.lock.yaml` | RPM dependency spec + lockfile for Cachi2 |
| `embeddings_model/model.safetensors.tar.gz.*` | Committed chunks of the embedding-model binary |

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
  ├── Reassemble model.safetensors from committed archive chunks
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
  ├── PATH-selected python3.12 -m pip install split lockfiles from Cachi2 cache (hermetic) or `.[cpu]` (local)
  ├── Discover NLTK cache from runtime llama_index.core and symlink /root/nltk_data
  ├── COPY embeddings_model and reassemble model.safetensors from archive chunks
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
| `install-tools` | Verify uv | Check prerequisites; uv provisions Python 3.12 |
| `install-deps` | `uv pip install` | Install runtime deps |
| `install-deps-test` | `uv pip install" black mypy ruff` | Install dev deps |
| `bump` | `scripts/konflux_resolve.py --profile cpu [--package PKG --version VERSION]` | Refresh dependencies or perform a targeted minimum-version update |
| `update-konflux-deps` | Alias for `bump` | Compatibility entry point |
| `test-resolver-image` | `OLS_TEST_RESOLVER_IMAGE=1 make test-unit` | Exercise the real forked uv using local package-index fixtures |
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

Cachi2 prefetches two dependency types:
- **pip**: Runtime packages from `requirements.hashes.source.txt`, `requirements.hashes.wheel.txt`, and `requirements.hashes.wheel.pypi.txt`; build/bootstrap wheels from `requirements.hermetic.txt`; and PyPI build dependencies from `requirements-build.txt` via `requirements_build_files`. Explicit `binary.packages` lists distinguish wheels from source distributions.
- **rpm**: From `rpms.lock.yaml`.

`byok/Containerfile.tool` copies all three runtime lockfiles and passes each to the hermetic `pip install` command. `requirements.hashes.wheel.pypi.txt` may contain no packages, but must still be generated, prefetched, and consumed so an allowed PyPI wheel fallback is not omitted from the image. This wiring does not change the resolver's RHOAI-first source-selection policy.

### Build

Uses `buildah` task with:
- `hermetic=true` -- network-isolated build.
- Build args: `HERMETIC=true`.
- The prefetched dependencies are injected into the build context.

### Post-build

- **Source image**: Created for artifact provenance tracking.
- **Label check**: Validates enterprise contract labels.

### Customer-workflow integration

The required IntegrationTestScenario for application `rag-tool` resolves the BYOK test pipeline.
The pipeline extracts the digest-pinned `lightspeed-rag-tool` image and source commit from
SNAPSHOT and runs the test on a `linux-mlarge/amd64` VM. The VM runner uses an infrastructure
container for Podman tooling, transfers registry and OpenAI credentials without shell tracing,
and returns Konflux `TEST_OUTPUT` even on workflow failure.

`tests/integration-konflux/pipeline-konflux.sh` runs the product's default CMD with mounted
fictional Markdown, `STORAGE_DRIVER=vfs`, and the snapshot tool image as `BYOK_TOOL_IMAGE`.
It loads the archive, extracts `/rag/vector_db`, checks metadata, and runs the OLS service's
default entrypoint with that index. The query must return the answer-only fictional recovery
phrase and the expected `referenced_documents` title/URL. The OLS service and output UBI base
are explicit digest-pinned parameters because they are not components of the `rag-tool`
application snapshot. See `byok/README.md` for local execution, registration, and credentials.

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
make bump → scripts/konflux_resolve.py
     (forked uv image: --index-strategy prefer-index)
     │
     ▼
requirements.hashes.source.txt       (PyPI runtime source distributions, hashed)
requirements.hashes.wheel.txt        (RHOAI runtime wheels, hashed)
requirements.hashes.wheel.pypi.txt    (PyPI runtime wheel fallbacks, hashed)
requirements-build.txt              (PyPI build dependencies, pinned and hashed)
requirements.hermetic.txt           (RHOAI build/bootstrap wheels)
requirements.overrides.txt          (explicit override policy for uv)

rpms.in.yaml → rpms.lock.yaml
     (Cachi2 RPM resolution for container build)

embeddings_model/model.safetensors.tar.gz.*
     (committed model archive chunks reassembled during the image build)
```

### Targeted dependency resolution

`make bump` provisions Python 3.12, packaging, tomlkit, and source-discovery tooling through host uv. It invokes the existing resolver with optional `--package`/`--version` arguments. Compilation remains in `quay.io/syedriko/uv:prefer-index`: the index policy is implemented by that fork, not upstream uv.

For targeted updates, the resolver seeds a scratch output file with runtime, build, and bootstrap pins, then uses `--upgrade-package` to allow the target to move. Pins are preferences rather than constraints. Tomlkit preserves project-file structure when raising direct/optional dependency floors. Equality restrictions, including wildcard release-series bounds such as `==1.*`, are retained; incompatible requested minima fail without editing the project. The requested minimum is passed in memory through every solve (initial runtime, joint resolution, and runtime projection), and written only to a temporary scratch file passed with `--constraints`. No persistent transitive-minimum file is read or written. Subsequent targeted runs use current lockfiles as preferences; full refreshes use the existing project requirements and override policy without any remembered transitive minimums. Existing `requirements.overrides.txt` is still passed with `--override` as deliberate policy, but targeted updates never modify it.

Source-build requirements are discovered with `pybuild_deps.finder.find_build_dependencies` under the profile interpreter. The resolver jointly compiles project, bootstrap, and reachable build requirements, then projects that solution onto runtime roots using exact constraints from the **new** solution. Index annotations and dependency-parent annotations track source policy and recursive build reachability. Discovery repeats until the roots and selected versions stabilize, with cycle detection and a 12-round limit. Runtime/build overlap therefore uses the same selected version instead of deleting an unchecked duplicate or restoring an old pin.

If a joint solve is incompatible, discovery retains the source-package versions that introduced build requirements. A breadth-first search retries with temporary exclusions of those versions, rediscovering requirements from scratch while preserving the original lockfile preferences, requested minimum, and project/override policy. This allows a build-tool update to move its source parent without refreshing unrelated dependencies. The search tries at most 64 alternatives; exhaustion reports an explicit error rather than publishing an unchecked result. Non-resolution failures are not retried.

Runtime artifacts go in `requirements.hashes.wheel.txt` (RHOAI wheels), `requirements.hashes.source.txt` (PyPI source), or `requirements.hashes.wheel.pypi.txt` (permitted PyPI wheel fallbacks); build-only RHOAI artifacts go in `requirements.hermetic.txt`, and build-only PyPI artifacts in `requirements-build.txt`. Both Tekton prefetch configurations include `requirements.hashes.wheel.pypi.txt`, and their binary package lists include runtime and build wheels. All outputs are generated in scratch space before publication. PDM locks are not synchronized.

## Implementation Notes

- The NLTK data symlink (`ln -s .../nltk_cache /root/nltk_data`) is required because LlamaIndex's sentence tokenizer depends on NLTK's `punkt` tokenizer data. The data is bundled with the llama-index-core package but needs to be discoverable at the default NLTK data path.

- The `ubi-minimal` final image digest is periodically updated by Konflux/Mintmaker automation, which submits PRs to update the `@sha256:...` pinning.

- `scripts/generate_packages_to_prefetch.py` is a legacy Cachito-era script (obsolete). Lockfile generation is now handled by `make bump` and `scripts/konflux_resolve.py`.
