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

7. [DEPRECATED] The embedding model's `model.safetensors` file is reassembled from committed `embeddings_model/model.safetensors.tar.gz.*` archive chunks during the image build.

8. [DEPRECATED] Container labels must satisfy Red Hat enterprise contract requirements: `com.redhat.component`, `cpe`, `description`, `distribution-scope`, `io.k8s.description`, `io.k8s.display-name`, `io.openshift.tags`, `name`, `release`, `url`, `vendor`, `version`, `summary`.

9. [DEPRECATED] The root Containerfile previously supported `FLAVOR` build arg for CPU/GPU base image selection. Now CPU-only.

## Behavioral Rules -- BYOK Tool Image

10. The BYOK tool image is built from `byok/Containerfile.tool`. It contains: `buildah`, Python 3.12, CPU Python dependencies, the embedding model, the BYOK embedding script (`generate_embeddings_tool.py`), and the output Containerfile template (`Containerfile.output`).

11. The tool image's CMD runs `buildah build` to produce the customer's RAG image from Markdown content mounted at `/markdown`, then pushes the result as a tar archive to `/output/`. Dependency installation, model validation, and embedding execution use the same PATH-selected `python3.12` environment.

## Behavioral Rules -- Hermetic Builds

12. Hermetic builds (`HERMETIC=true`) operate without network access during the container build step.

13. All Python packages are pre-fetched via Cachi2 and installed from the prefetch cache. The requirements files include package hashes for verification. The BYOK hermetic build must prefetch and install all three runtime requirement sets: RHOAI wheels (`requirements.hashes.wheel.txt`), PyPI source distributions (`requirements.hashes.source.txt`), and permitted PyPI wheel fallbacks (`requirements.hashes.wheel.pypi.txt`).

14. The embedding model binary (`model.safetensors`) is stored as committed archive chunks and reassembled during the image build; it is not fetched as a Cachi2 generic artifact.

15. RPM packages are resolved and locked via `rpms.in.yaml` (input specification) and `rpms.lock.yaml` (locked versions).

16. URL reachability validation is skipped during hermetic builds (the `--hermetic-build true` flag is passed to the embedding script).

## Behavioral Rules -- CI/CD (Konflux/Tekton)

17. Two active pipelines exist as Tekton PipelineRun definitions:
    - `lightspeed-rag-tool-push/pull-request` -- BYOK tool image using `byok/Containerfile.tool`. Actively maintained.
    - [REMOVED] `lightspeed-ocp-rag-push/pull-request` and `own-app-lightspeed-rag-content-push/pull-request` have been deleted. OCP docs are served by OKP.

18. Push pipelines trigger on merge to `main`. Pull-request pipelines trigger on PRs.

19. All pipelines use hermetic builds with Cachi2 prefetch for pip packages and RPMs.

20. [REMOVED] The lsc/GPU pipeline has been deleted. All builds are now CPU-only.

21. The required BYOK customer-workflow integration scenario runs the exact snapshot tool image with its default CMD on an x86_64 Konflux VM. It uses that same image for the nested build, loads the exported customer image, checks the packaged index metadata, and serves the index through an explicitly digest-pinned OLS image with real LLM inference. Success requires an answer-only fact from fictional Markdown and its matching document title/URL citation. Missing snapshot components, image digests, or source commits must fail rather than fall back to a mutable tag or branch.

## Configuration Surface

| Parameter | Type | Default | Purpose |
|---|---|---|---|
| `HERMETIC` | Build arg | `false` | Enable hermetic build mode |
| `EMBEDDING_MODEL` | Build arg | `sentence-transformers/all-mpnet-base-v2` | HuggingFace repo ID |
| `embeddings_model/model.safetensors.tar.gz.*` | Files | -- | Committed chunks of the embedding-model archive |
| `rpms.in.yaml` | File | -- | RPM dependency specifications |
| `rpms.lock.yaml` | File | -- | Locked RPM versions |
| `requirements.hashes.source.txt` | File | -- | Hashed PyPI source dependencies |
| `requirements.hashes.wheel.txt` | File | -- | Hashed RHOAI runtime wheel dependencies |
| `requirements.hashes.wheel.pypi.txt` | File | -- | Hashed PyPI runtime wheel fallbacks |
| `requirements-build.txt` | File | -- | Hashed PyPI build dependencies |
| `requirements.hermetic.txt` | File | -- | Hashed RHOAI build/bootstrap wheels |
| `requirements.overrides.txt` | File | -- | Deliberately configured overrides of upstream requirements |

## Constraints

1. The NLTK data directory must be symlinked after pip install to make tokenization data available. Its path is discovered from `llama_index.core` in the runtime Python environment, not a hard-coded system site-packages directory.

2. Python dependency updates use `make bump` and generate split Konflux requirements for RHOAI wheels, PyPI source dependencies, and permitted PyPI wheel fallbacks.
   - With no arguments, the command refreshes dependencies to the newest mutually compatible versions permitted by the project requirements and overrides.
   - With `PKG=<name> VERSION=<version>`, the command sets the named dependency's minimum version to `VERSION` and produces a compatible dependency set containing that version or a newer one.
   - Targeted updates must prefer existing locked versions of other packages. Other runtime, build, or bootstrap dependencies may be updated, added, or removed as needed to accommodate the requested update. Unrelated dependencies must not be refreshed merely because newer versions are available.
   - Requested minimums must intersect upstream dependency ranges, not replace them. Transitive minimums apply only to the current targeted run and must not introduce a persistent policy file or new inputs for full refreshes. Subsequent targeted updates use the current lockfiles as preferences, not a history of requested minimums. Direct and optional dependency minimums are updated in the project requirements. Deliberately configured overrides are a separate policy input and must not be modified by targeted updates.
   - If project constraints prevent a compatible solution satisfying the requested minimum version, the command must fail with a diagnostic identifying the blocking constraints. It must not silently lower the requested minimum or discard explicit compatibility restrictions.
   - Successful updates regenerate the affected requirements and prefetch configuration. The resulting dependency set must satisfy the applicable constraints for the image's target Python version and platform.

3. The `ubi-minimal` final image is pinned by digest, not tag. Digest updates are managed by automated Konflux/Mintmaker PRs.
