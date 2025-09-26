"""Utility script for querying RAG database."""

import argparse
import importlib
import json
import logging
import os
import sys
import tempfile
from typing import Any

import yaml
from llama_index.core import Settings, load_index_from_storage
from llama_index.core.llms.utils import resolve_llm
from llama_index.core.storage.storage_context import StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.faiss import FaissVectorStore


def _llama_index_query(args: argparse.Namespace) -> None:
    os.environ["TRANSFORMERS_CACHE"] = args.model_path
    os.environ["TRANSFORMERS_OFFLINE"] = "1"

    Settings.llm = resolve_llm(None)
    Settings.embed_model = HuggingFaceEmbedding(model_name=args.model_path)

    storage_context = StorageContext.from_defaults(
        vector_store=FaissVectorStore.from_persist_dir(args.db_path),
        persist_dir=args.db_path,
    )
    vector_index = load_index_from_storage(
        storage_context=storage_context,
        index_id=args.product_index,
    )

    if args.node is not None:
        node = storage_context.docstore.get_node(args.node)
        result = {
            "query": args.query,
            "type": "single_node",
            "node_id": args.node,
            "node": {
                "id": node.node_id,
                "text": node.text,
                "metadata": node.metadata if hasattr(node, "metadata") else {},
            },
        }
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(node)
    else:
        retriever = vector_index.as_retriever(similarity_top_k=args.top_k)
        nodes = retriever.retrieve(args.query)

        if len(nodes) == 0:
            logging.warning(f"No nodes retrieved for query: {args.query}")
            if args.json:
                result = {
                    "query": args.query,
                    "top_k": args.top_k,
                    "threshold": args.threshold,
                    "nodes": [],
                }
                print(json.dumps(result, indent=2))
            exit(1)

        if args.threshold > 0.0 and nodes[0].score < args.threshold:
            logging.warning(
                f"Score {nodes[0].score} of the top retrieved node for query '{args.query}' "
                f"didn't cross the minimal threshold {args.threshold}."
            )
            if args.json:
                result = {
                    "query": args.query,
                    "top_k": args.top_k,
                    "threshold": args.threshold,
                    "nodes": [],
                }
                print(json.dumps(result, indent=2))
            exit(1)

        # Format results
        result = {
            "query": args.query,
            "top_k": args.top_k,
            "threshold": args.threshold,
            "nodes": [],
        }
        for node in nodes:  # type: ignore
            node_data = {
                "id": node.node_id,
                "score": node.score,
                "text": node.text,
                "metadata": node.metadata if hasattr(node, "metadata") else {},
            }
            result["nodes"].append(node_data)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            for n in nodes:
                print("=" * 80)
                print(n)


def _get_db_path_dict(vector_type: str, config: dict[str, Any]) -> dict[str, Any]:
    """Return the dict where db_path key is from our llama-stack config."""
    try:
        res: dict[str, Any] = config["providers"]["vector_io"][0]["config"]
        if vector_type == "llamastack-faiss":
            res = res["kvstore"]
        return res
    except (KeyError, IndexError) as e:
        raise ValueError(f"Invalid configuration structure: {e}")


def _llama_stack_query(args: argparse.Namespace) -> None:
    tmp_dir = tempfile.TemporaryDirectory(prefix="ls-rag-")
    os.environ["LLAMA_STACK_CONFIG_DIR"] = tmp_dir.name

    cfg = yaml.safe_load(
        open(os.path.join(args.db_path, "llama-stack.yaml"), "r", encoding="utf-8")
    )

    db_dict = _get_db_path_dict(args.vector_store_type, cfg)
    db_filename = os.path.basename(db_dict["db_path"])
    db_dict["db_path"] = os.path.realpath(os.path.join(args.db_path, db_filename))

    if args.model_path:
        cfg["models"][0]["provider_model_id"] = os.path.realpath(args.model_path)

    cfg_file = os.path.join(tmp_dir.name, "llama-stack.yaml")
    yaml.safe_dump(cfg, open(cfg_file, "w", encoding="utf-8"))

    stack_lib = importlib.import_module("llama_stack")
    try:
        client = stack_lib.distribution.library_client.LlamaStackAsLibraryClient(cfg_file)
        client.initialize()

        # No need to register the DB as it's defined in llama-stack.yaml
        # model_id = cfg["models"][0]["model_id"]
        # client.vector_dbs.register(
        #     vector_db_id=args.product_index, embedding_model=model_id
        # )

        query_cfg = {
            "chunk_size_in_tokens": 380,  # Not configurable on this script
            "mode": "vector",  # "vector", "keyword", or "hybrid". Default "vector"
            "max_chunks": args.top_k,
            "chunk_overlap_in_tokens": 0,  # Not configurable on this script
            # "chunk_template": "Result {index}\\nContent: {chunk.content}\\n"
            #                   "Metadata: {metadata}\\n"
            #      Available placeholders:
            #        {index}: 1-based chunk ordinal
            #        {chunk.content}: chunk content string
            #        {metadata}: chunk metadata dict
            # "max_tokens_in_context": Maximum number of tokens in the context.
            # "ranker": Ranker to use in hybrid search. Defaults to RRF ranker.
        }
        res = client.tool_runtime.rag_tool.query(
            vector_db_ids=[args.product_index], content=args.query, query_config=query_cfg
        )

        md = res.metadata
        if len(md["chunks"]) == 0:
            logging.warning(f"No chunks retrieved for query: {args.query}")
            if args.json:
                result = {
                    "query": args.query,
                    "top_k": args.top_k,
                    "threshold": args.threshold,
                    "nodes": [],
                }
                print(json.dumps(result, indent=2))
            exit(1)

        threshold = args.threshold
        if threshold > 0.0 and md.get("scores") and md["scores"][0].score < threshold:
            logging.warning(
                f"Score {md['scores'][0].score} of the top retrieved node for query '{args.query}' "
                f"didn't cross the minimal threshold {threshold}."
            )
            if args.json:
                result = {
                    "query": args.query,
                    "top_k": args.top_k,
                    "threshold": args.threshold,
                    "nodes": [],
                }
                print(json.dumps(result, indent=2))
            exit(1)

        # Format results
        result = {
            "query": args.query,
            "top_k": args.top_k,
            "threshold": args.threshold,
            "nodes": [],
        }

        for _id, chunk, score in zip(md["document_ids"], md["chunks"], md["scores"]):
            node_data = {
                "id": _id,
                "score": score.score if hasattr(score, "score") else score,
                "text": chunk,
                "metadata": {},
            }
            result["nodes"].append(node_data)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            for _id, chunk, score in zip(md["document_ids"], md["chunks"], md["scores"]):
                print("=" * 80)
                print(f"Node ID: {_id}\nScore: {score}\nText:\n{chunk}")

        # Method 2 to present data:
        # for content in res.content:
        #     if content.type == 'text':
        #         print(content.text)
        #     else:
        #         print(content)
    finally:
        client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Utility script for querying RAG database"
    )
    parser.add_argument(
        "-p",
        "--db-path",
        required=True,
        help="path to the vector db",
    )
    parser.add_argument("-x", "--product-index", required=True, help="product index")
    parser.add_argument(
        "-m", "--model-path", required=True, help="path to the embedding model"
    )
    parser.add_argument("-q", "--query", type=str, required=True, help="query to run")
    parser.add_argument("-k", "--top-k", type=int, default=1, help="similarity_top_k")
    parser.add_argument("-n", "--node", help="retrieve node")
    parser.add_argument(
        "-t",
        "--threshold",
        type=float,
        default=0.0,
        help="Minimal score for top node retrieved",
    )
    parser.add_argument(
        "--vector-store-type",
        default="auto",
        choices=["auto", "faiss", "llamastack-faiss", "llamastack-sqlite-vec"],
        help="vector store type to be used.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format",
    )

    args = parser.parse_args()

    if args.json:
        # In JSON mode, only show ERROR or higher to avoid polluting JSON output
        logging.basicConfig(
            level=logging.ERROR,
            format="%(levelname)s: %(message)s",
            stream=sys.stderr,  # Send logs to stderr to keep stdout clean for JSON
        )
    else:
        # In normal mode, show info and above
        logging.basicConfig(level=logging.INFO, format="%(message)s")

    if not args.json:
        logging.info("Command line used: " + " ".join(sys.argv))

    vector_store_type = args.vector_store_type
    if args.vector_store_type == "auto":
        if os.path.exists(os.path.join(args.db_path, "metadata.json")):
            args.vector_store_type = "faiss"
        elif os.path.exists(os.path.join(args.db_path, "sqlite-vec_store.db")):
            args.vector_store_type = "llamastack-sqlite-vec"
        elif os.path.exists(os.path.join(args.db_path, "faiss_store.db")):
            args.vector_store_type = "llamastack-faiss"
        else:
            logging.error(f"Cannot recognize the DB in {args.db_path}")
            exit(1)

    if args.vector_store_type == "faiss":
        _llama_index_query(args)
    else:
        _llama_stack_query(args)

    import asyncio
    for t in asyncio.all_tasks():
        if t is not asyncio.current_task() and not t.done():
            t.print_stack()

#    import atexit, logging
#    @atexit.register
#    def _quiet_exit():
#        logging.getLogger().handlers.clear()

