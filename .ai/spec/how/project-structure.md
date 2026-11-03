# Project Structure

This spec describes how the lightspeed-rag-content codebase is organized:
directory layout, package map, and key relationships.

## Directory Layout

```
cmd/byok-go/          — production binary: CLI, pipeline orchestration
cmd/byok-go-dev/      — dev helpers: chunk dumps, single-text query
                        embeddings for parity/validation harnesses (not
                        shipped in the image)
internal/tokenizer/   — pure-Go WordPiece tokenizer (mpnet tokenizer.json,
                        exact Python parity)
internal/counter/     — cl100k_base token counting (llama_index's budget
                        tokenizer)
internal/chunker/     — SentenceSplitter-mirroring span chunker (punkt
                        sentences via github.com/neurosnap/sentences)
internal/docparse/    — markdown discovery, YAML frontmatter, metadata
                        extraction
internal/persist/     — llama_index storage-format emitters (docstore,
                        index/vector/graph stores, metadata.json, UUIDs,
                        content hashes)
internal/embed/       — onnxruntime cgo wrapper (mpnet inference, mean
                        pooling, L2 normalization, batched embedding)
internal/faissidx/    — faiss C API cgo wrapper (IndexFlatIP, add,
                        serialize — byte-identical serialization)
internal/assemble/    — container image archive (docker-archive format)
                        assembly without a container runtime
                        (layers, manifest, config)
model/                — mpnet.onnx as gzip chunks + tokenizer.json +
                        cl100k_base.tiktoken + sentence_bert_config.json
third_party/          — git submodules: faiss v1.12.0 source, onnxruntime
                        v1.31.0 source + FetchContent deps, OpenBLAS v0.3.29
testdata/             — committed fixtures for unit tests
vendor/               — vendored Go modules (build with -mod=vendor)
scripts/              — stage-go-native.sh (local cgo build staging),
                        setup-ort-deps.sh (FetchContent overrides)
tests/integration-konflux/ — BYOK customer-workflow e2e scenario
.tekton/              — Konflux pipelines + integration-test scenario
Containerfile         — multi-stage tool image build
Makefile              — build / test / lint / model-chunks targets
rpms.in.yaml, rpms.lock.yaml — RPM dependencies for the native build stage
```

## Package Map

| Package | Native deps? | Responsibility |
|---|---|---|
| `internal/tokenizer` | no | WordPiece tokenization of input text for mpnet |
| `internal/counter` | no | cl100k_base token counting for chunk budgets |
| `internal/chunker` | no | SentenceSplitter-equivalent text splitting |
| `internal/docparse` | no | file discovery + metadata extraction |
| `internal/persist` | no | llama_index persist file set + metadata.json |
| `internal/assemble` | no | container image archive (docker-archive format) writing |
| `internal/embed` | **cgo** (onnxruntime) | mpnet inference |
| `internal/faissidx` | **cgo** (faiss) | FAISS index + serialization |

## Key Relationships

- `cmd/byok-go` orchestrates the pipeline:
  `docparse → chunker (budget via counter) → embed → faissidx → persist → assemble`.
- `chunker` depends on `counter` (token budgets) and embeds its punkt
  training data (`english.json`).
- `persist` depends on `docparse` types (Document metadata ordering must
  match llama_index's insertion order for parity).
- `embed` depends on `tokenizer` (WordPiece input encoding).
- `cmd/byok-go-dev` reuses `docparse`/`chunker`/`counter`/`embed` for
  parity measurements; it links cgo and is not shipped.

## Testing

- Pure-Go packages test with `make test` (CGO_ENABLED=0) — no native
  libraries needed.
- All packages including cgo test with `make test-native` after staging
  faiss + onnxruntime via `scripts/stage-go-native.sh`.
- `make lint` checks gofmt across non-vendored sources.
- `tests/integration-konflux/` holds the BYOK customer-workflow e2e
  scenario (Python validation script + fictional corpus).

## Conventions

- Go 1.26, gofmt formatting, no external linters.
- Internal packages under `internal/`, binaries under `cmd/`.
- Vendored modules; no network needed for `go build`.
- Commits and PRs start with `OLS-XXXX`; fork-based workflow (see AGENTS.md).
