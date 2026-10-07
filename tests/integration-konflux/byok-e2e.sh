#!/usr/bin/env bash
# Run on a Konflux-provisioned Podman VM, against the image in the PR snapshot.
set -euo pipefail

TOOL_IMAGE=${1:?Usage: byok-e2e.sh TOOL_IMAGE}
command -v podman >/dev/null || { echo 'Podman is required on the test VM' >&2; exit 1; }

work=$(mktemp -d "${HOME}/byok-e2e.XXXXXX")
cid=
cleanup() {
    if [ -n "$cid" ]; then podman rm "$cid" >/dev/null 2>&1 || true; fi
    podman unshare rm -rf "$work" 2>/dev/null || rm -rf "$work" 2>/dev/null || true
}
trap cleanup EXIT
mkdir -p "$work/markdown" "$work/output"
printf '# BYOK integration test\n\nOpenShift Lightspeed sample content.\n' > "$work/markdown/sample.md"

podman pull "$TOOL_IMAGE"

# Use the tested snapshot image for BOTH the outer tool and its builder stage.
# Do not use a floating :latest tag or skip the default nested Buildah path.
# /dev/fuse and SELinux mounts match the documented customer invocation.
podman run --rm --pull=never --device=/dev/fuse \
    -e BYOK_TOOL_IMAGE="$TOOL_IMAGE" \
    -e STORAGE_DRIVER=vfs \
    -e HF_HUB_OFFLINE=1 \
    -v "$work/markdown:/markdown:ro,Z" \
    -v "$work/output:/output:Z" \
    "$TOOL_IMAGE"

archive="$work/output/byok-image.tar"
test -s "$archive"
podman load -i "$archive"

# Validate the *loaded output image*, not just a file left in the tool image.
# The output is data-only: it is read by the OLS service, which owns the model.
podman run --rm --entrypoint /bin/sh localhost/byok-image:latest -c '
    test -s /rag/vector_db/default__vector_store.json &&
    test -s /rag/vector_db/metadata.json &&
    test -s /rag/vector_db/docstore.json &&
    test -s /rag/vector_db/index_store.json &&
    grep -q '"index-id": "vector_db_index"' /rag/vector_db/metadata.json &&
    grep -q '"total-embedded-files": 1' /rag/vector_db/metadata.json
'
# The output image is intentionally data-only. Copy the index out and check it
# with the same FAISS library used by the builder, not just its file size.
cid=$(podman create localhost/byok-image:latest)
podman cp "$cid:/rag/vector_db/default__vector_store.json" "$work/faiss.index"
podman rm "$cid" >/dev/null
cid=
podman run --rm --pull=never \
    -v "$work/faiss.index:/tmp/index:ro,Z" \
    --entrypoint python3.12 "$TOOL_IMAGE" \
    -c 'import faiss; assert faiss.read_index("/tmp/index").ntotal > 0'
echo 'BYOK tool created a loadable image with a populated FAISS index'
