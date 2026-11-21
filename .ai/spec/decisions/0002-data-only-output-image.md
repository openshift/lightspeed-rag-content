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
- no `Cmd` or `Entrypoint` in the image config — nothing from the image
  is ever executed;
- the config keeps a nominal `architecture: amd64` so the image stays a
  plain single-platform manifest, which is pullable on any node arch.

On the consumer side, the OLS operator stages `cp` from the OLS service
image (which the pod runs anyway, so it already matches the node
architecture) and runs it as the RAG init container command — the same
pattern OLM uses for bundle unpacking. The customer image only has to be
pullable, never executable.

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
