# Behavioral Specifications (what/)

These specs define WHAT the RAG content pipeline must do -- testable behavioral rules, configuration surface, constraints, and planned changes. They are technology-neutral where possible and survive a complete rewrite in a different framework.

## Spec Index

| Spec | Description |
|------|-------------|
| [system-overview.md](system-overview.md) | Project purpose, boundaries, integration contract with lightspeed-service |
| [content-sources.md](content-sources.md) | OCP docs, runbooks, OKP content -- acquisition, versioning, metadata, exclusions |
| [embedding-pipeline.md](embedding-pipeline.md) | Shared behavioral rules for all pipeline variants: chunking, embedding, vector store output, index organization |
| [byok.md](byok.md) | Bring Your Own Knowledge -- customer content import via tool container |
| [container-build.md](container-build.md) | Container images, hermetic builds, CI/CD pipelines, dependency management |

## How to Use These Specs

- **Fixing a bug**: Read the relevant spec to understand correct behavior, then compare against the code.
- **Adding a feature**: Check if the spec covers the requirement. Update the spec before implementing.
- **Refactoring**: Use the specs as acceptance criteria. The implementation can change freely as long as it meets the behavioral rules.
- **Understanding planned work**: Look for `[PLANNED: OLS-XXXX]` markers inline and "Planned Changes" sections.

## Relationship to how/ Specs

These `what/` specs define the behavioral contract. The [`how/` specs](../how/README.md) describe the current implementation architecture. Read `what/` to understand requirements, read `how/` to understand the codebase structure.
