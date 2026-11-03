# Container Build (Implementation)

This spec describes how the tool container image is built: the Containerfile
stages, the native library builds, model packaging, and the Makefile. The
behavioral rules are in `what/container-build.md`.

## Containerfile Stages

```
output-base   (ubi9-minimal, digest-pinned)
    └─ flattened into base-layer.tar (rootfs tar with fixed metadata)

native        (ubi9)
    ├─ OpenBLAS v0.3.29     — static-only build from submodule; serial,
    │                        pure-C (C_LAPACK=1, NOFORTRAN=1)
    ├─ faiss v1.12.0       — cmake, C API on, GPU/Python off, static libs
    ├─ onnxruntime v1.31.0 — cmake, CPU only, static; component archives
    │                        merged into libonnxruntime.a (ar MRI script);
    │                        FetchContent deps wired to
    │                        third_party/onnxruntime-deps/ via
    │                        FETCHCONTENT_SOURCE_DIR_<NAME> (setup-ort-deps.sh)
    ├─ model reassembly    — cat model/mpnet.onnx.gz.* | gunzip, sha256 -c
    └─ licenses             — faiss/openblas/onnxruntime/deps → /out/licenses

builder       (ubi9/go-toolset)
    ├─ byok-go              — static CGO link: all native archives in
    │                         --start-group, static libstdc++ (from the
    │                         native stage) and -static-libgcc
    └─ base-layer.tar       — flattened rootfs tar of output-base

runtime       (ubi9-micro, digest-pinned)
    /opt/byok/              — mpnet.onnx, tokenizer.json, cl100k_base.tiktoken,
                              sentence_bert_config.json, base-layer.tar, licenses/
    /usr/local/bin/byok-go  — statically linked; needs only glibc
    CMD byok-go -i /markdown -o /output/$OUT_IMAGE_TAG.tar ...
```

Key decisions (see also `decisions/0001-static-native-linking.md`):

- The native libraries are linked statically into `byok-go`: the runtime
  image ships a single binary plus the model, with no `/opt/byok/libs` and
  no `LD_LIBRARY_PATH` — ubi9-micro's glibc is the only shared-library
  dependency.
- faiss's `write_index` dispatch references every index type, so BLAS/LAPACK
  symbols are link-required; they resolve against the static OpenBLAS built
  in the native stage (no static OpenBLAS exists in the ubi9 repos).
- onnxruntime's static mode exposes component libraries
  (`onnxruntime_common`, `onnxruntime_session`, ...), which are merged into
  one `libonnxruntime.a`; `re2` needs an explicit `make re2`.
- cgo's flag filter drops `-static-libstdc++`; the static libstdc++.a comes
  from the native stage (via `libstdc++-static` from CRB), and libgcc is
  made static through `go build -ldflags "-extldflags -static-libgcc"`.
- The customer output base layer is baked at build time so the running tool
  never needs `podman`/`buildah`/registry access to produce an image.
- Cachi2 env (`/cachi2/cachi2.env`) is sourced when present so dnf resolves
  RPMs from the prefetch cache in hermetic Konflux builds.

## Native Library Pinning

- faiss: `third_party/faiss` submodule, v1.12.0 — must match the service's
  faiss-cpu for serialization compatibility.
- onnxruntime: `third_party/onnxruntime` submodule, v1.31.0; all CMake
  FetchContent dependencies are submodules under
  `third_party/onnxruntime-deps/` (abseil, protobuf, eigen, re2, etc.).
  `scripts/setup-ort-deps.sh` emits the `FETCHCONTENT_SOURCE_DIR_*` cmake
  flags. The protobuf utf8_range include path is added via CXXFLAGS.
- OpenBLAS: `third_party/openblas` submodule, v0.3.29 — same major version
  family as the service's openblas runtime; built static/serial/pure-C.

## Makefile Targets

| Target | Purpose |
|---|---|
| `make build` | Stage native libs, `go build ./cmd/byok-go` |
| `make build-dev` | Build `cmd/byok-go-dev` |
| `make build-image` | Build the tool image with podman/docker |
| `make test` | Pure-Go unit tests (CGO_ENABLED=0) + gofmt check |
| `make test-native` | All tests incl. cgo packages (stages native libs) |
| `make lint` | gofmt check (fails on unformatted files) |
| `make format` | gofmt -w |
| `make model-chunks MODEL=...` | Regenerate `model/mpnet.onnx.gz.*` + sha256 |

`scripts/stage-go-native.sh` compiles/stages the static faiss + onnxruntime
+ OpenBLAS archives into `.byok-go-native/` (override with
`BYOK_GO_NATIVE_DIR`) and prints the CGO environment (including the static
link flags via `GO_BUILD_LDFLAGS`) for local builds and `make test-native`.

## CI/CD

- `.tekton/lightspeed-rag-tool-pull-request.yaml` and
  `-push.yaml` — Konflux docker-build trusted-artifact pipelines.
- `.tekton/integration-tests/` — the BYOK customer-workflow e2e scenario;
  driver script in `tests/integration-konflux/pipeline-konflux.sh`.

## Dependency Management

- Go modules vendored; update with standard `go mod tidy && go mod vendor`.
- RPMs: `rpms.in.yaml` (gcc, gcc-c++, cmake, make, git, gzip, perl,
  libstdc++-static from CRB) locked in
  `rpms.lock.yaml`.
  What each is for: gcc/gcc-c++/cmake/make compile the native libraries;
  `git` applies the onnxruntime submodule patches
  (`scripts/setup-ort-deps.sh` uses `git apply` — without git the patches
  are *silently* skipped); `gzip` reassembles the model chunks; `perl` is
  required by the OpenBLAS build; `libstdc++-static` provides
  `libstdc++.a` for the static link.
  onnxruntime needs no Python in static mode (its Python usage —
  generating the shared library's symbol-export def file — is guarded by
  `onnxruntime_BUILD_SHARED_LIB`).
- Base image digests: automated Konflux/Mintmaker PRs (renovate.json).
- Model chunks: `make model-chunks` from a local mpnet.onnx; verify sha256
  committed in `model/mpnet.onnx.sha256`.

### Regenerating `rpms.lock.yaml`

The lockfile must be regenerated whenever `rpms.in.yaml` changes (adding or
removing packages); committing a changed input without a matching lockfile
breaks hermetic Konflux builds, because dnf can then only install what the
Cachi2 prefetch cache contains. The generator is
[rpm-lockfile-prototype](https://github.com/konflux-ci/rpm-lockfile-prototype);
it is not on PyPI, so install it from git in a ubi9 container (it needs the
system dnf bindings):

```bash
podman run --rm -v "$PWD:/src:Z" registry.access.redhat.com/ubi9/ubi:latest \
  bash -c 'dnf install -y --nodocs python3-pip python3-dnf git && \
    pip3 install "git+https://github.com/konflux-ci/rpm-lockfile-prototype.git" && \
    rpm-lockfile-prototype --bare /src/rpms.in.yaml --outfile /src/rpms.lock.yaml'
```

Notes:

- `--bare` resolves against the repofiles referenced by `rpms.in.yaml`
  (`ubi.repo`, including the CRB repo) without needing a container image.
- The tool locks both `x86_64` and `aarch64` (per `arches:` in
  `rpms.in.yaml`) and all transitive dependencies.
- Warnings about missing **source** RPMs (e.g. `libstdc++-devel`,
  `llvm-libs`) are informational; only binary RPM resolution matters for
  the prefetch cache.
- The tool needs network access to `cdn-ubi.redhat.com` (and to
  `github.com`/PyPI for the one-time install).
