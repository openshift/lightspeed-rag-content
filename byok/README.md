# BYOK tooling HOWTO

These are quick notes on how to build and run OpenShift Lightspeed BYOK tooling. The rest of the text assumes you created the
`quay.io/$USERNAME/tool` container repository and corrected the first line in byok/Containerfile.output accordingly:

```Containerfile
FROM quay.io/$USERNAME/tool:latest as tool
```

## Design

The tool image, quay.io/$USERNAME/tool:latest, which wraps buildah, byok/Containerfile.output and the RAG embeddings
generation script with its Python dependencies. The purpose of the tool image is to encapsulate in a container everything
needed to build a BYOK container image. There are two mandatory parameters: the input directory with the user-provided
content and an output directory for the resulting container image. byok/Containerfile.output is the Containerfile
for resulting image containing the RAG database.

## These steps will be done during the OLS build:

Only used for your experimentation and once released will be replaced with a real image tag under registry.redhat.io/openshift-lightspeed-tech-preview.

### Build and push the BYOK tool image.

```bash
$ podman build -t quay.io/$USERNAME/tool:latest -f byok/Containerfile.tool .
$ podman push quay.io/$USERNAME/tool:latest
```

## This is how the user runs the BYOK tool:

```bash
$ podman run -e OUT_IMAGE_TAG=my-byok-image -it --rm --device=/dev/fuse -v <dir_tree_with_markdown_files>:/markdown:Z -v <dir_for_image_tar>:/output:Z quay.io/$USERNAME/tool:latest
```

The tool runs on CPUs, not GPUs.

There are two mandatory parameters:

- <dir_tree_with_markdown_files> is the root of the directory tree containing the content to be included in the BYOK RAG database, in Markdown. It is accessed for reading.
- <dir_for_image_tar> is the directory where the resulting image tar archive will be written. It needs to be writable.

The OUT_IMAGE_TAG environment variable can be used to override the tag of the generated image. It defaults to "byok-image".

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
The database is located at /rag/vector_db and the Faiss index id is "vector_db_index".
