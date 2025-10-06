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

"""This module contains AsciidoctorConverter that can be used to convert AsciiDoc files.

The code in this module is heavily dependent on ruby and asciidoctor. These commands
must be installed before using this module. Otherwise, monsters and dragons await you!

Typical usage example:

    >>> adoc_converter = AsciidoctorConverter()
    >>> adoc_converter.convert(Path("input.adoc"), Path("output.txt"))

An example of more involved usage:

    >>> adoc_converter = AsciidoctorConverter(
    ...    target_format='custom',
    ...    attributes_file=Path('./attributes.yaml'),
    ...    converter_file=Path('./asciidoc_custom_format_converter.rb'),
    ... )
    >>> adoc_converter.convert(Path("input.adoc"), Path("output.custom"))

'attributes.yaml' content:

    ---
    attribute_name_1: attribute_value_1
    attribute_name_2: attribute_value_2
    ...

'asciidoc_custom_format_converter.rb' has to be compatible with asciidoctor.
Please read: https://docs.asciidoctor.org/asciidoctor/latest/extensions/
You can also investigate the default text converter 'asciidoc_text_converter.rb'
stored in the asciidoc package.
"""
import logging
import shutil
import subprocess
from importlib import resources
from pathlib import Path
from typing import Optional

import yaml

LOG: logging.Logger = logging.getLogger(__name__)

PACKAGE = __package__ or ""

RUBY_ASCIIDOC_DIR: Path = Path(str(resources.files(PACKAGE))).joinpath("ruby_asciidoc")


class AsciidoctorConverter:
    """Convert AsciiDoc formatted documents to different formats.

    The class requires asciidoctor to be installed. By default, all files are
    converted to text format using a custom asciidoctor compatible extension
    that is written in Ruby.
    """

    def __init__(
        self,
        target_format: str = "text",
        attributes_file: Optional[Path] = None,
        converter_file: Optional[Path] = None,
    ):
        """Initialize AsciidoctorConverter.

        Args:
            target_format:
                A format to which input files should be converted. These formats
                are currently supported: text, html5, xhtml5, manpage.
            attributes_file: A path pointing to an attributes file.
            converter_file: An asciidoctor compatible extension.

        Raises:
            FileNotFoundError:
                When asciidoctor executable or converter_file cannot be found.

            yaml.YAMLError:
                When attributes_file is not valid YAML file.
        """
        self.target_format = target_format
        self.attribute_list = self._get_attribute_list(attributes_file)

        if not converter_file:
            self.converter_file = self._get_converter_file(target_format)
        else:
            self.converter_file = converter_file

        self.asciidoctor_cmd = self._get_asciidoctor_path()

    @staticmethod
    def _get_converter_file(target_format: str) -> Optional[Path]:
        """Return converter file if target_format requires one."""
        asciidoctor_supported_formats = ["html5", "xhtml5", "manpage"]
        if target_format in asciidoctor_supported_formats:
            return None

        converter_files = {
            "text": "asciidoc_text_converter.rb",
        }

        if not (converter_file := converter_files.get(target_format, None)):
            raise FileNotFoundError(
                f"There is no extension available for target format: {target_format}"
            )

        return RUBY_ASCIIDOC_DIR.joinpath(converter_file)

    @staticmethod
    def _get_asciidoctor_path() -> str:
        """Check whether asciidoctor and ruby are installed."""
        asciidoctor_path = shutil.which("asciidoctor")
        if not asciidoctor_path:
            raise FileNotFoundError("asciidoctor executable not found")

        LOG.info("Using asciidoctor with %s path", asciidoctor_path)
        return asciidoctor_path

    @staticmethod
    def _get_attribute_list(attributes_file: Path | None) -> list[str]:
        """Convert file containing attributes to list of '-a <key>=<value>'."""
        attribute_list: list[str] = []

        if attributes_file is None:
            return attribute_list

        with open(attributes_file, "r", encoding="utf-8") as file:
            if (attributes := yaml.safe_load(file)) is None:
                return attribute_list

            for key, value in attributes.items():
                attribute_list += ["-a", key + f"={value}"]

        return attribute_list

    def convert(self, source_file: Path, destination_file: Path) -> None:
        """Convert AsciiDoc formatted file to target format.

        Args:
            source_file: A path of a file that should be converted.
            destination_file:
                A path of where the converted file should be stored. If
                the directories in the path do not exist, they will be created

        Raises:
            subprocess.CalledSubprocessError:
                If an error occurs when running asciidoctor.
        """
        LOG.info("Processing: %s", str(source_file.absolute()))
        if not destination_file.exists():
            destination_file.parent.mkdir(parents=True, exist_ok=True)
        else:
            LOG.warning(
                "Destination file %s exists. It will be overwritten!",
                destination_file,
            )

        command = [self.asciidoctor_cmd]

        if self.attribute_list:
            command += self.attribute_list
        if self.converter_file:
            command += ["-r", str(self.converter_file.absolute())]

        command = [
            *command,
            "-b",
            self.target_format,
            "-o",
            str(destination_file.absolute()),
            "--trace",
            "--quiet",
            str(source_file.absolute()),
        ]

        subprocess.run(command, check=True, capture_output=True)  # noqa: S603
