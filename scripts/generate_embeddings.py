"""Utility script to generate embeddings."""

import argparse
import json
import os
import re
import time
from typing import Callable, Dict, List, Union

import faiss
import requests
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.llms.utils import resolve_llm

# from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.core.schema import TextNode, Document
from llama_index.core.storage.storage_context import StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.readers.file.flat.base import FlatReader
from llama_index.vector_stores.faiss import FaissVectorStore

from langchain.text_splitter import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

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
    return any(c.isspace() for c in str(text))


def get_chunk_text(chunk: Union[str, Document]) -> str:
    """Return the text content of the input chunk; extract from page_content if input is a Document."""
    if isinstance(chunk, str):
        return chunk
    return getattr(chunk, "page_content", getattr(chunk, "text", str(chunk)))


def token_count(text: Union[str, Document]) -> int:
    """Approximate token count by splitting on whitespace."""
    return len(get_chunk_text(text).split())


def split_by_headers(text: str) -> List[str]:
    """
    Split text into sections based on markdown headers.
    A header is defined as a line starting with one or more '#' followed by a space.
    (Each section includes its header.)
    """
    pattern = re.compile(r'^(#+\s.*)$', re.MULTILINE)
    headers = list(pattern.finditer(text))
    if not headers:
        return [text]
    sections = []
    for i, header in enumerate(headers):
        start = header.start()
        end = headers[i+1].start() if i+1 < len(headers) else len(text)
        sections.append(text[start:end].strip())
    return sections


def split_by_paragraphs(text: str, token_limit: int) -> List[str]:
    """
    Split text into chunks by grouping whole paragraphs (delimited by "\n\n")
    so that each chunk does not exceed token_limit.
    """
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = ""
    for para in paragraphs:
        candidate = current_chunk + "\n\n" + para if current_chunk else para
        if token_count(candidate) <= token_limit:
            current_chunk = candidate
        else:
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = para
            else:
                # If a single paragraph exceeds token_limit, return it as its own chunk.
                chunks.append(para)
                current_chunk = ""
    if current_chunk:
        chunks.append(current_chunk)
    return chunks


def is_procedure_block(text: str) -> bool:
    """
    Return whether a block of text is a procedure (based on lines starting with number and a dot).
    """
    lines = text.splitlines()
    step_count = sum(1 for line in lines if re.match(r"^\s*\d+\.\s+", line))
    return step_count >= 2


def split_procedure_block(text: str, token_limit: int) -> List[str]:
    """
    Split procedure that are too long into chunks, without breaking individual steps.
    """
    lines = text.splitlines()
    steps = []
    current_step = []
    for line in lines:
        if re.match(r"^\s*\d+\.\s+", line) and current_step:
            steps.append("\n".join(current_step))
            current_step = [line]
        else:
            current_step.append(line)
    if current_step:
        steps.append("\n".join(current_step))

    chunks = []
    current_chunk = ""
    for step in steps:
        candidate = current_chunk + "\n\n" + step if current_chunk else step
        if token_count(candidate) <= token_limit:
            current_chunk = candidate
        else:
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = step
            else:
                # If a single step exceeds token_limit, return it as a chunk.
                chunks.append(step)
                current_chunk = ""
    if current_chunk:
        chunks.append(current_chunk)
    return chunks


def layered_split_text(text: str, token_limit: int) -> List[str]:
    """
    Layered splitting:
      1. If text is within token_limit, return [text].
      2. Otherwise, split text into sections using markdown headers.
      3. For each section:
           - If its token count is within token_limit, keep it as one chunk.
           - Else if it appears to be a procedure block, split it using split_procedure_block.
           - Otherwise, split it by grouping paragraphs using split_by_paragraphs.
    """
    text = str(text)
    if token_count(text) <= token_limit:
        return [text]

    sections = split_by_headers(text)
    final_chunks = []
    for section in sections:
        if token_count(section) <= token_limit:
            final_chunks.append(section)
        else:
            if is_procedure_block(section):
                proc_chunks = split_procedure_block(section, token_limit)
                final_chunks.extend(proc_chunks)
            else:
                para_chunks = split_by_paragraphs(section, token_limit)
                final_chunks.extend(para_chunks)
    return final_chunks


def split_documents(documents, token_limit: int) -> List[TextNode]:
    """
    Split all documents using layered splitting.
    """
    nodes = []
    for doc in documents:
        chunks = layered_split_text(doc.text, token_limit)
        for chunk in chunks:
            node = TextNode(text=chunk, metadata=doc.metadata)
            nodes.append(node)
    return nodes


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
        "-em",
        "--exclude-metadata",
        nargs="+",
        default=None,
        help="Metadata to be excluded during embedding",
    )
    parser.add_argument("-o", "--output", help="Vector DB output folder")
    parser.add_argument("-i", "--index", help="Product index")
    parser.add_argument("-v", "--ocp-version", help="OCP version")
    parser.add_argument(
        "-hb", "--hermetic-build", type=bool, default=False, help="Hermetic build"
    )
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

    # Split based on header/section
    # md_parser = MarkdownNodeParser()
    # documents = md_parser.get_nodes_from_documents(documents)

    # Create chunks/nodes using the layered splitter.
    nodes = split_documents(documents, Settings.chunk)

    # Filter out invalid nodes
    good_nodes = []
    for node in nodes:
        if isinstance(node, TextNode) and got_whitespace(node.text):
            # Exclude given metadata during embedding
            # if args.exclude_metadata is not None:
            #     node.excluded_embed_metadata_keys.extend(args.exclude_metadata)
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
    runbook_nodes = split_documents(runbook_documents, Settings.chunk)

    good_nodes.extend(runbook_nodes)

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

    with open(os.path.join(PERSIST_FOLDER, "metadata.json"), "w") as file:
        file.write(json.dumps(metadata))

    if UNREACHABLE_DOCS > 0:
        print(
            "WARNING:\n"
            f"There were documents with {UNREACHABLE_DOCS} unreachable URLs, "
            "grep the log for UNREACHABLE.\n"
            "Please update the plain text."
        )
