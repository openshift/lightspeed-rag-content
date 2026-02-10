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
"""Document processing for vector database."""

import asyncio
import json
import logging
import os
import tempfile
import time
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional, Union

import faiss
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.llms.utils import resolve_llm
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.core.readers.base import BaseReader
from llama_index.core.schema import Document, TextNode
from llama_index.core.storage.storage_context import StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.vector_stores.postgres import PGVectorStore
from sentence_transformers import SentenceTransformer

from lightspeed_rag_content.metadata_processor import MetadataProcessor

if TYPE_CHECKING:
    from llama_index.core.vector_stores.types import BasePydanticVectorStore

LOG = logging.getLogger(__name__)


class _Config:
    """This is a bag of holding allowing attribute access to keyword args."""

    __attributes: dict[str, Any]

    def __init__(self, **kwargs: Any):
        # Use an internal dict instead of self.__dict__.update(kwargs) to
        # help with typechecking
        self.__attributes = kwargs

    def __getattr__(self, name: str) -> Any:
        return self.__attributes[name]

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "_Config__attributes":
            super().__setattr__(name, value)
        else:
            self.__attributes[name] = value


class _BaseDB:
    def __init__(self, config: _Config):
        self.config = config

        if config.vector_store_type.startswith("llamastack"):
            if config.manual_chunking:
                Settings.chunk_size = self.config.chunk_size
                Settings.chunk_overlap = self.config.chunk_overlap
            if config.doc_type in ("markdown", "html"):
                Settings.node_parser = MarkdownNodeParser()
            return

        if config.manual_chunking:
            Settings.chunk_size = self.config.chunk_size
            Settings.chunk_overlap = self.config.chunk_overlap
            Settings.embed_model = HuggingFaceEmbedding(
                model_name=str(self.config.embeddings_model_dir)
            )
            Settings.llm = resolve_llm(None)
        # HTML uses MarkdownNodeParser since HTMLReader converts to Markdown
        if config.doc_type in ("markdown", "html"):
            Settings.node_parser = MarkdownNodeParser()

    @staticmethod
    def _got_whitespace(text: str) -> bool:
        """Indicate if the parameter string contains whitespace."""
        for c in text:
            if c.isspace():
                return True
        return False

    @classmethod
    def _filter_out_invalid_nodes(cls, nodes: list[Any]) -> list[TextNode]:
        """Filter out invalid nodes."""
        good_nodes = []
        for node in nodes:
            if isinstance(node, TextNode) and cls._got_whitespace(node.text):
                # Exclude given metadata during embedding
                good_nodes.append(node)
            else:
                LOG.debug("Skipping node without whitespace: %s", repr(node))
        return good_nodes

    @classmethod
    def _split_and_filter(cls, docs: list[Document]) -> list[TextNode]:
        nodes = Settings.text_splitter.get_nodes_from_documents(docs)
        valid_nodes = cls._filter_out_invalid_nodes(nodes)
        return valid_nodes


class _LlamaIndexDB(_BaseDB):
    def __init__(self, config: _Config):
        vector_store: None | BasePydanticVectorStore = None

        assert config.vector_store_type in ("faiss", "postgres")  # noqa: S101
        super().__init__(config)

        self.config.embedding_dimension = len(
            Settings.embed_model.get_text_embedding("random text")
        )

        if config.vector_store_type == "faiss":
            faiss_index = faiss.IndexFlatIP(config.embedding_dimension)
            vector_store = FaissVectorStore(faiss_index=faiss_index)

        elif config.vector_store_type == "postgres":
            user = os.getenv("POSTGRES_USER")
            password = os.getenv("POSTGRES_PASSWORD")
            host = os.getenv("POSTGRES_HOST")
            port = os.getenv("POSTGRES_PORT")
            database = os.getenv("POSTGRES_DATABASE")
            vector_store = PGVectorStore.from_params(
                database=database,
                host=host,
                password=password,
                port=port,
                user=user,
                table_name=config.table_name,
                embed_dim=config.embedding_dimension,  # openai embedding dimension
            )
        self.storage_context = StorageContext.from_defaults(vector_store=vector_store)
        # List of good nodes
        self._good_nodes: list[TextNode] = []

    def add_docs(self, docs: list[Document]) -> None:
        """Add documents to the list of documents to save."""
        valid_nodes = self._split_and_filter(docs)
        self._good_nodes.extend(valid_nodes)

    def save(
        self, index: str, output_dir: str, embedded_files: int, exec_time: int
    ) -> None:
        """Save vector store index and metadata."""
        self._save_index(index, output_dir)
        self._save_metadata(index, output_dir, embedded_files, exec_time)

    def _save_index(self, index: str, persist_folder: str) -> None:
        """Create and save the Vector Store Index."""
        idx = VectorStoreIndex(
            self._good_nodes,
            storage_context=self.storage_context,
        )
        idx.set_index_id(index)
        idx.storage_context.persist(persist_dir=persist_folder)

    def _save_metadata(
        self, index: str, persist_folder: str, embedded_files: int, exec_time: int
    ) -> None:
        """Create and save the metadata."""
        vector_db = (
            "faiss.IndexFlatIP"
            if self.config.vector_store_type == "faiss"
            else "PGVectorStore"
        )
        metadata: dict[str, Union[str, int, float]] = {
            "execution-time": exec_time,
            "llm": "None",
            "embedding-model": self.config.model_name,
            "index-id": index,
            "vector-db": vector_db,
            "embedding-dimension": self.config.embedding_dimension,
            "chunk": self.config.chunk_size,
            "overlap": self.config.chunk_overlap,
            "total-embedded-files": embedded_files,
        }
        with open(
            os.path.join(persist_folder, "metadata.json"), "w", encoding="utf-8"
        ) as file:
            file.write(json.dumps(metadata))


class _LlamaStackDB(_BaseDB):
    # Lllama-stack faiss vector-db uses IndexFlatL2 (it's hardcoded for now)
    TEMPLATE = """version: 2
image_name: starter

apis:
- files
- tool_runtime
- vector_io
- inference

server:
  port: 8321
conversations_store:
  db_path: /tmp/conversations.db
  type: sqlite
metadata_store:
  db_path: /tmp/registry.db
  type: sqlite

providers:
  inference:
  - config: {{}}
    provider_id: sentence-transformers
    provider_type: inline::sentence-transformers
  files:
  - config:
      metadata_store:
        table_name: files_metadata
        backend: sql_default
      storage_dir: /tmp/files
    provider_id: meta-reference-files
    provider_type: inline::localfs
  tool_runtime:
  - config: {{}}
    provider_id: rag-runtime
    provider_type: inline::rag-runtime
  vector_io:
  - config:
      persistence:
        namespace: vector_io::{provider_type}
        backend: kv_rag
    provider_id: {index_id}
    provider_type: inline::{provider_type}
storage:
  backends:
    kv_rag:
      type: kv_sqlite
      db_path: {kv_db_path}
    kv_default:
      type: kv_sqlite
      db_path: /tmp/kv_store.db
    sql_default:
      type: sql_sqlite
      db_path: /tmp/sql_store.db
  stores:
    metadata:
      namespace: registry
      backend: kv_default
    inference:
      table_name: inference_store
      backend: sql_default
    conversations:
      table_name: openai_conversations
      backend: sql_default
registered_resources:
  models:
  - metadata:
      embedding_dimension: {dimension}
    model_id: {model_name}
    provider_id: sentence-transformers
    provider_model_id: {model_name_or_dir}
    model_type: embedding
  vector_stores: []
  shields: []
  datasets: []
  scoring_fns: []
  benchmarks: []
  tool_groups:
  - toolgroup_id: builtin::rag
    provider_id: rag-runtime
"""
    # Template for vector_stores section, added after vector store is created
    VECTOR_STORES_TEMPLATE = """vector_stores:
  - embedding_dimension: {dimension}
    embedding_model: sentence-transformers/{model_name_or_dir}
    provider_id: {vector_io_provider_id}
    vector_store_id: {vector_store_id}"""

    CFG_FILENAME = "llama-stack.yaml"

    def __init__(self, config: _Config):
        """Initialize the llama-stack Vector IO database.

        We have 2 options, we either create a llama-stack configuration file or
        we start it with a template and then make a series of calls to create
        the providers: model, inference, vector_io.

        We have chosen to create a configuration file which we can then leave
        together with the database for reference.

        Llama-stack is used as a library and this class supports 2 llama-stack
        Vector IO providers: faiss and sqlite-vec.

        Faiss seems to create much larger database files, to the point of
        absurdity.

        LIMITATION: It can only work once for now, since we are using a file
                    and not clearing things up.

        Embedding and Chunk Creation:
            The methods `_insert_prechunked_documents` and `_upload_and_process_files`
            are responsible for creating embeddings and building chunks. The chunk
            metadata (converted to attributes in the vector store) is expected to
            contain the following fields:
            - docs_url: URL of the source document
            - title: Title of the document
            - document_id: Unique identifier for the document
        """
        assert config.vector_store_type in (  # noqa: S101
            "llamastack-faiss",
            "llamastack-sqlite-vec",
        )

        super().__init__(config)

        # When using a model directory We need to use absolute paths because
        # the configuration file is not in the current directory.
        if os.path.exists(config.embeddings_model_dir):
            self.model_name_or_dir = os.path.realpath(config.embeddings_model_dir)
        else:
            self.model_name_or_dir = config.model_name

        model = SentenceTransformer(self.model_name_or_dir)
        self.config.embedding_dimension = model.get_sentence_embedding_dimension()

        # faiss_store.db or sqlitevec_store.db
        self.db_filename = config.vector_store_type[11:] + "_store.db"

        # We need to set env var before importing llama_stack
        # Create temp directory for the llama-stack configuration file and the DB
        self.tmp_dir = tempfile.TemporaryDirectory(  # pylint: disable=R1732
            prefix="ls-rag-"
        )
        # Force a default directory to prevent llama-stack from using hosts's
        # ~/.llama content
        os.environ["LLAMA_STACK_CONFIG_DIR"] = self.tmp_dir.name

        # TODO: This part may need to be changed to support multiple usages
        # Not using importlib to help with typechecking
        import llama_stack_api  # pylint: disable=C0415
        from llama_stack.core.library_client import (  # pylint: disable=C0415
            AsyncLlamaStackAsLibraryClient,
        )

        self.document_class = llama_stack_api.rag_tool.RAGDocument
        self.client_class = AsyncLlamaStackAsLibraryClient
        self.documents: list[dict[str, Any] | llama_stack_api.rag_tool.RAGDocument] = []

    @property
    def provider_type(self) -> str:
        """Extract provider type from vector_store_type (e.g., 'llamastack-faiss' -> 'faiss')."""
        return str(self.config.vector_store_type).split("-", 1)[1]

    def write_yaml_config(
        self, index_id: str, filename: str, db_file: str, files_metadata_db_file: str
    ) -> None:
        """Write a llama-stack configuration file using class templates."""
        if self.config.vector_store_type == "llamastack-faiss":
            vector_io_cfg = ""
        else:
            vector_io_cfg = "db_path: " + db_file

        with open(filename, "w", encoding="utf-8") as fd:
            data = self.TEMPLATE.format(
                index_id=index_id,
                provider_type=self.provider_type,
                vector_io_cfg=vector_io_cfg,
                kv_db_path=db_file,
                sql_db_path=files_metadata_db_file,
                model_name=self.config.model_name,
                model_name_or_dir=self.model_name_or_dir,
                dimension=self.config.embedding_dimension,
            )
            fd.write(data)

    async def _run_llama_stack(self, cfg_file: str, index: str) -> str:
        """Run vector store operations with llama-stack client.

        Call the proper method depending on --auto-chunking flag.
        Uses async context manager for automatic initialization and shutdown.

        Returns:
            The vector store ID
        """
        async with self.client_class(cfg_file) as client:
            if self.config.manual_chunking:
                return await self._insert_prechunked_documents(client, index)
            return await self._upload_and_process_files(client, index)

    def add_docs(self, docs: list[Document]) -> None:
        """Add documents to the list of documents to save."""
        if self.config.manual_chunking:
            for node in self._split_and_filter(docs):
                # Add document_id to node's metadata because llama-stack needs it
                node.metadata["document_id"] = node.ref_doc_id
                chunk_metadata = {
                    "document_id": node.ref_doc_id,
                    "chunk_id": node.id_,
                    "source": node.metadata.get("docs_url", node.metadata["title"]),
                }
                self.documents.append(
                    {
                        "content": node.text,
                        # "mime_type": "text/plain",  # Not part of Chunk type schema
                        "metadata": node.metadata,
                        "chunk_metadata": chunk_metadata,
                        "chunk_id": node.id_,
                    }
                )

        else:
            self.documents.extend(
                self.document_class(
                    document_id=doc.doc_id,
                    content=doc.text,
                    mime_type="text/plain",
                    metadata=doc.metadata,
                )
                for doc in docs
            )

    async def _insert_prechunked_documents(  # pylint: disable=R0914
        self, client: Any, index: str
    ) -> str:
        """Manual chunking: Insert pre-chunked documents into the vector store.

        This method uses two new llama-stack APIs (OpenAI compatible):
        1. vector_stores API: Creates a new vector store
        2. files API: Creates empty placeholder files for citation metadata
           (provides document ID, URL, and title for citations)
        And the vector_io API: Inserts chunks with embeddings

        The empty files serve as citation anchors, linking chunks back to their
        source documents without storing duplicate content (we don't use files downstream).

        Returns:
            The vector store ID
        """
        vector_store = await client.vector_stores.create(
            name=index,
            extra_body={
                "provider_id": index,
                "embedding_model": f"sentence-transformers/{self.model_name_or_dir}",
                "embedding_dimension": self.config.embedding_dimension,
            },
        )

        async def upload_file(chunk_indices: list[int]) -> str:
            """Upload a placeholder file and update all related chunks.

            Args:
                chunk_indices: List of indices in self.documents for chunks from same source

            Returns:
                File ID
            """
            first_chunk = dict(self.documents[chunk_indices[0]])
            doc_metadata = first_chunk["metadata"]

            doc_uuid = doc_metadata["document_id"]
            filename = f"{doc_uuid}"

            file_obj = BytesIO("".encode("utf-8"))  # Empty file for citation anchor
            file_obj.name = f"{filename}.txt"

            uploaded_file = await client.files.create(
                file=file_obj,
                purpose="assistants",
            )

            # Update ALL chunks from this source document with the file_id
            for chunk_idx in chunk_indices:
                chunk_doc = dict(self.documents[chunk_idx])
                chunk_doc["chunk_metadata"]["document_id"] = uploaded_file.id
                chunk_doc["metadata"]["document_id"] = uploaded_file.id

            return str(uploaded_file.id)

        # Group chunks by source document
        doc_groups: dict[str, list[int]] = {}
        for idx, chunk in enumerate(self.documents):
            chunk = dict(chunk)
            doc_id = chunk["metadata"]["document_id"]
            if doc_id not in doc_groups:
                doc_groups[doc_id] = []
            doc_groups[doc_id].append(idx)

        upload_tasks = [
            upload_file(chunk_indices) for chunk_indices in doc_groups.values()
        ]
        results = await asyncio.gather(*upload_tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, Exception):
                LOG.error("Failed to upload file: %s", result)

        # Compute embeddings
        LOG.info("Computing embeddings for %d chunks...", len(self.documents))
        chunks_to_insert = []
        embedding_model = f"sentence-transformers/{self.model_name_or_dir}"

        for idx, doc in enumerate(self.documents):
            if isinstance(doc, dict):
                embedding_response = await client.embeddings.create(
                    input=doc["content"],
                    model=embedding_model,
                )
                embedding = embedding_response.data[0].embedding

                chunk = {
                    "content": doc["content"],
                    "chunk_id": doc["chunk_id"],
                    "metadata": doc.get("metadata", {}),
                    "chunk_metadata": doc["chunk_metadata"],
                    "embedding": embedding,
                    "embedding_model": embedding_model,
                    "embedding_dimension": self.config.embedding_dimension,
                }
                chunks_to_insert.append(chunk)
            else:
                chunks_to_insert.append(doc)

        LOG.info("Inserting %d chunks into vector store...", len(chunks_to_insert))
        await client.vector_io.insert(
            vector_store_id=vector_store.id, chunks=chunks_to_insert
        )
        return str(vector_store.id)

    async def _upload_and_process_files(  # noqa: C901  # pylint: disable=R0912,R0914
        self, client: Any, index: str
    ) -> str:
        """Auto chunking: Upload and process files one at a time.

        Called when --auto-chunking flag enabled.
        File batch processing in llama-stack applies the attributes dict to all files.
        We use single file upload until batch upload allows giving attributes per file.

        Returns:
            The vector store ID
        """
        vector_store = await client.vector_stores.create(
            name=index,
            extra_body={
                "provider_id": index,
                "embedding_model": f"sentence-transformers/{self.model_name_or_dir}",
                "embedding_dimension": self.config.embedding_dimension,
            },
        )

        chunking_strategy = {
            "type": "static",
            "static": {
                "max_chunk_size_tokens": self.config.chunk_size,
                "chunk_overlap_tokens": self.config.chunk_overlap,
            },
        }

        total_docs = len(self.documents)
        successful = 0
        failed_docs = []

        LOG.info("Processing %d files...", total_docs)

        for idx, rag_doc in enumerate(self.documents):
            doc_uuid = rag_doc.document_id  # type: ignore[union-attr]
            max_retries = 3

            for attempt in range(max_retries):
                try:
                    # Upload file (rag_doc is RAGDocument in auto chunking mode)
                    file_obj = BytesIO(rag_doc.content.encode("utf-8"))  # type: ignore[union-attr]
                    file_obj.name = f"{doc_uuid}.txt"

                    uploaded_file = await client.files.create(
                        file=file_obj,
                        purpose="assistants",
                    )

                    # Attach file to vector store and wait for processing
                    attributes = {
                        **rag_doc.metadata,  # type: ignore[union-attr]
                        "document_id": doc_uuid,
                    }
                    vs_file = await client.vector_stores.files.create(
                        vector_store_id=vector_store.id,
                        file_id=uploaded_file.id,
                        attributes=attributes,
                        chunking_strategy=chunking_strategy,
                    )

                    # Wait for this file to be processed
                    max_wait = 5 * 60
                    start_time = time.time()
                    while (time.time() - start_time) < max_wait:
                        vs_file = await client.vector_stores.files.retrieve(
                            vector_store_id=vector_store.id,
                            file_id=uploaded_file.id,
                        )
                        if vs_file.status in ("completed", "failed", "cancelled"):
                            break
                        await asyncio.sleep(0.5)

                    if vs_file.status == "completed":
                        successful += 1
                        if (idx + 1) % 10 == 0 or (idx + 1) == total_docs:
                            LOG.info(
                                "Progress: %d/%d files processed",
                                idx + 1,
                                total_docs,
                            )
                        break

                    error = getattr(vs_file, "last_error", "unknown error")
                    LOG.warning(
                        "File %s attempt %d/%d failed: %s",
                        doc_uuid,
                        attempt + 1,
                        max_retries,
                        error,
                    )
                    if attempt == max_retries - 1:
                        failed_docs.append((doc_uuid, error))

                except Exception as e:  # pylint: disable=broad-exception-caught
                    LOG.warning(
                        "File %s attempt %d/%d error: %s",
                        doc_uuid,
                        attempt + 1,
                        max_retries,
                        e,
                    )
                    if attempt == max_retries - 1:
                        failed_docs.append((doc_uuid, str(e)))
                    else:
                        await asyncio.sleep(1)

        LOG.info(
            "File processing finished: successful=%d/%d, failed=%d",
            successful,
            total_docs,
            len(failed_docs),
        )

        if failed_docs:
            for doc_uuid, error in failed_docs[:10]:  # Show first 10
                LOG.error("Failed document %s: %s", doc_uuid, error)
            raise RuntimeError(
                f"Failed to process {len(failed_docs)}/{total_docs} files"
            )

        LOG.info("All files processed successfully")
        return str(vector_store.id)

    def _update_yaml_config(
        self, cfg_file: str, index: str, vector_store_id: str
    ) -> None:
        """Update the config file with the created vector_store_id."""
        vector_stores_section = self.VECTOR_STORES_TEMPLATE.format(
            dimension=self.config.embedding_dimension,
            model_name_or_dir=self.model_name_or_dir,
            vector_io_provider_id=index,
            vector_store_id=vector_store_id,
        )
        with open(cfg_file, "r", encoding="utf-8") as f:
            config_content = f.read()
        config_content = config_content.replace(
            "vector_stores: []", vector_stores_section
        )
        with open(cfg_file, "w", encoding="utf-8") as f:
            f.write(config_content)

    def save(
        self,
        index: str,
        output_dir: str,
        embedded_files: Optional[int] = None,  # pylint: disable=W0613
        exec_time: Optional[int] = None,  # pylint: disable=W0613
    ) -> None:
        """Save in the vector database all the documents we added."""
        os.makedirs(output_dir, exist_ok=True)
        db_file = os.path.realpath(os.path.join(output_dir, self.db_filename))
        files_metadata_db_file = os.path.realpath(
            os.path.join(output_dir, "files_metadata.db")
        )
        cfg_file = os.path.join(output_dir, self.CFG_FILENAME)
        # There's no need to register the DB because the YAML includes it
        self.write_yaml_config(index, cfg_file, db_file, files_metadata_db_file)
        try:
            vector_store_id = asyncio.run(self._run_llama_stack(cfg_file, index))
            self._update_yaml_config(cfg_file, index, vector_store_id)
        except Exception as exc:
            LOG.error("Failed to insert document: %s", exc)
            raise


class DocumentProcessor:
    """Processes documents into vector database entries."""

    def __init__(
        self,
        chunk_size: int,
        chunk_overlap: int,
        model_name: str,
        embeddings_model_dir: Path,
        num_workers: Optional[int] = 0,
        vector_store_type: str = "faiss",
        table_name: Optional[str] = None,
        manual_chunking: bool = True,
        doc_type: str = "text",
    ):
        """Initialize instance."""
        if vector_store_type == "postgres" and not table_name:
            table_name = "table_name"

        self.config = _Config(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            model_name=model_name,
            embeddings_model_dir=embeddings_model_dir,
            embedding_dimension=None,  # Calculated in the DB __init__ method
            num_workers=num_workers,
            vector_store_type=vector_store_type,
            table_name=table_name,
            manual_chunking=manual_chunking,
            doc_type=doc_type,
        )

        self._check_config(self.config)

        # Total number of embedded files
        self._num_embedded_files = 0
        # Start of time, used to calculate the execution time
        self._start_time = time.time()

        if embeddings_model_dir:
            os.environ["HF_HOME"] = str(embeddings_model_dir)
            os.environ["TRANSFORMERS_OFFLINE"] = "1"

        self.db = self._get_db()

    @staticmethod
    def _check_config(config: _Config) -> None:
        if config.vector_store_type == "faiss" and not config.manual_chunking:
            LOG.warning("Ignoring manual_chunking parameter, not supported by faiss")

        if config.vector_store_type != "postgres" and config.table_name:
            LOG.warning("Ignoring table_name parameter, not supported by faiss")

    def _get_db(self) -> _LlamaIndexDB | _LlamaStackDB:
        if self.config.vector_store_type in ("faiss", "postgres"):
            return _LlamaIndexDB(self.config)

        if self.config.vector_store_type.startswith("llamastack"):
            return _LlamaStackDB(self.config)

        raise RuntimeError(
            f"Unknown vector store type: {self.config.vector_store_type}"
        )

    def process(
        self,
        docs_dir: Path,
        metadata: MetadataProcessor,
        required_exts: Optional[list[str]] = None,
        file_extractor: Optional[dict[str, BaseReader]] = None,
        unreachable_action: Optional[str] = "warn",
        ignore_list: Optional[list[str]] = None,
    ) -> None:
        """Read documents from a path and split them into nodes for a vector database.

        unreachable_action:
        "warn": Just log a warning message for links that are unreacheable
        "fail": Fail in case of an unreachable link. Raises RuntimeError
        "drop": Drop the document, do not include it into the vector database

        ignore_list:
        List of document titles to exclude from unreachable URL validation.
        Documents with titles in this list will be included in the vector database
        regardless of their url_reachable status.
        """
        reader = SimpleDirectoryReader(
            str(docs_dir),
            recursive=True,
            file_metadata=metadata.populate,
            required_exts=required_exts,
            file_extractor=file_extractor,
        )

        # Create chunks/nodes
        docs = reader.load_data(num_workers=self.config.num_workers)

        # Check for unreachable URLs if we are not ignoring them
        if unreachable_action != "warn":
            # Separate docs into those we should check and those in ignore_list
            if ignore_list:
                docs_to_check = []
                ignored_docs = []
                for doc in docs:
                    if doc.metadata.get("title") in ignore_list:
                        ignored_docs.append(doc)
                    else:
                        docs_to_check.append(doc)
            else:
                docs_to_check = docs
                ignored_docs = []

            # Find reachable docs among those we're checking
            reachable_docs = [
                doc for doc in docs_to_check if doc.metadata["url_reachable"] is True
            ]

            if len(docs_to_check) != len(reachable_docs):
                # Optionally fail on unreachable URLs
                if unreachable_action == "fail":
                    raise RuntimeError("Some documents have unreachable URLs. ")
                # Optionally drop unreachable URLs (but keep ignored docs)
                if unreachable_action == "drop":
                    docs = reachable_docs + ignored_docs

        self.db.add_docs(docs)

        # Count embedded files and unreachable nodes
        self._num_embedded_files += len(docs)

    def save(self, index: str, output_dir: str) -> None:
        """Save all the documents we've added to the vector database."""
        exec_time = int(time.time() - self._start_time)
        self.db.save(index, output_dir, self._num_embedded_files, exec_time)
