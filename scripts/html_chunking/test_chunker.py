"""
Tests for the HTML chunker implementation.
"""

import unittest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup

from .parser import parse_html, HtmlSection
from .tokenizer import count_html_tokens
from .chunker import chunk_html, _chunk_by_heading_level, _identify_oversized_chunks


class TestHtmlChunker(unittest.TestCase):
    """Test cases for the HTML chunker."""

    def setUp(self):
        """Set up test environment."""
        # Create a simple mock for token counting to make tests deterministic
        self.token_counter_patcher = patch('html_chunking.chunker.count_html_tokens')
        self.mock_count_tokens = self.token_counter_patcher.start()
        
        # By default, make tokens equal to length / 5 (a simple approximation)
        self.mock_count_tokens.side_effect = lambda text, count_tags: len(text) // 5

    def tearDown(self):
        """Clean up test environment."""
        self.token_counter_patcher.stop()

    def test_no_chunk_needed(self):
        """Test when content is already under token limit."""
        html = "<h1>Test</h1><p>This is a small test</p>"
        self.mock_count_tokens.return_value = 10  # Under limit
        
        result = chunk_html(html, max_token_limit=20)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], html)

    def test_chunk_by_h1(self):
        """Test chunking by h1 headings."""
        html = """
        <h1>Section 1</h1>
        <p>Content 1</p>
        <h1>Section 2</h1>
        <p>Content 2</p>
        <h1>Section 3</h1>
        <p>Content 3</p>
        """
        
        # First make the whole content exceed the limit
        self.mock_count_tokens.side_effect = lambda text, count_tags: 100 if text == html else 30
        
        result = chunk_html(html, max_token_limit=50, keep_siblings_together=False)
        
        self.assertEqual(len(result), 3)  # Three chunks, one for each h1 section
        self.assertIn("Section 1", result[0])
        self.assertIn("Content 1", result[0])
        self.assertIn("Section 2", result[1])
        self.assertIn("Content 2", result[1])
        self.assertIn("Section 3", result[2])
        self.assertIn("Content 3", result[2])

    def test_keep_siblings_together(self):
        """Test keeping sibling sections together when under the limit."""
        html = """
        <h1>Section 1</h1>
        <p>Content 1</p>
        <h1>Section 2</h1>
        <p>Content 2</p>
        <h1>Section 3</h1>
        <p>Content 3</p>
        """
        
        # Set up mock to make full content exceed limit, but combinations under limit
        def count_side_effect(text, count_tags):
            if text == html:
                return 100  # Whole document exceeds limit
            elif "Section 1" in text and "Section 2" in text and "Section 3" in text:
                return 100  # All three sections exceed limit
            elif "Section 1" in text and "Section 2" in text:
                return 40  # First two sections together under limit
            elif "Section 3" in text:
                return 30  # Last section under limit
            else:
                return 20  # Individual sections under limit
        
        self.mock_count_tokens.side_effect = count_side_effect
        
        result = chunk_html(html, max_token_limit=50, keep_siblings_together=True)
        
        self.assertEqual(len(result), 2)  # Two chunks: sections 1+2, and section 3
        self.assertIn("Section 1", result[0])
        self.assertIn("Content 1", result[0])
        self.assertIn("Section 2", result[0])
        self.assertIn("Content 2", result[0])
        self.assertIn("Section 3", result[1])
        self.assertIn("Content 3", result[1])

    def test_prepend_parent_text(self):
        """Test prepending parent section text to child sections."""
        html = """
        <h1>Parent Section</h1>
        <p>Parent content</p>
        <h2>Child Section 1</h2>
        <p>Child content 1</p>
        <h2>Child Section 2</h2>
        <p>Child content 2</p>
        """
        
        # Make the whole content exceed the limit, but h2 sections with parent text under limit
        def count_side_effect(text, count_tags):
            if text == html or "Parent Section" in text and "Child Section 1" in text and "Child Section 2" in text:
                return 100  # Whole document or all content exceeds limit
            elif "Parent Section" in text and "Parent content" in text and "Child Section" in text:
                return 40  # Parent heading + content + one child section under limit
            else:
                return 20  # Individual sections under limit
        
        self.mock_count_tokens.side_effect = count_side_effect
        
        result = chunk_html(
            html, max_token_limit=50, keep_siblings_together=False, prepend_parent_section_text=True
        )
        
        self.assertEqual(len(result), 2)  # Two chunks
        self.assertIn("Parent Section", result[0])
        self.assertIn("Parent content", result[0])
        self.assertIn("Child Section 1", result[0])
        self.assertIn("Child content 1", result[0])
        self.assertIn("Parent Section", result[1])
        self.assertIn("Parent content", result[1])
        self.assertIn("Child Section 2", result[1])
        self.assertIn("Child content 2", result[1])

    def test_deep_section_hierarchy(self):
        """Test chunking with a deep hierarchy of sections."""
        html = """
        <h1>Level 1</h1>
        <p>Level 1 content</p>
        <h2>Level 2</h2>
        <p>Level 2 content</p>
        <h3>Level 3</h3>
        <p>Level 3 content</p>
        <h4>Level 4</h4>
        <p>Level 4 content</p>
        <h5>Level 5</h5>
        <p>Level 5 content</p>
        <h6>Level 6</h6>
        <p>Level 6 content</p>
        """
        
        # Make the whole content and each level exceed the limit
        def count_side_effect(text, count_tags):
            if len(text) > 100:  # Rough proxy for detecting larger chunks
                return 100  # Exceeds limit
            else:
                return 30  # Individual sections under limit
        
        self.mock_count_tokens.side_effect = count_side_effect
        
        result = chunk_html(
            html, max_token_limit=50, keep_siblings_together=False, prepend_parent_section_text=False
        )
        
        # We should get multiple chunks broken down by heading levels
        self.assertGreater(len(result), 1)
        self.assertTrue(any("Level 1" in chunk for chunk in result))
        self.assertTrue(any("Level 6" in chunk for chunk in result))

    def test_procedure_handling(self):
        """Test handling of procedures in chunking."""
        html = """
        <h3>Installing Software</h3>
        <p>Follow these steps to install the software:</p>
        <p>Procedure</p>
        <ol>
            <li>Download the installer from the website.</li>
            <li>Run the installer with administrator privileges.</li>
            <li>Follow the on-screen instructions.</li>
            <li>Restart your computer when prompted.</li>
        </ol>
        """
        
        # Setup token counting to make procedures split if needed
        def count_side_effect(text, count_tags):
            if "Procedure" in text and all([
                "Download the installer" in text,
                "Run the installer" in text, 
                "Follow the on-screen" in text,
                "Restart your computer" in text
            ]):
                return 60  # Whole procedure exceeds limit
            elif "Procedure" in text:
                return 30  # Procedure marker under limit
            elif "<ol" in text:
                return 40  # Just the ordered list exceeds limit
            elif "Download the installer" in text and "Run the installer" in text:
                return 30  # First two steps under limit
            elif "Follow the on-screen" in text and "Restart your computer" in text:
                return 30  # Last two steps under limit
            else:
                return 10  # Individual elements under limit
        
        self.mock_count_tokens.side_effect = count_side_effect
        
        result = chunk_html(html, max_token_limit=50)
        
        # The procedure should be split appropriately
        self.assertGreater(len(result), 1)
        self.assertTrue(any("Installing Software" in chunk for chunk in result))
        self.assertTrue(any("Procedure" in chunk for chunk in result))
        self.assertTrue(any("Download the installer" in chunk for chunk in result))

    def test_code_block_handling(self):
        """Test handling of code blocks in chunking."""
        html = """
        <h2>Code Example</h2>
        <p>Here is an example of Python code:</p>
        <pre><code>
        def hello_world():
            print("Hello, world!")
            
        if __name__ == "__main__":
            hello_world()
        </code></pre>
        <p>This is a simple hello world program.</p>
        """
        
        # Setup token counting to make code blocks split if needed
        def count_side_effect(text, count_tags):
            if "Code Example" in text and "hello_world" in text and "simple hello world program" in text:
                return 100  # Whole example exceeds limit
            elif "Here is an example" in text and "hello_world" in text:
                return 60  # Intro + code exceeds limit
            elif "hello_world" in text and "simple hello world program" in text:
                return 60  # Code + outro exceeds limit
            elif "hello_world" in text:
                return 40  # Just code under limit
            else:
                return 20  # Individual elements under limit
        
        self.mock_count_tokens.side_effect = count_side_effect
        
        result = chunk_html(html, max_token_limit=50)
        
        # Code should be split appropriately
        self.assertGreater(len(result), 1)
        self.assertTrue(any("Code Example" in chunk for chunk in result))
        self.assertTrue(any("example of Python code" in chunk for chunk in result))
        self.assertTrue(any("hello_world" in chunk for chunk in result))
        self.assertTrue(any("simple hello world program" in chunk for chunk in result))

    def test_table_handling(self):
        """Test handling of tables in chunking."""
        html = """
        <h2>Data Table</h2>
        <p>Here is a sample data table:</p>
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Age</th>
                    <th>Occupation</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>John Doe</td>
                    <td>30</td>
                    <td>Engineer</td>
                </tr>
                <tr>
                    <td>Jane Smith</td>
                    <td>28</td>
                    <td>Doctor</td>
                </tr>
                <tr>
                    <td>Bob Johnson</td>
                    <td>45</td>
                    <td>Teacher</td>
                </tr>
            </tbody>
        </table>
        <p>This table shows sample employee data.</p>
        """
        
        # Setup token counting to make tables split if needed
        def count_side_effect(text, count_tags):
            if "Data Table" in text and "John Doe" in text and "sample employee data" in text:
                return 100  # Whole example exceeds limit
            elif "sample data table" in text and "John Doe" in text:
                return 60  # Intro + table exceeds limit
            elif "John Doe" in text and "sample employee data" in text:
                return 60  # Table + outro exceeds limit
            elif "<table>" in text and "</table>" in text:
                return 70  # Whole table exceeds limit
            elif "John Doe" in text and "Jane Smith" in text and "Bob Johnson" in text:
                return 60  # All rows exceed limit
            elif "John Doe" in text:
                return 20  # First row under limit
            elif "Jane Smith" in text:
                return 20  # Second row under limit
            elif "Bob Johnson" in text:
                return 20  # Third row under limit
            else:
                return 10  # Individual elements under limit
        
        self.mock_count_tokens.side_effect = count_side_effect
        
        result = chunk_html(html, max_token_limit=50)
        
        # Table should be split appropriately
        self.assertGreater(len(result), 1)
        self.assertTrue(any("Data Table" in chunk for chunk in result))
        self.assertTrue(any("sample data table" in chunk for chunk in result))
        self.assertTrue(any("John Doe" in chunk for chunk in result))
        self.assertTrue(any("sample employee data" in chunk for chunk in result))

    def test_identify_oversized_chunks(self):
        """Test that oversized chunks are correctly identified."""
        chunks = ["Small chunk", "Medium chunk", "Very large chunk that exceeds the token limit"]
        
        # Set up the mock to make only the third chunk oversized
        def count_side_effect(text, count_tags):
            if text == "Very large chunk that exceeds the token limit":
                return 60  # Exceeds limit
            else:
                return 20  # Under limit
        
        self.mock_count_tokens.side_effect = count_side_effect
        
        options = MagicMock()
        options.max_token_limit = 50
        options.count_tag_tokens = True
        
        oversized = _identify_oversized_chunks(chunks, options)
        
        self.assertEqual(len(oversized), 1)
        self.assertEqual(list(oversized)[0], 2)  # The third chunk (index 2) is oversized

    def test_mixed_content(self):
        """Test chunking with mixed content types."""
        html = """
        <h1>Mixed Content</h1>
        <p>This section contains mixed content.</p>
        <h2>Code Example</h2>
        <pre><code>print("Hello world")</code></pre>
        <h2>Procedure</h2>
        <p>Procedure</p>
        <ol>
            <li>Step 1</li>
            <li>Step 2</li>
        </ol>
        <h2>Table</h2>
        <table>
            <tr><th>Header</th></tr>
            <tr><td>Data</td></tr>
        </table>
        """
        
        # Make the whole content and each major section exceed the limit
        def count_side_effect(text, count_tags):
            if len(text) > 100:  # Rough proxy for detecting larger chunks
                return 100  # Exceeds limit
            elif "Code Example" in text and "print" in text:
                return 60  # Code section exceeds limit
            elif "Procedure" in text and "Step 1" in text and "Step 2" in text:
                return 60  # Procedure section exceeds limit
            elif "Table" in text and "<table>" in text:
                return 60  # Table section exceeds limit
            else:
                return 30  # Individual elements under limit
        
        self.mock_count_tokens.side_effect = count_side_effect
        
        result = chunk_html(html, max_token_limit=50)
        
        # Mixed content should be split appropriately
        self.assertGreater(len(result), 1)
        self.assertTrue(any("Mixed Content" in chunk for chunk in result))
        self.assertTrue(any("Code Example" in chunk for chunk in result))
        self.assertTrue(any("Procedure" in chunk for chunk in result))
        self.assertTrue(any("Table" in chunk for chunk in result))


if __name__ == "__main__":
    unittest.main()
