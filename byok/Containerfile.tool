FROM registry.access.redhat.com/ubi9/ubi:latest
ARG OUT_IMAGE_TAG=byok-image
RUN dnf install -y buildah python3.11 python3.11-pip

USER 0
WORKDIR /workdir

COPY requirements.cpu.txt .
RUN pip3.11 install --no-cache-dir -r requirements.cpu.txt

COPY embeddings_model ./embeddings_model
COPY byok/generate_embeddings_tool.py byok/Containerfile.output .

ENV _BUILDAH_STARTED_IN_USERNS=""
ENV BUILDAH_ISOLATION=chroot
ENV OUT_IMAGE_TAG=$OUT_IMAGE_TAG
CMD buildah build -t $OUT_IMAGE_TAG -f Containerfile.output -v /markdown:/markdown:Z . && rm -f /output/$OUT_IMAGE_TAG.tar && buildah push $OUT_IMAGE_TAG docker-archive:/output/$OUT_IMAGE_TAG.tar
