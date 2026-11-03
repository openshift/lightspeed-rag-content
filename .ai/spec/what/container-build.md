# Container Build

This spec defines the rules for building the tool container image, hermetic
build support, and CI/CD pipeline behavior.

## Behavioral Rules — Tool Image

1. The tool image is built from the root `Containerfile`. It contains: the
   statically linked `byok-go` binary (native libraries are linked in; the
   only shared-library dependency is glibc), the embedding model
   (mpnet.onnx, tokenizer, tiktoken ranks, sentence_bert config),
   third-party license files, and the baked output base layer.

2. The runtime stage is `ubi9-micro` (digest-pinned): no Python, no package
   manager, no shipped native libraries. The model and base layer ship in
   `/opt/byok`.

3. The tool image's CMD runs `byok-go` with the default mounts
   (`/markdown` in, `/output/$OUT_IMAGE_TAG.tar` out).

4. Native libraries (faiss v1.12.0, onnxruntime v1.31.0, OpenBLAS v0.3.29)
   are compiled from source in the image build from the git submodules
   under `third_party/` and linked statically into the `byok-go` binary.
   onnxruntime's CMake FetchContent dependencies are also git submodules
   (`third_party/onnxruntime-deps/`) and are wired via
   `FETCHCONTENT_SOURCE_DIR_<NAME>` overrides — no network downloads.

5. The embedding model binary (`mpnet.onnx`) is stored as committed gzip
   chunks under `model/` and reassembled during the image build, verified
   against a committed sha256.

## Behavioral Rules — Hermetic Builds

6. Hermetic builds (`HERMETIC=true`) operate without network access during
   the container build step, beyond the Cachi2-prefetched RPM toolchain.

7. All Go module dependencies are vendored (`vendor/`); `go build` runs
   with `-mod=vendor`.

8. RPM packages are resolved and locked via `rpms.in.yaml` (input
   specification) and `rpms.lock.yaml` (locked versions). Digest updates to
   base images are managed by automated Konflux/Mintmaker PRs.

9. Third-party license files are collected into `/opt/byok/licenses/`
   during the build for SBOM/attribution.

## Behavioral Rules — CI/CD (Konflux/Tekton)

10. Two pipelines exist as Tekton PipelineRun definitions:
    - `lightspeed-rag-tool-on-pull-request` (`.tekton/lightspeed-rag-tool-pull-request.yaml`)
      — pull-request builds.
    - `lightspeed-rag-tool-on-push` (`.tekton/lightspeed-rag-tool-push.yaml`)
      — merge-to-main builds.
    Both use the Konflux docker-build trusted-artifact pipeline with
    hermetic Cachi2 RPM prefetch.

11. The BYOK customer-workflow integration scenario (in
    `.tekton/integration-tests/`) runs the tool image with its default CMD
    on a fictional Markdown corpus, loads the exported customer image with
    podman, checks the packaged index metadata, and serves the index
    through an explicitly digest-pinned OLS image with real LLM inference.
    Success requires an answer-only fact from fictional Markdown and its
    matching document title/URL citation. Missing snapshot components,
    image digests, or source commits must fail rather than fall back to a
    mutable tag or branch.

## Configuration Surface

| Parameter | Type | Default | Purpose |
|---|---|---|---|
| `HERMETIC` | Build arg | `false` | Enable hermetic build mode |
| `GO_TOOLSET` | Build arg | `ubi9/go-toolset:latest` | Go builder stage image |
| `NATIVE_IMAGE` | Build arg | `ubi9/ubi:latest` | Native compile stage image |
| `TOOL_IMAGE` | Build arg | `ubi9-micro` (digest-pinned) | Runtime stage image |
| `OUTPUT_BASE_IMAGE` | Build arg | `ubi9-minimal` (digest-pinned) | Customer output image base |
| `OUT_IMAGE_TAG` | Build arg / env | `byok-image` | Tag for the output image |
| `VECTOR_DB_INDEX` | Build arg / env | `vector_db_index` | Index ID string |
| `model/mpnet.onnx.gz.*` | Files | — | Committed gzip chunks of the embedding model |
| `model/mpnet.onnx.sha256` | File | — | sha256 of the reassembled `mpnet.onnx` |
| `rpms.in.yaml` / `rpms.lock.yaml` | Files | — | RPM dependency specs and locks |

## Constraints

1. The base images of the final stages (`TOOL_IMAGE`, `OUTPUT_BASE_IMAGE`)
   are pinned by digest, not tag. Digest updates are managed by automated
   Konflux/Mintmaker PRs.

2. The git submodules under `third_party/` must be initialized
   (`git submodule update --init --recursive`) before building locally;
   Konflux clones with submodules.

3. Local builds of cgo packages stage the native libraries via
   `scripts/stage-go-native.sh` (cached under `.byok-go-native/`); pure-Go
   packages build and test without any native libraries.

4. Regenerating the model chunks requires a local `mpnet.onnx`:
   `make model-chunks MODEL=/path/to/mpnet.onnx`.
