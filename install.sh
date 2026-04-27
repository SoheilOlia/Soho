#!/bin/bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RECIPE_DIR="${HOME}/.config/goose/recipes"

echo "SOHO installer"
echo

python3 "${REPO_DIR}/scripts/validate.py"

mkdir -p "${RECIPE_DIR}"
cp "${REPO_DIR}/soho.yaml" "${RECIPE_DIR}/soho.yaml"

if [ -d "${REPO_DIR}/sub-recipes" ]; then
  mkdir -p "${RECIPE_DIR}/sub-recipes"
  cp "${REPO_DIR}/sub-recipes/"*.yaml "${RECIPE_DIR}/sub-recipes/"
fi

echo "Installed Goose recipe files to ${RECIPE_DIR}"
echo
echo "Next steps:"
echo "  1. Start Goose and run /soho"
echo "  2. For Codex / Claude / Cursor, use the local plugin manifests in this repo"
echo "  3. Read docs/capability-matrix.md before relying on host-dependent swarm behavior"
