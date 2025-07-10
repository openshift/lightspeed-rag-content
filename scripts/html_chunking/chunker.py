"""
HTML chunker module.

This module splits HTML content into chunks based on semantic boundaries.
"""

from typing import Any, Optional
from dataclasses import dataclass
from bs4 import BeautifulSoup, Tag, NavigableString
import warnings

from .tokenizer import count_html_tokens

# Constants
DEFAULT_CHARS_PER_TOKEN_RATIO = 3.5

@dataclass
class ChunkingOptions:
    max_token_limit: int = 500
    count_tag_tokens: bool = True

@dataclass
class Chunk:
    """A dataclass to hold a chunk's text and its associated metadata."""
    text: str
    metadata: dict[str, Any]


def find_first_anchor(chunk_soup: BeautifulSoup) -> Optional[str]:
    """Finds the first ID attribute from a significant tag in a soup object."""
    for tag_name in ["section", "div", "h1", "h2", "h3", "h4", "h5", "h6"]:
        first_tag = chunk_soup.find(tag_name, id=True)
        if first_tag:
            return first_tag.get('id')
    first_tag_with_id = chunk_soup.find(id=True)
    if first_tag_with_id:
        return first_tag_with_id.get('id')
    return None


def get_document_title(soup: BeautifulSoup) -> str:
    """Extracts the document title from the <title> tag."""
    title_tag = soup.find('title')
    return title_tag.get_text(strip=True) if title_tag else "Untitled"


def chunk_html(
    html_content: str,
    source_url: str,
    max_token_limit: int = 500,
    count_tag_tokens: bool = True,
    **kwargs
) -> list[Chunk]:
    """
    Chunks the given HTML content and generates metadata with source URLs and anchors.

    Args:
        html_content: The HTML content to be chunked.
        source_url: The original public URL of the HTML document.
        max_token_limit: The maximum number of tokens allowed per chunk.
        count_tag_tokens: Whether to count HTML tags as tokens.

    Returns:
        A list of Chunk objects, each containing text and metadata.
    """
    options = ChunkingOptions(
        max_token_limit=max_token_limit,
        count_tag_tokens=count_tag_tokens
    )

    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        document_title = get_document_title(soup)

        if count_html_tokens(html_content, options.count_tag_tokens) <= options.max_token_limit:
            metadata = {
                "docs_url": source_url,
                "title": document_title,
                "section_title": document_title
            }
            return [Chunk(text=html_content, metadata=metadata)]
    except Exception as e:
        warnings.warn("Could not pre-calculate total tokens: %s. Proceeding with chunking." % e)
        document_title = "Untitled"

    try:
        body = soup.body or soup
        string_chunks = _split_element_by_children(body, options)
    except Exception as e:
        warnings.warn("A critical error occurred during semantic chunking: %s. Falling back to linear splitting." % e)
        string_chunks = _linear_split(html_content, options)

    # Post-process string chunks to add stateful anchor and title metadata
    final_chunks = []
    last_seen_anchor = None
    last_heading_text = document_title

    for s_chunk in string_chunks:
        if not s_chunk.strip():
            continue
        
        chunk_soup = BeautifulSoup(s_chunk, 'html.parser')
        current_anchor = find_first_anchor(chunk_soup)
        
        if current_anchor:
            last_seen_anchor = current_anchor
            
        final_anchor = last_seen_anchor
        
        chunk_headings = chunk_soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        if chunk_headings:
            last_heading_text = chunk_headings[-1].get_text(strip=True)

        section_title = last_heading_text

        full_source_url = f"{source_url}#{final_anchor}" if final_anchor else source_url
        metadata = {
            "docs_url": full_source_url,
            "title": document_title,
            "section_title": section_title
        }
        final_chunks.append(Chunk(text=s_chunk, metadata=metadata))

    if not final_chunks:
        metadata = {
            "docs_url": source_url,
            "title": document_title,
            "section_title": document_title
        }
        return [Chunk(text=html_content, metadata=metadata)]

    return final_chunks


def _split_element_by_children(element: Tag, options: ChunkingOptions) -> list[str]:
    chunks, current_chunk_elements, current_tokens = [], [], 0
    children = [child for child in element.children if not (isinstance(child, NavigableString) and not child.strip())]
    
    i = 0
    while i < len(children):
        child, processed_elements = children[i], 1
        child_html = str(child)
        
        is_heading = isinstance(child, Tag) and child.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        is_p_tag = isinstance(child, Tag) and child.name == 'p'
        
        if is_heading and i + 1 < len(children):
            child_html += str(children[i+1])
            processed_elements = 2
        elif is_p_tag and child.get_text(strip=True).endswith(':') and i + 1 < len(children):
            next_child = children[i+1]
            if isinstance(next_child, Tag) and (next_child.name in ['table', 'rh-table', 'ol', 'ul'] or ('class' in next_child.attrs and 'variablelist' in next_child.attrs['class'])):
                child_html += str(next_child)
                processed_elements = 2
        
        try:
            child_tokens = count_html_tokens(child_html, options.count_tag_tokens)
            is_oversized = child_tokens > options.max_token_limit
        except Exception:
            child_tokens, is_oversized = options.max_token_limit + 1, True

        if is_oversized:
            if current_chunk_elements: chunks.append("".join(current_chunk_elements))
            root_to_split = BeautifulSoup(child_html, 'html.parser').body or BeautifulSoup(child_html, 'html.parser')
            chunks.extend(_split_element_by_children_no_grouping(root_to_split, options))
            current_chunk_elements, current_tokens = [], 0
        elif current_chunk_elements and current_tokens + child_tokens > options.max_token_limit:
            chunks.append("".join(current_chunk_elements))
            current_chunk_elements, current_tokens = [child_html], child_tokens
        else:
            current_chunk_elements.append(child_html)
            current_tokens += child_tokens
        
        i += processed_elements
            
    if current_chunk_elements: chunks.append("".join(current_chunk_elements))
    return chunks

def _split_element_by_children_no_grouping(element: Tag, options: ChunkingOptions) -> list[str]:
    chunks, current_chunk_elements, current_tokens = [], [], 0
    children = [child for child in element.children if not (isinstance(child, NavigableString) and not child.strip())]
    
    for child in children:
        child_html = str(child)
        try:
            child_tokens = count_html_tokens(child_html, options.count_tag_tokens)
            is_oversized = child_tokens > options.max_token_limit
        except Exception:
            child_tokens, is_oversized = options.max_token_limit + 1, True

        if is_oversized:
            if current_chunk_elements: chunks.append("".join(current_chunk_elements))
            if isinstance(child, Tag):
                if child.name in ['table', 'rh-table']: chunks.extend(_split_table(child, options))
                elif child.name in ['ol', 'ul']: chunks.extend(_split_list(child, options))
                elif child.name == 'pre': chunks.extend(_split_code(child, options))
                elif child.name == 'div' and 'class' in child.attrs and 'variablelist' in child.attrs['class']: chunks.extend(_split_definition_list(child, options))
                else: chunks.extend(_split_element_by_children_no_grouping(child, options))
            else: chunks.extend(_linear_split(child_html, options))
            current_chunk_elements, current_tokens = [], 0
            continue
        
        if current_chunk_elements and current_tokens + child_tokens > options.max_token_limit:
            chunks.append("".join(current_chunk_elements))
            current_chunk_elements, current_tokens = [child_html], child_tokens
        else:
            current_chunk_elements.append(child_html)
            current_tokens += child_tokens
    
    if current_chunk_elements: chunks.append("".join(current_chunk_elements))
    return chunks

def _split_definition_list(div_element: Tag, options: ChunkingOptions) -> list[str]:
    dl = div_element.find('dl')
    if not dl: return _split_element_by_children(div_element, options)
    chunks, current_chunk_pairs_html, current_tokens = [], [], 0
    pairs, children, i = [], list(dl.children), 0
    while i < len(children):
        child = children[i]
        if isinstance(child, Tag) and child.name == 'dt':
            term_html = str(child)
            def_html = ""
            if i + 1 < len(children) and isinstance(children[i+1], Tag) and children[i+1].name == 'dd':
                def_html = str(children[i+1]); i += 1
            pairs.append(term_html + def_html)
        i += 1
    for pair_html in pairs:
        pair_tokens = count_html_tokens(pair_html, options.count_tag_tokens)
        if current_chunk_pairs_html and current_tokens + pair_tokens > options.max_token_limit:
            chunks.append(f'<div class="variablelist"><dl>{"".join(current_chunk_pairs_html)}</dl></div>')
            current_chunk_pairs_html, current_tokens = [pair_html], pair_tokens
        else:
            current_chunk_pairs_html.append(pair_html); current_tokens += pair_tokens
    if current_chunk_pairs_html: chunks.append(f'<div class="variablelist"><dl>{"".join(current_chunk_pairs_html)}</dl></div>')
    return chunks if chunks else [str(div_element)]

def _split_table(table: Tag, options: ChunkingOptions) -> list[str]:
    chunks, header = [], table.find('thead')
    rows = table.find_all('tr')
    header_rows_ids = set(id(r) for r in header.find_all('tr')) if header else set()
    body_rows = [row for row in rows if id(row) not in header_rows_ids]
    table_attrs = " ".join([f'{k}="{v}"' for k, v in table.attrs.items()])
    table_open, table_close = f"<table {table_attrs}>", "</table>"
    header_html = str(header) if header else ""
    base_tokens = count_html_tokens(table_open + header_html + table_close, options.count_tag_tokens)
    current_chunk_rows, current_tokens = [], base_tokens
    for row in body_rows:
        row_html, row_tokens = str(row), count_html_tokens(str(row), options.count_tag_tokens)
        if row_tokens + base_tokens > options.max_token_limit:
            if current_chunk_rows: chunks.append(table_open + header_html + "".join(current_chunk_rows) + table_close)
            chunks.extend(_split_oversized_row(row, table_open, header_html, table_close, options))
            current_chunk_rows, current_tokens = [], base_tokens
            continue
        if current_chunk_rows and (current_tokens + row_tokens > options.max_token_limit):
            chunks.append(table_open + header_html + "".join(current_chunk_rows) + table_close)
            current_chunk_rows, current_tokens = [row_html], base_tokens + row_tokens
        else:
            current_chunk_rows.append(row_html); current_tokens += row_tokens
    if current_chunk_rows: chunks.append(table_open + header_html + "".join(current_chunk_rows) + table_close)
    return chunks if chunks else [str(table)]

def _split_oversized_row(row: Tag, table_open: str, header_html: str, table_close: str, options: ChunkingOptions) -> list[str]:
    row_chunks, cells = [], row.find_all(['td', 'th'], recursive=False)
    cell_sub_chunks = [_split_element_by_children(cell, options) for cell in cells]
    max_len = max(len(c) for c in cell_sub_chunks) if cell_sub_chunks else 0
    if max_len == 0: return [table_open + header_html + str(row) + table_close]
    for i in range(max_len):
        new_row_html = "<tr>"
        for j, cell in enumerate(cells):
            cell_tag, cell_attrs = cell.name, " ".join([f'{k}="{v}"' for k, v in cell.attrs.items()])
            content = cell_sub_chunks[j][i] if i < len(cell_sub_chunks[j]) else ""
            new_row_html += f"<{cell_tag} {cell_attrs}>{content}</{cell_tag}>"
        new_row_html += "</tr>"
        row_chunks.append(table_open + header_html + new_row_html + table_close)
    return row_chunks

def _split_list(list_element: Tag, options: ChunkingOptions) -> list[str]:
    chunks, items = [], list_element.find_all('li', recursive=False)
    list_attrs = " ".join([f'{k}="{v}"' for k, v in list_element.attrs.items()])
    list_open, list_close = f"<{list_element.name} {list_attrs}>", f"</{list_element.name}>"
    base_tokens = count_html_tokens(list_open + list_close, options.count_tag_tokens)
    current_chunk_items, current_tokens = [], base_tokens
    for item in items:
        item_html, item_tokens = str(item), count_html_tokens(str(item), options.count_tag_tokens)
        if item_tokens + base_tokens > options.max_token_limit:
            if current_chunk_items: chunks.append(list_open + "".join(current_chunk_items) + list_close)
            item_soup = BeautifulSoup(item_html, 'html.parser').li
            if item_soup:
                 sub_chunks = _split_element_by_children(item_soup, options)
                 for sub_chunk in sub_chunks: chunks.append(list_open + f"<li>{sub_chunk}</li>" + list_close)
            else: chunks.append(list_open + item_html + list_close)
            current_chunk_items, current_tokens = [], base_tokens
            continue
        if current_chunk_items and (current_tokens + item_tokens > options.max_token_limit):
            chunks.append(list_open + "".join(current_chunk_items) + list_close)
            current_chunk_items, current_tokens = [item_html], base_tokens + item_tokens
        else:
            current_chunk_items.append(item_html); current_tokens += item_tokens
    if current_chunk_items: chunks.append(list_open + "".join(current_chunk_items) + list_close)
    return chunks if chunks else [str(list_element)]

def _split_code(pre_element: Tag, options: ChunkingOptions) -> list[str]:
    chunks, code_text = [], pre_element.get_text()
    lines = code_text.split('\n')
    attrs = " ".join([f'{k}="{v}"' for k, v in pre_element.attrs.items()])
    open_tag, close_tag = f"<pre {attrs}>", "</pre>"
    base_tokens = count_html_tokens(open_tag + close_tag, options.count_tag_tokens)
    current_chunk_lines, current_tokens = [], base_tokens
    for line in lines:
        line_tokens = count_html_tokens(line + '\n', options.count_tag_tokens)
        if current_chunk_lines and current_tokens + line_tokens > options.max_token_limit:
            chunks.append(open_tag + "\n".join(current_chunk_lines) + close_tag)
            current_chunk_lines, current_tokens = [line], base_tokens + line_tokens
        else:
            current_chunk_lines.append(line); current_tokens += line_tokens
    if current_chunk_lines: chunks.append(open_tag + "\n".join(current_chunk_lines) + close_tag)
    return chunks if chunks else [str(pre_element)]

def _linear_split(html_content: str, options: ChunkingOptions) -> list[str]:
    warnings.warn("Using linear character split as a fallback for an oversized, indivisible chunk.")
    chars_per_chunk = int(options.max_token_limit * DEFAULT_CHARS_PER_TOKEN_RATIO)
    return [html_content[i:i + chars_per_chunk] for i in range(0, len(html_content), chars_per_chunk)]
