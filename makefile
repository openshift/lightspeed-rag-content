VERSION := latest
IMAGE_REPO := quay.io/redhat_emp1
EMBEDDING_MODEL := sentence-transformers/all-mpnet-base-v2

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
	@set -e && for OCP_VERSION in $$(ls -1 ocp-product-docs-plaintext); do \
		scripts/get_ocp_plaintext_docs.sh $$OCP_VERSION; \
	done

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

build-tekton-test:
	podman build -f "Containerfile.tekton" -t rag-pipeline-tasks:test . 
	podman tag  rag-pipeline-tasks:${VERSION} ${IMAGE_REPO}/rag-pipeline-tasks:test 
	podman push ${IMAGE_REPO}/rag-pipeline-tasks:test 

build-tekton-lateast: 
	podman build --arch=x86_64 -f "Containerfile.tekton" -t rag-pipeline-tasks:${VERSION} . 
	podman tag  rag-pipeline-tasks:${VERSION} ${IMAGE_REPO}/rag-pipeline-tasks:${VERSION} 
	podman push ${IMAGE_REPO}/rag-pipeline-tasks:${VERSION} 

local-dev-env: 
	python scripts/download_embeddings_model.py -l ./embeddings_model -r ${EMBEDDING_MODEL}

test-generate-embeddings: 
	podman run --env-file=.env -v  ./persist-dir:/workdir/output localhost/rag-pipeline-tasks:latest python generate_embeddings.py \
																						-f ocp-product-docs-plaintext/4.15 \
																						-md embeddings_model \
																						-o /workdir/output \
																						-mn sentence-transformers/all-mpnet-base-v2 \
																						-v 4.15
																						

test-generate-embeddings-folders: 
	podman run --env-file=.env -v ./output:/workdir/output localhost/rag-pipeline-tasks:latest python generate_embeddings.py \
																						-fo 'ocp-product-docs-plaintext/4.15 ocp-product-docs-plaintext/4.16'\
																						-md embeddings_model \
																						-mn sentence-transformers/all-mpnet-base-v2 \
																						-o /workdir/output

test-evaluation: 
	podman run -v ./output:/workdir/output localhost/rag-pipeline-tasks:latest python evaluation.py \
	                                                                                    -p bam\
																						-i /workdir/output/4.15 \
																						-x 4_15 \
																						-m ibm/granite-13b-chat-v2 \
																						-lq questions/openai-gpt-3.5-turbo_no_eval.json \
																						-o /workdir/output \
																						-n 5
