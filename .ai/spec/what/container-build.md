# Container Build

This spec defines the rules for building container images, hermetic build support, and CI/CD pipeline behavior.

## Behavioral Rules -- Main RAG Content Image

1. The build is a multi-stage process: a builder stage generates all vector indexes, then a minimal final stage copies only the output artifacts.

2. The builder stage supports two base images selected by the `FLAVOR` build arg:
   - `cpu`: UBI9 Python 3.11 (`registry.access.redhat.com/ubi9/python-311`).
   - `gpu`: NVIDIA CUDA 12.9.1 devel on UBI9 (`nvcr.io/nvidia/cuda:12.9.1-devel-ubi9`), with additional system packages installed via dnf.

3. The builder stage iterates over all version directories in `ocp-product-docs-plaintext/` and generates one FAISS index per version using the plaintext pipeline script. Each version's index includes both OCP docs and runbooks.

4. After all indexes are generated, a `latest` symlink is created pointing to the highest version directory (determined by version-aware sorting).

5. The final image uses `ubi9/ubi-minimal` (pinned by digest) as base and contains only:
   - `/rag/vector_db/ocp_product_docs/` -- all version index directories plus the `latest` symlink.
   - `/rag/embeddings_model/` -- the sentence-transformer model.
   - `/licenses/LICENSE` -- Apache 2.0 license for enterprise contract compliance.

6. The final image runs as non-root user (UID 65532, GID 65532).

7. The embedding model's `model.safetensors` file is sourced based on the `HERMETIC` build arg:
   - `HERMETIC=false`: Downloaded from HuggingFace at build time (URL pinned to a specific commit hash).
   - `HERMETIC=true`: Copied from the Cachi2 prefetch cache at `/cachi2/output/deps/generic/model.safetensors`.

8. Container labels must satisfy Red Hat enterprise contract requirements: `com.redhat.component`, `cpe`, `description`, `distribution-scope`, `io.k8s.description`, `io.k8s.display-name`, `io.openshift.tags`, `name`, `release`, `url`, `vendor`, `version`, `summary`.

## Behavioral Rules -- BYOK Tool Image

9. The BYOK tool image is built from `byok/Containerfile.tool`. It contains: `buildah`, Python 3.11, CPU Python dependencies, the embedding model, the BYOK embedding script (`generate_embeddings_tool.py`), and the output Containerfile template (`Containerfile.output`).

10. The tool image's CMD runs `buildah build` to produce the customer's RAG image from Markdown content mounted at `/markdown`, then pushes the result as a tar archive to `/output/`.

## Behavioral Rules -- Hermetic Builds

11. Hermetic builds (`HERMETIC=true`) operate without network access during the container build step.

12. All Python packages are pre-fetched via Cachi2 and installed from the prefetch cache. The requirements files include package hashes for verification.

13. The embedding model binary (`model.safetensors`) is fetched as a generic artifact via Cachi2 with a pinned SHA256 hash defined in `artifacts.lock.yaml`.

14. RPM packages are resolved and locked via `rpms.in.yaml` (input specification) and `rpms.lock.yaml` (locked versions).

15. URL reachability validation is skipped during hermetic builds (the `--hermetic-build true` flag is passed to the embedding script).

## Behavioral Rules -- CI/CD (Konflux/Tekton)

16. Six pipelines exist as Tekton PipelineRun definitions:
    - Push and pull-request variants for the main RAG content image.
    - Push and pull-request variants for the BYOK tool image.
    - Push and pull-request variants for an alternative build variant.

17. Push pipelines trigger on merge to `main`. Pull-request pipelines trigger on PRs.

18. All pipelines use hermetic builds with Cachi2 prefetch for pip packages, RPMs, and generic artifacts.

19. The main RAG image builds with `FLAVOR=gpu` in CI.

20. An integration test verifies the built image contains the expected paths: a `index_store.json` file under `/rag/vector_db/` for at least one OCP version, and `config.json` under `/rag/embeddings_model/`.

## Configuration Surface

| Parameter | Type | Default | Purpose |
|---|---|---|---|
| `FLAVOR` | Build arg | `cpu` | Base image selection: `cpu` or `gpu` |
| `HERMETIC` | Build arg | `false` | Enable hermetic build mode |
| `EMBEDDING_MODEL` | Build arg | `sentence-transformers/all-mpnet-base-v2` | HuggingFace repo ID |
| `artifacts.lock.yaml` | File | -- | Pinned `model.safetensors` URL + SHA256 |
| `rpms.in.yaml` | File | -- | RPM dependency specifications |
| `rpms.lock.yaml` | File | -- | Locked RPM versions |
| `requirements.cpu.txt` | File | -- | Exported pip dependencies with hashes (CPU) |
| `requirements.gpu.txt` | File | -- | Exported pip dependencies with hashes (GPU) |
| `pdm.lock.cpu` | File | -- | PDM lockfile (CPU) |
| `pdm.lock.gpu` | File | -- | PDM lockfile (GPU) |
| `renovate.json` | File | -- | Dependency update automation config |

## Constraints

1. The NLTK data directory must be symlinked after pip install to make tokenization data available.

2. GPU builds require the CUDA compatibility library path to be set for library discovery.

3. Python dependencies are managed by PDM with separate lockfiles per compute flavor. The `pdm export` command generates the `requirements.*.txt` files used by pip inside the container build.

4. The `ubi-minimal` final image is pinned by digest, not tag. Digest updates are managed by automated Konflux/Mintmaker PRs.

5. Python package auto-updates via Renovate are disabled (configured in `renovate.json`). Dependency updates are manual and require lockfile regeneration.
