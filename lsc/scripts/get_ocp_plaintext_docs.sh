#!/bin/bash
set -eou pipefail

OCP_VERSION=$1

trap "rm -rf openshift-docs" EXIT

rm -rf ocp-product-docs-plaintext/${OCP_VERSION}

git clone --single-branch --branch enterprise-${OCP_VERSION} https://github.com/openshift/openshift-docs.git

python scripts/asciidoctor-text/convert-it-all.py -i openshift-docs -t openshift-docs/_topic_maps/_topic_map.yml \
    -d openshift-enterprise -o ocp-product-docs-plaintext/${OCP_VERSION} -a scripts/asciidoctor-text/${OCP_VERSION}/attributes.yaml

for f in $(cat config/exclude.conf); do
    rm ocp-product-docs-plaintext/${OCP_VERSION}/$f
done
