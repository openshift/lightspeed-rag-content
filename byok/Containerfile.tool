FROM registry.access.redhat.com/ubi9/ubi:latest
ARG OUT_IMAGE_TAG=byok-image
RUN dnf install -y buildah

USER 0
WORKDIR /workdir

COPY byok/Containerfile.output .

ENV _BUILDAH_STARTED_IN_USERNS=""
ENV BUILDAH_ISOLATION=chroot
ENV OUT_IMAGE_TAG=$OUT_IMAGE_TAG
CMD buildah build -t $OUT_IMAGE_TAG -f Containerfile.output -v /markdown:/markdown:ro . && rm -f /output/$OUT_IMAGE_TAG.tar && buildah push $OUT_IMAGE_TAG docker-archive:/output/$OUT_IMAGE_TAG.tar
