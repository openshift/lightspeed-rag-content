# OpenShift Lightspeed RAG content

## Hermetic / Konflux dependency lockfiles

Cachi2 prefetch uses split hashed requirements (RHOAI wheels vs PyPI source) and optional build-dependency lockfiles. Keep the Konflux lockfiles and CPU PDM lock in sync after changing `pyproject.toml` or `requirements.overrides.txt`.

All dependency updates use a single entry point:

```bash
make bump                                   # resolve every dependency to the latest allowed version
make bump PKG=<name> VERSION=<version>      # bump one dependency; keep every other package pinned
```

`make bump` updates the dependency constraint when `PKG`/`VERSION` are given, regenerates the
Konflux lockfiles, then refreshes the CPU PDM lock (`pdm.lock.cpu`). Its build-dependency
compilation runs under the Python version recorded in `requirements-build.txt` and pins
`pybuild-deps==0.5.0`, `pip-tools==7.5.3`, and `pip==24.3.1`.

In targeted mode, every other package is frozen at its committed version by uv constraints and
a build-dependency pin restore, so only the requested dependency and changes it forces move.
Konflux prefers RHOAI-index wheels while PDM resolves indexed packages from PyPI, so versions can
differ when the sources expose different builds.

If the set of wheels or sdists changes, review the `prefetch-input` blocks in `.tekton/*.yaml` and update their `pip.binary.packages` entries where needed. If resolution fails with a `dbm` cache error, remove the corrupted `pybuild-deps` cache under `~/.cache/pybuild-deps/` and rerun the command; do not commit lockfiles until it completes successfully.

RPM lockfiles (`rpms.lock.yaml`) are maintained with your org’s **rpm-lockfile** workflow; see `make update-rpm-lock` for a short pointer.

## Legacy

`scripts/generate_packages_to_prefetch.py` is **obsolete** (Cachito-era); it exits with an error and points to the targets above.
