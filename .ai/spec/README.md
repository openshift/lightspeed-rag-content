# OpenShift Lightspeed RAG Content (Go) — Specifications

These specs define the requirements, behaviors, and architecture for the
lightspeed-rag-content project: the Go BYOK RAG tool. They are organized in
two layers:

## Structure

| Layer | Path | Purpose |
|---|---|---|
| **what/** | `.ai/spec/what/` | Behavioral rules. What the system must do. Implementation-agnostic. |
| **how/** | `.ai/spec/how/` | Codebase navigation. How the code is organized. Implementation-specific. |

### what/ — Behavioral Specifications

| Spec | Description |
|------|-------------|
| [system-overview.md](what/system-overview.md) | Project purpose, boundaries, integration contract with lightspeed-service |
| [byok.md](what/byok.md) | BYOK tool behavior — input handling, output artifact, configuration surface |
| [embedding-pipeline.md](what/embedding-pipeline.md) | Chunking, embedding, vector store output, output-image format |
| [container-build.md](what/container-build.md) | Tool container image, hermetic builds, CI/CD pipelines, dependency management |

### how/ — Architecture Specifications

| Spec | Description |
|------|-------------|
| [project-structure.md](how/project-structure.md) | Directory layout, package map, key relationships |
| [byok-pipeline.md](how/byok-pipeline.md) | End-to-end data flow through the internal packages |
| [container-build.md](how/container-build.md) | Containerfile stages, native library builds, model packaging, Makefile targets |

### decisions/ — Architecture Decision Records

`decisions/` holds lightweight ADRs recording notable architectural
decisions. Each file follows the `NNNN-slug.md` naming convention. See
[decisions/README.md](decisions/README.md).

## Scope

These specs cover the **lightspeed-rag-content** project only — the BYOK
tool that generates FAISS vector indexes from customer-supplied Markdown and
packages them as `podman load`-able container image archives
(docker-archive format). The lightspeed-service
(which consumes these artifacts at runtime), the operator, and the console
plugin are separate projects.

## Audience

AI agents. Specs optimize for precision, unambiguous rules, and
machine-parseable structure.

## Quick Start

| I want to... | Read |
|--------------|------|
| Understand what this project does | `what/system-overview.md` |
| Understand BYOK input/output behavior | `what/byok.md` |
| Understand chunking/embedding/output rules | `what/embedding-pipeline.md` |
| Understand the container build and CI | `what/container-build.md` |
| Navigate the codebase | `how/project-structure.md` |
| Trace the pipeline data flow | `how/byok-pipeline.md` |
| Modify the Containerfile or build | `how/container-build.md` |
| See recorded architecture decisions | `decisions/` |

## Cross-Reference

| what/ | how/ |
|---|---|
| `what/system-overview.md` | `how/project-structure.md` |
| `what/byok.md` | `how/byok-pipeline.md` |
| `what/embedding-pipeline.md` | `how/byok-pipeline.md` |
| `what/container-build.md` | `how/container-build.md` |

## Conventions

- **Rule numbering:** behavioral rules are numbered sequentially within each what/ file.
- **Planned changes:** unimplemented behavior is marked with `[PLANNED]` or `[PLANNED: OLS-XXXX]` inline next to the rule it affects.
- **Authority:** what/ specs are authoritative for behavior. how/ specs are authoritative for implementation. When they conflict, what/ wins.
- **When to create a new file vs. extend an existing one:** if the new concern has its own lifecycle, configuration surface, and can be understood independently, it gets its own file. If it's a capability added to an existing component, it goes in that component's file.
- User-configurable values are referenced by CLI flag name or environment variable name.
- Internal constants are stated as behavioral rules without numeric values; `how/` specs may include specific values.

## Relationship to lightspeed-service

This project produces artifacts consumed by lightspeed-service. The
`lightspeed-service` repo's `what/rag.md` spec describes how it loads and
queries these indexes at runtime (llama-index-core `FaissVectorStore.from_persist_dir`).
This project's specs describe how the indexes are built. The integration
contract is documented in `what/system-overview.md`.
