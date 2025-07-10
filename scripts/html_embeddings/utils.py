"""
Utility functions for the HTML embeddings pipeline.
"""

import logging
import os
import sys
from pathlib import Path
from typing import Optional, Any


import re
from urllib.parse import urlparse


def setup_logging(verbose: bool = False) -> logging.Logger:
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("html_embeddings.log", encoding="utf-8"),
        ],
    )

    return logging.getLogger(__name__)


def validate_dependencies() -> None:
    """Validate that required dependencies are available."""
    package_import_map = {
        "llama_index": "llama_index",
        "transformers": "transformers",
        "faiss": "faiss",
        "aiohttp": "aiohttp",
        "beautifulsoup4": "bs4",
        "PyYAML": "yaml",
    }

    missing_packages = []
    for package_name, import_name in package_import_map.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)

    if missing_packages:
        raise ImportError("Missing required packages: %s" % ', '.join(missing_packages))


def create_directory_structure(
    cache_dir: str,
    output_dir: str,
    product: dict[str, Any],
    specific_doc: Optional[str] = None,
) -> tuple[dict[str, Path], dict[str, Any]]:
    """Create directory structure for pipeline and return paths and updated product info."""
    logger = logging.getLogger(__name__)

    product_slug = product.get("slug")
    product_version = product.get("version")
    doc_url = product.get("url")

    if doc_url and not product_slug:
        parsed_url = urlparse(doc_url)
        path_parts = parsed_url.path.strip("/").split("/")

        if "redhat.com" in parsed_url.hostname:
            try:
                doc_index = path_parts.index("documentation")
                # Path: /documentation/{lang}/{slug}/{version}/...
                if re.match(r'^[a-z]{2}(-[a-z]{2})?$', path_parts[doc_index + 1]):
                    product_slug = path_parts[doc_index + 2]
                    product_version = path_parts[doc_index + 3]
                else: # Path: /documentation/{slug}/{version}/...
                    product_slug = path_parts[doc_index + 1]
                    product_version = path_parts[doc_index + 2]
            except (ValueError, IndexError):
                logger.warning("Could not parse Red Hat doc URL format for %s", doc_url)
                product_slug = parsed_url.hostname.replace(".", "_")
                product_version = "latest"
        else:
            # Sanitize the full URL to use as a directory path for non-redhat sites
            sanitized_url = re.sub(r'https?://', '', doc_url).replace('/', '_')
            product_slug = sanitized_url
            product_version = ""

    product['slug'] = product_slug
    product['version'] = product_version if product_version else "latest"

    cache_path = Path(cache_dir)
    output_path = Path(output_dir)

    base_cache_path = cache_path / product_slug / product_version if product_version else cache_path / product_slug

    downloads_dir = base_cache_path / "downloads"
    stripped_dir = base_cache_path / "stripped"
    chunks_dir = base_cache_path / "chunks"

    if specific_doc:
        downloads_dir = downloads_dir / specific_doc
        stripped_dir = stripped_dir / specific_doc

    directories = {
        "cache": cache_path,
        "output": output_path,
        "downloads": downloads_dir,
        "stripped": stripped_dir,
        "chunks": chunks_dir,
    }

    for dir_path in directories.values():
        dir_path.mkdir(parents=True, exist_ok=True)

    return directories, product


def sanitize_directory_path(path: str) -> str:
    """Sanitize directory path for security."""
    normalized = os.path.normpath("/" + path).lstrip("/")
    if normalized == "":
        normalized = "."
    return normalized


def check_disk_space(directory: Path, required_gb: float = 1.0) -> bool:
    """Check if directory has sufficient disk space."""
    try:
        stat = os.statvfs(directory)
        available_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
        return available_gb >= required_gb
    except (OSError, AttributeError):
        return True


def get_file_count(directory: Path, pattern: str = "*") -> int:
    """Get count of files matching pattern in directory."""
    if not directory.exists():
        return 0

    try:
        return len(list(directory.rglob(pattern)))
    except Exception:
        return 0


def estimate_processing_time(file_count: int, base_time_per_file: float = 0.5) -> float:
    """Estimate processing time based on file count."""
    return file_count * base_time_per_file


def format_duration(seconds: float) -> str:
    """Format duration in seconds to human readable format."""
    if seconds < 60:
        return "%.1f seconds" % seconds
    elif seconds < 3600:
        minutes = seconds / 60
        return "%.1f minutes" % minutes
    else:
        hours = seconds / 3600
        return "%.1f hours" % hours


def get_cache_info(
    cache_dir: Path, version: str, specific_doc: Optional[str] = None
) -> dict[str, int]:
    """Get information about cached files."""
    base_path = cache_dir / "downloads" / version
    if specific_doc:
        base_path = base_path / specific_doc

    downloads_count = get_file_count(base_path, "*.html")

    base_path = cache_dir / "stripped" / version
    if specific_doc:
        base_path = base_path / specific_doc

    stripped_count = get_file_count(base_path, "*.html")

    base_path = cache_dir / "chunks" / version
    if specific_doc:
        base_path = base_path / specific_doc

    chunks_count = get_file_count(base_path, "*.json")

    return {
        "downloads": downloads_count,
        "stripped": stripped_count,
        "chunks": chunks_count,
    }


def cleanup_cache(cache_dir: Path, keep_days: int = 7) -> None:
    """Clean up old cache files."""
    import time

    current_time = time.time()
    cutoff_time = current_time - (keep_days * 24 * 3600)

    for file_path in cache_dir.rglob("*"):
        if file_path.is_file():
            try:
                if file_path.stat().st_mtime < cutoff_time:
                    file_path.unlink()
            except (OSError, FileNotFoundError):
                pass


def verify_model_directory(model_dir: str) -> bool:
    """Verify that model directory contains required files."""
    model_path = Path(model_dir)

    required_files = ["config.json", "pytorch_model.bin", "tokenizer.json", "vocab.txt"]

    if not (model_path / "pytorch_model.bin").exists():
        safetensors_files = list(model_path.glob("*.safetensors"))
        if safetensors_files:
            required_files.remove("pytorch_model.bin")

    missing_files = []
    for file_name in required_files:
        if not (model_path / file_name).exists():
            missing_files.append(file_name)

    if missing_files:
        logging.warning("Model directory missing files: %s", missing_files)
        return False

    return True


def validate_version_format(version: str) -> bool:
    """Validate OpenShift version format."""
    import re

    pattern = r"^\d+\.\d+$"
    return bool(re.match(pattern, version))


def get_output_summary(output_dir: Path) -> dict[str, any]:
    """Get summary of output files."""
    metadata_file = output_dir / "metadata.json"

    summary = {
        "exists": output_dir.exists(),
        "has_metadata": metadata_file.exists(),
        "file_count": get_file_count(output_dir),
        "metadata": None,
    }

    if summary["has_metadata"]:
        try:
            import json

            with open(metadata_file, "r", encoding="utf-8") as f:
                summary["metadata"] = json.load(f)
        except Exception:
            pass

    return summary
