# Project Structure -- Architecture

OpenShift LightSpeed RAG Content is organized into three areas: `scripts/` (pipeline scripts and utilities), `byok/` (BYOK tooling), and root-level build/config files. The project has no runtime component -- all code runs during build or development.

> **Note:** The `lsc/` directory (installable Python library for the llamastack-faiss pipeline) has been removed. OCP docs are now served by OKP via the RHOKP sidecar.

## Module Map

### `scripts/` -- Pipeline scripts

| Path | Purpose |
|---|---|
| `generate_embeddings.py` | **Plaintext pipeline** -- loads OCP docs + runbooks, generates FAISS index. The script invoked by the production Containerfile. 248 lines. |
| `html_chunking/chunker.py` | Semantic HTML chunker -- splits HTML by DOM structure (sections, tables, lists, code blocks, definition lists). Generates anchor-aware metadata. 408 lines. |
| `html_chunking/tokenizer.py` | `count_html_tokens()` -- token counting for HTML content with optional tag token counting. |
| `html_chunking/parser.py` | HTML parsing utilities for the chunking library. |
| `html_chunking/test_chunker.py` | Unit tests for HTML chunking logic. |
| `html_chunking/example.py` | Example usage of the HTML chunking library. |
| `html_chunking/html-stripper.py` | Standalone HTML stripping utility. |
| `html_embeddings/generate_embeddings.py` | **HTML pipeline** orchestrator -- 5-step pipeline: download, strip, chunk, runbooks, embed. Supports batch processing via config file. 659 lines. |
| `html_embeddings/download_docs.py` | `download_documentation()` -- fetches HTML docs from Red Hat documentation portal. |
| `html_embeddings/strip_html.py` | `strip_html_content()` -- removes non-content HTML (navigation, headers, footers, scripts, styles). |
| `html_embeddings/chunk_html.py` | `chunk_html_documents()` -- bridges the HTML chunking library to the embeddings pipeline. Manages per-document output directories and metadata extraction. 470 lines. |
| `html_embeddings/process_runbooks.py` | `process_runbooks()` -- converts Markdown runbooks to JSON chunk files for the HTML pipeline. |
| `html_embeddings/utils.py` | `setup_logging()`, `create_directory_structure()`, `validate_dependencies()`, `sanitize_directory_path()`. 264 lines. |
| `html_embeddings/test_html_embeddings.py` | Unit tests for the HTML embeddings pipeline. |
| `html_embeddings/setup.py` | Package setup for the HTML embeddings pipeline. |
| `doc_downloader/downloader.py` | Red Hat documentation HTML downloader -- fetches pages from a starting URL, preserving directory structure. |
| `asciidoctor-text/convert-it-all.py` | Bulk AsciiDoc-to-plaintext conversion using topic maps. Reads `_topic_map.yml`, filters by distribution, and converts each referenced `.adoc` file. |
| `asciidoctor-text/text-converter.rb` | Ruby text format converter extension for asciidoctor. |
| `get_ocp_plaintext_docs.sh` | Clones openshift-docs for a given version, runs AsciiDoc conversion, applies exclusions from `config/exclude.conf`. |
| `get_runbooks.sh` | Sparse-checkout of `alerts/` directory from openshift/runbooks repo. Removes README files, empty dirs, deprecated dirs. |
| `query_rag.py` | Debug utility -- loads a persisted FAISS index and retrieves top-k similar nodes for a query. |
| `distance.py` | Debug utility -- computes cosine + euclidean distance between two text embeddings. |
| `iterate_docstore.py` | Debug utility -- dumps all nodes from a vector DB's docstore.json. |
| `download_embeddings_model.py` | Downloads the embedding model from HuggingFace via `snapshot_download()`. Removes unneeded files (pytorch_model.bin, onnx/, openvino/). |
| `generate_packages_to_prefetch.py` | Generates Cachi2-compatible requirements files for hermetic builds. Complex: strips torch, handles CPU wheel separately, computes hashes. |
| `verify_rag_image_test.py` | Integration test -- verifies container image has `/rag/vector_db/{version}/index_store.json` and `/rag/embeddings_model/config.json`. |

### `byok/` -- BYOK tooling

| Path | Purpose |
|---|---|
| `generate_embeddings_tool.py` | BYOK embedding generator -- simplified pipeline for customer Markdown. Uses `FlatReader` and YAML frontmatter parsing. 128 lines. |
| `Containerfile.tool` | BYOK tool container definition (buildah + Python + model + script). |
| `Containerfile.output` | BYOK output container template (vectors only, built inside the tool container). |
| `README.md` | BYOK usage documentation: environment variables, frontmatter format, examples. |

### `config/` -- Content configuration

| Path | Purpose |
|---|---|
| `exclude.conf` | Newline-delimited list of relative file paths to exclude from OCP docs after AsciiDoc conversion. |

### `ocp-product-docs-plaintext/` -- Committed OCP documentation

Contains plaintext-converted OCP documentation organized by version (`4.16/` through `4.22/`). Each version directory preserves the category structure from openshift-docs (e.g., `applications/`, `architecture/`, `authentication/`, `backup_and_restore/`, etc.).

### `runbooks/` -- Committed alert runbooks

Contains Markdown runbooks organized under `alerts/` with operator-specific subdirectories (e.g., `cluster-etcd-operator/`, `cluster-dns-operator/`, `openshift-virtualization-operator/`).

### `embeddings_model/` -- Sentence-transformer model

Contains the `sentence-transformers/all-mpnet-base-v2` model files (`config.json`, `tokenizer.json`, `vocab.txt`, `1_Pooling/` config). The `model.safetensors` binary is not committed -- it is downloaded at build time or fetched from Cachi2.

### Root-level build and config files

| Path | Purpose |
|---|---|
| `Containerfile` | RAG content image -- multi-stage build (builder, minimal). CPU-only. |
| `Makefile` | Developer-facing build automation (install-deps, update-docs, build-image, format, verify, etc.). |
| `pyproject.toml` | Project metadata. Dependencies, optional groups (cpu), ruff/mypy config. |
| `requirements.hashes.source.cpu.txt` | Hashed PyPI source dependencies for Cachi2. |
| `requirements.hashes.wheel.cpu.txt` | Hashed RHOAI wheel dependencies for Cachi2. |
| `requirements-build.cpu.txt` | Build-time pip dependencies for Cachi2. |
| `requirements.hermetic.txt` | Bootstrap deps (pip) for hermetic builds. |
| `requirements.overrides.txt` | Version pins for uv compilation. |
| `rpms.in.yaml` / `rpms.lock.yaml` | RPM dependency spec + lockfile for Cachi2 hermetic builds. |
| `artifacts.lock.yaml` | Pinned `model.safetensors` URL + SHA256 checksum. |
| `.gitleaks.toml` | Secret scanning configuration. |
| `.syft.yaml` | SBOM generation configuration. |
| `OWNERS` | GitHub ownership: approvers list. |
| `CLAUDE.md` / `AGENTS.md` | Development guide for AI agents. |

## Dependency Management

**Package manager**: uv for compilation, pip for installation. CPU-only builds.

**Lockfile generation**: `scripts/konflux_requirements.sh` compiles `pyproject.toml` with uv using dual-index strategy (RHOAI wheels first, then PyPI). Produces split hashed lockfiles for Cachi2 prefetch.

**Core dependencies**: `llama-index-core`, `llama-index-vector-stores-faiss`, `llama-index-embeddings-huggingface`, `llama-index-readers-file`, `faiss-cpu`, `torch` (RHOAI CPU wheel), `huggingface-hub`, `accelerate`, `python-frontmatter`, `beautifulsoup4`, `aiohttp`, `PyYAML`, `urllib3`.

**Dev dependencies**: `black`, `mypy`, `ruff`, `types-requests`.

## Key Relationships

1. **Production Containerfile uses `scripts/generate_embeddings.py`** for embedding generation.

2. **HTML pipeline is standalone** -- it does not share code with the plaintext pipeline. It has its own download, strip, chunk, and embed steps.

3. **Test infrastructure is minimal**: `scripts/html_chunking/test_chunker.py` and `scripts/html_embeddings/test_html_embeddings.py` use `unittest`. `scripts/verify_rag_image_test.py` verifies container image contents. No pytest configuration exists.
