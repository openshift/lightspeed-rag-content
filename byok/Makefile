NUM_WORKERS ?= $$(( $(shell nproc --all) / 2))
ARTIFACT_DIR := $(if $(ARTIFACT_DIR),$(ARTIFACT_DIR),tests/test_results)

# Define arguments for pgvector support
POSTGRES_USER ?= postgres
POSTGRES_PASSWORD ?= somesecret
POSTGRES_HOST ?= localhost
POSTGRES_PORT ?= 15432
POSTGRES_DATABASE ?= postgres


.PHONY: unit-test
test-unit: ## Run the unit tests
	@echo "Running unit tests..."
	@echo "Reports will be written to ${ARTIFACT_DIR}"
	COVERAGE_FILE="${ARTIFACT_DIR}/.coverage.unit" uv run pytest tests --cov=src/lightspeed_rag_content --cov-report term-missing --cov-report "json:${ARTIFACT_DIR}/coverage_unit.json" --junit-xml="${ARTIFACT_DIR}/junit_unit.xml" --cov-fail-under=60

.PHONY: install-tools
install-tools: ## Install required utilities/tools
	@command -v uv > /dev/null || { echo >&2 "uv is not installed. Installing..."; pip3.12 install --upgrade pip uv; }

.PHONY: uv-lock-check
uv-lock-check: ## Check that the uv.lock file is in a good shape
	uv lock --check

.PHONY: install-global
install-global: install-tools ## Install ligthspeed-rag-content into file system.
	uv pip install --python 3.12 --system .

.PHONY: install-hooks
install-hooks: install-deps-test ## Install commit hooks
	uv pip install pre-commit

.PHONY: install-deps
install-deps: install-tools uv-lock-check ## Install all required dependencies, according to uv.lock
	uv sync
	uv export --no-emit-workspace --no-dev --no-annotate --no-header --output-file requirements.txt

.PHONY: install-deps-test
install-deps-test: install-tools uv-lock-check ## Install all required dev dependencies, according to uv.lock
	uv sync --dev

.PHONY: update-deps
update-deps: ## Check pyproject.toml for changes, update the lock file if needed, then sync.
	uv lock --upgrade
	uv sync
	uv sync --dev
	uv export --no-emit-workspace --no-dev --no-annotate --no-header --output-file requirements.txt

.PHONY: check-types
check-types: ## Check types in the code.
	@echo "Running $@ target ..."
	uv run mypy --namespace-packages --explicit-package-bases --strict --disallow-untyped-calls --disallow-untyped-defs --disallow-incomplete-defs src scripts

.PHONY: check-format
check-format: ## Check that the code is properly formatted using Black and Ruff formatter.
	@echo "Running $@ target ..."
	uv run black --check scripts src tests
	uv run ruff check scripts src

.PHONY: check-coverage
check-coverage: ## Check the coverage of unit tests.
	@echo "Running $@ target ..."
	uv run coverage run --source=src/lightspeed_rag_content -m unittest discover tests --verbose && uv run coverage report -m --fail-under 90

.PHONY: check-code-metrics
check-code-metrics: ## Check the code using Radon.
	@echo "Running $@ target ..."
	@OUTPUT=$$(uv run radon cc -a A src/ | tee /dev/tty | tail -1) && \
	GRADE=$$(echo $$OUTPUT | grep -oP " [A-F] " | tr -d '[:space:]') && \
	if [ "$$GRADE" = "A" ]; then exit 0; else exit 1; fi

.PHONY: format
format: ## Format the code into unified format
	uv run black scripts src tests
	uv run ruff check scripts src --fix
	uv run pre-commit run

black:
	uv tool run black --check .

pylint:
	uv run pylint src

ruff:
	uv run ruff check src

.PHONY: verify
verify: check-types check-format check-code-metrics check-coverage ## Verify the code using various linters

.PHONY: start-postgres
start-postgres: ## Start postgresql from the pgvector container image
	mkdir -pv ./postgresql/data ./output
	podman run -d --name pgvector --rm -e POSTGRES_PASSWORD=$(POSTGRES_PASSWORD) \
	 -p $(POSTGRES_PORT):5432 \
	 -v $(PWD)/postgresql/data:/var/lib/postgresql/data:Z pgvector/pgvector:pg16

.PHONY: start-postgres-debug
start-postgres-debug: ## Start postgresql from the pgvector container image with debugging enabled
	mkdir -pv ./postgresql/data ./output
	podman run --name pgvector --rm -e POSTGRES_PASSWORD=$(POSTGRES_PASSWORD) \
	 -p $(POSTGRES_PORT):5432 \
	 -v ./postgresql/data:/var/lib/postgresql/data:Z pgvector/pgvector:pg16 \
	 postgres -c log_statement=all -c log_destination=stderr

update-docs: ## Update the plaintext OCP docs in ocp-product-docs-plaintext/
	@set -e && for OCP_VERSION in $$(ls -1 ocp-product-docs-plaintext); do \
		scripts/get_ocp_plaintext_docs.sh $$OCP_VERSION; \
	done
	scripts/get_runbooks.sh

.PHONY: help
help: ## Show this help screen
	@echo 'Usage: make <OPTIONS> ... <TARGETS>'
	@echo ''
	@echo 'Available targets are:'
	@echo ''
	@grep -E '^[ a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'
	@echo ''
