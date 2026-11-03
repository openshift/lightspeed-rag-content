# Draft: updated "Providing custom knowledge to the LLM" section

Updates the published page (OLS 2.0 → Configure → 1.13.2) for the Go port of
the BYOK tool. Substantive changes vs. the current published page:

1. No `--device /dev/fuse` — the Go tool does not mount a FUSE filesystem
   (that was the Python pipeline's buildah-based build).
2. No `auth.json` mount — the tool no longer pulls from a registry at
   customer runtime; the output image is assembled in-process from a base
   layer baked into the tool image.
3. Output filename and image tag are set via environment variables
   (`OUT_IMAGE_TAG`, `VECTOR_DB_INDEX`) rather than an interactive prompt.
4. Clarified that no container runtime privileges are needed to produce the
   image archive — only `podman load`/`podman push` afterwards.

---

## 1.13.2. Providing custom knowledge to the LLM

By default, the OpenShift Lightspeed service answers questions using a
built-in RAG (retrieval-augmented generation) database that contains the
OpenShift Container Platform documentation. You can supplement or replace
that built-in database with your own content — for example, internal
documentation or application runbooks — by using the *bring your own
knowledge* (BYOK) feature.

BYOK works as follows:

1. You collect your content as a directory tree of Markdown (`.md`)
   files.
2. You run the BYOK tool on those files. The tool converts the
   content into a RAG database, packages that database into a container
   image, and writes the image to your local machine as an archive file.
3. You push the image to a container image registry that your cluster can
   access, such as `quay.io`.
4. You reference the image in your `OLSConfig` custom resource (CR). The
   OpenShift Lightspeed Operator deploys the image alongside the built-in
   RAG database (which you can also disable, see below), and the service
   can then use your content when generating answers.
5. You can repeat this process with several content sets: the service
   supports multiple BYOK images at the same time, each listed as a
   separate entry in `spec.ols.rag`.

The examples in this procedure use `quay.io` as the registry, with the
image path `quay.io/<username>/my-byok-image:latest`.

[NOTE]
====
The generated container image is immutable: it is a snapshot of your
Markdown content at the time you ran the BYOK tool. If your content
changes, the image does not update automatically. To make new content
available to the service, run the BYOK tool again and push the new image
to the same registry path; no `OLSConfig` CR change is needed. The
OpenShift Lightspeed Operator periodically re-imports the referenced
image tags and, when it detects new content, redeploys the service with
the updated RAG database.
====

[IMPORTANT]
====
BYOK is a Technology Preview feature. Technology
Preview features are not supported with Red Hat production service level
agreements (SLAs) and might not be functionally complete. Red Hat does not
recommend using them in production. These features provide early access to
upcoming product features, enabling customers to test functionality and
provide feedback during the development process.

For more information about the support scope of Red Hat Technology Preview
features, see _Technology Preview Features Support Scope_.
====

### Title and URL metadata in your Markdown files

Each Markdown file can carry a title and a URL. The BYOK tool passes
these through to the RAG database, and the service returns them with its
answers so that the console can show the source of the information: the
title identifies the source document and the URL becomes the link in the
listed sources. How each is determined, in order of precedence:

- **Title**: from a `title:` key in the file's YAML front matter; if
  absent, from the first level-1 heading (`# ...`); if neither is
  present, the file path is used.
- **URL**: from a `url:` key in the file's YAML front matter.

For example, a file beginning with

```
---
title: Runbook: restarting the payment service
url: https://wiki.example.com/runbooks/payment-restart
---
```

is listed among the answer's sources with the title *Runbook: restarting
the payment service* and links to the given URL.

> **Important**: provide a `url:` key (with a valid URL) in the front
> matter of every file for which you want sources listed. If a file has
> no `url:` key, its content is still indexed and used, but it cannot be
> shown as a source, because there is no URL to link to.

### Prerequisites

- You are logged in to the OpenShift Container Platform web console as a
  user with permission to edit the cluster-scoped `OLSConfig` custom
  resource (CR), such as a user with the `cluster-admin` role.
- You have an LLM provider available for use with the OpenShift Lightspeed
  Service.
- You have installed the OpenShift Lightspeed Operator.
- Your custom content consists of Markdown files with `.md` extensions.
  The tool does not support other file formats.
- You have logged in to `registry.redhat.io` by using Podman. You need
  this to download the BYOK tool image.
- You have an account for a container image registry, such as `quay.io`,
  to which you can push images.

### Procedure

1. Generate a container image from your Markdown files by running the
   BYOK tool:

   ```
   $ podman run -it --rm \
       -v <dir_tree_with_markdown_files>:/markdown:Z \
       -v <dir_for_image_tar>:/output:Z \
       -e OUT_IMAGE_TAG=my-byok-image \
       registry.redhat.io/openshift-lightspeed-tech-preview/lightspeed-rag-tool-rhel9:latest
   ```

   The tool reads the Markdown files from `/markdown`, converts them into a
   RAG database, and writes the resulting container image to
   `/output/my-byok-image.tar`.

   The optional `OUT_IMAGE_TAG` environment variable sets the repository
   tag for the generated image (default: `byok-image`). The optional
   `VECTOR_DB_INDEX` environment variable sets the identifier for the
   vector database index (default: `vector_db_index`).

   The tool assembles the image archive entirely on your machine. It does
   not need a container runtime, registry access, or elevated privileges;
   the base filesystem of the output image is built into the tool image.

2. Load the generated image into your local Podman image store:

   ```
   $ podman load < <dir_for_image_tar>/my-byok-image.tar
   ```

3. Confirm that the image is present:

   ```
   $ podman images
   ```

   This command returns an output similar to the following example:

   ```
   REPOSITORY                            TAG                IMAGE ID      CREATED       SIZE
   localhost/my-byok-image               latest             be7d1770bf10  1 minute ago  2.37 GB
   ...
   ```

4. Tag the image with your registry's path:

   ```
   $ podman tag localhost/my-byok-image:latest quay.io/<username>/my-byok-image:latest
   ```

5. Push the image to your registry:

   ```
   $ podman push quay.io/<username>/my-byok-image:latest
   ```

6. Reference the image in your `OLSConfig` CR so that the Operator deploys
   your RAG database alongside the built-in one:

   1. In the OpenShift Container Platform web console, click *Operators →
      Installed Operators*.
   2. Select *All Projects* in the *Project* dropdown at the top of the
      screen.
   3. Click *OpenShift Lightspeed Operator*.
   4. Click *OLSConfig*, then click the `cluster` configuration instance
      in the list.
   5. Click the *YAML* tab.
   6. Insert the `spec.ols.rag` YAML code:

      ```yaml
      apiVersion: ols.openshift.io/v1alpha1
      kind: OLSConfig
      metadata:
        name: cluster
      spec:
        ols:
          rag:
          - image: quay.io/<username>/my-byok-image:latest
      ```

      Each entry in `spec.ols.rag` points to one image that you pushed to
      a registry. You can list more than one RAG database image; the
      Operator deploys all of them.

   7. Optional: if your registry is private and the standard cluster-wide
      pull secret cannot access it, add pull secrets to the
      `spec.ols.imagePullSecrets` section:

      ```yaml
      apiVersion: ols.openshift.io/v1alpha1
      kind: OLSConfig
      metadata:
        name: cluster
        namespace: openshift-lightspeed
      spec:
        llm:
          providers: ...
        ols:
          imagePullSecrets:
          - name: <my_pull_secret_1>
          - name: <my_pull_secret_2>
      ```

      The secrets are a general list, not tied to specific images: for
      every BYOK image, the system tries each pull secret in
      order until authentication succeeds.

   8. Click *Save*.

### Verification

Open the OpenShift Lightspeed intelligent assistant and submit a question
that is answerable only from your custom content.

The assistant generates a response based on that content.

---

### If you want the service to use only your content

The service still uses the built-in OpenShift Container Platform
documentation database even after you add your own. To restrict the service
to the RAG databases you provide, see
"Disabling the OpenShift Container Platform documentation RAG database"
(`spec.ols.byokRAGOnly`).

---

Notes for the docs team:

- The "logged in to `registry.redhat.io`" prerequisite is kept because the
  tool image itself still comes from there; only the customer-runtime pull
  of a base image is gone.
- Section 1.13.3 (`byokRAGOnly`) needs no changes for the Go port.
