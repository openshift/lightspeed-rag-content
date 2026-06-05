#!/usr/bin/env bash
# Generate RAG vector DB on a GPU host and export rag/ for multi-arch packaging.
# Mirrors the lightspeed-rag-builder stage in Containerfile (Konflux embed-rag task).
set -euo pipefail

cd /var/workdir/source

EMBEDDING_MODEL="${EMBEDDING_MODEL:-sentence-transformers/all-mpnet-base-v2}"
HERMETIC="${HERMETIC:-true}"
FLAVOR="${FLAVOR:-gpu}"
RAG_EXPORT_DIR="${RAG_EXPORT_DIR:-/var/workdir/source/rag-export}"
CACHI2_ROOT="${CACHI2_ROOT:-/cachi2}"

if [ "${HERMETIC}" = "true" ] && [ -f "${CACHI2_ROOT}/cachi2.env" ]; then
  # shellcheck disable=SC1091
  source "${CACHI2_ROOT}/cachi2.env"
fi

if [ "${FLAVOR}" != "gpu" ]; then
  echo "embed-rag-content requires FLAVOR=gpu" >&2
  exit 1
fi

pip3.12 install --no-cache-dir -r requirements.gpu.txt
ln -sf /usr/local/lib/python3.12/site-packages/llama_index/core/_static/nltk_cache /root/nltk_data

cd embeddings_model
if [ "${HERMETIC}" = "true" ]; then
  cp "${CACHI2_ROOT}/output/deps/generic/model.safetensors" model.safetensors
else
  curl -L -O "https://huggingface.co/sentence-transformers/all-mpnet-base-v2/resolve/9a3225965996d404b775526de6dbfe85d3368642/model.safetensors"
fi
cd ..

python3.12 -c "import torch; print('cuda', torch.version.cuda, torch.cuda.is_available())"

for OCP_VERSION in $(ls -1 ocp-product-docs-plaintext); do
  python3.12 scripts/generate_embeddings.py \
    -f "ocp-product-docs-plaintext/${OCP_VERSION}" \
    -r runbooks/alerts \
    -md embeddings_model \
    -mn "${EMBEDDING_MODEL}" \
    -o "vector_db/ocp_product_docs/${OCP_VERSION}" \
    -i "ocp-product-docs-$(echo "${OCP_VERSION}" | sed 's/\./_/g')" \
    -v "${OCP_VERSION}" \
    -hb "${HERMETIC}"
done

LATEST_VERSION=$(ls -1 vector_db/ocp_product_docs/ | sort -V | tail -n 1)
ln -sf "${LATEST_VERSION}" "vector_db/ocp_product_docs/latest"

rm -rf "${RAG_EXPORT_DIR}"
mkdir -p "${RAG_EXPORT_DIR}/rag"
cp -a vector_db "${RAG_EXPORT_DIR}/rag/"
cp -a embeddings_model "${RAG_EXPORT_DIR}/rag/"
cp LICENSE "${RAG_EXPORT_DIR}/"
cp Containerfile.arm64 "${RAG_EXPORT_DIR}/"

test -d "${RAG_EXPORT_DIR}/rag/vector_db/ocp_product_docs"
test -d "${RAG_EXPORT_DIR}/rag/embeddings_model"
test -f "${RAG_EXPORT_DIR}/LICENSE"
test -f "${RAG_EXPORT_DIR}/Containerfile.arm64"
