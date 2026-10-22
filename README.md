# OpenShift Lightspeed RAG content

## Hermetic / Konflux dependency lockfiles

Cachi2 prefetch uses split hashed requirements for runtime dependencies, build dependencies, and bootstrap tools. Update them with:

```bash
make bump                                  # refresh dependencies using existing project policy
make bump PKG=<package> VERSION=<minimum>   # require this version or newer
```

Replace the placeholders with the package name and minimum version, and repeat the targeted command for each package you need to update.

Targeted updates prefer existing locked versions of other packages, but allow changes required by the update—including build dependencies and shared runtime/build packages. `VERSION` is a minimum, not an exact pin. Explicit compatibility bounds are preserved; an unsatisfiable update fails with the resolver's diagnostic. Direct-URL dependencies must be updated explicitly in `pyproject.toml` rather than rewritten by the command.

A targeted update applies the requested minimum as a temporary constraint for that run, intersecting rather than replacing upstream requirements. Direct and optional dependency minimums are also updated in `pyproject.toml`; transitive minimums are not saved as persistent policy. `requirements.overrides.txt` remains separate, deliberately configured policy and is never modified by targeted updates.

The implementation is in `scripts/konflux_resolve.py`. **Compilation uses the forked `quay.io/syedriko/uv:prefer-index` image**, whose `prefer-index` policy is not available in upstream uv. Host uv provisions Python **3.12** and the discovery tools (`pybuild-deps`, `pip-tools`, `pip`). Podman or Docker and network access to the package indexes are required.

Runtime and recursively discovered source-build requirements are resolved together. Existing lockfile versions are soft preferences, never restored after resolution. Build/bootstrap requirements use the profile's target Python version, not an old generated-file header. Generated requirements and Tekton prefetch lists are staged before replacing their existing files; review their diffs after a successful run. A failed run may leave the requested minimum in the input files, but does not publish partially generated requirements. PDM lockfiles are not refreshed.

`make update-konflux-deps` remains an alias for `make bump`. Run `make test-unit` for unit tests, or `make test-resolver-image` to also exercise deterministic local indexes through the real forked image.

If discovery fails with a `dbm` cache error, remove the corrupted `pybuild-deps` cache under `~/.cache/pybuild-deps/` and rerun. Do not commit generated outputs until the command completes successfully.

RPM lockfiles (`rpms.lock.yaml`) are maintained with your org’s **rpm-lockfile** workflow; see `make update-rpm-lock` for a short pointer.

### Typical dependency update workflow

1. **Run `make bump`.** This resolves updated dependency versions using the existing project requirements and overrides, then regenerates the lockfiles and prefetch configuration. It does not rewrite those policy inputs.
2. **Run `make bump PKG=<package> VERSION=<minimum>` for each package you need to update.** Each run uses the current lockfiles as version preferences, including the results of the preceding update. Other packages can change when compatibility requires it, but are not refreshed merely because newer versions exist.
3. **Review and commit the changes together.** Include any changes to `pyproject.toml`, the generated requirements, and Tekton prefetch configuration. There is no additional constraints file to create, review, or maintain.

The requested minimum is enforced throughout that targeted run, including build dependency resolution. Afterward, the selected version is recorded in the generated lockfiles. For a package declared in `pyproject.toml`, its updated minimum also persists there. For a transitive package, later runs prefer its locked version but do not remember the earlier request as a hard minimum; a later compatible solution may select an older version.

If resolution fails, inspect its diagnostic for the blocking requirements. Do not use an override simply to bypass a parent's compatibility restriction. A failed targeted update may leave an edited minimum in `pyproject.toml`; if you abandon the request, revert only that attempt's input changes. Generated requirements are not published when resolution fails.

## Legacy

`scripts/generate_packages_to_prefetch.py` is **obsolete** (Cachito-era); it exits with an error and points to the targets above.
