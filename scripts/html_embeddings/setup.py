#!/usr/bin/env python3
"""
Setup script for the HTML embeddings pipeline.

This script helps set up the environment, validate dependencies,
and prepare the directory structure for the HTML embeddings pipeline.
"""

import argparse
import os
import sys
import subprocess
from pathlib import Path
from typing import List, Tuple, Dict


def check_python_version() -> bool:
    """Check if Python version is adequate."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"Error: Python 3.8+ required, found {version.major}.{version.minor}")
        return False

    print(f"Python {version.major}.{version.minor}.{version.micro}")
    return True


def check_dependencies() -> Tuple[List[str], List[str]]:
    """Check if required dependencies are installed."""
    required_packages = [
        "llama_index",
        "transformers",
        "faiss",
        "aiohttp",
        "beautifulsoup4",
        "PyYAML",
        "sqlite3",  # Built-in but check anyway
    ]

    installed = []
    missing = []

    for package in required_packages:
        try:
            if package == "sqlite3":
                import sqlite3
            elif package == "llama_index":
                import llama_index
            elif package == "beautifulsoup4":
                import bs4
            elif package == "PyYAML":
                import yaml
            else:
                __import__(package.replace("-", "_"))
            installed.append(package)
            print(f"  {package}: installed")
        except ImportError:
            missing.append(package)
            print(f"  {package}: missing")

    return installed, missing


def install_missing_packages(packages: List[str]) -> bool:
    """Install missing packages using pip."""
    if not packages:
        return True

    print(f"\nInstalling missing packages: {', '.join(packages)}")

    pip_names = {
        "beautifulsoup4": "beautifulsoup4",
        "llama_index": "llama-index",
        "aiohttp": "aiohttp",
        "transformers": "transformers",
        "faiss": "faiss-cpu",
        "PyYAML": "PyYAML",
    }

    for package in packages:
        pip_name = pip_names.get(package, package)
        try:
            print(f"Installing {pip_name}...")
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", pip_name],
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                print(f"Successfully installed {pip_name}")
            else:
                print(f"Failed to install {pip_name}: {result.stderr}")
                return False
        except Exception as e:
            print(f"Error installing {pip_name}: {e}")
            return False

    return True


def create_directory_structure(base_dir: Path) -> Dict[str, Path]:
    """Create the recommended directory structure."""
    directories = {
        "scripts": base_dir / "scripts" / "html_embeddings",
        "cache": base_dir / "cache",
        "vector_db": base_dir / "vector_db",
        "embeddings_model": base_dir / "embeddings_model",
        "runbooks": base_dir / "runbooks",
    }

    print("\nCreating directory structure...")
    for name, path in directories.items():
        path.mkdir(parents=True, exist_ok=True)
        print(f"  {name}: {path}")

    return directories


def validate_existing_components(base_dir: Path) -> Dict[str, bool]:
    """Validate existing components like model directory."""
    validations = {}

    # Check if embedding model exists
    model_dir = base_dir / "embeddings_model"
    if model_dir.exists():
        required_files = ["config.json"]
        has_required = any((model_dir / f).exists() for f in required_files)
        validations["embedding_model"] = has_required
        status = "found" if has_required else "not found"
        print(f"Embedding model: {model_dir} ({status})")
    else:
        validations["embedding_model"] = False
        print(f"Embedding model: {model_dir} (not found)")

    # Check if runbooks exist
    runbooks_dir = base_dir / "runbooks"
    if runbooks_dir.exists():
        md_files = list(runbooks_dir.rglob("*.md"))
        validations["runbooks"] = len(md_files) > 0
        status = "found" if len(md_files) > 0 else "empty"
        print(f"Runbooks: {runbooks_dir} ({len(md_files)} .md files, {status})")
    else:
        validations["runbooks"] = False
        print(f"Runbooks: {runbooks_dir} (not found)")

    return validations


def create_example_config(base_dir: Path) -> None:
    """Create example configuration files."""
    config_dir = base_dir / "scripts" / "html_embeddings"

    # Create example run script
    example_script = config_dir / "run_example.sh"
    with open(example_script, "w", encoding="utf-8") as f:
        f.write(
            """#!/bin/bash

# Example script to run HTML embeddings pipeline for OpenShift 4.18

# Set variables
VERSION="4.18"
INDEX="ocp-4.18"
OUTPUT_DIR="./vector_db"
MODEL_DIR="./embeddings_model"
CACHE_DIR="./cache"

# Run the pipeline
python generate_embeddings.py \\
  --version "$VERSION" \\
  --index "$INDEX" \\
  --output-dir "$OUTPUT_DIR" \\
  --model-dir "$MODEL_DIR" \\
  --cache-dir "$CACHE_DIR" \\
  --max-token-limit 384 \\
  --verbose

echo "Pipeline completed. Check $OUTPUT_DIR for results."
"""
        )

    example_script.chmod(0o755)
    print(f"Created example script: {example_script}")

    # Create example configuration
    config_file = config_dir / "config.example.json"
    config_content = {
        "default_version": "4.18",
        "max_token_limit": 380,
        "cache_dir": "./cache",
        "output_dir": "./vector_db",
        "model_dir": "./embeddings_model",
        "runbooks_dir": "./runbooks",
        "chunking_options": {
            "count_tag_tokens": True,
            "keep_siblings_together": True,
            "prepend_parent_section_text": True,
        },
    }

    import json

    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config_content, f, indent=2)

    print(f"Created example config: {config_file}")


def print_next_steps(validations: Dict[str, bool], base_dir: Path) -> None:
    """Print next steps for the user."""
    print("\nSETUP COMPLETE - NEXT STEPS")

    print("\n1. EMBEDDING MODEL")
    if not validations.get("embedding_model", False):
        print("   Download an embedding model to ./embeddings_model/")
        print("   Example: sentence-transformers/all-MiniLM-L6-v2")
        print("   Or run: python scripts/download_embeddings_model.py")
    else:
        print("   Embedding model detected")

    print("\n2. RUNBOOKS (optional)")
    if not validations.get("runbooks", False):
        print("   Get runbooks with: ./scripts/get_runbooks.sh")
        print("   Or skip with: --skip-runbooks")
    else:
        print("   Runbooks detected")

    print("\n3. RUN PIPELINE")
    print("   Basic usage:")
    print("   cd", base_dir)
    print("   python scripts/html_embeddings/generate_embeddings.py \\")
    print("     --version 4.18 \\")
    print("     --index ocp-4.18 \\")
    print("     --output-dir ./vector_db \\")
    print("     --model-dir ./embeddings_model")

    print("\n4. EXAMPLE SCRIPTS")
    print("   See: scripts/html_embeddings/run_example.sh")
    print("   See: scripts/html_embeddings/config.example.json")

    print("\n5. DOCUMENTATION")
    print("   Read: scripts/html_embeddings/README.md")

    print("\nTip: Use --use-cached-downloads for faster testing")
    print("Tip: Use --verbose for detailed logging")


def main():
    """Main setup function."""
    parser = argparse.ArgumentParser(description="Setup HTML embeddings pipeline")
    parser.add_argument(
        "--base-dir", default=".", help="Base directory (default: current)"
    )
    parser.add_argument(
        "--install-deps", action="store_true", help="Install missing dependencies"
    )
    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip existing component validation",
    )

    args = parser.parse_args()

    base_dir = Path(args.base_dir).resolve()
    print(f"Setting up HTML embeddings pipeline in: {base_dir}")

    print("\nCHECKING PYTHON VERSION")
    if not check_python_version():
        sys.exit(1)

    print("\nCHECKING DEPENDENCIES")
    installed, missing = check_dependencies()

    if missing:
        if args.install_deps:
            if not install_missing_packages(missing):
                print("Failed to install some dependencies. Please install manually.")
                sys.exit(1)
        else:
            print(f"\nMissing packages: {', '.join(missing)}")
            print("Run with --install-deps to install automatically")
            print("Or install manually with: pip install " + " ".join(missing))

    print("\nCREATING DIRECTORIES")
    directories = create_directory_structure(base_dir)

    print("\nVALIDATING COMPONENTS")
    if not args.skip_validation:
        validations = validate_existing_components(base_dir)
    else:
        validations = {}

    print("\nCREATING EXAMPLES")
    create_example_config(base_dir)

    # Print next steps
    print_next_steps(validations, base_dir)


if __name__ == "__main__":
    main()
