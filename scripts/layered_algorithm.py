"""Layered chunking algorithm for markdown documents."""

import re
from typing import Dict, List, Optional, Set, Tuple, Union
import tiktoken

class MarkdownChunker:
    """A class for chunking markdown documents according to the specified algorithm."""

    def __init__(
        self,
        token_limit: int = 1024,
        keep_siblings_together: bool = True,
        prepend_parent_section_text: bool = True,
        encoding_name: str = "cl100k_base"
    ):
        """Initialize the chunker with specific options.

        Args:
            token_limit: Maximum tokens per chunk
            keep_siblings_together: Whether to keep sibling headings together
            prepend_parent_section_text: Whether to prepend parent section text
            encoding_name: The name of the encoding to use for tokenization
        """
        self.token_limit = token_limit
        self.keep_siblings_together = keep_siblings_together
        self.prepend_parent_section_text = prepend_parent_section_text
        self.encoding = tiktoken.get_encoding(encoding_name)
        self.used_sections = set()  # Track sections that have been included in chunks

    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in the text."""
        return len(self.encoding.encode(text))

    def is_over_token_limit(self, text: str) -> bool:
        """Check if the text is over the token limit."""
        return self.count_tokens(text) > self.token_limit

    def find_code_blocks(self, text: str) -> List[Dict]:
        """Find all code blocks in the text.

        Args:
            text: The text to analyze

        Returns:
            List of dictionaries with code block information
        """
        # Find code blocks enclosed in triple backticks
        code_block_pattern = r'```(?:[^\n]*)?(?:\n|\r\n)(.*?)```'
        code_blocks = []

        for match in re.finditer(code_block_pattern, text, re.DOTALL):
            code_blocks.append({
                'content': match.group(0),  # The whole code block including backticks
                'code': match.group(1),     # Just the code inside
                'start': match.start(),
                'end': match.end()
            })

        return code_blocks

    def is_inside_code_block(self, position: int, code_blocks: List[Dict]) -> bool:
        """Check if a position is inside a code block.

        Args:
            position: The position to check
            code_blocks: List of code blocks

        Returns:
            True if the position is inside a code block, False otherwise
        """
        for block in code_blocks:
            if block['start'] <= position < block['end']:
                return True
        return False

    def find_headings(self, text: str) -> Dict[int, List[Dict]]:
        """Find all headings in the text, organized by level.

        Args:
            text: The text to analyze

        Returns:
            Dictionary mapping heading level to list of heading info dictionaries
        """
        # First, identify all code blocks to avoid false positives
        code_blocks = self.find_code_blocks(text)

        heading_pattern = r'^(#{1,6})\s+(.+?)$'
        headings_by_level = {}

        for match in re.finditer(heading_pattern, text, re.MULTILINE):
            position = match.start()

            # Skip headings inside code blocks
            if self.is_inside_code_block(position, code_blocks):
                continue

            level = len(match.group(1))
            title = match.group(2).strip()

            if level not in headings_by_level:
                headings_by_level[level] = []

            headings_by_level[level].append({
                'level': level,
                'title': title,
                'start': position,
                'line': match.group(0),
                'id': f"h{level}-{position}"  # Unique ID for tracking
            })

        # Calculate the end position for each heading
        for level in sorted(headings_by_level.keys()):
            headings = headings_by_level[level]
            for i, heading in enumerate(headings):
                if i < len(headings) - 1:
                    heading['end'] = headings[i + 1]['start']
                else:
                    heading['end'] = len(text)

        return headings_by_level

    def extract_sections_by_level(self, text: str, level: int) -> List[Dict]:
        """Extract sections at a specific heading level.

        Args:
            text: The text to process
            level: The heading level (1 for #, 2 for ##, etc.)

        Returns:
            A list of dictionaries with section information
        """
        headings_by_level = self.find_headings(text)

        if level not in headings_by_level:
            return []

        sections = []
        headings = headings_by_level[level]

        for i, heading in enumerate(headings):
            start = heading['start']
            end = heading['end']
            content = text[start:end]

            sections.append({
                'heading': heading['title'],
                'content': content,
                'start': start,
                'end': end,
                'level': level,
                'id': heading['id']
            })

        return sections

    def find_parent_section(self, section: Dict, all_sections_by_level: Dict[int, List[Dict]]) -> Optional[Dict]:
        """Find the parent section of a given section.

        Args:
            section: The section to find the parent for
            all_sections_by_level: Dictionary mapping heading level to list of sections

        Returns:
            The parent section dictionary or None if no parent exists
        """
        if section['level'] <= 1:
            return None

        parent_level = section['level'] - 1

        if parent_level not in all_sections_by_level:
            return None

        parent_sections = all_sections_by_level[parent_level]

        for parent in parent_sections:
            if parent['start'] < section['start'] and section['end'] <= parent['end']:
                return parent

        return None

    def extract_parent_section_text(self, section: Dict, all_sections_by_level: Dict[int, List[Dict]], collected_parents: Set[str] = None) -> Tuple[str, Set[str]]:
        """Extract the content directly under the parent heading but not in any child sections.

        Args:
            section: The section to extract parent text for
            all_sections_by_level: Dictionary mapping heading level to list of sections
            collected_parents: Set of parent IDs that have already been collected

        Returns:
            Tuple of (parent section heading and text, updated set of collected parent IDs)
        """
        if collected_parents is None:
            collected_parents = set()

        parent = self.find_parent_section(section, all_sections_by_level)

        if not parent or parent['id'] in collected_parents:
            return "", collected_parents

        parent_content = parent['content']

        # Extract only the content before any child sections
        child_level = parent['level'] + 1

        if child_level in all_sections_by_level:
            relevant_children = []

            for child in all_sections_by_level[child_level]:
                if child['start'] >= parent['start'] and child['end'] <= parent['end']:
                    relevant_children.append(child)

            if relevant_children:
                # Sort children by start position
                relevant_children.sort(key=lambda x: x['start'])

                # Extract the content before the first child section
                first_child = relevant_children[0]
                parent_text = parent_content[:first_child['start'] - parent['start']]

                # Mark this parent as collected
                collected_parents.add(parent['id'])

                # Recursively collect parent's parent text
                grandparent_text, collected_parents = self.extract_parent_section_text(
                    parent, all_sections_by_level, collected_parents
                )

                return grandparent_text + parent_text, collected_parents

        # If no children, return the entire parent content
        collected_parents.add(parent['id'])

        # Recursively collect parent's parent text
        grandparent_text, collected_parents = self.extract_parent_section_text(
            parent, all_sections_by_level, collected_parents
        )

        return grandparent_text + parent_content, collected_parents

    def extract_procedures(self, text: str) -> List[Dict]:
        """Extract procedures (numbered steps) from text.

        Args:
            text: The text to process

        Returns:
            A list of dictionaries with procedure information
        """
        # Regular expression to match the start of a procedure step
        step_pattern = r'^\s*(\d+)\.\s+(.*?)$'
        step_matches = list(re.finditer(step_pattern, text, re.MULTILINE))

        if not step_matches:
            return []

        # Check for presence in code blocks
        code_blocks = self.find_code_blocks(text)
        valid_step_matches = []

        for match in step_matches:
            position = match.start()
            if not self.is_inside_code_block(position, code_blocks):
                valid_step_matches.append({
                    'match': match,
                    'start': match.start(),
                    'number': int(match.group(1)),
                    'content': match.group(2)
                })

        if not valid_step_matches:
            return []

        procedures = []
        current_steps = []

        for i, match_info in enumerate(valid_step_matches):
            match = match_info['match']
            step_number = match_info['number']
            start = match_info['start']

            # If this is the first step or the start of a new procedure (step 1)
            if not current_steps or step_number == 1:
                if current_steps:
                    # Finish the previous procedure
                    procedures.append({
                        'steps': current_steps,
                        'start': current_steps[0]['start'],
                        'end': current_steps[-1]['end']
                    })
                current_steps = []

            # Determine where this step ends
            if i < len(valid_step_matches) - 1:
                end = valid_step_matches[i + 1]['start']
            else:
                end = len(text)

            current_steps.append({
                'number': step_number,
                'content': match_info['content'],
                'start': start,
                'end': end,
                'text': text[start:end]
            })

        # Add the last procedure
        if current_steps:
            procedures.append({
                'steps': current_steps,
                'start': current_steps[0]['start'],
                'end': current_steps[-1]['end']
            })

        return procedures

    def chunk_by_headings(self, text: str, level: int = 1, chunk_ids_with_parent: Dict[str, Set[str]] = None) -> List[str]:
        """Chunk text by headings at the specified level.

        Args:
            text: The text to chunk
            level: The heading level to chunk by
            chunk_ids_with_parent: Dictionary tracking which chunks already have which parent sections

        Returns:
            A list of text chunks
        """
        # Initialize tracking of chunks with parent sections
        if chunk_ids_with_parent is None:
            chunk_ids_with_parent = {}

        # If the text is under the token limit, return it as is
        if not self.is_over_token_limit(text):
            return [text]

        # Find all sections at this level
        sections = self.extract_sections_by_level(text, level)

        # If no sections were found at this level
        if not sections:
            # If we're at the top level and no headings were found, try level 2
            if level == 1:
                return self.chunk_by_headings(text, level=2, chunk_ids_with_parent=chunk_ids_with_parent)
            # If we're already at a deeper level or reached level 6, try special elements
            elif level >= 6:
                return self.chunk_special_elements(text, chunk_ids_with_parent)
            # Otherwise, try the next heading level
            else:
                return self.chunk_by_headings(text, level=level+1, chunk_ids_with_parent=chunk_ids_with_parent)

        # Find all sections at all levels for parent text extraction
        all_sections_by_level = {}
        for l in range(1, 7):
            level_sections = self.extract_sections_by_level(text, l)
            if level_sections:
                all_sections_by_level[l] = level_sections

        chunks = []
        current_chunk = ""
        current_chunk_id = None
        current_sections = []

        # Handle any text before the first section
        if sections[0]['start'] > 0:
            preamble = text[:sections[0]['start']]
            if not self.is_over_token_limit(preamble):
                chunks.append(preamble)

        for section in sections:
            # Mark this section as used
            self.used_sections.add(section['id'])

            section_content = section['content']
            original_section_content = section_content

            # Set of parent IDs already prepended to this section
            if current_chunk_id not in chunk_ids_with_parent:
                chunk_ids_with_parent[current_chunk_id] = set()

            # If prepending parent section text is enabled and we're not at level 1
            if self.prepend_parent_section_text and level > 1:
                parent_text, parent_ids = self.extract_parent_section_text(
                    section, all_sections_by_level, set(chunk_ids_with_parent.get(current_chunk_id, set()))
                )

                if parent_text:
                    # Check if adding parent text would exceed token limit
                    combined_text = parent_text + section_content
                    if not self.is_over_token_limit(combined_text):
                        section_content = combined_text
                        if current_chunk_id:
                            chunk_ids_with_parent[current_chunk_id].update(parent_ids)

            # Check if this section itself is over the token limit
            if self.is_over_token_limit(section_content):
                # If we have sections in the current chunk, add it
                if current_sections:
                    chunks.append(current_chunk)
                    current_chunk = ""
                    current_chunk_id = None
                    current_sections = []

                # Try to chunk at the next heading level
                if level < 6:
                    sub_chunks = self.chunk_by_headings(
                        original_section_content, level + 1, chunk_ids_with_parent
                    )
                    chunks.extend(sub_chunks)
                else:
                    # If we've reached the deepest heading level, try special elements
                    sub_chunks = self.chunk_special_elements(
                        original_section_content, chunk_ids_with_parent
                    )
                    chunks.extend(sub_chunks)
                continue

            # If keeping siblings together is enabled
            if self.keep_siblings_together:
                # Check if adding this section would exceed the token limit
                if current_chunk and not self.is_over_token_limit(current_chunk + section_content):
                    current_chunk += section_content
                    current_sections.append(section)
                else:
                    # If we have a current chunk, add it before starting a new one
                    if current_chunk:
                        chunks.append(current_chunk)
                    current_chunk = section_content
                    current_chunk_id = f"chunk-{len(chunks)}"
                    current_sections = [section]

                    # Initialize parent tracking for this chunk
                    chunk_ids_with_parent[current_chunk_id] = set()

                    # Add any parent IDs that were prepended
                    if self.prepend_parent_section_text and level > 1:
                        _, parent_ids = self.extract_parent_section_text(
                            section, all_sections_by_level, set()
                        )
                        chunk_ids_with_parent[current_chunk_id].update(parent_ids)
            else:
                # Each section is its own chunk
                chunks.append(section_content)

        # Add the last chunk if there is any content left
        if current_chunk:
            chunks.append(current_chunk)

        # Check if all chunks are under the token limit
        over_limit_chunks = [chunk for chunk in chunks if self.is_over_token_limit(chunk)]

        if over_limit_chunks:
            # For chunks still over the limit, try to chunk at the next level
            final_chunks = []
            for chunk in chunks:
                if self.is_over_token_limit(chunk):
                    if level < 6:
                        sub_chunks = self.chunk_by_headings(
                            chunk, level + 1, chunk_ids_with_parent
                        )
                    else:
                        sub_chunks = self.chunk_special_elements(
                            chunk, chunk_ids_with_parent
                        )
                    final_chunks.extend(sub_chunks)
                else:
                    final_chunks.append(chunk)
            return final_chunks

        return chunks

    def chunk_procedure(self, text: str, procedure: Dict) -> List[str]:
        """Chunk a procedure that is over the token limit.

        Args:
            text: The full text
            procedure: Dictionary with procedure information

        Returns:
            A list of text chunks
        """
        procedure_text = text[procedure['start']:procedure['end']]

        # If the procedure is under the token limit, return it as is
        if not self.is_over_token_limit(procedure_text):
            return [procedure_text]

        # We need to split the procedure, but only between steps
        chunks = []
        current_chunk = ""

        for step in procedure['steps']:
            step_text = text[step['start']:step['end']]

            # If adding this step would exceed the token limit
            if current_chunk and self.is_over_token_limit(current_chunk + step_text):
                chunks.append(current_chunk)
                current_chunk = step_text
            else:
                current_chunk += step_text

        # Add the last chunk if there is any content left
        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def chunk_code_block(self, text: str, code_block: Dict) -> List[str]:
        """Chunk a code block that is over the token limit.

        Args:
            text: The full text
            code_block: Dictionary with code block information

        Returns:
            A list of text chunks
        """
        code_text = code_block['content']

        # If the code block is under the token limit, return it as is
        if not self.is_over_token_limit(code_text):
            return [code_text]

        # We need to split the code block, but only between lines
        lines = code_block['code'].split("\n")
        chunks = []
        current_chunk = "```\n"  # Start with opening backticks

        for line in lines:
            line_with_newline = line + "\n"

            # If adding this line would exceed the token limit
            if self.is_over_token_limit(current_chunk + line_with_newline + "```"):
                current_chunk += "```"  # Close the code block
                chunks.append(current_chunk)
                current_chunk = "```\n" + line_with_newline  # Start a new code block
            else:
                current_chunk += line_with_newline

        # Add the last chunk if there is any content left
        if current_chunk != "```\n":
            current_chunk += "```"  # Close the code block
            chunks.append(current_chunk)

        return chunks

    def chunk_special_elements(self, text: str, chunk_ids_with_parent: Dict[str, Set[str]] = None) -> List[str]:
        """Chunk text by special elements like procedures and code blocks.

        Args:
            text: The text to chunk
            chunk_ids_with_parent: Dictionary tracking which chunks already have which parent sections

        Returns:
            A list of text chunks
        """
        # Initialize tracking of chunks with parent sections
        if chunk_ids_with_parent is None:
            chunk_ids_with_parent = {}

        # If the text is under the token limit, return it as is
        if not self.is_over_token_limit(text):
            return [text]

        # First look for code blocks (prioritize keeping code blocks intact)
        code_blocks = self.find_code_blocks(text)

        # Then look for procedures
        procedures = self.extract_procedures(text)

        # If no special elements were found, fall back to chunking by paragraphs
        if not code_blocks and not procedures:
            return self.chunk_by_paragraphs(text)

        # Combine procedures and code blocks, sorted by start position
        special_elements = []
        for procedure in procedures:
            special_elements.append({
                'type': 'procedure',
                'data': procedure,
                'start': procedure['start'],
                'end': procedure['end']
            })

        for code_block in code_blocks:
            special_elements.append({
                'type': 'code_block',
                'data': code_block,
                'start': code_block['start'],
                'end': code_block['end']
            })

        special_elements.sort(key=lambda x: x['start'])

        # Process the text with special elements
        chunks = []
        current_chunk = ""
        current_chunk_id = None
        last_end = 0

        for element in special_elements:
            # Get the text before this element
            before_text = text[last_end:element['start']]

            if element['type'] == 'code_block':
                code_block = element['data']
                code_block_chunks = self.chunk_code_block(text, code_block)

                # Try to combine with the text before
                if before_text and not self.is_over_token_limit(before_text + code_block_chunks[0]):
                    combined_chunk = before_text + code_block_chunks[0]
                    if current_chunk and not self.is_over_token_limit(current_chunk + combined_chunk):
                        current_chunk += combined_chunk
                    else:
                        if current_chunk:
                            chunks.append(current_chunk)
                        current_chunk = combined_chunk
                        current_chunk_id = f"chunk-{len(chunks)}"
                        chunk_ids_with_parent[current_chunk_id] = set()

                    # Add the rest of the code block chunks
                    for chunk in code_block_chunks[1:]:
                        chunks.append(chunk)
                else:
                    # Add before_text as its own chunk if it's not empty
                    if before_text:
                        if current_chunk and not self.is_over_token_limit(current_chunk + before_text):
                            current_chunk += before_text
                        else:
                            if current_chunk:
                                chunks.append(current_chunk)
                            if self.is_over_token_limit(before_text):
                                before_chunks = self.chunk_by_paragraphs(before_text)
                                chunks.extend(before_chunks)
                            else:
                                chunks.append(before_text)
                            current_chunk = ""
                            current_chunk_id = None

                    # Add the code block chunks
                    if current_chunk and not self.is_over_token_limit(current_chunk + code_block_chunks[0]):
                        current_chunk += code_block_chunks[0]
                        for chunk in code_block_chunks[1:]:
                            chunks.append(chunk)
                    else:
                        if current_chunk:
                            chunks.append(current_chunk)
                        chunks.extend(code_block_chunks)
                        current_chunk = ""
                        current_chunk_id = None

            elif element['type'] == 'procedure':
                procedure = element['data']
                procedure_chunks = self.chunk_procedure(text, procedure)

                # Try to combine with the text before
                if before_text and not self.is_over_token_limit(before_text + procedure_chunks[0]):
                    combined_chunk = before_text + procedure_chunks[0]
                    if current_chunk and not self.is_over_token_limit(current_chunk + combined_chunk):
                        current_chunk += combined_chunk
                    else:
                        if current_chunk:
                            chunks.append(current_chunk)
                        current_chunk = combined_chunk
                        current_chunk_id = f"chunk-{len(chunks)}"
                        chunk_ids_with_parent[current_chunk_id] = set()

                    # Add the rest of the procedure chunks
                    for chunk in procedure_chunks[1:]:
                        chunks.append(chunk)
                else:
                    # Add before_text as its own chunk if it's not empty
                    if before_text:
                        if current_chunk and not self.is_over_token_limit(current_chunk + before_text):
                            current_chunk += before_text
                        else:
                            if current_chunk:
                                chunks.append(current_chunk)
                            if self.is_over_token_limit(before_text):
                                before_chunks = self.chunk_by_paragraphs(before_text)
                                chunks.extend(before_chunks)
                            else:
                                chunks.append(before_text)
                            current_chunk = ""
                            current_chunk_id = None

                    # Add the procedure chunks
                    if current_chunk and not self.is_over_token_limit(current_chunk + procedure_chunks[0]):
                        current_chunk += procedure_chunks[0]
                        for chunk in procedure_chunks[1:]:
                            chunks.append(chunk)
                    else:
                        if current_chunk:
                            chunks.append(current_chunk)
                        chunks.extend(procedure_chunks)
                        current_chunk = ""
                        current_chunk_id = None

            last_end = element['end']

        # Add any remaining text
        if last_end < len(text):
            remaining_text = text[last_end:]

            if remaining_text:
                if current_chunk and not self.is_over_token_limit(current_chunk + remaining_text):
                    current_chunk += remaining_text
                else:
                    if current_chunk:
                        chunks.append(current_chunk)

                    # If the remaining text is over the limit, chunk it by paragraphs
                    if self.is_over_token_limit(remaining_text):
                        remaining_chunks = self.chunk_by_paragraphs(remaining_text)
                        chunks.extend(remaining_chunks)
                    else:
                        chunks.append(remaining_text)

                    current_chunk = ""
                    current_chunk_id = None

        # Add the last chunk if there is any content left
        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def chunk_by_paragraphs(self, text: str) -> List[str]:
        """Chunk text by paragraphs as a last resort.

        Args:
            text: The text to chunk

        Returns:
            A list of text chunks
        """
        # If the text is under the token limit, return it as is
        if not self.is_over_token_limit(text):
            return [text]

        # Split by double newlines (paragraph breaks)
        paragraphs = re.split(r'\n\s*\n', text)

        chunks = []
        current_chunk = ""

        for paragraph in paragraphs:
            # Skip empty paragraphs
            if not paragraph.strip():
                continue

            # If the paragraph alone exceeds the token limit
            if self.is_over_token_limit(paragraph):
                # Add current chunk if it exists
                if current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = ""

                # Split the paragraph by sentences
                sentences = re.split(r'(?<=[.!?])\s+', paragraph)
                current_sentence_chunk = ""

                for sentence in sentences:
                    # If the sentence alone exceeds the token limit, we'll have to accept it
                    if self.is_over_token_limit(sentence):
                        if current_sentence_chunk:
                            chunks.append(current_sentence_chunk)
                        chunks.append(sentence)
                        current_sentence_chunk = ""
                    # If adding this sentence would exceed the token limit
                    elif current_sentence_chunk and self.is_over_token_limit(current_sentence_chunk + " " + sentence):
                        chunks.append(current_sentence_chunk)
                        current_sentence_chunk = sentence
                    else:
                        if current_sentence_chunk:
                            current_sentence_chunk += " " + sentence
                        else:
                            current_sentence_chunk = sentence

                # Add the last sentence chunk if there is any content left
                if current_sentence_chunk:
                    chunks.append(current_sentence_chunk)
            else:
                # Try to add to the current chunk
                if current_chunk:
                    combined_chunk = current_chunk + "\n\n" + paragraph
                    if not self.is_over_token_limit(combined_chunk):
                        current_chunk = combined_chunk
                    else:
                        chunks.append(current_chunk)
                        current_chunk = paragraph
                else:
                    current_chunk = paragraph

        # Add the last chunk if there is any content left
        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def process_standalone_sections(self, chunks: List[str]) -> List[str]:
        """Remove standalone sections that have been prepended to other chunks.

        Args:
            chunks: List of text chunks

        Returns:
            List of processed chunks
        """
        result_chunks = []

        for chunk in chunks:
            # Skip empty chunks
            if not chunk.strip():
                continue

            result_chunks.append(chunk)

        return result_chunks

    def chunk_document(self, text: str) -> List[str]:
        """Chunk the document according to the algorithm.

        Args:
            text: The text to chunk

        Returns:
            A list of text chunks
        """
        # Reset the set of used sections
        self.used_sections = set()

        # If the whole document is under the token limit, return it as is
        if not self.is_over_token_limit(text):
            return [text]

        # Start by trying to chunk by top-level headings
        chunks = self.chunk_by_headings(text, level=1)

        # Process chunks to remove standalone sections that have been prepended
        return self.process_standalone_sections(chunks)

def chunk_markdown(
    text: str,
    token_limit: int = 1024,
    keep_siblings_together: bool = True,
    prepend_parent_section_text: bool = True
) -> List[str]:
    """Chunk markdown text according to the algorithm.

    Args:
        text: The text to chunk
        token_limit: Maximum tokens per chunk
        keep_siblings_together: Whether to keep sibling headings together
        prepend_parent_section_text: Whether to prepend parent section text

    Returns:
        A list of text chunks
    """
    chunker = MarkdownChunker(
        token_limit=token_limit,
        keep_siblings_together=keep_siblings_together,
        prepend_parent_section_text=prepend_parent_section_text
    )
    return chunker.chunk_document(text)
