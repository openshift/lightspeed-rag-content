import os
import argparse

from llama_index.core.llms.utils import resolve_llm
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.core import Settings, StorageContext, load_index_from_storage, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Utility script for iterating over a RAG database"
    )
    parser.add_argument(
        "-p",
        "--db-path",
        required=True,
        help="path to the vector db",
    )
    parser.add_argument(
        "-m", "--model-path", required=True, help="path to the embedding model"
    )
    args = parser.parse_args()

    os.environ["TRANSFORMERS_CACHE"] = args.model_path
    os.environ["TRANSFORMERS_OFFLINE"] = "1"

    Settings.llm = resolve_llm(None)
    Settings.embed_model = HuggingFaceEmbedding(model_name=args.model_path)

    vector_store = FaissVectorStore.from_persist_dir(args.db_path)
    storage_context = StorageContext.from_defaults(
       vector_store=vector_store, persist_dir=args.db_path,
    )
    index = load_index_from_storage(storage_context)

    # Iterate over all nodes in the docstore
    for node in index.docstore.docs.values():
        print("Node ID:", node.node_id)
        print("Content:", node.get_content())
        # Metadata, if you stored it:
        print("Metadata:", node.metadata)
