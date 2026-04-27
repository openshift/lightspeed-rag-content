# HTML Pipeline -- Architecture

This spec documents the HTML-based embedding pipeline in `scripts/html_embeddings/` and the semantic chunking library in `scripts/html_chunking/`. This pipeline downloads HTML documentation from the Red Hat portal, strips non-content markup, performs semantic HTML chunking that preserves document structure and anchor IDs, and generates FAISS vector indexes.

## Module Map

| Path | Key Symbols |
|---|---|
| `scripts/html_embeddings/generate_embeddings.py` | `main()`, `setup_environment()`, `run_download_step()`, `run_strip_step()`, `run_chunk_step()`, `run_runbooks_step()`, `run_embedding_step()`, `load_chunks_as_nodes()` |
| `scripts/html_embeddings/download_docs.py` | `download_documentation()` |
| `scripts/html_embeddings/strip_html.py` | `strip_html_content()` |
| `scripts/html_embeddings/chunk_html.py` | `chunk_html_documents()`, `chunk_single_html_file()`, `extract_metadata_from_path()`, `validate_chunks()`, `get_chunking_stats()` |
| `scripts/html_embeddings/process_runbooks.py` | `process_runbooks()` |
| `scripts/html_embeddings/utils.py` | `setup_logging()`, `create_directory_structure()`, `validate_dependencies()`, `sanitize_directory_path()` |
| `scripts/html_chunking/chunker.py` | `chunk_html()`, `ChunkingOptions`, `Chunk`, `find_first_anchor()`, `get_document_title()`, `_split_element_by_children()`, `_split_element_by_children_no_grouping()`, `_split_table()`, `_split_list()`, `_split_code()`, `_split_definition_list()`, `_linear_split()`, `_get_anchored_url()` |
| `scripts/html_chunking/tokenizer.py` | `count_html_tokens()` |

## Data Flow -- 5-Step Pipeline

```
1. DOWNLOAD
   Input:  --doc-url | --doc-url-slug | --config-file
   Output: cache/{slug}/{version}/downloads/*.html
   Action: Fetch HTML pages from docs.redhat.com portal.
           Supports single URL, slug+version, or batch config file.

2. STRIP
   Input:  cache/{slug}/{version}/downloads/*.html
   Output: cache/{slug}/{version}/stripped/*.html
   Action: Remove non-content HTML (navigation, header, footer,
           scripts, styles). Preserve document body structure.

3. CHUNK
   Input:  cache/{slug}/{version}/stripped/*.html
   Output: cache/{slug}/{version}/chunks/{doc_name}/*_chunk_NNNN.json
   Action: Semantic HTML chunking → individual JSON chunk files.
           Each chunk carries metadata (docs_url, title, section_title,
           chunk_index, token_count).

4. RUNBOOKS
   Input:  --runbooks-dir (default: ./runbooks)
   Output: cache/{slug}/{version}/chunks/*.json (flat, at base level)
   Action: Convert Markdown runbooks to JSON chunk files.
           Stored flat (not in doc-specific subdirectories).

5. EMBED
   Input:  cache/{slug}/{version}/chunks/**/*.json
   Output: --output-dir containing FAISS index + metadata.json
   Action: Load JSON chunks as TextNode objects, create
           VectorStoreIndex, persist to output directory.
```

## Key Abstractions

### HTML Chunking Library (`scripts/html_chunking/`)

The chunker operates on parsed HTML DOM trees via BeautifulSoup. The algorithm is recursive and structure-aware.

**Entry point**: `chunk_html(html_content, source_url, max_token_limit, count_tag_tokens) -> list[Chunk]`

**Short-circuit**: If the entire document fits within `max_token_limit`, it is returned as a single chunk.

**Primary splitter**: `_split_element_by_children(element, options)` iterates over direct children of an HTML element, accumulating them into a chunk until the token limit is exceeded. Special grouping rules:
- **Sections with IDs**: Processed recursively after flushing the current chunk. Section context (ID) is tracked and wrapped around chunk content.
- **Headings** (h1-h6): Grouped with the following sibling element to keep heading + first content together.
- **Paragraphs ending with `:`**: Grouped with the following table, list, or definition list to keep introductory text + content together.
- **Oversized children**: Recursively split via `_split_element_by_children_no_grouping()`.

**Secondary splitter**: `_split_element_by_children_no_grouping(element, options)` accumulates children without grouping heuristics. Delegates to specialized splitters for structured elements:
- `_split_table(table, options)` -- Splits by rows, preserving `<thead>` header in every chunk. Oversized rows are split by cells.
- `_split_list(list_element, options)` -- Splits `<ol>`/`<ul>` by `<li>` items, preserving list wrapper tags and attributes. Oversized items are recursively split.
- `_split_code(pre_element, options)` -- Splits `<pre>` blocks by lines, preserving wrapper tag and attributes.
- `_split_definition_list(div_element, options)` -- Splits `<div class="variablelist">` by `<dt>`/`<dd>` pairs, preserving wrapper structure.

**Fallback**: `_linear_split(html_content, options)` -- last-resort character-based splitting using a 3.5 characters-per-token ratio estimate. Emits a warning when used.

### Anchor and Section Tracking

After chunking, a stateful post-processing pass assigns metadata:
- `last_seen_anchor` -- Most recent HTML element ID encountered across chunks. Persists across chunk boundaries so chunks without IDs inherit the previous anchor.
- `last_heading_text` -- Most recent heading text, used for `section_title` metadata.
- `chapter_anchor` -- Set when an `h2` heading is encountered. Used to build two-level anchored URLs.

### URL Construction

`_get_anchored_url(source_url, my_id, parent_id)` builds deep-linked URLs:
- Replaces `/html-single/` with `/html/` in the source URL and strips trailing `/`.
- If no anchor ID: returns the source URL as-is.
- With anchor ID: `{source_url}/{parent_id}#{my_id}` (if parent_id present) or `{source_url}/{my_id}`.

### Chunk Intermediate Format

Each chunk is persisted as a JSON file:
```json
{
  "id": "{doc_id}_chunk_0001",
  "content": "<html content>",
  "metadata": {
    "docs_url": "https://docs.redhat.com/.../monitoring#my-section",
    "title": "Monitoring",
    "section_title": "Configuring alerting rules",
    "chunk_index": 1,
    "total_chunks": 42,
    "token_count": 350,
    "source_file": "monitoring/index.html",
    "doc_name": "monitoring",
    "doc_id": "monitoring",
    "version": "4.18",
    "doc_type": "openshift_container_platform_documentation"
  }
}
```

### Input Source Resolution

Three mutually exclusive input methods:
- `--doc-url` -- A full URL to a documentation page. Slug and version are parsed from the URL path. Supports both Red Hat documentation format (`/documentation/{lang}/{slug}/{version}/...`) and arbitrary URLs.
- `--doc-url-slug` + `--doc-url-version` -- Product slug (e.g., `openshift_container_platform`) with explicit version. If the slug looks like a URL, it is parsed to extract the actual slug.
- `--config-file` -- YAML or JSON file with a `products` list, each containing `slug`/`version` or `url`. Enables batch processing of multiple products in one invocation.

### Pipeline Step Functions

Each step follows a consistent pattern:
```python
def run_{step}_step(args, paths, [product,] logger) -> bool:
```
Returns `True` on success, `False` on failure. The main loop checks return values and either continues (with `--continue-on-error`) or aborts.

## Integration Points

### html_chunking → html_embeddings

`chunk_html.py` imports from the chunking library via `sys.path.insert`:
```python
sys.path.insert(0, str(Path(__file__).parent.parent / "html_chunking"))
from chunker import chunk_html, Chunk
from tokenizer import count_html_tokens
```
This is not a proper package import -- it relies on filesystem adjacency.

### chunks → embeddings

`load_chunks_as_nodes(chunks_dir, logger)` reads all `*.json` files (excluding `*_summary.json`) from the chunks directory, constructs `TextNode` objects from each chunk's `content`, `metadata`, and `id`, and returns them for indexing.

## Implementation Notes

- The HTML pipeline operates on HTML content throughout -- HTML tags are preserved in chunks and counted toward the token budget by default. The `--no-count-tag-tokens` flag excludes HTML tags from token counting.

- The pipeline writes intermediate results to a cache directory structure (`cache/{slug}/{version}/{step}/`), enabling `--use-cached-downloads` to skip re-fetching. Each step can be run independently if its inputs exist.

- `--continue-on-error` allows the pipeline to proceed past failed steps using data from previous runs. This is useful for iterative development.

- The embedding step does NOT apply the whitespace filter used by the plaintext pipeline. All loaded chunks are embedded.

- Runbook chunks are stored as flat JSON files in the base chunks directory (not in doc-specific subdirectories). This is how `run_embedding_step` distinguishes them from doc chunks when `--specific-doc` is used: doc chunks are in subdirectories, runbooks are at the base level.

- `chunk_html_documents()` writes a `chunking_summary.json` alongside the chunks with statistics: total files, processed files, total chunks, and chunking parameters.

- `validate_chunks()` provides optional post-hoc validation with a 10% tolerance on chunk token size. Undersized chunks are those below 10% of max_token_limit.

- The `extract_metadata_from_path()` function derives `doc_name`, `doc_id`, `version`, and `doc_type` from the file's relative path within the cache directory. Version is extracted via regex matching path components against `^\d+\.\d+(\.\d+)?$`.

- Logging outputs to both stdout and a `html_embeddings.log` file.
