# lsc Library -- Architecture

This spec documents the `lsc/src/lightspeed_rag_content/` installable Python library -- the most recent and most capable pipeline implementation, supporting multiple vector store backends (FAISS, PostgreSQL, llama-stack faiss, llama-stack sqlite-vec).

## Module Map

| Path | Key Symbols |
|---|---|
| `lsc/src/lightspeed_rag_content/document_processor.py` | `DocumentProcessor`, `_Config`, `_BaseDB`, `_LlamaIndexDB`, `_LlamaStackDB` |
| `lsc/src/lightspeed_rag_content/metadata_processor.py` | `MetadataProcessor` (abstract base) |
| `lsc/src/lightspeed_rag_content/okp.py` | `OKPMetadataProcessor`, `parse_metadata()`, `yield_files_related_to_projects()`, `is_file_related_to_projects()`, `metadata_has_url_and_title()` |
| `lsc/src/lightspeed_rag_content/utils.py` | `get_common_arg_parser()` |
| `lsc/src/lightspeed_rag_content/asciidoc/asciidoctor_converter.py` | `AsciidoctorConverter` |

## Class Hierarchy

```
DocumentProcessor              Public API. Owns a _Config and a _BaseDB subclass.
  │
  ├── _Config                  Attribute-bag for keyword args (dynamic __getattr__).
  │
  └── _BaseDB                  Abstract base. Initializes LlamaIndex Settings.
       │                       Provides _got_whitespace(), _filter_out_invalid_nodes(),
       │                       _split_and_filter().
       │
       ├── _LlamaIndexDB       FAISS and PostgreSQL backends via LlamaIndex.
       │                       Accumulates nodes in _good_nodes list.
       │                       save() creates VectorStoreIndex and writes metadata.json.
       │
       └── _LlamaStackDB       llama-stack faiss and sqlite-vec backends.
                                Accumulates documents/chunks in self.documents list.
                                save() writes YAML config, runs async llama-stack client,
                                updates config with vector_store_id.
```

## Data Flow -- DocumentProcessor Lifecycle

```
1. __init__(chunk_size, chunk_overlap, model_name, embeddings_model_dir,
            vector_store_type, manual_chunking, doc_type, ...)
   ├── Create _Config bag from kwargs
   ├── Validate config via _check_config():
   │     - Warn if manual_chunking=False with faiss (not supported)
   │     - Warn if table_name set for non-postgres backend
   ├── Set HF_HOME = embeddings_model_dir, TRANSFORMERS_OFFLINE = "1"
   └── Instantiate DB backend via _get_db():
         "faiss" or "postgres"           → _LlamaIndexDB(config)
         "llamastack-faiss/sqlite-vec"   → _LlamaStackDB(config)

2. process(docs_dir, metadata, required_exts, file_extractor,
           unreachable_action, ignore_list)
   ├── Create SimpleDirectoryReader with metadata.populate as file_metadata
   ├── Load documents: reader.load_data(num_workers=config.num_workers)
   ├── If unreachable_action != "warn":
   │     ├── Separate ignore-listed docs from checkable docs
   │     ├── Filter checkable docs by url_reachable == True
   │     ├── If unreachable found:
   │     │     "fail" → raise RuntimeError
   │     │     "drop" → keep only reachable + ignored docs
   │     └── Merge reachable + ignored back into docs
   ├── db.add_docs(docs) → split, filter, accumulate
   └── Increment _num_embedded_files by len(docs)

   (process() can be called multiple times to accumulate docs from
    multiple sources before a single save())

3. save(index, output_dir)
   ├── Calculate exec_time = int(time.time() - start_time)
   └── db.save(index, output_dir, _num_embedded_files, exec_time)
```

## _LlamaIndexDB Internals

### Initialization

```python
def __init__(self, config):
    super().__init__(config)  # Configures Settings: chunk_size, chunk_overlap,
                               # embed_model, llm=None, node_parser

    # Compute embedding dimension dynamically
    config.embedding_dimension = len(
        Settings.embed_model.get_text_embedding("random text")
    )

    # Create vector store
    if config.vector_store_type == "faiss":
        faiss_index = faiss.IndexFlatIP(config.embedding_dimension)
        vector_store = FaissVectorStore(faiss_index=faiss_index)

    elif config.vector_store_type == "postgres":
        # All Postgres config from environment variables:
        # POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST,
        # POSTGRES_PORT, POSTGRES_DATABASE
        vector_store = PGVectorStore.from_params(...)

    self.storage_context = StorageContext.from_defaults(vector_store=vector_store)
    self._good_nodes = []
```

### Document Processing

`add_docs(docs)` splits documents via `Settings.text_splitter`, filters out nodes without whitespace (via `_filter_out_invalid_nodes`), and appends valid nodes to `_good_nodes`.

### Persistence

`save()` creates a `VectorStoreIndex` from accumulated `_good_nodes`, sets the index ID, persists the storage context, and writes `metadata.json` with:
- `execution-time`, `llm` ("None"), `embedding-model`, `index-id`
- `vector-db` ("faiss.IndexFlatIP" or "PGVectorStore")
- `embedding-dimension`, `chunk`, `overlap`, `total-embedded-files`

## _LlamaStackDB Internals

### Initialization

```python
def __init__(self, config):
    super().__init__(config)  # Settings configuration

    # Resolve model path (absolute for directories, name for repos)
    if os.path.exists(config.embeddings_model_dir):
        self.model_name_or_dir = os.path.realpath(config.embeddings_model_dir)
    else:
        self.model_name_or_dir = config.model_name

    # Compute embedding dimension via SentenceTransformer
    model = SentenceTransformer(self.model_name_or_dir)
    config.embedding_dimension = model.get_sentence_embedding_dimension()

    # Database filename: "faiss_store.db" or "sqlitevec_store.db"
    self.db_filename = config.vector_store_type[11:] + "_store.db"

    # Create temp dir, set LLAMA_STACK_CONFIG_DIR to prevent
    # using host's ~/.llama content
    self.tmp_dir = tempfile.TemporaryDirectory(prefix="ls-rag-")
    os.environ["LLAMA_STACK_CONFIG_DIR"] = self.tmp_dir.name

    # Deferred imports of llama_stack (not in pyproject.toml deps)
    import llama_stack_api
    from llama_stack.core.library_client import AsyncLlamaStackAsLibraryClient
```

### Document Accumulation

`add_docs(docs)` behaves differently based on `manual_chunking`:

**Manual chunking** (`manual_chunking=True`, the default):
- Splits documents via `_split_and_filter()` (same as _LlamaIndexDB).
- Converts each node to a dict with: `content`, `metadata` (including `document_id`), `chunk_metadata` (document_id, chunk_id, source), and `chunk_id`.

**Auto chunking** (`manual_chunking=False`):
- Wraps each document as a `RAGDocument` object with: `document_id`, `content`, `mime_type="text/plain"`, `metadata`.
- No splitting is performed -- llama-stack handles chunking at upload time.

### Persistence

`save()` orchestrates the llama-stack workflow:
1. Create output directory.
2. Compute paths: db_file, files_metadata_db_file, cfg_file.
3. Write YAML config from `TEMPLATE` via `write_yaml_config()`.
4. Run `asyncio.run(_run_llama_stack(cfg_file, index))`.
5. Update YAML with the created vector_store_id via `_update_yaml_config()`.

### Manual Chunking Path (`_insert_prechunked_documents`)

```
1. Create vector store:
   client.vector_stores.create(name=index, provider_id=index,
     embedding_model="sentence-transformers/{model}",
     embedding_dimension=dim)

2. Group chunks by source document ID → doc_groups dict

3. Upload placeholder files per source document (concurrent):
   For each doc group:
     - Create empty BytesIO file
     - client.files.create(file=file_obj, purpose="assistants")
     - Update all chunks in group with uploaded file's ID
   All uploads via asyncio.gather()

4. Compute embeddings per chunk:
   For each chunk:
     - client.embeddings.create(input=content, model=embedding_model)
     - Build chunk dict with content, metadata, embedding, etc.

5. Batch insert:
   client.vector_io.insert(vector_store_id=vs.id, chunks=all_chunks)
```

### Auto Chunking Path (`_upload_and_process_files`)

```
For each RAGDocument (sequential, one at a time):
  1. Upload file: client.files.create(file=BytesIO(content), purpose="assistants")
  2. Attach to vector store: client.vector_stores.files.create(
       vector_store_id, file_id, attributes=metadata,
       chunking_strategy={type: "static", max_chunk_size_tokens, chunk_overlap_tokens})
  3. Poll for completion (up to 5 minutes, 0.5s interval):
       client.vector_stores.files.retrieve() until status in
       ("completed", "failed", "cancelled")
  4. On failure: retry up to 3 times with 1s backoff
  5. After all retries exhausted: add to failed_docs list

If any files failed: raise RuntimeError
```

### YAML Config Template

The `TEMPLATE` class variable generates a complete llama-stack configuration file:
- **APIs**: files, tool_runtime, vector_io, inference
- **Providers**: `sentence-transformers` for inference, `localfs` for files, `rag-runtime` for tool_runtime, configurable provider for vector_io (faiss or sqlite-vec)
- **Storage**: SQLite backends for metadata, KV store, and SQL store. The KV store path (`kv_db_path`) points to the output database file.
- **Registered model**: Embedding model with dimension and provider mapping.

After vector store creation, `_update_yaml_config()` replaces `vector_stores: []` with the actual vector store section containing dimension, model, provider ID, and store ID.

## MetadataProcessor Contract

```python
class MetadataProcessor(ABC):
    def __init__(self, hermetic_build: bool)

    def populate(self, file_path: str) -> dict:
        # Returns {"docs_url": str, "title": str, "url_reachable": bool}
        # Calls url_function() for URL, get_file_title() for title,
        # ping_url() for reachability (skipped if hermetic_build=True)

    def get_file_title(self, file_path: str) -> str:
        # Reads first line, strips "\n" and leading "# "

    def ping_url(self, url: str, retries: int = 3) -> bool:
        # HTTP GET with 30s timeout, retries on failure or non-200

    @abstractmethod
    def url_function(self, file_path: str) -> str:
        # Subclass implements: derive source URL from file path
```

### OKPMetadataProcessor

Subclass for OKP/errata files. Overrides both `url_function` and `get_file_title`:
- `url_function()`: Parses TOML frontmatter, returns `metadata["extra"]["reference_url"]`.
- `get_file_title()`: Parses TOML frontmatter, returns `metadata["title"]`.

Supporting functions:
- `parse_metadata(filepath)` -- Reads file, extracts TOML between `+++` markers via regex, parses with `tomllib`.
- `yield_files_related_to_projects(directory, projects)` -- Yields paths of `.md` files in directory whose `portal_product_names` match any of the given project names (case-insensitive substring match).
- `is_file_related_to_projects(metadata, projects)` -- Returns `True` if any project name is a substring of any product name in the metadata.
- `metadata_has_url_and_title(metadata)` -- Returns `True` if `reference_url` exists in `extra` and `title` is non-empty.

## AsciidoctorConverter

Wraps the `asciidoctor` CLI binary:
- Default target format: `"text"`, using the custom Ruby converter at `ruby_asciidoc/asciidoc_text_converter.rb`.
- Built-in asciidoctor formats (`html5`, `xhtml5`, `manpage`) use no custom converter file.
- Attribute files (YAML) are read and converted to `-a key=value` CLI arguments.
- `convert(source_file, destination_file)` runs `subprocess.run(command, check=True, capture_output=True)`. Creates destination directories if needed.
- Constructor validates that `asciidoctor` is on PATH via `shutil.which()`.
- Custom converter files are located via `importlib.resources.files()` relative to the package.

## Implementation Notes

- `_Config` uses a private `__attributes` dict with `__getattr__`/`__setattr__` overrides rather than `self.__dict__` updates. The mangled name `_Config__attributes` is handled specially in `__setattr__` via `super().__setattr__()`. This pattern avoids polluting the instance namespace and helps with type checking.

- `_BaseDB.__init__` sets `Settings.node_parser = MarkdownNodeParser()` when `doc_type` is `"markdown"` or `"html"`. This is because LlamaIndex's `HTMLReader` converts HTML to Markdown internally, so both content types benefit from Markdown-aware node parsing.

- `_LlamaStackDB` has a documented limitation: it can only work once per instance. The YAML config file and database files in the temp directory are not cleaned up between runs. Creating a second index would require a new `DocumentProcessor` instance.

- `DocumentProcessor._check_config()` warns but does not fail when `manual_chunking=False` is passed with FAISS (`auto_chunking` only works with llama-stack), or when `table_name` is set for non-Postgres backends.

- The `process()` method can be called multiple times before `save()`. This is the intended pattern for combining docs from multiple sources (e.g., OCP docs + runbooks) into a single index.

- `_LlamaStackDB` uses deferred imports (`import llama_stack_api` inside `__init__`) because llama-stack packages are not in the project's core `pyproject.toml` dependencies. They are optional, only needed when using llama-stack backends.

- The `TEMPLATE` uses double-brace `{{}}` for literal braces in the YAML output since it uses Python's `str.format()` for interpolation.

- PostgreSQL configuration for `_LlamaIndexDB` is read entirely from environment variables (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DATABASE`), not from `_Config`. This means Postgres config cannot be passed via CLI arguments.

- The `_LlamaStackDB` placeholder file upload pattern (uploading empty files for citation metadata) exists because llama-stack's citation system needs a `file_id` to link chunks back to source documents. The actual content is in the chunks, not the files.
