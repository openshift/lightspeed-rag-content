# OpenShift Lightspeed RAG Content (Go) — Development Guide for AI

## Overview

BYOK RAG tool: generates a FAISS vector database from customer-supplied
Markdown and packages it as a `podman load`-able docker-archive. Go
implementation with ONNX Runtime for inference and faiss for indexing.

## Commands

```bash
make build          # build the binary (stages native libs first)
make build-image    # build the container image from vendored artifacts
make test           # pure-Go unit tests (no native libraries needed)
make test-native    # all tests incl. cgo packages
make format         # gofmt
make lint           # gofmt check
```

## Conventions

- Go 1.26, `gofmt` formatting, no external linters
- Internal packages under `internal/`, binary under `cmd/`
- Native libraries (faiss, onnxruntime) are cgo; pure-Go packages are
  testable without them (`make test`)
- Vendored Go modules (`vendor/`) — no network needed for `go build`
- The embedding model ships as gzip chunks in `model/` (regenerate with
  `make model-chunks MODEL=...`)
- Third-party sources (faiss v1.12.0, onnxruntime 1.31.0) are vendored in
  `third_party/` for hermetic builds

## Git and PR Workflow

### Commit Messages
- Start with the Jira ticket reference: `OLS-XXXX: description`
- Keep the first line under 72 characters
- Use imperative mood

### Pull Requests
This repo uses a **fork-based workflow**:

1. **Push to your fork**, not to `origin` (openshift/lightspeed-rag-content)
2. **Create the PR** against `origin/main` using your fork's branch
3. **PR title** must start with the Jira reference
4. **Squash commits** before pushing
