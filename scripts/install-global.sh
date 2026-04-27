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
  Claude local marketplace path -> ${CLAUDE_MARKETPLACES_DIR}/soho-dev
  Cursor local plugin path -> ${CURSOR_LOCAL_PLUGINS_DIR}/soho

Next steps:
  Goose:
    restart Goose, then open the recipe:
      goose recipe open soho
    Note: Goose recipes do not appear as slash commands in an existing chat.

  Codex:
    restart Codex so it re-discovers ~/.agents/skills.
    Soho appears as skills, not as a public marketplace listing.

  Claude Code:
    run:
      claude plugin marketplace add ${CLAUDE_MARKETPLACES_DIR}/soho-dev
      claude plugin install soho@soho-dev
    The installer creates a local marketplace path; Claude Code still requires
    the two CLI commands above.

  Cursor:
    restart Cursor and verify the local plugin at:
      ${CURSOR_LOCAL_PLUGINS_DIR}/soho
    Cursor local plugin discovery is host-version-dependent.
EOF
