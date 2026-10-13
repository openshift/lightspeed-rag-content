# BYOK tooling HOWTO

These are quick notes on how to build and run OpenShift Lightspeed BYOK tooling. The rest of the text assumes you created
`quay.io/$USERNAME/byok_tool` container image repository.

## Design

The purpose of the tool image is to encapsulate in a container everything needed to build a BYOK container image.
The tool image wraps buildah, byok/Containerfile.output and the RAG embeddings
generation script with its Python dependencies. There are two mandatory parameters: the input directory with the user-provided
content and an output directory for the resulting container image. byok/Containerfile.output is the Containerfile
for resulting image containing the RAG database.

## These steps will be done during the OLS build:

Use for your experimentation. Once released, MY_BYOK_TOOL_IMAGE will be registry.redhat.io/openshift-lightspeed-tech-preview/lightspeed-rag-tool-rhel9:latest.

### Build and push the BYOK tool image.

```bash
$ MY_BYOK_TOOL_IMAGE=quay.io/$USERNAME/byok_tool:0.0.1
$ podman build --build-arg BYOK_TOOL_IMAGE=$MY_BYOK_TOOL_IMAGE -t $MY_BYOK_TOOL_IMAGE -f byok/Containerfile.tool .
$ podman push $MY_BYOK_TOOL_IMAGE
```

## This is how to run the BYOK tool you built yourself:

```bash
$ MY_BYOK_TOOL_IMAGE=quay.io/$USERNAME/byok_tool:0.0.1
$ podman run -e OUT_IMAGE_TAG=my-byok-image -it --rm --device=/dev/fuse \
  -v $XDG_RUNTIME_DIR/containers/auth.json:/run/user/0/containers/auth.json:Z \
  -v <dir_tree_with_markdown_files>:/markdown:Z \
  -v <dir_for_image_tar>:/output:Z \
  $MY_BYOK_TOOL_IMAGE
```

The released version of the tool can be run as follows:

```bash
$ podman run -it --rm --device=/dev/fuse \
  -v $XDG_RUNTIME_DIR/containers/auth.json:/run/user/0/containers/auth.json:Z \
  -v <dir_tree_with_markdown_files>:/markdown:Z \
  -v <dir_for_image_tar>:/output:Z \
  registry.redhat.io/openshift-lightspeed-tech-preview/lightspeed-rag-tool-rhel9:latest
```

The tool runs on CPUs, not GPUs.

There are two mandatory parameters:

- <dir_tree_with_markdown_files> is the root of the directory tree containing the content to be included in the BYOK RAG database, in Markdown. It is accessed for reading. File extensions are expected to be `.md`.
- <dir_for_image_tar> is the directory where the resulting image tar archive will be written. It needs to be writable.

The OUT_IMAGE_TAG environment variable can be used to override the tag of the generated image. It defaults to "byok-image".
The VECTOR_DB_INDEX environment variable can be used to override the database index. It defaults to "vector_db_index".

The BYOK tool will produce the resulting container image as a tar archive named `<dir_for_image_tar>/my-byok-image.tar`. Existing `<dir_for_image_tar>/my-byok-image.tar` will be overwritten.

The image can be instantiated like so:

```bash
$ podman load < <dir_for_image_tar>/my-byok-image.tar
$ podman images
REPOSITORY                      TAG                IMAGE ID      CREATED         SIZE
localhost/my-byok-image         latest             33f09213a608  23 seconds ago  103 MB
...
```

and then tagged and pushed to the desired container image registry:

```bash
$ podman tag localhost/my-byok-image:latest quay.io/$USENAME/my-byok-image:latest
$ podman push quay.io/$USENAME/my-byok-image:latest
```

Here is what is inside of the generated image:
```bash
$ podman run --rm localhost/byok-image-foobar:latest ls -l /rag/vector_db
total 1408
-rw-r--r--. 1 root root 682029 Apr  4 03:30 default__vector_store.json
-rw-r--r--. 1 root root 731051 Apr  4 03:30 docstore.json
-rw-r--r--. 1 root root     18 Apr  4 03:30 graph_store.json
-rw-r--r--. 1 root root     72 Apr  4 03:30 image__vector_store.json
-rw-r--r--. 1 root root  11417 Apr  4 03:30 index_store.json
-rw-r--r--. 1 root root    268 Apr  4 03:30 metadata.json
$ podman run --rm localhost/byok-image-foobar:latest cat /rag/vector_db/metadata.json
{"execution-time": 82.21773672103882, "llm": "None", "embedding-model-name": "sentence-transformers/all-mpnet-base-v2", "index-id": "vector_db_index", "vector-db": "faiss.IndexFlatIP", "embedding-dimension": 768, "chunk": 380, "overlap": 0, "total-embedded-files": 29}
```
The database is located at /rag/vector_db and by default the Faiss index id is "vector_db_index". The VECTOR_DB_INDEX environment variable can be used to override this default:

```bash
$ podman run -e VECTOR_DB_INDEX=acme_openshift_sop ...
```

## Customer-workflow integration test

`tests/integration-konflux/pipeline-konflux.sh` exercises the shipped tool image.
It mounts a fictional OpenShift runbook, runs the nested build using the same tool
image, loads the exported customer image archive, and extracts `/rag/vector_db`.
It checks index metadata, then starts the real OLS service with that index and asks
for the runbook's recovery phrase. Success requires the phrase in the
answer **and** the matching title/URL in `referenced_documents`. The question does not
contain the phrase, so echoing it or answering from general training knowledge cannot pass.

The test uses `STORAGE_DRIVER=vfs` for nested buildah, avoiding overlay-on-overlay
limitations in the VM test runner. Both inner Podman runs use `--network=host`,
matching the reference and avoiding netavark bridge setup inside the runner.
It copies Markdown into a disposable writable mount, as used by the customer
invocation above; a read-only outer mount prevents nested buildah from remounting it.
Neither tested product image receives dependency installs, Python path overrides,
or replacement entrypoints. Only the surrounding test runner installs infrastructure
tools. The OLS config disables authentication/TLS for local loopback testing; the
service otherwise runs its default entrypoint with real inference.

### Run locally

Requires Podman, `/dev/fuse`, Python with PyYAML for unit tests, curl, registry pull
credentials, and an OpenAI API key authorized for `gpt-4o-mini`.

```bash
make test-unit

export BYOK_TOOL_IMAGE=<tool-image>@sha256:<digest>
export OLS_SERVICE_IMAGE=<service-image>@sha256:<digest>
export UBI_BASE_IMAGE=<output-base-image>@sha256:<digest>
# Set OPENAI_API_KEY in your environment; do not put it in tracked files.
# Set REGISTRY_AUTH_FILE if pull auth is not in $XDG_RUNTIME_DIR/containers/auth.json.
ARTIFACT_DIR=/tmp/byok-e2e-artifacts bash tests/integration-konflux/pipeline-konflux.sh
```

For a locally built tool image, make it available through a registry: the nested build
must be able to pull the same image that the outer container runs. Logs and the API
response are retained in `ARTIFACT_DIR` on success and failure. Temporary containers,
customer output images, and credential files are removed. The test binds OLS to
loopback port 18080; do not run another service on that port concurrently.

A local non-hermetic tool build also needs enabled RHEL RPM repositories or appropriate
subscription mounts for the RHOAI base. Konflux supplies prefetched RPMs for its
hermetic build; a base-image RPM repository failure locally is not a Python test failure.

### Register in Konflux

The pipeline follows the VM-backed Podman pattern used by lightspeed-core/rag-content.
It selects the tool image and exact source commit from `SNAPSHOT`, rejects absent or
ambiguous components and mutable image references, and reports Konflux `TEST_OUTPUT`.
It currently runs on `linux-mlarge/amd64`, matching the x86_64-only CPU lockfiles.

The tenant needs:

- The Konflux multi-platform controller and capacity for that VM platform.
- Secret `openai` with key `token`, matching the other OLS integration tests.
- Existing registry Secrets `openshift-lightspeed` (Quay) and `registry-redhat-io`
  (Red Hat registry), each with key `.dockerconfigjson`. Ensure they permit pulling
  the snapshot tool and the chosen OLS image. The public UBI output base needs no auth.

The OpenAI Secret name is a pipeline parameter. The registry Secrets are mounted
read-only and their auth entries are merged into a temporary `auth.json` with mode
0600 for Podman and nested buildah. Registry credentials should grant only the required
pull access; use a scoped, budget-limited inference key for this test.

The credentials are copied over SSH into a private VM directory, mounted into the
infrastructure runner, and removed after execution. No
shell tracing is enabled. The runner is privileged to support nested Podman/buildah;
privilege is confined to the provisioned test VM, not granted to the product service.

The snapshot checkout contains executable test scripts, and the product images themselves
run with pull/inference credentials available. Before enabling this scenario for PR builds,
confirm the tenant's trusted-contributor/manual-approval controls prevent untrusted fork
code from receiving those credentials. Private mounts and disabled shell tracing are not
a substitute for that approval boundary. SSH uses the provisioned VM secret and follows
the reference runner's disabled host-key checking; use this only on tenant-managed test VMs.

After merging the pipeline, review the digest-pinned OLS and output-base image parameters
in `.tekton/integration-tests/byok-integration-test-scenario.yaml`, then register it:

```bash
oc apply -f .tekton/integration-tests/byok-integration-test-scenario.yaml
```

The scenario belongs to application `rag-tool`, with context
`component_lightspeed-rag-tool`. It is required, not optional. The OLS consumer is an
explicit pinned parameter because it is not in this application's snapshot; update its
pin intentionally when updating the consumer used for compatibility validation. To
bootstrap the test before merge, point a copy of the scenario's git resolver at the PR
repository and commit. The test payload is always checked out at the snapshot source
revision, never at an implicit `main` fallback.

VM artifacts are copied back to `/var/workdir/artifacts` in the test TaskRun and relevant
output is in Tekton logs. This directory is ephemeral; retrieve it before the TaskRun
pod is removed if you need the full files. The pipeline does not upload credentials or
artifacts to an external registry. Artifact retrieval failures are reported as warnings in
`TEST_OUTPUT`; unconfirmed remote or local credential deletion makes the task fail.
Bootstrap failures also produce a failure result, even before the VM runner starts.

## Document title and URL
OpenShift Ligthspeed can display titles and URLs of the documents used for generation of answers. In the RAG database, titles and URLs accompany documents as metadata. The BYOK tool can obtain the title and url attributes from YAML frontmatter if found in Markdown files it processes:

```Markdown
---
title: "Introduction to Layers {#gimp-concepts-layers}"
url: "https://docs.gimp.org/3.0/en/gimp-using-layers.html"
---

# Introduction to Layers
...
```

If a Markdown file does not have frontmatter with the title and url attributes, the first top-level Markdown heading (ex. `# Introduction to Layers`) becomes the title and the file path becomes the URL.
