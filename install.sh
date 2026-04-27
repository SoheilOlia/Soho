#!/bin/bash
set -e

# SOHO Installer — Swarm Orchestration with Disciplined Methodology
# Installs the /soho recipe into your Goose config directory

RECIPE_DIR="${HOME}/.config/goose/recipes"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🌊 SOHO Installer"
echo "═══════════════════════════════════════"
echo ""

# Create recipes directory if it doesn't exist
mkdir -p "${RECIPE_DIR}"

# Copy main recipe
cp "${SCRIPT_DIR}/soho.yaml" "${RECIPE_DIR}/soho.yaml"
echo "✅ Installed soho.yaml → ${RECIPE_DIR}/soho.yaml"

# Copy sub-recipes (if they exist)
if [ -d "${SCRIPT_DIR}/sub-recipes" ]; then
    mkdir -p "${RECIPE_DIR}/sub-recipes"
    cp "${SCRIPT_DIR}/sub-recipes/"*.yaml "${RECIPE_DIR}/sub-recipes/"
    echo "✅ Installed $(ls "${SCRIPT_DIR}/sub-recipes/"*.yaml | wc -l | tr -d ' ') sub-recipes → ${RECIPE_DIR}/sub-recipes/"
fi

echo ""
echo "═══════════════════════════════════════"
echo "🌊 SOHO installed. Start a new Goose session and type /soho"
echo ""
echo "What's inside:"
echo "  • 14 auto-activating skills (from superpowers)"
echo "  • 16 specialized agent roles (from ruflo)"
echo "  • 4 swarm topologies (hierarchical, mesh, ring, star)"
echo "  • 3-mode decision system (auto-solo, auto-swarm, recommend)"
echo "  • 10 deep-dive sub-recipes"
echo "  • SPARC methodology"
echo ""
echo "To uninstall: rm ${RECIPE_DIR}/soho.yaml"
