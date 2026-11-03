# 0001: Link the native libraries statically into byok-go

Date: 2026-11-03
Status: accepted

## Context

The Go port originally shipped faiss, ONNX Runtime, and their transitive
dependencies (OpenBLAS, libgfortran, libgomp, libstdc++) as shared libraries
in `/opt/byok/libs` of the tool image, with `LD_LIBRARY_PATH` set so the cgo
binary could find them. This mirrored the Python image's layout, where the
Python interpreter and site-packages legitimately needed shared libraries.

For the Go tool this is unnecessary: there is exactly one native consumer
(`byok-go`), and the runtime image is `ubi9-micro`, which has no package
manager — the `.so` files had to be hand-copied from the build stage, and any
missed or incompatible transitive library surfaced only at customer runtime
as a loader error.

## Decision

Compile faiss, onnxruntime, and OpenBLAS as static archives and link them
into the `byok-go` executable. The runtime image ships only the binary, the
embedding model, the baked output base layer, and license files. The only
shared-library dependency left is glibc (provided by ubi9-micro).

Implementation notes:

- faiss builds with `BUILD_SHARED_LIBS=OFF`; its cmake is pointed at the
  static OpenBLAS via `BLAS_LIBRARIES`/`LAPACK_LIBRARIES` cache variables,
  so no system BLAS is needed at configure time.
- onnxruntime builds with `onnxruntime_BUILD_SHARED_LIB=OFF`; the component
  archives (`libonnxruntime_common.a`, `libonnxruntime_session.a`, ...) are
  merged into a single `libonnxruntime.a` with an `ar` MRI script, and `re2`
  requires an explicit `make re2` (it is not part of the default target).
- OpenBLAS is built from a new `third_party/openblas` submodule (v0.3.29)
  with `NO_SHARED=1 USE_THREAD=0 C_LAPACK=1 NOFORTRAN=1`: static, serial,
  and pure C, so no Fortran runtime is needed. faiss's `write_index`
  dispatch references every index type, which makes BLAS/LAPACK symbols
  link-required even though the tool only adds vectors and serializes.
- The C++ runtime links statically: `libstdc++.a` comes from
  `libstdc++-static` (CRB) staged out of the native image, and
  `-static-libgcc` is passed through `go build -ldflags "-extldflags
  -static-libgcc"` because cgo's flag filter silently drops it from
  `CGO_LDFLAGS`.
- The binary is ~55 MB unstripped; `ubi9-micro` remains the runtime base.

## Consequences

- The runtime image has no `/opt/byok/libs` and no `LD_LIBRARY_PATH`; the
  binary runs anywhere glibc exists.
- One class of customer-runtime failures (missing/incompatible shared
  libraries) is eliminated.
- Local builds and tests use the same static staging
  (`scripts/stage-go-native.sh`); pure-Go tests remain unaffected
  (`make test`, CGO_ENABLED=0).
- The native build gains an OpenBLAS compile (~5 min) and the onnxruntime
  static build is slightly more involved (archive merge, explicit `re2`).
- New RPM requirements: `perl` (OpenBLAS build) and `libstdc++-static`
  (CRB); `rpms.lock.yaml` must be regenerated when these change.
- faiss serialization compatibility with the service is unaffected — it is
  a format property, not a linkage property.
