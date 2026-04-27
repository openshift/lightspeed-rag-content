#!/bin/bash

# Split lockfiles for Konflux Cachi2 prefetch (PyPI source vs RHOAI wheels) from pyproject.toml.
# - Compile with uv (dual index + overrides), like openshift/lightspeed-service
# - Emit:
#   - requirements.hashes.source.<flavor>.txt, requirements.hashes.wheel.<flavor>.txt
#   - requirements-build.cpu.txt or lsc/requirements-build.txt (gpu reuses cpu build lockfile)
#   - update binary package lists in the matching .tekton PipelineRuns
#
# Flavors:
#   cpu  - root component CPU variant (cpu-ubi9 RHOAI index)   → lightspeed-rag-tool pipelines
#   gpu  - root component GPU variant (cuda12.9-ubi9 RHOAI index) → own-app pipelines
#   lsc  - LSC rag-content image (lsc/pyproject.toml, cpu-ubi9 index) → lightspeed-ocp-rag pipelines
#
# Usage: ./scripts/konflux_requirements.sh [cpu|gpu|lsc]

set -euo pipefail

FLAVOR="${1:-}"
if [[ "$FLAVOR" != "cpu" && "$FLAVOR" != "gpu" && "$FLAVOR" != "lsc" ]]; then
	echo "Usage: $0 {cpu|gpu|lsc}" >&2
	exit 1
fi

# Align with RHOAI wheels on packages.redhat.com (cp312 ubi9)
PY_VERSION="3.12"

case "$FLAVOR" in
cpu)
	RHOAI_INDEX_URL="https://packages.redhat.com/api/pypi/public-rhai/rhoai/3.3/cpu-ubi9/simple/"
	PYPROJECT="pyproject.toml"
	OVERRIDES="requirements.overrides.txt"
	EXTRA_OVERRIDES=""
	EXTRA_FLAVOR_ARG="--extra cpu"
	RAW_REQ_FILE="requirements.no_hashes.cpu.txt"
	SOURCE_FILE="requirements.source.cpu.txt"
	WHEEL_FILE="requirements.wheel.cpu.txt"
	SOURCE_HASH_FILE="requirements.hashes.source.cpu.txt"
	WHEEL_HASH_FILE="requirements.hashes.wheel.cpu.txt"
	BUILD_FILE="requirements-build.cpu.txt"
	PKG_FORCE_WHEEL="faiss-cpu numpy pandas scipy"
	SKIP_PYBUILD_PACKAGES="banks"
	# first-index: RHOAI wins for any package it carries; overrides pin the exact RHOAI versions
	INDEX_STRATEGY="first-index"
	;;
gpu)
	RHOAI_INDEX_URL="https://packages.redhat.com/api/pypi/public-rhai/rhoai/3.3/cuda12.9-ubi9/simple/"
	PYPROJECT="pyproject.toml"
	# GPU uses its own self-contained overrides: same as requirements.overrides.txt but torch==2.9.0
	# (RHOAI cuda12.9-ubi9 has torch==2.9.0; cpu-ubi9 has torch==2.9.1).
	OVERRIDES="requirements.overrides.gpu.txt"
	EXTRA_OVERRIDES=""
	EXTRA_FLAVOR_ARG="--extra gpu"
	RAW_REQ_FILE="requirements.no_hashes.gpu.txt"
	SOURCE_FILE="requirements.source.gpu.txt"
	WHEEL_FILE="requirements.wheel.gpu.txt"
	SOURCE_HASH_FILE="requirements.hashes.source.gpu.txt"
	WHEEL_HASH_FILE="requirements.hashes.wheel.gpu.txt"
	# Same root pyproject as cpu — Cachi2 build-deps prefetch uses requirements-build.cpu.txt (see own-app .tekton).
	PKG_FORCE_WHEEL="numpy pandas scipy"
	# GPU: faiss-cpu resolves from PyPI; pybuild-deps cannot use its sdist graph (meson) in this hermetic flow.
	SKIP_PYBUILD_PACKAGES="banks,faiss-cpu"
	INDEX_STRATEGY="first-index"
	;;
lsc)
	RHOAI_INDEX_URL="https://packages.redhat.com/api/pypi/public-rhai/rhoai/3.3/cpu-ubi9/simple/"
	PYPROJECT="lsc/pyproject.toml"
	OVERRIDES="lsc/requirements.overrides.txt"
	EXTRA_OVERRIDES=""
	EXTRA_FLAVOR_ARG=""
	RAW_REQ_FILE="lsc/requirements.no_hashes.txt"
	SOURCE_FILE="lsc/requirements.source.txt"
	WHEEL_FILE="lsc/requirements.wheel.txt"
	SOURCE_HASH_FILE="lsc/requirements.hashes.source.txt"
	WHEEL_HASH_FILE="lsc/requirements.hashes.wheel.txt"
	BUILD_FILE="lsc/requirements-build.txt"
	PKG_FORCE_WHEEL="faiss-cpu numpy pandas scipy"
	SKIP_PYBUILD_PACKAGES="banks"
	# unsafe-best-match: lsc/pyproject.toml has exact pins (llama-stack, pyyaml, etc.) that may differ
	# from RHOAI's modified versions. Overrides file still pins the RHOAI ML packages explicitly.
	INDEX_STRATEGY="unsafe-best-match"
	;;
esac

# extra wheels for Cachi2 binary prefetch (build helpers + wheels that should not duplicate in build lockfile)
EXTRA_WHEELS="uv,uv-build,pip,maturin,griffe,griffecli,griffelib"

# Wheel-only or C-extension PyPI packages: must appear in binary.packages so Cachi2 fetches
# the pre-built wheel rather than attempting a source build (which would need unprefetched build deps).
# These packages stay in the source requirements file but are whitelisted here for Cachi2.
if [[ "$FLAVOR" == "lsc" ]]; then
	# sqlite-vec: wheel-only on PyPI (no sdist exists)
	# cryptography: not on RHOAI index; requires Rust to build from source
	# All remaining pure-Python and C-extension packages that resolve from PyPI (not on RHOAI cpu-ubi9
	# for LSC) have both wheel+sdist. Without binary.packages Cachi2 fetches the sdist; pip then needs
	# build backends (hatchling, flit_core, setuptools+wheel, etc.) that are not prefetched.
	# List every such package from lsc/requirements.hashes.source.txt here.
	EXTRA_WHEELS="${EXTRA_WHEELS},sqlite-vec,cryptography,banks,chardet,charset-normalizer,click,dirtyjson,fastapi,filelock,fsspec,googleapis-common-protos,greenlet,idna,llama-index,llama-index-core,llama-index-embeddings-huggingface,llama-index-embeddings-openai,llama-index-instrumentation,llama-index-llms-openai,llama-index-readers-file,llama-index-vector-stores-faiss,llama-index-vector-stores-postgres,llama-index-workflows,llama-stack,llama-stack-api,llama-stack-client,nltk,openai,opentelemetry-api,opentelemetry-exporter-otlp-proto-common,opentelemetry-exporter-otlp-proto-http,opentelemetry-proto,opentelemetry-sdk,opentelemetry-semantic-conventions,packaging,pgvector,platformdirs,protobuf,psycopg2-binary,pyaml,pydantic,pygments,pyjwt,pypdf,python-dotenv,python-multipart,pytz,pyyaml,regex,requests,rich,sentence-transformers,soupsieve,sqlalchemy,starlette,striprtf,tenacity,tinytag,tornado,typer,typer-slim,tzdata,uvicorn,wcwidth,wrapt,zipp"
elif [[ "$FLAVOR" == "gpu" ]]; then
	# faiss-cpu: not on RHOAI GPU (cuda12.9) index; C extension, needs cmake/wheel to build from sdist.
	# Pure Python packages below are also not on the RHOAI cuda12.9 index (unlike cpu-ubi9 which carries
	# them). They resolve from PyPI and have both wheel+sdist; without binary.packages Cachi2 fetches
	# the sdist. Building from sdist requires build backends (flit_core, hatchling, etc.) that are not
	# prefetched. List every pure-Python PyPI package from requirements.hashes.source.gpu.txt here so
	# Cachi2 fetches the wheel instead.
	EXTRA_WHEELS="${EXTRA_WHEELS},faiss-cpu,aiosqlite,banks,dirtyjson,llama-index-core,llama-index-embeddings-huggingface,llama-index-instrumentation,llama-index-readers-file,llama-index-vector-stores-faiss,llama-index-workflows,pypdf,python-frontmatter,striprtf,tinytag"
fi
NO_WHEEL_PACKAGES="markupsafe"

# filtered source file for pybuild-deps to avoid RecursionError
SOURCE_FILE_FOR_BUILD=$(mktemp)

extract_pkg_name() {
	# e.g. "foo==1" -> foo; "foo @ https://..." -> foo
	local line="$1"
	local s="${line%%@*}"
	s="${s%%=*}"
	s="${s// /}"
	echo "$s" | tr '[:upper:]' '[:lower:]'
}

cleanup() {
	rm -f "$RAW_REQ_FILE" "$WHEEL_FILE" "$SOURCE_FILE" "$SOURCE_FILE_FOR_BUILD"
}
trap cleanup EXIT INT TERM

# --- 1) Compile unhashed, annotated with index origin (torch and other RHOAI wheels from the flavor index).
# cpu/gpu use first-index so RHOAI wins for any package it carries.
# lsc uses unsafe-best-match because lsc/pyproject.toml has exact pins (llama-stack, pyyaml…) that
# differ from RHOAI's modified versions; overrides.txt still anchors the RHOAI ML wheels explicitly.
# Build --override flags: always include OVERRIDES; append EXTRA_OVERRIDES if set (GPU shadow-overrides).
OVERRIDE_ARGS="--override ${OVERRIDES}"
[[ -n "${EXTRA_OVERRIDES:-}" ]] && OVERRIDE_ARGS="${OVERRIDE_ARGS} --override ${EXTRA_OVERRIDES}"

# shellcheck disable=SC2086
uv pip compile "$PYPROJECT" -o "$RAW_REQ_FILE" \
	--python-platform x86_64-unknown-linux-gnu \
	--python-version "$PY_VERSION" \
	$EXTRA_FLAVOR_ARG \
	--refresh \
	--index "${RHOAI_INDEX_URL}" \
	--default-index https://pypi.org/simple/ \
	--index-strategy "${INDEX_STRATEGY}" \
	--emit-index-annotation \
	--no-sources \
	$OVERRIDE_ARGS

echo "# Packages from pypi.org" >"$SOURCE_FILE"
echo "# This file was autogenerated by $(basename -- "$0")" >>"$SOURCE_FILE"
echo "# Packages from ${RHOAI_INDEX_URL}" >"$WHEEL_FILE"
echo "# This file was autogenerated by $(basename -- "$0")" >>"$WHEEL_FILE"
echo "--index-url ${RHOAI_INDEX_URL}" >>"$WHEEL_FILE"

# --- 2) Split by index origin (see lightspeed-service) + flush orphan top-level lines (e.g. URL pins)
current_package=""

while IFS= read -r line || [[ -n "$line" ]]; do
	if [[ "$line" =~ ^[a-zA-Z0-9] ]]; then
		if [[ -n "$current_package" ]]; then
			echo "$current_package" >>"$SOURCE_FILE"
		fi
		current_package="$line"
	elif [[ "$line" =~ ^[[:space:]]*#[[:space:]]*from[[:space:]]+(.*) ]]; then
		index_url="${BASH_REMATCH[1]}"
		if [[ -n "$current_package" ]]; then
			package_name="$(extract_pkg_name "$current_package")"
			force_no_wheel=0
			for no_wheel_pkg in ${NO_WHEEL_PACKAGES//,/ }; do
				[[ "$package_name" == "$no_wheel_pkg" ]] && force_no_wheel=1 && break
			done
			if [[ "$index_url" == "https://pypi.org/simple/" ]]; then
				echo "$current_package" >>"$SOURCE_FILE"
			elif [[ "$force_no_wheel" -eq 1 ]]; then
				echo "$current_package" >>"$SOURCE_FILE"
			elif [[ "$index_url" == "${RHOAI_INDEX_URL}" ]]; then
				echo "$current_package" >>"$WHEEL_FILE"
			else
				echo "$current_package" >>"$SOURCE_FILE"
			fi
			current_package=""
		fi
	fi
done <"$RAW_REQ_FILE"
if [[ -n "$current_package" ]]; then
	echo "$current_package" >>"$SOURCE_FILE"
fi

# uv can annotate these on PyPI; for Konflux (and pybuild-deps) prefer RHOAI wheels when that index carries them.
for p in $PKG_FORCE_WHEEL; do
	tmpf=$(mktemp)
	while IFS= read -r pline; do
		case "$pline" in
		${p}==* | ${p}\ @\ *) echo "$pline" >>"$WHEEL_FILE" ;;
		*) echo "$pline" >>"$tmpf" ;;
		esac
	done <"$SOURCE_FILE"
	mv "$tmpf" "$SOURCE_FILE"
done

wheel_packages=$(grep -v "^[#-]" "$WHEEL_FILE" | sed 's/==.*//;s/[[:space:]]*@.*//' | awk 'NF' | tr '\n' ',' | sed 's/,$//')
echo "WHEEL_PACKAGE_NAMES: $wheel_packages" >&1

# --- 3) Hash lockfiles
# --universal and --python-platform are mutually exclusive in uv; RHOAI wheels are linux+cp312-specific here
uv pip compile "$WHEEL_FILE" --refresh --generate-hashes --index-url "${RHOAI_INDEX_URL}" \
	--python-version "$PY_VERSION" --python-platform x86_64-unknown-linux-gnu \
	--emit-index-url --no-deps --no-annotate >"$WHEEL_HASH_FILE"
uv pip compile "$SOURCE_FILE" --refresh --generate-hashes --python-version "$PY_VERSION" \
	--python-platform x86_64-unknown-linux-gnu \
	--emit-index-url --no-deps --no-annotate >"$SOURCE_HASH_FILE"

# --- 4) Drop extra wheels from source (they are only listed as binaries)
for pkg in ${EXTRA_WHEELS//,/ }; do
	pkg=$(echo "$pkg" | tr -d '[:space:]')
	[[ -n "$pkg" ]] && sed -i "/^${pkg}[=<>!~@]/d" "$SOURCE_FILE"
done

# Build deps: pybuild-deps, with optional banks → hatchling workaround
{
	grep -v "^[#-]" "$SOURCE_FILE" | while IFS= read -r bline; do
		[[ -z "$bline" ]] && continue
		pkg_name="${bline%%@*}"; pkg_name="${pkg_name%%=*}"; pkg_name="${pkg_name// /}"
		skip=0
		for skip_pkg in ${SKIP_PYBUILD_PACKAGES//,/ }; do
			skip_pkg=$(echo "$skip_pkg" | tr -d '[:space:]' | tr '[:upper:]' '[:lower:]')
			[[ -n "$skip_pkg" ]] && [[ $(echo "$pkg_name" | tr '[:upper:]' '[:lower:]') == "$skip_pkg" ]] && skip=1 && break
		done
		[[ $skip -eq 0 ]] && echo "$bline"
	done
	if [[ "$SKIP_PYBUILD_PACKAGES" == *"banks"* ]] && grep -qE '^banks' "$SOURCE_FILE" 2>/dev/null; then
		echo "hatchling==1.29.0"
	fi
} >>"$SOURCE_FILE_FOR_BUILD"

# --- 4b) Build-deps lockfile (cpu + lsc only). GPU uses the same root pyproject build graph as cpu;
# own-app pipelines prefetch requirements-build.cpu.txt to avoid an empty duplicate requirements-build.gpu.txt.
if [[ "$FLAVOR" == "gpu" ]]; then
	echo "Skipping pybuild-deps for gpu (prefetch uses requirements-build.cpu.txt)."
else
	# Treat pybuild-deps failures as non-fatal (it chokes on some sdist graphs, e.g. meson-based packages).
	if ! uv run --no-project --with "pybuild-deps>=0.5" pybuild-deps compile --output-file="$BUILD_FILE" "$SOURCE_FILE_FOR_BUILD"; then
		echo "WARNING: pybuild-deps failed — $BUILD_FILE not generated" >&2
		: >"$BUILD_FILE"
	fi

	# --- 5) Do not list wheel deps twice in build file
	IFS=,
	for pkg in $wheel_packages; do
		pkg=$(echo "$pkg" | tr -d '[:space:]' | tr '[:upper:]' '[:lower:]')
		[[ -z "$pkg" ]] && continue
		sed -i "/^${pkg}[=<>!~@]/d" "$BUILD_FILE" 2>/dev/null || true
	done
	unset IFS
fi

# --- 6) Sync pip.binary.packages in prefetch-input (same sed as openshift/lightspeed-service).
# Requires a one-line JSON value containing "packages": "comma,separated,names".
for extra in ${EXTRA_WHEELS//,/ }; do
	extra=$(echo "$extra" | tr -d '[:space:]')
	[[ -n "$extra" ]] && wheel_packages="${wheel_packages:+$wheel_packages,}$extra"
done

update_prefetch_binary_packages() {
	local tf="$1"
	[[ -f "$tf" ]] || return 0
	if grep -q '"packages": "[^"]*"' "$tf"; then
		sed -i 's/"packages": "[^"]*"/"packages": "'"$wheel_packages"'"/' "$tf"
		echo "  updated pip.binary.packages: $tf"
	else
		echo "  skip (no matching \"packages\" string): $tf" >&2
	fi
}

case "$FLAVOR" in
cpu)
	for tf in \
		.tekton/lightspeed-rag-tool-pull-request.yaml \
		.tekton/lightspeed-rag-tool-push.yaml \
		.konflux/lightspeed-rag-tool-pull-request.yaml \
		.konflux/lightspeed-rag-tool-push.yaml; do
		update_prefetch_binary_packages "$tf"
	done
	;;
gpu)
	for tf in \
		.tekton/own-app-lightspeed-rag-content-pull-request.yaml \
		.tekton/own-app-lightspeed-rag-content-push.yaml \
		.konflux/own-app-lightspeed-rag-content-pull-request.yaml \
		.konflux/own-app-lightspeed-rag-content-push.yaml; do
		update_prefetch_binary_packages "$tf"
	done
	;;
lsc)
	for tf in \
		.tekton/lightspeed-ocp-rag-pull-request.yaml \
		.tekton/lightspeed-ocp-rag-push.yaml; do
		update_prefetch_binary_packages "$tf"
	done
	;;
esac

echo "Done for flavor: $FLAVOR"
echo "  $SOURCE_HASH_FILE  ($(grep -c -v '^#' <"$SOURCE_HASH_FILE" 2>/dev/null || true) non-comment lines; hash lines vary)"
echo "  $WHEEL_HASH_FILE"
if [[ "$FLAVOR" != "gpu" ]]; then
	echo "  $BUILD_FILE"
else
	echo "  (build-deps: requirements-build.cpu.txt — run cpu flavor first or \`make update-konflux-deps\`)"
fi
echo "  pip.binary.packages value: $wheel_packages"
echo "Commit these, requirements.overrides*, and any updated PipelineRun YAML under .tekton/ (and .konflux/ if used)."
