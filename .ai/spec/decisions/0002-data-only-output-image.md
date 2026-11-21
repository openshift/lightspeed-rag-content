# 0002: Data-only, single-manifest customer output image

Date: 2025-11-27
Status: accepted

## Context

The customer output image used to embed a baked ubi9-minimal base layer
(flattened at tool-build time into `base-layer.tar`), mainly so the OLS
operator's RAG init container could run `sh -c "mkdir ... && cp -a ..."`
from the image's own filesystem. That tied the output image to a specific
architecture twice over: the base layer contained x86_64 binaries, and the
consumer executed a shell from the image.

OLM solves the same problem for operator bundles with a different
convention: bundle images are pure data, the consumer overrides the
entrypoint with a binary staged from a separate multi-arch image, and the
image is a single-platform manifest (not a manifest list). Container
runtimes apply the platform filter only when selecting from a manifest
list, so a single-manifest image is pullable on any node architecture —
which is why OLM can unpack amd64-only operator bundles on arm64/ppc64le/
s390x clusters.

## Decision

The customer output image is data-only:

- one layer, holding `/rag/vector_db` — no base layer at all;
- no `Cmd` or `Entrypoint` in the image config — the image declares
  nothing to execute;
- the config keeps a nominal `architecture: amd64` so the image stays a
  plain single-platform manifest, which is pullable on any node arch.

On the consumer side, the OLS operator stages a complete copy tool from
the OLS service image (which the pod runs anyway, so it already matches
the node architecture) into a `rag-util` emptyDir: the real coreutils
binary, the dynamic loader, and the binary's shared libraries, invoked
as `/rag-util/ld.so --library-path /rag-util/lib /rag-util/cp ...` in the
RAG init containers. RHEL's coreutils is dynamically linked, so the
loader staging is required — a dynamically linked binary executed
directly would fail because its `PT_INTERP` loader path resolves against
the data-only image's rootfs, where `/lib64` does not exist. (OLM's
equivalent `cpb` helper is a statically linked Go binary, which is why
it needs no loader staging.) The customer image only has to be
pullable — as a single-platform manifest it is pullable on any node
architecture — and its entrypoint and binaries are not run. (Boundary
note: the staged loader does execute in the customer image's root
filesystem and honors its `/etc/ld.so.preload`; the image's entrypoint
and own binaries are what never run.) This is the same pattern OLM
uses for bundle unpacking.

## Consequences

- Customer indexes built on any machine work on any OLS cluster
  architecture; the operator side no longer requires a shell inside the
  customer image.
- The output image is no longer a "RHEL-based image" — image scanners that
  expect a package-managed base will see an empty OS layer. Labels are
  preserved in the image config for identification.
- The tool image no longer bakes or ships `base-layer.tar`, and the
  `OUTPUT_BASE_IMAGE` build arg and `-base-layer` flag are gone.
- If a future use case ever needs to *run* something from the output
  image, this decision must be revisited.
