#!/usr/bin/env python3
"""
Example script demonstrating the HTML chunking library.

This script shows how to use the HTML chunker with a sample HTML document.
"""

import os
import sys
import json
from chunker import chunk_html
from tokenizer import count_html_tokens, set_custom_tokenizer

def main():
    """Run the HTML chunking example."""
    print("HTML Chunking Example")
    print("====================\n")
    
    # Load the HTML sample document
    sample_path = "example.html"
    if not os.path.exists(sample_path):
        print(f"Error: Sample document {sample_path} not found.")
        print("Make sure example.html is in the current directory.")
        return 1
    
    try:
        with open(sample_path, "r", encoding="utf-8") as f:
            sample_html = f.read()
    except Exception as e:
        print(f"Error reading HTML file: {e}")
        return 1
    
    # Count tokens in the original document
    try:
        print("Counting tokens in the document...")
        original_tokens = count_html_tokens(sample_html)
        print(f"Original document has {original_tokens} tokens\n")
    except Exception as e:
        print(f"Error counting tokens: {e}")
        print("Will proceed with chunking anyway")
    
    # Chunk with default settings
    try:
        # First, set maximum token limit
        max_token_limit = 500
        print(f"Chunking with max {max_token_limit} tokens per chunk...")
        
        # Perform chunking
        chunks = chunk_html(
            sample_html, 
            max_token_limit=max_token_limit,
            count_tag_tokens=True,
            keep_siblings_together=True,
            prepend_parent_section_text=True
        )
        
        # Print chunk information
        print(f"Created {len(chunks)} chunks:")
        
        # Check if chunks are reasonable
        unreasonable_chunks = 0
        too_small_chunks = 0
        for i, chunk in enumerate(chunks, 1):
            token_count = count_html_tokens(chunk)
            
            # Check if chunk is too small (less than 20% of the limit)
            if token_count < max_token_limit * 0.2:
                too_small_chunks += 1
            
            # Check if chunk is way too large
            if token_count > max_token_limit * 1.2:
                unreasonable_chunks += 1
                
            # Print info for first 5 chunks
            if i <= 5:
                print(f"  Chunk {i}: {token_count} tokens")
                # Show a brief preview of the chunk's content
                soup_chunk = chunk.replace("\n", " ").strip()
                preview = soup_chunk[:100] + "..." if len(soup_chunk) > 100 else soup_chunk
                print(f"  Preview: {preview}\n")
        
        if i > 5:
            print(f"  ... and {len(chunks) - 5} more chunks\n")
            
        if too_small_chunks > 0:
            print(f"Warning: {too_small_chunks} chunks are less than 20% of the token limit.")
        
        if unreasonable_chunks > 0:
            print(f"Warning: {unreasonable_chunks} chunks exceed the token limit by more than 20%.")
        
        # Save all chunks to a single file with separators
        print("\nSaving all chunks to a single file...")
        with open("chunked_output.html", "w", encoding="utf-8") as f:
            f.write("<!DOCTYPE html>\n<html>\n<head>\n")
            f.write("<title>Chunked HTML Document</title>\n")
            f.write("<style>\n")
            f.write(".chunk-separator { margin: 20px 0; border-top: 5px solid #3c82f6; padding-top: 10px; }\n")
            f.write(".chunk-header { background-color: #f0f0f0; padding: 10px; font-weight: bold; margin-bottom: 10px; font-size: 16px; }\n")
            f.write(".chunk-content { border: 1px solid #ddd; padding: 15px; }\n")
            f.write("body { font-family: Arial, sans-serif; max-width: 1200px; margin: 20px auto; padding: 0 20px; }\n")
            f.write("</style>\n")
            f.write("</head>\n<body>\n")
            
            f.write("<h1>Chunked HTML Document</h1>\n")
            f.write(f"<p><strong>Original document:</strong> {original_tokens} tokens</p>\n")
            f.write(f"<p><strong>Split into:</strong> {len(chunks)} chunks with max {max_token_limit} tokens per chunk</p>\n")
            f.write("<p><strong>Chunking settings:</strong></p>\n")
            f.write("<ul>\n")
            f.write("  <li>count_tag_tokens: Yes</li>\n")
            f.write("  <li>keep_siblings_together: Yes</li>\n")
            f.write("  <li>prepend_parent_section_text: Yes</li>\n")
            f.write("</ul>\n")
            
            # Add a statistics table
            f.write("<h2>Chunk Statistics</h2>\n")
            f.write("<table border='1' cellpadding='5' style='border-collapse: collapse; width: 100%;'>\n")
            f.write("<tr><th>Statistic</th><th>Value</th></tr>\n")
            f.write(f"<tr><td>Number of chunks</td><td>{len(chunks)}</td></tr>\n")
            
            # Calculate more statistics
            chunk_tokens = [count_html_tokens(chunk) for chunk in chunks]
            avg_tokens = sum(chunk_tokens) / len(chunk_tokens) if chunk_tokens else 0
            min_tokens = min(chunk_tokens) if chunk_tokens else 0
            max_tokens = max(chunk_tokens) if chunk_tokens else 0
            
            f.write(f"<tr><td>Average tokens per chunk</td><td>{avg_tokens:.1f}</td></tr>\n")
            f.write(f"<tr><td>Minimum tokens</td><td>{min_tokens}</td></tr>\n")
            f.write(f"<tr><td>Maximum tokens</td><td>{max_tokens}</td></tr>\n")
            f.write(f"<tr><td>Chunks below 100 tokens</td><td>{sum(1 for t in chunk_tokens if t < 100)}</td></tr>\n")
            f.write(f"<tr><td>Chunks above token limit</td><td>{sum(1 for t in chunk_tokens if t > max_token_limit)}</td></tr>\n")
            f.write("</table>\n<br><hr><br>\n")
            
            for i, chunk in enumerate(chunks, 1):
                token_count = count_html_tokens(chunk)
                if i > 1:
                    f.write('<div class="chunk-separator"></div>\n')
                
                # Add token count color based on size
                color_class = ""
                if token_count < max_token_limit * 0.2:
                    color_class = " style='background-color: #FFF0F0;'"  # Light red for too small
                elif token_count > max_token_limit * 1.1:
                    color_class = " style='background-color: #FFE0E0;'"  # Red for too large
                
                f.write(f'<div class="chunk-header"{color_class}>Chunk {i} ({token_count} tokens)</div>\n')
                f.write('<div class="chunk-content">\n')
                f.write(chunk)
                f.write('\n</div>\n')
            
            f.write("</body>\n</html>")
        
        print(f"All chunks saved to chunked_output.html")
        
    except Exception as e:
        print(f"Error during chunking: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
