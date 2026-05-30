#!/usr/bin/env bash
# install.sh — Install the probity-docx Quarto extension into a target project.
#
# Usage:
#   ./install.sh /path/to/target/project
#   ./install.sh                  # installs into the current directory
#
# The script copies _extensions/probity/ into the target and verifies that
# the extension is readable by Quarto. Use this when `quarto add` from a
# local path does not work.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXT_SRC="${SCRIPT_DIR}/_extensions/probity"
TARGET="${1:-.}"

# ---- guards ----
if [ ! -f "${EXT_SRC}/_extension.yml" ]; then
    echo "ERROR: Cannot find _extensions/probity/_extension.yml in ${SCRIPT_DIR}" >&2
    echo "       Run this script from the probity_doc repository root." >&2
    exit 1
fi

if [ ! -f "${EXT_SRC}/reference.docx" ]; then
    echo "ERROR: reference.docx is missing from the extension." >&2
    echo "       Run: python3 build/make_reference.py" >&2
    exit 1
fi

if [ ! -d "${TARGET}" ]; then
    echo "ERROR: Target directory does not exist: ${TARGET}" >&2
    exit 1
fi

TARGET_EXT="${TARGET}/_extensions/probity"

# ---- install ----
echo "Installing probity-docx extension into: ${TARGET}"

# Remove a previous copy so stale files do not linger.
if [ -d "${TARGET_EXT}" ]; then
    echo "  Removing previous installation..."
    rm -rf "${TARGET_EXT}"
fi

mkdir -p "${TARGET_EXT}"
cp -r "${EXT_SRC}"/* "${TARGET_EXT}"/

# Copy assets directory if it exists (logos for header).
if [ -d "${EXT_SRC}/assets" ]; then
    cp -r "${EXT_SRC}/assets" "${TARGET_EXT}/"
fi

# ---- project root marker ----
# Quarto needs _quarto.yml at the project root to discover extensions when
# rendering documents inside subdirectories. Create a minimal one if missing.
QUARTO_YML="${TARGET}/_quarto.yml"
if [ ! -f "${QUARTO_YML}" ]; then
    echo "  Creating minimal _quarto.yml (needed for subdirectory discovery)..."
    cat > "${QUARTO_YML}" <<'YAML'
project:
  title: "Project"
YAML
fi

# ---- verify ----
echo "  Verifying extension files..."
required_files=(
    "_extension.yml"
    "reference.docx"
)
for f in "${required_files[@]}"; do
    if [ ! -f "${TARGET_EXT}/${f}" ]; then
        echo "ERROR: Expected file missing after install: ${TARGET_EXT}/${f}" >&2
        exit 1
    fi
done

echo "  Checking Quarto can read the extension..."
if command -v quarto &>/dev/null; then
    # quarto inspect will fail if the extension is malformed.
    if quarto inspect "${TARGET_EXT}/_extension.yml" &>/dev/null; then
        echo "  Quarto reports the extension is valid."
    else
        echo "  WARNING: quarto inspect reported an issue. The extension may still"
        echo "           work — try rendering a document with 'format: probity-docx'."
    fi
else
    echo "  (quarto not found on PATH; skipping validation)"
fi

echo ""
echo "Done. Add the following to your .qmd front matter:"
echo ""
echo "    format: probity-docx"
echo "    lang: en-GB"
echo ""
echo "If your documents are in a subdirectory, the _quarto.yml at the project"
echo "root ensures Quarto can discover the extension."
