#!/usr/bin/env python3
"""
Example script demonstrating the HTML chunking library.

This script reads an HTML file, splits it into chunks based on a token limit,
and generates a report for visual inspection.
"""

import argparse
import os
import sys
from typing import List

# Imports are deferred into main() to support running the script
# from within its directory, which requires a sys.path modification first.

def create_argument_parser() -> argparse.ArgumentParser:
    """Creates and configures the argument parser."""
    parser = argparse.ArgumentParser(
        description="HTML Chunking Example",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "html_file",
        nargs="?",
        default=os.path.join(os.path.dirname(__file__), "example.html"),
        help="Path to the input HTML file."
    )
    parser.add_argument(
        "--max-token-limit",
        type=int,
        default=500,
        help="Max tokens per chunk."
    )
    parser.add_argument(
        "-o", "--output",
        default="chunked_output.html",
        help="Output HTML file name for the report."
    )
    return parser

def generate_html_report(output_path: str, chunks: List['Chunk'], original_tokens: int, max_token_limit: int, count_html_tokens_func) -> None:
    """Generates a single HTML file containing all chunks for review."""
    print(f"\nSaving all chunks to a single file: {output_path}...")
    
    chunk_tokens = [count_html_tokens_func(chunk.text) for chunk in chunks]
    avg_tokens = sum(chunk_tokens) / len(chunk_tokens) if chunk_tokens else 0
    min_tokens = min(chunk_tokens) if chunk_tokens else 0
    max_tokens = max(chunk_tokens) if chunk_tokens else 0
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html>\n<html>\n<head>\n<title>Chunked HTML Document</title>\n")
        f.write("<style>body{font-family:Arial,sans-serif;max-width:1200px;margin:20px auto;padding:0 20px}.chunk-separator{margin:20px 0;border-top:5px solid #3c82f6;padding-top:10px}.chunk-header{background-color:#f0f0f0;padding:10px;font-weight:bold;margin-bottom:10px;font-size:16px}.chunk-meta{background-color:#eaf2ff;padding:5px 10px;font-family:monospace;font-size:12px;word-wrap:break-word}.chunk-content{border:1px solid #ddd;padding:15px}</style>\n")
        f.write("</head>\n<body>\n<h1>Chunked HTML Document</h1>\n")
        
        f.write(f"<p><strong>Original document:</strong> {original_tokens} tokens</p>\n")
        f.write(f"<p><strong>Split into:</strong> {len(chunks)} chunks with max {max_token_limit} tokens per chunk</p>\n")
        
        f.write("<h2>Chunk Statistics</h2>\n<table border='1' cellpadding='5' style='border-collapse:collapse;width:100%;'>\n")
        f.write("<tr><th>Statistic</th><th>Value</th></tr>\n")
        f.write(f"<tr><td>Number of chunks</td><td>{len(chunks)}</td></tr>\n")
        f.write(f"<tr><td>Average tokens per chunk</td><td>{avg_tokens:.1f}</td></tr>\n")
        f.write(f"<tr><td>Minimum tokens</td><td>{min_tokens}</td></tr>\n")
        f.write(f"<tr><td>Maximum tokens</td><td>{max_tokens}</td></tr>\n")
        f.write(f"<tr><td>Chunks &lt; 100 tokens</td><td>{sum(1 for t in chunk_tokens if t < 100)}</td></tr>\n")
        f.write(f"<tr><td>Chunks &gt; token limit</td><td>{sum(1 for t in chunk_tokens if t > max_token_limit)}</td></tr>\n")
        f.write("</table>\n<br><hr><br>\n")
        
        for i, chunk in enumerate(chunks, 1):
            token_count = chunk_tokens[i-1]
            if i > 1: f.write('<div class="chunk-separator"></div>\n')
            
            style = " style='background-color:#FFE0E0;'" if token_count > max_token_limit else ""
            f.write(f'<div class="chunk-header"{style}>Chunk {i} ({token_count} tokens)</div>\n')
            f.write(f'<div class="chunk-meta"><strong>Title:</strong> {chunk.metadata.get("title", "N/A")}<br><strong>Source:</strong> {chunk.metadata.get("docs_url", "N/A")}</div>\n')
            f.write('<div class="chunk-content">\n')
            f.write(chunk.text)
            f.write('\n</div>\n')
        
        f.write("</body>\n</html>")
    print(f"Report saved to {output_path}")

def main():
    """Main function to run the HTML chunking example."""
    from html_chunking.chunker import chunk_html, Chunk
    from html_chunking.tokenizer import count_html_tokens

    parser = create_argument_parser()
    args = parser.parse_args()

    print("HTML Chunking Example\n====================\n")

    if not os.path.exists(args.html_file):
        print("Error: Sample document '%s' not found." % args.html_file, file=sys.stderr)
        return 1

    try:
        with open(args.html_file, "r", encoding="utf-8") as f:
            sample_html = f.read()
    except IOError as e:
        print("Error reading HTML file '%s': %s" % (args.html_file, e), file=sys.stderr)
        return 1

    original_tokens = count_html_tokens(sample_html)
    print(f"Original document has {original_tokens} tokens.\n")

    print(f"Chunking with max {args.max_token_limit} tokens per chunk...\n")

    source_url_for_example = f"file://{os.path.abspath(args.html_file)}"

    chunks = chunk_html(
        html_content=sample_html,
        source_url=source_url_for_example,
        max_token_limit=args.max_token_limit
    )

    print(f"Created {len(chunks)} chunks.")
    
    generate_html_report(args.output, chunks, original_tokens, args.max_token_limit, count_html_tokens)
    
    return 0

if __name__ == "__main__":
    # This block allows the script to be run directly from within the html_chunking
    # directory by ensuring the parent 'scripts' directory is in the Python path.
    if __package__ is None:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
    
    try:
        sys.exit(main())
    except ImportError as e:
        print("Error: Failed to import a required module.", file=sys.stderr)
        print("Detail: %s" % e, file=sys.stderr)
        print("\nSuggestion: Try running this script from the project's root directory using 'python -m html_chunking.example'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print("An unexpected error occurred: %s" % e, file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
