#!/bin/bash
set -euo pipefail

SOHO_REPO_URL="${SOHO_REPO_URL:-https://github.com/SoheilOlia/Soho.git}"
SOHO_INSTALL_DIR="${SOHO_INSTALL_DIR:-$HOME/agent-plugins/soho}"

mkdir -p "$(dirname "${SOHO_INSTALL_DIR}")"

if [ -d "${SOHO_INSTALL_DIR}/.git" ]; then
  echo "Updating existing Soho clone at ${SOHO_INSTALL_DIR}"
  git -C "${SOHO_INSTALL_DIR}" pull --ff-only
else
  if [ -e "${SOHO_INSTALL_DIR}" ]; then
    echo "Target path exists but is not a git clone: ${SOHO_INSTALL_DIR}" >&2
    exit 1
  fi
  echo "Cloning Soho into ${SOHO_INSTALL_DIR}"
  git clone "${SOHO_REPO_URL}" "${SOHO_INSTALL_DIR}"
fi

cd "${SOHO_INSTALL_DIR}"
./scripts/install-global.sh
