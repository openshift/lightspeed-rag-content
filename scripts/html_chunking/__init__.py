"""
HTML Chunking Package

This package splits HTML content into chunks based on semantic boundaries.

Main functions:
    chunk_html - Split HTML content into chunks with semantic boundaries

Example:
    from html_chunking import chunk_html
    
    html_content = "<h1>Title</h1><p>Content</p>..."
    chunks = chunk_html(
        html_content,
        max_token_limit=500,
        count_tag_tokens=True
    )
"""

from .parser import HtmlSection, parse_html, identify_special_sections
from .tokenizer import TokenCounter, count_html_tokens, count_tokens, set_custom_tokenizer
from .chunker import ChunkingOptions, chunk_html

__all__ = [
    "chunk_html",
    "parse_html",
    "HtmlSection",
    "count_tokens",
    "count_html_tokens",
    "set_custom_tokenizer",
    "TokenCounter",
    "ChunkingOptions",
    "identify_special_sections",
]

__version__ = '1.0.0'
