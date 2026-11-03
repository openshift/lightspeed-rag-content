# BYOK (Bring Your Own Knowledge)

BYOK enables customers to create custom RAG indexes from their own
documentation, so that OpenShift Lightspeed responses incorporate
organization-specific knowledge alongside standard product documentation.

## Behavioral Rules

1. BYOK accepts customer-supplied Markdown files as input, mounted at
   `/markdown` in the tool container. The input directory is walked
   recursively; only files with the `.md` extension are processed. An input
   directory with no Markdown files is an error.

2. Documents are ingested as raw text (no Markdown structure parsing).

3. Markdown files may optionally contain YAML frontmatter (delimited by
   `---`) with `title` and `url` fields. If present, these override the
   default metadata extraction.

4. If no YAML frontmatter is present, `title` is extracted from the first
   `# ` heading line of the document body; if the document has no heading,
   `title` defaults to the file path.

5. `docs_url` defaults to the file path. YAML frontmatter with a `url` field
   overrides it.

6. Each document carries five metadata fields in the docstore:
   `filename`, `extension`, `file_path`, `title`, `docs_url`. Every chunk of
   a document inherits the document's metadata.

7. The BYOK tool uses the same embedding model
   (`sentence-transformers/all-mpnet-base-v2`), default chunk size (380
   tokens), default chunk overlap (0), and FAISS output format
   (`IndexFlatIP`) as the service expects. Customer indexes are
   interchangeable with product indexes from lightspeed-service's
   perspective.

8. The tool produces a container image archive (docker-archive format) at
   `/output/{tag}.tar`. The output image contains the vector DB at
   `/rag/vector_db/`. The archive is assembled in-process, without
   a container runtime (no buildah, no nested build): the output image is
   a baked base layer plus one data layer.

9. Node filtering (whitespace-only chunk checks applied in other pipelines)
   is NOT applied in BYOK. All chunks from the splitter are included in the
   index.

10. The output image contains only the vector DB, NOT the embedding model.
    lightspeed-service ships its own copy of the embedding model for query
    embedding.

## Configuration Surface — Environment Variables (Tool Container)

| Variable | Default | Purpose |
|---|---|---|
| `OUT_IMAGE_TAG` | `byok-image` | Tag for the output container image |
| `VECTOR_DB_INDEX` | `vector_db_index` | Index ID string |

## Configuration Surface — CLI Flags (`byok-go`)

| Flag | Default | Purpose |
|---|---|---|
| `-i` | `/markdown` | Input directory with markdown content |
| `-o` | (empty → `/output/$OUT_IMAGE_TAG.tar`) | Output image archive path |
| `-tag` | `byok-image` | Repository tag for the output image |
| `-id` | `vector_db_index` | Index ID string |
| `-model` | `/opt/byok` | Directory with `mpnet.onnx`, `tokenizer.json`, `cl100k_base.tiktoken`, `sentence_bert_config.json` |
| `-base-layer` | `/opt/byok/base-layer.tar` | Baked output base layer |
| `-threads` | `4` | ONNX Runtime intra-op threads |

## Constraints

1. The tool image runs as root (USER 0) — the tool writes directly to the
   mounted `/output` volume and needs no container runtime.

2. The output directory path is not sanitized against path traversal beyond
   what the CLI flags permit; the customer controls both mounts.

3. The customer must mount their Markdown content at `/markdown` and their
   output directory at `/output` when running the tool container.

## Planned Changes

- [PLANNED: OCPSTRAT-1494 Phase 2] Seamless one-click import from Git
  repositories and Confluence, replacing the manual container-based
  workflow.
- [PLANNED: OLS-1872] Internal web source integration for BYOK.
