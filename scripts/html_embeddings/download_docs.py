"""
Download OpenShift documentation using the portal fetcher.
"""

import asyncio
import logging
import sys
import importlib.util
from pathlib import Path
from typing import Optional

portal_fetcher_path = (
    Path(__file__).parent.parent / "doc_downloader" / "downloader.py"
)
spec = importlib.util.spec_from_file_location(
    "downloader", portal_fetcher_path
)
downloader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(downloader)


def download_documentation(
    version: str,
    product_slug: str,
    doc_url: Optional[str] = None,
    specific_doc: Optional[str] = None,
    output_dir: Path = Path("./downloads"),
    cache_existing: bool = True,
    concurrency: int = 5,
    max_retries: int = 3,
    fail_on_error: bool = False,
) -> bool:
    """
    Download documentation.

    Args:
        version: Product version (e.g., "4.18")
        product_slug: Product URL slug (e.g., "openshift_container_platform")
        doc_url: The full URL to the documentation page.
        specific_doc: Optional specific document to download
        output_dir: Directory to save downloaded files
        cache_existing: Whether to use cached downloads
        concurrency: Number of concurrent downloads
        max_retries: Maximum retry attempts
        fail_on_error: Stop the pipeline if any document fails to download

    Returns:
        True if download was successful
    """
    logger = logging.getLogger(__name__)

    if doc_url is not None:
        base_url = doc_url
    elif specific_doc:
        base_url = f"https://docs.redhat.com/en/documentation/{product_slug}/{version}/html-single/{specific_doc}"
    else:
        base_url = f"https://docs.redhat.com/en/documentation/{product_slug}/{version}"

    logger.info("Downloading from: %s", base_url)
    logger.info("Output directory: %s", output_dir)

    try:
        verification_passed, toc_verification_passed, elapsed_time = asyncio.run(
            downloader.run_downloader(
                base_url=base_url,
                output_dir=str(output_dir),
                concurrency=concurrency,
                force=not cache_existing,
                max_retries=max_retries,
            )
        )

        success = verification_passed and toc_verification_passed

        if success:
            logger.info(
                "Download completed successfully in %.2f seconds", elapsed_time
            )
        else:
            logger.error("Download completed with verification failures")

        return success

    except Exception as e:
        logger.error("Download failed: %s", e)
        return False


def main():
    """Command line interface for standalone usage."""
    import argparse

    parser = argparse.ArgumentParser(description="Download OpenShift documentation")
    parser.add_argument("--version", "-v", required=True, help="OpenShift version")
    parser.add_argument("--specific-doc", "-d", help="Specific document to download")
    parser.add_argument(
        "--output-dir", "-o", default="./downloads", help="Output directory"
    )
    parser.add_argument(
        "--no-cache", action="store_true", help="Don't use cached downloads"
    )
    parser.add_argument(
        "--concurrency", "-c", type=int, default=5, help="Concurrent downloads"
    )
    parser.add_argument(
        "--max-retries", "-r", type=int, default=3, help="Max retry attempts"
    )
    parser.add_argument("--verbose", action="store_true", help="Verbose logging")

    args = parser.parse_args()

    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s - %(levelname)s - %(message)s")

    success = download_documentation(
        version=args.version,
        specific_doc=args.specific_doc,
        output_dir=Path(args.output_dir),
        cache_existing=not args.no_cache,
        concurrency=args.concurrency,
        max_retries=args.max_retries,
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
