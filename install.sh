#!/usr/bin/env bash
set -euo pipefail

echo "Installing Mission-Forge..."

# Check required tools
if ! command -v python3 &>/dev/null && ! command -v python &>/dev/null; then
    echo "Error: python3 (or python) not found. Install it from https://python.org" >&2
    exit 1
fi

if ! command -v pip &>/dev/null && ! command -v pip3 &>/dev/null; then
    echo "Error: pip not found. Install it from https://python.org" >&2
    exit 1
fi

if ! command -v npx &>/dev/null; then
    echo "Error: npx not found. Install Node.js 18+ from https://nodejs.org" >&2
    exit 1
fi

pip install git+https://github.com/loudiman/Mission-Forge.git
npx -y skills add loudiman/Mission-Forge

echo "✓ missionforge CLI installed"
echo "✓ Agent skills installed"
echo "Run \`missionforge init MF-001\` to create your first mission."
