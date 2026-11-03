# BYOK Pipeline

This spec describes the end-to-end data flow through the tool, as
orchestrated by `cmd/byok-go/main.go`. The behavioral rules it implements
are in `what/byok.md` and `what/embedding-pipeline.md`.

## Pipeline Phases

### 1. Setup (`cmd/byok-go/main.go`)

- Parses CLI flags; applies defaults from flags → env (`OUT_IMAGE_TAG`,
  `VECTOR_DB_INDEX`) → constants (`byok-image`, `vector_db_index`,
  `/output/{tag}.tar`).
- Loads the WordPiece tokenizer from `{model}/tokenizer.json`.
- Creates the embedder: onnxruntime session over `{model}/mpnet.onnx`,
  embedding dim 768, max sequence length read from
  `{model}/sentence_bert_config.json` (default 384), intra-op threads from
  `-threads`.
- Loads the cl100k_base token counter from
  `{model}/cl100k_base.tiktoken`.

### 2. Document loading (`internal/docparse`)

- `LoadDocuments(dir)` walks the input directory for `.md` files.
- `newDocument` parses optional YAML frontmatter (`title`, `url`), falls
  back to first `# ` heading for `title`, and defaults both `title` and
  `docs_url` to the file path.
- Each document exposes ordered metadata
  (`filename`, `extension`, `file_path`, `title`, `docs_url`), a metadata
  string (llama_index `get_metadata_str` equivalent — its token count
  reduces the chunk budget), and a metadata map (docstore form).

### 3. Chunking (`internal/chunker`, `internal/counter`)

- Per document: effective chunk budget = 380 − tokens(metadataStr);
  error if ≤ 0.
- `ChunkDocument` mirrors llama_index's `SentenceSplitter`: split on
  paragraph separator → punkt sentences (embedded `english.json` training
  data via `github.com/neurosnap/sentences`) → phrase regex → recursive
  split of oversized pieces → greedy merge under budget. Chunks are
  verbatim slices with rune-index start/end offsets.
- Each chunk becomes a `persist.Node`: fresh UUID, ref-doc UUID, text,
  start/end, document metadata map, and the document's sha256 content hash.

### 4. Embedding (`internal/embed`)

- `EmbedBatch(texts)` sorts texts by length to minimize padding, encodes
  each with the WordPiece tokenizer (truncated to max sequence length),
  runs the onnxruntime session, then mean-pools and L2-normalizes each
  output into a 768-dim vector.

### 5. Indexing (`internal/faissidx`)

- `NewFlatIPIndex(768)` creates a FAISS IndexFlatIP via the C API; `Add`
  appends the vectors in node order; `Serialize` returns faiss
  `write_index` bytes (byte-compatible with faiss v1.12.0 / the service's
  faiss-cpu).

### 6. Persistence (`internal/persist`)

- `PersistDir(dir, nodes, faissBytes, indexID)` writes the llama_index
  storage persistence file set into a temp `vector_db/` directory:
  - `default__vector_store.json` — **raw faiss bytes** under a
    `.json`-named file (replicating llama_index's quirk so
    `FaissVectorStore.from_persist_dir` loads it).
  - `graph_store.json`, `index_store.json`, `docstore.json`, and an
    empty `image__vector_store.json` — real JSON in llama-index-core
    0.14.x layout.
- `WriteToolMetadata` writes `metadata.json` (execution time, model name,
  index ID, vector DB type, embedding dim, chunk size, overlap, file
  count).

### 7. Output assembly (`internal/assemble`)

- `AssembleOutput(dest, tag, baseLayerPath, dataDir)`:
  - tars the vector DB directory as a single data layer rooted at
    `rag/vector_db` (sorted entries, epoch mtimes, root ownership);
  - reads the baked ubi-minimal base layer shipped in the image;
  - builds the OCI image config (amd64/linux, epoch creation, minimal env,
    `/bin/bash` CMD, BYOK labels) and a docker-archive-format manifest
    (`manifest.json` with `Config`/`RepoTags`/`Layers`) with
    sha256 layer digests;
  - writes the archive to the output path.

## Error Handling

Any phase failure prints `ERROR: <err>` to stderr and exits 1. The tool
never writes partial output: the archive is assembled in memory/temp and
written once at the end.

## Dev Binary (`cmd/byok-go-dev`)

Parity/validation helpers not shipped in the image: dumps document chunks
(JSON with text/start/end) and embeds single query texts for validation
harnesses. Links the same internal packages including cgo.
