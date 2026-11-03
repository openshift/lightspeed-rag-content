# lightspeed-rag-content

BYOK RAG tool for OpenShift Lightspeed: generates a FAISS vector database
from customer-supplied Markdown and packages it as a `podman load`-able
container image archive (docker-archive format). The output is consumed
by the OLS service via
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

Produces `<output_dir>/my-byok-image.tar` — a container image archive
(docker-archive format) containing `/rag/vector_db` with the FAISS index.

## How the output image is assembled

The output image archive is assembled in pure Go by `internal/assemble` —
no container runtime, no registry access, and no privileges are needed on
the customer's machine. The trick is that the customer image's base
filesystem is captured once, when the tool's own image is built:

```
Containerfile (tool build, in Konflux)       byok-go (customer runtime)
──────────────────────────────────────       ─────────────────────────
ubi9/ubi-minimal (pulled by digest,
  pinned in the OUTPUT_BASE_IMAGE ARG)
        │ COPY --from=output-base /
        ▼
/base-rootfs/ (directory)
        │ tar --sort=name --mtime=@0
        │   --numeric-owner --owner=0 --group=0
        ▼
/opt/byok/base-layer.tar ──────────────► -base-layer flag ──► embedded as
  (shipped inside the tool image)             the bottom layer of the
                                               customer's output tar
```

At customer runtime, `byok-go` stacks two layers into the archive: the
baked base layer plus one data layer holding `/rag/vector_db` (the llama_index
persist file set from `internal/persist`, tarred by
`internal/assemble`). The image config and manifest are emitted directly,
with epoch timestamps and sorted tar entries.

The Go code never refers to ubi-minimal or to any image — it only sees an
opaque `layer.tar` behind the `-base-layer` flag. This indirection is what
replaced the original Python pipeline's buildah build-and-push step (which
needed a container runtime and a registry pull at customer runtime). Note
that the base layer is fixed at tool-build time: it only refreshes when the
tool image is rebuilt with a new `OUTPUT_BASE_IMAGE` digest.

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
internal/assemble   — container image archive assembly without a container runtime
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
