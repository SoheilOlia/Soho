#!/bin/bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MIRROR_DIR="${SOHO_SKILLS_MIRROR_DIR:-$HOME/skills/soho/skills}"

if [ ! -d "${MIRROR_DIR}" ]; then
  echo "Soho skills mirror not found; skipping mirror check: ${MIRROR_DIR}"
  exit 0
fi

diff -qr "${REPO_DIR}/skills" "${MIRROR_DIR}"
echo "Soho skills mirror matches: ${MIRROR_DIR}"
