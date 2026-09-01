# Spec health report

Last evaluated: 2026-08-31
Trigger: staleness + accuracy check (post-OKP-adoption alignment)
Layout: software (.ai/spec/)

## Stale

- **how/container-build.md** (Makefile Targets table, `install-tools` row): documented command is `pip3.11 install pdm`, but the actual Makefile runs `pip3.12 install --no-cache-dir --upgrade pip pdm`. Stale from the Python 3.11 -> 3.12 migration.
- **how/project-structure.md** (lsc module map): line counts drifted by one for three files — `document_processor.py` says 836 (actual 835), `okp.py` says 153 (actual 152), `utils.py` says 72 (actual 71). (`asciidoctor_converter.py` 188 and `metadata_processor.py` 100 are correct.)
- **what/embedding-pipeline.md**: internal contradiction on OLS-1729. Rule 7 carries the inline marker `[PLANNED: OLS-1729 -- fine-tuned embedding models]`, but the Planned Changes section lists `[REMOVED: OLS-1729]` (superseded by OKP adoption). The inline PLANNED marker is stale.

## Missing

- **README.md** does not reference the `.ai/spec/decisions/` directory, which exists (ADR directory added in commit fe282951). Not in the Structure table, Quick Start, or Conventions.
- **how/project-structure.md** module map omits several files that now exist:
  - Root: `ARCHITECTURE.md`, `requirements-build.in`.
  - `lsc/` root: `Makefile`, `rpms.in.yaml`, `rpms.lock.yaml`, `uv.lock`.

## Structural concerns

- Root **ARCHITECTURE.md** (a repo doc, NOT a `.ai/spec/` file) describes the OCP product-docs FAISS pipeline as active ("converts OpenShift product documentation and operational runbooks into pre-built FAISS vector indexes"). This contradicts the OKP-adoption deprecation stance now carried throughout `what/`. Flagged for human review — out of scope for spec edits (not under `.ai/spec/`).

## Findability issues

- The `decisions/` ADR directory is not discoverable from the spec README (see Missing).

## No issues

- All module-map file references verified present in the codebase (all deprecated pipelines, scripts, Containerfiles, and `.tekton/` pipelines still exist in-tree — deprecation is documented, not deleted).
- Integration test python version is correct: `.tekton/integration-tests/lightspeed-rag-content-image-verification.yaml` runs `python3.11 scripts/verify_rag_image_test.py`, matching how/container-build.md.
- Deprecation markers in `what/` (system-overview, content-sources, container-build) align with code that is present-but-deprecated.
- `[PLANNED]` / `[REMOVED]` markers otherwise consistent (OLS-2704, OLS-1872, OCPSTRAT-1494 open; OLS-2294, OLS-2903 removed/completed).
- BYOK behavioral rules, config surfaces (env vars, CLI args), and constraints match `byok/generate_embeddings_tool.py` and `byok/Containerfile.tool`.
