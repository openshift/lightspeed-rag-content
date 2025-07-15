"""
Strip HTML ballast from downloaded documentation.
"""

import logging
import sys
import importlib.util
from pathlib import Path
from typing import Optional

# Load the html-stripper utility dynamically
html_stripper_path = Path(__file__).parent.parent / "html_chunking" / "html-stripper.py"
spec = importlib.util.spec_from_file_location("html_stripper", html_stripper_path)
html_stripper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(html_stripper)


def strip_html_content(
    input_dir: Path, output_dir: Path, exclusion_list: Optional[list[str]] = None
) -> bool:
    """
    Strip HTML ballast from all files in input directory.

    Args:
        input_dir: Directory containing downloaded HTML files
        output_dir: Directory to save stripped HTML files
        exclusion_list: Optional list of files to exclude

    Returns:
        True if stripping was successful
    """
    logger = logging.getLogger(__name__)

    if not input_dir.exists():
        logger.error("Input directory does not exist: %s", input_dir)
        return False

    html_files = list(input_dir.rglob("*.html"))
    if not html_files:
        logger.warning("No HTML files found in %s", input_dir)
        return True

    logger.info("Found %s HTML files to process", len(html_files))

    try:
        processed_files = 0
        # This logic is now more direct to avoid path ambiguities.
        # It iterates through found files and constructs a precise output path.
        for input_file in html_files:
            if exclusion_list is not None and str(input_file) in exclusion_list:
                logger.debug("Skipping excluded file: %s", input_file)
                continue

            # Calculate the output path by replacing the input base dir with the output base dir.
            relative_path = input_file.relative_to(input_dir)
            output_file_path = output_dir / relative_path

            # Ensure the parent directory for the output file exists.
            output_file_path.parent.mkdir(parents=True, exist_ok=True)

            # Call the single-file stripper from the utility script.
            # We pass the direct parent of the target file as the output directory
            # and tell the utility not to handle path preservation itself.
            result_path_str = html_stripper.strip_html_content(
                input_file_path=str(input_file),
                output_dir=str(output_file_path.parent),
                strip_mode='all',
                strip_links=True,
                preserve_path=False,
            )

            if result_path_str:
                processed_files += 1

        logger.info("Successfully processed %s files", processed_files)

        if processed_files < len(html_files) * 0.8:
            logger.warning(
                "Fewer output files than expected - some processing may have failed"
            )

        return processed_files > 0

    except Exception as e:
        logger.error("HTML stripping failed: %s", e)
        return False


def strip_single_html_file(input_file: Path, output_file: Path) -> bool:
    """
    Strip HTML ballast from a single file.

    Args:
        input_file: Path to input HTML file
        output_file: Path to output stripped HTML file

    Returns:
        True if stripping was successful
    """
    logger = logging.getLogger(__name__)

    if not input_file.exists():
        logger.error("Input file does not exist: %s", input_file)
        return False

    try:
        output_file.parent.mkdir(parents=True, exist_ok=True)

        result = html_stripper.strip_html_content(
            input_file_path=str(input_file),
            output_dir=str(output_file.parent),
            strip_mode='all',
            strip_links=True,
            preserve_path=False,
        )

        if result:
            logger.info("Successfully stripped %s -> %s", input_file, output_file)
            return True
        else:
            logger.error("Failed to strip %s", input_file)
            return False

    except Exception as e:
        logger.error("Error stripping %s: %s", input_file, e)
        return False


def validate_stripped_html(file_path: Path) -> bool:
    """
    Validate that stripped HTML file contains expected content.

    Args:
        file_path: Path to stripped HTML file

    Returns:
        True if file appears to be properly stripped
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        required_elements = ["<html>", "<body>", "</html>", "</body>"]
        has_required = all(elem in content for elem in required_elements)

        unwanted_elements = [
            'class="breadcrumb"',
            'class="navigation"',
            'class="sidebar"',
            'id="navigation"',
        ]
        has_unwanted = any(elem in content for elem in unwanted_elements)

        has_chapter = '<section class="chapter">' in content

        return has_required and not has_unwanted and has_chapter

    except Exception:
        return False


def get_stripping_stats(input_dir: Path, output_dir: Path) -> dict:
    """
    Get statistics about the stripping process.

    Args:
        input_dir: Input directory
        output_dir: Output directory

    Returns:
        Dictionary with statistics
    """
    input_files = list(input_dir.rglob("*.html")) if input_dir.exists() else []
    output_files = list(output_dir.rglob("*.html")) if output_dir.exists() else []

    input_size = sum(f.stat().st_size for f in input_files if f.exists())
    output_size = sum(f.stat().st_size for f in output_files if f.exists())

    size_reduction = 0
    if input_size > 0:
        size_reduction = ((input_size - output_size) / input_size) * 100

    return {
        "input_files": len(input_files),
        "output_files": len(output_files),
        "input_size_mb": input_size / (1024 * 1024),
        "output_size_mb": output_size / (1024 * 1024),
        "size_reduction_percent": size_reduction,
        "success_rate": (
            (len(output_files) / len(input_files) * 100) if input_files else 0
        ),
    }


def main():
    """Command line interface for standalone usage."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Strip HTML ballast from documentation"
    )
    parser.add_argument("--input-dir", "-i", required=True, help="Input directory")
    parser.add_argument("--output-dir", "-o", required=True, help="Output directory")
    parser.add_argument(
        "--exclude", "-e", nargs="+", default=[], help="Files to exclude"
    )
    parser.add_argument("--verbose", action="store_true", help="Verbose logging")
    parser.add_argument(
        "--stats", action="store_true", help="Show processing statistics"
    )

    args = parser.parse_args()

    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s - %(levelname)s - %(message)s")

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)

    success = strip_html_content(
        input_dir=input_dir, output_dir=output_dir, exclusion_list=args.exclude
    )

    if args.stats:
        stats = get_stripping_stats(input_dir, output_dir)
        print("\nStripping Statistics:")
        print(f"  Input files: {stats['input_files']}")
        print(f"  Output files: {stats['output_files']}")
        print(f"  Input size: {stats['input_size_mb']:.1f} MB")
        print(f"  Output size: {stats['output_size_mb']:.1f} MB")
        print(f"  Size reduction: {stats['size_reduction_percent']:.1f}%")
        print(f"  Success rate: {stats['success_rate']:.1f}%")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
