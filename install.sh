#!/usr/bin/env bash
# install.sh — Install the probity-docx Quarto extension into a target project.
#
# Usage:
#   ./install.sh                                   # install into the current directory
#   ./install.sh <project-dir>                     # install at the project root
#   ./install.sh <project-dir> <deck-subdir>       # also make the extension resolvable
#                                                  # from a document kept in a subdirectory
#                                                  # (copies the extension next to it)
#   ./install.sh --link <project-dir> <deck-subdir>
#                                                  # as above, but symlink instead of copy
#                                                  # (Unix filesystems only — see below)
#
# The script copies _extensions/probity/ into the target and verifies that the
# extension is readable by Quarto. Use this when `quarto add` from a local path
# does not work.
#
# Why <deck-subdir> exists
#   Quarto discovers `_extensions/` by walking up from the .qmd only as far as the
#   project root — the nearest ancestor directory containing a `_quarto.yml`. A root
#   `_quarto.yml` (which this script creates) is enough for discovery in the simple
#   case, but a document in a subdirectory still fails when there is no root
#   `_quarto.yml` (e.g. after `quarto add`) or an intermediate `_quarto.yml`
#   re-anchors the project root below `_extensions/`:
#     "Unable to read the extension 'probity'".
#   (The branded logo is baked into reference.docx, so unlike the PDF template there
#   is no extra logo-path problem — but any figure that references
#   `_extensions/probity/assets/...` from a subdirectory would also resolve once the
#   extension is co-located.)
#   Co-locating the extension with the document fixes this. Pass <deck-subdir> to do it.
#
#   The default is a copy because it is self-contained and portable: it survives
#   zipping, emailing, and moving to another machine, and it works on Windows.
#   --link makes a relative symlink instead (one source of truth, no duplication),
#   but symlinks need Administrator/Developer Mode on Windows and do not survive
#   being zipped or copied off the filesystem; the script falls back to a copy if
#   the symlink cannot be created or resolved.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXT_SRC="${SCRIPT_DIR}/_extensions/probity"

LINK_MODE=0
ARGS=()
for arg in "$@"; do
    case "$arg" in
        --link) LINK_MODE=1 ;;
        -h|--help)
            sed -n '2,41p' "$0" | sed 's/^# \{0,1\}//'
            exit 0 ;;
        *) ARGS+=("$arg") ;;
    esac
done

TARGET="${ARGS[0]:-.}"
DECK_SUBDIR="${ARGS[1]:-}"

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

TARGET="$(cd "${TARGET}" && pwd)"   # absolute, normalised
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

# ---- optional: co-locate the extension with a document in a subdirectory ----
if [ -n "${DECK_SUBDIR}" ]; then
    DECK_DIR="${TARGET}/${DECK_SUBDIR}"
    mkdir -p "${DECK_DIR}"
    DECK_DIR="$(cd "${DECK_DIR}" && pwd)"
    DEST="${DECK_DIR}/_extensions"

    if [ "${DECK_DIR}" = "${TARGET}" ]; then
        echo "  Document subdirectory is the project root; nothing extra to do."
    else
        linked=0
        if [ "${LINK_MODE}" -eq 1 ]; then
            if [ -e "${DEST}" ] && [ ! -L "${DEST}" ]; then
                echo "  Note: '${DEST}' is an existing directory; symlinking would shadow it. Copying instead."
            else
                [ -L "${DEST}" ] && rm -f "${DEST}"
                if command -v python3 >/dev/null 2>&1; then
                    REL="$(python3 -c 'import os,sys; print(os.path.relpath(sys.argv[1], sys.argv[2]))' "${TARGET}/_extensions" "${DECK_DIR}")"
                else
                    REL="${TARGET}/_extensions"   # absolute fallback target
                fi
                if ln -s "${REL}" "${DEST}" 2>/dev/null && [ -r "${DEST}/probity/_extension.yml" ]; then
                    echo "  Linked ${DECK_SUBDIR}/_extensions -> ${REL}"
                    linked=1
                else
                    rm -f "${DEST}" 2>/dev/null || true
                    echo "  Note: could not create a working symlink here; copying instead."
                fi
            fi
        fi
        if [ "${linked}" -eq 0 ]; then
            [ -L "${DEST}" ] && rm -f "${DEST}"
            mkdir -p "${DEST}"
            rm -rf "${DEST}/probity"
            cp -r "${EXT_SRC}" "${DEST}/"
            echo "  Copied extension into ${DECK_SUBDIR}/_extensions/probity/ (self-contained, portable)"
        fi
    fi
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
echo "A document at the project root renders with no special handling. If a"
echo "document in a subdirectory reports \"Unable to read the extension\", re-run"
echo "this script with the subdirectory as the second argument, e.g.:"
echo "    bash install.sh ${TARGET} pipeline/docs"
