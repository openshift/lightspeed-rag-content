# Spec health report

Last evaluated: 2026-05-29
Trigger: structural evaluation (post spec-first:init alignment)
Layout: software (.ai/spec/)

## Stale

None. All stale references from the initial evaluation have been fixed:
- Python version updated from 3.11 to 3.12 across all spec files (container-build, plaintext-pipeline, byok)
- GPU base images updated to current versions (CUDA 12.9.2, rhai/base-image-cuda-12.9-rhel9:3.3)
- CPU base image updated from python-311 to python-312
- asciidoctor_converter.py line count updated from 160 to 188

## Missing

None. Previously undocumented files have been added to how/project-structure.md:
- `scripts/doc_downloader/downloader.py`
- `scripts/html_chunking/example.py`, `scripts/html_chunking/html-stripper.py`
- `scripts/html_embeddings/setup.py`
- `lsc/scripts/remove_pytorch_cpu_pyproject.py`
- `lsc/.../ruby_asciidoc/asciidoc_structure_dumper.rb`

## Structural concerns

None.

## Findability issues

None.

## No issues

- All module map file references verified as present in the codebase.
- All `[PLANNED: OLS-XXXX]` markers reference open future work.
- Behavioral rules in what/ files match current code behavior.
- Python versions, base images, and CUDA versions now match current Containerfiles.
- OCP version directories (4.16-4.22), Tekton pipelines, chunk defaults, and embedding model all current.
