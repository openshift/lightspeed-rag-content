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
        <html>
        <head><title>Main Document Title</title></head>
        <body>
            <section id="intro">
                <div><h2>Introduction</h2>
                    <p>Text about intro.</p>
                </div>
                <section id="topic">
                    <div><h3>Topic</h3></div>
                    <div>
                        <p>Content</p>
                        <p>More content, still under Topic.</p>
                    </div>
                    <section id="sub_topic">
                        <div><h4>Sub Topic</h4></div>
                        <div>
                            <p>The inner most content of subtopic</p>
                        </div>
                    </section>
                </section>
                <section id="final">
                    <div><h3>Final</h3></div>
                    <div>
                        <p>Final conclusion</p>
                    </div>
                </section>
            </section>
        </body>
        </html>
        """
        # if there is "/html-single/" in the url every hyperlink is based on the last
        # section id as fragment on the "index" path of the document (url/index#child-section-id)
        chunks = chunk_html(html, "http://example.com/html-single/meta/", max_token_limit=25)
        self.assertGreaterEqual(len(chunks), 7)

        # Check document title consistency
        for chunk in chunks:
            self.assertEqual(chunk.metadata["title"], "Main Document Title")

        # Check section titles and anchors
        intro_chunk = chunks[0]
        self.assertEqual(intro_chunk.metadata["docs_url"], "http://example.com/html-single/meta/index#intro")
        self.assertEqual(intro_chunk.metadata["section_title"], "Introduction")

        topic_chunks = chunks[1:4]
        self.assertTrue(all(c.metadata["docs_url"] == "http://example.com/html-single/meta/index#topic"
                        for c in topic_chunks))
        self.assertTrue(all(c.metadata["section_title"] == "Topic"
                        for c in topic_chunks))

        subtopic_chunks = chunks[4:6]
        self.assertTrue(all(c.metadata["docs_url"] == "http://example.com/html-single/meta/index#sub_topic"
                        for c in subtopic_chunks))
        self.assertTrue(all(c.metadata["section_title"] == "Sub Topic"
                        for c in subtopic_chunks))

        final_chunks = chunks[6:8]
        self.assertTrue(all(c.metadata["docs_url"] == "http://example.com/html-single/meta/index#final"
                        for c in final_chunks))
        self.assertTrue(all(c.metadata["section_title"] == "Final"
                        for c in final_chunks))

        # if there is only "/html/" in the url every hyperlink is based on
        # it's parent clubbed with fragment on the last section id (url/parent-section-id#child-section-id)
        chunks = chunk_html(html, "http://example.com/html/meta/", max_token_limit=25)
        self.assertGreaterEqual(len(chunks), 5)

        # Check document title consistency
        for chunk in chunks:
            self.assertEqual(chunk.metadata["title"], "Main Document Title")

        # Check section titles and anchors
        intro_chunk = chunks[0]
        # only the parent will not have any fragement (url/parent-section-id)
        self.assertEqual(intro_chunk.metadata["docs_url"], "http://example.com/html/meta/intro")
        self.assertEqual(intro_chunk.metadata["section_title"], "Introduction")

        topic_chunks = chunks[1:4]
        self.assertTrue(all(c.metadata["docs_url"] == "http://example.com/html/meta/intro#topic"
                        for c in topic_chunks))
        self.assertTrue(all(c.metadata["section_title"] == "Topic"
                        for c in topic_chunks))

        subtopic_chunks = chunks[4:6]
        self.assertTrue(all(c.metadata["docs_url"] == "http://example.com/html/meta/intro#sub_topic"
                        for c in subtopic_chunks))
        self.assertTrue(all(c.metadata["section_title"] == "Sub Topic"
                        for c in subtopic_chunks))

        final_chunks = chunks[6:8]
        self.assertTrue(all(c.metadata["docs_url"] == "http://example.com/html/meta/intro#final"
                        for c in final_chunks))
        self.assertTrue(all(c.metadata["section_title"] == "Final"
                        for c in final_chunks))

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
