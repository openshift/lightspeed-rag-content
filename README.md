# OpenShift Lightspeed RAG content

## Hermetic / Konflux dependency lockfiles

Cachi2 prefetch uses split hashed requirements (RHOAI wheels vs PyPI source) and optional build-dependency lockfiles. Regenerate them with **uv** and Python **3.12** after changing `pyproject.toml`, `lsc/pyproject.toml`, or `requirements.overrides*.txt`:

```bash
make update-konflux-deps       # root: cpu + gpu (run together; gpu reuses requirements-build.cpu.txt)
make update-konflux-deps-lsc   # LSC image: lsc/* lockfiles + lightspeed-ocp-rag pip.binary.packages
```

Implementation: `scripts/konflux_requirements.sh`. If the set of wheels or sdists changes, review the `prefetch-input` blocks in `.tekton/*.yaml` (the script updates `pip.binary.packages` where it finds a matching JSON line).

RPM lockfiles (`rpms.lock.yaml`, `lsc/rpms.lock.yaml`) are maintained with your org’s **rpm-lockfile** workflow; see `make update-rpm-lock` for a short pointer.

## Legacy

`scripts/generate_packages_to_prefetch.py` is **obsolete** (Cachito-era); it exits with an error and points to the targets above.
