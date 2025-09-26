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
"""This module can be used to convert and investigate AsciiDoc files."""

import argparse
import logging
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

from lightspeed_rag_content.asciidoc.asciidoctor_converter import (
    RUBY_ASCIIDOC_DIR,
    AsciidoctorConverter,
)

LOG: logging.Logger = logging.getLogger(__package__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def main_convert(args: argparse.Namespace) -> None:
    """Process convert subcommand."""
    try:
        converter = AsciidoctorConverter(
            target_format=args.target_format,
            attributes_file=args.attributes_file,
            converter_file=args.converter_file,
        )
        converter.convert(args.input_file, args.output_file)
    except subprocess.CalledProcessError as e:
        LOG.error(e.stderr)
        sys.exit(e.returncode)
    except (FileNotFoundError, yaml.YAMLError) as e:
        LOG.error(str(e))
        sys.exit(1)


def main_get_structure(args: argparse.Namespace) -> None:
    """Process get_structure subcommand."""
    ruby_cmd = shutil.which("ruby")
    if not ruby_cmd:
        LOG.error("Missing ruby executable")
        sys.exit(1)

    try:
        dumper_script_path: Path = RUBY_ASCIIDOC_DIR.joinpath(
            "asciidoc_structure_dumper.rb"
        )
        subprocess.run(  # noqa: S603
            [
                ruby_cmd,
                str(dumper_script_path.absolute()),
                str(args.input_file.absolute()),
            ],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        LOG.error(e.stderr)
        sys.exit(1)


def get_argument_parser() -> argparse.ArgumentParser:
    """Get ArgumentParser for ligthspeed_rag_content.asciidoc module."""
    parser = argparse.ArgumentParser(
        description="A command that can be used to convert AsciiDoc file to different"
        "formats (convert) and investigate AsciiDoc file structure (get_structure).",
        prog=__package__,
    )
    subparser = parser.add_subparsers(dest="command", required=True)

    convert_parser = subparser.add_parser(
        "convert",
        help="Convert AsciiDoc to text formatted file.",
    )
    convert_parser.add_argument(
        "-i",
        "--input-file",
        required=True,
        type=Path,
        help="AsciiDoc formatted file that should be converted to requested format.",
    )
    convert_parser.add_argument(
        "-o",
        "--output-file",
        required=True,
        type=Path,
        help="A path of where the converted file should be stored.",
    )
    convert_parser.add_argument(
        "-a",
        "--attributes-file",
        required=False,
        type=str,
        help="A file containing attributes that should be passed to asciidoctor.",
    )
    convert_parser.add_argument(
        "-c",
        "--converter-file",
        required=False,
        type=Path,
        help="Asciidoctor compatible extension that should be used to convert the input file.",
    )
    convert_parser.add_argument(
        "-t",
        "--target-format",
        required=False,
        type=str,
        default="text",
        choices=["text", "html5", "xhtml5", "manpage"],
        help="Target format in which the input file should be saved.",
    )

    get_structure_parser = subparser.add_parser(
        "get_structure",
        help="Get structure of AsciiDoc formatted file.",
    )
    get_structure_parser.add_argument(
        "input_file",
        type=Path,
        help="AsciiDoc formatted file that should be investigated.",
    )

    return parser


if __name__ == "__main__":
    parser = get_argument_parser()
    args = parser.parse_args()

    if args.command == "convert":
        main_convert(args)
    else:
        main_get_structure(args)
