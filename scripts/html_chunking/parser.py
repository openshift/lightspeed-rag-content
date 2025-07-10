"""
HTML parser module for identifying document structure.
"""

from typing import Tuple, Optional, Union, Set, Any
from bs4 import BeautifulSoup, Tag, NavigableString
import re
from dataclasses import dataclass, field

# Constants
MAX_SEARCH_DEPTH = 10
MAX_PROCEDURE_SEARCH_DEPTH = 5
MAX_CODE_BLOCKS = 100
MAX_TABLES = 50
MAX_TABLE_ROWS = 100


@dataclass
class HtmlSection:
    """
    Represents a section of HTML content defined by a heading and its content.
    
    This class provides a lightweight representation of document structure that
    can be used for analyzing and chunking HTML content.
    """
    heading_tag: Optional[Tag] = None
    level: int = 0
    parent: Optional['HtmlSection'] = None
    content: list[Union[Tag, NavigableString, 'HtmlSection']] = field(default_factory=list)
    children: list['HtmlSection'] = field(default_factory=list)
    html: str = ""
    
    def add_content(self, content: Union[Tag, NavigableString, 'HtmlSection']) -> None:
        """Add content to this section."""
        self.content.append(content)
    
    def add_child(self, child: 'HtmlSection') -> None:
        """Add a child section to this section."""
        self.children.append(child)
        child.parent = self
    
    def get_heading_text(self) -> str:
        """Get the text of the heading for this section."""
        if self.heading_tag:
            try:
                return self.heading_tag.get_text(strip=True)
            except Exception:
                # Fallback if BeautifulSoup operation fails
                return str(self.heading_tag)
        return ""
    
    def get_html(self) -> str:
        """Get the HTML representation of this section."""
        if self.html:
            return self.html
        
        try:
            result = []
            if self.heading_tag:
                result.append(str(self.heading_tag))
            
            for item in self.content:
                if isinstance(item, (Tag, NavigableString)):
                    result.append(str(item))
                elif isinstance(item, HtmlSection):
                    result.append(item.get_html())
            
            self.html = "".join(result)
            return self.html
        except Exception as e:
            # Fallback in case of error
            if self.heading_tag:
                return str(self.heading_tag)
            return ""


def parse_html(html_content: str) -> Tuple[BeautifulSoup, HtmlSection]:
    """
    Parse HTML content and build a hierarchical section structure.
    
    Args:
        html_content: The HTML content to parse.
    
    Returns:
        A tuple containing the parsed BeautifulSoup object and the root section.
    """
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        root_section = HtmlSection()
        
        # Process document in non-recursive way to prevent stack overflow
        section_stack = [root_section]
        current_section = root_section
        
        body = soup.body or soup
        
        # First pass: identify all headings
        all_headings = []
        for element in body.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            if element.name and re.match(r'h[1-6]$', element.name):
                level = int(element.name[1])
                all_headings.append((element, level))
        
        # Sort headings by their position in the document
        all_headings.sort(key=lambda x: _get_element_position(soup, x[0]))
        
        # Initialize section map to keep track of hierarchy
        section_map = {0: root_section}
        
        # Create section hierarchy based on heading levels
        for heading, level in all_headings:
            # Find parent section - closest ancestor with lower level
            parent_level = level - 1
            while parent_level > 0 and parent_level not in section_map:
                parent_level -= 1
                
            parent_section = section_map.get(parent_level, root_section)
            
            # Create new section
            new_section = HtmlSection(heading, level, parent_section)
            parent_section.add_child(new_section)
            
            # Update section map
            section_map[level] = new_section
            
            # Clear any higher level sections from the map
            # (they can't be parents to sections after this one)
            for l in list(section_map.keys()):
                if l > level:
                    del section_map[l]
        
        # Second pass: assign content to sections
        if all_headings:
            # Create list of section boundaries
            boundaries = []
            for heading, level in all_headings:
                boundaries.append((heading, 'start', level))
                
            # Sort boundaries by document position
            boundaries.sort(key=lambda x: _get_element_position(soup, x[0]))
            
            # Process content between boundaries
            current_level = 0
            current_section = root_section
            
            for element in body.children:
                if not element or (isinstance(element, str) and not element.strip()):
                    continue
                    
                is_section_start = False
                new_level = None
                
                if isinstance(element, Tag) and element.name and re.match(r'h[1-6]$', element.name):
                    level = int(element.name[1])
                    for section in _flatten_sections(root_section):
                        if section.heading_tag and section.heading_tag == element:
                            is_section_start = True
                            new_level = level
                            current_section = section
                            break
                
                if not is_section_start:
                    current_section.add_content(element)
        else:
            for element in body.children:
                if element:
                    root_section.add_content(element)
        
        return soup, root_section
    except Exception as e:
        # Fallback if parsing fails
        soup = BeautifulSoup(html_content, 'html.parser')
        root_section = HtmlSection()
        
        for element in soup.children:
            if element:
                root_section.add_content(element)
                
        return soup, root_section


def _get_element_position(soup: BeautifulSoup, element: Tag) -> int:
    """
    Get the position of an element in the document.
    
    Args:
        soup: The BeautifulSoup object.
        element: The element to find.
        
    Returns:
        The position index of the element.
    """
    all_elements = list(soup.find_all())
    if element in all_elements:
        return all_elements.index(element)
    return -1


def _flatten_sections(section: HtmlSection) -> list[HtmlSection]:
    """
    Flatten a section hierarchy into a list.
    
    Args:
        section: The root section.
        
    Returns:
        A flattened list of all sections.
    """
    result = [section]
    for child in section.children:
        result.extend(_flatten_sections(child))
    return result


def identify_special_sections(soup: BeautifulSoup) -> dict[str, list[dict]]:
    """
    Identify special sections in the HTML that need special handling during chunking.
    
    Args:
        soup: The parsed BeautifulSoup object.
    
    Returns:
        A dictionary with lists of special sections by type.
    """
    try:
        special_sections = {
            'procedures': identify_procedure_sections(soup),
            'code_blocks': identify_code_blocks(soup),
            'tables': identify_tables(soup)
        }
        
        return special_sections
    except Exception as e:
        return {
            'procedures': [],
            'code_blocks': [],
            'tables': []
        }


def identify_procedure_sections(soup: BeautifulSoup) -> list[dict]:
    """
    Identify procedure sections in the HTML.
    
    A procedure section typically contains:
    - A heading (e.g., h3)
    - Introductory text
    - Prerequisites section (optional)
    - The word "Procedure" on its own line
    - An ordered list of steps (the actual procedure)
    
    Args:
        soup: The parsed BeautifulSoup object.
    
    Returns:
        A list of procedure sections with their components.
    """
    procedures = []
    
    try:
        # Multiple ways to identify procedures
        procedure_markers = []
        for element in soup.find_all(string=lambda text: text and "Procedure" in text):
            if element.parent and element.parent.name not in ('script', 'style'):
                procedure_markers.append(element)
                
        ordered_lists = soup.find_all('ol')
        
        processed_lists = set()
        
        for marker in procedure_markers:
            if not marker or not marker.parent:
                continue
                
            ol = None
            current = marker.parent
            search_depth = 0
            
            while current and search_depth < MAX_PROCEDURE_SEARCH_DEPTH:
                search_depth += 1
                if current.name == 'ol':
                    ol = current
                    break
                
                next_sibling = current.find_next_sibling()
                if next_sibling and next_sibling.name == 'ol':
                    ol = next_sibling
                    break
                    
                ol_in_children = current.find('ol')
                if ol_in_children:
                    ol = ol_in_children
                    break
                    
                current = current.find_next()
            
            if not ol or id(ol) in processed_lists:
                continue
                
            heading = _find_closest_heading(marker.parent)
            
            intro = []
            if heading:
                current = heading.find_next()
                while current and current != marker.parent and current != ol:
                    if current.name not in ('script', 'style'):
                        intro.append(current)
                    current = current.find_next()
            
            prerequisites = None
            for element in intro:
                if isinstance(element, Tag) and element.get_text() and "Prerequisites" in element.get_text():
                    prerequisites = element
                    break
            
            procedures.append({
                'heading': heading,
                'intro': intro,
                'prerequisites': prerequisites,
                'marker': marker.parent,
                'steps': ol
            })
            
            processed_lists.add(id(ol))
        
        for ol in ordered_lists:
            if id(ol) in processed_lists:
                continue
                
            # Check if this has procedure-like structure
            has_structure = False
            for li in ol.find_all('li', recursive=False):
                if li.find('p') or li.find('pre') or li.find('code'):
                    has_structure = True
                    break
                    
            if not has_structure:
                continue
                
            # Find heading for this ol
            heading = _find_closest_heading(ol)
            
            # Find introduction elements
            intro = []
            if heading:
                current = heading.find_next()
                while current and current != ol:
                    if current.name not in ('script', 'style'):
                        intro.append(current)
                    current = current.find_next()
            
            # Check for prerequisites section
            prerequisites = None
            for element in intro:
                if isinstance(element, Tag) and element.get_text() and "Prerequisites" in element.get_text():
                    prerequisites = element
                    break
            
            # Look for explicit procedure marker
            marker = None
            for element in intro:
                if isinstance(element, Tag) and element.get_text() and "Procedure" in element.get_text():
                    marker = element
                    break
            
            # Add to procedures if it looks like a procedure
            if heading or marker or prerequisites:
                procedures.append({
                    'heading': heading,
                    'intro': intro,
                    'prerequisites': prerequisites,
                    'marker': marker,
                    'steps': ol
                })
                
                # Mark as processed
                processed_lists.add(id(ol))
        
        return procedures
    except Exception as e:
        # Return empty list if procedure identification fails
        return []


def _find_closest_heading(element: Tag) -> Optional[Tag]:
    """
    Find the closest heading above an element.
    
    Args:
        element: The element to find a heading for.
        
    Returns:
        The closest heading, or None if not found.
    """
    if not element:
        return None
        
    # Check previous siblings
    current = element
    search_depth = 0
    
    while current and search_depth < MAX_SEARCH_DEPTH:
        search_depth += 1
        current = current.previous_sibling
        
        if current and isinstance(current, Tag) and current.name and re.match(r'h[1-6]$', current.name):
            return current
    
    # Check parent's previous siblings
    if element.parent:
        return _find_closest_heading(element.parent)
        
    return None


def identify_code_blocks(soup: BeautifulSoup) -> list[dict]:
    """
    Identify code blocks in the HTML.
    
    Code blocks are typically found within <pre>, <code>, or similar elements.
    
    Args:
        soup: The parsed BeautifulSoup object.
    
    Returns:
        A list of code blocks with their context.
    """
    code_blocks = []
    
    try:
        # Find all code blocks
        pre_tags = soup.find_all('pre', limit=MAX_CODE_BLOCKS)  # Limit to prevent excessive processing
        code_tags = soup.find_all('code', limit=MAX_CODE_BLOCKS)
        
        # Process pre tags
        processed_tags = set()
        
        for pre in pre_tags:
            # Skip if already processed
            if id(pre) in processed_tags:
                continue
                
            processed_tags.add(id(pre))
            
            # Skip if this pre tag is inside a code tag that we'll process later
            if pre.parent and pre.parent.name == 'code' and pre.parent in code_tags:
                continue
                
            # Find the previous paragraph for context
            prev_paragraph = pre.find_previous('p')
            
            # Find the next paragraph
            next_paragraph = pre.find_next('p')
            
            code_blocks.append({
                'block': pre,
                'prev_paragraph': prev_paragraph,
                'next_paragraph': next_paragraph
            })
        
        # Process code tags (that aren't inside pre tags)
        for code in code_tags:
            # Skip if already processed
            if id(code) in processed_tags:
                continue
                
            processed_tags.add(id(code))
            
            # Skip if this code tag is inside a pre tag that we've already processed
            if code.parent and code.parent.name == 'pre' and id(code.parent) in processed_tags:
                continue
                
            # Find the previous paragraph for context
            prev_paragraph = code.find_previous('p')
            
            # Find the next paragraph
            next_paragraph = code.find_next('p')
            
            code_blocks.append({
                'block': code,
                'prev_paragraph': prev_paragraph,
                'next_paragraph': next_paragraph
            })
        
        return code_blocks
    except Exception as e:
        # Return empty list if code block identification fails
        return []


def identify_tables(soup: BeautifulSoup) -> list[dict]:
    """
    Identify tables in the HTML.
    
    Args:
        soup: The parsed BeautifulSoup object.
    
    Returns:
        A list of tables with their context.
    """
    tables = []
    
    try:
        # Find all tables, including those in custom components like rh-table
        table_tags = soup.find_all(['table', 'rh-table'], limit=MAX_TABLES)
        
        # For custom table components, extract the actual table
        expanded_tables = []
        for tag in table_tags:
            if tag.name == 'rh-table':
                # Look for nested table
                nested_table = tag.find('table')
                if nested_table:
                    expanded_tables.append(nested_table)
                else:
                    expanded_tables.append(tag)
            else:
                expanded_tables.append(tag)
        
        for table in expanded_tables:
            # Find the previous paragraph for context
            prev_paragraph = table.find_previous('p')
            
            # Find the next paragraph
            next_paragraph = table.find_next('p')
            
            # Get header and rows safely
            header = None
            try:
                header = table.find('thead')
            except Exception:
                pass
                
            rows = []
            try:
                # Get rows not in header
                if header:
                    header_rows = set(id(row) for row in header.find_all('tr'))
                    all_rows = table.find_all('tr', limit=MAX_TABLE_ROWS)
                    rows = [row for row in all_rows if id(row) not in header_rows]
                else:
                    rows = table.find_all('tr', limit=MAX_TABLE_ROWS)
            except Exception:
                pass
            
            # Also check for captions or titles
            caption = table.find('caption') if hasattr(table, 'find') else None
            
            tables.append({
                'table': table,
                'prev_paragraph': prev_paragraph,
                'next_paragraph': next_paragraph,
                'header': header,
                'caption': caption,
                'rows': rows
            })
        
        return tables
    except Exception as e:
        # Return empty list if table identification fails
        return []
