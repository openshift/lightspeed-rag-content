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

install-tools: ## Install required utilities/tools
	@command -v pdm > /dev/null || { echo >&2 "pdm is not installed. Installing..."; pip3.11 install --no-cache-dir --upgrade pip pdm; }

pdm-lock-check: ## Check that the pdm.lock file is in a good shape
	pdm lock --check --group cpu --lockfile pdm.lock.cpu
	pdm lock --check --group gpu --lockfile pdm.lock.gpu

install-deps: install-tools pdm-lock-check ## Install all required dependencies, according to pdm.lock
	pdm sync --group $(TORCH_GROUP) --lockfile pdm.lock.$(TORCH_GROUP)

install-deps-test: install-tools pdm-lock-check ## Install all required dev dependencies, according to pdm.lock
	pdm sync --dev --group $(TORCH_GROUP) --lockfile pdm.lock.$(TORCH_GROUP)

update-deps: ## Check pyproject.toml for changes, update the lock file if needed, then sync.
	pdm install --group $(TORCH_GROUP) --lockfile pdm.lock.$(TORCH_GROUP)
	pdm install --dev --group $(TORCH_GROUP) --lockfile pdm.lock.$(TORCH_GROUP)
	pdm export --group $(TORCH_GROUP) --lockfile pdm.lock.$(TORCH_GROUP) -o requirements.$(TORCH_GROUP).txt

check-types: ## Checks type hints in sources
	mypy --explicit-package-bases --disallow-untyped-calls --disallow-untyped-defs --disallow-incomplete-defs scripts

format: ## Format the code into unified format
	black scripts
	ruff check scripts --fix --per-file-ignores=scripts/*:S101

verify: ## Verify the code using various linters
	black --check scripts
	ruff check scripts --per-file-ignores=scripts/*:S101

update-docs: ## Update the plaintext OCP docs in ocp-product-docs-plaintext/
	@set -e && for OCP_VERSION in $$(ls -1 ocp-product-docs-plaintext); do \
		scripts/get_ocp_plaintext_docs.sh $$OCP_VERSION; \
	done
	scripts/get_runbooks.sh

update-model: ## Update the local copy of the embedding model
	@rm -rf ./embeddings_model
	@python scripts/download_embeddings_model.py -l ./embeddings_model -r ibm-granite/granite-embedding-125m-english

build-image: ## Build a rag-content container image.
	podman build -t rag-content .

help: ## Show this help screen
	@echo 'Usage: make <OPTIONS> ... <TARGETS>'
	@echo ''
	@echo 'Available targets are:'
	@echo ''
	@grep -E '^[ a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'
	@echo ''
