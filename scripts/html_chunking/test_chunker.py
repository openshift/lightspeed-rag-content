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

    def test_chunk_html_small_input(self):
        """Tests that HTML smaller than the max_token_limit is not chunked."""
        html = "<html><body><h1>My Title</h1><p>This is a small test.</p></body></html>"
        chunks = chunk_html(html, "http://example.com/small", max_token_limit=100)
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0].text, html)
        self.assertEqual(chunks[0].metadata["docs_url"], "http://example.com/small")
        self.assertEqual(chunks[0].metadata["title"], "My Title")

    def test_basic_splitting(self):
        """Tests basic splitting of multiple paragraphs."""
        html = "<html><body>"
        for i in range(10):
            html += f"<p>This is paragraph {i}. It contains several words to simulate content.</p>"
        html += "</body></html>"
        chunks = chunk_html(html, "http://example.com/basic", max_token_limit=100)
        self.assertEqual(len(chunks), 3)
        self.assertTrue(all(mock_count_html_tokens(c.text) <= 110 for c in chunks))
        self.assertIn("paragraph 0", chunks[0].text)
        self.assertIn("paragraph 9", chunks[-1].text)

    def test_oversized_element_splitting(self):
        """Tests that a single element larger than the limit is recursively split."""
        long_text = "word " * 200
        html = f"<html><body><div>{long_text}</div></body></html>"
        chunks = chunk_html(html, "http://example.com/oversized", max_token_limit=100)
        self.assertGreater(len(chunks), 1)
        full_text = "".join(BeautifulSoup(c.text, 'html.parser').get_text() for c in chunks)
        self.assertIn("word", full_text)
        self.assertGreater(len(full_text), 500)

    def test_table_splitting(self):
        """Tests that large tables are split, preserving the header in each chunk."""
        header = "<thead><tr><th>Header 1</th><th>Header 2</th></tr></thead>"
        rows = "".join([f"<tr><td>Row {i} Col 1</td><td>Row {i} Col 2</td></tr>" for i in range(20)])
        html = f"<html><body><table>{header}<tbody>{rows}</tbody></table></body></html>"
        chunks = chunk_html(html, "http://example.com/table", max_token_limit=100)
        self.assertGreater(len(chunks), 1)
        for chunk in chunks:
            self.assertIn("<thead>", chunk.text)
            self.assertIn("Header 1", chunk.text)
            self.assertIn("</table>", chunk.text)
        self.assertIn("Row 0", chunks[0].text)
        self.assertNotIn("Row 19", chunks[0].text)
        self.assertIn("Row 19", chunks[-1].text)

    def test_list_splitting(self):
        """Tests that large lists are split correctly."""
        items = "".join([f"<li>Item {i} is here.</li>" for i in range(30)])
        html = f"<html><body><ul>{items}</ul></body></html>"
        chunks = chunk_html(html, "http://example.com/list", max_token_limit=100)
        self.assertGreater(len(chunks), 1)
        for chunk in chunks:
            self.assertIn("<ul ", chunk.text)
            self.assertIn("</ul>", chunk.text)
        self.assertIn("Item 0", chunks[0].text)
        self.assertIn("Item 29", chunks[-1].text)

    def test_definition_list_splitting(self):
        """Tests splitting of a definition list."""
        items = "".join([f"<dt>Term {i}</dt><dd>Definition {i} is quite long and elaborate.</dd>" for i in range(15)])
        html = f"<html><body><div class='variablelist'><dl>{items}</dl></div></body></html>"
        chunks = chunk_html(html, "http://example.com/dl", max_token_limit=100)
        self.assertGreater(len(chunks), 1)
        for chunk in chunks:
            self.assertIn("<dl>", chunk.text)
            self.assertIn("</dl>", chunk.text)
        self.assertIn("Term 0", chunks[0].text)
        self.assertIn("Term 14", chunks[-1].text)

    def test_code_splitting(self):
        """Tests that preformatted code blocks are split by lines."""
        code_lines = "\n".join([f"line_{i} = 'some code here';" for i in range(50)])
        html = f"<html><body><pre>{code_lines}</pre></body></html>"
        chunks = chunk_html(html, "http://example.com/code", max_token_limit=50)
        self.assertGreater(len(chunks), 1)
        for chunk in chunks:
            self.assertIn("<pre ", chunk.text)
            self.assertIn("</pre>", chunk.text)
        self.assertIn("line_0", chunks[0].text)
        self.assertIn("line_49", chunks[-1].text)
        self.assertNotIn("line_49", chunks[0].text)

    def test_heading_grouping(self):
        """Tests that headings are grouped with the following element."""
        html = "<html><body>"
        for i in range(5):
            html += f"<h2>Title {i}</h2><p>This is paragraph for title {i}. It has text.</p>"
        html += "</body></html>"
        chunks = chunk_html(html, "http://example.com/headings", max_token_limit=50)
        self.assertEqual(len(chunks), 5)
        for i, chunk in enumerate(chunks):
            self.assertIn(f"Title {i}", chunk.text)
            self.assertIn(f"paragraph for title {i}", chunk.text)

    def test_paragraph_ending_with_colon_grouping(self):
        """Tests grouping of a paragraph ending with a colon with the next list/table."""
        html = ("<html><body><p>Here are the items:</p>"
                "<ul><li>Item 1</li><li>Item 2</li></ul></body></html>")
        chunks = chunk_html(html, "http://example.com/colon", max_token_limit=100)
        self.assertEqual(len(chunks), 1)
        self.assertIn("Here are the items:", chunks[0].text)
        self.assertIn("<li>Item 1</li>", chunks[0].text)

    def test_metadata_anchor_handling(self):
        """Tests the generation of source metadata with correct anchors."""
        html = """
        <html><body>
            <section id="intro"><h1>Intro</h1><p>Text</p></section>
            <div id="main-content">
                <h2 id="topic1">Topic 1</h2><p>Content 1</p>
                <p>More content 1</p>
            </div>
            <section id="conclusion">
                <p>Conclusion text</p>
                <h3 id="final-thoughts">Final Thoughts</h3><p>Final words.</p>
            </section>
        </body></html>
        """
        chunks = chunk_html(html, "http://example.com/meta", max_token_limit=25)
        
        self.assertGreaterEqual(len(chunks), 3)

        # The first chunk might not have a specific anchor if it's just the title
        self.assertIn(chunks[0].metadata["docs_url"], ["http://example.com/meta", "http://example.com/meta#intro"])
        self.assertEqual(chunks[0].metadata["title"], "Intro")

        topic1_chunks = [c for c in chunks if "Topic 1" in c.text or "Content 1" in c.text or "More content 1" in c.text]
        self.assertTrue(all(c.metadata["docs_url"] == "http://example.com/meta#topic1" for c in topic1_chunks))
        
        final_thoughts_chunk = next((c for c in chunks if "Final words" in c.text), None)
        
        self.assertIsNotNone(final_thoughts_chunk, "Final thoughts chunk not found")
        
        self.assertEqual(final_thoughts_chunk.metadata["docs_url"], "http://example.com/meta#final-thoughts")
        self.assertEqual(final_thoughts_chunk.metadata["title"], "Intro")

    def test_no_anchor_found(self):
        """Tests that the source URL has no anchor if no IDs are present."""
        html = "<html><body><h1>No Anchor Title</h1><p>Paragraph 1.</p><p>Paragraph 2.</p></body></html>"
        chunks = chunk_html(html, "http://example.com/no-anchor", max_token_limit=15)
        self.assertEqual(len(chunks), 2)
        self.assertEqual(chunks[0].metadata["docs_url"], "http://example.com/no-anchor")
        self.assertEqual(chunks[1].metadata["docs_url"], "http://example.com/no-anchor")
        self.assertEqual(chunks[0].metadata["title"], "No Anchor Title")

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
