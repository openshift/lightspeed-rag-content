from typing import List, Dict, Any, Tuple, Optional, Union
from bs4 import BeautifulSoup, Tag, NavigableString
import re

class HtmlSection:
    """
    Represents a section of HTML content defined by a heading and its content.
    """
    def __init__(self, heading_tag: Optional[Tag] = None, level: int = 0, parent: Optional['HtmlSection'] = None):
        self.heading_tag = heading_tag
        self.level = level
        self.parent = parent
        self.content = []  # All content within this section
        self.children = []  # Child sections (subsections)
        self.html = ""  # Complete HTML for this section
    
    def add_content(self, content: Union[Tag, NavigableString, 'HtmlSection']):
        """Add content to this section."""
        self.content.append(content)
    
    def add_child(self, child: 'HtmlSection'):
        """Add a child section to this section."""
        self.children.append(child)
        child.parent = self
    
    def get_heading_text(self) -> str:
        """Get the text of the heading for this section."""
        if self.heading_tag:
            return self.heading_tag.get_text(strip=True)
        return ""
    
    def get_html(self) -> str:
        """Get the HTML representation of this section."""
        if self.html:
            return self.html
        
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
    
    def __str__(self) -> str:
        heading = self.get_heading_text() if self.heading_tag else "Root"
        return f"Section({heading}, level={self.level}, children={len(self.children)})"
    
    def __repr__(self) -> str:
        return self.__str__()

def parse_html(html_content: str) -> Tuple[BeautifulSoup, HtmlSection]:
    """
    Parse HTML content and build a hierarchical section structure.
    
    Args:
        html_content (str): The HTML content to parse.
    
    Returns:
        Tuple[BeautifulSoup, HtmlSection]: The parsed BeautifulSoup object and the root section.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    root_section = HtmlSection()
    current_section = root_section
    section_stack = []
    
    # Find all heading tags (h1-h6) and content between them
    body = soup.body or soup
    
    for element in body.children:
        if not isinstance(element, Tag):
            continue
        
        if element.name and re.match(r'h[1-6]$', element.name):
            level = int(element.name[1])
            
            # Go back up the section stack if needed
            while section_stack and section_stack[-1].level >= level:
                section_stack.pop()
            
            # Create a new section
            parent_section = section_stack[-1] if section_stack else root_section
            new_section = HtmlSection(element, level, parent_section)
            parent_section.add_child(new_section)
            
            section_stack.append(new_section)
            current_section = new_section
        else:
            # Add content to the current section
            current_section.add_content(element)
    
    return soup, root_section

def identify_procedure_sections(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """
    Identify procedure sections in the HTML.
    
    A procedure section typically contains:
    - A heading (e.g., h3)
    - Introductory text
    - Prerequisites section (optional)
    - The word "Procedure" on its own line
    - An ordered list of steps (the actual procedure)
    
    Args:
        soup (BeautifulSoup): The parsed BeautifulSoup object.
    
    Returns:
        List[Dict[str, Any]]: A list of procedure sections with their components.
    """
    procedures = []
    processed_ols = set()  # Track ordered lists that we've already processed
    
    # Look for elements containing the word "Procedure"
    procedure_markers = soup.find_all(string=lambda text: text and "Procedure" in text)
    
    for marker in procedure_markers:
        # Find the nearest heading above
        heading = None
        current = marker.parent
        while current and current.name != 'body' and not heading:
            prev = current.find_previous_sibling()
            while prev and not heading:
                if prev.name and re.match(r'h[1-6]$', prev.name):
                    heading = prev
                    break
                prev = prev.find_previous_sibling()
            current = current.parent
        
        # Find the ordered list (procedure steps)
        ol = marker.parent.find_next('ol')
        if not ol:
            continue
            
        # Skip if we've already processed this ordered list
        if id(ol) in processed_ols:
            continue
            
        # Track this ordered list
        processed_ols.add(id(ol))
        
        # Find nearest section container for context
        section_container = None
        parent = marker.parent
        while parent and parent.name != 'body':
            if parent.name == 'div' and 'sectionbody' in parent.get('class', []):
                section_container = parent
                break
            parent = parent.parent
        
        # Skip procedure sections without proper context if we've already found one with context
        if not section_container and any(proc.get('section_container') for proc in procedures):
            continue
        
        # Find prerequisites section if it exists
        prerequisites = None
        prereq_headings = soup.find_all(string=lambda text: text and "Prerequisites" in text)
        for prereq_heading in prereq_headings:
            if prereq_heading.parent.name and re.match(r'h[1-6]$', prereq_heading.parent.name):
                if heading and prereq_heading.parent.get_text() > heading.get_text():
                    prerequisites = prereq_heading.parent
                    break
        
        # Get introductory text
        intro_text = []
        if heading:
            current = heading.next_sibling
            while current and current != marker.parent and current != prerequisites:
                if isinstance(current, (Tag, NavigableString)) and current.name != 'script':
                    intro_text.append(current)
                current = current.next_sibling
        
        procedures.append({
            'heading': heading,
            'intro': intro_text,
            'prerequisites': prerequisites,
            'marker': marker.parent,
            'steps': ol,
            'section_container': section_container
        })
    
    return procedures
