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
from typing import List, Optional
from bs4 import BeautifulSoup, Tag

# Constants
MAX_UNWRAP_PASSES = 5


def _aggressively_strip_tags_and_attributes(soup: BeautifulSoup, strip_links: bool) -> None:
    """
    Modifies a BeautifulSoup object in-place to strip unwanted tags and attributes.

    Args:
        soup: The BeautifulSoup object to modify.
        strip_links: If True, unwraps <a> tags, keeping only the text.
    """
    # 1. Tags to be unwrapped (content kept, tag removed)
    tags_to_unwrap = [
        'div.titlepage', 'div.itemizedlist', 'div.variablelist',
        'div._additional-resources', 'span.strong', 'span.inlinemediaobject',
        'rh-table', 'colgroup', 'span'
    ]
    if strip_links:
        tags_to_unwrap.append('a')
        
    for selector in tags_to_unwrap:
        for tag in soup.select(selector):
            try:
                tag.unwrap()
            except ValueError:
                continue

    # 2. Special transformation for <rh-alert>
    for rh_alert in soup.find_all('rh-alert'):
        state = rh_alert.get('state', 'note')
        content_div = rh_alert.find('div', slot=None) or rh_alert.find('p')

        if content_div:
            new_div = soup.new_tag('div')
            new_div['class'] = f'alert alert-{state}'
            new_div.extend(content_div.contents)
            rh_alert.replace_with(new_div)
        else:
            try:
                rh_alert.unwrap()
            except ValueError:
                continue

    # 3. Strip attributes from all remaining tags
    attributes_to_keep = {
        'a': ['href', 'title'],
        'section': ['id'],
        'h1': ['id'], 'h2': ['id'], 'h3': ['id'],
        'h4': ['id'], 'h5': ['id'], 'h6': ['id'],
        'th': ['scope'],
        'img': ['src', 'alt']
    }

    for tag in soup.find_all(True):
        attrs_to_remove = [
            attr for attr in tag.attrs 
            if attr not in attributes_to_keep.get(tag.name, [])
        ]
        for attr in attrs_to_remove:
            del tag[attr]

    # 4. Unwrap nested, attribute-less divs
    for _ in range(MAX_UNWRAP_PASSES):  # Run multiple passes to handle deeply nested structures
        unwrapped_in_pass = False
        for tag in soup.find_all('div', attrs={}):
            child_elements = [c for c in tag.children if isinstance(c, Tag)]
            if len(child_elements) == 1 and not tag.get_text(strip=True):
                tag.unwrap()
                unwrapped_in_pass = True
        if not unwrapped_in_pass:
            break

    # 5. Remove tags that have become empty after stripping
    tags_to_check_for_emptiness = ['p', 'div', 'li', 'ul', 'ol', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'section', 'dd', 'dt']
    for tag in soup.find_all(tags_to_check_for_emptiness):
        if not tag.get_text(strip=True) and not tag.find_all(recursive=False):
            tag.decompose()


def strip_html_content(
    input_file_path: str,
    output_dir: str,
    strip_mode: str,
    strip_links: bool,
    preserve_path: bool = True
) -> Optional[str]:
    """
    Extract and clean the main content from an HTML file and save it.
    """
    try:
        with open(input_file_path, "r", encoding="utf-8") as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, "html.parser")

        if strip_mode in ['sections', 'all']:
            body_content = soup.body or soup
            new_soup = BeautifulSoup("<html><body></body></html>", "html.parser")

            chapters = body_content.find_all("section", class_="chapter")
            if not chapters:
                chapters = [body_content]

            for chapter in chapters:
                new_soup.body.append(chapter.extract())
            
            soup = new_soup

        if strip_mode in ['tags', 'all']:
            _aggressively_strip_tags_and_attributes(soup, strip_links)
            
        if preserve_path:
            try:
                base_input_dir = os.path.abspath(os.path.dirname(input_file_path))
                rel_path = os.path.relpath(input_file_path, start=base_input_dir)
            except ValueError:
                rel_path = os.path.basename(input_file_path)

            output_file_path = os.path.join(output_dir, rel_path)
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        else:
            filename = os.path.basename(input_file_path)
            output_file_path = os.path.join(output_dir, filename)
            os.makedirs(output_dir, exist_ok=True)

        with open(output_file_path, "w", encoding="utf-8") as file:
            file.write(str(soup.prettify()))

        print(f"Cleaned HTML saved to {output_file_path} (mode: {strip_mode}, strip-links: {strip_links})")
        return output_file_path

    except Exception as e:
        print(f"Error processing {input_file_path}: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return None


def process_directory(
    input_dir: str,
    output_dir: str,
    strip_mode: str,
    strip_links: bool,
    exclusion_list: Optional[List[str]] = None
) -> None:
    """
    Process all HTML files in a directory and its subdirectories.
    """
    if exclusion_list is None:
        exclusion_list = []
    
    abs_input_dir = os.path.abspath(input_dir)

    processed_files = 0
    skipped_files = 0

    for root, _, files in os.walk(abs_input_dir):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)

                if file_path in exclusion_list:
                    print(f"Skipping excluded file: {file_path}")
                    skipped_files += 1
                    continue
                
                # Make a path relative to the input dir to preserve structure in output
                relative_dir = os.path.relpath(root, abs_input_dir)
                current_output_dir = os.path.join(output_dir, relative_dir)

                result = strip_html_content(file_path, current_output_dir, strip_mode, strip_links, preserve_path=False)
                if result:
                    processed_files += 1

    print(f"\nProcessed {processed_files} HTML files, skipped {skipped_files} files.")


def main() -> None:
    """Parse command line arguments and run the HTML content stripper."""
    parser = argparse.ArgumentParser(
        description="Strip unnecessary content from HTML documentation files.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument("-i", "--input", required=True, help="HTML file or directory to process")
    parser.add_argument("-o", "--output-dir", default="clean_html", help="Directory to save cleaned HTML files (default: 'clean_html')")
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
        "--no-link-stripping",
        action="store_false",
        dest="strip_links",
        help="Keep <a> tags and their href/title attributes. By default, links are stripped."
    )
    parser.add_argument("-e", "--exclude", nargs="+", default=[], help="Files to exclude from processing")
    parser.set_defaults(strip_links=True)

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input path {args.input} does not exist.", file=sys.stderr)
        sys.exit(1)

    if input_path.is_file():
        if not input_path.name.endswith(".html"):
            print(f"Error: Input file {args.input} is not an HTML file.", file=sys.stderr)
            sys.exit(1)
        strip_html_content(str(input_path), args.output_dir, args.strip_mode, args.strip_links, preserve_path=False)
    else:
        process_directory(str(input_path), args.output_dir, args.strip_mode, args.strip_links, args.exclude)

if __name__ == "__main__":
    main()
