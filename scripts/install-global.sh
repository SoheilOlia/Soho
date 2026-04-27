#!/bin/bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GOOSE_RECIPE_DIR="${GOOSE_RECIPE_DIR:-$HOME/.config/goose/recipes}"
CODEX_SKILLS_DIR="${CODEX_SKILLS_DIR:-$HOME/.agents/skills}"
CLAUDE_MARKETPLACES_DIR="${CLAUDE_MARKETPLACES_DIR:-$HOME/.claude/plugins/marketplaces}"
CURSOR_LOCAL_PLUGINS_DIR="${CURSOR_LOCAL_PLUGINS_DIR:-$HOME/.cursor/plugins/local}"

python3 "${REPO_DIR}/scripts/validate.py"

mkdir -p "${GOOSE_RECIPE_DIR}"
cp "${REPO_DIR}/soho.yaml" "${GOOSE_RECIPE_DIR}/soho.yaml"
mkdir -p "${GOOSE_RECIPE_DIR}/sub-recipes"
cp "${REPO_DIR}/sub-recipes/"*.yaml "${GOOSE_RECIPE_DIR}/sub-recipes/"

mkdir -p "${CODEX_SKILLS_DIR}"
ln -sfn "${REPO_DIR}/skills" "${CODEX_SKILLS_DIR}/soho"

mkdir -p "${CLAUDE_MARKETPLACES_DIR}"
ln -sfn "${REPO_DIR}" "${CLAUDE_MARKETPLACES_DIR}/soho-dev"

mkdir -p "${CURSOR_LOCAL_PLUGINS_DIR}"
ln -sfn "${REPO_DIR}" "${CURSOR_LOCAL_PLUGINS_DIR}/soho"

cat <<EOF
Soho global install complete.

Installed:
  Goose recipes -> ${GOOSE_RECIPE_DIR}
  Codex skills -> ${CODEX_SKILLS_DIR}/soho
  Claude marketplace -> ${CLAUDE_MARKETPLACES_DIR}/soho-dev
  Cursor local plugin -> ${CURSOR_LOCAL_PLUGINS_DIR}/soho

Next steps:
  Goose:
    restart Goose and run /soho

  Codex:
    restart Codex so it re-discovers ~/.agents/skills

  Claude Code:
    run:
      /plugin marketplace add ${CLAUDE_MARKETPLACES_DIR}/soho-dev
      /plugin install soho@soho-dev

  Cursor:
    restart Cursor and verify the local plugin at:
      ${CURSOR_LOCAL_PLUGINS_DIR}/soho
EOF
