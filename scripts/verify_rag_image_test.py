import os

versions = ["4.15", "4.16", "4.17", "4.18"]

if __name__ == "__main__":
    for version in versions:
        path = f"/rag/vector_db/ocp_product_docs/{version}/index_store.json"
        assert os.path.isfile(path)

        path = "/rag/embeddings_model/config.json"
        assert os.path.isfile(path)
    print("Success")
