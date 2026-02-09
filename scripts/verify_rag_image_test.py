import os
from pathlib import Path

versions = [p.name for p in Path("ocp-product-docs-plaintext").iterdir() if p.is_dir()]

if __name__ == "__main__":
    for version in versions:
        path = f"/rag/vector_db/ocp_product_docs/{version}/index_store.json"
        assert os.path.isfile(path)

        path = "/rag/embeddings_model/config.json"
        assert os.path.isfile(path)
    print("Success")
