# Probity Data Analytics — Quarto Word template

A Quarto format extension that produces brand-compliant Word documents (`.docx`)
for Probity Data Analytics: navy/gold palette, Calibri type, logo header,
page-numbered footer, and styled tables.

## Quick start

```bash
cp template.qmd my-report.qmd     # start from the example
quarto render my-report.qmd       # produces my-report.docx
```

In the front matter, set:

```yaml
format: probity-docx
```

## What's here

| Path | Purpose |
|---|---|
| `_extensions/probity/` | The Quarto format extension (`probity-docx`) |
| `_extensions/probity/reference.docx` | Branded reference doc (generated) |
| `_extensions/probity/assets/` | Probity logo files |
| `template.qmd` | Starter document |
| `SKILL.md` | Full guide: usage, brand rules, writing voice |
| `build/make_reference.py` | Regenerates `reference.docx` |
| `install.sh` | Helper script to install into another project |

## Using it in another project

### Option A: install script (recommended)

```bash
# From the probity_doc repo:
./install.sh /path/to/target/project                 # document at the project root
./install.sh /path/to/target/project pipeline/docs   # document in a subdirectory
```

The script copies `_extensions/probity/` into the target, creates a minimal
`_quarto.yml` at the project root if one is missing, and validates the
installation. If the document will live in a **subdirectory**, pass that
subdirectory as a second argument — the script then also places the extension
next to the document, which avoids the subdirectory-discovery failure below. The
default is a copy (portable, Windows-safe); `--link` makes a relative symlink
instead on Unix.

### Option B: quarto add

```bash
cd /path/to/target/project
quarto add /path/to/probity_doc/_extensions    # note: the _extensions dir, not the subdirectory
```

`quarto add` does **not** create a `_quarto.yml`. Without one at the project
root, a document in a subdirectory will fail with `Unable to read the extension`
(see below) — add a minimal `_quarto.yml` yourself, or use Option A.

### Option C: manual copy

```bash
cp -r _extensions/probity /path/to/target/project/_extensions/
```

### Important: directory structure

A document **at the project root** — beside `_extensions/` and `_quarto.yml` —
renders with no special handling:

```
my-project/
  _quarto.yml              # marks the project root
  _extensions/
    probity/
  report.qmd               # format: probity-docx
```

Quarto discovers `_extensions/` by walking up from the document only as far as
the project root (the nearest ancestor with a `_quarto.yml`). A document in a
**subdirectory** fails with `Unable to read the extension 'probity'` when that
walk-up cannot reach the extension — in two common cases:

1. **No `_quarto.yml` at the project root** (e.g. after `quarto add`): the
   document's own directory becomes the project root and only
   `<docdir>/_extensions/` is searched.
2. **An intermediate `_quarto.yml`** between the document and `_extensions/`: it
   re-anchors the project root below the extension, so the walk-up stops short.

The reliable fix is to **co-locate the extension with the document**. The install
script does this when you pass the document's subdirectory:

```bash
./install.sh my-project pipeline/docs
```

```
my-project/
  _quarto.yml
  _extensions/
    probity/                 # project-root copy
  pipeline/
    docs/
      _extensions/
        probity/             # co-located copy, next to the document
      report.qmd             # format: probity-docx
```

Use `--link` to symlink the co-located copy back to the project-root one instead
of duplicating it (Unix only; the script falls back to a copy if a working
symlink cannot be created). A co-located extension also resolves any figure that
references `_extensions/probity/assets/...` from the subdirectory. Minimal
`_quarto.yml`:

```yaml
project:
  title: "My Project"
```

## Troubleshooting

### `Unable to read the extension 'probity'`

Quarto could not discover `_extensions/` while walking up from the document to
the project root. The usual causes when rendering from a subdirectory are a
**missing `_quarto.yml`** at the project root (e.g. after `quarto add`) or an
**intermediate `_quarto.yml`** that re-anchors the root below `_extensions/`.

Fixes:
- For a document at the project root: ensure a `_quarto.yml` exists there, and
  that `_extensions/probity/` is a direct child of the same directory.
- For a document in a subdirectory: co-locate the extension with it —
  `./install.sh <project> <doc-subdir>` (see [Important: directory
  structure](#important-directory-structure)).
- Also confirm all options under `contributes.formats.docx` are valid docx
  format options. Do **not** put document-level metadata (`lang`, `title`,
  `date`) inside the format definition — those belong in the document's own
  front matter.

### `Invalid extension` / `Found 0 extensions`

This error comes from `quarto add`. The local path must point to the
**`_extensions` directory itself**, not to the extension subdirectory:

```bash
# Correct — points to _extensions/ (contains probity/ inside it)
quarto add /path/to/probity_doc/_extensions

# Wrong — points to probity/ (quarto add cannot validate this)
quarto add /path/to/probity_doc/_extensions/probity
```

If `quarto add` still fails, use the install script or manual copy instead.

### Document-level options

Set these in your `.qmd` front matter, not inside the format block:

```yaml
---
title: "Report Title"
author: "Author"
date: today
format: probity-docx
lang: en-GB          # document-level, not format-level
---
```

## Rebuilding the reference doc

`reference.docx` is generated. Edit the palette/header/footer in
`build/make_reference.py`, then:

```bash
python3 build/make_reference.py
quarto render template.qmd
```

See `SKILL.md` for the complete brand specification and writing voice.
