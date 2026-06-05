#!/usr/bin/env bash
# GPU host setup + embed entrypoint (Konflux embed-rag remote podman step).
set -euo pipefail

HERMETIC="${HERMETIC:-true}"
CACHI2_SRC="${CACHI2_ROOT:-/var/workdir/cachi2}"
CACHI2_ROOT="/cachi2"

if [ -f /mnt/trusted-ca/ca-bundle.crt ]; then
  cp /mnt/trusted-ca/ca-bundle.crt /etc/pki/ca-trust/source/anchors/
  update-ca-trust
fi

prepare_cachi2() {
  if [ ! -f "${CACHI2_SRC}/cachi2.env" ]; then
    echo "Missing cachi2 prefetch: ${CACHI2_SRC}/cachi2.env" >&2
    return 1
  fi

  # Match buildah-remote-oci-ta: cachi2.env references file:///cachi2/...
  rm -rf /tmp/cachi2
  cp -a "${CACHI2_SRC}" /tmp/cachi2
  chmod -R go+rwX /tmp/cachi2

  arch=$(uname -m)
  rpm_prefetch_dir="/tmp/cachi2/output/deps/rpm"
  if [ -d "${rpm_prefetch_dir}" ]; then
    for path in "${rpm_prefetch_dir}"/*; do
      [ -e "${path}" ] || continue
      if [ "$(basename "${path}")" != "${arch}" ]; then
        rm -rf "${path}"
      fi
    done
  fi

  rm -rf /cachi2
  ln -sf /tmp/cachi2 /cachi2
}

install_rpms() {
  local packages=(python3.12 python3.12-pip libcudnn9 libnccl libcusparselt0)

  if [ "${HERMETIC}" = "true" ]; then
    # Prevent the CUDA base image from using host/RHSM repos.
    find /usr/share/rhel/secrets -type l -exec unlink {} \; 2>/dev/null || true

    prepare_cachi2

    # shellcheck disable=SC1091
    . /cachi2/cachi2.env

    dnf install -y "${packages[@]}"
  else
    dnf install -y "${packages[@]}"
  fi
}

install_rpms

test -d /var/workdir/source/scripts
cd /var/workdir/source
chmod +x ./scripts/embed-rag-content.sh ./scripts/embed-remote-setup.sh
export CACHI2_ROOT
exec ./scripts/embed-rag-content.sh
