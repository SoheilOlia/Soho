#!/bin/bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="${DIST_DIR:-${REPO_DIR}/dist}"
BUILD_DIR="${BUILD_DIR:-${REPO_DIR}/build/dmg}"
STAGE_DIR="${BUILD_DIR}/stage"
SOURCE_DIR="${STAGE_DIR}/Soho"
INSTALLER_PATH="${STAGE_DIR}/Install Soho.command"
README_PATH="${STAGE_DIR}/README.txt"
DRY_RUN="${SOHO_DMG_DRY_RUN:-0}"

command -v python3 >/dev/null 2>&1 || {
  echo "ERROR: python3 is required." >&2
  exit 1
}

VERSION="${SOHO_VERSION:-$(python3 - "${REPO_DIR}" <<'PY'
import json
import sys
from pathlib import Path

repo = Path(sys.argv[1])
manifest = json.loads((repo / ".claude-plugin" / "plugin.json").read_text())
print(manifest["version"])
PY
)}"

DMG_NAME="${SOHO_DMG_NAME:-Soho-${VERSION}.dmg}"
DMG_PATH="${DIST_DIR}/${DMG_NAME}"
VOLUME_NAME="${SOHO_DMG_VOLUME_NAME:-Soho ${VERSION}}"

command -v rsync >/dev/null 2>&1 || {
  echo "ERROR: rsync is required." >&2
  exit 1
}

if [ "${DRY_RUN}" != "1" ]; then
  command -v hdiutil >/dev/null 2>&1 || {
    echo "ERROR: hdiutil is required to build a DMG. Run this on macOS." >&2
    exit 1
  }
fi

python3 "${REPO_DIR}/scripts/validate.py"

rm -rf "${BUILD_DIR}"
mkdir -p "${SOURCE_DIR}" "${DIST_DIR}"

rsync -a --delete \
  --exclude ".git" \
  --exclude ".DS_Store" \
  --exclude "__pycache__" \
  --exclude ".pytest_cache" \
  --exclude ".venv" \
  --exclude "build" \
  --exclude "dist" \
  --exclude "*.bak" \
  --exclude "*.swp" \
  --exclude "*~" \
  "${REPO_DIR}/" "${SOURCE_DIR}/"

cat > "${INSTALLER_PATH}" <<INSTALLER
#!/bin/bash
set -euo pipefail

echo "Soho Installer"
echo

SOURCE_DIR="\$(cd "\$(dirname "\$0")/Soho" && pwd)"
INSTALL_DIR="\${SOHO_INSTALL_DIR:-\$HOME/agent-plugins/soho}"

if [ -e "\${INSTALL_DIR}" ] || [ -L "\${INSTALL_DIR}" ]; then
  BACKUP_DIR="\${INSTALL_DIR}.backup-\$(date +%Y%m%d-%H%M%S)"
  echo "Existing Soho install found:"
  echo "  \${INSTALL_DIR}"
  echo "Moving it to:"
  echo "  \${BACKUP_DIR}"
  mv "\${INSTALL_DIR}" "\${BACKUP_DIR}"
fi

mkdir -p "\$(dirname "\${INSTALL_DIR}")"
echo "Copying Soho ${VERSION} to:"
echo "  \${INSTALL_DIR}"
rsync -a "\${SOURCE_DIR}/" "\${INSTALL_DIR}/"

cd "\${INSTALL_DIR}"
./scripts/install-global.sh

if command -v claude >/dev/null 2>&1; then
  echo
  echo "Installing Soho into Claude Code through the Claude CLI..."
  claude plugin marketplace add "\$HOME/.claude/plugins/marketplaces/soho-dev" || true
  claude plugin install soho@soho-dev || true
else
  echo
  echo "Claude Code CLI not found. To install later, run:"
  echo "  claude plugin marketplace add ~/.claude/plugins/marketplaces/soho-dev"
  echo "  claude plugin install soho@soho-dev"
fi

echo
echo "Soho install complete."
echo "Goose: open with 'goose recipe open soho'."
echo "Codex/Cursor/Claude Code: restart the host so it reloads local files/plugins."

if [ -t 0 ]; then
  echo
  read -r -p "Press Return to close this window."
fi
INSTALLER

chmod +x "${INSTALLER_PATH}"

cat > "${README_PATH}" <<README
Soho ${VERSION}

Double-click "Install Soho.command" to install Soho globally on this Mac.

The installer copies the bundled Soho source to:
  ~/agent-plugins/soho

Then it runs:
  scripts/install-global.sh

After installation:
  Goose: goose recipe open soho
  Codex: restart Codex so it discovers ~/.agents/skills/soho
  Claude Code: restart Claude Code after plugin install
  Cursor: restart Cursor and verify local plugin discovery

This DMG is unsigned and not notarized. For public distribution, sign and notarize
the release artifact before broad use.
README

if [ "${DRY_RUN}" = "1" ]; then
  echo "Soho DMG dry run complete."
  echo "Staged files at: ${STAGE_DIR}"
  exit 0
fi

rm -f "${DMG_PATH}"
hdiutil create \
  -volname "${VOLUME_NAME}" \
  -srcfolder "${STAGE_DIR}" \
  -ov \
  -format UDZO \
  "${DMG_PATH}"

echo "Soho DMG created:"
echo "  ${DMG_PATH}"
