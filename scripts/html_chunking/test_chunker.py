#!/usr/bin/env python3

import os
import sys
import time
import subprocess
import argparse
from html_chunking import chunker
from bs4 import BeautifulSoup
import tempfile
import importlib.util

def clean_html(html_content):
    """Remove unnecessary whitespace and format HTML for comparison."""
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.prettify()

def test_chunking(html_path, txt_path=None, config=None):
    """
    Compare new HTML chunking with original text chunking.
    
    Args:
        html_path (str): Path to the HTML file to chunk.
        txt_path (str, optional): Path to the text file to compare with.
        config (dict): Configuration options for chunking.
    
    Returns:
        dict: Results of the comparison.
    """
    # Default configuration if none provided
    if config is None:
        config = {
            'max_token_limit': 500,
            'count_tag_tokens': True,
            'keep_siblings_together': True,
            'prepend_parent_section_text': True
        }
    
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    
    # Create results directory if it doesn't exist
    if not os.path.exists("results"):
        os.makedirs("results")
    
    # Apply new chunking to HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    new_chunks = chunker.chunk_html(html_content, **config)
    
    new_results_path = f"results/new_chunking_{timestamp}.html"
    with open(new_results_path, 'w', encoding='utf-8') as f:
        # Add HTML header
        f.write("""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>HTML Chunking Results</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        pre { background-color: #f8f8f8; padding: 10px; overflow: auto; }
    </style>
</head>
<body>
<h1>HTML Chunking Results</h1>
""")
        for i, chunk in enumerate(new_chunks, 1):
            # Alternate between red and blue colors for chunks
            color = "red" if i % 2 == 1 else "blue"  # Red for odd, Blue for even
            
            f.write(f"<div style='color:{color}; border:1px solid {color}; padding:10px; margin-bottom:10px;'>\n")
            f.write(f"<h3 style='color:{color}'>CHUNK {i}</h3>\n")
            f.write(clean_html(chunk))
            f.write(f"</div>\n\n")
    
    # Apply original chunking to TXT if provided
    if txt_path:
        with open(txt_path, 'r', encoding='utf-8') as f:
            txt_content = f.read()
        
        # Import the original chunking function dynamically if available
        try:
            # Try to import from the original script
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            
            # Check if the original script exists
            script_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                "generate_embeddings_original.py"
            )
            
            if os.path.exists(script_path):
                # Import using importlib for better error handling
                spec = importlib.util.spec_from_file_location("generate_embeddings_original", script_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Get the chunking function
                chunk_text_original = getattr(module, "chunk_text_original", None)
                
                if chunk_text_original:
                    old_chunks = chunk_text_original(txt_content, max_tokens=config['max_token_limit'])
                    
                    old_results_path = f"results/old_chunking_{timestamp}.html"
                    with open(old_results_path, 'w', encoding='utf-8') as f:
                        # Add HTML header
                        f.write("""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Old Chunking Results</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        pre { background-color: #f8f8f8; padding: 10px; overflow: auto; }
    </style>
</head>
<body>
<h1>Old Chunking Results</h1>
""")
                        for i, chunk in enumerate(old_chunks, 1):
                            # Alternate between red and blue colors for chunks
                            color = "red" if i % 2 == 1 else "blue"  # Red for odd, Blue for even
                            
                            f.write(f"<div style='color:{color}; border:1px solid {color}; padding:10px; margin-bottom:10px;'>\n")
                            f.write(f"<h3 style='color:{color}'>CHUNK {i}</h3>\n")
                            f.write(chunk)
                            f.write(f"</div>\n\n")
                    
                    # Run vimdiff for comparison if available and not skipped
                    if not args.skip_vimdiff:
                        try:
                            subprocess.run(["vimdiff", old_results_path, new_results_path])
                        except Exception as e:
                            print(f"Error running vimdiff: {e}")
                    # Close HTML file
                    with open(old_results_path, 'a', encoding='utf-8') as f:
                        f.write("</body>\n</html>")
                    
                    print(f"Results saved to {old_results_path} and {new_results_path}")
                    
                    return {
                        'old_chunk_count': len(old_chunks),
                        'new_chunk_count': len(new_chunks),
                        'old_results_path': old_results_path,
                        'new_results_path': new_results_path
                    }
                else:
                    print("Original chunking function 'chunk_text_original' not found in the script.")
            else:
                print(f"Original script not found at {script_path}")
        except Exception as e:
            print(f"Error importing original chunking function: {e}")
    
    # If we can't run the original chunking or comparison, just return the new chunks
    print(f"Only new chunking results available at {new_results_path}")
    
    # Try running the HTML chunks through w3m for a text representation
    try:
        text_chunks = []
        for chunk in new_chunks:
            with tempfile.NamedTemporaryFile(suffix=".html", mode="w", encoding="utf-8", delete=False) as tmp:
                tmp.write("<html><body>" + chunk + "</body></html>")
                tmp_path = tmp.name
            
            try:
                result = subprocess.run(
                    ["w3m", "-dump", tmp_path], 
                    capture_output=True, 
                    text=True, 
                    check=True
                )
                text_chunks.append(result.stdout)
            except Exception:
                # Fallback to displaying plain text
                chunk_soup = BeautifulSoup(chunk, 'html.parser')
                text_chunks.append(chunk_soup.get_text(separator='\n'))
            
            os.unlink(tmp_path)
        
        text_results_path = f"results/text_chunking_{timestamp}.html"
        with open(text_results_path, 'w', encoding='utf-8') as f:
            # Add HTML header
            f.write("""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Text Chunking Results</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        pre { background-color: #f8f8f8; padding: 10px; overflow: auto; }
    </style>
</head>
<body>
<h1>Text Representation of Chunks</h1>
""")
            for i, chunk in enumerate(text_chunks, 1):
                # Alternate between red and blue colors for chunks
                color = "red" if i % 2 == 1 else "blue"  # Red for odd, Blue for even
                
                f.write(f"<div style='color:{color}; border:1px solid {color}; padding:10px; margin-bottom:10px;'>\n")
                f.write(f"<h3 style='color:{color}'>CHUNK {i}</h3>\n")
                f.write(chunk)
                f.write(f"</div>\n\n")
        
        # Close HTML file
        with open(text_results_path, 'a', encoding='utf-8') as f:
            f.write("</body>\n</html>")
            
        print(f"Text representation saved to {text_results_path}")
    except Exception as e:
        print(f"Error creating text representation: {e}")
    
    # Close the HTML file
    with open(new_results_path, 'a', encoding='utf-8') as f:
        f.write("</body>\n</html>")
        
    return {
        'new_chunk_count': len(new_chunks),
        'new_results_path': new_results_path
    }

def run_tests():
    """Run a set of predefined tests on the chunking algorithm."""
    test_cases = [
        {
            'description': 'Simple heading structure with no sections combined',
            'html': """
            <html>
              <body>
                <h1>First Main Section</h1>
                <p>Text under first main section.</p>
                
                <h2>First Subsection</h2>
                <p>Text under first subsection.</p>
                
                <h2>Second Subsection</h2>
                <p>Text under second subsection.</p>
                
                <h1>Second Main Section</h1>
                <p>Text under second main section.</p>
              </body>
            </html>
            """,
            'config': {
                'max_token_limit': 100,  # Small limit to force splitting
                'count_tag_tokens': True,
                'keep_siblings_together': False,
                'prepend_parent_section_text': True
            },
            'expected_chunks': 4  # Each section should be its own chunk
        },
        {
            'description': 'Procedure handling example',
            'html': """
            <html>
              <body>
                <h3>Installing the Software</h3>
                <p>This section explains how to install the software on your system.</p>
                
                <h4>Prerequisites</h4>
                <ul>
                  <li>Administrator access to your system</li>
                  <li>At least 2GB of free disk space</li>
                  <li>Internet connection</li>
                </ul>
                
                <p>Procedure</p>
                <ol>
                  <li>Download the installer from the website.</li>
                  <li>Run the installer with administrator privileges.</li>
                  <li>Follow the on-screen instructions.</li>
                  <li>Restart your computer when prompted.</li>
                </ol>
              </body>
            </html>
            """,
            'config': {
                'max_token_limit': 500,
                'count_tag_tokens': True,
                'keep_siblings_together': True,
                'prepend_parent_section_text': True
            },
            'expected_chunks': 1  # Everything should fit in one chunk
        },
        {
            'description': 'Code block handling example',
            'html': """
            <html>
              <body>
                <p>To install the package, run the following command:</p>
                <pre><code>
pip install my-package
                </code></pre>
                <p>This will install the latest version from PyPI.</p>
              </body>
            </html>
            """,
            'config': {
                'max_token_limit': 500,
                'count_tag_tokens': True,
                'keep_siblings_together': True,
                'prepend_parent_section_text': True
            },
            'expected_chunks': 1  # Everything should fit in one chunk
        },
        {
            'description': 'Table handling example',
            'html': """
            <html>
              <body>
                <p>The following table shows resource requirements:</p>
                <table>
                  <tr>
                    <th>Component</th>
                    <th>Minimum</th>
                    <th>Recommended</th>
                  </tr>
                  <tr>
                    <td>CPU</td>
                    <td>2 cores</td>
                    <td>4 cores</td>
                  </tr>
                  <tr>
                    <td>RAM</td>
                    <td>4 GB</td>
                    <td>8 GB</td>
                  </tr>
                </table>
              </body>
            </html>
            """,
            'config': {
                'max_token_limit': 500,
                'count_tag_tokens': True,
                'keep_siblings_together': True,
                'prepend_parent_section_text': True
            },
            'expected_chunks': 1  # Everything should fit in one chunk
        }
    ]
    
    results = {}
    
    for i, test in enumerate(test_cases, 1):
        print(f"Running test {i}: {test['description']}")
        
        # Create a temporary HTML file
        with tempfile.NamedTemporaryFile(suffix=".html", mode="w", encoding="utf-8", delete=False) as tmp:
            tmp.write(test['html'])
            html_path = tmp.name
        
        # Create a temporary TXT file (empty, just for placeholder)
        with tempfile.NamedTemporaryFile(suffix=".txt", mode="w", encoding="utf-8", delete=False) as tmp:
            tmp.write("Test")
            txt_path = tmp.name
        
        try:
            # Run the chunking with the test configuration
            chunks = chunker.chunk_html(test['html'], **test['config'])
            
            # Verify the results
            success = len(chunks) == test['expected_chunks']
            status = "PASS" if success else "FAIL"
            
            print(f"Test {i}: {status}")
            print(f"  Expected: {test['expected_chunks']} chunks")
            print(f"  Actual:   {len(chunks)} chunks")
            
            if not success:
                print("  Chunks:")
                for j, chunk in enumerate(chunks, 1):
                    # Use different text for odd vs even chunks for terminal display
                    chunk_label = "RED CHUNK" if j % 2 == 1 else "BLUE CHUNK"
                    
                    print(f"  --- {chunk_label} {j} ---")
                    print("  " + (clean_html(chunk)[:100] + "..." if len(chunk) > 100 else clean_html(chunk)))
            
            results[i] = {
                'description': test['description'],
                'status': status,
                'expected': test['expected_chunks'],
                'actual': len(chunks)
            }
        
        finally:
            # Clean up temporary files
            os.unlink(html_path)
            os.unlink(txt_path)
    
    # Print summary
    print("\nTest Summary:")
    for test_id, result in results.items():
        print(f"Test {test_id}: {result['status']} - {result['description']}")
    
    passes = sum(1 for result in results.values() if result['status'] == "PASS")
    print(f"\n{passes}/{len(results)} tests passed")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test HTML chunking against original text chunking")
    parser.add_argument('--html', help="Path to the HTML file to chunk")
    parser.add_argument('--txt', help="Path to the text file to compare with")
    parser.add_argument('--max-tokens', type=int, default=500, help="Maximum token limit per chunk")
    parser.add_argument('--count-tags', action='store_true', help="Whether to count HTML tags as tokens")
    parser.add_argument('--keep-siblings', action='store_true', default=True, help="Keep adjacent heading sections together if under token limit")
    parser.add_argument('--prepend-parent', action='store_true', default=True, help="Include parent heading text in child section chunks")
    parser.add_argument('--run-tests', action='store_true', help="Run predefined tests instead of comparing files")
    parser.add_argument('--skip-vimdiff', action='store_true', help="Skip running vimdiff and just output results to files")
    
    args = parser.parse_args()
    
    if args.run_tests:
        run_tests()
    elif args.html:
        config = {
            'max_token_limit': args.max_tokens,
            'count_tag_tokens': args.count_tags,
            'keep_siblings_together': args.keep_siblings,
            'prepend_parent_section_text': args.prepend_parent
        }
        
        results = test_chunking(args.html, args.txt if args.txt else None, config)
        
        if 'old_chunk_count' in results:
            print(f"Old chunking: {results['old_chunk_count']} chunks")
        print(f"New chunking: {results['new_chunk_count']} chunks")
        print(f"Results saved to {results.get('old_results_path', '')} and {results['new_results_path']}")
    else:
        print("Please provide at least the HTML file path, or use --run-tests")
        parser.print_help()
