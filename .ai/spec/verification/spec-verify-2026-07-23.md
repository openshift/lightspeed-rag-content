# Verification Report: lightspeed-rag-content Spec
Verified: 2026-07-23
Spec root: /Users/xavi/street/github.com/AI/ols/lightspeed-rag-content/.ai/spec/

## Summary
- 2 broken or inaccurate internal references
- 1 internal inconsistency
- 1 completeness gap
- 0 cross-repo alignment issues

## Reference Issues

1. **`README.md` references `what/rag.md` ambiguously.**
Line 84: "The service's `what/rag.md` spec describes how it loads and queries these indexes at runtime." The file exists in lightspeed-service, but the reference doesn't specify the repo. A reader could look for `what/rag.md` in this repo's spec directory and find nothing. Should say "lightspeed-service's `what/rag.md`". Also note: the parent OLS spec calls this file `rag-pipeline.md`, adding to the naming confusion.

2. **`how/container-build.md:135` shows wrong base image for BYOK tool container.**
The spec shows `FROM ubi9/ubi:latest` as the base image for the BYOK tool container. The actual `byok/Containerfile.tool` uses `FROM ${UBI_BASE_IMAGE}` where `UBI_BASE_IMAGE` defaults to `registry.redhat.io/rhai/base-image-cpu-rhel9:3.3`. The `ubi9/ubi:latest` default is from `Containerfile.output` (the output template), not the tool container.

## Internal Inconsistencies

1. **`UBI_BASE_IMAGE` default conflation in `what/byok.md`.**
`byok.md` line 34 documents `UBI_BASE_IMAGE` with default `registry.access.redhat.com/ubi9/ubi:latest` and describes it as "Base image for the output container" in the Tool Container env vars table. But `Containerfile.tool` also has its own `UBI_BASE_IMAGE` ARG defaulting to `registry.redhat.io/rhai/base-image-cpu-rhel9:3.3` — a different value for the tool container's own base. The spec conflates two different uses of the same variable name.

## Completeness Gaps

1. **No `constraints.md` or `glossary.md`.**
Terms like OKP, RHOKP, BYOK, Cachi2, Konflux, Mintmaker, and PDM are used throughout without definitions. Minor gap since each term is introduced in context, but a glossary would help for AI/new-contributor readers.

## Cross-Repo Alignment Issues

None. The parent OLS spec (`rag-pipeline.md`) is correctly aligned:
- "lightspeed-rag-content: BYOK tool image only. Main RAG content image deprecated." ✓
- BYOK flow (FAISS indexes from Markdown, `sentence-transformers/all-mpnet-base-v2`, mount paths) ✓
- Embedding model for BYOK (768-dim) ✓
- BYOK filesystem paths (`/rag/vector_db/{index_name}/`, `/rag/embeddings_model/`) ✓
- Planned changes (OLS-2704, OLS-1872) referenced consistently ✓

## Files Checked

### what/
- system-overview.md, byok.md, container-build.md, content-sources.md, embedding-pipeline.md

### how/
- project-structure.md, plaintext-pipeline.md, html-pipeline.md, lsc-library.md, container-build.md

### Other
- README.md, decisions/README.md (empty), health-report.md (last evaluated 2026-05-29, all prior issues resolved)
- No constraints.md or glossary.md

### Codebase cross-checks (existence verified)
- byok/Containerfile.tool, byok/Containerfile.output, byok/generate_embeddings_tool.py
- scripts/generate_embeddings.py, scripts/html_chunking/chunker.py, scripts/html_embeddings/generate_embeddings.py
- lsc/Containerfile.konflux, lsc/src/lightspeed_rag_content/{document,metadata}_processor.py, lsc/src/lightspeed_rag_content/okp.py
- .tekton/ (6 pipeline files + integration test directory)
- ocp-product-docs-plaintext/ (versions 4.16-4.22 present)

### Cross-repo
- /Users/xavi/street/github.com/AI/ols/.ai/spec/what/rag-pipeline.md
- /Users/xavi/street/github.com/AI/ols/lightspeed-service/.ai/spec/what/rag.md (exists, confirms README target is valid)
