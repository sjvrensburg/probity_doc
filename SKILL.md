---
name: probity-quarto-docx
description: "Create branded Word documents for Probity Data Analytics using the Quarto reference-doc template in this repository. Use this skill whenever the user asks to write, draft, restyle, or produce a Probity Word document (.docx) from Quarto or Markdown: methodology write-ups, technical reports, audit-trail documents, memos, proposals, client deliverables, or anything that will leave the studio under the Probity name. Trigger it even when the user only says 'make a Probity report', 'use our Word template', 'apply our branding', or attaches a Quarto/Markdown file to convert. It pins down the navy/gold palette, Calibri type, logo header, page-numbered footer, table styling, and the Probity writing voice."
---

# Probity Data Analytics — Quarto Word template

This skill produces brand-compliant Word documents (`.docx`) for Probity Data
Analytics through Quarto, using a pre-built `reference.docx` that carries the
house style: navy/gold palette, Calibri, navy headings, a logo header, and a
page-numbered footer.

The template is a Quarto **format extension** named `probity`, living in
`_extensions/probity/`. Authors write plain Quarto (`.qmd`) or Markdown and
select `format: probity-docx`. All chrome and styling comes from the reference
doc; authors never touch Word styles by hand.

## Quick reference

| Element | Value |
|---|---|
| Primary navy | `#0A325A` |
| Deep navy | `#062340` |
| Mid blue | `#4A7BA8` |
| Light blue | `#8BABCB` |
| Pale blue tint | `#E8EEF5` |
| Off-background | `#F7F9FC` |
| Gold accent | `#C8881F` (reserved, not for body or chart fills) |
| Body text | `#1F2937` |
| Muted text | `#6B7280` |
| Rule / hairline | `#D5DEE9` |
| Primary font | Calibri (Arial fallback) |
| Mono / code | Consolas |
| Output format | `probity-docx` |
| Reference doc | `_extensions/probity/reference.docx` |
| Logo assets | `_extensions/probity/assets/` |

## How to use the template

### 1. Render an existing document

If a `.qmd` already declares `format: probity-docx`, render it from the repo root:

```bash
quarto render path/to/document.qmd
```

The extension must be discoverable. Quarto finds `_extensions/probity/`
automatically when the document is inside this repository (or any directory
where `_extensions/probity/` is on the path up to the project root).

### 2. Start a new document

Copy `template.qmd` and edit the front matter and body:

```bash
cp template.qmd my-report.qmd
```

Minimum front matter:

```yaml
---
title: "Document Title"
subtitle: "A short descriptive subtitle"
author: "Author Name, Role"
date: today
format: probity-docx
abstract: |
  One short paragraph: what this document is and what it concludes.
---
```

`title` renders as the big navy heading, `subtitle` as the mid-blue line,
`author` and `date` as muted lines, `abstract` as a centred summary block. A
table of contents is on by default (`toc: true`, depth 3); set `toc: false` in
the front matter to drop it.

### 3. Use the template in another project

To brand documents outside this repo, install the extension into the target
project. Three methods:

**Install script (recommended):**

```bash
./install.sh /path/to/target/project
```

**quarto add:**

```bash
cd /path/to/target/project
quarto add /path/to/probity_doc/_extensions
```

Note: point `quarto add` at the `_extensions` directory itself, not at the
`_extensions/probity` subdirectory.

**Manual copy:**

```bash
cp -r _extensions/probity /path/to/target/project/_extensions/
```

Then set `format: probity-docx` in the document's front matter. The
`_extensions/` directory must be in a parent directory of the document (at the
project root), not next to the document itself. Document-level options like
`lang: en-GB` go in the document front matter, not inside the format block.

**Required: `_quarto.yml` at the project root.** Quarto uses this file to
identify the project boundary. Without it, documents in subdirectories (e.g.
`pipeline/docs/report.qmd`) will fail with "Unable to read the extension".
A minimal file is enough:

```yaml
project:
  title: "My Project"
```

The install script creates one automatically if missing.

## What the template gives you automatically

- **Header**: the navy Probity wordmark top-left, a muted "Data Analytics" tag
  right-aligned, and a thin navy hairline below. Appears on every body page.
- **Footer**: bold navy "Probity Data Analytics", a muted " · Confidential"
  tag, and a right-aligned "Page X of Y", over a hairline rule.
- **Title block**: navy title (30pt), mid-blue subtitle, muted author and date,
  centred abstract.
- **Headings**: H1 navy 18pt bold, H2 navy 14pt bold, H3 deep-navy 12pt bold,
  H4-H6 deep-navy bold italic. All Calibri.
- **Tables**: navy header row with white bold text, hairline body rows, no side
  borders. Pipe tables in Markdown pick this up with no extra work.
- **Body**: Calibri 11pt, body-text grey, comfortable line spacing, A4 page.

To change the footer tag (for example "Draft" instead of "Confidential") or the
logo size, edit `build/make_reference.py` and rebuild (see below). Do not hand
-edit `reference.docx`: it is a generated artefact.

## Authoring conventions inside the document

Write Markdown the normal way. A few Probity-specific patterns:

- **Bold navy lead-in** for caveat lists: start the line with `**Phrase.**`
  then continue in plain body text. Bold runs inherit navy from the theme.
- **Tables**: standard pipe tables. Add a caption with
  `: Caption text {#tbl-id}` on the line after the table.
- **Figures**: `![Caption](path){#fig-id width=60%}`. Captions render muted
  italic below the figure.
- **Blockquotes** (`>`) suit the honesty pattern: headline finding first, then
  what it depends on.
- **Code**: fenced blocks render in Consolas.

## Writing voice (non-negotiable)

These rules apply to every word in a Probity document. Apply them as you draft.

1. **No em dashes.** Replace with a colon, comma, full stop, parentheses, or a
   restructured sentence. Hyphens and en dashes in compounds are fine
   (`forward-looking`, `lag-1`, `out-of-sample`).
2. **UK spelling.** `rigour, behaviour, defence, analyse, recognised, modelled,
   centred, organisation, programme`. Keep native spelling in proper nouns
   (Stats SA, SARB, Bureau of Labor Statistics).
3. **Plain register.** Short sentences, one idea each. Active voice. Concrete
   nouns. Cut filler: "in order to" becomes "to"; drop "it should be noted
   that".
4. **Lead with the answer, then the qualification.** State the headline finding,
   then state the dependency or limitation in the very next sentence. Do not
   bury caveats.
5. **Honesty about limitations.** State sample sizes, regime dependencies, and
   out-of-sample residuals openly. When reporting model fit, lead with whether
   the sign matches theory, not with R².
6. **No AI-slop tells.** Avoid "delve into", "leverage", "unleash", "robust"
   (when vague), "holistic", "seamless", "navigate the landscape", "in today's
   fast-paced world", and emoji. No decorative full-width coloured bars or
   accent lines beyond the template's own hairlines.
7. **Smart typography.** Use `'`, `'`, `"`, `"` for quotes and apostrophes.
8. **Numbers.** Thousands separators (`R 14,903,239`). Percentages with no space
   (`12.5%`). Shorthand money `R 14.9M` in prose, full digits in tables. Dates:
   ISO `2024-06-30` in tables, "30 June 2024" in prose. Fiscal years
   `FY 2024/25`. Lag notation `lag-1`. Greek letters written out in prose,
   actual characters (`α`, `β₁`) in tables and equations.

## Workflow when producing a document

1. **Draft the content** in a `.qmd` with `format: probity-docx`, applying the
   voice rules above as you write (do not write loosely then clean up).
2. **Render**: `quarto render <file>.qmd`.
3. **Visual check**: convert to PDF and inspect pages.
   ```bash
   soffice -env:UserInstallation=file:///tmp/lohome --headless \
     --convert-to pdf <file>.docx --outdir build
   pdftoppm -png -r 90 build/<file>.pdf build/pg
   ```
   Confirm the logo header, navy headings, navy table headers, and footer page
   numbers are present.
4. **Voice pass**: grep the source for em dashes and US spellings, fix any hits.
   ```bash
   grep -nP '\xe2\x80\x94' <file>.qmd                 # em dash
   grep -niE 'color|analyze|behavior|defense|organization' <file>.qmd
   ```

## Rebuilding the reference doc

`reference.docx` is generated, not edited by hand. The generator is
`build/make_reference.py` (stdlib only). It takes pandoc's default reference doc
(`build/reference-default.docx`), applies the palette, fonts, heading colours,
and table style, and injects the logo header and page-numbered footer.

To change styling (colours, sizes, footer tag, logo dimensions), edit the
palette constants or the `HEADER`/`FOOTER` strings near the top of the script,
then rebuild:

```bash
python3 build/make_reference.py
quarto render template.qmd        # confirm it still renders
```

If `build/reference-default.docx` is missing, regenerate it first:

```bash
pandoc -o build/reference-default.docx --print-default-data-file reference.docx
```

## Files in this template

- `_extensions/probity/_extension.yml` — Quarto format definition (`probity-docx`)
- `_extensions/probity/reference.docx` — generated branded reference doc
- `_extensions/probity/assets/` — logo files:
  - `logo.png` — full logo, navy on white (2816×1536)
  - `logo_trim.png` — whitespace-trimmed (2283×708), for cover marks on white
  - `logo_white.png` — white-line version for dark backgrounds
  - `logo_navy_small.png` — small navy wordmark (1400×434), used in the header
- `template.qmd` — starter document, copy to begin
- `build/make_reference.py` — reference-doc generator
- `build/reference-default.docx` — pandoc default, generator input
