# BYOK tool end-to-end integration test

`pipeline/byok-tool-integration-test.yaml` follows the multi-platform Konflux VM
pattern of `lightspeed-core/rag-content`'s integration test. It extracts the
`lightspeed-rag-tool` image and source revision from the `SNAPSHOT`, then uses
Konflux's `multi-platform-ssh-$(context.taskRun.name)` secret to run
`tests/integration-konflux/byok-e2e.sh` on an amd64 Podman VM. It fetches the
script at the snapshot's commit; it never tests a floating `:latest` image.

The VM test runs the **default tool command** against mounted Markdown, uses
the snapshot image as both the outer image and its nested Buildah builder,
checks the generated archive, loads the image, and checks its vector DB and
metadata. A missing archive, failed nested build, or invalid output image fails
the PipelineRun. The task writes a Konflux `TEST_OUTPUT` JSON result. The
existing build-time `byok/smoke_tool.py` remains a faster, separate check for
Python imports and the embedding CLI.

The current tool image is **amd64-only**, so the default `platforms` matrix has
only `linux-mlarge/amd64`. Add arm64 when a compatible tool image is built.
The test needs the Konflux multi-platform controller to provision a Podman VM,
SSH secrets for that VM, network access to the snapshot image registry and the
output base image registry, and enough disk for the tool image in both the
Podman and nested Buildah stores. It does not query a running OLS service or
measure build time. It uses the documented `/dev/fuse` and SELinux bind-mount
workflow, not `--privileged` to mask mount failures. `STORAGE_DRIVER=vfs` avoids
an overlay-on-overlay failure in nested Buildah; it does not bypass the
`/markdown` remount error.

**Known failure on PR #808's current image:** a local Podman run of this script
reached Buildah's `RUN` step and failed remounting `/markdown` (`operation not
permitted`). The PR's build-time FAISS smoke test passes, but its default BYOK
image build remains broken. Do not merge based on the smoke test alone; either
fix the nested build or explicitly separate the full-flow failure into a
tracked blocking issue before enabling this scenario as a required PR gate.

To **enable** this as a PR/push integration test, a Konflux admin must register
`integration-test-scenarios/byok-tool.yaml` in the
`crt-nshift-lightspeed-tenant` namespace (for example, using `oc apply -f`).
Committing these files alone does *not* register the scenario or gate PRs.
Check that `rag-tool` is the Konflux application and `lightspeed-rag-tool` its
component before applying. The scenario is non-optional, so failure blocks
the snapshot.

The checked-in resolver points at upstream `main`. To run the test against an
**unmerged PR**, apply a copy of the scenario with resolver URL
`https://github.com/sriroopar/lightspeed-rag-content.git` and revision
`fix/OLS-4390-python-env`. Restore upstream `main` when the PR merges. The
snapshot selects the PR's *image*; the resolver selects the Pipeline definition.
