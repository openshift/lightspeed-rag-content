#!/bin/bash 
VERSION=latest # 13
IMAGE_REPO=quay.io/redhat_emp1


podman build -f "src/dockerfile" -t rag-pipeline-tasks:${VERSION} "images/rag"
podman tag  rag-pipeline-tasks:${VERSION} ${IMAGE_REPO}/rag-pipeline-tasks:${VERSION}
podman push ${IMAGE_REPO}/rag-pipeline-tasks:${VERSION}