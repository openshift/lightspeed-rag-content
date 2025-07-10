import unittest
from unittest.mock import patch
from bs4 import BeautifulSoup

# Add the parent directory to the path to allow direct import of html_chunking
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from html_chunking.chunker import chunk_html

# --- Mock Tokenizer ---
# This mock tokenizer provides predictable token counts for testing purposes.
def mock_count_html_tokens(html_string, count_tag_tokens=True):
    """
    A mock token counting function.
    Counts 1 token per word and 10 tokens per tag for consistent testing.
    """
    if not isinstance(html_string, str):
        html_string = str(html_string)
    soup = BeautifulSoup(html_string, 'html.parser')
    text = soup.get_text()
    words = text.split()
    word_tokens = len(words)
    tag_tokens = 0
    if count_tag_tokens:
        tags = soup.find_all(True)
        tag_tokens = len(tags) * 10
    return word_tokens + tag_tokens

@patch('html_chunking.chunker.count_html_tokens', new=mock_count_html_tokens)
class TestHtmlChunker(unittest.TestCase):

    def test_small_input_no_chunking(self):
        """Tests that HTML smaller than the max_token_limit is not chunked."""
        html = "<html><head><title>Test Title</title></head><body><p>This is a small test.</p></body></html>"
        chunks = chunk_html(html, "http://example.com/small", max_token_limit=100)
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0].text, html)
        self.assertEqual(chunks[0].metadata["docs_url"], "http://example.com/small")
        self.assertEqual(chunks[0].metadata["title"], "Test Title")
        self.assertEqual(chunks[0].metadata["section_title"], "Test Title")

    def test_basic_splitting(self):
        """Tests basic splitting of multiple paragraphs."""
        html = "<html><head><title>Basic Splitting</title></head><body>"
        for i in range(10):
            html += f"<p>This is paragraph {i}. It contains several words to simulate content.</p>"
        html += "</body></html>"
        chunks = chunk_html(html, "http://example.com/basic", max_token_limit=100)
        self.assertEqual(len(chunks), 3)
        self.assertTrue(all(mock_count_html_tokens(c.text) <= 110 for c in chunks))
        self.assertIn("paragraph 0", chunks[0].text)
        self.assertIn("paragraph 9", chunks[-1].text)
        self.assertEqual(chunks[0].metadata["title"], "Basic Splitting")

    def test_oversized_element_splitting(self):
        """Tests that a single element larger than the limit is recursively split."""
        long_text = "word " * 200
        html = f"<html><head><title>Oversized</title></head><body><div>{long_text}</div></body></html>"
        chunks = chunk_html(html, "http://example.com/oversized", max_token_limit=100)
        self.assertGreater(len(chunks), 1)
        full_text = "".join(BeautifulSoup(c.text, 'html.parser').get_text() for c in chunks)
        self.assertIn("word", full_text)
        self.assertGreater(len(full_text), 500)
        self.assertEqual(chunks[0].metadata["title"], "Oversized")

    def test_table_splitting(self):
        """Tests that large tables are split, preserving the header in each chunk."""
        header = "<thead><tr><th>Header 1</th><th>Header 2</th></tr></thead>"
        rows = "".join([f"<tr><td>Row {i} Col 1</td><td>Row {i} Col 2</td></tr>" for i in range(20)])
        html = f"<html><head><title>Table Test</title></head><body><table>{header}<tbody>{rows}</tbody></table></body></html>"
        chunks = chunk_html(html, "http://example.com/table", max_token_limit=100)
        self.assertGreater(len(chunks), 1)
        for chunk in chunks:
            self.assertIn("<thead>", chunk.text)
            self.assertIn("Header 1", chunk.text)
            self.assertIn("</table>", chunk.text)
            self.assertEqual(chunk.metadata["title"], "Table Test")
        self.assertIn("Row 0", chunks[0].text)
        self.assertNotIn("Row 19", chunks[0].text)
        self.assertIn("Row 19", chunks[-1].text)

    def test_list_splitting(self):
        """Tests that large lists are split correctly."""
        items = "".join([f"<li>Item {i} is here.</li>" for i in range(30)])
        html = f"<html><head><title>List Test</title></head><body><ul>{items}</ul></body></html>"
        chunks = chunk_html(html, "http://example.com/list", max_token_limit=100)
        self.assertGreater(len(chunks), 1)
        for chunk in chunks:
            self.assertIn("<ul ", chunk.text)
            self.assertIn("</ul>", chunk.text)
            self.assertEqual(chunk.metadata["title"], "List Test")
        self.assertIn("Item 0", chunks[0].text)
        self.assertIn("Item 29", chunks[-1].text)

    def test_metadata_and_section_titles(self):
        """Tests the generation of metadata with correct anchors and section titles."""
        html = """
        <html><head><title>Main Document Title</title></head><body>
            <section id="intro"><h1>Introduction</h1><p>Text about intro.</p></section>
            <div id="main-content">
                <h2 id="topic1">Topic 1</h2><p>Content 1</p>
                <p>More content 1, still under Topic 1.</p>
            </div>
            <section id="conclusion">
                <p>Conclusion text, still under Topic 1 technically.</p>
                <h3 id="final-thoughts">Final Thoughts</h3><p>Final words.</p>
            </section>
        </body></html>
        """
        chunks = chunk_html(html, "http://example.com/meta", max_token_limit=25)
        
        self.assertGreaterEqual(len(chunks), 4)

        # Check document title consistency
        for chunk in chunks:
            self.assertEqual(chunk.metadata["title"], "Main Document Title")

        # Check section titles and anchors
        intro_chunk = next(c for c in chunks if "Introduction" in c.text)
        self.assertIn(intro_chunk.metadata["docs_url"], ["http://example.com/meta#intro", "http://example.com/meta"])
        self.assertEqual(intro_chunk.metadata["section_title"], "Introduction")

        topic1_chunks = [c for c in chunks if "Topic 1" in c.text or "Content 1" in c.text]
        self.assertTrue(all(c.metadata["docs_url"] == "http://example.com/meta#topic1" for c in topic1_chunks))
        self.assertTrue(all(c.metadata["section_title"] == "Topic 1" for c in topic1_chunks))

        conclusion_chunk = next(c for c in chunks if "Conclusion text" in c.text)
        self.assertEqual(conclusion_chunk.metadata["section_title"], "Topic 1") # Inherited from previous heading

        final_thoughts_chunk = next(c for c in chunks if "Final words" in c.text)
        self.assertEqual(final_thoughts_chunk.metadata["docs_url"], "http://example.com/meta#final-thoughts")
        self.assertEqual(final_thoughts_chunk.metadata["section_title"], "Final Thoughts")

    def test_no_anchor_found(self):
        """Tests that the source URL has no anchor if no IDs are present."""
        html = "<html><head><title>No Anchor Title</title></head><body><p>Paragraph 1.</p><p>Paragraph 2.</p></body></html>"
        chunks = chunk_html(html, "http://example.com/no-anchor", max_token_limit=15)
        self.assertEqual(len(chunks), 2)
        self.assertEqual(chunks[0].metadata["docs_url"], "http://example.com/no-anchor")
        self.assertEqual(chunks[1].metadata["docs_url"], "http://example.com/no-anchor")
        self.assertEqual(chunks[0].metadata["title"], "No Anchor Title")
        self.assertEqual(chunks[0].metadata["section_title"], "No Anchor Title")

    def test_empty_html(self):
        """Tests that empty or minimal HTML does not cause errors."""
        chunks_empty = chunk_html("", "http://example.com/empty")
        self.assertEqual(len(chunks_empty), 1)
        self.assertEqual(chunks_empty[0].text, "")

        chunks_html = chunk_html("<html></html>", "http://example.com/empty")
        self.assertEqual(len(chunks_html), 1)
        self.assertEqual(chunks_html[0].text, "<html></html>")
        
        chunks_body = chunk_html("<body></body>", "http://example.com/empty")
        self.assertEqual(len(chunks_body), 1)
        self.assertEqual(chunks_body[0].text, "<body></body>")

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
