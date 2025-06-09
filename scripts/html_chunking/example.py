#!/usr/bin/env python3
"""
Example script demonstrating the HTML chunking library.

This script shows how to use the HTML chunker with a sample HTML document.
"""

import os
import sys
import argparse
from pathlib import Path
from chunker import chunk_html, Chunk
from tokenizer import count_html_tokens

def main():
    """Run the HTML chunking example."""
    parser = argparse.ArgumentParser(
        description="HTML Chunking Example",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "html_file",
        nargs="?",
        default="example.html",
        help="Path to the input HTML file."
    )
    parser.add_argument(
        "--max-token-limit",
        type=int,
        default=500,
        help="Max tokens per chunk"
    )
    parser.add_argument(
        "-o", "--output",
        default="chunked_output.html",
        help="Output HTML file name"
    )
    args = parser.parse_args()
    
    print("HTML Chunking Example")
    print("====================\n")
    
    sample_path = args.html_file
    if not os.path.exists(sample_path):
        print(f"Error: Sample document {sample_path} not found.", file=sys.stderr)
        return 1
    
    try:
        with open(sample_path, "r", encoding="utf-8") as f:
            sample_html = f.read()
    except Exception as e:
        print(f"Error reading HTML file: {e}", file=sys.stderr)
        return 1
    
    try:
        print("Counting tokens in the document...")
        original_tokens = count_html_tokens(sample_html)
        print(f"Original document has {original_tokens} tokens\n")
    except Exception as e:
        print(f"Warning: Could not count tokens accurately: {e}", file=sys.stderr)
        original_tokens = "N/A"
    
    print(f"Chunking with max {args.max_token_limit} tokens per chunk...")
    # These options are now handled internally by the improved chunker
    print("Chunking options:")
    print("  - Count tag tokens: True")
    print("  - Keep siblings together: True")
    print("  - Prepend parent section text: True\n")
    
    try:
        # Define a source URL for the example file. In a real pipeline,
        # this would come from url_mapping.json.
        source_url_for_example = f"file://{os.path.abspath(sample_path)}"

        # Perform chunking using the updated function signature
        chunks = chunk_html(
            html_content=sample_html,
            source_url=source_url_for_example,
            max_token_limit=args.max_token_limit,
            count_tag_tokens=True
        )
        
        print(f"Created {len(chunks)} chunks:")
        
        chunk_tokens = [count_html_tokens(chunk.text) for chunk in chunks]
        
        # Print info for the first 5 chunks
        for i, chunk in enumerate(chunks[:5], 1):
            print(f"  Chunk {i}: {chunk_tokens[i-1]} tokens")
            print(f"  Metadata Source: {chunk.metadata.get('source', 'N/A')}\n")

        if len(chunks) > 5:
            print(f"  ... and {len(chunks) - 5} more chunks\n")

        # Save all chunks to a single file with separators
        output_filename = args.output
        print(f"\nSaving all chunks to a single file: {output_filename}...")
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write("<!DOCTYPE html>\n<html>\n<head>\n")
            f.write("<title>Chunked HTML Document</title>\n")
            f.write("<style>\n")
            f.write("body { font-family: Arial, sans-serif; max-width: 1200px; margin: 20px auto; padding: 0 20px; }\n")
            f.write(".chunk-separator { margin: 20px 0; border-top: 5px solid #3c82f6; padding-top: 10px; }\n")
            f.write(".chunk-header { background-color: #f0f0f0; padding: 10px; font-weight: bold; margin-bottom: 10px; font-size: 16px; }\n")
            f.write(".chunk-meta { background-color: #eaf2ff; padding: 5px 10px; font-family: monospace; font-size: 12px; margin-bottom: 10px; word-wrap: break-word; }\n")
            f.write(".chunk-content { border: 1px solid #ddd; padding: 15px; }\n")
            f.write("</style>\n</head>\n<body>\n")
            
            f.write("<h1>Chunked HTML Document</h1>\n")
            f.write(f"<p><strong>Original document:</strong> {original_tokens} tokens</p>\n")
            f.write(f"<p><strong>Split into:</strong> {len(chunks)} chunks with max {args.max_token_limit} tokens per chunk</p>\n")
            
            # --- START: Re-added summary section ---
            f.write("<p><strong>Chunking settings (now internal):</strong></p>\n")
            f.write("<ul>\n")
            f.write("  <li>count_tag_tokens: True</li>\n")
            f.write("  <li>keep_siblings_together: True</li>\n")
            f.write("  <li>prepend_parent_section_text: True</li>\n")
            f.write("</ul>\n")
            
            f.write("<h2>Chunk Statistics</h2>\n")
            f.write("<table border='1' cellpadding='5' style='border-collapse: collapse; width: 100%;'>\n")
            f.write("<tr><th>Statistic</th><th>Value</th></tr>\n")
            f.write(f"<tr><td>Number of chunks</td><td>{len(chunks)}</td></tr>\n")
            
            # Calculate statistics
            avg_tokens = sum(chunk_tokens) / len(chunk_tokens) if chunk_tokens else 0
            min_tokens = min(chunk_tokens) if chunk_tokens else 0
            max_tokens = max(chunk_tokens) if chunk_tokens else 0
            
            f.write(f"<tr><td>Average tokens per chunk</td><td>{avg_tokens:.1f}</td></tr>\n")
            f.write(f"<tr><td>Minimum tokens</td><td>{min_tokens}</td></tr>\n")
            f.write(f"<tr><td>Maximum tokens</td><td>{max_tokens}</td></tr>\n")
            f.write(f"<tr><td>Chunks below 100 tokens</td><td>{sum(1 for t in chunk_tokens if t < 100)}</td></tr>\n")
            f.write(f"<tr><td>Chunks above token limit</td><td>{sum(1 for t in chunk_tokens if t > args.max_token_limit)}</td></tr>\n")
            f.write("</table>\n")
            # --- END: Re-added summary section ---

            f.write("<br><hr><br>\n")
            
            for i, chunk in enumerate(chunks, 1):
                token_count = chunk_tokens[i-1]
                if i > 1:
                    f.write('<div class="chunk-separator"></div>\n')
                
                color_style = ""
                if token_count > args.max_token_limit:
                    color_style = " style='background-color: #FFE0E0;'"  # Red for oversized
                
                f.write(f'<div class="chunk-header"{color_style}>Chunk {i} ({token_count} tokens)</div>\n')
                f.write(f'<div class="chunk-meta"><strong>Source:</strong> {chunk.metadata.get("source", "N/A")}</div>\n')
                f.write('<div class="chunk-content">\n')
                f.write(chunk.text)
                f.write('\n</div>\n')
            
            f.write("</body>\n</html>")
        
        print(f"All chunks saved to {output_filename}")
        
    except Exception as e:
        print(f"Error during chunking: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
