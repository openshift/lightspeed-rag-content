# Default to CPU if not specified
FLAVOR ?= cpu

# Define behavior based on the flavor
ifeq ($(FLAVOR),cpu)
TORCH_GROUP := cpu
else ifeq ($(FLAVOR),gpu)
TORCH_GROUP := gpu
else
$(error Unsupported FLAVOR $(FLAVOR), must be 'cpu' or 'gpu')
endif

install-tools: ## Install uv (Python 3.12) for local development
	@command -v uv > /dev/null || { echo >&2 "uv is not installed. Install: https://docs.astral.sh/uv/"; exit 1; }
	@command -v python3.12 > /dev/null || { echo >&2 "Python 3.12 is required."; exit 1; }

.venv:
	uv venv -p 3.12

install-deps: install-tools .venv ## Install app dependencies (matches pyproject extra)
	uv pip install --python .venv/bin/python -e ".[$(TORCH_GROUP)]"

install-deps-test: install-tools .venv ## Install with dev tools (Ruff, mypy, etc.)
	uv pip install --python .venv/bin/python -e ".[$(TORCH_GROUP)]" black mypy ruff "types-requests"

# Regenerate Cachi2/Konflux lockfiles; commit outputs + update .tekton `binary.packages` if the wheel set changes
update-konflux-deps: install-tools
	./scripts/konflux_requirements.sh cpu
	./scripts/konflux_requirements.sh gpu
	@echo "If pip.binary packages changed, update the prefetch block in the matching .tekton/* files"
	@echo "Note: gpu flavor reuses requirements-build.cpu.txt; cpu must run before gpu in this target."

update-konflux-deps-lsc: install-tools ## Regenerate RHOAI-sourced hermetic requirements for the LSC component
	./scripts/konflux_requirements.sh lsc

# Regenerate rpms.lock.yaml (subscription + rpm-lockfile-prototype / Konflux tooling; not scripted in-repo).
update-rpm-lock:
	@echo "From repo root, with Red Hat repo auth configured, run your org's rpm-lock workflow, e.g.:"
	@echo "  rpm-lockfile-prototype rpms.in.yaml --outfile rpms.lock.yaml"
	@echo "Adjust paths if you maintain a separate lockfile (e.g. lsc/rpms.in.yaml)."

check-types: install-tools .venv ## Checks type hints in sources
	.venv/bin/mypy --explicit-package-bases --disallow-untyped-calls --disallow-untyped-defs --disallow-incomplete-defs scripts

format: install-tools .venv
	.venv/bin/black scripts
	.venv/bin/ruff check scripts --fix --per-file-ignores=scripts/*:S101

verify: install-tools .venv
	.venv/bin/black --check scripts
	.venv/bin/ruff check scripts --per-file-ignores=scripts/*:S101

update-docs: ## Update the plaintext OCP docs in ocp-product-docs-plaintext/
	@set -e && for OCP_VERSION in $$(ls -1 ocp-product-docs-plaintext); do \
		scripts/get_ocp_plaintext_docs.sh $$OCP_VERSION; \
	done
	scripts/get_runbooks.sh

update-model: install-tools .venv ## Update the local copy of the embedding model
	@rm -rf ./embeddings_model
	@.venv/bin/python scripts/download_embeddings_model.py -l ./embeddings_model -r sentence-transformers/all-mpnet-base-v2

build-image: ## Build a rag-content container image
	podman build -t rag-content .

help: ## Show this help screen
	@echo 'Usage: make <OPTIONS> ... <TARGETS>'
	@echo ''
	@echo 'Available targets are:'
	@echo ''
	@grep -E '^[ a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'
	@echo ''
	
model-safetensors: ## Download model.safetensors to embeddings_model
	@if [ ! -f embeddings_model/model.safetensors ]; then \
		echo "Downloading model.safetensors..."; \
		wget "https://huggingface.co/sentence-transformers/all-mpnet-base-v2/resolve/9a3225965996d404b775526de6dbfe85d3368642/model.safetensors" -O embeddings_model/model.safetensors; \
	else \
		echo "model.safetensors already exists. Skipping download."; \
	fi
