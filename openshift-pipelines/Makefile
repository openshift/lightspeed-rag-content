.ONESHELL:
.DELETE_ON_ERROR:
.SHELLFLAGS := -eu -o pipefail -c
SHELL := bash
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules
MAKEFLAGS += --no-print-directory

DOC_SLUG ?= "red_hat_openshift_pipelines"
DOC_VERSION ?= "1.20"
IMAGE_CMD ?= "podman"
IMAGE_WITH_TAG ?= "openshift-pipelines-rag-byok:latest"

##@ Commands
.PHONY: help
help: ## Display this help.
	@awk 'BEGIN {
		FS = ":.*##";
		printf "\nUsage:\n  make \033[36m<target>\033[0m\n"
	}
	/^[a-zA-Z_0-9-]+:.*?##/ {
		printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2
	}
	/^##@/ {
		printf "\n\033[1m%s\033[0m\n", substr($$0, 5)
	}' $(MAKEFILE_LIST)

.PHONY: setup-env
setup-env: ## Installs python environment and required python packages into a virtual env
	@uv python install 3.11
	@uv venv --python 3.11
	@uv pip install -r ../requirements.cpu.txt

.PHONY: download-docs
download-docs: ## Downloads openshift-pipelines docs into 'openshift-pipelines' folder corresponding to the version and preps them
	@pushd ..

	@mkdir -p openshift-pipelines/${DOC_SLUG}/${DOC_VERSION}/downloads/

	@python3.11 scripts/doc_downloader/downloader.py \
	--doc-url "https://docs.redhat.com/en/documentation/${DOC_SLUG}/${DOC_VERSION}/" \
	--output-dir openshift-pipelines/${DOC_SLUG}/${DOC_VERSION}/downloads/ \
	--max-retries 1

	@find openshift-pipelines/${DOC_SLUG}/${DOC_VERSION}/downloads/html-single -empty -type d -delete
	@find openshift-pipelines/${DOC_SLUG}/${DOC_VERSION}/downloads/html-single -not -name index.html -type f -delete

	@find openshift-pipelines/${DOC_SLUG}/${DOC_VERSION}/downloads/html -type f -delete
	@find openshift-pipelines/${DOC_SLUG}/${DOC_VERSION}/downloads/html -empty -type d -delete

	@mv openshift-pipelines/${DOC_SLUG}/${DOC_VERSION}/downloads/html-single/* openshift-pipelines/${DOC_SLUG}/${DOC_VERSION}/downloads/

	@popd

.PHONY: create-rag
create-rag: ## Creates vector db based on cached downloads
	@pushd ..

	@if test -d openshift-pipelines/${DOC_SLUG}/${DOC_VERSION}/chunks; then
		@find openshift-pipelines/${DOC_SLUG}/${DOC_VERSION}/chunks -type f -delete
		@find openshift-pipelines/${DOC_SLUG}/${DOC_VERSION}/chunks -empty -type d -delete
	fi

	@if test -d openshift-pipelines/${DOC_SLUG}/${DOC_VERSION}/stripped; then
		@find openshift-pipelines/${DOC_SLUG}/${DOC_VERSION}/stripped -type f -delete
		@find openshift-pipelines/${DOC_SLUG}/${DOC_VERSION}/stripped -empty -type d -delete
	fi

	@python3.11 scripts/html_embeddings/generate_embeddings.py \
	--doc-url-version ${DOC_VERSION} \
	--doc-url-slug ${DOC_SLUG} \
	--output-dir vector_db \
	--index vector_db_index \
	--skip-runbooks \
	--use-cached-downloads \
	--cache-dir openshift-pipelines/ \
	--verbose
	@popd

.PHONY: build-openshift-pipelines-rag
build-openshift-pipelines-rag: ## Builds a container with openshift-pipelines RAG content
	@pushd ..
	@${IMAGE_CMD} build -f openshift-pipelines/Containerfile -t ${IMAGE_WITH_TAG} .
	@popd
