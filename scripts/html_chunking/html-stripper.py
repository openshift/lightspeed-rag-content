#!/usr/bin/env python3

"""
HTML content stripper for Red Hat OpenShift documentation pages.
Removes navigation, headers, footers, and other unnecessary elements,
keeping only the main documentation content.
"""

import argparse
import os
import sys
from pathlib import Path
from bs4 import BeautifulSoup


def strip_html_content(input_file_path, output_dir):
    """
    Extract the main content from an HTML file and save it to the output directory.

    Args:
        input_file_path (str): Path to the HTML file to process
        output_dir (str): Directory to save the cleaned HTML file

    Returns:
        str: Path to the cleaned HTML file
    """
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, 'html.parser')

        new_soup = BeautifulSoup('<html><body></body></html>', 'html.parser')

        page_header = soup.find('div', class_='page-header')

        # Find the main content div
        main_content = soup.find('div', class_='col-xs-12 col-sm-9 col-md-9 main')
        if not main_content:
            main_content = soup.find('div', class_='main')

        if not page_header and not main_content:
            print(f"Warning: Could not identify required content in {input_file_path}")
            return None

        if main_content:
            toc = main_content.find('div', id='toc')
            if toc:
                toc.extract()

        if page_header:
            new_soup.body.append(page_header)

        if main_content:
            new_soup.body.append(main_content)

        rel_path = os.path.relpath(input_file_path)
        output_file_path = os.path.join(output_dir, rel_path)

        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(str(new_soup))

        print(f"Cleaned HTML saved to {output_file_path}")
        return output_file_path

    except Exception as e:
        print(f"Error processing {input_file_path}: {str(e)}")
        return None


def process_directory(input_dir, output_dir, exclusion_list=None):
    """
    Process all HTML files in a directory and its subdirectories.

    Args:
        input_dir (str): Directory containing HTML files to process
        output_dir (str): Directory to save cleaned HTML files
        exclusion_list (list): List of file paths to exclude
    """
    if exclusion_list is None:
        exclusion_list = []

    processed_files = 0
    skipped_files = 0

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)

                if file_path in exclusion_list:
                    print(f"Skipping excluded file: {file_path}")
                    skipped_files += 1
                    continue

                result = strip_html_content(file_path, output_dir)
                if result:
                    processed_files += 1

    print(f"Processed {processed_files} HTML files, skipped {skipped_files} files.")


def main():
    parser = argparse.ArgumentParser(
        description="Strip unnecessary content from HTML documentation files."
    )

    parser.add_argument(
        '--input', '-i', required=True,
        help="HTML file or directory to process"
    )
    parser.add_argument(
        '--output-dir', '-o', default='clean_html',
        help="Directory to save cleaned HTML files (default: 'clean_html')"
    )
    parser.add_argument(
        '--exclude', '-e', nargs='+', default=[],
        help="Files to exclude from processing"
    )

    args = parser.parse_args()

    # Determine if input is a file or directory
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input path {args.input} does not exist.")
        sys.exit(1)

    if input_path.is_file():
        if not input_path.name.endswith('.html'):
            print(f"Error: Input file {args.input} is not an HTML file.")
            sys.exit(1)

        strip_html_content(str(input_path), args.output_dir)
    else:
        process_directory(str(input_path), args.output_dir, args.exclude)


if __name__ == "__main__":
    main()
