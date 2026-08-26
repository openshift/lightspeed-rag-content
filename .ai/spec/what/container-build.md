# Container Build

This spec defines the rules for building container images, hermetic build support, and CI/CD pipeline behavior.

## DEPRECATED: Behavioral Rules -- Main RAG Content Image

> The main RAG content image is deprecated. OCP product docs are now served by OKP via the RHOKP sidecar deployed by the operator. Only the BYOK tool image is actively maintained.

1. [DEPRECATED] The root `Containerfile` builds the main RAG content image using the plaintext pipeline with `scripts/generate_embeddings.py`, producing LlamaIndex FAISS indexes. [REMOVED: `lsc/Containerfile.konflux` and the lsc library pipeline have been deleted along with their Tekton pipelines.]

2. [DEPRECATED] Both Containerfiles follow a multi-stage build: a builder stage generates all vector indexes, then a minimal final stage copies only the output artifacts.

3. [DEPRECATED] Both builder stages iterate over all version directories in `ocp-product-docs-plaintext/` and generate one index per version. Each version's index includes both OCP docs and runbooks.

4. [DEPRECATED] The root Containerfile creates a `latest` symlink pointing to the highest version directory (determined by version-aware sorting).

5. [DEPRECATED] The final image uses `ubi9/ubi-minimal` (pinned by digest) as base and contains only:
   - `/rag/vector_db/ocp_product_docs/` -- all version index directories.
   - `/rag/embeddings_model/` -- the sentence-transformer model.
   - `/licenses/LICENSE` -- Apache 2.0 license for enterprise contract compliance.

6. [DEPRECATED] The final image runs as non-root user (UID 65532, GID 65532).

7. [DEPRECATED] The embedding model's `model.safetensors` file is sourced based on the `HERMETIC` build arg:
   - `HERMETIC=false`: Downloaded from HuggingFace at build time (URL pinned to a specific commit hash).
   - `HERMETIC=true`: Copied from the Cachi2 prefetch cache at `/cachi2/output/deps/generic/model.safetensors`.

8. [DEPRECATED] Container labels must satisfy Red Hat enterprise contract requirements: `com.redhat.component`, `cpe`, `description`, `distribution-scope`, `io.k8s.description`, `io.k8s.display-name`, `io.openshift.tags`, `name`, `release`, `url`, `vendor`, `version`, `summary`.

9. [DEPRECATED] The root Containerfile previously supported `FLAVOR` build arg for CPU/GPU base image selection. Now CPU-only.

## Behavioral Rules -- BYOK Tool Image

10. The BYOK tool image is built from `byok/Containerfile.tool`. It contains: `buildah`, Python 3.12, CPU Python dependencies, the embedding model, the BYOK embedding script (`generate_embeddings_tool.py`), and the output Containerfile template (`Containerfile.output`).

11. The tool image's CMD runs `buildah build` to produce the customer's RAG image from Markdown content mounted at `/markdown`, then pushes the result as a tar archive to `/output/`.

## Behavioral Rules -- Hermetic Builds

12. Hermetic builds (`HERMETIC=true`) operate without network access during the container build step.

13. All Python packages are pre-fetched via Cachi2 and installed from the prefetch cache. The requirements files include package hashes for verification.

14. The embedding model binary (`model.safetensors`) is fetched as a generic artifact via Cachi2 with a pinned SHA256 hash defined in `artifacts.lock.yaml`.

15. RPM packages are resolved and locked via `rpms.in.yaml` (input specification) and `rpms.lock.yaml` (locked versions).

16. URL reachability validation is skipped during hermetic builds (the `--hermetic-build true` flag is passed to the embedding script).

## Behavioral Rules -- CI/CD (Konflux/Tekton)

17. Two active pipelines exist as Tekton PipelineRun definitions:
    - `lightspeed-rag-tool-push/pull-request` -- BYOK tool image using `byok/Containerfile.tool`. Actively maintained.
    - [REMOVED] `lightspeed-ocp-rag-push/pull-request` and `own-app-lightspeed-rag-content-push/pull-request` have been deleted. OCP docs are served by OKP.

18. Push pipelines trigger on merge to `main`. Pull-request pipelines trigger on PRs.

19. All pipelines use hermetic builds with Cachi2 prefetch for pip packages, RPMs, and generic artifacts.

20. [REMOVED] The lsc/GPU pipeline has been deleted. All builds are now CPU-only.

21. [DEPRECATED] An integration test verifies the built image contains the expected paths: an `index_store.json` file under `/rag/vector_db/ocp_product_docs/{version}/` for every OCP version present in `ocp-product-docs-plaintext/`, and `config.json` under `/rag/embeddings_model/`.

## Configuration Surface

| Parameter | Type | Default | Purpose |
|---|---|---|---|
| `HERMETIC` | Build arg | `false` | Enable hermetic build mode |
| `EMBEDDING_MODEL` | Build arg | `sentence-transformers/all-mpnet-base-v2` | HuggingFace repo ID |
| `artifacts.lock.yaml` | File | -- | Pinned `model.safetensors` URL + SHA256 |
| `rpms.in.yaml` | File | -- | RPM dependency specifications |
| `rpms.lock.yaml` | File | -- | Locked RPM versions |
| `requirements.hashes.source.cpu.txt` | File | -- | Hashed PyPI source dependencies |
| `requirements.hashes.wheel.cpu.txt` | File | -- | Hashed RHOAI wheel dependencies |
| `requirements-build.cpu.txt` | File | -- | Build dependencies |
| `requirements.hermetic.txt` | File | -- | Bootstrap deps (pip) |
| `requirements.overrides.txt` | File | -- | Version pins for uv compilation |

## Constraints

1. The NLTK data directory must be symlinked after pip install to make tokenization data available.

2. Python dependencies are compiled by uv with split lockfiles (RHOAI wheels vs PyPI source). `scripts/konflux_requirements.sh` generates the lockfiles.

3. The `ubi-minimal` final image is pinned by digest, not tag. Digest updates are managed by automated Konflux/Mintmaker PRs.
