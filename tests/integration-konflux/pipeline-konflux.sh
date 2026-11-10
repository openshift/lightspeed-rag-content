#!/usr/bin/env bash
# BYOK customer-workflow e2e test for the Go tool.
#
# Exercises the shipped tool image end-to-end:
#   1. Run the tool's default CMD on a fictional markdown corpus
#   2. Load the output container image archive with podman
#   3. Extract /rag/vector_db and assert metadata fields
#   4. Start the real OLS service with the extracted index
#   5. Send a query that can only be answered from the corpus
#   6. Assert the answer contains the recovery phrase and correct citation
#
# Adapted from the Python tool's e2e test: no fuse, no registry credentials,
# no nested builds — the Go tool needs none of those.
set -euo pipefail
umask 077

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
: "${BYOK_TOOL_IMAGE:?Set BYOK_TOOL_IMAGE to the product image under test}"
: "${OLS_SERVICE_IMAGE:?Set OLS_SERVICE_IMAGE to a digest-pinned OLS service image}"
: "${OPENAI_API_KEY:?Set OPENAI_API_KEY for real inference}"

ARTIFACT_DIR="${ARTIFACT_DIR:-$(mktemp -d /tmp/byok-test-artifacts.XXXXXX)}"
mkdir -p "$ARTIFACT_DIR"
ARTIFACT_DIR="$(cd "$ARTIFACT_DIR" && pwd)"
echo "[byok-e2e] Artifacts: $ARTIFACT_DIR"
WORK_DIR="$(mktemp -d)"
RUN_ID="byok-e2e-$(basename "$WORK_DIR" | tr '[:upper:]' '[:lower:]')"
TOOL_CONTAINER="$RUN_ID-tool"
SERVICE_CONTAINER="$RUN_ID-service"
OUTPUT_CONTAINER="$RUN_ID-output"
OUT_IMAGE_TAG="$RUN_ID"
OUTPUT_IMAGE="localhost/$OUT_IMAGE_TAG:latest"

cleanup() {
    local status=$?
    trap - EXIT
    for name in "$TOOL_CONTAINER" "$SERVICE_CONTAINER"; do
        podman logs "$name" > "$ARTIFACT_DIR/$name.log" 2>&1 || true
    done
    podman rm -f "$TOOL_CONTAINER" "$SERVICE_CONTAINER" "$OUTPUT_CONTAINER" >/dev/null 2>&1 || true
    podman rmi "$OUTPUT_IMAGE" >/dev/null 2>&1 || true
    podman unshare rm -rf "$WORK_DIR" 2>/dev/null || rm -rf "$WORK_DIR"
    exit "$status"
}
trap cleanup EXIT

mkdir -p "$WORK_DIR/output" "$WORK_DIR/index" "$WORK_DIR/credentials" "$WORK_DIR/markdown"
cp "$SCRIPT_DIR/corpus/manual.md" "$WORK_DIR/markdown/"
printf %s "$OPENAI_API_KEY" > "$WORK_DIR/credentials/openai-api-key"
chmod 755 "$WORK_DIR" "$WORK_DIR/credentials"
podman unshare chown 1001:0 "$WORK_DIR/credentials/openai-api-key" 2>/dev/null \
    || chown 1001:0 "$WORK_DIR/credentials/openai-api-key"
podman unshare chmod 400 "$WORK_DIR/credentials/openai-api-key" 2>/dev/null \
    || chmod 400 "$WORK_DIR/credentials/openai-api-key"

# ---------------------------------------------------------------------------
# 1. Run the tool's default CMD on the corpus
#    (no fuse, no registry, no auth — the Go tool needs none of those)
# ---------------------------------------------------------------------------
echo "[byok-e2e] Running default CMD: $BYOK_TOOL_IMAGE"
podman pull "$BYOK_TOOL_IMAGE"
# --network=host: netavark cannot create a network namespace inside the
# nested container in the Konflux VM (setns: Operation not permitted)
podman run --name "$TOOL_CONTAINER" --network=host \
    -v "$WORK_DIR/markdown:/markdown" \
    -v "$WORK_DIR/output:/output" \
    -e OUT_IMAGE_TAG="$OUT_IMAGE_TAG" \
    -e VECTOR_DB_INDEX=byok-e2e-index \
    "$BYOK_TOOL_IMAGE" 2>&1 | tee "$ARTIFACT_DIR/build.log"

# ---------------------------------------------------------------------------
# 2. Load the output container image archive
# ---------------------------------------------------------------------------
ARCHIVE="$WORK_DIR/output/$OUT_IMAGE_TAG.tar"
test -s "$ARCHIVE"
echo "[byok-e2e] Loading the customer image archive"
podman load -i "$ARCHIVE" | tee "$ARTIFACT_DIR/load.log"

# ---------------------------------------------------------------------------
# 3. Extract and validate /rag/vector_db
# ---------------------------------------------------------------------------
podman create --name "$OUTPUT_CONTAINER" "$OUTPUT_IMAGE" /bin/true >/dev/null
podman cp "$OUTPUT_CONTAINER:/rag/vector_db/." "$WORK_DIR/index"
podman unshare chmod -R a+rX "$WORK_DIR/index" 2>/dev/null || chmod -R a+rX "$WORK_DIR/index"
for file in default__vector_store.json docstore.json index_store.json metadata.json; do
    test -s "$WORK_DIR/index/$file"
done
jq -e '
    .["index-id"] == "byok-e2e-index" and
    .["embedding-dimension"] == 768 and
    .["total-embedded-files"] == 1 and
    .["vector-db"] == "faiss.IndexFlatIP"
' "$WORK_DIR/index/metadata.json" >/dev/null || {
    echo "[byok-e2e] metadata.json has unexpected content:" >&2
    cat "$WORK_DIR/index/metadata.json" >&2
    exit 1
}
cp "$WORK_DIR/index/metadata.json" "$ARTIFACT_DIR/metadata.json"

# ---------------------------------------------------------------------------
# 4. Start the real OLS service with the extracted index
# ---------------------------------------------------------------------------
echo "[byok-e2e] Starting OLS with the index extracted from the archive"
podman pull "$OLS_SERVICE_IMAGE"
podman run -d --name "$SERVICE_CONTAINER" --network=host \
    --security-opt label=disable \
    -v "$WORK_DIR/index:/rag/vector_db:ro" \
    -v "$WORK_DIR/credentials:/credentials:ro" \
    -v "$SCRIPT_DIR/config/olsconfig.yaml:/app-root/olsconfig.yaml:ro" \
    -e OLS_CONFIG_FILE=/app-root/olsconfig.yaml \
    -e OTEL_SDK_DISABLED=true \
    "$OLS_SERVICE_IMAGE" >/dev/null

READY=false
for _ in $(seq 1 60); do
    if [[ "$(podman inspect --format '{{.State.Running}}' "$SERVICE_CONTAINER")" != true ]]; then
        echo "[byok-e2e] OLS exited before readiness" >&2
        exit 1
    fi
    if curl --fail --silent --max-time 5 http://127.0.0.1:18080/readiness >/dev/null; then
        READY=true
        break
    fi
    sleep 5
done
[[ "$READY" == true ]] || { echo "[byok-e2e] OLS readiness timed out" >&2; exit 1; }

# ---------------------------------------------------------------------------
# 5. Ask a question that can only be answered from the BYOK corpus
# ---------------------------------------------------------------------------
echo "[byok-e2e] Asking for a fact absent from the question and training knowledge"
HTTP_CODE="$(curl --silent --show-error --max-time 180 \
    -o "$ARTIFACT_DIR/response.json" -w '%{http_code}' \
    -H 'Content-Type: application/json' \
    -d '{"query":"Our Zyranex T7 relay controller deployment on OpenShift reports ZRX-4401. According to our internal runbook, what exact recovery phrase must the operator enter before restarting the deployment?"}' \
    http://127.0.0.1:18080/v1/query)"
[[ "$HTTP_CODE" == 200 ]] || { echo "[byok-e2e] Query returned HTTP $HTTP_CODE" >&2; exit 1; }

# ---------------------------------------------------------------------------
# 6. Assert the answer contains the recovery phrase and correct citation
# ---------------------------------------------------------------------------
jq -e '
    (.response | type == "string") and
    (.response | ascii_downcase | contains("orbital-mango-731")) and
    ([.referenced_documents[]? |
        select(.doc_title == "Zyranex T7 OpenShift Runbook" and
               .doc_url == "https://docs.quorbitex.example.com/openshift/zyranex-t7")] | length > 0)
' "$ARTIFACT_DIR/response.json" >/dev/null || {
    echo "[byok-e2e] Answer is missing the recovery phrase or the expected citation:" >&2
    cat "$ARTIFACT_DIR/response.json" >&2
    exit 1
}
echo "[byok-e2e] Customer BYOK workflow passed"
