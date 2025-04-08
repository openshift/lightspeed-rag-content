from typing import List, Dict, Any, Tuple, Optional, Union
from bs4 import BeautifulSoup, Tag, NavigableString
import re
import os

from html_chunking.parser import parse_html, HtmlSection, identify_procedure_sections
from html_chunking.tokenizer import count_html_tokens

def chunk_html(html_content: str,
              max_token_limit: int = 500,
              count_tag_tokens: bool = True,
              keep_siblings_together: bool = True,
              prepend_parent_section_text: bool = True) -> List[str]:
    """
    Split HTML content into chunks based on specified parameters.

    Args:
        html_content (str): The HTML content to chunk.
        max_token_limit (int): Maximum number of tokens allowed per chunk.
        count_tag_tokens (bool): Whether to count HTML tags as tokens.
        keep_siblings_together (bool): Keep adjacent heading sections together if under token limit.
        prepend_parent_section_text (bool): Include parent heading text in child section chunks.

    Returns:
        List[str]: A list of HTML chunks.
    """
    html_content = _clean_duplicate_procedures(html_content)
    soup, root_section = parse_html(html_content)

    # Calculate tag-to-text ratio and provide a warning if it's high
    html_tokens = count_html_tokens(html_content, True)
    text_tokens = count_html_tokens(html_content, False)
    tag_to_text_ratio = html_tokens / max(1, text_tokens)

    if count_tag_tokens and tag_to_text_ratio > 3.0:
        print(f"Warning: High tag-to-text ratio detected ({tag_to_text_ratio:.2f})")
        print(f"  HTML tokens: {html_tokens}, Text-only tokens: {text_tokens}")
        print(f"  This may result in excessive chunking with count_tag_tokens=True")
        print(f"  Consider using count_tag_tokens=False if you're stripping HTML before embedding")

    if count_html_tokens(html_content, count_tag_tokens) <= max_token_limit:
        return [html_content]

    chunks = []
    found_headings = False
    processed_sections = set()

    # First try chunking by h1 sections
    for section in root_section.children:
        if section.level == 1:
            found_headings = True
            _chunk_section_tree(section, chunks, max_token_limit, count_tag_tokens,
                             keep_siblings_together, prepend_parent_section_text, "", processed_sections)

    # If no h1 sections, try h2 sections
    if not found_headings:
        for section in root_section.children:
            if section.level == 2:
                found_headings = True
                _chunk_section_tree(section, chunks, max_token_limit, count_tag_tokens,
                                keep_siblings_together, prepend_parent_section_text, "", processed_sections)

    # If still no chunks, use fallback strategies
    if not found_headings or not chunks:
        raw_html = str(soup)
        if count_html_tokens(raw_html, count_tag_tokens) <= max_token_limit:
            chunks = [raw_html]
        else:
            # Try to chunk by section divs if available (common in many HTML docs)
            section_divs = soup.find_all('div', class_='sect1')
            if section_divs:
                for div in section_divs:
                    div_html = str(div)
                    if count_html_tokens(div_html, count_tag_tokens) <= max_token_limit:
                        chunks.append(div_html)
                    else:
                        subsections = div.find_all('div', class_='sectionbody')
                        for subsection in subsections:
                            chunks.append(str(subsection))
            else:
                # Final fallback: chunk by top-level elements
                current_chunk = ""
                for tag in soup.body.children if soup.body else soup.children:
                    if isinstance(tag, Tag):
                        tag_html = str(tag)
                        if count_html_tokens(current_chunk + tag_html, count_tag_tokens) <= max_token_limit:
                            current_chunk += tag_html
                        else:
                            if current_chunk:
                                chunks.append(current_chunk)
                            current_chunk = tag_html

                if current_chunk:
                    chunks.append(current_chunk)

    # Process special elements like procedures, code blocks, and tables
    chunks = _handle_special_elements(chunks, soup, max_token_limit, count_tag_tokens)

    return chunks

def _clean_duplicate_procedures(html_content: str) -> str:
    """
    Remove duplicate procedure sections from the HTML content.

    Args:
        html_content (str): The original HTML content.

    Returns:
        str: HTML content with duplicate procedures removed.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all "Procedure" elements
    procedure_markers = soup.find_all(string=lambda text: text and "Procedure" in text)

    # Skip if no procedures
    if not procedure_markers or len(procedure_markers) <= 1:
        return html_content

    # First, find all procedure sections with proper context
    procedures_with_context = []
    procedures_without_context = []

    for marker in procedure_markers:
        # Find the associated ordered list
        ol = marker.parent.find_next('ol')
        if not ol:
            continue

        # Find the section context
        in_section = False
        parent = marker.parent
        while parent and parent.name != 'body':
            if parent.name == 'div' and 'sectionbody' in parent.get('class', []):
                in_section = True
                break
            parent = parent.parent

        if in_section:
            procedures_with_context.append((marker, ol))
        else:
            procedures_without_context.append((marker, ol))

    # If we have procedures with proper context, remove the ones without proper context
    if procedures_with_context:
        for marker, _ in procedures_without_context:
            # Find the complete section to remove
            section_to_remove = marker.parent

            # Go up until we find a suitable container to remove (like a div)
            parent = section_to_remove
            while parent and parent.name != 'body':
                if parent.name == 'div' or parent.name == 'section':
                    section_to_remove = parent
                    break
                parent = parent.parent

            # If we didn't find a suitable container, start with the title
            if section_to_remove == marker.parent:
                # Look for a previous sibling that might be the title
                prev = section_to_remove.previous_sibling
                while prev and (not isinstance(prev, Tag) or not prev.name or 'title' not in prev.get('class', [])):
                    prev = prev.previous_sibling

                if prev and isinstance(prev, Tag) and 'title' in prev.get('class', []):
                    # Remove the title element
                    prev.decompose()

            # Now remove the procedure section
            section_to_remove.decompose()

    # As a last resort, detect duplicate ordered lists with identical steps
    ol_lists = soup.find_all('ol', class_='arabic')
    ol_texts = {}

    for ol in ol_lists:
        # Get the text content of the list for comparison
        ol_text = ol.get_text().strip()

        if ol_text in ol_texts:
            # This is a duplicate, remove it
            # First try to find and remove its parent container
            parent = ol.parent
            while parent and parent.name != 'body':
                if parent.name == 'div' or parent.name == 'section':
                    parent.decompose()
                    break
                parent = parent.parent

            # If we couldn't find a container, just remove the list itself
            if parent and parent.name == 'body':
                # Look for a previous sibling that might be the title
                prev = ol.previous_sibling
                while prev and (not isinstance(prev, Tag) or not prev.name or 'title' not in prev.get('class', [])):
                    prev = prev.previous_sibling

                if prev and isinstance(prev, Tag) and 'title' in prev.get('class', []):
                    # Remove the title element
                    prev.decompose()

                # Remove the list
                ol.decompose()
        else:
            ol_texts[ol_text] = ol

    return str(soup)

def chunk_html_file(file_path: str, **kwargs) -> List[str]:
    """
    Read an HTML file and chunk its content.

    Args:
        file_path (str): Path to the HTML file.
        **kwargs: Additional arguments to pass to chunk_html.

    Returns:
        List[str]: A list of HTML chunks.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    return chunk_html(html_content, **kwargs)

def _chunk_section_tree(section: HtmlSection,
                      chunks: List[str],
                      max_token_limit: int,
                      count_tag_tokens: bool,
                      keep_siblings_together: bool,
                      prepend_parent_section_text: bool,
                      parent_html: str = "",
                      processed_sections: set = None) -> None:
    """
    Recursively chunk a section tree.

    Args:
        section (HtmlSection): The section to chunk.
        chunks (List[str]): The list to append chunks to.
        max_token_limit (int): Maximum number of tokens allowed per chunk.
        count_tag_tokens (bool): Whether to count HTML tags as tokens.
        keep_siblings_together (bool): Keep adjacent heading sections together if under token limit.
        prepend_parent_section_text (bool): Include parent heading text in child section chunks.
        parent_html (str): HTML of parent section to possibly prepend.
        processed_sections (set): Set to track processed sections to avoid duplicates.
    """
    if processed_sections is None:
        processed_sections = set()

    section_id = id(section)
    if section_id in processed_sections:
        return

    processed_sections.add(section_id)

    # Get section's heading for parent prepending
    section_heading_html = ""
    if section.heading_tag:
        section_heading_html = str(section.heading_tag)

    # Combine parent HTML with current section's heading
    section_prefix = ""
    if prepend_parent_section_text:
        section_prefix = parent_html

    if not section.children:
        section_html = section.get_html()
        if section_html.strip():
            if prepend_parent_section_text and parent_html:
                combined_html = parent_html + section_html
                if count_html_tokens(combined_html, count_tag_tokens) <= max_token_limit:
                    chunks.append(combined_html)
                else:
                    chunks.append(section_html)
            else:
                chunks.append(section_html)
        return

    if keep_siblings_together:
        sibling_groups = _group_siblings_by_size(
            section.children, max_token_limit, count_tag_tokens,
            section_prefix
        )

        for group in sibling_groups:
            if len(group) == 1:
                child_section = group[0]
                child_html = child_section.get_html()

                # Create new parent HTML by combining existing parent HTML with current section heading
                new_parent_html = section_prefix
                if section_heading_html:
                    new_parent_html += section_heading_html

                if prepend_parent_section_text:
                    combined_parent_child = new_parent_html + child_html
                    if count_html_tokens(combined_parent_child, count_tag_tokens) <= max_token_limit:
                        _chunk_section_tree(
                            child_section, chunks, max_token_limit, count_tag_tokens,
                            keep_siblings_together, prepend_parent_section_text,
                            new_parent_html, processed_sections
                        )
                    else:
                        # If too large with parent text, still pass the parent text for deeper levels
                        _chunk_section_tree(
                            child_section, chunks, max_token_limit, count_tag_tokens,
                            keep_siblings_together, prepend_parent_section_text,
                            new_parent_html, processed_sections
                        )
                else:
                    _chunk_section_tree(
                        child_section, chunks, max_token_limit, count_tag_tokens,
                        keep_siblings_together, prepend_parent_section_text,
                        "", processed_sections
                    )
            else:
                combined_html = section_prefix
                for child_section in group:
                    processed_sections.add(id(child_section))
                    combined_html += child_section.get_html()

                chunks.append(combined_html)
    else:
        for child_section in section.children:
            if id(child_section) in processed_sections:
                continue

            child_html = child_section.get_html()

            # Create new parent HTML by combining existing parent HTML with current section heading
            new_parent_html = section_prefix
            if section_heading_html:
                new_parent_html += section_heading_html

            if prepend_parent_section_text:
                combined_parent_child = new_parent_html + child_html
                if count_html_tokens(combined_parent_child, count_tag_tokens) <= max_token_limit:
                    # If combined content fits, create a single chunk
                    chunks.append(combined_parent_child)
                else:
                    # If too large, recursively process with parent text
                    _chunk_section_tree(
                        child_section, chunks, max_token_limit, count_tag_tokens,
                        keep_siblings_together, prepend_parent_section_text,
                        new_parent_html, processed_sections
                    )
            else:
                _chunk_section_tree(
                    child_section, chunks, max_token_limit, count_tag_tokens,
                    keep_siblings_together, prepend_parent_section_text,
                    "", processed_sections
                )

def _group_siblings_by_size(sections: List[HtmlSection],
                          max_token_limit: int,
                          count_tag_tokens: bool,
                          parent_html: str = "") -> List[List[HtmlSection]]:
    """
    Group sibling sections together if they fit within the token limit.

    Args:
        sections (List[HtmlSection]): List of sibling sections.
        max_token_limit (int): Maximum number of tokens allowed per chunk.
        count_tag_tokens (bool): Whether to count HTML tags as tokens.
        parent_html (str): HTML of parent section to possibly prepend.

    Returns:
        List[List[HtmlSection]]: Grouped sections.
    """
    if not sections:
        return []

    groups = []
    current_group = []
    current_size = count_html_tokens(parent_html, count_tag_tokens)

    for section in sections:
        section_html = section.get_html()
        section_size = count_html_tokens(section_html, count_tag_tokens)

        if not current_group or current_size + section_size <= max_token_limit:
            current_group.append(section)
            current_size += section_size
        else:
            groups.append(current_group)
            current_group = [section]
            current_size = count_html_tokens(parent_html, count_tag_tokens) + section_size

    if current_group:
        groups.append(current_group)

    return groups

def _handle_special_elements(chunks: List[str],
                           soup: BeautifulSoup,
                           max_token_limit: int,
                           count_tag_tokens: bool) -> List[str]:
    """
    Process chunks to handle special elements like procedures, code blocks, and tables.

    Args:
        chunks (List[str]): The initial chunks.
        soup (BeautifulSoup): The parsed BeautifulSoup object.
        max_token_limit (int): Maximum number of tokens allowed per chunk.
        count_tag_tokens (bool): Whether to count HTML tags as tokens.

    Returns:
        List[str]: Updated chunks with special elements handled.
    """
    chunks = _handle_procedures(chunks, soup, max_token_limit, count_tag_tokens)
    chunks = _handle_code_blocks(chunks, soup, max_token_limit, count_tag_tokens)
    chunks = _handle_tables(chunks, soup, max_token_limit, count_tag_tokens)

    return chunks

def _handle_procedures(chunks: List[str],
                     soup: BeautifulSoup,
                     max_token_limit: int,
                     count_tag_tokens: bool) -> List[str]:
    """
    Handle procedure sections in the chunks.

    Args:
        chunks (List[str]): The initial chunks.
        soup (BeautifulSoup): The parsed BeautifulSoup object.
        max_token_limit (int): Maximum number of tokens allowed per chunk.
        count_tag_tokens (bool): Whether to count HTML tags as tokens.

    Returns:
        List[str]: Updated chunks with procedures handled.
    """
    procedures = identify_procedure_sections(soup)
    if not procedures:
        return chunks

    # Process each chunk to handle procedures
    result_chunks = []

    for chunk in chunks:
        chunk_soup = BeautifulSoup(chunk, 'html.parser')

        # Check if this chunk contains a procedure
        contains_procedure = False
        for proc in procedures:
            proc_marker = chunk_soup.find(string=lambda text: text and "Procedure" in text)
            proc_steps = chunk_soup.find('ol')

            if proc_marker and proc_steps:
                contains_procedure = True

                # Try to keep the entire procedure intact
                if count_html_tokens(chunk, count_tag_tokens) <= max_token_limit:
                    result_chunks.append(chunk)
                else:
                    # The procedure is too large, split it
                    # First, try to keep heading + intro + prerequisites if they fit
                    heading_html = ""
                    if proc.get('heading'):
                        heading_html = str(proc['heading'])

                    intro_html = ""
                    if proc.get('intro'):
                        intro_html = "".join(str(elem) for elem in proc['intro'])

                    prereq_html = ""
                    if proc.get('prerequisites'):
                        prereq_html = str(proc['prerequisites'])

                    marker_html = str(proc_marker.parent)
                    steps_html = str(proc_steps)

                    # Try combinations to keep as much context as possible
                    if count_html_tokens(heading_html + intro_html + prereq_html + marker_html + steps_html,
                                       count_tag_tokens) <= max_token_limit:
                        # Everything fits
                        result_chunks.append(heading_html + intro_html + prereq_html + marker_html + steps_html)
                    elif count_html_tokens(prereq_html + marker_html + steps_html,
                                       count_tag_tokens) <= max_token_limit:
                        # Prerequisites + procedure fits
                        result_chunks.append(heading_html + intro_html)
                        result_chunks.append(prereq_html + marker_html + steps_html)
                    elif count_html_tokens(marker_html + steps_html,
                                       count_tag_tokens) <= max_token_limit:
                        # Just procedure fits
                        result_chunks.append(heading_html + intro_html + prereq_html)
                        result_chunks.append(marker_html + steps_html)
                    else:
                        # Need to split the procedure steps themselves
                        result_chunks.append(heading_html + intro_html + prereq_html)
                        result_chunks.append(marker_html)

                        # Split procedure steps
                        step_chunks = _split_list_items(proc_steps, max_token_limit, count_tag_tokens)
                        result_chunks.extend(step_chunks)

                break

        if not contains_procedure:
            result_chunks.append(chunk)

    return result_chunks

def _handle_code_blocks(chunks: List[str],
                      soup: BeautifulSoup,
                      max_token_limit: int,
                      count_tag_tokens: bool) -> List[str]:
    """
    Handle code blocks in the chunks.

    Args:
        chunks (List[str]): The initial chunks.
        soup (BeautifulSoup): The parsed BeautifulSoup object.
        max_token_limit (int): Maximum number of tokens allowed per chunk.
        count_tag_tokens (bool): Whether to count HTML tags as tokens.

    Returns:
        List[str]: Updated chunks with code blocks handled.
    """
    # Process each chunk to handle code blocks
    result_chunks = []
    for chunk in chunks:
        chunk_soup = BeautifulSoup(chunk, 'html.parser')
        code_blocks = chunk_soup.find_all(['pre', 'code'])

        if not code_blocks:
            result_chunks.append(chunk)
            continue

        # Check if the entire chunk fits within the token limit
        if count_html_tokens(chunk, count_tag_tokens) <= max_token_limit:
            result_chunks.append(chunk)
            continue

        # Find the heading element for context
        heading = None
        for h_tag in chunk_soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            heading = h_tag
            break

        heading_html = str(heading) if heading else ""

        # Group adjacent code blocks with their context
        current_group = []
        current_size = count_html_tokens(heading_html, count_tag_tokens)

        # Find all elements in document order
        elements = []
        for el in chunk_soup.find_all(True):
            # Skip nested elements to avoid duplication
            if not any(el in p.descendants for p in elements):
                elements.append(el)

        for element in elements:
            # Skip the heading as we've already included it
            if element == heading:
                continue

            is_code_block = element.name in ['pre', 'code']
            element_html = str(element)
            element_size = count_html_tokens(element_html, count_tag_tokens)

            # If the element is small enough to add to the current group
            if current_size + element_size <= max_token_limit:
                current_group.append(element_html)
                current_size += element_size
            else:
                # Current group is full, output it and start a new group
                if current_group:
                    result_chunks.append(heading_html + "".join(current_group))

                # If the element itself is too large, split it
                if is_code_block and element_size > max_token_limit:
                    # Split code block by chunks of lines
                    code_text = element.get_text()
                    lines = code_text.split('\n')

                    # Try to split into larger chunks (50 lines per chunk)
                    LINES_PER_CHUNK = 50
                    for i in range(0, len(lines), LINES_PER_CHUNK):
                        chunk_lines = lines[i:i+LINES_PER_CHUNK]
                        code_chunk = f"<{element.name}>{' '.join(chunk_lines)}</{element.name}>"

                        # Check if this chunk fits
                        if count_html_tokens(heading_html + code_chunk, count_tag_tokens) <= max_token_limit:
                            result_chunks.append(heading_html + code_chunk)
                        else:
                            # Have to split further
                            current_chunk = f"<{element.name}>"
                            for line in chunk_lines:
                                line_html = line + '\n'
                                test_chunk = current_chunk + line_html + f"</{element.name}>"
                                if count_html_tokens(heading_html + test_chunk, count_tag_tokens) <= max_token_limit:
                                    current_chunk += line_html
                                else:
                                    current_chunk += f"</{element.name}>"
                                    result_chunks.append(heading_html + current_chunk)
                                    current_chunk = f"<{element.name}>{line_html}"

                            if current_chunk != f"<{element.name}>":
                                current_chunk += f"</{element.name}>"
                                result_chunks.append(heading_html + current_chunk)
                else:
                    # Start a new group with this element
                    current_group = [element_html]
                    current_size = count_html_tokens(heading_html + element_html, count_tag_tokens)

        # Output the final group if it has content
        if current_group:
            result_chunks.append(heading_html + "".join(current_group))

    return result_chunks

def _handle_tables(chunks: List[str],
                 soup: BeautifulSoup,
                 max_token_limit: int,
                 count_tag_tokens: bool) -> List[str]:
    """
    Handle tables in the chunks.

    Args:
        chunks (List[str]): The initial chunks.
        soup (BeautifulSoup): The parsed BeautifulSoup object.
        max_token_limit (int): Maximum number of tokens allowed per chunk.
        count_tag_tokens (bool): Whether to count HTML tags as tokens.

    Returns:
        List[str]: Updated chunks with tables handled.
    """
    # Process each chunk to handle tables
    result_chunks = []
    for chunk in chunks:
        chunk_soup = BeautifulSoup(chunk, 'html.parser')
        tables = chunk_soup.find_all('table')

        if not tables:
            result_chunks.append(chunk)
            continue

        # Check if the entire chunk fits within the token limit
        if count_html_tokens(chunk, count_tag_tokens) <= max_token_limit:
            result_chunks.append(chunk)
            continue

        # The chunk has tables and exceeds the token limit, process it
        for table in tables:
            # Get the table's context (preceding and following paragraphs)
            prev_paragraph = table.find_previous('p')
            next_paragraph = table.find_next('p')

            table_html = str(table)
            table_size = count_html_tokens(table_html, count_tag_tokens)

            if table_size <= max_token_limit:
                # The table fits, try to include context
                context_html = ""
                if prev_paragraph:
                    context_html += str(prev_paragraph)

                combined_html = context_html + table_html
                combined_size = count_html_tokens(combined_html, count_tag_tokens)

                if combined_size <= max_token_limit and next_paragraph:
                    # Also include following paragraph if it fits
                    next_html = str(next_paragraph)
                    if count_html_tokens(combined_html + next_html, count_tag_tokens) <= max_token_limit:
                        combined_html += next_html

                result_chunks.append(combined_html)
            else:
                # The table itself exceeds the token limit, split it by rows
                if prev_paragraph:
                    result_chunks.append(str(prev_paragraph))

                # Get header row if exists
                header_row = table.find('thead')
                rows = table.find_all('tr')

                # Start with header
                current_chunk = "<table>"
                if header_row:
                    current_chunk += str(header_row)

                # Add body rows
                for row in rows:
                    row_html = str(row)
                    if count_html_tokens(current_chunk + row_html + "</table>",
                                       count_tag_tokens) <= max_token_limit:
                        current_chunk += row_html
                    else:
                        current_chunk += "</table>"
                        result_chunks.append(current_chunk)

                        # Start new table chunk with header if it exists
                        current_chunk = "<table>"
                        if header_row:
                            current_chunk += str(header_row)
                        current_chunk += row_html

                if current_chunk != "<table>":
                    current_chunk += "</table>"
                    result_chunks.append(current_chunk)

                if next_paragraph:
                    result_chunks.append(str(next_paragraph))

        # Add parts of the chunk that aren't tables
        table_parents = set()
        for table in tables:
            parent = table.parent
            while parent and parent.name != 'body':
                table_parents.add(parent)
                parent = parent.parent

        for element in chunk_soup.body.children if chunk_soup.body else chunk_soup.children:
            if element not in tables and element not in table_parents:
                result_chunks.append(str(element))

    return result_chunks

def _split_list_items(ol: Tag,
                    max_token_limit: int,
                    count_tag_tokens: bool) -> List[str]:
    """
    Split an ordered list into chunks that fit within the token limit.

    Args:
        ol (Tag): The ordered list tag.
        max_token_limit (int): Maximum number of tokens allowed per chunk.
        count_tag_tokens (bool): Whether to count HTML tags as tokens.

    Returns:
        List[str]: List of HTML chunks containing parts of the ordered list.
    """
    items = ol.find_all('li', recursive=False)
    if not items:
        return [str(ol)]

    chunks = []
    current_chunk = "<ol>"
    current_item_index = 1

    for item in items:
        item_html = str(item)

        if count_html_tokens(current_chunk + item_html + "</ol>", count_tag_tokens) <= max_token_limit:
            current_chunk += item_html
            current_item_index += 1
        else:
            current_chunk += "</ol>"
            chunks.append(current_chunk)

            # Start a new chunk with the correct start index
            current_chunk = f'<ol start="{current_item_index}">'
            current_chunk += item_html
            current_item_index += 1

    if current_chunk != "<ol>":
        current_chunk += "</ol>"
        chunks.append(current_chunk)

    return chunks
