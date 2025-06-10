# HTML Embeddings Pipeline

The pipeline has the following stages:

1. **Download** - Fetch HTML documentation from Red Hat's portal
2. **Strip** - Remove navigation, headers, and other ballast from HTML 
3. **Chunk** - Semantically chunk HTML content preserving document structure
4. **Process Runbooks** - Handle runbooks using existing Markdown logic
5. **Embed** - Generate embeddings and store in vector database

I've put them into separate files, which can be useful for e.g. running only a subset of stages:

```
scripts/html_embeddings/
├── generate_embeddings.py    # Main orchestrator script
├── download_docs.py          # Portal fetcher wrapper
├── strip_html.py             # HTML stripper wrapper
├── chunk_html.py             # HTML chunking wrapper
├── process_runbooks.py       # Runbooks processing
├── utils.py                  # Shared utilities
└── README.md                 # This file
```

## Usage

Standard:

```bash
# Generate embeddings for OpenShift 4.18
python scripts/html_embeddings/generate_embeddings.py \
  --version 4.18 \
  --output-dir ./vector_db \
  --model-dir ./embeddings_model
```

Specify custom index name instead of the auto-generated one:

```bash
# Generate embeddings for OpenShift 4.18
python scripts/html_embeddings/generate_embeddings.py \
  --version 4.18 \
  --output-dir ./vector_db \
  --index ocp-4.18 \
  --model-dir ./embeddings_model
```

Process only specific document and skip runbooks (good for quick testing):

```bash
# Process only monitoring documentation
python scripts/html_embeddings/generate_embeddings.py \
  --version 4.18 \
  --specific-doc observability_overview \
  --output-dir ./vector_db \
  --model-dir ./embeddings_model \
  --skip-runbooks
```

Use cached downloads:

```bash
# Use previously downloaded files
python scripts/html_embeddings/generate_embeddings.py \
  --version 4.18 \
  --use-cached-downloads \
  --output-dir ./vector_db \
  --model-dir ./embeddings_model
```

Set a custom token limit (default is the same 380 as in Markdown-based chunking):

```bash
# Set the token limit
python generate_embeddings.py \
  --version 4.18 \
  --chunk 380 \
  --output-dir ./vector_db \
  --model-dir ./embeddings_model
```

## CLI options

### Main arguments

- `--version` - OpenShift version (required, e.g., "4.18")
- `--index` - Index name (optional, e.g., "ocp-4.18")
- `--output-dir` - Vector DB output directory (default: "./vector_db")
- `--model-dir` - Embedding model directory (default: "./embeddings_model")

### Pipeline control

- `--specific-doc` - Process only specific document (e.g., "monitoring_apis")
- `--use-cached-downloads` - Use existing downloads instead of re-fetching
- `--skip-runbooks` - Skip runbooks processing
- `--cache-dir` - Directory for intermediate files (default: "./cache")
- `--continue-on-error` - Continue with cached data if a step fails

### HTML chunking parameters

- `--max-token-limit` - Maximum tokens per chunk (default: 380)
- `--count-tag-tokens` / `--no-count-tag-tokens` - Include/exclude HTML tags in token count

### Other options

- `--runbooks-dir` - Directory containing runbooks (default: "./runbooks")
- `--exclude-metadata` - Metadata to exclude during embedding
- `--chunk` - Chunk size (maps to --max-token-limit)
- `--verbose` - Enable verbose logging

## Pipeline stages

### 1. Download stage

Downloads HTML documentation from Red Hat's portal using the portal fetcher.

**Standalone usage:**
```bash
python scripts/html_embeddings/download_docs.py --version 4.18 --output-dir ./downloads
```

### 2. Strip stage

Removes navigation, headers, footers, and other non-content elements from HTML.

**Standalone usage:**
```bash
python scripts/html_embeddings/strip_html.py --input-dir ./downloads --output-dir ./stripped
```

### 3. Chunk stage

Semantically chunks HTML documents while preserving structure and context.

**Standalone usage:**
```bash
python scripts/html_embeddings/chunk_html.py --input-dir ./stripped --output-dir ./chunks --max-token-limit 380
```

### 4. Runbooks stage

Processes runbooks using the existing Markdown chunking logic.

**Standalone usage:**
```bash
python scripts/html_embeddings/process_runbooks.py --runbooks-dir ./runbooks --output-dir ./chunks
```

### 5. Embedding stage

Generates embeddings from all chunks and stores in vector database.

## Cache Structure

The pipeline creates a structured cache to avoid re-processing:

```
cache/
├── downloads/           # Raw HTML downloads
├── stripped/            # Stripped HTML
└── chunks/              # JSON chunk files
```

## Output Format

Chunks are saved as JSON files with the following structure:

```json
{
  "id": "monitoring_chunk_0001",
  "content": "<h2>Monitoring Overview</h2><p>...",
  "metadata": {
    "doc_name": "monitoring",
    "doc_id": "monitoring",
    "version": "4.18",
    "file_path": "monitoring/index.html",
    "doc_type": "openshift_documentation",
    "source": "https://docs.redhat.com/en/documentation/openshift_container_platform/4.18/html-single/monitoring/",
    "chunk_index": 1,
    "total_chunks": 45,
    "token_count": 375,
    "source_file": "monitoring/index.html",
  }
}
```
