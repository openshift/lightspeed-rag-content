# Embedding Pipeline

This spec defines the shared behavioral rules that all pipeline implementations (plaintext, HTML, lsc library) must satisfy. Individual pipeline architectures are documented in the corresponding `how/` specs.

## Behavioral Rules -- Chunking

1. Documents must be split into chunks before embedding. The default chunk size is configurable via CLI with a default of 380 tokens and 0 overlap.

2. Plaintext documents use LlamaIndex's default sentence splitter (`SentenceSplitter`), which splits on sentence boundaries and respects the configured chunk size and overlap.

3. Markdown and HTML documents may use LlamaIndex's `MarkdownNodeParser` for section-aware splitting. This parser splits on Markdown heading boundaries, producing one node per section.

4. HTML documents may alternatively use a semantic chunking algorithm that respects HTML DOM structure -- splitting at section, table, list, code block, and definition list boundaries -- and preserves HTML anchor IDs for deep-link metadata generation.

5. Chunks consisting entirely of non-whitespace characters (containing no spaces, tabs, or newlines) must be filtered out as invalid. This catches degenerate chunks produced from non-textual content.

## Behavioral Rules -- Embedding

6. Embeddings are generated using a HuggingFace-compatible sentence-transformer model loaded from a local filesystem directory.

7. The default embedding model is `sentence-transformers/all-mpnet-base-v2`, producing 768-dimensional vectors. The model must be redistributable under an Apache 2.0 compatible license. [PLANNED: OLS-1729 -- fine-tuned embedding models]

8. The embedding dimension is determined dynamically at initialization by encoding a probe string through the model, not hardcoded. This ensures correctness regardless of which model is loaded.

9. The environment variables `HF_HOME` and `TRANSFORMERS_OFFLINE=1` must be set before loading the model to prevent runtime model downloads and direct HuggingFace Hub to the local model directory.

10. The LLM setting must be explicitly set to `None` (via `resolve_llm(None)`) to prevent LlamaIndex from attempting to load a language model, which is not needed for embedding generation.

## Behavioral Rules -- Vector Store Output

11. The primary vector store backend is FAISS using `IndexFlatIP` (inner product similarity). `IndexFlatIP` requires normalized vectors; the sentence-transformers model produces normalized embeddings by default.

12. Alternative backends are supported by the lsc library: PostgreSQL via `PGVectorStore`, llama-stack with faiss, and llama-stack with sqlite-vec.

13. Each index is identified by an index ID string. For OCP product docs, the convention is `ocp-product-docs-{version}` with dots replaced by underscores (e.g., `ocp-product-docs-4_19`).

14. FAISS indexes persisted via LlamaIndex produce a directory containing: `docstore.json`, `index_store.json`, `graph_store.json`, `vector_store.json`.

15. A `metadata.json` file must be written alongside the index containing at minimum: execution time, embedding model name, index ID, vector DB type, embedding dimension, chunk size, chunk overlap, and total embedded files count.

16. llama-stack backends produce a `llama-stack.yaml` configuration file and a provider-specific database file (`faiss_store.db` or `sqlitevec_store.db`) instead of the LlamaIndex JSON files.

## Behavioral Rules -- Index Organization

17. Each OCP version gets its own index in a separate directory: `vector_db/ocp_product_docs/{version}/`.

18. A `latest` symlink must be created pointing to the highest version directory, determined by version-aware sorting.

19. Runbook embeddings are merged into each OCP version index -- they are combined with OCP doc nodes into a single index, not stored separately.

## Behavioral Rules -- Metadata per Chunk

20. Each chunk stored in the vector index must carry metadata including at minimum: `docs_url` (source URL) and `title` (document title).

21. For HTML pipeline chunks, additional metadata is carried: `section_title` (nearest heading text), `chunk_index` (position within the source document), `total_chunks` (total chunks from that document), `token_count` (tokens in the chunk), and `source_file` (relative path to the source file).

22. For llama-stack backends, `document_id` must also be present in chunk metadata to support the citation linking mechanism.

## Configuration Surface

| CLI Argument | Default | Purpose |
|---|---|---|
| `--folder` / `-f` | (required) | Input document directory |
| `--model-dir` / `-md` | `embeddings_model` | Path to the HuggingFace-compatible embedding model directory |
| `--model-name` / `-mn` | (none) | HuggingFace repo ID of the embedding model (for metadata recording) |
| `--chunk` / `-c` | `380` | Chunk size in tokens |
| `--overlap` / `-l` | `0` | Chunk overlap in tokens |
| `--output` / `-o` | (required) | Vector DB output directory |
| `--index` / `-i` | (required) | Index ID string |
| `--vector-store-type` | `faiss` | Backend: `faiss`, `postgres`, `llamastack-faiss`, `llamastack-sqlite-vec` |
| `--auto-chunking` | `False` | Delegate chunking to llama-stack runtime (lsc library only) |
| `--hermetic-build` / `-hb` | `False` | Skip URL reachability checks |
| `--workers` / `-w` | `None` | Number of workers for parallel document loading |

## Constraints

1. The embedding model used to build an index must be identical to the model used by lightspeed-service for query embedding. A model mismatch produces meaningless similarity scores.

2. FAISS indexes are loaded read-only by lightspeed-service. They must never be modified at runtime.

3. The `--auto-chunking` flag only applies to llama-stack backends. FAISS always uses manual (pre-split) chunking.

4. PostgreSQL backend configuration is read from environment variables (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DATABASE`), not CLI arguments.

## Planned Changes

- [PLANNED: OLS-1729] Embedding model fine-tuning -- generate domain-specific vocabulary from OCP docs and augment the embedding model's vocabulary corpus.
- [PLANNED: OLS-2294] Add metadata generation stage -- add a dedicated metadata generation/enrichment step to the pipeline.
- [PLANNED: OLS-2903] OKP-based RAG -- integrate OKP (OpenShift Knowledge Platform) errata content.
