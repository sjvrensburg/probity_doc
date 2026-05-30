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

## Using it in another project

```bash
quarto add ./_extensions/probity
```

or copy `_extensions/probity/` into the target project, then set
`format: probity-docx`.

## Rebuilding the reference doc

`reference.docx` is generated. Edit the palette/header/footer in
`build/make_reference.py`, then:

```bash
python3 build/make_reference.py
quarto render template.qmd
```

See `SKILL.md` for the complete brand specification and writing voice.
