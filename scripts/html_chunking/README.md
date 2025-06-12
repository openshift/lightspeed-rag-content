# HTML chunking library

This library provides an HTML chunker that splits single-page HTML documentation into semantically-aware chunks suitable for RAG.

## Core usage

The primary function is `chunk_html`. It takes an HTML string and returns a list of chunk objects, each with its own content and metadata.

```python
from html_chunking.chunker import chunk_html

# Assuming 'sample_html_content' is a string containing the HTML document
# and 'source_url' is the public URL of the document.
source_url = "https://docs.openshift.com/container-platform/4.18/html-single/monitoring/"
with open("path/to/your/document.html", "r", encoding="utf-8") as f:
    sample_html_content = f.read()

chunks = chunk_html(
    html_content=sample_html_content,
    source_url=source_url,
    max_token_limit=380,
    count_tag_tokens=True
)

# Process the resulting chunks
for i, chunk in enumerate(chunks):
    print(f"--- Chunk {i+1} ---")
    print(f"Source: {chunk.metadata.get('source')}")
    print(f"Content: {chunk.text[:100]}...")
```

### Parameters

| Name                | Type     | Description                                                                                             | Default |
| ------------------- | -------- | ------------------------------------------------------------------------------------------------------- | ------- |
| `html_content`      | `str`    | The raw HTML content to be chunked.                                                                     |         |
| `source_url`        | `str`    | The public source URL of the document, used for generating `source` metadata.                           |         |
| `max_token_limit`   | `int`    | The target maximum token limit for each chunk. The chunker will _try_ to keep chunks below this size.   | `380`   |
| `count_tag_tokens`  | `bool`   | If `True`, HTML tags are included in the token count.                                                   | `True`  |

### Return value

The function returns a list of `Chunk` objects. Each `Chunk` object has two attributes:

* **`text` (`str`)**: The HTML content of the chunk.
* **`metadata` (`dict`)**: A dictionary containing metadata about the chunk. It includes:
    * `source`: A URL pointing to the original document, appended with an HTML anchor (`#anchor-id`) that links directly to the section where the chunk originated.

## Standalone Example and Visual Report

Use `example.py` to run chunking on an example document and inspect the resulting chunks:

```bash
python example.py --max-token-limit=600 --output=limit-600.html
```
