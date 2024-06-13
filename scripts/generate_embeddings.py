"""Utility script to generate embeddings."""

import argparse
import json
import os
import time
from typing import Dict
import faiss
import requests
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.llms.utils import resolve_llm

# from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.core.schema import TextNode
from llama_index.core.storage.storage_context import StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.faiss import FaissVectorStore

OCP_DOCS_ROOT_URL = "https://docs.openshift.com/container-platform/"
OCP_DOCS_VERSION = " "
UNREACHABLE_DOCS: bool = False


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


def file_metadata_func(file_path: str) -> Dict:
    """Populate the docs_url metadata element with the corresponding OCP docs URL.

    Args:
        file_path: str: file path in str
    """
    docs_url = (
        OCP_DOCS_ROOT_URL
        + OCP_DOCS_VERSION
        + file_path.removeprefix(EMBEDDINGS_ROOT_DIR).removesuffix("txt")
        + "html"
    )
    title = get_file_title(file_path)
    msg = f"file_path: {file_path}, title: {title}, docs_url: {docs_url}"
    if not ping_url(docs_url):
        print("--> unreachable: {docs_url} ")
        global UNREACHABLE_DOCS
        UNREACHABLE_DOCS = True
        msg += ", UNREACHABLE"
    print(msg)
    return {"docs_url": docs_url, "title": title}


def got_whitespace(text: str) -> bool:
    """Indicate if the parameter string contains whitespace."""
    for c in text:
        if c.isspace():
            return True
    return False


def gen_metadata_file(start_time, args, embedding_dimension, folder, folder_index, PERSIST_FOLDER, documents):
    metadata = {}
    metadata["execution-time"] = time.time() - start_time
    metadata["llm"] = "None"
    metadata["folder"] = folder
    metadata["embedding-model"] = args.model_name
    metadata["index-id"] = folder_index
    metadata["vector-db"] = "faiss"
    metadata["embedding-dimension"] = embedding_dimension
    metadata["chunk"] = args.chunk
    metadata["overlap"] = args.overlap
    metadata["total-embedded-files"] = len(documents)

    with open(os.path.join(PERSIST_FOLDER, f"metadata_{folder_index}.json"), "w") as file:
        file.write(json.dumps(metadata))

if __name__ == "__main__":

    start_time = time.time()

    parser = argparse.ArgumentParser(description="embedding cli for task execution")
    parser.add_argument("-f", "--folder", help="Plain text folder path")
    parser.add_argument("-fo", "--folders", help="Multiple plain text folders paths separated by space]")
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
    args = parser.parse_args()
    print(f"Arguments used: {args}")

    os.environ["HF_HOME"] = args.model_dir
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    Settings.chunk_size = args.chunk
    Settings.chunk_overlap = args.overlap
    Settings.embed_model = HuggingFaceEmbedding(model_name=args.model_dir)

    embedding_dimension = len(Settings.embed_model.get_text_embedding("random text"))
    faiss_index = faiss.IndexFlatIP(embedding_dimension)
    vector_store = FaissVectorStore(faiss_index=faiss_index)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    folder_list = []
    if args.folder:
        folder_list.append(args.folder)
    if args.folders: 
        folder_list = folder_list + args.folders.split()
    print(f" --> List of folders: {folder_list}")

    for folder in folder_list: 
        if not os.path.exists(folder):
            print(f" --> Couldn't fine path for folder: {folder}")
        else:     
            folder_index = folder.split("/")[-1]

            PERSIST_FOLDER = args.output
            EMBEDDINGS_ROOT_DIR = os.path.abspath(folder)
            if EMBEDDINGS_ROOT_DIR.endswith("/"):
                EMBEDDINGS_ROOT_DIR = EMBEDDINGS_ROOT_DIR[:-1]

            OCP_DOCS_VERSION = folder.split("/")[-1]
            output_folder = os.path.join(PERSIST_FOLDER,folder_index)

            os.makedirs(output_folder)
            print(f" --> Starting embedding for: {folder}")
            documents = SimpleDirectoryReader(folder, recursive=True, file_metadata=file_metadata_func).load_data()

            if UNREACHABLE_DOCS:
                raise Exception(
                    "There were documents with unreachable URLs, grep the log for UNREACHABLE.\n"
                    "Please update the plain text."
                )

            good_nodes = []
            nodes = Settings.text_splitter.get_nodes_from_documents(documents)
            for node in nodes:
                if isinstance(node, TextNode) and got_whitespace(node.text):
                    good_nodes.append(node)
                else:
                    print("skipping node without whitespace: " + node.__repr__())

            index = VectorStoreIndex(
                good_nodes,
                storage_context=storage_context,
            )
            
            print(f" --> Setting index {folder_index}")  
            index.set_index_id(folder_index.replace(".","_"))
            index.storage_context.persist(persist_dir= output_folder)

            print(f" --> List of folders: {folder_list}")
            gen_metadata_file(start_time, args, embedding_dimension, folder, folder_index, PERSIST_FOLDER, documents)

    print(f" --> Completed embedding generation")


