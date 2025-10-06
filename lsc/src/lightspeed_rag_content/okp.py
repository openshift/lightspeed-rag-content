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
"""Utility methods processing OKP files."""

import logging
import re
import tomllib
from pathlib import Path
from typing import Any, Generator

from lightspeed_rag_content.metadata_processor import MetadataProcessor

LOG = logging.getLogger(__name__)


def is_file_related_to_projects(metadata: dict[str, Any], projects: list[str]) -> bool:
    """Check if the OKP file is related to specific projects.

    This function checks if the metadata of an OKP file indicates that it is
    related to any of the specified projects. It does this by looking for
    project names in the `portal_product_names` field of the metadata.

    Matching is done by substring because product names can be more specific.
    For example, "Red Hat OpenStack" or "Red Hat OpenStack Platform" both
    should match simply "OpenStack".

    Args:
        metadata (dict[str, Any]): The metadata dictionary of the OKP file.
        projects (list[str]): A list of project names to check against.

    Returns:
        bool: True if the file is related to any of the specified projects,
              False otherwise.

    """
    product_names = metadata.get("extra", {}).get("portal_product_names", [])
    # Lowercase both lists
    product_names = [p.lower() for p in product_names]
    projects = [p.lower() for p in projects]
    return any(p in pn for p in projects for pn in product_names)


def metadata_has_url_and_title(metadata: dict[str, Any]) -> bool:
    """Check if the metadata contains the URL and title.

    Args:
        metadata (dict[str, Any]): The metadata dictionary to check.

    Returns:
        bool: True if both URL and title are present, False otherwise.
    """
    return (
        "reference_url" in metadata.get("extra", {})
        and metadata.get("title", "").strip()
    )


def yield_files_related_to_projects(
    directory: str, projects: list[str]
) -> Generator[Path, None, None]:
    """Yield OKP files paths in a given directory for specific projects.

    This method scans the specified directory for OKP files,
    extracts their metadata, and yields the file paths if they are related
    to the specified projects and contain both a URL and a title.

    For example, the errata/ directory contains files with metadata
    that can be used to determine if the file is related to a specific project.
    The metadata is expected to have a structure similar to:
    {
        "title": "Example Title",
        "extra": {
            "reference_url": "https://example.com",
            "portal_product_names": ["Project Foo", "Project Bar"]
        }
    }

    Args:
        directory (str): The directory to scan for OKP files.
        projects (list[str]): A list of project names to filter the files.

    Yields:
        Path: The path to the OKP file if it is related to the specified projects.
    """
    for filepath in Path(directory).glob("*.md"):
        try:
            metadata = parse_metadata(str(filepath))
            if is_file_related_to_projects(metadata, projects):
                if metadata_has_url_and_title(metadata):
                    yield filepath
                else:
                    LOG.warning(
                        "Skipping OKP file %s: does not have URL and/or title.",
                        filepath,
                    )
        except ValueError as e:
            LOG.warning("Skipping OKP file %s: %s", filepath, e)


def parse_metadata(filepath: str) -> dict[str, Any]:
    """Extract metadata from the OKP file.

    This function reads the content of the OKP file, extracts the metadata block
    enclosed by `+++` markers, and parses it as TOML. It returns the metadata as a
    dictionary.

    Args:
        filepath (str): The path to the OKP file.

    Returns:
        dict[str, Any]: The parsed metadata from the OKP file.

    Raises:
        ValueError: If no metadata block is found in the file.

    """
    with open(filepath, "rb") as f:
        content = f.read()

    # Extract everything between the +++ markers
    match = re.search(rb"\+{3,}\s*(.*?)\s*\+{3,}", content, re.S)
    if not match:
        raise ValueError(f"No metadata found in {filepath}")

    metadata_block = match.group(1)
    return tomllib.loads(metadata_block.decode("utf-8"))


class OKPMetadataProcessor(MetadataProcessor):
    """Metadata processor for OKP files."""

    def url_function(self, file_path: str) -> str:
        """Return the URL for the OKP file."""
        md = parse_metadata(file_path)
        return md["extra"]["reference_url"]

    def get_file_title(self, file_path: str) -> str:
        """Return the title of the OKP file."""
        md = parse_metadata(file_path)
        return md["title"]
