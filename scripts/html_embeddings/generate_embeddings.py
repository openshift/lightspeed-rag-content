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
from typing import Optional, Dict, Any, List

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
        description="Generate embeddings from OpenShift HTML documentation",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--version", "-v", required=True, help="OpenShift version (e.g., 4.18)"
    )
    parser.add_argument(
        "--specific-doc",
        "-d",
        help="Optional specific document to download (e.g., 'monitoring')",
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


def setup_environment(args: argparse.Namespace) -> Dict[str, Any]:
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
    
    if not args.index:
        if args.specific_doc:
            args.index = f"ocp-{args.version}-{args.specific_doc}"
        else:
            args.index = f"ocp-{args.version}"
        logger.info("Auto-generated index name: %s", args.index)

    paths = create_directory_structure(
        cache_dir=args.cache_dir,
        output_dir=args.output_dir,
        version=args.version,
        specific_doc=args.specific_doc,
    )

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

    return {"logger": logger, "paths": paths}


def run_download_step(args: argparse.Namespace, paths: Dict[str, Path], logger) -> bool:
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
        logger.info("Downloading OpenShift %s documentation...", args.version)
        success = download_documentation(
            version=args.version,
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


def run_strip_step(args: argparse.Namespace, paths: Dict[str, Path], logger) -> bool:
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


def run_chunk_step(args: argparse.Namespace, paths: Dict[str, Path], logger) -> bool:
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
            input_dir=stripped_dir, output_dir=chunks_dir, **chunking_options
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


def run_runbooks_step(args: argparse.Namespace, paths: Dict[str, Path], logger) -> bool:
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


def load_chunks_as_nodes(chunks_dir: Path, logger) -> List[TextNode]:
    """Load all chunks as TextNode objects."""
    nodes = []

    chunk_files = list(chunks_dir.glob("*.json"))
    chunk_files = [f for f in chunk_files if not f.name.endswith("_summary.json")]

    logger.info("Found %s chunk files to load", len(chunk_files))

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
    args: argparse.Namespace, paths: Dict[str, Path], logger
) -> bool:
    """Run the embedding generation step."""
    chunks_dir = paths["chunks"]
    output_dir = Path(args.output_dir)

    try:
        logger.info("Loading chunks...")
        nodes = load_chunks_as_nodes(chunks_dir, logger)

        if not nodes:
            logger.error("No chunks found to embed")
            return False

        logger.info("Setting up vector store...")
        embedding_dimension = len(Settings.embed_model.get_text_embedding("test"))
        faiss_index = faiss.IndexFlatIP(embedding_dimension)
        vector_store = FaissVectorStore(faiss_index=faiss_index)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        logger.info("Generating embeddings...")
        index = VectorStoreIndex(nodes, storage_context=storage_context)
        index.set_index_id(args.index)

        logger.info("Persisting vector database...")
        index.storage_context.persist(persist_dir=output_dir)

        metadata = {
            "version": args.version,
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

    try:
        env = setup_environment(args)
        logger = env["logger"]
        paths = env["paths"]

        logger.info(
            "Starting HTML embeddings pipeline for OpenShift %s", args.version
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
            logger.info("Running %s step...", step_name)

            success = step_func(args, paths, logger)

            if not success:
                if args.continue_on_error:
                    logger.warning(
                        "Step %s failed, but continuing due to --continue-on-error",
                        step_name,
                    )
                else:
                    logger.error("Step %s failed, stopping pipeline", step_name)
                    return 1

        logger.info("HTML embeddings pipeline completed successfully!")
        return 0

    except Exception as e:
        print(f"Pipeline failed with error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
