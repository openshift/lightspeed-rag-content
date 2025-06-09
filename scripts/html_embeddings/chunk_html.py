"""
Chunk HTML documents semantically using the HTML chunking library.
"""

import json
import logging
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse

# Import the HTML chunking library
sys.path.insert(0, str(Path(__file__).parent.parent / "html_chunking"))
from chunker import chunk_html
from tokenizer import count_html_tokens


def chunk_html_documents(
    input_dir: Path,
    output_dir: Path,
    max_token_limit: int = 380,
    count_tag_tokens: bool = True,
    keep_siblings_together: bool = True,
    prepend_parent_section_text: bool = True,
) -> bool:
    """
    Chunk all HTML documents in input directory.

    Args:
        input_dir: Directory containing stripped HTML files
        output_dir: Directory to save chunked content
        max_token_limit: Maximum tokens per chunk
        count_tag_tokens: Whether to count HTML tags in token count
        keep_siblings_together: Keep sibling sections together when possible
        prepend_parent_section_text: Prepend parent section text to chunks

    Returns:
        True if chunking was successful
    """
    logger = logging.getLogger(__name__)

    if not input_dir.exists():
        logger.error("Input directory does not exist: %s", input_dir)
        return False

    html_files = list(input_dir.rglob("*.html"))
    if not html_files:
        logger.warning("No HTML files found in %s", input_dir)
        return True

    logger.info("Found %s HTML files to chunk", len(html_files))

    try:
        output_dir.mkdir(parents=True, exist_ok=True)

        total_chunks = 0
        processed_files = 0

        for html_file in html_files:
            logger.debug("Processing %s", html_file)

            success, chunk_count = chunk_single_html_file(
                input_file=html_file,
                output_dir=output_dir,
                input_base_dir=input_dir,
                max_token_limit=max_token_limit,
                count_tag_tokens=count_tag_tokens,
                keep_siblings_together=keep_siblings_together,
                prepend_parent_section_text=prepend_parent_section_text,
            )

            if success:
                processed_files += 1
                total_chunks += chunk_count
                logger.debug("Processed %s: %s chunks", html_file, chunk_count)
            else:
                logger.warning("Failed to process %s", html_file)

        logger.info("Successfully processed %s/%s files", processed_files, len(html_files))
        logger.info("Generated %s total chunks", total_chunks)

        summary = {
            "total_files": len(html_files),
            "processed_files": processed_files,
            "total_chunks": total_chunks,
            "chunking_params": {
                "max_token_limit": max_token_limit,
                "count_tag_tokens": count_tag_tokens,
                "keep_siblings_together": keep_siblings_together,
                "prepend_parent_section_text": prepend_parent_section_text,
            },
        }

        with open(output_dir / "chunking_summary.json", "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

        return processed_files > 0

    except Exception as e:
        logger.error("HTML chunking failed: %s", e)
        return False


def chunk_single_html_file(
    input_file: Path,
    output_dir: Path,
    input_base_dir: Path,
    max_token_limit: int = 380,
    count_tag_tokens: bool = True,
    keep_siblings_together: bool = True,
    prepend_parent_section_text: bool = True,
) -> tuple[bool, int]:
    """
    Chunk a single HTML file.

    Args:
        input_file: Path to input HTML file
        output_dir: Directory to save chunks
        input_base_dir: Base directory for input files (for relative path calculation)
        max_token_limit: Maximum tokens per chunk
        count_tag_tokens: Whether to count HTML tags
        keep_siblings_together: Keep sibling sections together
        prepend_parent_section_text: Prepend parent section text

    Returns:
        Tuple of (success, chunk_count)
    """
    logger = logging.getLogger(__name__)

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            html_content = f.read()

        if not html_content.strip():
            logger.warning("Empty file: %s", input_file)
            return True, 0

        chunks = chunk_html(
            html_content=html_content,
            max_token_limit=max_token_limit,
            count_tag_tokens=count_tag_tokens,
            keep_siblings_together=keep_siblings_together,
            prepend_parent_section_text=prepend_parent_section_text,
        )

        if not chunks:
            logger.warning("No chunks generated for %s", input_file)
            return True, 0

        relative_path = input_file.relative_to(input_base_dir)
        base_metadata = extract_metadata_from_path(relative_path)

        chunk_count = 0
        for i, chunk_content in enumerate(chunks):
            chunk_metadata = {
                **base_metadata,
                "chunk_index": i,
                "total_chunks": len(chunks),
                "token_count": count_html_tokens(chunk_content, count_tag_tokens),
                "source_file": str(relative_path),
            }

            chunk_data = {
                "id": f"{base_metadata['doc_id']}_chunk_{i:04d}",
                "content": chunk_content,
                "metadata": chunk_metadata,
            }

            chunk_filename = f"{base_metadata['doc_id']}_chunk_{i:04d}.json"
            chunk_file_path = output_dir / chunk_filename

            with open(chunk_file_path, "w", encoding="utf-8") as f:
                json.dump(chunk_data, f, indent=2, ensure_ascii=False)

            chunk_count += 1

        return True, chunk_count

    except Exception as e:
        logger.error("Error chunking %s: %s", input_file, e)
        return False, 0


def extract_metadata_from_path(file_path: Path) -> Dict[str, Any]:
    """
    Extract metadata from file path.

    Args:
        file_path: Relative path to the file

    Returns:
        Dictionary with extracted metadata
    """
    parts = file_path.parts

    if len(parts) >= 2 and parts[-1] == "index.html":
        doc_name = parts[-2]
    else:
        doc_name = file_path.stem

    doc_id = doc_name.replace(" ", "_").replace("-", "_").lower()

    version = None
    for part in parts:
        # Heuristic to find OpenShift versions like "4.1", "4.12", etc.
        if part.startswith("4.") and len(part) <= 5:
            version = part
            break

    return {
        "doc_name": doc_name,
        "doc_id": doc_id,
        "version": version,
        "file_path": str(file_path),
        "doc_type": "openshift_documentation",
    }


def validate_chunks(output_dir: Path, max_token_limit: int) -> Dict[str, Any]:
    """
    Validate generated chunks.

    Args:
        output_dir: Directory containing chunks
        max_token_limit: Expected maximum token limit

    Returns:
        Validation results
    """
    logger = logging.getLogger(__name__)

    chunk_files = list(output_dir.glob("*.json"))

    if not chunk_files:
        return {"valid": False, "error": "No chunk files found"}

    validation_results = {
        "total_chunks": len(chunk_files),
        "valid_chunks": 0,
        "oversized_chunks": 0,
        "undersized_chunks": 0,
        "empty_chunks": 0,
        "invalid_json": 0,
        "token_stats": {"min": float("inf"), "max": 0, "avg": 0, "total": 0},
    }

    token_counts = []

    for chunk_file in chunk_files:
        try:
            with open(chunk_file, "r", encoding="utf-8") as f:
                chunk_data = json.load(f)

            content = chunk_data.get("content", "")
            metadata = chunk_data.get("metadata", {})
            token_count = metadata.get("token_count", 0)

            if not content.strip():
                validation_results["empty_chunks"] += 1
                continue

            # Allow for a 10% tolerance on the max token limit for oversized chunks
            if token_count > max_token_limit * 1.1:
                validation_results["oversized_chunks"] += 1
            elif token_count < max_token_limit * 0.1:
                validation_results["undersized_chunks"] += 1
            else:
                validation_results["valid_chunks"] += 1

            token_counts.append(token_count)

        except json.JSONDecodeError:
            validation_results["invalid_json"] += 1
            logger.warning("Invalid JSON in %s", chunk_file)
        except Exception as e:
            logger.warning("Error validating %s: %s", chunk_file, e)

    if token_counts:
        validation_results["token_stats"] = {
            "min": min(token_counts),
            "max": max(token_counts),
            "avg": sum(token_counts) / len(token_counts),
            "total": sum(token_counts),
        }

    validation_results["valid"] = (
        validation_results["valid_chunks"] > 0
        and validation_results["invalid_json"] == 0
        and validation_results["empty_chunks"] < len(chunk_files) * 0.1
    )

    return validation_results


def get_chunking_stats(output_dir: Path) -> Dict[str, Any]:
    """
    Get statistics about chunked documents.

    Args:
        output_dir: Directory containing chunks

    Returns:
        Statistics dictionary
    """
    chunk_files = list(output_dir.glob("*.json"))

    if not chunk_files:
        return {"total_chunks": 0}

    doc_counts = {}
    token_counts = []

    for chunk_file in chunk_files:
        try:
            with open(chunk_file, "r", encoding="utf-8") as f:
                chunk_data = json.load(f)

            metadata = chunk_data.get("metadata", {})
            doc_name = metadata.get("doc_name", "unknown")
            token_count = metadata.get("token_count", 0)

            doc_counts[doc_name] = doc_counts.get(doc_name, 0) + 1
            token_counts.append(token_count)

        except Exception:
            continue

    stats = {
        "total_chunks": len(chunk_files),
        "documents": len(doc_counts),
        "chunks_per_doc": doc_counts,
        "avg_chunks_per_doc": (
            sum(doc_counts.values()) / len(doc_counts) if doc_counts else 0
        ),
    }

    if token_counts:
        stats["token_stats"] = {
            "min": min(token_counts),
            "max": max(token_counts),
            "avg": sum(token_counts) / len(token_counts),
            "median": sorted(token_counts)[len(token_counts) // 2],
        }

    return stats


def main():
    """Command line interface for standalone usage."""
    import argparse

    parser = argparse.ArgumentParser(description="Chunk HTML documents semantically")
    parser.add_argument("--input-dir", "-i", required=True, help="Input directory")
    parser.add_argument("--output-dir", "-o", required=True, help="Output directory")
    parser.add_argument(
        "--max-token-limit", "-t", type=int, default=380, help="Max tokens per chunk"
    )
    parser.add_argument(
        "--no-count-tag-tokens", action="store_true", help="Don't count HTML tags"
    )
    parser.add_argument(
        "--no-keep-siblings", action="store_true", help="Don't keep siblings together"
    )
    parser.add_argument(
        "--no-prepend-parent", action="store_true", help="Don't prepend parent text"
    )
    parser.add_argument("--verbose", action="store_true", help="Verbose logging")
    parser.add_argument(
        "--validate", action="store_true", help="Validate chunks after generation"
    )
    parser.add_argument("--stats", action="store_true", help="Show chunking statistics")

    args = parser.parse_args()

    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s - %(levelname)s - %(message)s")

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)

    success = chunk_html_documents(
        input_dir=input_dir,
        output_dir=output_dir,
        max_token_limit=args.max_token_limit,
        count_tag_tokens=not args.no_count_tag_tokens,
        keep_siblings_together=not args.no_keep_siblings,
        prepend_parent_section_text=not args.no_prepend_parent,
    )

    if args.validate and success:
        print("\nValidating chunks...")
        validation = validate_chunks(output_dir, args.max_token_limit)
        print("Validation: %s" % ('PASSED' if validation['valid'] else 'FAILED'))
        print("  Total chunks: %s" % validation['total_chunks'])
        print("  Valid chunks: %s" % validation['valid_chunks'])
        print("  Oversized chunks: %s" % validation['oversized_chunks'])
        print("  Undersized chunks: %s" % validation['undersized_chunks'])
        print("  Empty chunks: %s" % validation['empty_chunks'])

    if args.stats and success:
        print("\nChunking Statistics:")
        stats = get_chunking_stats(output_dir)
        print("  Total chunks: %s" % stats['total_chunks'])
        print("  Documents: %s" % stats['documents'])
        print("  Avg chunks per doc: %.1f" % stats['avg_chunks_per_doc'])
        if "token_stats" in stats:
            ts = stats["token_stats"]
            print(
                "  Token stats - Min: %s, Max: %s, Avg: %.1f"
                % (ts['min'], ts['max'], ts['avg'])
            )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
