#!/usr/bin/env python3
"""Build the Probity Data Analytics Quarto reference.docx.

Takes pandoc's default reference.docx, applies the Probity house style
(navy/gold palette, Calibri, navy headings), and adds a branded header
(logo + hairline) and footer (Probity wordmark + page numbers).

Stdlib only. Run:  python3 build/make_reference.py
"""
import os, re, shutil, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "build", "reference-default.docx")
ASSETS = os.path.join(ROOT, "_extensions", "probity", "assets")
OUT = os.path.join(ROOT, "_extensions", "probity", "reference.docx")
WORK = os.path.join(ROOT, "build", "ref")

# Palette
NAVY = "0A325A"; NAVY_DARK = "062340"; BLUE_MED = "4A7BA8"
TEXT = "1F2937"; MUTE = "6B7280"; RULE = "D5DEE9"; GOLD = "C8881F"
FONT = "Calibri"; MONO = "Consolas"

# ---- 1. fresh extraction ----
if os.path.exists(WORK):
    shutil.rmtree(WORK)
os.makedirs(WORK)
with zipfile.ZipFile(SRC) as z:
    names = z.namelist()
    z.extractall(WORK)

def rd(p):
    with open(os.path.join(WORK, p), encoding="utf-8") as f:
        return f.read()

def wr(p, s):
    full = os.path.join(WORK, p)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(s)

# ---- 2. theme: Calibri + navy accent1 ----
th = rd("word/theme/theme1.xml")
th = th.replace('<a:latin typeface="Aptos Display" panose="02110004020202020204"/>',
                '<a:latin typeface="Calibri"/>')
th = th.replace('<a:latin typeface="Aptos" panose="02110004020202020204"/>',
                '<a:latin typeface="Calibri"/>')
th = re.sub(r'<a:accent1>\s*<a:srgbClr val="[0-9A-Fa-f]{6}"/>\s*</a:accent1>',
            f'<a:accent1><a:srgbClr val="{NAVY}"/></a:accent1>', th)
wr("word/theme/theme1.xml", th)

# ---- 3. styles.xml ----
st = rd("word/styles.xml")

def replace_style(styleid, rpr=None, ppr=None, drop_semihidden=True):
    """Replace rPr / insert pPr inside a named style block."""
    global st
    m = re.search(r'(<w:style [^>]*w:styleId="' + styleid + r'".*?</w:style>)', st, re.S)
    if not m:
        raise SystemExit("style not found: " + styleid)
    block = m.group(1)
    if drop_semihidden:
        block = block.replace("<w:semiHidden />", "").replace("<w:semiHidden/>", "")
    if rpr is not None:
        if re.search(r'<w:rPr>.*?</w:rPr>', block, re.S):
            block = re.sub(r'<w:rPr>.*?</w:rPr>', rpr, block, flags=re.S)
        else:
            block = block.replace("</w:style>", rpr + "</w:style>")
    if ppr is not None:
        if re.search(r'<w:pPr>.*?</w:pPr>', block, re.S):
            block = re.sub(r'<w:pPr>.*?</w:pPr>', ppr, block, flags=re.S)
        else:
            block = re.sub(r'(<w:qFormat />)', r'\1' + ppr, block, count=1)
    st = st[:m.start()] + block + st[m.end():]

# Normal: Calibri 11pt, body text colour, comfortable line spacing
replace_style("Normal",
    rpr=f'<w:rPr><w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}" w:cs="{FONT}"/>'
        f'<w:color w:val="{TEXT}"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>',
    ppr='<w:pPr><w:spacing w:line="276" w:lineRule="auto"/></w:pPr>')

# Title: big navy, left aligned
replace_style("Title",
    rpr=f'<w:rPr><w:rFonts w:asciiTheme="majorHAnsi" w:hAnsiTheme="majorHAnsi"/>'
        f'<w:b/><w:color w:val="{NAVY}"/><w:sz w:val="60"/><w:szCs w:val="60"/></w:rPr>',
    ppr='<w:pPr><w:spacing w:before="240" w:after="80" w:line="240" w:lineRule="auto"/>'
        '<w:contextualSpacing/><w:jc w:val="left"/></w:pPr>')

# Subtitle: mid-blue, left aligned
replace_style("Subtitle",
    rpr=f'<w:rPr><w:rFonts w:asciiTheme="majorHAnsi" w:hAnsiTheme="majorHAnsi"/>'
        f'<w:color w:val="{BLUE_MED}"/><w:sz w:val="34"/><w:szCs w:val="34"/></w:rPr>',
    ppr='<w:pPr><w:spacing w:before="0" w:after="200" w:line="240" w:lineRule="auto"/>'
        '<w:contextualSpacing/><w:jc w:val="left"/></w:pPr>')

# Author / Date: muted, left
for sid in ("Author", "Date"):
    replace_style(sid,
        rpr=f'<w:rPr><w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}"/>'
            f'<w:color w:val="{MUTE}"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>',
        ppr='<w:pPr><w:spacing w:after="40"/><w:jc w:val="left"/></w:pPr>')

# Headings: explicit navy (strip theme shade so colour is exact)
replace_style("Heading1",
    rpr=f'<w:rPr><w:rFonts w:asciiTheme="majorHAnsi" w:hAnsiTheme="majorHAnsi"/>'
        f'<w:b/><w:color w:val="{NAVY}"/><w:sz w:val="36"/><w:szCs w:val="36"/></w:rPr>')
replace_style("Heading2",
    rpr=f'<w:rPr><w:rFonts w:asciiTheme="majorHAnsi" w:hAnsiTheme="majorHAnsi"/>'
        f'<w:b/><w:color w:val="{NAVY}"/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>')
replace_style("Heading3",
    rpr=f'<w:rPr><w:rFonts w:asciiTheme="majorHAnsi" w:hAnsiTheme="majorHAnsi"/>'
        f'<w:b/><w:color w:val="{NAVY_DARK}"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>')
for sid in ("Heading4", "Heading5", "Heading6"):
    replace_style(sid,
        rpr=f'<w:rPr><w:rFonts w:asciiTheme="majorHAnsi" w:hAnsiTheme="majorHAnsi"/>'
            f'<w:b/><w:i/><w:color w:val="{NAVY_DARK}"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>')

# Captions: muted italic
for sid in ("Caption", "TableCaption", "ImageCaption"):
    try:
        replace_style(sid,
            rpr=f'<w:rPr><w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}"/>'
                f'<w:i/><w:color w:val="{MUTE}"/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>')
    except SystemExit:
        pass

# Table: navy header fill + white bold text, hairline body rows
TABLE_NEW = f'''<w:style w:type="table" w:default="1" w:styleId="Table">
    <w:name w:val="Table" />
    <w:basedOn w:val="TableNormal" />
    <w:qFormat />
    <w:tblPr>
      <w:tblInd w:w="0" w:type="dxa" />
      <w:tblBorders>
        <w:top w:val="single" w:sz="4" w:space="0" w:color="{RULE}"/>
        <w:bottom w:val="single" w:sz="4" w:space="0" w:color="{RULE}"/>
        <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{RULE}"/>
      </w:tblBorders>
      <w:tblCellMar>
        <w:top w:w="60" w:type="dxa" />
        <w:left w:w="108" w:type="dxa" />
        <w:bottom w:w="60" w:type="dxa" />
        <w:right w:w="108" w:type="dxa" />
      </w:tblCellMar>
    </w:tblPr>
    <w:tblStylePr w:type="firstRow">
      <w:rPr>
        <w:b/>
        <w:color w:val="FFFFFF"/>
      </w:rPr>
      <w:tcPr>
        <w:shd w:val="clear" w:color="auto" w:fill="{NAVY}"/>
        <w:tcBorders>
          <w:top w:val="single" w:sz="8" w:space="0" w:color="{NAVY}"/>
          <w:bottom w:val="single" w:sz="8" w:space="0" w:color="{NAVY}"/>
        </w:tcBorders>
        <w:vAlign w:val="center"/>
      </w:tcPr>
    </w:tblStylePr>
  </w:style>'''
st = re.sub(r'<w:style w:type="table" w:default="1" w:styleId="Table">.*?</w:style>',
            TABLE_NEW, st, flags=re.S)

# Code: pin Consolas explicitly so it does not rely on pandoc defaults.
# VerbatimChar = inline code and fenced blocks; SourceCode = code-block paragraph.
CODE_RPR = (f'<w:rPr><w:rFonts w:ascii="{MONO}" w:hAnsi="{MONO}" w:cs="{MONO}"/>'
            f'<w:color w:val="{NAVY_DARK}"/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>')
for sid in ("VerbatimChar", "SourceCode"):
    try:
        replace_style(sid, rpr=CODE_RPR)
    except SystemExit:
        pass

wr("word/styles.xml", st)

# ---- 4. header + footer parts ----
# logo: navy small wordmark, ~120 x 37 px -> EMU (x9525)
LOGO_W = 120 * 9525
LOGO_H = int(LOGO_W * 434 / 1400)
os.makedirs(os.path.join(WORK, "word", "media"), exist_ok=True)
shutil.copy(os.path.join(ASSETS, "logo_navy_small.png"),
            os.path.join(WORK, "word", "media", "logo.png"))

HEADER = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:hdr xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">
  <w:p>
    <w:pPr>
      <w:pBdr><w:bottom w:val="single" w:sz="6" w:space="4" w:color="{NAVY}"/></w:pBdr>
      <w:tabs><w:tab w:val="right" w:pos="9072"/></w:tabs>
      <w:spacing w:after="0"/>
    </w:pPr>
    <w:r>
      <w:drawing>
        <wp:inline distT="0" distB="0" distL="0" distR="0">
          <wp:extent cx="{LOGO_W}" cy="{LOGO_H}"/>
          <wp:effectExtent l="0" t="0" r="0" b="0"/>
          <wp:docPr id="101" name="Probity logo"/>
          <wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>
          <a:graphic>
            <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
              <pic:pic>
                <pic:nvPicPr>
                  <pic:cNvPr id="101" name="Probity logo"/>
                  <pic:cNvPicPr/>
                </pic:nvPicPr>
                <pic:blipFill>
                  <a:blip r:embed="rIdLogo"/>
                  <a:stretch><a:fillRect/></a:stretch>
                </pic:blipFill>
                <pic:spPr>
                  <a:xfrm><a:off x="0" y="0"/><a:ext cx="{LOGO_W}" cy="{LOGO_H}"/></a:xfrm>
                  <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
                </pic:spPr>
              </pic:pic>
            </a:graphicData>
          </a:graphic>
        </wp:inline>
      </w:drawing>
    </w:r>
    <w:r><w:tab/></w:r>
    <w:r>
      <w:rPr><w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}"/><w:color w:val="{MUTE}"/><w:sz w:val="18"/></w:rPr>
      <w:t xml:space="preserve">Data Analytics</w:t>
    </w:r>
  </w:p>
</w:hdr>'''
wr("word/header1.xml", HEADER)

FOOTER = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:p>
    <w:pPr>
      <w:pBdr><w:top w:val="single" w:sz="4" w:space="4" w:color="{RULE}"/></w:pBdr>
      <w:tabs><w:tab w:val="right" w:pos="9072"/></w:tabs>
      <w:spacing w:after="0"/>
    </w:pPr>
    <w:r><w:rPr><w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}"/><w:b/><w:color w:val="{NAVY}"/><w:sz w:val="18"/></w:rPr><w:t>Probity Data Analytics</w:t></w:r>
    <w:r><w:rPr><w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}"/><w:color w:val="{MUTE}"/><w:sz w:val="18"/></w:rPr><w:t xml:space="preserve">    &#183;    Confidential</w:t></w:r>
    <w:r><w:tab/></w:r>
    <w:r><w:rPr><w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}"/><w:color w:val="{MUTE}"/><w:sz w:val="18"/></w:rPr><w:t xml:space="preserve">Page </w:t></w:r>
    <w:r><w:rPr><w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}"/><w:b/><w:color w:val="{NAVY}"/><w:sz w:val="18"/></w:rPr><w:fldChar w:fldCharType="begin"/></w:r>
    <w:r><w:rPr><w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}"/><w:b/><w:color w:val="{NAVY}"/><w:sz w:val="18"/></w:rPr><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>
    <w:r><w:rPr><w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}"/><w:b/><w:color w:val="{NAVY}"/><w:sz w:val="18"/></w:rPr><w:fldChar w:fldCharType="end"/></w:r>
    <w:r><w:rPr><w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}"/><w:color w:val="{MUTE}"/><w:sz w:val="18"/></w:rPr><w:t xml:space="preserve"> of </w:t></w:r>
    <w:r><w:rPr><w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}"/><w:b/><w:color w:val="{NAVY}"/><w:sz w:val="18"/></w:rPr><w:fldChar w:fldCharType="begin"/></w:r>
    <w:r><w:rPr><w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}"/><w:b/><w:color w:val="{NAVY}"/><w:sz w:val="18"/></w:rPr><w:instrText xml:space="preserve"> NUMPAGES </w:instrText></w:r>
    <w:r><w:rPr><w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}"/><w:b/><w:color w:val="{NAVY}"/><w:sz w:val="18"/></w:rPr><w:fldChar w:fldCharType="end"/></w:r>
  </w:p>
</w:ftr>'''
wr("word/footer1.xml", FOOTER)

# header rels (logo image)
wr("word/_rels/header1.xml.rels",
   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
   '<Relationship Id="rIdLogo" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/logo.png"/>'
   '</Relationships>')

# ---- 5. wire up document rels, content types, sectPr ----
rels = rd("word/_rels/document.xml.rels")
rels = rels.replace("</Relationships>",
    '<Relationship Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Id="rIdHdr1" Target="header1.xml" />'
    '<Relationship Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Id="rIdFtr1" Target="footer1.xml" />'
    "</Relationships>")
wr("word/_rels/document.xml.rels", rels)

ct = rd("[Content_Types].xml")
ct = ct.replace("</Types>",
    '<Default Extension="png" ContentType="image/png" />'
    '<Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml" />'
    '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml" />'
    "</Types>")
wr("[Content_Types].xml", ct)

doc = rd("word/document.xml")
sect = ('<w:sectPr>'
        '<w:headerReference w:type="default" r:id="rIdHdr1"/>'
        '<w:footerReference w:type="default" r:id="rIdFtr1"/>'
        '<w:footnotePr><w:numRestart w:val="eachSect" /></w:footnotePr>'
        '<w:pgSz w:w="11906" w:h="16838"/>'
        '<w:pgMar w:top="1700" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>'
        '</w:sectPr>')
doc = re.sub(r'<w:sectPr>.*?</w:sectPr>', sect, doc, flags=re.S)
wr("word/document.xml", doc)

# ---- 6. repack ----
extra = ["word/header1.xml", "word/footer1.xml",
         "word/_rels/header1.xml.rels", "word/media/logo.png"]
allnames = list(dict.fromkeys(names + extra))
if os.path.exists(OUT):
    os.remove(OUT)
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    for n in allnames:
        z.write(os.path.join(WORK, n), n)
print("wrote", OUT)
