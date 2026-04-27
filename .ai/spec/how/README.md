# Architecture Specifications (how/)

These specs describe HOW the RAG content pipeline is structured -- module boundaries, data flow, design patterns, key abstractions, and implementation decisions. They are grounded in the current Python codebase and should be updated when the code changes.

## Spec Index

| Spec | Description |
|------|-------------|
| [project-structure.md](project-structure.md) | Directory layout, module map, dependency management, key relationships |
| [plaintext-pipeline.md](plaintext-pipeline.md) | `scripts/generate_embeddings.py` -- the production pipeline used by the Containerfile |
| [html-pipeline.md](html-pipeline.md) | `scripts/html_embeddings/` + `scripts/html_chunking/` -- HTML-based pipeline with semantic chunking |
| [lsc-library.md](lsc-library.md) | `lsc/src/lightspeed_rag_content/` -- installable library with multi-backend support |
| [container-build.md](container-build.md) | Containerfiles, Makefile targets, Konflux/Tekton pipelines, dependency management |

## When to Read These

- **Navigating the codebase**: Start with `project-structure.md` to understand where things live.
- **Modifying a pipeline**: Read the relevant pipeline spec to understand the current architecture before making changes.
- **Adding a new vector store backend**: Read `lsc-library.md` for the `_BaseDB` extension pattern.
- **Debugging**: The data flow sections trace the exact path documents take through the pipeline.
- **Changing the build**: Read `container-build.md` for Containerfile stages and Konflux pipeline structure.

## Relationship to what/ Specs

The [`what/` specs](../what/README.md) define behavioral contracts (technology-neutral). These `how/` specs describe the implementation that fulfills those contracts. When the two diverge, the `what/` spec is the source of truth for correct behavior, and the `how/` spec should be updated to reflect the current code.
