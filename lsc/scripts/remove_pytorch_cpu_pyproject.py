"""
Removes the pytorch-cpu dependency from the pyproject.toml file.

This script removes the pytorch-cpu dependency from the pyproject.toml file.
It is used to create a container image with GPU CUDA backend.

Usage:
    python remove_pytorch_cpu_pyproject.py

The script will remove the 'tool.uv.index' and 'tool.uv.sources' sections
from the pyproject.toml file in the current directory.
"""

from tomlkit import parse, dumps
from pathlib import Path


def remove_sections(file_path: str, sections_to_remove: list[str]) -> None:
    """
    Remove specified sections from a TOML file.

    Args:
        file_path (str): Path to the TOML file to modify
        sections_to_remove (list[str]): List of section paths to remove,
                                      using dot notation (e.g., "tool.uv.index")

    The function parses the TOML file, removes the specified sections,
    and writes the modified content back to the file.
    """
    path = Path(file_path)
    content = path.read_text(encoding="utf-8")
    doc = parse(content)

    for section in sections_to_remove:
        keys = section.split(".")
        current = doc
        for key in keys[:-1]:
            if key not in current:
                break
            current = current[key]  # type: ignore
        else:
            current.pop(keys[-1], None)

    path.write_text(dumps(doc), encoding="utf-8")


if __name__ == "__main__":
    file_path = "pyproject.toml"
    print(f"pyproject file path: {file_path}")
    sections = ["tool.uv.index", "tool.uv.sources"]
    remove_sections(file_path, sections)
