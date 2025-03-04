#!/usr/bin/env python3
"""Utility script to generate embeddings."""

import argparse
import json
import os
import time
from typing import Callable, Dict, List

import faiss
import requests
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.llms.utils import resolve_llm

from llama_index.core.schema import TextNode, Document
from llama_index.core.storage.storage_context import StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.readers.file.flat.base import FlatReader
from llama_index.vector_stores.faiss import FaissVectorStore

# from langchain.text_splitter import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from layered_algorithm import chunk_markdown

OCP_DOCS_ROOT_URL = "https://docs.openshift.com/container-platform/"
OCP_DOCS_VERSION = "4.15"
UNREACHABLE_DOCS: int = 0
RUNBOOKS_ROOT_URL = "https://github.com/openshift/runbooks/blob/master/alerts"
HERMETIC_BUILD = False


def ping_url(url: str) -> bool:
    """Check if the URL parameter is live."""
    try:
        response = requests.get(url, timeout=30)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def get_file_title(file_path: str) -> str:
    """Extract title from the plaintext doc file."""
    title = ""
    try:
        with open(file_path, "r") as file:
            title = file.readline().rstrip("\n").lstrip("# ")
    except Exception:  # noqa: S110
        pass
    return title


def file_metadata_func(file_path: str, docs_url_func: Callable[[str], str]) -> Dict:
    """Populate the docs_url and title metadata elements with docs URL and the page's title.

    Args:
        file_path: str: file path in str
        docs_url_func: Callable[[str], str]: lambda for the docs_url
    """
    docs_url = docs_url_func(file_path)
    title = get_file_title(file_path)
    msg = f"file_path: {file_path}, title: {title}, docs_url: {docs_url}"
    if not HERMETIC_BUILD:
        if not ping_url(docs_url):
            global UNREACHABLE_DOCS
            UNREACHABLE_DOCS += 1
            msg += ", UNREACHABLE"
    print(msg)
    return {"docs_url": docs_url, "title": title}


def ocp_file_metadata_func(file_path: str) -> Dict:
    """Populate metadata for an OCP docs page.

    Args:
        file_path: str: file path in str
    """
    docs_url = lambda file_path: (  # noqa: E731
        OCP_DOCS_ROOT_URL
        + OCP_DOCS_VERSION
        + file_path.removeprefix(EMBEDDINGS_ROOT_DIR).removesuffix("txt")
        + "html"
    )
    return file_metadata_func(file_path, docs_url)


def runbook_file_metadata_func(file_path: str) -> Dict:
    """Populate metadata for a runbook page.

    Args:
        file_path: str: file path in str
    """
    docs_url = lambda file_path: (  # noqa: E731
        RUNBOOKS_ROOT_URL + file_path.removeprefix(RUNBOOKS_ROOT_DIR)
    )
    return file_metadata_func(file_path, docs_url)


def got_whitespace(text: str) -> bool:
    """Indicate if the parameter string contains whitespace."""
    for c in text:
        if c.isspace():
            return True
    return False


def create_nodes_from_chunks(doc: Document, chunks: List[str]) -> List[TextNode]:
    """Create TextNode objects from chunks with the document's metadata.

    Args:
        doc: The source document
        chunks: List of text chunks

    Returns:
        List of TextNode objects
    """
    nodes = []

    for chunk in chunks:
        if not chunk.strip():
            continue

        node = TextNode(
            text=chunk,
            metadata=doc.metadata.copy()
        )
        nodes.append(node)

    return nodes


def create_nodes_with_layered_chunking(documents: List[Document], token_limit: int,
                                   keep_siblings_together: bool, prepend_parent_section_text: bool) -> List[TextNode]:
    """Create nodes from documents using the layered chunking algorithm.

    Args:
        documents: List of Document objects
        token_limit: Maximum tokens per chunk
        keep_siblings_together: Whether to keep sibling headings together
        prepend_parent_section_text: Whether to prepend parent section text

    Returns:
        List of TextNode objects
    """
    all_nodes = []

    for doc in documents:
        # Chunk the document text
        chunks = chunk_markdown(
            doc.text,
            token_limit=token_limit,
            keep_siblings_together=keep_siblings_together,
            prepend_parent_section_text=prepend_parent_section_text
        )

        # Create TextNode objects from chunks
        doc_nodes = create_nodes_from_chunks(doc, chunks)
        all_nodes.extend(doc_nodes)

    return all_nodes


if __name__ == "__main__":

    start_time = time.time()

    parser = argparse.ArgumentParser(description="embedding cli for task execution")
    parser.add_argument("-f", "--folder", help="Plain text folder path")
    parser.add_argument("-r", "--runbooks", help="Runbooks folder path")
    parser.add_argument(
        "-md",
        "--model-dir",
        default="embeddings_model",
        help="Directory containing the embedding model",
    )
    parser.add_argument(
        "-mn",
        "--model-name",
        help="HF repo id of the embedding model",
    )
    parser.add_argument(
        "-c", "--chunk", type=int, default=380, help="Chunk size for embedding"
    )
    parser.add_argument(
        "-l", "--overlap", type=int, default=0, help="Chunk overlap for embedding"
    )
    parser.add_argument(
        "-k", "--keep-siblings", type=bool, default=True,
        help="Whether to keep sibling headings together"
    )
    parser.add_argument(
        "-p", "--prepend-parent", type=bool, default=True,
        help="Whether to prepend parent section text"
    )
    parser.add_argument(
        "-em",
        "--exclude-metadata",
        nargs="+",
        default=None,
        help="Metadata to be excluded during embedding",
    )
    parser.add_argument("-o", "--output", help="Vector DB output folder")
    parser.add_argument("-i", "--index", help="Product index")
    parser.add_argument("-v", "--ocp-version", help="OCP version")
    parser.add_argument("-hb", "--hermetic-build", type=bool, default=False, help="Hermetic build")
    args = parser.parse_args()
    print(f"Arguments used: {args}")

    # OLS-823: sanitize directory
    PERSIST_FOLDER = os.path.normpath("/" + args.output).lstrip("/")
    if PERSIST_FOLDER == "":
        PERSIST_FOLDER = "."

    EMBEDDINGS_ROOT_DIR = os.path.abspath(args.folder)
    if EMBEDDINGS_ROOT_DIR.endswith("/"):
        EMBEDDINGS_ROOT_DIR = EMBEDDINGS_ROOT_DIR[:-1]
    RUNBOOKS_ROOT_DIR = os.path.abspath(args.runbooks)
    if RUNBOOKS_ROOT_DIR.endswith("/"):
        RUNBOOKS_ROOT_DIR = RUNBOOKS_ROOT_DIR[:-1]

    OCP_DOCS_VERSION = args.ocp_version
    HERMETIC_BUILD = args.hermetic_build

    os.environ["HF_HOME"] = args.model_dir
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    Settings.chunk_size = args.chunk
    Settings.chunk_overlap = args.overlap
    Settings.embed_model = HuggingFaceEmbedding(model_name=args.model_dir)
    Settings.llm = resolve_llm(None)

    embedding_dimension = len(Settings.embed_model.get_text_embedding("random text"))
    faiss_index = faiss.IndexFlatIP(embedding_dimension)
    vector_store = FaissVectorStore(faiss_index=faiss_index)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Load documents
    documents = SimpleDirectoryReader(
        args.folder, recursive=True, file_metadata=ocp_file_metadata_func
    ).load_data()

    # Create chunks/nodes using the layered algorithm
    nodes = create_nodes_with_layered_chunking(
        documents,
        args.chunk,
        args.keep_siblings,
        args.prepend_parent
    )

    # Filter out invalid nodes
    good_nodes = []
    for node in nodes:
        if isinstance(node, TextNode) and got_whitespace(node.text):
            # Exclude given metadata during embedding
            if args.exclude_metadata is not None:
                node.excluded_embed_metadata_keys.extend(args.exclude_metadata)
            good_nodes.append(node)
        else:
            print("skipping node without whitespace: " + node.__repr__())

    runbook_documents = SimpleDirectoryReader(
        args.runbooks,
        recursive=True,
        required_exts=[".md"],
        file_extractor={".md": FlatReader()},
        file_metadata=runbook_file_metadata_func,
    ).load_data()

    # Create runbook nodes using the layered algorithm
    runbook_nodes = create_nodes_with_layered_chunking(
        runbook_documents,
        args.chunk,
        args.keep_siblings,
        args.prepend_parent
    )

    # Filter out invalid runbook nodes
    good_runbook_nodes = []
    for node in runbook_nodes:
        if isinstance(node, TextNode) and got_whitespace(node.text):
            # Exclude given metadata during embedding
            if args.exclude_metadata is not None:
                node.excluded_embed_metadata_keys.extend(args.exclude_metadata)
            good_runbook_nodes.append(node)
        else:
            print("skipping node without whitespace: " + node.__repr__())

    good_nodes.extend(good_runbook_nodes)

    # Create & save Index
    index = VectorStoreIndex(
        good_nodes,
        storage_context=storage_context,
    )
    index.set_index_id(args.index)
    index.storage_context.persist(persist_dir=PERSIST_FOLDER)

    metadata: dict = {}
    metadata["execution-time"] = time.time() - start_time
    metadata["llm"] = "None"
    metadata["embedding-model"] = args.model_name
    metadata["index-id"] = args.index
    metadata["vector-db"] = "faiss.IndexFlatIP"
    metadata["embedding-dimension"] = embedding_dimension
    metadata["chunk"] = args.chunk
    metadata["overlap"] = args.overlap
    metadata["total-embedded-files"] = len(documents)
    metadata["chunking-algorithm"] = "markdown-aware-chunker"
    metadata["keep-siblings-together"] = args.keep_siblings
    metadata["prepend-parent-section-text"] = args.prepend_parent

    with open(os.path.join(PERSIST_FOLDER, "metadata.json"), "w") as file:
        file.write(json.dumps(metadata))

    if UNREACHABLE_DOCS > 0:
        print(
            "WARNING:\n"
            f"There were documents with {UNREACHABLE_DOCS} unreachable URLs, "
            "grep the log for UNREACHABLE.\n"
            "Please update the plain text."
        )
