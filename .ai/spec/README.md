# OpenShift LightSpeed RAG Content -- Specifications

These specs define the requirements, behaviors, and architecture for the lightspeed-rag-content project. They are organized into two layers:

- **[`what/`](what/README.md)** -- Behavioral rules: WHAT the system must do and WHY. Technology-neutral, testable assertions. Use these to understand requirements, fix bugs, or rebuild components.
- **[`how/`](how/README.md)** -- Architecture specs: HOW the current implementation is structured. Module boundaries, data flow, design patterns. Use these to navigate, modify, and extend the codebase.

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

## Conventions

- `[PLANNED: OLS-XXXX]` markers in `what/` specs indicate existing rules about to change due to open Jira work.
- "Planned Changes" sections list new capabilities not yet in code.
- User-configurable values are referenced by CLI argument name or environment variable name.
- Internal constants are stated as behavioral rules without numeric values; `how/` specs may include specific values.

## Relationship to lightspeed-service

This project produces artifacts consumed by lightspeed-service. The service's `what/rag.md` spec describes how it loads and queries these indexes at runtime. This project's specs describe how the indexes are built. The integration contract is documented in `what/system-overview.md`.
