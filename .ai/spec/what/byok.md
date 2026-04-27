# BYOK (Bring Your Own Knowledge)

BYOK enables customers to create custom RAG indexes from their own documentation, so that OpenShift LightSpeed responses incorporate organization-specific knowledge alongside standard product documentation.

## Behavioral Rules

1. BYOK accepts customer-supplied Markdown files as input, mounted at `/markdown` in the tool container.

2. Markdown files may optionally contain YAML frontmatter (delimited by `---`) with `title` and `url` fields. If present, these override the default metadata extraction.

3. If no YAML frontmatter is present, `title` is extracted from the first line of the file (stripping any leading `# ` prefix), and `docs_url` defaults to the file path.

4. Only `.md` files are processed. Files are read recursively from the input directory using `FlatReader` (raw text ingestion -- no Markdown structure parsing).

5. The BYOK tool uses the same embedding model (`sentence-transformers/all-mpnet-base-v2`), default chunk size (380 tokens), default chunk overlap (0), and FAISS output format (`IndexFlatIP`) as the main pipeline. Customer indexes are interchangeable with product indexes from lightspeed-service's perspective.

6. The BYOK tool produces a container image as an OCI tar archive at `/output/{tag}.tar`. The output image contains the vector DB at `/rag/vector_db/`.

7. The tool container uses `buildah` internally to build the output image. It runs a nested container build using `Containerfile.output`, which:
   - Uses the tool image itself as the builder stage to run the embedding generation script.
   - Copies the generated vectors into a minimal UBI base image.

8. Node filtering (the whitespace-only check applied in other pipelines) is NOT applied in BYOK. All chunks from the text splitter are included in the index.

9. The output image contains only the vector DB, NOT the embedding model. The service must provide the model separately (typically from the main RAG content image).

## Configuration Surface -- Environment Variables (Tool Container)

| Variable | Default | Purpose |
|---|---|---|
| `OUT_IMAGE_TAG` | `byok-image` | Tag for the output container image |
| `VECTOR_DB_INDEX` | `vector_db_index` | Index ID string |
| `BYOK_TOOL_IMAGE` | `registry.redhat.io/.../lightspeed-rag-tool-rhel9:latest` | Base image for the tool stage |
| `UBI_BASE_IMAGE` | `registry.access.redhat.com/ubi9/ubi:latest` | Base image for the output container |
| `LOG_LEVEL` | `info` | buildah log level |

## Configuration Surface -- CLI Arguments (`generate_embeddings_tool.py`)

| Argument | Default | Purpose |
|---|---|---|
| `-i` / `--input-dir` | (required) | Input directory with Markdown content |
| `-emd` / `--embedding-model-dir` | `embeddings_model` | Embedding model directory |
| `-emn` / `--embedding-model-name` | (required) | HuggingFace repo ID |
| `-cs` / `--chunk-size` | `380` | Chunk size in tokens |
| `-co` / `--chunk-overlap` | `0` | Chunk overlap in tokens |
| `-o` / `--output-dir` | (required) | Vector DB output directory |
| `-id` / `--index-id` | (required) | Index ID string |

## Constraints

1. The tool container requires `buildah` and uses `BUILDAH_ISOLATION=chroot` for rootless container building.

2. The tool container runs as root (USER 0) because buildah requires privilege for image building.

3. BYOK uses CPU-only dependencies (`requirements.cpu.txt`). GPU acceleration is not supported for BYOK.

4. The output directory path is sanitized via `os.path.normpath("/" + path).lstrip("/")` to prevent path traversal.

5. The customer must mount their Markdown content at `/markdown` and their output directory at `/output` when running the tool container.

## Planned Changes

- [PLANNED: OCPSTRAT-1494 Phase 2] Seamless one-click import from Git repositories and Confluence, replacing the manual container-based workflow.
- [PLANNED: OLS-1872] Internal web source integration for BYOK.
