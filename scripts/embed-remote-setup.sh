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

pkg_installed() {
  case "$1" in
    libcudnn9) rpm -qa | grep -q '^libcudnn9' ;;
    *) rpm -q "$1" &>/dev/null ;;
  esac
}

prepare_cachi2() {
  if [ ! -f "${CACHI2_SRC}/cachi2.env" ] && [ ! -f "${CACHI2_SRC}/prefetch.env" ]; then
    echo "Missing cachi2 prefetch: ${CACHI2_SRC}/cachi2.env" >&2
    return 1
  fi

  # Match buildah-remote-oci-ta: prefetched paths use file:///cachi2/...
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

source_prefetch_env() {
  if [ -f /cachi2/prefetch.env ]; then
    # shellcheck disable=SC1091
    . /cachi2/prefetch.env
  elif [ -f /cachi2/cachi2.env ]; then
    # shellcheck disable=SC1091
    . /cachi2/cachi2.env
  fi
}

enable_prefetched_repos() {
  local arch repos_src repo_file

  arch=$(uname -m)
  repos_src="/cachi2/output/deps/rpm/${arch}/repos.d"
  if [ ! -d "${repos_src}" ]; then
    echo "Missing prefetched rpm repos: ${repos_src}" >&2
    return 1
  fi

  # Same as buildah-remote: inject only regular *.repo files into /etc/yum.repos.d.
  find /usr/share/rhel/secrets -type l -exec unlink {} \; 2>/dev/null || true
  mkdir -p /etc/yum.repos.d
  rm -f /etc/yum.repos.d/*.repo

  shopt -s nullglob
  for repo_file in "${repos_src}"/*.repo; do
    cp "${repo_file}" /etc/yum.repos.d/
  done
  shopt -u nullglob

  if ! compgen -G "/etc/yum.repos.d/*.repo" >/dev/null; then
    echo "No prefetched .repo files found in ${repos_src}" >&2
    return 1
  fi
}

install_rpms() {
  local packages=(python3.12 python3.12-pip libcudnn9 libnccl libcusparselt0)
  local missing=()
  local pkg

  if [ -n "${TEST_INSTALL_PACKAGES:-}" ]; then
    # shellcheck disable=SC2206
    packages=(${TEST_INSTALL_PACKAGES})
  fi

  for pkg in "${packages[@]}"; do
    if ! pkg_installed "${pkg}"; then
      missing+=("${pkg}")
    fi
  done

  if [ "${#missing[@]}" -eq 0 ]; then
    echo "Required RPMs already present in builder image"
    return 0
  fi

  echo "Installing missing RPMs: ${missing[*]}"

  if [ "${HERMETIC}" = "true" ]; then
    prepare_cachi2
    enable_prefetched_repos
    source_prefetch_env
    dnf install -y "${missing[@]}"
  else
    dnf install -y "${missing[@]}"
  fi
}

install_rpms

if [ "${EMBED_REMOTE_SETUP_ONLY:-false}" = "true" ]; then
  echo "EMBED_REMOTE_SETUP_ONLY: skipping GPU embed"
  exit 0
fi

test -d /var/workdir/source/scripts
cd /var/workdir/source
chmod +x ./scripts/embed-rag-content.sh ./scripts/embed-remote-setup.sh
export CACHI2_ROOT
exec ./scripts/embed-rag-content.sh
