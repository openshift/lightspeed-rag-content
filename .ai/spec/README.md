# OpenShift LightSpeed RAG Content -- Specifications

These specs define the requirements, behaviors, and architecture for the lightspeed-rag-content project. They are organized into two layers:

## Structure

| Layer | Path | Purpose |
|---|---|---|
| **what/** | `.ai/spec/what/` | Behavioral rules. What the system must do. Implementation-agnostic. |
| **how/** | `.ai/spec/how/` | Codebase navigation. How the code is organized. Implementation-specific. |

### what/ -- Behavioral Specifications

These specs define WHAT the RAG content pipeline must do -- testable behavioral rules, configuration surface, constraints, and planned changes. They are technology-neutral where possible and survive a complete rewrite in a different framework.

| Spec | Description |
|------|-------------|
| [system-overview.md](what/system-overview.md) | Project purpose, boundaries, integration contract with lightspeed-service |
| [content-sources.md](what/content-sources.md) | OCP docs, runbooks, OKP content -- acquisition, versioning, metadata, exclusions |
| [embedding-pipeline.md](what/embedding-pipeline.md) | Shared behavioral rules for all pipeline variants: chunking, embedding, vector store output, index organization |
| [byok.md](what/byok.md) | Bring Your Own Knowledge -- customer content import via tool container |
| [container-build.md](what/container-build.md) | Container images, hermetic builds, CI/CD pipelines, dependency management |

### how/ -- Architecture Specifications

These specs describe HOW the RAG content pipeline is structured -- module boundaries, data flow, design patterns, key abstractions, and implementation decisions. They are grounded in the current Python codebase and should be updated when the code changes.

| Spec | Description |
|------|-------------|
| [project-structure.md](how/project-structure.md) | Directory layout, module map, dependency management, key relationships |
| [plaintext-pipeline.md](how/plaintext-pipeline.md) | `scripts/generate_embeddings.py` -- the production pipeline used by the Containerfile |
| [html-pipeline.md](how/html-pipeline.md) | `scripts/html_embeddings/` + `scripts/html_chunking/` -- HTML-based pipeline with semantic chunking |
| [lsc-library.md](how/lsc-library.md) | `lsc/src/lightspeed_rag_content/` -- installable library with multi-backend support |
| [container-build.md](how/container-build.md) | Containerfiles, Makefile targets, Konflux/Tekton pipelines, dependency management |

## Scope

These specs cover the **lightspeed-rag-content** project only -- the offline pipeline that produces pre-built vector indexes and packages them as container images. The lightspeed-service (which consumes these artifacts at runtime), the operator, and the console plugin are separate projects.

## Audience

AI agents (Claude). Specs optimize for precision, unambiguous rules, and machine-parseable structure.

## Quick Start

| I want to... | Read |
|--------------|------|
| Understand what this project does | `what/system-overview.md` |
| Understand content sources and acquisition | `what/content-sources.md` |
| Understand the embedding pipeline rules | `what/embedding-pipeline.md` |
| Understand BYOK (customer content) | `what/byok.md` |
| Understand the container build process | `what/container-build.md` |
| Navigate the codebase | `how/project-structure.md` |
| Modify the plaintext pipeline | `how/plaintext-pipeline.md` |
| Modify the HTML pipeline | `how/html-pipeline.md` |
| Modify the lsc library | `how/lsc-library.md` |
| Modify the container build or CI | `how/container-build.md` |
| See what's planned | Look for `[PLANNED: OLS-XXXX]` in `what/` specs |

## Cross-Reference

When what/ and how/ file names don't match 1:1, this table maps behavioral specs to their implementation guides:

| what/ | how/ |
|---|---|
| `what/system-overview.md` | `how/project-structure.md` |
| `what/content-sources.md` | `how/plaintext-pipeline.md`, `how/html-pipeline.md`, `how/lsc-library.md` |
| `what/embedding-pipeline.md` | `how/plaintext-pipeline.md`, `how/html-pipeline.md`, `how/lsc-library.md` |
| `what/byok.md` | `how/container-build.md` (BYOK Containerfile sections) |
| `what/container-build.md` | `how/container-build.md` |

## Conventions

- **Rule numbering:** behavioral rules are numbered sequentially within each what/ file.
- **Planned changes:** unimplemented behavior is marked with `[PLANNED]` or `[PLANNED: OLS-XXXX]` inline next to the rule it affects. "Planned Changes" sections list new capabilities not yet in code.
- **Constraints:** component-specific and cross-cutting constraints go in the relevant what/ file's Constraints section, co-located with behavioral rules. Development conventions go in CLAUDE.md.
- **Authority:** what/ specs are authoritative for behavior. how/ specs are authoritative for implementation. When they conflict, what/ wins.
- **When to create a new file vs. extend an existing one:** if the new concern has its own lifecycle, configuration surface, and can be understood independently, it gets its own file. If it's a capability added to an existing component, it goes in that component's file.
- User-configurable values are referenced by CLI argument name or environment variable name.
- Internal constants are stated as behavioral rules without numeric values; `how/` specs may include specific values.

## Relationship to lightspeed-service

This project produces artifacts consumed by lightspeed-service. The service's `what/rag.md` spec describes how it loads and queries these indexes at runtime. This project's specs describe how the indexes are built. The integration contract is documented in `what/system-overview.md`.
