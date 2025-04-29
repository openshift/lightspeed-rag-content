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
        count_tag_tokens=True,
        keep_siblings_together=True,
        prepend_parent_section_text=True
    )
"""

from .parser import parse_html, HtmlSection, identify_special_sections
from .tokenizer import count_tokens, count_html_tokens, set_custom_tokenizer, TokenCounter
from .chunker import chunk_html, ChunkingOptions

__all__ = [
    'chunk_html',
    'parse_html',
    'HtmlSection',
    'count_tokens',
    'count_html_tokens',
    'set_custom_tokenizer',
    'TokenCounter',
    'ChunkingOptions',
    'identify_special_sections'
]

__version__ = '1.0.0'
