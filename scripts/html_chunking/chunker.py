"""
HTML chunker module.

This module splits HTML content into chunks based on semantic boundaries.
"""

from typing import List, Dict, Any, Tuple, Optional, Set, Union, Callable
from dataclasses import dataclass
from bs4 import BeautifulSoup, Tag, NavigableString
import re
import warnings

from tokenizer import count_html_tokens


@dataclass
class ChunkingOptions:
    max_token_limit: int = 500
    count_tag_tokens: bool = True
    keep_siblings_together: bool = True
    prepend_parent_section_text: bool = True


def chunk_html(
    html_content: str,
    max_token_limit: int = 500,
    count_tag_tokens: bool = True,
    keep_siblings_together: bool = True,
    prepend_parent_section_text: bool = True
) -> List[str]:
    # Check if the whole content is under the token limit
    try:
        content_tokens = count_html_tokens(html_content, count_tag_tokens)
        if content_tokens <= max_token_limit:
            return [html_content]
    except Exception as e:
        warnings.warn(f"Error counting tokens: {e}. Will proceed with chunking anyway.")
    
    options = ChunkingOptions(
        max_token_limit=max_token_limit,
        count_tag_tokens=count_tag_tokens,
        keep_siblings_together=keep_siblings_together,
        prepend_parent_section_text=prepend_parent_section_text
    )
    
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Use heading-based chunking as the primary approach
        chunks = _chunk_by_headings(soup, options)
        
        # If no chunks were created, try other approaches
        if not chunks:
            chunks = _chunk_by_semantic_elements(soup, options)
            
        # If still no chunks, use linear chunking
        if not chunks:
            chunks = _linear_chunking(html_content, options)
        
        # Check that we haven't lost content
        total_content = "".join(chunks)
        if len(total_content) < len(html_content) * 0.9:  # Lost more than 10%
            warnings.warn("Chunking may have lost content. Falling back to linear chunking.")
            chunks = _linear_chunking(html_content, options)
        
        # Post-process chunks to remove empty ones
        chunks = [chunk for chunk in chunks if chunk.strip()]
        
        # If we have no chunks, return the original content as one chunk
        if not chunks:
            return [html_content]
            
        return chunks
    except Exception as e:
        warnings.warn(f"Error during chunking: {e}. Falling back to linear chunking.")
        return _linear_chunking(html_content, options)


def _chunk_by_headings(soup: BeautifulSoup, options: ChunkingOptions) -> List[str]:
    """
    Chunk HTML based on heading elements.
    
    Args:
        soup: BeautifulSoup object of the HTML.
        options: Chunking options.
        
    Returns:
        List of HTML chunks.
    """
    chunks = []
    
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    
    if not headings:
        return []
    
    # Create chunks based on headings
    for i, heading in enumerate(headings):
        # Determine the level of this heading
        level = int(heading.name[1])
        
        # Find the next heading of same or higher level
        next_heading = None
        for h in headings[i+1:]:
            next_level = int(h.name[1])
            if next_level <= level:
                next_heading = h
                break
        
        # Extract content between this heading and the next heading
        chunk_content = [str(heading)]
        current = heading.next_sibling
        
        while current and (not next_heading or current != next_heading):
            # Skip empty elements
            if (isinstance(current, NavigableString) and not current.strip()) or (hasattr(current, 'is_empty_element') and current.is_empty_element):
                current = current.next_sibling
                continue
                
            # Add this element to the chunk
            chunk_content.append(str(current))
            current = current.next_sibling
        
        chunk = "".join(chunk_content)
        
        # Check if chunk is too large
        try:
            chunk_tokens = count_html_tokens(chunk, options.count_tag_tokens)
            
            if chunk_tokens <= options.max_token_limit:
                # Chunk is fine, add it
                chunks.append(chunk)
            else:
                # Chunk is too large, split it further
                sub_chunks = _split_oversized_chunk(chunk, options)
                chunks.extend(sub_chunks)
        except Exception:
            # If token counting fails, be conservative and split
            sub_chunks = _split_oversized_chunk(chunk, options)
            chunks.extend(sub_chunks)
    
    # Handle content before the first heading
    first_heading = headings[0]
    before_content = []
    current = first_heading.parent.contents[0]
    
    while current != first_heading:
        # Skip empty elements
        if (isinstance(current, NavigableString) and not current.strip()) or (hasattr(current, 'is_empty_element') and current.is_empty_element):
            current = current.next_sibling
            continue
            
        # Add this element to the chunk
        before_content.append(str(current))
        current = current.next_sibling
    
    # Combine content into a chunk
    if before_content:
        before_chunk = "".join(before_content)
        
        # Check if chunk is too large
        try:
            chunk_tokens = count_html_tokens(before_chunk, options.count_tag_tokens)
            
            if chunk_tokens <= options.max_token_limit:
                # Chunk is fine, add it
                chunks.insert(0, before_chunk)
            else:
                # Chunk is too large, split it further
                sub_chunks = _split_oversized_chunk(before_chunk, options)
                for i, sub in enumerate(sub_chunks):
                    chunks.insert(i, sub)
        except Exception:
            # If token counting fails, be conservative and split
            sub_chunks = _split_oversized_chunk(before_chunk, options)
            for i, sub in enumerate(sub_chunks):
                chunks.insert(i, sub)
    
    return chunks


def _chunk_by_semantic_elements(soup: BeautifulSoup, options: ChunkingOptions) -> List[str]:
    """
    Chunk HTML based on semantic elements like sections, divs, etc.
    
    Args:
        soup: BeautifulSoup object of the HTML.
        options: Chunking options.
        
    Returns:
        List of HTML chunks.
    """
    chunks = []
    
    # Find all semantic elements
    semantic_elements = soup.find_all(['section', 'article', 'div', 'main', 'aside', 'nav'])
    
    # Sort by size (number of descendants)
    top_level_elements = []
    for elem in semantic_elements:
        # Skip tiny elements
        if len(list(elem.descendants)) < 5:
            continue
            
        # Check if this element is a direct child of body
        parent = elem.parent
        is_top_level = parent.name == 'body' or parent == soup
        
        if is_top_level:
            top_level_elements.append(elem)
    
    if not top_level_elements:
        return []
    
    # Create chunks from top-level elements
    for element in top_level_elements:
        element_html = str(element)
        
        # Check if element is too large
        try:
            element_tokens = count_html_tokens(element_html, options.count_tag_tokens)
            
            if element_tokens <= options.max_token_limit:
                # Element is fine, add it
                chunks.append(element_html)
            else:
                # Element is too large, try to split by inner headings
                inner_chunks = _chunk_by_inner_headings(element, options)
                
                if inner_chunks:
                    chunks.extend(inner_chunks)
                else:
                    # No inner headings, split linearly
                    sub_chunks = _split_oversized_chunk(element_html, options)
                    chunks.extend(sub_chunks)
        except Exception:
            # If token counting fails, be conservative and split
            sub_chunks = _split_oversized_chunk(element_html, options)
            chunks.extend(sub_chunks)
    
    return chunks


def _chunk_by_inner_headings(element: Tag, options: ChunkingOptions) -> List[str]:
    """
    Chunk an element by its inner headings.
    
    Args:
        element: HTML element to chunk.
        options: Chunking options.
        
    Returns:
        List of HTML chunks.
    """
    chunks = []
    
    # Find all headings in the element
    headings = element.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    
    if not headings:
        return []
    
    # Create chunks based on headings
    for i, heading in enumerate(headings):
        # Find the next heading
        next_heading = None
        if i < len(headings) - 1:
            next_heading = headings[i+1]
        
        # Extract content between this heading and the next heading
        chunk_content = [str(heading)]
        current = heading.next_sibling
        
        while current and (not next_heading or current != next_heading):
            # Skip empty elements
            if (isinstance(current, NavigableString) and not current.strip()) or (hasattr(current, 'is_empty_element') and current.is_empty_element):
                current = current.next_sibling
                continue
                
            # Add this element to the chunk
            chunk_content.append(str(current))
            current = current.next_sibling
        
        # Combine content into a chunk
        chunk = "".join(chunk_content)
        
        # Check if chunk is too large
        try:
            chunk_tokens = count_html_tokens(chunk, options.count_tag_tokens)
            
            if chunk_tokens <= options.max_token_limit:
                # Chunk is fine, add it
                chunks.append(chunk)
            else:
                # Chunk is too large, split it further
                sub_chunks = _split_oversized_chunk(chunk, options)
                chunks.extend(sub_chunks)
        except Exception:
            # If token counting fails, be conservative and split
            sub_chunks = _split_oversized_chunk(chunk, options)
            chunks.extend(sub_chunks)
    
    # Handle content before the first heading
    first_heading = headings[0]
    before_content = []
    
    # Check if the first heading is not the first content in the element
    if first_heading != element.contents[0]:
        current = element.contents[0]
        
        while current != first_heading:
            # Skip empty elements
            if (isinstance(current, NavigableString) and not current.strip()) or (hasattr(current, 'is_empty_element') and current.is_empty_element):
                current = current.next_sibling
                continue
                
            # Add this element to the chunk
            before_content.append(str(current))
            current = current.next_sibling
        
        # Combine content into a chunk
        if before_content:
            before_chunk = "".join(before_content)
            
            # Check if chunk is too large
            try:
                chunk_tokens = count_html_tokens(before_chunk, options.count_tag_tokens)
                
                if chunk_tokens <= options.max_token_limit:
                    # Chunk is fine, add it
                    chunks.insert(0, before_chunk)
                else:
                    # Chunk is too large, split it further
                    sub_chunks = _split_oversized_chunk(before_chunk, options)
                    for i, sub in enumerate(sub_chunks):
                        chunks.insert(i, sub)
            except Exception:
                # If token counting fails, be conservative and split
                sub_chunks = _split_oversized_chunk(before_chunk, options)
                for i, sub in enumerate(sub_chunks):
                    chunks.insert(i, sub)
    
    return chunks


def _split_oversized_chunk(chunk: str, options: ChunkingOptions) -> List[str]:
    """
    Split an oversized chunk into smaller chunks.
    
    Args:
        chunk: HTML content to split.
        options: Chunking options.
        
    Returns:
        List of smaller HTML chunks.
    """
    # Try to parse the chunk
    soup = BeautifulSoup(chunk, 'html.parser')
    
    # First try to split by special elements
    special_element_chunks = _split_by_special_elements(soup, options)
    if special_element_chunks:
        return special_element_chunks
    
    # Then try to split by block elements
    block_element_chunks = _split_by_block_elements(soup, options)
    if block_element_chunks:
        return block_element_chunks
    
    # If all else fails, split linearly
    return _linear_split(chunk, options)


def _split_by_special_elements(soup: BeautifulSoup, options: ChunkingOptions) -> List[str]:
    """
    Split content by special elements like tables, lists, code blocks.
    
    Args:
        soup: BeautifulSoup object of content to split.
        options: Chunking options.
        
    Returns:
        List of HTML chunks.
    """
    chunks = []
    
    # Find special elements
    special_elements = soup.find_all(['table', 'pre', 'ol', 'ul', 'code'])
    
    if not special_elements:
        return []
    
    # Sort special elements by their position in the document
    special_elements.sort(key=lambda x: _get_element_position(x))
    
    # Create chunks around special elements
    for i, element in enumerate(special_elements):
        # Find content before this element up to previous special element
        prev_special = special_elements[i-1] if i > 0 else None
        
        before_content = []
        current = element.previous_sibling
        
        while current and (not prev_special or current != prev_special):
            # Skip empty elements
            if (isinstance(current, NavigableString) and not current.strip()) or (hasattr(current, 'is_empty_element') and current.is_empty_element):
                current = current.previous_sibling
                continue
                
            # Add this element to the chunk (in reverse order)
            before_content.insert(0, str(current))
            current = current.previous_sibling
        
        # Combine content before this element
        if before_content:
            before_chunk = "".join(before_content)
            
            # Check if chunk is too large
            try:
                chunk_tokens = count_html_tokens(before_chunk, options.count_tag_tokens)
                
                if chunk_tokens <= options.max_token_limit:
                    # Chunk is fine, add it
                    chunks.append(before_chunk)
                else:
                    # Chunk is too large, split it further
                    sub_chunks = _linear_split(before_chunk, options)
                    chunks.extend(sub_chunks)
            except Exception:
                # If token counting fails, be conservative and split
                sub_chunks = _linear_split(before_chunk, options)
                chunks.extend(sub_chunks)
        
        # Handle the special element itself
        element_html = str(element)
        
        # Check if element is too large
        try:
            element_tokens = count_html_tokens(element_html, options.count_tag_tokens)
            
            if element_tokens <= options.max_token_limit:
                # Element is fine, add it
                chunks.append(element_html)
            else:
                # Element is too large, split it based on its type
                if element.name == 'table':
                    table_chunks = _split_table(element, options)
                    chunks.extend(table_chunks)
                elif element.name in ['ol', 'ul']:
                    list_chunks = _split_list(element, options)
                    chunks.extend(list_chunks)
                elif element.name in ['pre', 'code']:
                    code_chunks = _split_code(element, options)
                    chunks.extend(code_chunks)
                else:
                    # Unknown type, split linearly
                    sub_chunks = _linear_split(element_html, options)
                    chunks.extend(sub_chunks)
        except Exception:
            # If token counting fails, be conservative and split
            sub_chunks = _linear_split(element_html, options)
            chunks.extend(sub_chunks)
    
    # Handle content after the last special element
    last_special = special_elements[-1]
    after_content = []
    current = last_special.next_sibling
    
    while current:
        # Skip empty elements
        if (isinstance(current, NavigableString) and not current.strip()) or (hasattr(current, 'is_empty_element') and current.is_empty_element):
            current = current.next_sibling
            continue
            
        # Add this element to the chunk
        after_content.append(str(current))
        current = current.next_sibling
    
    # Combine content after the last element
    if after_content:
        after_chunk = "".join(after_content)
        
        # Check if chunk is too large
        try:
            chunk_tokens = count_html_tokens(after_chunk, options.count_tag_tokens)
            
            if chunk_tokens <= options.max_token_limit:
                # Chunk is fine, add it
                chunks.append(after_chunk)
            else:
                # Chunk is too large, split it further
                sub_chunks = _linear_split(after_chunk, options)
                chunks.extend(sub_chunks)
        except Exception:
            # If token counting fails, be conservative and split
            sub_chunks = _linear_split(after_chunk, options)
            chunks.extend(sub_chunks)
    
    return chunks


def _split_by_block_elements(soup: BeautifulSoup, options: ChunkingOptions) -> List[str]:
    """
    Split content by block elements.
    
    Args:
        soup: BeautifulSoup object of content to split.
        options: Chunking options.
        
    Returns:
        List of HTML chunks.
    """
    chunks = []
    
    # Find block elements
    block_elements = soup.find_all(['p', 'div', 'section', 'article', 'header', 'footer', 'nav'])
    
    if not block_elements:
        return []
    
    # Create chunks by grouping block elements
    current_chunk = []
    current_tokens = 0
    
    for element in block_elements:
        element_html = str(element)
        
        try:
            element_tokens = count_html_tokens(element_html, options.count_tag_tokens)
            
            # If this element alone exceeds the limit, split it
            if element_tokens > options.max_token_limit:
                # First add any accumulated content
                if current_chunk:
                    chunks.append("".join(current_chunk))
                    current_chunk = []
                    current_tokens = 0
                
                # Split this element
                sub_chunks = _linear_split(element_html, options)
                chunks.extend(sub_chunks)
                continue
            
            # If adding this element would exceed limit, create a new chunk
            if current_chunk and current_tokens + element_tokens > options.max_token_limit:
                chunks.append("".join(current_chunk))
                current_chunk = [element_html]
                current_tokens = element_tokens
            else:
                # Add to current chunk
                current_chunk.append(element_html)
                current_tokens += element_tokens
        except Exception:
            # If token counting fails, be conservative
            if current_chunk:
                chunks.append("".join(current_chunk))
                current_chunk = [element_html]
                current_tokens = 0  # Reset counter since we can't count reliably
            else:
                chunks.append(element_html)
    
    # Add the last chunk
    if current_chunk:
        chunks.append("".join(current_chunk))
    
    return chunks


def _linear_chunking(html_content: str, options: ChunkingOptions) -> List[str]:
    """
    Chunk HTML content linearly.
    
    Args:
        html_content: HTML content to chunk.
        options: Chunking options.
        
    Returns:
        List of HTML chunks.
    """
    # Try to parse the content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Get all direct children of body
    body = soup.body or soup
    children = list(body.children)
    
    # Filter out empty elements
    filtered_children = []
    for child in children:
        if (isinstance(child, NavigableString) and child.strip()) or (isinstance(child, Tag) and not (hasattr(child, 'is_empty_element') and child.is_empty_element)):
            filtered_children.append(child)
    
    # If no children, return original content
    if not filtered_children:
        return [html_content]
    
    # Create chunks by grouping elements
    return _linear_split(html_content, options)


def _linear_split(html_content: str, options: ChunkingOptions) -> List[str]:
    """
    Split HTML content linearly into chunks.
    
    Args:
        html_content: HTML content to split.
        options: Chunking options.
        
    Returns:
        List of HTML chunks.
    """
    chunks = []
    
    # Try to parse the content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Get all top-level elements
    top_elements = list(soup.children)
    
    # Create chunks by grouping elements
    current_chunk = []
    current_tokens = 0
    
    for element in top_elements:
        # Skip empty elements
        if (isinstance(element, NavigableString) and not element.strip()) or (hasattr(element, 'is_empty_element') and element.is_empty_element):
            continue
            
        element_html = str(element)
        
        try:
            element_tokens = count_html_tokens(element_html, options.count_tag_tokens)
            
            # If this element alone exceeds the limit, split it
            if element_tokens > options.max_token_limit:
                # First add any accumulated content
                if current_chunk:
                    chunks.append("".join(current_chunk))
                    current_chunk = []
                    current_tokens = 0
                
                # Split this element
                if isinstance(element, Tag):
                    # For tags, try to split by child elements
                    child_chunks = _split_element_by_children(element, options)
                    chunks.extend(child_chunks)
                else:
                    # For text nodes, split by characters
                    chars_per_token = 4  # Rough estimate
                    chars_per_chunk = options.max_token_limit * chars_per_token
                    
                    for i in range(0, len(element_html), chars_per_chunk):
                        chunks.append(element_html[i:i+chars_per_chunk])
                
                continue
            
            # If adding this element would exceed limit, create a new chunk
            if current_chunk and current_tokens + element_tokens > options.max_token_limit:
                chunks.append("".join(current_chunk))
                current_chunk = [element_html]
                current_tokens = element_tokens
            else:
                # Add to current chunk
                current_chunk.append(element_html)
                current_tokens += element_tokens
        except Exception:
            # If token counting fails, be conservative
            if current_chunk:
                chunks.append("".join(current_chunk))
                current_chunk = [element_html]
            else:
                # Split by a rough character count
                chars_per_token = 4  # Rough estimate
                chars_per_chunk = options.max_token_limit * chars_per_token
                
                if len(element_html) > chars_per_chunk:
                    for i in range(0, len(element_html), chars_per_chunk):
                        chunks.append(element_html[i:i+chars_per_chunk])
                else:
                    chunks.append(element_html)
    
    # Add the last chunk
    if current_chunk:
        chunks.append("".join(current_chunk))
    
    # If no chunks were created, split by characters
    if not chunks:
        chars_per_token = 4  # Rough estimate
        chars_per_chunk = options.max_token_limit * chars_per_token
        
        for i in range(0, len(html_content), chars_per_chunk):
            chunks.append(html_content[i:i+chars_per_chunk])
    
    return chunks


def _split_element_by_children(element: Tag, options: ChunkingOptions) -> List[str]:
    """
    Split an element by its children.
    
    Args:
        element: HTML element to split.
        options: Chunking options.
        
    Returns:
        List of HTML chunks.
    """
    chunks = []
    
    # Get tag name and attributes
    tag_name = element.name
    attrs = element.attrs
    
    # Build opening tag
    open_tag = f"<{tag_name}"
    for attr, value in attrs.items():
        if isinstance(value, list):
            value = " ".join(value)
        open_tag += f' {attr}="{value}"'
    open_tag += ">"
    
    close_tag = f"</{tag_name}>"
    
    # Get children
    children = list(element.children)
    
    # Create chunks by grouping children
    current_chunk = []
    current_tokens = count_html_tokens(open_tag + close_tag, options.count_tag_tokens)
    
    for child in children:
        # Skip empty elements
        if (isinstance(child, NavigableString) and not child.strip()) or (hasattr(child, 'is_empty_element') and child.is_empty_element):
            continue
            
        child_html = str(child)
        
        try:
            child_tokens = count_html_tokens(child_html, options.count_tag_tokens)
            
            # If this child alone exceeds the limit, split it
            if child_tokens > options.max_token_limit - count_html_tokens(open_tag + close_tag, options.count_tag_tokens):
                # First add any accumulated content
                if current_chunk:
                    chunks.append(open_tag + "".join(current_chunk) + close_tag)
                    current_chunk = []
                    current_tokens = count_html_tokens(open_tag + close_tag, options.count_tag_tokens)
                
                # Split this child
                if isinstance(child, Tag):
                    # For tags, recursively split
                    child_chunks = _split_element_by_children(child, options)
                    
                    # Wrap each chunk in the parent tag
                    for i, child_chunk in enumerate(child_chunks):
                        chunks.append(open_tag + child_chunk + close_tag)
                else:
                    # For text nodes, split by characters
                    chars_per_token = 4  # Rough estimate
                    chars_per_chunk = (options.max_token_limit - current_tokens) * chars_per_token
                    
                    for i in range(0, len(child_html), chars_per_chunk):
                        chunks.append(open_tag + child_html[i:i+chars_per_chunk] + close_tag)
                
                continue
            
            # If adding this child would exceed limit, create a new chunk
            if current_chunk and current_tokens + child_tokens > options.max_token_limit:
                chunks.append(open_tag + "".join(current_chunk) + close_tag)
                current_chunk = [child_html]
                current_tokens = count_html_tokens(open_tag + child_html + close_tag, options.count_tag_tokens)
            else:
                # Add to current chunk
                current_chunk.append(child_html)
                current_tokens += child_tokens
        except Exception:
            # If token counting fails, be conservative
            if current_chunk:
                chunks.append(open_tag + "".join(current_chunk) + close_tag)
                current_chunk = [child_html]
                current_tokens = count_html_tokens(open_tag + close_tag, options.count_tag_tokens)
            else:
                # Split by a rough character count
                chars_per_token = 4  # Rough estimate
                chars_per_chunk = (options.max_token_limit - current_tokens) * chars_per_token
                
                if len(child_html) > chars_per_chunk:
                    for i in range(0, len(child_html), chars_per_chunk):
                        chunks.append(open_tag + child_html[i:i+chars_per_chunk] + close_tag)
                else:
                    chunks.append(open_tag + child_html + close_tag)
    
    # Add the last chunk
    if current_chunk:
        chunks.append(open_tag + "".join(current_chunk) + close_tag)
    
    return chunks


def _split_table(table: Tag, options: ChunkingOptions) -> List[str]:
    """
    Split a table into chunks.
    
    Args:
        table: Table element to split.
        options: Chunking options.
        
    Returns:
        List of HTML chunks.
    """
    chunks = []
    
    # Get table components
    header = table.find('thead')
    rows = table.find_all('tr')
    
    # Skip rows that are in the header
    if header:
        header_rows = set(id(row) for row in header.find_all('tr'))
        body_rows = [row for row in rows if id(row) not in header_rows]
    else:
        body_rows = rows
    
    # Get table attributes
    table_attrs = ""
    for attr, value in table.attrs.items():
        if isinstance(value, list):
            value = " ".join(value)
        table_attrs += f' {attr}="{value}"'
    
    # Create the table opening tag
    table_open = f"<table{table_attrs}>"
    table_close = "</table>"
    
    # Add header to all chunks
    header_html = str(header) if header else ""
    
    # Create chunks by grouping rows
    current_chunk = []
    current_html = table_open + header_html
    current_tokens = count_html_tokens(current_html + table_close, options.count_tag_tokens)
    
    for row in body_rows:
        row_html = str(row)
        
        try:
            row_tokens = count_html_tokens(row_html, options.count_tag_tokens)
            
            # If adding this row would exceed limit, create a new chunk
            if current_chunk and current_tokens + row_tokens > options.max_token_limit:
                chunks.append(current_html + "".join(current_chunk) + table_close)
                current_chunk = [row_html]
                current_html = table_open + header_html
                current_tokens = count_html_tokens(current_html + row_html + table_close, options.count_tag_tokens)
            else:
                # Add to current chunk
                current_chunk.append(row_html)
                current_tokens += row_tokens
        except Exception:
            # If token counting fails, be conservative
            if current_chunk:
                chunks.append(current_html + "".join(current_chunk) + table_close)
                current_chunk = [row_html]
                current_html = table_open + header_html
                current_tokens = 0  # Reset counter since we can't count reliably
            else:
                chunks.append(table_open + header_html + row_html + table_close)
    
    # Add the last chunk
    if current_chunk:
        chunks.append(current_html + "".join(current_chunk) + table_close)
    
    return chunks


def _split_list(list_element: Tag, options: ChunkingOptions) -> List[str]:
    """
    Split a list into chunks.
    
    Args:
        list_element: List element to split.
        options: Chunking options.
        
    Returns:
        List of HTML chunks.
    """
    chunks = []
    
    # Get list items
    items = list_element.find_all('li', recursive=False)
    
    # Get list attributes
    list_attrs = ""
    for attr, value in list_element.attrs.items():
        if isinstance(value, list):
            value = " ".join(value)
        if attr != "start":  # We'll handle start separately
            list_attrs += f' {attr}="{value}"'
    
    # Create the list opening tag
    list_open = f"<{list_element.name}{list_attrs}>"
    list_close = f"</{list_element.name}>"
    
    # Create chunks by grouping items
    current_chunk = []
    current_tokens = count_html_tokens(list_open + list_close, options.count_tag_tokens)
    current_item_index = 1
    
    for item in items:
        item_html = str(item)
        
        try:
            item_tokens = count_html_tokens(item_html, options.count_tag_tokens)
            
            # If this item alone exceeds the limit, split it
            if item_tokens > options.max_token_limit - count_html_tokens(list_open + list_close, options.count_tag_tokens):
                # First add any accumulated content
                if current_chunk:
                    chunks.append(list_open + "".join(current_chunk) + list_close)
                    current_chunk = []
                    current_tokens = count_html_tokens(list_open + list_close, options.count_tag_tokens)
                
                # Split this item by its content
                item_chunks = _split_list_item(item, options)
                
                # Add each chunk as its own list
                for i, item_chunk in enumerate(item_chunks):
                    if list_element.name == 'ol':
                        # For ordered lists, set the start attribute
                        list_tag = f"<{list_element.name}{list_attrs} start=\"{current_item_index}\">"
                    else:
                        list_tag = list_open
                        
                    chunks.append(list_tag + item_chunk + list_close)
                
                current_item_index += 1
                continue
            
            # If adding this item would exceed limit, create a new chunk
            if current_chunk and current_tokens + item_tokens > options.max_token_limit:
                chunks.append(list_open + "".join(current_chunk) + list_close)
                current_chunk = [item_html]
                
                if list_element.name == 'ol':
                    # For ordered lists, set the start attribute
                    list_open = f"<{list_element.name}{list_attrs} start=\"{current_item_index}\">"
                
                current_tokens = count_html_tokens(list_open + item_html + list_close, options.count_tag_tokens)
            else:
                # Add to current chunk
                current_chunk.append(item_html)
                current_tokens += item_tokens
            
            current_item_index += 1
        except Exception:
            # If token counting fails, be conservative
            if current_chunk:
                chunks.append(list_open + "".join(current_chunk) + list_close)
                current_chunk = [item_html]
                
                if list_element.name == 'ol':
                    # For ordered lists, set the start attribute
                    list_open = f"<{list_element.name}{list_attrs} start=\"{current_item_index}\">"
                
                current_tokens = 0  # Reset counter since we can't count reliably
            else:
                if list_element.name == 'ol':
                    # For ordered lists, set the start attribute
                    list_tag = f"<{list_element.name}{list_attrs} start=\"{current_item_index}\">"
                else:
                    list_tag = list_open
                    
                chunks.append(list_tag + item_html + list_close)
            
            current_item_index += 1
    
    # Add the last chunk
    if current_chunk:
        chunks.append(list_open + "".join(current_chunk) + list_close)
    
    return chunks


def _split_list_item(item: Tag, options: ChunkingOptions) -> List[str]:
    """
    Split a list item into chunks.
    
    Args:
        item: List item to split.
        options: Chunking options.
        
    Returns:
        List of HTML chunks.
    """
    # This function splits a single list item into multiple items
    # Each returned chunk should be a valid list item
    chunks = []
    
    # Get item children
    children = list(item.children)
    
    # If no children, return the item as is
    if not children:
        return [str(item)]
    
    # Get item attributes
    item_attrs = ""
    for attr, value in item.attrs.items():
        if isinstance(value, list):
            value = " ".join(value)
        item_attrs += f' {attr}="{value}"'
    
    # Split by paragraphs if possible
    paragraphs = item.find_all('p')
    
    if paragraphs:
        current_chunk = []
        current_tokens = count_html_tokens(f"<li{item_attrs}></li>", options.count_tag_tokens)
        
        for p in paragraphs:
            p_html = str(p)
            
            try:
                p_tokens = count_html_tokens(p_html, options.count_tag_tokens)
                
                # If adding this paragraph would exceed limit, create a new chunk
                if current_chunk and current_tokens + p_tokens > options.max_token_limit:
                    chunks.append(f"<li{item_attrs}>" + "".join(current_chunk) + "</li>")
                    current_chunk = [p_html]
                    current_tokens = count_html_tokens(f"<li{item_attrs}>{p_html}</li>", options.count_tag_tokens)
                else:
                    # Add to current chunk
                    current_chunk.append(p_html)
                    current_tokens += p_tokens
            except Exception:
                # If token counting fails, be conservative
                if current_chunk:
                    chunks.append(f"<li{item_attrs}>" + "".join(current_chunk) + "</li>")
                    current_chunk = [p_html]
                    current_tokens = 0  # Reset counter since we can't count reliably
                else:
                    chunks.append(f"<li{item_attrs}>{p_html}</li>")
        
        # Add the last chunk
        if current_chunk:
            chunks.append(f"<li{item_attrs}>" + "".join(current_chunk) + "</li>")
    else:
        # No paragraphs, split by children
        current_chunk = []
        current_tokens = count_html_tokens(f"<li{item_attrs}></li>", options.count_tag_tokens)
        
        for child in children:
            # Skip empty elements
            if (isinstance(child, NavigableString) and not child.strip()) or (hasattr(child, 'is_empty_element') and child.is_empty_element):
                continue
                
            child_html = str(child)
            
            try:
                child_tokens = count_html_tokens(child_html, options.count_tag_tokens)
                
                # If adding this child would exceed limit, create a new chunk
                if current_chunk and current_tokens + child_tokens > options.max_token_limit:
                    chunks.append(f"<li{item_attrs}>" + "".join(current_chunk) + "</li>")
                    current_chunk = [child_html]
                    current_tokens = count_html_tokens(f"<li{item_attrs}>{child_html}</li>", options.count_tag_tokens)
                else:
                    # Add to current chunk
                    current_chunk.append(child_html)
                    current_tokens += child_tokens
            except Exception:
                # If token counting fails, be conservative
                if current_chunk:
                    chunks.append(f"<li{item_attrs}>" + "".join(current_chunk) + "</li>")
                    current_chunk = [child_html]
                    current_tokens = 0  # Reset counter since we can't count reliably
                else:
                    chunks.append(f"<li{item_attrs}>{child_html}</li>")
        
        # Add the last chunk
        if current_chunk:
            chunks.append(f"<li{item_attrs}>" + "".join(current_chunk) + "</li>")
    
    # If no chunks were created, return the item as is
    if not chunks:
        return [str(item)]
    
    return chunks


def _split_code(code_element: Tag, options: ChunkingOptions) -> List[str]:
    """
    Split a code element into chunks.
    
    Args:
        code_element: Code element to split.
        options: Chunking options.
        
    Returns:
        List of HTML chunks.
    """
    chunks = []
    
    # Get code text
    code_text = code_element.get_text()
    
    # Get element attributes
    code_attrs = ""
    for attr, value in code_element.attrs.items():
        if isinstance(value, list):
            value = " ".join(value)
        code_attrs += f' {attr}="{value}"'
    
    # Create the code opening tag
    code_open = f"<{code_element.name}{code_attrs}>"
    code_close = f"</{code_element.name}>"
    
    # Split by lines
    lines = code_text.split('\n')
    
    # Create chunks by grouping lines
    current_chunk = []
    current_tokens = count_html_tokens(code_open + code_close, options.count_tag_tokens)
    
    for line in lines:
        line_html = line + '\n'
        
        try:
            line_tokens = count_html_tokens(line_html, options.count_tag_tokens)
            
            # If adding this line would exceed limit, create a new chunk
            if current_chunk and current_tokens + line_tokens > options.max_token_limit:
                chunks.append(code_open + "".join(current_chunk) + code_close)
                current_chunk = [line_html]
                current_tokens = count_html_tokens(code_open + line_html + code_close, options.count_tag_tokens)
            else:
                # Add to current chunk
                current_chunk.append(line_html)
                current_tokens += line_tokens
        except Exception:
            # If token counting fails, be conservative
            if current_chunk:
                chunks.append(code_open + "".join(current_chunk) + code_close)
                current_chunk = [line_html]
                current_tokens = 0  # Reset counter since we can't count reliably
            else:
                chunks.append(code_open + line_html + code_close)
    
    # Add the last chunk
    if current_chunk:
        chunks.append(code_open + "".join(current_chunk) + code_close)
    
    return chunks


def _get_element_position(element: Tag) -> int:
    """
    Get the position of an element in its parent.
    
    Args:
        element: The element to find position for.
        
    Returns:
        The position index of the element.
    """
    if not element or not element.parent:
        return -1
        
    return list(element.parent.children).index(element)
