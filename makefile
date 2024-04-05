install-tools: ## Install required utilities/tools
	@command -v pdm > /dev/null || { echo >&2 "pdm is not installed. Installing..."; pip install pdm; }

pdm-lock-check: ## Check that the pdm.lock file is in a good shape
	pdm lock --check

install-deps: install-tools pdm-lock-check ## Install all required dependencies, according to pdm.lock
	pdm sync

install-deps-test: install-tools pdm-lock-check ## Install all required dev dependencies, according to pdm.lock
	pdm sync --dev

update-deps: ## Check pyproject.toml for changes, update the lock file if needed, then sync.
	pdm install
	pdm install --dev

check-types: ## Checks type hints in sources
	mypy --explicit-package-bases --disallow-untyped-calls --disallow-untyped-defs --disallow-incomplete-defs scripts

format: ## Format the code into unified format
	black scripts
	ruff check scripts --fix --per-file-ignores=scripts/*:S101

verify: ## Verify the code using various linters
	black --check scripts
	ruff check scripts --per-file-ignores=scripts/*:S101

update-ocp-docs: ## Update the plaintext OCP docs in ocp-product-docs-plaintext/
	scripts/get_ocp_plaintext_docs.sh 4.15

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
