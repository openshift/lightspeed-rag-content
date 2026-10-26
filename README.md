# lightspeed-rag-content

BYOK RAG tool for OpenShift Lightspeed: generates a FAISS vector database
from customer-supplied Markdown and packages it as a `podman load`-able
docker-archive. The output is consumed by the OLS service via
`llama-index-core` + `FaissVectorStore.from_persist_dir`.

Go implementation with ONNX Runtime for inference (mpnet embeddings) and
faiss for indexing (same v1.12.0 as the service, so serialized indexes are
byte-compatible).

## Usage

```bash
podman run --rm \
  -v <markdown_dir>:/markdown:Z \
  -v <output_dir>:/output:Z \
  -e OUT_IMAGE_TAG=my-byok-image \
  -e VECTOR_DB_INDEX=my-index \
  <tool-image>
```

Produces `<output_dir>/my-byok-image.tar` — a docker-archive containing
`/rag/vector_db` with the FAISS index.

## Development

```bash
make test           # pure-Go unit tests (no native libs needed)
make build          # build the binary (stages faiss + onnxruntime first)
make build-image    # build the container image from vendored artifacts
make test-native    # all tests incl. cgo packages
```

The six pure-Go packages (`tokenizer`, `counter`, `chunker`, `docparse`,
`persist`, `assemble`) test without any native libraries. The two cgo
packages (`embed`, `faissidx`) need faiss and onnxruntime staged via
`scripts/stage-go-native.sh`.

## Layout

```
cmd/byok-go/       — production binary
cmd/byok-go-dev/   — dev helpers (chunk dumps, query embeddings)
internal/tokenizer  — pure-Go WordPiece (exact Python parity)
internal/counter    — cl100k_base counting (llama_index's budget tokenizer)
internal/chunker    — SentenceSplitter-mirroring span chunker
internal/docparse   — markdown walk, frontmatter, metadata
internal/persist    — llama_index storage format emitters
internal/assemble   — docker-archive assembly without a container runtime
internal/embed      — onnxruntime cgo wrapper (mpnet inference)
internal/faissidx   — faiss C API cgo wrapper (byte-identical serialization)
model/              — mpnet.onnx as gzip chunks + tokenizer + ranks
third_party/        — faiss v1.12.0 source + onnxruntime 1.31.0 release
testdata/           — committed fixtures for unit tests
vendor/             — vendored Go modules
```

## Verified parity (2026-10-23, llama-index-core 0.14.23)

- **Tokenizer**: exact token-id parity with the transformers tokenizer
- **Embeddings**: cosine 1.00000000 against the torch reference
- **FAISS**: serialization byte-identical to `faiss::write_index`
- **Chunker**: 78% exact / 82% within-50-chars boundary match on real docs,
  median deviation 0, identical chunking on the e2e corpus
- **Persist format**: loads through llama-index; retrieval returns correct
  chunks with citation metadata
- **Batching**: measured net-negative for long-chunk CPU workloads;
  `BatchSize` defaults to 1 (see `internal/embed/embed.go`)

## License

Apache License 2.0
