"""
Compile the CROI 2026 submission packet into a single .docx.

Everything is read from the source files -- body.txt, FIGURE_CAPTION.txt, the
rendered figure, README.md and CITATION.cff -- so the document cannot drift from
what the repository actually contains. Nothing is retyped here.

    python3 manuscript/croi2026/build_docx.py   # -> CROI2026_eligibility_dynamics.docx

The abstract itself comes first and ends with the figure. Everything after the
page break is marked as not part of the submission: it is the material a
co-author needs to review the decisions, not text to paste into the portal.
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.shared import Inches, Pt, RGBColor

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FIGURE = ROOT / "outputs" / "figures" / "croi_falsification.png"

BODY = HERE / "body.txt"
CAPTION = HERE / "FIGURE_CAPTION.txt"
README = HERE / "README.md"
CITATION = ROOT / "CITATION.cff"
OUT = HERE / "CROI2026_eligibility_dynamics.docx"

TITLE = ("Temporary Loss of Eligibility Cancels Exactly in "
         "Cross-Sectional HIV Incidence Estimation")

SERIF, GREY = "Times New Roman", RGBColor(0x59, 0x59, 0x59)


# ---------------------------------------------------------------------------
# Source extraction
# ---------------------------------------------------------------------------

def author_line() -> str:
    """Single author from CITATION.cff. Co-authors are the submitter's call."""
    txt = CITATION.read_text()
    fam = re.search(r"family-names:\s*(.+)", txt).group(1).strip()
    given = re.search(r"given-names:\s*(.+)", txt).group(1).strip()
    aff = re.search(r'affiliation:\s*"(.+)"', txt).group(1).strip()
    orcid = re.search(r'orcid:\s*"(.+)"', txt).group(1).strip()
    return f"{given} {fam}, {aff}. ORCID {orcid.rsplit('/', 1)[-1]}."


def body_sections() -> list[tuple[str, str]]:
    """[(label, prose)] from body.txt, preserving submission order."""
    out = []
    for block in re.split(r"\n\s*\n", BODY.read_text().strip()):
        label, _, prose = block.partition(":")
        out.append((label.strip(), " ".join(prose.split())))
    return out


def unwrap(text: str) -> str:
    """Join hard-wrapped lines within a paragraph."""
    return "\n\n".join(" ".join(p.split())
                       for p in re.split(r"\n\s*\n", text.strip()))


def md_section(name: str) -> str:
    """Raw markdown under a `## name` heading, up to the next `## `."""
    txt = README.read_text()
    m = re.search(rf"^## {re.escape(name)}\s*$(.*?)(?=^## |\Z)",
                  txt, re.M | re.S)
    return m.group(1).strip() if m else ""


def md_table(block: str) -> tuple[list[str], list[list[str]]]:
    """Header and rows of the first GFM table in a markdown block."""
    rows = [ln for ln in block.splitlines() if ln.strip().startswith("|")]
    cells = [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in rows]
    body = [r for r in cells[1:] if not set("".join(r)) <= set("-: ")]
    header = [h if h.strip() else "#" for h in cells[0]]
    return header, body


BULLET = re.compile(r"^\s*[-*]\s+")


def is_bullets(chunk: str) -> bool:
    """
    A bullet block starts with a marker FOLLOWED BY WHITESPACE.

    Testing chunk.startswith("*") also matches bold/italic markdown, which
    silently swallowed the "**Submit:** ..." line -- it was classified as a list,
    produced no items, and rendered as nothing at all.
    """
    return bool(BULLET.match(chunk.splitlines()[0])) if chunk.strip() else False


def md_bullets(chunk: str) -> list[str]:
    """
    Markdown list items, each joined into one string.

    A new item starts with "-" or "*" at column 0; every other line continues
    the item it follows. Splitting per source line instead -- which is the
    obvious thing and is wrong -- turns one wrapped bullet into three stray
    paragraphs in Word.
    """
    items: list[str] = []
    for line in chunk.splitlines():
        if BULLET.match(line):
            items.append(BULLET.sub("", line))
        elif items and line.strip():
            items[-1] += " " + line.strip()
    return items


def demarkdown(s: str) -> str:
    """Strip the markdown a Word reader does not want to see."""
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)     # links -> text
    s = re.sub(r"[`*_]", "", s)
    s = s.replace("\\", "").replace("$", "")
    return " ".join(s.split())


# ---------------------------------------------------------------------------
# Document helpers
# ---------------------------------------------------------------------------

def style(doc):
    n = doc.styles["Normal"]
    n.font.name, n.font.size = SERIF, Pt(11)
    n.paragraph_format.space_after = Pt(8)
    n.paragraph_format.line_spacing = 1.15
    for s in doc.sections:
        s.top_margin = s.bottom_margin = Inches(0.9)
        s.left_margin = s.right_margin = Inches(1.0)


def para(doc, text="", *, size=11, bold=False, italic=False, align=None,
         space_after=8, colour=None, font=SERIF):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    if align is not None:
        p.alignment = align
    if text:
        r = p.add_run(text)
        r.font.name, r.font.size = font, Pt(size)
        r.bold, r.italic = bold, italic
        if colour is not None:
            r.font.color.rgb = colour
    return p


def labelled(doc, label, prose):
    """CROI structured-abstract paragraph: bold label, then running prose."""
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(8)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(f"{label}: ")
    r.bold = True
    r.font.name, r.font.size = SERIF, Pt(11)
    r = p.add_run(prose)
    r.font.name, r.font.size = SERIF, Pt(11)
    return p


def rule(doc):
    para(doc, "—" * 46, size=9, colour=GREY,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)


def table(doc, header, rows, widths=None):
    t = doc.add_table(rows=1, cols=len(header))
    t.style = "Table Grid"
    for c, h in zip(t.rows[0].cells, header):
        c.paragraphs[0].paragraph_format.space_after = Pt(2)
        r = c.paragraphs[0].add_run(demarkdown(h))
        r.bold = True
        r.font.name, r.font.size = SERIF, Pt(9)
    for row in rows:
        cells = t.add_row().cells
        for c, v in zip(cells, row):
            c.paragraphs[0].paragraph_format.space_after = Pt(2)
            r = c.paragraphs[0].add_run(demarkdown(v))
            r.font.name, r.font.size = SERIF, Pt(9)
    if widths:
        for row in t.rows:
            for cell, w in zip(row.cells, widths):
                cell.width = Inches(w)
    return t


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def main() -> int:
    for p in (BODY, CAPTION, README, CITATION, FIGURE):
        if not p.exists():
            raise SystemExit(f"missing source: {p.relative_to(ROOT)}")

    doc = Document()
    style(doc)

    # ---- the submission ------------------------------------------------
    para(doc, "CROI 2026 · abstract submission", size=9, colour=GREY,
         space_after=4)
    para(doc, TITLE, size=14, bold=True, space_after=6)
    para(doc, author_line(), size=10, italic=True, space_after=14)

    sections = body_sections()
    words = sum(len(prose.split()) + len(label.split())
                for label, prose in sections)
    for label, prose in sections:
        labelled(doc, label, prose)

    para(doc, f"Body: {words} words (limit 350). Figure: 1.", size=9,
         colour=GREY, space_after=0)

    # ---- figure --------------------------------------------------------
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    para(doc, "Figure", size=12, bold=True, space_after=8)
    pic = doc.add_paragraph()
    pic.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pic.paragraph_format.space_after = Pt(10)
    pic.add_run().add_picture(str(FIGURE), width=Inches(6.5))

    cap = unwrap(CAPTION.read_text())
    head, _, rest = cap.partition("\n\n")
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(head)
    r.bold = True
    r.font.name, r.font.size = SERIF, Pt(9.5)
    for block in rest.split("\n\n"):
        q = doc.add_paragraph()
        q.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        q.paragraph_format.space_after = Pt(6)
        r = q.add_run(block)
        r.font.name, r.font.size = SERIF, Pt(9.5)

    # ---- everything below is not the submission ------------------------
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    para(doc, "Submission notes", size=13, bold=True, space_after=2)
    para(doc, "Not part of the abstract. Decisions, provenance and the "
              "boundaries of what is claimed — for co-author review, not "
              "for the portal.", size=9.5, italic=True, colour=GREY,
         space_after=12)

    # Display names differ from the README's headings where the README heading
    # is unambiguous in context but not here: "Figure" already titles the page
    # holding the actual figure.
    NOTES = [("Title", "Title"),
             ("Category", "Category"),
             ("Figure", "Figure choice"),
             ("Held out of version 1, deliberately", "Held out of version 1")]
    for name, shown in NOTES:
        block = md_section(name)
        if not block:
            continue
        para(doc, shown, size=11, bold=True, space_after=4)
        for chunk in re.split(r"\n\s*\n", block):
            chunk = chunk.strip()
            if not chunk:
                continue
            if chunk.startswith("|"):
                table(doc, *md_table(chunk), widths=[0.4, 3.4, 2.6])
                para(doc, space_after=6)
                continue
            if chunk.startswith("###"):
                # Render the subheading rather than dropping it: its body
                # paragraphs are separate chunks and survive either way, but
                # without the heading they read as a continuation of the
                # section above, which inverts their meaning here
                # ("Rejected alternatives" following a recommendation).
                para(doc, demarkdown(chunk.lstrip("# ")), size=10, bold=True,
                     italic=True, space_after=3)
                continue
            if is_bullets(chunk):
                for li in md_bullets(chunk):
                    b = doc.add_paragraph(style="List Bullet")
                    b.paragraph_format.space_after = Pt(3)
                    r = b.add_run(demarkdown(li))
                    r.font.name, r.font.size = SERIF, Pt(10)
            else:
                para(doc, demarkdown(chunk), size=10, space_after=6,
                     align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        rule(doc)

    para(doc, "Number provenance", size=11, bold=True, space_after=4)
    para(doc, "Every quantitative claim in the body, the script that "
              "regenerates it, and the test that asserts it.", size=9.5,
         italic=True, colour=GREY, space_after=6)
    hdr, rows = md_table(md_section("Number provenance"))
    table(doc, hdr, rows, widths=[2.0, 1.25, 1.65, 1.6])
    para(doc, space_after=8)

    para(doc, "Figure numbers", size=11, bold=True, space_after=4)
    para(doc, "As plotted, from the committed tables.", size=9.5, italic=True,
         colour=GREY, space_after=6)
    with (ROOT / "outputs" / "tables" / "croi_figA_census.csv").open() as fh:
        rr = list(csv.reader(fh))
    table(doc, ["condition", "analytic", "Monte Carlo", "SE", "t"], rr[1:],
          widths=[2.4, 1.0, 1.1, 1.0, 0.7])
    rule(doc)

    para(doc, "Claims deliberately not made", size=11, bold=True, space_after=4)
    for chunk in re.split(r"\n\s*\n", md_section("Claims deliberately NOT made")):
        chunk = chunk.strip()
        if is_bullets(chunk):
            for li in md_bullets(chunk):
                b = doc.add_paragraph(style="List Bullet")
                b.paragraph_format.space_after = Pt(3)
                r = b.add_run(demarkdown(li))
                r.font.name, r.font.size = SERIF, Pt(10)
        elif chunk:
            para(doc, demarkdown(chunk), size=10, space_after=6)

    para(doc, space_after=6)
    rule(doc)
    para(doc, "This document is generated. It is built by "
              "manuscript/croi2026/build_docx.py from body.txt, "
              "FIGURE_CAPTION.txt, README.md, CITATION.cff and the rendered "
              "figure; edits made here are overwritten on the next build, so "
              "change the sources instead.", size=9, italic=True, colour=GREY,
         space_after=4)
    para(doc, "Reproduction: github.com/Nyx-Dynamics/nyx-eligibility-dynamics — "
              "make verify (72 tests), make figures, make croi-figure, "
              "make docx.", size=9, colour=GREY)

    doc.save(OUT)
    print(f"  wrote {OUT.relative_to(ROOT)}")
    print(f"  abstract body {words} words, figure embedded at 6.5in")
    return 0


if __name__ == "__main__":
    sys.exit(main())
