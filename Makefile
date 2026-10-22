LINT_PYTHON := scripts/konflux_resolve.py scripts/generate_embeddings.py scripts/download_embeddings_model.py byok/generate_embeddings_tool.py tests/unit tests/integration-konflux/validate_response.py

install-tools: ## Verify uv; Python 3.12 is provisioned by uv
	@command -v uv > /dev/null || { echo >&2 "uv is not installed. Install: https://docs.astral.sh/uv/"; exit 1; }

.venv:
	uv venv -p 3.12

install-deps: install-tools .venv ## Install app dependencies (matches pyproject extra)
	uv pip install --python .venv/bin/python -e ".[cpu]"

install-deps-test: install-tools .venv ## Install with dev tools (Ruff, mypy, etc.)
	uv pip install --python .venv/bin/python -e ".[cpu]" black mypy ruff "types-requests"

# Host uv provisions tooling only. Compilation uses the forked prefer-index image.
.PHONY: bump update-konflux-deps
bump: install-tools ## Refresh dependencies, or target PKG=<name> VERSION=<minimum>
	@if { [ -n "$(PKG)" ] && [ -z "$(VERSION)" ]; } || { [ -z "$(PKG)" ] && [ -n "$(VERSION)" ]; }; then \
		echo 'Supply PKG and VERSION together: make bump PKG=<name> VERSION=<minimum>' >&2; exit 2; \
	fi
	env -u UV_CONFIG_FILE -u UV_INDEX_URL -u UV_DEFAULT_INDEX -u UV_INDEX \
		-u UV_EXTRA_INDEX_URL -u PIP_INDEX_URL -u PIP_EXTRA_INDEX_URL \
		UV_NO_CONFIG=1 PIP_CONFIG_FILE=/dev/null \
		uv run --no-project --python 3.12 --with packaging --with tomlkit \
		--with pybuild-deps --with pip-tools --with pip \
		python scripts/konflux_resolve.py --profile cpu \
		$(if $(PKG),--package "$(PKG)" --version "$(VERSION)")

update-konflux-deps: bump ## Compatibility alias for make bump

# Regenerate rpms.lock.yaml (subscription + rpm-lockfile-prototype / Konflux tooling; not scripted in-repo).
update-rpm-lock:
	@echo "From repo root, with Red Hat repo auth configured, run your org's rpm-lock workflow, e.g.:"
	@echo "  rpm-lockfile-prototype rpms.in.yaml --outfile rpms.lock.yaml"
	@echo "Adjust paths if you maintain a separate lockfile."

test-unit: ## Run runtime, dependency-tooling, and integration-harness regression tests
	uv run --no-project --python 3.12 --with pyyaml --with packaging --with tomlkit python -m unittest discover -s tests/unit -v

.PHONY: test-resolver-image
test-resolver-image: ## Include real forked-uv prefer-index resolution tests (requires Podman/Docker)
	OLS_TEST_RESOLVER_IMAGE=1 $(MAKE) test-unit

check-types: install-tools .venv ## Checks type hints in sources
	.venv/bin/mypy --explicit-package-bases --disallow-untyped-calls --disallow-untyped-defs --disallow-incomplete-defs scripts

format: install-tools .venv
	.venv/bin/black $(LINT_PYTHON)
	.venv/bin/ruff check $(LINT_PYTHON) --fix --extend-per-file-ignores=scripts/*:S101,byok/*:S101

verify: install-tools .venv
	.venv/bin/black --check $(LINT_PYTHON)
	.venv/bin/ruff check $(LINT_PYTHON) --extend-per-file-ignores=scripts/*:S101,byok/*:S101

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
