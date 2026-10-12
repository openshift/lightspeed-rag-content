#!/usr/bin/env bash
set -euo pipefail
umask 077

: "${RESULTS_TEST_OUTPUT_PATH:?Missing Tekton result path}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
SSH_ARGS=(-o StrictHostKeyChecking=no -o ServerAliveInterval=60 -o ServerAliveCountMax=10)
LOCAL_WORK="$(mktemp -d)"
REMOTE_DIR=""
SSH_HOST=""
IS_LOCALHOST=false

finish() {
    local status=$?
    trap - EXIT
    local result=FAILURE successes=0 failures=1 warnings=0
    if [[ -n "$REMOTE_DIR" ]]; then
        if [[ "$IS_LOCALHOST" == true ]]; then
            if ! cp -r "$REMOTE_DIR/artifacts" /var/workdir/artifacts; then
                echo "WARNING: Could not retain VM artifacts" >&2
                warnings=$((warnings + 1))
            fi
            if ! rm -rf "$REMOTE_DIR"; then
                echo "ERROR: VM credential cleanup could not be confirmed" >&2
                warnings=$((warnings + 1))
                status=1
            fi
        elif [[ -n "$SSH_HOST" ]]; then
            if ! rsync -r -e "ssh ${SSH_ARGS[*]}" "$SSH_HOST:$REMOTE_DIR/artifacts/" /var/workdir/artifacts/; then
                echo "WARNING: Could not retrieve VM artifacts" >&2
                warnings=$((warnings + 1))
            fi
            if ! ssh "${SSH_ARGS[@]}" "$SSH_HOST" bash -s -- "$REMOTE_DIR" <<'CLEANUP'
rm -rf -- "$1"
CLEANUP
            then
                echo "ERROR: Remote credential cleanup could not be confirmed" >&2
                warnings=$((warnings + 1))
                status=1
            fi
        fi
    fi
    if ! rm -rf "$LOCAL_WORK"; then
        echo "ERROR: Local credential cleanup could not be confirmed" >&2
        warnings=$((warnings + 1))
        status=1
    fi
    if [[ "$status" == 0 ]]; then
        result=SUCCESS successes=1 failures=0
    fi
    jq -jn --arg result "$result" --arg timestamp "$(date -u +%FT%TZ)" \
        --argjson successes "$successes" --argjson failures "$failures" --argjson warnings "$warnings" \
        '{result: $result, timestamp: $timestamp, successes: $successes, failures: $failures, warnings: $warnings}' \
        | tee "$RESULTS_TEST_OUTPUT_PATH"
    exit "$status"
}
trap finish EXIT

merge_registry_auth() {
    local output="$1"
    shift
    : > "$output"
    chmod 600 "$output"
    jq -se '
        if all(.[]; (.auths | type == "object") and (.auths | length > 0)) then
            {auths: (reduce .[] as $config ({}; . + $config.auths))}
        else
            error("Registry configurations must contain nonempty auths objects")
        end
    ' "$@" > "$output"
}

for image in "$BYOK_TOOL_IMAGE" "$OLS_SERVICE_IMAGE" "$UBI_BASE_IMAGE"; do
    [[ "$image" =~ ^[^[:space:]]+@sha256:[a-f0-9]{64}$ ]] || { echo "Image must be digest-pinned: $image" >&2; exit 1; }
done
[[ -r /var/run/openai/token ]] || { echo "Missing token key in OpenAI secret" >&2; exit 1; }
[[ -r /var/run/quay-auth/.dockerconfigjson ]] || { echo "Missing openshift-lightspeed registry config" >&2; exit 1; }
[[ -r /var/run/redhat-auth/.dockerconfigjson ]] || { echo "Missing registry-redhat-io registry config" >&2; exit 1; }
if [[ -e /ssh/error ]]; then
    echo "Konflux VM provisioning failed" >&2
    exit 1
fi
SSH_HOST="$(< /ssh/host)"
if [[ "$SSH_HOST" == localhost ]]; then
    IS_LOCALHOST=true
elif [[ -s /ssh/otp ]]; then
    mkdir -p "$HOME/.ssh"
    curl --fail --silent --show-error --cacert /ssh/otp-ca -d @/ssh/otp "$(< /ssh/otp-server)" > "$HOME/.ssh/id_rsa"
    printf '\n' >> "$HOME/.ssh/id_rsa"
    chmod 600 "$HOME/.ssh/id_rsa"
elif [[ -s /ssh/id_rsa ]]; then
    mkdir -p "$HOME/.ssh"
    cp /ssh/id_rsa "$HOME/.ssh/id_rsa"
    chmod 600 "$HOME/.ssh/id_rsa"
else
    echo "No VM SSH authentication mechanism found" >&2
    exit 1
fi

mkdir -p "$LOCAL_WORK/tests" "$LOCAL_WORK/credentials"
cp -r "$REPO_ROOT/tests/integration-konflux" "$LOCAL_WORK/tests/"
chmod -R a+rX "$LOCAL_WORK/tests"
cp /var/run/openai/token "$LOCAL_WORK/credentials/openai-api-key"
merge_registry_auth "$LOCAL_WORK/credentials/auth.json" \
    /var/run/quay-auth/.dockerconfigjson /var/run/redhat-auth/.dockerconfigjson
chmod 600 "$LOCAL_WORK/credentials/"*
for name in BYOK_TOOL_IMAGE OLS_SERVICE_IMAGE UBI_BASE_IMAGE; do
    printf '%s=%q\n' "$name" "${!name}" >> "$LOCAL_WORK/images.env"
done
cat > "$LOCAL_WORK/run.sh" <<'RUN'
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
set -a
source images.env
set +a
mkdir -p artifacts
podman run --rm --privileged --network=host \
    --security-opt label=disable --security-opt seccomp=unconfined \
    -v "$PWD/tests:/tests:ro" \
    -v "$PWD/credentials:/credentials:ro" \
    -v "$PWD/artifacts:/artifacts" \
    -e BYOK_TOOL_IMAGE -e OLS_SERVICE_IMAGE -e UBI_BASE_IMAGE \
    -e REGISTRY_AUTH_FILE=/credentials/auth.json \
    -e ARTIFACT_DIR=/artifacts -e STORAGE_DRIVER=vfs \
    registry.access.redhat.com/ubi9/ubi:latest \
    bash -c 'set -euo pipefail; dnf -y install podman fuse-overlayfs python3 curl-minimal;
      export OPENAI_API_KEY="$(< /credentials/openai-api-key)";
      bash /tests/integration-konflux/pipeline-konflux.sh' \
    2>&1 | tee artifacts/workflow.log
RUN
chmod 700 "$LOCAL_WORK/run.sh"

if [[ "$IS_LOCALHOST" == true ]]; then
    REMOTE_DIR="$(mktemp -d)"
    cp -r "$LOCAL_WORK/." "$REMOTE_DIR/"
    bash "$REMOTE_DIR/run.sh"
else
    BUILD_DIR="$(< /ssh/user-dir)"
    [[ "$BUILD_DIR" =~ ^/[a-zA-Z0-9_./-]+$ ]] || { echo "Invalid VM working directory" >&2; exit 1; }
    REMOTE_DIR="$BUILD_DIR/byok-$(basename "$LOCAL_WORK")"
    ssh "${SSH_ARGS[@]}" "$SSH_HOST" bash -s -- "$REMOTE_DIR" <<'PREPARE'
mkdir -m 700 "$1"
PREPARE
    rsync -r -e "ssh ${SSH_ARGS[*]}" "$LOCAL_WORK/" "$SSH_HOST:$REMOTE_DIR/"
    ssh "${SSH_ARGS[@]}" "$SSH_HOST" bash -s -- "$REMOTE_DIR" <<'RUN_REMOTE'
bash "$1/run.sh"
RUN_REMOTE
fi
