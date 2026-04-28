#!/bin/bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT_DIR="${1:-$(pwd)}"
COMMANDS_DIR="${PROJECT_DIR}/.cursor/commands"

if [ ! -d "${PROJECT_DIR}" ]; then
  echo "ERROR: project directory does not exist: ${PROJECT_DIR}" >&2
  exit 1
fi

mkdir -p "${COMMANDS_DIR}"

for command_file in "${REPO_DIR}/commands/"*.md; do
  cp "${command_file}" "${COMMANDS_DIR}/$(basename "${command_file}")"
done

cat <<EOF
Soho Cursor commands installed.

Project:
  ${PROJECT_DIR}

Commands:
  ${COMMANDS_DIR}/soho.md
  ${COMMANDS_DIR}/soho-plan.md
  ${COMMANDS_DIR}/soho-swarm.md

Cursor:
  Open or reload this project, then type /soho in Cursor chat.
EOF
