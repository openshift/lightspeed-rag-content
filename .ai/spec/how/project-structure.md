# Project Structure -- Architecture

OpenShift LightSpeed RAG Content is organized into four areas: `lsc/` (installable Python library), `scripts/` (standalone pipeline scripts and utilities), `byok/` (BYOK tooling), and root-level build/config files. The project has no runtime component -- all code runs during build or development.

## Module Map

### `lsc/src/lightspeed_rag_content/` -- Installable Python library

| Path | Purpose |
|---|---|
| `document_processor.py` | `DocumentProcessor` class -- orchestrates document loading, chunking, embedding, and vector store persistence. Delegates to `_LlamaIndexDB` (FAISS/PostgreSQL) or `_LlamaStackDB` (llama-stack faiss/sqlite-vec). 836 lines. |
| `metadata_processor.py` | `MetadataProcessor` abstract base -- defines the `populate()` callback for LlamaIndex's `file_metadata` parameter. Subclasses implement `url_function()` to derive URLs from file paths. 100 lines. |
| `okp.py` | `OKPMetadataProcessor` -- parses TOML frontmatter from OKP/errata files. Helpers: `parse_metadata()`, `yield_files_related_to_projects()`, `is_file_related_to_projects()`, `metadata_has_url_and_title()`. 153 lines. |
| `utils.py` | `get_common_arg_parser()` -- shared CLI argument definitions (folder, model-dir, chunk, overlap, output, index, workers, vector-store-type, auto-chunking). 72 lines. |
| `asciidoc/asciidoctor_converter.py` | `AsciidoctorConverter` -- wraps the `asciidoctor` CLI for AsciiDoc format conversion. Supports custom Ruby converter extensions and per-version YAML attribute files. 160 lines. |
| `asciidoc/ruby_asciidoc/` | Ruby converter extensions for asciidoctor. `asciidoc_text_converter.rb` implements the custom text output format. |
| `asciidoc/__main__.py` | CLI entry point for AsciiDoc conversion. |

### `scripts/` -- Standalone pipeline scripts

| Path | Purpose |
|---|---|
| `generate_embeddings.py` | **Plaintext pipeline** -- loads OCP docs + runbooks, generates FAISS index. The script invoked by the production Containerfile. 248 lines. |
| `html_chunking/chunker.py` | Semantic HTML chunker -- splits HTML by DOM structure (sections, tables, lists, code blocks, definition lists). Generates anchor-aware metadata. 408 lines. |
| `html_chunking/tokenizer.py` | `count_html_tokens()` -- token counting for HTML content with optional tag token counting. |
| `html_chunking/parser.py` | HTML parsing utilities for the chunking library. |
| `html_chunking/test_chunker.py` | Unit tests for HTML chunking logic. |
| `html_embeddings/generate_embeddings.py` | **HTML pipeline** orchestrator -- 5-step pipeline: download, strip, chunk, runbooks, embed. Supports batch processing via config file. 659 lines. |
| `html_embeddings/download_docs.py` | `download_documentation()` -- fetches HTML docs from Red Hat documentation portal. |
| `html_embeddings/strip_html.py` | `strip_html_content()` -- removes non-content HTML (navigation, headers, footers, scripts, styles). |
| `html_embeddings/chunk_html.py` | `chunk_html_documents()` -- bridges the HTML chunking library to the embeddings pipeline. Manages per-document output directories and metadata extraction. 470 lines. |
| `html_embeddings/process_runbooks.py` | `process_runbooks()` -- converts Markdown runbooks to JSON chunk files for the HTML pipeline. |
| `html_embeddings/utils.py` | `setup_logging()`, `create_directory_structure()`, `validate_dependencies()`, `sanitize_directory_path()`. 264 lines. |
| `html_embeddings/test_html_embeddings.py` | Unit tests for the HTML embeddings pipeline. |
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
| `Containerfile` | Main RAG content image -- multi-stage build (builder, minimal). |
| `Makefile` | Developer-facing build automation (install-deps, update-docs, build-image, format, verify, etc.). |
| `pyproject.toml` | PDM project metadata. Dependencies, optional groups (cpu/gpu), ruff/mypy config. |
| `pdm.lock.cpu` / `pdm.lock.gpu` | PDM lockfiles per compute flavor. |
| `requirements.cpu.txt` / `requirements.gpu.txt` | Exported pip dependencies with hashes, generated by `pdm export`. |
| `requirements-build.txt` | Build-time pip dependencies for Cachi2. |
| `rpms.in.yaml` / `rpms.lock.yaml` | RPM dependency spec + lockfile for Cachi2 hermetic builds. |
| `artifacts.lock.yaml` | Pinned `model.safetensors` URL + SHA256 checksum. |
| `renovate.json` | Renovate bot config -- Python package auto-updates disabled. |
| `.gitleaks.toml` | Secret scanning configuration. |
| `.syft.yaml` | SBOM generation configuration. |
| `ubi.repo` / `cuda.repo` | DNF repository files for use inside container builds. |
| `OWNERS` | GitHub ownership: approvers list. |
| `CLAUDE.md` / `AGENTS.md` | Development guide for AI agents. |

## Dependency Management

**Package manager**: PDM (not pip/poetry). Two lockfiles exist per compute flavor:
- `pdm.lock.cpu` -- pins PyTorch CPU variant from `download.pytorch.org/whl/cpu`.
- `pdm.lock.gpu` -- pins standard PyTorch from PyPI.

**Makefile `FLAVOR` variable** (default: `cpu`): Maps to `TORCH_GROUP` which selects the lockfile and requirements file for all PDM operations.

**Core dependencies**: `llama-index-core`, `llama-index-vector-stores-faiss`, `llama-index-embeddings-huggingface`, `llama-index-readers-file`, `faiss-cpu`, `torch`, `huggingface-hub`, `accelerate`, `python-frontmatter`, `beautifulsoup4`, `aiohttp`, `PyYAML`, `urllib3`.

**Dev dependencies**: `black`, `mypy`, `ruff`, `types-requests`.

**Optional (not in pyproject.toml)**: `llama-stack-api`, `llama-stack-core`, `pgvector`, `psycopg` -- used by the lsc library for non-FAISS backends.

## Key Relationships

1. **Production Containerfile uses `scripts/generate_embeddings.py`**, not the lsc library. The lsc library is for downstream consumers and alternative backends.

2. **HTML pipeline is standalone** -- it does not share code with the plaintext pipeline or the lsc library. It has its own download, strip, chunk, and embed steps.

3. **Content acquisition scripts exist in both `scripts/` and `lsc/scripts/`**. The `lsc/` copies are the maintained versions; the `scripts/` copies are the originals used by the Containerfile and Makefile.

4. **The lsc library is an installable package** (`lsc/` contains its own `pyproject.toml` structure via the `src/` layout), but it is not published to PyPI. It is imported directly by downstream projects.

5. **Test infrastructure is minimal**: `scripts/html_chunking/test_chunker.py` and `scripts/html_embeddings/test_html_embeddings.py` use `unittest`. `scripts/verify_rag_image_test.py` verifies container image contents. No pytest configuration exists.
