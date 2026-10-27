# =============================================================================
# lightspeed-rag-content (Go) — Makefile
# =============================================================================
# BYOK RAG tool: markdown → mpnet/ONNX → FAISS → docker-archive.
# Follows the patterns of lightspeed-hub and lightspeed-operator.
# =============================================================================

BINARY ?= byok-go
IMG ?= byok-tool-go:latest
CONTAINER_TOOL ?= $(shell which podman >/dev/null 2>&1 && echo podman || echo docker)

.PHONY: all
all: build

# -----------------------------------------------------------------------------
# Build
# -----------------------------------------------------------------------------

.PHONY: build
build: ## Build the byok-go binary (stages native libs first)
	eval "$$(scripts/stage-go-native.sh)" && \
		CGO_ENABLED=1 go build -o $(BINARY) ./cmd/byok-go

.PHONY: build-dev
build-dev: ## Build the dev helper binary
	eval "$$(scripts/stage-go-native.sh)" && \
		CGO_ENABLED=1 go build -o byok-go-dev ./cmd/byok-go-dev

.PHONY: build-image
build-image: ## Build the container image from vendored artifacts
	$(CONTAINER_TOOL) build -t $(IMG) -f Containerfile .

# -----------------------------------------------------------------------------
# Test
# -----------------------------------------------------------------------------

# Pure-Go packages (no native libraries needed)
PURE_PKGS := $(shell go list ./internal/... 2>/dev/null | grep -vE "embed|faissidx")

.PHONY: test
test: ## Run pure-Go unit tests (no native libraries needed)
	CGO_ENABLED=0 go test $(PURE_PKGS) && \
		test -z "$$(gofmt -l . | grep -v vendor)"

.PHONY: test-native
test-native: ## Run all tests incl. cgo packages (stage native libs first)
	eval "$$(scripts/stage-go-native.sh)" && go test ./...

# -----------------------------------------------------------------------------
# Lint
# -----------------------------------------------------------------------------

.PHONY: lint
lint: ## Check formatting and vet
	gofmt -l . | grep -v vendor | tee /dev/stderr | grep -q . && exit 1 || true
	go vet $(PURE_PKGS) 2>/dev/null || true

.PHONY: format
format: ## Format all Go source
	gofmt -w $(shell find . -name "*.go" -not -path "./vendor/*")

# -----------------------------------------------------------------------------
# Model chunks
# -----------------------------------------------------------------------------

.PHONY: model-chunks
model-chunks: ## Regenerate model/ chunks from a local mpnet.onnx (MODEL=...)
	@test -n "$$(MODEL)" || { echo "usage: make model-chunks MODEL=/path/to/mpnet.onnx"; exit 1; }
	cd model && rm -f mpnet.onnx.gz.* mpnet.onnx.sha256 && \
		sha256sum "$$(MODEL)" | awk '{print $$1"  mpnet.onnx"}' > mpnet.onnx.sha256 && \
		gzip -c "$$(MODEL)" | split -b 90m - mpnet.onnx.gz. && echo "chunks regenerated"

# -----------------------------------------------------------------------------
# Clean
# -----------------------------------------------------------------------------

.PHONY: clean
clean: ## Remove build artifacts
	rm -f $(BINARY) byok-go-dev
	rm -rf .byok-go-native

.PHONY: test-e2e
test-e2e: ## Run the customer-workflow e2e test (requires tool + service images + OpenAI key)
	@test -n "$$(BYOK_TOOL_IMAGE)" || { echo "Set BYOK_TOOL_IMAGE to the tool image"; exit 1; }
	@test -n "$$(OLS_SERVICE_IMAGE)" || { echo "Set OLS_SERVICE_IMAGE to the service image"; exit 1; }
	@test -n "$$(OPENAI_API_KEY)" || { echo "Set OPENAI_API_KEY"; exit 1; }
	ARTIFACT_DIR=/tmp/byok-e2e-artifacts bash tests/integration-konflux/pipeline-konflux.sh
