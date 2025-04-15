#!/usr/bin/env python3

"""
HTML content stripper for Red Hat OpenShift documentation pages.

Extracts the main documentation content by removing navigation elements,
headers, footers, and other non-essential page components.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional
from bs4 import BeautifulSoup


def strip_html_content(input_file_path: str, output_dir: str) -> Optional[str]:
    """
    Extract the main content from an HTML file and save it to the output directory.

    Args:
        input_file_path: Path to the HTML file to process
        output_dir: Directory to save the cleaned HTML file

    Returns:
        Path to the cleaned HTML file or None if processing failed
    """
    try:
        with open(input_file_path, "r", encoding="utf-8") as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, "html.parser")
        new_soup = BeautifulSoup("<html><body></body></html>", "html.parser")

        # Capture breadcrumbs if they exist
        breadcrumb = soup.find("ol", class_="breadcrumb hide-for-print")
        if breadcrumb:
            new_soup.body.append(breadcrumb)

        # Find all "chapter" sections that contain the main content
        chapters = soup.find_all("section", class_="chapter")

        if not chapters:
            print(f"Warning: No <section class='chapter'> found in {input_file_path}")
            return None

        # Add each chapter to our new document
        for chapter in chapters:
            new_soup.body.append(chapter)

        # Create output path
        rel_path = os.path.relpath(input_file_path)
        output_file_path = os.path.join(output_dir, rel_path)
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

        with open(output_file_path, "w", encoding="utf-8") as file:
            file.write(str(new_soup))

        print(f"Cleaned HTML saved to {output_file_path}")
        return output_file_path

    except Exception as e:
        print(f"Error processing {input_file_path}: {str(e)}")
        return None


def process_directory(
    input_dir: str, output_dir: str, exclusion_list: Optional[List[str]] = None
) -> None:
    """
    Process all HTML files in a directory and its subdirectories.

    Args:
        input_dir: Directory containing HTML files to process
        output_dir: Directory to save cleaned HTML files
        exclusion_list: List of file paths to exclude
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

                result = strip_html_content(file_path, output_dir)
                if result:
                    processed_files += 1

    print(f"Processed {processed_files} HTML files, skipped {skipped_files} files.")


def main() -> None:
    """Parse command line arguments and run the HTML content stripper."""
    parser = argparse.ArgumentParser(
        description="Strip unnecessary content from HTML documentation files."
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
        "--exclude",
        "-e",
        nargs="+",
        default=[],
        help="Files to exclude from processing",
    )

    args = parser.parse_args()

    # Check if input path exists
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input path {args.input} does not exist.")
        sys.exit(1)

    # Process single file or directory
    if input_path.is_file():
        if not input_path.name.endswith(".html"):
            print(f"Error: Input file {args.input} is not an HTML file.")
            sys.exit(1)
        strip_html_content(str(input_path), args.output_dir)
    else:
        process_directory(str(input_path), args.output_dir, args.exclude)


if __name__ == "__main__":
    main()
