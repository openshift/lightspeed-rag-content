# OpenShift Lightspeed RAG content

## BYOK dependency audit

Run `make check-unused-deps` to audit the Python code shipped by
`byok/Containerfile.tool`. The target scans `byok/`, not the deprecated root
image pipeline or unrelated development scripts. It runs a pinned deptry through
`uvx` in an isolated tool environment; the first run needs package-index access.
It does not install application dependencies or change lockfiles and is separate
from `make verify`.

Only the unused-dependency rule (`DEP002`) is enabled. Findings return a nonzero
exit status and require review: packages can be used indirectly by the embedding
stack, required as runtime backends, or declared to enforce security-version
floors. For example, PyTorch is required despite no direct import in the BYOK
script. Package/import-name mappings live in `pyproject.toml`; shared namespaces
such as `llama_index` make detection approximate.

Before removing a candidate, test Markdown ingestion (including YAML frontmatter),
embedding generation, and FAISS persistence with the pinned dependency stack.
The base image may already contain a package, so removing it from the application
requirements does not necessarily remove it from the final image. Regenerate
Konflux inputs only after confirming a removal is safe.

## Hermetic / Konflux dependency lockfiles

Cachi2 prefetch uses split hashed requirements (RHOAI wheels vs PyPI source) and optional build-dependency lockfiles. Regenerate them with **uv** and Python **3.12** after changing `pyproject.toml` or `requirements.overrides*.txt`:

```bash
make update-konflux-deps       # regenerate RHOAI/PyPI split lockfiles for Konflux
```

Implementation: `python3 scripts/konflux_resolve.py --profile cpu`, using the root
`profiles.toml`. It resolves dependencies in `quay.io/syedriko/uv:prefer-index`,
generates split hashed requirements and host-side build dependencies with
`pybuild-deps`, and updates the configured Tekton package lists. Regeneration
requires Podman or Docker, Python 3.12+ with `packaging`, and `pybuild-deps` on
`PATH`.

Run with a clean uv configuration (`UV_NO_CONFIG=1`, with `UV_CONFIG_FILE` and
custom index environment variables unset) so host-side build requirements stay
on public PyPI. Review all generated requirements and `.tekton/` changes;
`requirements-build.txt` must not contain `--index-url`. Do not commit generated
files until regeneration completes successfully.

RPM lockfiles (`rpms.lock.yaml`) are maintained with your org’s **rpm-lockfile** workflow; see `make update-rpm-lock` for a short pointer.

## Legacy

`scripts/generate_packages_to_prefetch.py` is **obsolete** (Cachito-era); it exits with an error and points to the targets above.
