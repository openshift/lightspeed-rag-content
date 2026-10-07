"""Exercise the BYOK embedding CLI in the tool image's default Python environment.

Run in the Containerfile (release gate), or on a published image with:
    podman run --rm --entrypoint python3.12 IMAGE smoke_tool.py
"""

import json
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

import faiss

if __name__ == "__main__":
    if sys.prefix != "/opt/app-root":
        raise RuntimeError(
            f"Expected the RHOAI runtime Python, got {sys.executable} ({sys.prefix})"
        )

    with TemporaryDirectory() as directory:
        root = Path(directory)
        markdown = root / "markdown"
        markdown.mkdir()
        (markdown / "sample.md").write_text(
            "# Smoke test\n\nOpenShift Lightspeed BYOK indexing.\n"
        )
        output = root / "vector_db"

        subprocess.run(  # noqa: S603 - fixed script path and arguments, no shell
            [
                sys.executable,
                str(Path(__file__).with_name("generate_embeddings_tool.py")),
                "-i",
                str(markdown),
                "-emd",
                str(Path(__file__).with_name("embeddings_model")),
                "-emn",
                "sentence-transformers/all-mpnet-base-v2",
                "-o",
                "vector_db",
                "-id",
                "vector_db_index",
            ],
            check=True,
            cwd=root,
        )
        metadata = json.loads((output / "metadata.json").read_text())
        if (
            metadata["index-id"] != "vector_db_index"
            or metadata["total-embedded-files"] != 1
        ):
            raise RuntimeError(f"Unexpected index metadata: {metadata}")
        for filename in ("docstore.json", "index_store.json", "graph_store.json"):
            if not (output / filename).is_file():
                raise RuntimeError(f"Missing {filename}")
        vector_store = output / "default__vector_store.json"
        if not vector_store.is_file() or faiss.read_index(str(vector_store)).ntotal < 1:
            raise RuntimeError("FAISS vector store missing or empty")
        print("BYOK embedding smoke test passed")
