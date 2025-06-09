#!/usr/bin/env python3

"""
HTML content stripper for Red Hat OpenShift documentation pages.

Extracts the main documentation content by removing navigation elements,
headers, footers, and other non-essential page components. Removes unnecessary
tags and attributes to reduce token count and avoid embedding noise.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional, Tuple
from bs4 import BeautifulSoup, Tag


def _aggressively_strip_tags_and_attributes(soup: BeautifulSoup) -> None:
    """
    Modifies a BeautifulSoup object in-place to strip unwanted tags and attributes.

    Args:
        soup: The BeautifulSoup object to modify.
    """
    # 1. Tags to be unwrapped (content kept, tag removed)
    tags_to_unwrap = [
        'div.titlepage', 'div.itemizedlist', 'div.variablelist',
        'div._additional-resources', 'span.strong', 'span.inlinemediaobject',
        'rh-table', 'colgroup', 'span.term'
    ]
    for selector in tags_to_unwrap:
        for tag in soup.select(selector):
            tag.unwrap()

    # 2. Special transformation for <rh-alert>
    for rh_alert in soup.find_all('rh-alert'):
        state = rh_alert.get('state', 'note')  # Default to 'note' if state is missing
        
        # Find the main content div (the one without the header)
        content_div = rh_alert.find('div', slot=None)
        if not content_div:
            content_div = rh_alert.find('p') # Fallback to finding the first paragraph

        if content_div:
            # Create a new, simpler div
            new_div = soup.new_tag('div')
            new_div['class'] = f'alert alert-{state}'
            new_div.extend(content_div.contents) # Move content
            rh_alert.replace_with(new_div)
        else:
            rh_alert.unwrap() # If structure is unexpected, just unwrap the content

    # 3. Strip attributes from all remaining tags
    # Attributes to keep for specific tags
    attributes_to_keep = {
        'a': ['href', 'title'],
        'section': ['id'],
        'h1': ['id'],
        'h2': ['id'],
        'h3': ['id'],
        'h4': ['id'],
        'h5': ['id'],
        'h6': ['id'],
        'th': ['scope'],
        'img': ['src', 'alt']
    }

    for tag in soup.find_all(True):
        # Get a list of attributes to remove for this tag
        attrs_to_remove = []
        for attr in tag.attrs:
            # Check if this attribute should be kept for this tag type
            if tag.name not in attributes_to_keep or attr not in attributes_to_keep[tag.name]:
                attrs_to_remove.append(attr)
        
        # Remove the identified attributes
        for attr in attrs_to_remove:
            del tag[attr]


def strip_html_content(
    input_file_path: str,
    output_dir: str,
    strip_mode: str,
    preserve_path: bool = True
) -> Optional[str]:
    """
    Extract and clean the main content from an HTML file and save it.

    Args:
        input_file_path: Path to the HTML file to process.
        output_dir: Directory to save the cleaned HTML file.
        strip_mode: The stripping mode ('all', 'sections', 'tags').
        preserve_path: Whether to preserve the directory structure.

    Returns:
        Path to the cleaned HTML file or None if processing failed.
    """
    try:
        with open(input_file_path, "r", encoding="utf-8") as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, "html.parser")

        # Mode 1: Isolate the main content sections (original functionality)
        if strip_mode in ['sections', 'all']:
            body_content = soup.body or soup
            new_soup = BeautifulSoup("<html><body></body></html>", "html.parser")

            breadcrumb = body_content.find("ol", class_="breadcrumb hide-for-print")
            if breadcrumb:
                new_soup.body.append(breadcrumb)

            chapters = body_content.find_all("section", class_="chapter")
            if not chapters:
                # If no chapters, take the whole body as a fallback
                chapters = [body_content]

            for chapter in chapters:
                new_soup.body.append(chapter)
            
            # The new_soup becomes the basis for further stripping
            soup = new_soup

        # Mode 2: Aggressively strip tags and attributes
        if strip_mode in ['tags', 'all']:
            _aggressively_strip_tags_and_attributes(soup)
            
        # Create output path
        if preserve_path:
            # Handle potential absolute paths by making them relative
            try:
                base_input_dir = os.path.commonpath([os.path.dirname(input_file_path), os.getcwd()])
                rel_path = os.path.relpath(input_file_path, start=base_input_dir)
            except ValueError:
                # Fallback for paths on different drives (e.g., Windows)
                rel_path = os.path.basename(input_file_path)

            output_file_path = os.path.join(output_dir, rel_path)
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        else:
            filename = os.path.basename(input_file_path)
            output_file_path = os.path.join(output_dir, filename)
            os.makedirs(output_dir, exist_ok=True)

        with open(output_file_path, "w", encoding="utf-8") as file:
            file.write(str(soup))

        print(f"Cleaned HTML saved to {output_file_path} (mode: {strip_mode})")
        return output_file_path

    except Exception as e:
        print(f"Error processing {input_file_path}: {str(e)}", file=sys.stderr)
        return None


def process_directory(
    input_dir: str,
    output_dir: str,
    strip_mode: str,
    exclusion_list: Optional[List[str]] = None
) -> None:
    """
    Process all HTML files in a directory and its subdirectories.

    Args:
        input_dir: Directory containing HTML files to process.
        output_dir: Directory to save cleaned HTML files.
        strip_mode: The stripping mode ('all', 'sections', 'tags').
        exclusion_list: List of file paths to exclude.
    """
    if exclusion_list is None:
        exclusion_list = []

    processed_files = 0
    skipped_files = 0

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)

                if file_path in exclusion_list:
                    print(f"Skipping excluded file: {file_path}")
                    skipped_files += 1
                    continue

                result = strip_html_content(file_path, output_dir, strip_mode, preserve_path=True)
                if result:
                    processed_files += 1

    print(f"\nProcessed {processed_files} HTML files, skipped {skipped_files} files.")


def main() -> None:
    """Parse command line arguments and run the HTML content stripper."""
    parser = argparse.ArgumentParser(
        description="Strip unnecessary content from HTML documentation files.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "--input", "-i", required=True, help="HTML file or directory to process"
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        default="clean_html",
        help="Directory to save cleaned HTML files (default: 'clean_html')",
    )
    parser.add_argument(
        "--strip-mode",
        choices=['all', 'sections', 'tags'],
        default='all',
        help="""Specify the stripping mode:
  'sections' - Only performs the original logic of isolating chapter/main content.
  'tags'     - Only performs aggressive tag/attribute stripping on the file.
  'all'      - Performs both 'sections' and 'tags' stripping (default)."""
    )
    parser.add_argument(
        "--exclude",
        "-e",
        nargs="+",
        default=[],
        help="Files to exclude from processing",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input path {args.input} does not exist.", file=sys.stderr)
        sys.exit(1)

    if input_path.is_file():
        if not input_path.name.endswith(".html"):
            print(f"Error: Input file {args.input} is not an HTML file.", file=sys.stderr)
            sys.exit(1)
        strip_html_content(str(input_path), args.output_dir, args.strip_mode, preserve_path=False)
    else:
        process_directory(str(input_path), args.output_dir, args.strip_mode, args.exclude)


if __name__ == "__main__":
    main()
