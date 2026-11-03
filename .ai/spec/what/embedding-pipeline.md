# Embedding Pipeline

This spec defines the behavioral rules for the BYOK embedding pipeline:
chunking, embedding, vector store output, and the output-image format. The
implementation architecture is documented in `how/byok-pipeline.md`.

## Behavioral Rules — Chunking

1. Documents are split into chunks before embedding. The default chunk size
   is 380 tokens with 0 overlap. The budget is metadata-aware: the token
   count of the document's metadata string is subtracted from the chunk
   size (mirroring llama_index's `split_text_metadata_aware`).

2. Chunking mirrors llama_index's `SentenceSplitter`: split on paragraph
   separators, then punkt sentence boundaries, then phrase boundaries,
   recursing on oversized pieces, then greedily merging pieces up to the
   token budget. Chunks are verbatim text slices of the source document.

3. Chunk boundaries are token-counted with the `cl100k_base` tokenizer
   (llama_index's budget tokenizer), not the embedding model's WordPiece
   tokenizer.

4. A document whose metadata consumes the entire chunk budget is an error.

## Behavioral Rules — Embedding

5. Embeddings are generated with the ONNX export of
   `sentence-transformers/all-mpnet-base-v2`, producing 768-dimensional
   vectors, loaded from a local file. No model download ever occurs.

6. The model's maximum sequence length is read from
   `sentence_bert_config.json` in the model directory (default 384);
   inputs are truncated to it.

7. Texts are embedded in batches sorted by length to minimize padding.

8. Mean pooling with L2 normalization is applied, producing normalized
   embeddings as required by `IndexFlatIP`.

## Behavioral Rules — Vector Store Output

9. The vector store backend is FAISS `IndexFlatIP` (inner product
   similarity). Vectors are added in the same order as the docstore nodes.

10. The FAISS index is serialized with faiss's `write_index` format
    (byte-compatible with faiss-cpu v1.12.0 as used by the service).

11. The output directory follows llama-index-core's storage persistence
    format, as loaded by `FaissVectorStore.from_persist_dir`: the FAISS bytes under
    `default__vector_store.json` (raw faiss bytes under a `.json`-named
    file, replicating llama_index's quirk), plus `graph_store.json`,
    `index_store.json`, `docstore.json`, and an empty
    `image__vector_store.json`.

12. A `metadata.json` file is written alongside the index containing at
    minimum: execution time, embedding model name, index ID, vector DB type,
    embedding dimension, chunk size, chunk overlap, and total embedded
    files count.

13. Each index is identified by an index ID string (default
    `vector_db_index` for BYOK).

## Behavioral Rules — Metadata per Chunk

14. Each chunk stored in the vector index carries the document's metadata:
    `filename`, `extension`, `file_path`, `title`, `docs_url`.

15. Each docstore node records the chunk's source document ID, its own UUID,
    verbatim chunk text with character start/end offsets, and the source
    document's content hash.

## Behavioral Rules — Output Image

16. The output is a container image archive in the docker-archive
    (`docker save`) format: a JSON config (fixed epoch creation
    timestamp, amd64/linux) plus two layers — the baked ubi9-minimal base
    layer and a data layer containing `/rag/vector_db`.

17. The output image's config carries a minimal default env, `/bin/bash`
    as CMD, and the labels `name`, `description`, `io.k8s.description`,
    `io.k8s.display-name`, `io.openshift.tags`, and `summary`.

## Constraints

1. The embedding model used to build an index must be identical to the
   model used by lightspeed-service for query embedding. A model mismatch
   produces meaningless similarity scores.

2. FAISS indexes are loaded read-only by lightspeed-service. They must
   never be modified at runtime.

3. The llama-index storage persistence format and faiss serialization must stay
   compatible with the service's llama-index-core and faiss-cpu versions;
   the tool's faiss version is pinned to match the service's.
