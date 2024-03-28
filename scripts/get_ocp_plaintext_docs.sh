#!/bin/bash
set -eou pipefail

OCP_VERSION=$1

trap "rm -rf openshift-docs" EXIT

git clone --single-branch --branch enterprise-${OCP_VERSION} https://github.com/openshift/openshift-docs.git

echo "product-version: $OCP_VERSION" >> scripts/asciidoctor-text/attributes.yaml

python scripts/asciidoctor-text/convert-it-all.py -i openshift-docs -t openshift-docs/_topic_maps/_topic_map.yml -o ocp-product-docs-plaintext/${OCP_VERSION} -a scripts/asciidoctor-text/attributes.yaml
