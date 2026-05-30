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
./install.sh /path/to/target/project
```

The script copies `_extensions/probity/` into the target and validates the
installation.

### Option B: quarto add

```bash
cd /path/to/target/project
quarto add /path/to/probity_doc/_extensions    # note: the _extensions dir, not the subdirectory
```

### Option C: manual copy

```bash
cp -r _extensions/probity /path/to/target/project/_extensions/
```

### Important: directory structure

Quarto discovers extensions by walking up from the document to the project root
looking for `_extensions/`. For documents in subdirectories (e.g.
`pipeline/docs/report.qmd`), two things are required:

1. `_extensions/probity/` must live at the project root.
2. A `_quarto.yml` must exist at the project root (even a minimal one) so Quarto
   can identify the project boundary.

```
my-project/
  _quarto.yml              # required — marks the project root
  _extensions/
    probity/
      _extension.yml
      reference.docx
  pipeline/
    docs/
      report.qmd          # format: probity-docx
```

A minimal `_quarto.yml`:

```yaml
project:
  title: "My Project"
```

Without `_quarto.yml`, Quarto will not walk up from subdirectories to find
`_extensions/`, and you will get "Unable to read the extension 'probity'".

## Troubleshooting

### `Unable to read the extension 'probity'`

Quarto cannot find or parse the extension. The most common cause when rendering
from a subdirectory is a **missing `_quarto.yml`** at the project root. Quarto
needs this file to know where the project boundary is, and it will not walk up
from subdirectories without it.

Check:
- A `_quarto.yml` exists at the project root (even a minimal one).
- `_extensions/probity/` is a direct child of the same directory as `_quarto.yml`.
- All options under `contributes.formats.docx` are valid docx format options.
  Do **not** put document-level metadata (`lang`, `title`, `date`) inside the
  format definition — those belong in the document's own front matter.

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
