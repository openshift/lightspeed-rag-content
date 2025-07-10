#!/usr/bin/env python3
"""
HTML-based embeddings generation pipeline for OpenShift documentation.

This script orchestrates the complete pipeline:
1. Download HTML docs from Red Hat portal
2. Strip HTML ballast
3. Chunk HTML semantically
4. Process runbooks (Markdown)
5. Generate embeddings and store in vector DB
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Optional, Any

import re
import yaml
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).parent))

from download_docs import download_documentation
from strip_html import strip_html_content
from chunk_html import chunk_html_documents
from process_runbooks import process_runbooks
from utils import setup_logging, create_directory_structure, validate_dependencies

import faiss
from llama_index.core import Settings, VectorStoreIndex
from llama_index.core.llms.utils import resolve_llm
from llama_index.core.schema import TextNode
from llama_index.core.storage.storage_context import StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.faiss import FaissVectorStore


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate embeddings from documentation.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Input source group
    source_group = parser.add_argument_group(
        "Input Source", "Specify the documentation source (choose one method)"
    )
    source_exclusive_group = source_group.add_mutually_exclusive_group(required=True)
    source_exclusive_group.add_argument(
        "--doc-url",
        help="The full URL to the documentation's page.",
    )
    source_exclusive_group.add_argument(
        "--doc-url-slug",
        help="The product's documentation slug (e.g., 'openshift_container_platform').",
    )
    source_exclusive_group.add_argument(
        "--config-file",
        type=Path,
        help="Path to a YAML or JSON configuration file specifying products to process.",
    )

    parser.add_argument(
        "--doc-url-version",
        default="latest",
        help="The product version. Defaults to 'latest'. Used with --doc-url-slug.",
    )
    parser.add_argument(
        "--specific-doc",
        "-d",
        help="Optional specific document to download (e.g., 'monitoring').",
    )
    parser.add_argument(
        "--output-dir", "-o", default="./vector_db", help="Vector DB output directory"
    )
    parser.add_argument(
        "--model-dir",
        "-md",
        default="./embeddings_model",
        help="Directory containing the embedding model",
    )
    parser.add_argument(
        "--index", "-i", help="Product index name (auto-generated if not provided)"
    )

    parser.add_argument(
        "--use-cached-downloads",
        action="store_true",
        help="Use existing downloads instead of re-fetching",
    )
    parser.add_argument(
        "--skip-runbooks", action="store_true", help="Skip runbooks processing"
    )
    parser.add_argument(
        "--cache-dir", default="./cache", help="Directory for intermediate files"
    )
    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Continue with cached data if a step fails",
    )
    parser.add_argument(
        "--fail-on-download-error",
        action="store_true",
        help="Stop the pipeline if any document fails to download. Default is to continue.",
    )

    parser.add_argument(
        "--max-token-limit", type=int, default=380, help="Maximum tokens per chunk"
    )
    parser.add_argument(
        "--count-tag-tokens",
        action="store_true",
        default=True,
        help="Include HTML tags in token count (default: True)",
    )
    parser.add_argument(
        "--no-count-tag-tokens",
        dest="count_tag_tokens",
        action="store_false",
        help="Exclude HTML tags from token count",
    )
    parser.add_argument(
        "--keep-siblings-together",
        action="store_true",
        default=True,
        help="Keep sibling sections together when possible (default: True)",
    )
    parser.add_argument(
        "--no-keep-siblings-together",
        dest="keep_siblings_together",
        action="store_false",
        help="Don't keep sibling sections together",
    )
    parser.add_argument(
        "--prepend-parent-text",
        action="store_true",
        default=True,
        help="Prepend parent section text to child sections (default: True)",
    )
    parser.add_argument(
        "--no-prepend-parent-text",
        dest="prepend_parent_text",
        action="store_false",
        help="Don't prepend parent section text",
    )

    parser.add_argument(
        "--chunk",
        "-c",
        type=int,
        help="Chunk size (maps to max-token-limit for backward compatibility)",
    )
    parser.add_argument(
        "--exclude-metadata",
        "-em",
        nargs="+",
        default=None,
        help="Metadata to be excluded during embedding",
    )

    parser.add_argument(
        "--runbooks-dir",
        "-r",
        default="./runbooks",
        help="Directory containing runbooks",
    )

    parser.add_argument("--model-name", "-mn", help="HF repo id of the embedding model")
    parser.add_argument(
        "--hermetic-build", "-hb", action="store_true", help="Hermetic build mode"
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    return parser.parse_args()


def setup_environment(args: argparse.Namespace, product: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Path]]:
    """Setup environment and validate dependencies."""
    logger = setup_logging(verbose=args.verbose)

    validate_dependencies()

    if args.chunk is not None:
        logger.info(
            "Using --chunk value %s for max-token-limit (backward compatibility)",
            args.chunk,
        )
        args.max_token_limit = args.chunk

    logger.info("Using max token limit: %s", args.max_token_limit)

    paths, product = create_directory_structure(
        cache_dir=args.cache_dir,
        output_dir=args.output_dir,
        product=product,
        specific_doc=args.specific_doc,
    )

    product_slug = product.get("slug", "default")
    product_version = product.get("version", "latest")

    if not args.index:
        if args.specific_doc:
            args.index = f"{product_slug}-{product_version}-{args.specific_doc}"
        else:
            args.index = f"{product_slug}-{product_version}"
        logger.info("Auto-generated index name: %s", args.index)

    model_path = Path(args.model_dir).resolve()

    if not model_path.exists():
        logger.error("Model directory does not exist: %s", model_path)
        raise FileNotFoundError(f"Model directory not found: {model_path}")

    logger.info("Using model directory: %s", model_path)

    os.environ["HF_HOME"] = str(model_path)
    os.environ["TRANSFORMERS_OFFLINE"] = "1"

    Settings.llm = resolve_llm(None)

    try:
        Settings.embed_model = HuggingFaceEmbedding(model_name=str(model_path))
    except Exception as e:
        logger.error("Failed to load embedding model from %s: %s", model_path, e)
        logger.info("Try using a Hugging Face model name instead of a local path")
        raise

    return {"logger": logger, "paths": paths}, product


def run_download_step(
    args: argparse.Namespace,
    paths: dict[str, Path],
    product: dict[str, Any],
    logger,
) -> bool:
    """Run the documentation download step."""
    downloads_dir = paths["downloads"]

    if (
        args.use_cached_downloads
        and downloads_dir.exists()
        and any(downloads_dir.iterdir())
    ):
        logger.info("Using cached downloads")
        return True

    try:
        logger.info(
            "Downloading %s %s documentation...",
            product.get("slug"),
            product.get("version"),
        )
        success = download_documentation(
            version=product.get("version"),
            product_slug=product.get("slug"),
            doc_url=product.get("url"),
            specific_doc=args.specific_doc,
            output_dir=downloads_dir,
            cache_existing=(not args.use_cached_downloads),
            fail_on_error=args.fail_on_download_error,
        )
        if success:
            logger.info("Download completed successfully")
            return True
        else:
            logger.error("Download failed")
            return False
    except Exception as e:
        logger.error("Download step failed: %s", e)
        return False


def run_strip_step(args: argparse.Namespace, paths: dict[str, Path], logger) -> bool:
    """Run the HTML stripping step."""
    downloads_dir = paths["downloads"]
    stripped_dir = paths["stripped"]

    try:
        logger.info("Stripping HTML ballast...")
        success = strip_html_content(input_dir=downloads_dir, output_dir=stripped_dir)
        if success:
            logger.info("HTML stripping completed successfully")
            return True
        else:
            logger.error("HTML stripping failed")
            return False
    except Exception as e:
        logger.error("Strip step failed: %s", e)
        return False


def run_chunk_step(
    args: argparse.Namespace,
    paths: dict[str, Path],
    product: dict[str, Any],
    logger,
) -> bool:
    """Run the HTML chunking step."""
    stripped_dir = paths["stripped"]
    chunks_dir = paths["chunks"]

    chunking_options = {
        "max_token_limit": args.max_token_limit,
        "count_tag_tokens": args.count_tag_tokens,
        "keep_siblings_together": args.keep_siblings_together,
        "prepend_parent_section_text": args.prepend_parent_text,
    }

    try:
        logger.info("Chunking HTML documents...")
        success = chunk_html_documents(
            input_dir=stripped_dir,
            output_dir=chunks_dir,
            product_slug=product.get("slug"),
            product_version=product.get("version"),
            doc_url=product.get("url"),
            **chunking_options,
        )
        if success:
            logger.info("HTML chunking completed successfully")
            return True
        else:
            logger.error("HTML chunking failed")
            return False
    except Exception as e:
        logger.error("Chunk step failed: %s", e)
        return False


def run_runbooks_step(args: argparse.Namespace, paths: dict[str, Path], logger) -> bool:
    """Run the runbooks processing step."""
    if args.skip_runbooks:
        logger.info("Skipping runbooks processing")
        return True

    runbooks_dir = Path(args.runbooks_dir)
    if not runbooks_dir.exists():
        logger.warning("Runbooks directory %s does not exist, skipping", runbooks_dir)
        return True

    chunks_dir = paths["chunks"]

    try:
        logger.info("Processing runbooks...")
        success = process_runbooks(
            runbooks_dir=runbooks_dir,
            output_dir=chunks_dir,
            max_token_limit=args.max_token_limit,
        )
        if success:
            logger.info("Runbooks processing completed successfully")
            return True
        else:
            logger.error("Runbooks processing failed")
            return False
    except Exception as e:
        logger.error("Runbooks step failed: %s", e)
        return False


def load_chunks_as_nodes(chunks_dir: Path, logger) -> list[TextNode]:
    """Load all chunks as TextNode objects."""
    nodes = []

    # Use a recursive glob to find chunk files in their document-specific subdirectories.
    chunk_files = list(chunks_dir.glob("**/*.json"))
    # Filter out the summary files that might be at various levels.
    chunk_files = [f for f in chunk_files if not f.name.endswith("_summary.json")]

    logger.info("Found %s chunk files to load from %s", len(chunk_files), chunks_dir)

    for chunk_file in chunk_files:
        try:
            with open(chunk_file, "r", encoding="utf-8") as f:
                chunk_data = json.load(f)

            node = TextNode(
                text=chunk_data["content"],
                metadata=chunk_data.get("metadata", {}),
                id_=chunk_data.get("id", str(chunk_file.stem)),
            )

            nodes.append(node)

        except Exception as e:
            logger.warning("Failed to load chunk %s: %s", chunk_file, e)

    logger.info("Loaded %s chunks as TextNode objects", len(nodes))
    return nodes


def run_embedding_step(
    args: argparse.Namespace,
    paths: dict[str, Path],
    product: dict[str, Any],
    logger,
) -> bool:
    """Run the embedding generation step."""
    base_chunks_dir = paths["chunks"]
    output_dir = Path(args.output_dir)
    nodes = []

    try:
        if args.specific_doc:
            logger.info("Loading chunks for specific document and runbooks.")
            # 1. Load chunks from the specific document's directory.
            doc_chunks_dir = base_chunks_dir / args.specific_doc
            if doc_chunks_dir.exists():
                logger.info("Loading from specific doc directory: %s", doc_chunks_dir)
                nodes.extend(load_chunks_as_nodes(doc_chunks_dir, logger))
            else:
                logger.warning(
                    "Chunk directory for specific doc not found: %s", doc_chunks_dir
                )

            # 2. Load runbook chunks (which are in the base directory).
            if not args.skip_runbooks:
                # Find JSON files directly in base_chunks_dir, not subdirectories.
                runbook_files = [
                    f for f in base_chunks_dir.glob("*.json") if f.is_file()
                ]
                runbook_files = [
                    f for f in runbook_files if not f.name.endswith("_summary.json")
                ]

                logger.info(
                    "Found %s potential runbook chunk files to load from %s",
                    len(runbook_files),
                    base_chunks_dir,
                )

                for chunk_file in runbook_files:
                    try:
                        with open(chunk_file, "r", encoding="utf-8") as f:
                            chunk_data = json.load(f)
                        node = TextNode(
                            text=chunk_data["content"],
                            metadata=chunk_data.get("metadata", {}),
                            id_=chunk_data.get("id", str(chunk_file.stem)),
                        )
                        nodes.append(node)
                    except Exception as e:
                        logger.warning("Failed to load chunk %s: %s", chunk_file, e)
        else:
            # No specific doc, so load everything from the base directory recursively.
            logger.info("Loading all chunks recursively from %s", base_chunks_dir)
            nodes = load_chunks_as_nodes(base_chunks_dir, logger)

        if not nodes:
            logger.error("No chunks found to embed")
            return False

        logger.info("Setting up vector store...")
        embedding_dimension = len(Settings.embed_model.get_text_embedding("test"))
        faiss_index = faiss.IndexFlatIP(embedding_dimension)
        vector_store = FaissVectorStore(faiss_index=faiss_index)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        logger.info("Generating embeddings for %s nodes...", len(nodes))
        index = VectorStoreIndex(nodes, storage_context=storage_context)
        index.set_index_id(args.index)

        logger.info("Persisting vector database...")
        index.storage_context.persist(persist_dir=output_dir)

        metadata = {
            "product_slug": product.get("slug"),
            "version": product.get("version"),
            "specific_doc": args.specific_doc,
            "index_id": args.index,
            "embedding_model": args.model_name or args.model_dir,
            "total_chunks": len(nodes),
            "max_token_limit": args.max_token_limit,
            "embedding_dimension": embedding_dimension,
            "creation_time": time.time(),
        }

        with open(output_dir / "metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        logger.info(
            "Embedding generation completed successfully. %s chunks processed.",
            len(nodes),
        )
        return True

    except Exception as e:
        logger.error("Embedding step failed: %s", e)
        return False


def main() -> int:
    """Main execution function."""
    args = parse_arguments()
    logger = setup_logging(verbose=args.verbose)

    if args.specific_doc and not args.doc_url_slug:
        logger.error("--specific-doc can only be used with --doc-url-slug.")
        return 1

    products_to_process = []

    # Determine source of products
    if args.config_file:
        if args.specific_doc:
            logger.error("--specific-doc cannot be used with --config-file.")
            return 1
        logger.info("Loading products from config file: %s", args.config_file)
        try:
            with open(args.config_file, "r") as f:
                if args.config_file.suffix in [".yaml", ".yml"]:
                    config = yaml.safe_load(f)
                elif args.config_file.suffix == ".json":
                    config = json.load(f)
                else:
                    logger.error(
                        "Unsupported config file format: %s. Use .yaml, .yml, or .json.",
                        args.config_file.suffix,
                    )
                    return 1
            products_to_process = config.get("products", [])
        except Exception as e:
            logger.error(
                "Failed to load or parse config file %s: %s", args.config_file, e
            )
            return 1

    elif args.doc_url:
        if args.specific_doc:
            logger.error("--specific-doc cannot be used with --doc-url.")
            return 1
        logger.info("Processing single product from URL: %s", args.doc_url)
        products_to_process.append({"url": args.doc_url})

    elif args.doc_url_slug:
        logger.info(
            "Processing single product from slug: %s, version: %s",
            args.doc_url_slug,
            args.doc_url_version,
        )
        slug = args.doc_url_slug
        if slug.startswith("http"):
            logger.warning(
                "Warning: --doc-url-slug was provided a full URL. Attempting to parse slug from it."
            )
            path_parts = urlparse(slug).path.strip("/").split("/")
            slug = path_parts[-1] if path_parts and path_parts[-1] else (path_parts[-2] if len(path_parts) > 1 else "unknown")
            logger.info("Parsed slug as: %s", slug)

        products_to_process.append({"slug": slug, "version": args.doc_url_version})

    if not products_to_process:
        logger.error("No products to process. Please check your input source.")
        return 1

    # Pre-process the list to parse URLs and fill in missing data
    for product in products_to_process:
        if "url" in product and "slug" not in product:
            parsed_url = urlparse(product["url"])
            path_parts = parsed_url.path.strip("/").split("/")
            slug = "unknown"
            version = "unknown"
            try:
                doc_index = path_parts.index("documentation")
                # Path format: /documentation/{lang}/{slug}/{version}/...
                if re.match(r"^[a-z]{2}(-[a-z]{2})?$", path_parts[doc_index + 1]):
                    slug = path_parts[doc_index + 2]
                    version = path_parts[doc_index + 3]
                else: # Path format: /documentation/{slug}/{version}/...
                    slug = path_parts[doc_index + 1]
                    version = path_parts[doc_index + 2]
            except (ValueError, IndexError):
                logger.warning(
                    "URL %s does not match standard Red Hat documentation format. Using fallback for slug and version.", product["url"]
                )
                slug = (
                    parsed_url.hostname.replace(".", "_")
                    if parsed_url.hostname
                    else "localdoc"
                )
                version = "latest"
            product["slug"] = slug
            product["version"] = version


    for product in products_to_process:
        try:
            # Set up environment for each product
            env, product = setup_environment(args, product)
            paths = env["paths"]

            logger.info(
                "Starting HTML embeddings pipeline for %s version %s",
                product.get("slug"),
                product.get("version"),
            )
            if args.specific_doc:
                logger.info("Processing specific document: %s", args.specific_doc)

            steps = [
                ("download", run_download_step),
                ("strip", run_strip_step),
                ("chunk", run_chunk_step),
                ("runbooks", run_runbooks_step),
                ("embed", run_embedding_step),
            ]

            for step_name, step_func in steps:
                logger.info(
                    "Running %s step for %s...", step_name, product.get("slug")
                )

                # Pass product info to steps that need it
                if step_name in ["download", "chunk", "embed"]:
                    success = step_func(args, paths, product, logger)
                else:
                    success = step_func(args, paths, logger)

                if not success:
                    if args.continue_on_error:
                        logger.warning(
                            "Step %s failed for %s, but continuing due to --continue-on-error",
                            step_name,
                            product.get("slug"),
                        )
                    else:
                        logger.error(
                            "Step %s failed for %s, stopping pipeline",
                            step_name,
                            product.get("slug"),
                        )
                        return 1

            logger.info(
                "HTML embeddings pipeline completed successfully for %s!",
                product.get("slug"),
            )

        except Exception as e:
            logger.error(
                "Pipeline failed for product %s with error: %s", product.get("slug"), e
            )
            if not args.continue_on_error:
                return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
