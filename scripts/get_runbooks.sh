#!/bin/bash
set -eou pipefail

rm -rf runbooks
git clone --single-branch --branch master --no-checkout --filter=blob:none https://github.com/openshift/runbooks.git
cd runbooks
git sparse-checkout init --cone
git sparse-checkout set alerts
git checkout
find . -mindepth 1 -maxdepth 1 ! -name 'alerts' -exec rm -rf {} \;
find . -type f \( ! -name '*.md' -o -name README.md \) -exec rm -rf {} \;
find . -depth -type d \( -empty -o -name deprecated \) -exec rm -rf {} \;
