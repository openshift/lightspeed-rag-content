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

import os
import sys, logging

logging.basicConfig(
    level=logging.DEBUG,  # Ensure DEBUG messages are shown
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr,
    force=True,
)

import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / "src"))

from lightspeed_rag_content.metadata_processor import MetadataProcessor
from lightspeed_rag_content.document_processor import DocumentProcessor
from lightspeed_rag_content import utils


class OCPMetadataProcessor(MetadataProcessor):

    def __init__(self, docs_root_url: str, docs_version: str, plaintext_root_dir: str):
        self.root_url = docs_root_url + "/" + docs_version
        self.docs_version = docs_version
        self.plaintext_root_dir = plaintext_root_dir + "/" + docs_version + "/"


    def url_function(self, file_path: str) -> str:
        return self.root_url
        + file_path.removeprefix(self.plaintext_root_dir).removesuffix("txt")
        + "html"


class RunbooksMetadataProcessor(MetadataProcessor):

    def __init__(self, runbooks_root_url: str, plaintext_root_dir: str):
        self.root_url = runbooks_root_url
        self.plaintext_root_dir = os.path.abspath(plaintext_root_dir)
        if self.plaintext_root_dir.endswith("/"):
            self.plaintext_root_dir = self.plaintext_root_dir[:-1]


    def url_function(self, file_path: str) -> str:
        print("file_path: " + file_path + ", self.plaintext_root_dir: " + self.plaintext_root_dir)
        return self.root_url + file_path.removeprefix(self.plaintext_root_dir)


if __name__ == "__main__":

    parser = utils.get_common_arg_parser()
    parser.add_argument(
        "-v", "--ocp-version", help="OCP version"
    )
    parser.add_argument(
        "-r", "--root-url", help="Root URL for the OCP docs website"
    )
    parser.add_argument(
        "-rbu", "--runbooks-root-url", help="Root URL for the runbooks website"
    )
    parser.add_argument(
        "-rbp", "--runbooks-plaintext-dir", help="Directory with runbooks plaintext"
    )
    args = parser.parse_args()

    # Instantiate Document Processor
    document_processor = DocumentProcessor(
        chunk_size=args.chunk,
        chunk_overlap=args.overlap,
        model_name=args.model_name,
        embeddings_model_dir=args.model_dir,
        num_workers=args.workers,
        vector_store_type=args.vector_store_type,
    )

    # Instantiate OCP Metadata Processor
    ocp_metadata_processor = OCPMetadataProcessor(
        args.root_url,
        args.ocp_version,
        args.folder
    )

    # Load and embed the documents, this method can be called multiple times
    # for different sets of documents
    document_processor.process(args.folder, metadata=ocp_metadata_processor)

    runbooks_metadata_processor = RunbooksMetadataProcessor(
        args.runbooks_root_url,
        args.runbooks_plaintext_dir
    )
    document_processor.process(args.runbooks_plaintext_dir, metadata=runbooks_metadata_processor)

    # Save the new vector database to the output directory
    document_processor.save(args.index, args.output)

    os._exit(0)