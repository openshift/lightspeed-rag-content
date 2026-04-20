# Plaintext Pipeline -- Architecture

This spec documents the implementation of `scripts/generate_embeddings.py` -- the production pipeline invoked by the main Containerfile to generate FAISS vector indexes from pre-converted plaintext OCP documentation and Markdown runbooks.

## Module Map

| Path | Key Symbols |
|---|---|
| `scripts/generate_embeddings.py` | `ocp_file_metadata_func()`, `runbook_file_metadata_func()`, `file_metadata_func()`, `ping_url()`, `get_file_title()`, `got_whitespace()`, `str2bool()` |

## Data Flow

```
CLI args parsed
  │
  ├── Set module-level globals:
  │     OCP_DOCS_VERSION, HERMETIC_BUILD,
  │     EMBEDDINGS_ROOT_DIR (abs path to docs folder),
  │     RUNBOOKS_ROOT_DIR (abs path to runbooks folder)
  │
  ├── Configure LlamaIndex Settings:
  │     Settings.chunk_size = args.chunk (default 380)
  │     Settings.chunk_overlap = args.overlap (default 0)
  │     Settings.embed_model = HuggingFaceEmbedding(model_name=args.model_dir)
  │     Settings.llm = resolve_llm(None)
  │
  ├── Compute embedding dimension: len(embed_model.get_text_embedding("random text"))
  │
  ├── Create FAISS index: faiss.IndexFlatIP(embedding_dimension)
  │     └── Wrap in FaissVectorStore → StorageContext
  │
  ├── Load OCP docs:
  │     SimpleDirectoryReader(args.folder, recursive=True,
  │                           file_metadata=ocp_file_metadata_func)
  │     └── ocp_file_metadata_func builds docs_url:
  │           OCP_DOCS_ROOT_URL + version + relative_path(.txt→.html)
  │
  ├── Split into nodes:
  │     Settings.text_splitter.get_nodes_from_documents(documents)
  │
  ├── Filter: keep only TextNode with whitespace in text
  │     → good_nodes list
  │
  ├── Load runbooks:
  │     SimpleDirectoryReader(args.runbooks, recursive=True,
  │                           required_exts=[".md"],
  │                           file_extractor={".md": FlatReader()},
  │                           file_metadata=runbook_file_metadata_func)
  │     └── runbook_file_metadata_func builds docs_url:
  │           RUNBOOKS_ROOT_URL + relative_path
  │
  ├── Split runbook nodes, append to good_nodes
  │     (no whitespace filter applied to runbook nodes)
  │
  ├── Create VectorStoreIndex(good_nodes, storage_context)
  │     → triggers embedding generation for all nodes
  │
  ├── Set index ID: index.set_index_id(args.index)
  │
  ├── Persist: index.storage_context.persist(persist_dir=PERSIST_FOLDER)
  │     → writes docstore.json, index_store.json, graph_store.json, vector_store.json
  │
  └── Write metadata.json with execution metrics
```

## Key Abstractions

### Metadata functions

`file_metadata_func(file_path, docs_url_func)` is the generic metadata populator. It:
1. Calls `docs_url_func(file_path)` to derive the URL.
2. Calls `get_file_title(file_path)` to extract the title from the first line.
3. Optionally calls `ping_url(docs_url)` if `HERMETIC_BUILD` is false.
4. Returns `{"docs_url": docs_url, "title": title}`.

`ocp_file_metadata_func(file_path)` and `runbook_file_metadata_func(file_path)` are thin wrappers that pass a URL-builder lambda to `file_metadata_func`.

### URL construction

- **OCP docs**: `https://docs.openshift.com/container-platform/{OCP_DOCS_VERSION}/{relative_path}.html`
  - `relative_path` = `file_path` with `EMBEDDINGS_ROOT_DIR` prefix stripped and `.txt` suffix replaced with `.html`.
- **Runbooks**: `https://github.com/openshift/runbooks/blob/master/alerts/{relative_path}`
  - `relative_path` = `file_path` with `RUNBOOKS_ROOT_DIR` prefix stripped.

### Node filtering

`got_whitespace(text)` iterates character-by-character and returns `True` if any character is whitespace. Only `TextNode` instances passing this check are included in `good_nodes`. This filters out degenerate chunks (e.g., single tokens without spaces).

## Implementation Notes

- `UNREACHABLE_DOCS` is a module-level global counter incremented via the `global` keyword. Not thread-safe, but the script is single-threaded.

- OCP docs and runbooks are loaded separately but merged into a single `good_nodes` list before index creation, producing one combined FAISS index per OCP version.

- Runbook nodes bypass the whitespace filter -- they are appended directly after splitting via `good_nodes.extend(runbook_nodes)`.

- `FlatReader()` is used for `.md` files to prevent LlamaIndex's default Markdown parser from interpreting structure. This treats Markdown as raw plaintext, preserving headings and formatting characters in the chunk text.

- The output directory is sanitized via `os.path.normpath("/" + args.output).lstrip("/")` to prevent path traversal (fix for OLS-823).

- `str2bool(value)` exists because Python's `bool("False")` returns `True`. The function handles string representations of booleans for the `--hermetic-build` argument, accepting: `true/false`, `yes/no`, `on/off`, `1/0`, `t/f`, `y/n`.

- The script runs as `__main__` only -- it has no importable API. All logic is in the `if __name__ == "__main__":` block.

- Metadata recorded in `metadata.json` includes `"llm": "None"` (string, not null) because no LLM is used during embedding generation.

- The Containerfile invokes this script once per OCP version in a shell loop:
  ```
  for OCP_VERSION in $(ls -1 ocp-product-docs-plaintext); do
      python3.11 generate_embeddings.py \
          -f ocp-product-docs-plaintext/${OCP_VERSION} \
          -r runbooks/alerts \
          -md embeddings_model \
          -mn ${EMBEDDING_MODEL} \
          -o vector_db/ocp_product_docs/${OCP_VERSION} \
          -i ocp-product-docs-$(echo $OCP_VERSION | sed 's/\./_/g') \
          -v ${OCP_VERSION} \
          -hb $HERMETIC
  done
  ```
