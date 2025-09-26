# Copyright 2025 Red Hat, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
"""Utilities for rag-content modules."""
import argparse


def get_common_arg_parser() -> argparse.ArgumentParser:
    """Provide common CLI arguments to document processing scripts."""
    parser = argparse.ArgumentParser(description="Embedding CLI for task execution")
    parser.add_argument(
        "-f", "--folder", help="Directory containing the plain text documentation"
    )
    parser.add_argument(
        "-md",
        "--model-dir",
        default="embeddings_model",
        help="Directory containing the embedding model.",
    )
    parser.add_argument("-mn", "--model-name", help="HF repo id of the embedding model")
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
    parser.add_argument(
        "-w",
        "--workers",
        default=None,
        type=int,
        help=(
            "Number of workers to parallelize the data loading. Set to a "
            "negative value by default, turning parallelism off"
        ),
    )
    parser.add_argument(
        "--vector-store-type",
        default="faiss",
        choices=["faiss", "postgres", "llamastack-faiss", "llamastack-sqlite-vec"],
        help="vector store type to be used.",
    )
    parser.add_argument(
        "--auto-chunking",
        action="store_false",
        default=True,
        dest="manual_chunking",
        help="How to do the chunking for llama-stack, manually like in "
        "llama-index or automatically using the RAG runtime tool.",
    )
    return parser
