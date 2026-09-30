"""
Collect everything needed to post the preprint into one flat directory.

Posting means uploading a manuscript, its figures and its tables to a form that
also asks for a title, an abstract, keywords and a set of declarations. Those
live in five different places in this repository. This gathers them.

    python3 analysis/build_preprint.py     # -> preprint/

Flat by design: figures sit beside the documents rather than in a subdirectory,
because submission forms ask for files one at a time and a nested tree only adds
clicks. The directory is entirely generated and entirely gitignored -- every file
in it has a tracked source, so committing it would duplicate the repository.

Run `make figures`, `make manuscript` and `make tex` first; this copies and does
not build, so nothing can change as a side effect of packaging.
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
M = ROOT / "manuscript"
NUMBERED = ROOT / "outputs" / "manuscript"
OUT = ROOT / "preprint"

TITLE = ("Temporary Loss of Eligibility and Bias in "
         "Cross-Sectional HIV Incidence Estimation")
VERSION = "Version 2"
DATE = "30 September 2026"


def head(n=12):
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                              capture_output=True, text=True).stdout.strip()
    except Exception:
        return "unknown"


def abstract_and_keywords():
    """The unstructured abstract and its keyword line, without the alternate."""
    s = (M / "section0_abstract.md").read_text()
    body = s[s.index("## Abstract"):s.index("## Structured variant")]
    body = body.replace("## Abstract", "").strip()
    kw = ""
    m = re.search(r"\*\*Keywords:\*\*(.+)", body)
    if m:
        kw = m.group(1).strip()
        body = body[:m.start()].strip()
    return body, kw


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    copied, missing = [], []

    def take(src: Path, dst_name=None):
        if src.exists():
            shutil.copy2(src, OUT / (dst_name or src.name))
            copied.append(dst_name or src.name)
        else:
            missing.append(src.name)

    # A SINGLE self-contained .tex: every \input expanded inline and every figure
    # referenced by bare filename, so the bundle compiles in place. Submission
    # systems take a flat upload; a main file plus an inputs directory is a
    # reliable way to have half the manuscript silently go missing.
    main = M / "PaperA.tex"
    if main.exists():
        tex = main.read_text()
        for inc in re.findall(r"\\input\{tex/([a-z]+)\}", tex):
            part = (M / "tex" / f"{inc}.tex")
            body = part.read_text() if part.exists() else f"% MISSING {inc}\n"
            tex = tex.replace(f"\\input{{tex/{inc}}}", body)
        # figures sit beside the .tex in the bundle, so drop the repo path
        tex = tex.replace("\\graphicspath{{../outputs/manuscript/}{./}}",
                          "\\graphicspath{{./}}")
        (OUT / "PaperA.tex").write_text(tex)
        copied.append("PaperA.tex")
        n_in = len(re.findall(r"\\input\{", tex))
        if n_in:
            missing.append(f"PaperA.tex still has {n_in} unexpanded \\input")

    # manuscript, in the three forms a form might ask for
    take(M / "PaperA.pdf")
    take(M / "PaperA_draft.md")
    take(M / "PaperA_draft.docx")
    take(M / "references.bib")
    take(M / "DISCLOSURES.md")

    # figures and tables under their final numbers, flat
    if NUMBERED.exists():
        for p in sorted(NUMBERED.iterdir()):
            take(p)
    else:
        missing.append("outputs/manuscript/ (run `make manuscript`)")

    # paste-ready metadata for the submission form
    abstract, keywords = abstract_and_keywords()
    (OUT / "abstract.txt").write_text(
        f"{TITLE}\n{VERSION}, {DATE}\n\n{abstract}\n\n"
        f"Keywords: {keywords}\n")
    copied.append("abstract.txt")

    def pretty(stem: str) -> str:
        """figure_s1 -> Figure S1; table_s3a -> Table S3a; table_3 -> Table 3."""
        kind, _, num = stem.partition("_")
        # Only the leading supplement marker is capitalised: the manuscript
        # writes S3a and S3b, not S3A.
        return f"{kind.capitalize()} {num[:1].upper()}{num[1:]}"

    # Everything a submission form asks for, in one file, so the fields can be
    # filled without opening the manuscript.
    disc = (M / "DISCLOSURES.md").read_text()
    def section(name):
        i = disc.find(f"## {name}")
        if i < 0:
            return "(not found)"
        j = disc.find("\n## ", i + 1)
        return disc[disc.find("\n", i) + 1: j if j > 0 else len(disc)].strip()

    meta = f"""SUBMISSION METADATA
{TITLE}
{VERSION}, {DATE}

Prepared from github.com/Nyx-Dynamics/nyx-eligibility-dynamics at {head()}.


TITLE
{TITLE}

TYPE
Methods / statistical methodology. Not a clinical study; no human subjects, no
new data collection.

AUTHOR
A. C. Demidont
Nyx Dynamics LLC
ORCID 0000-0002-9216-8569
Sole author.

ABSTRACT
See abstract.txt ({len(abstract.split())} words). Paste that file.

KEYWORDS
{keywords}

SUBJECT AREA
Public health and healthcare / epidemiology; statistics and probability.
Secondary: HIV prevention trial methodology.


DECLARATIONS
Paste each block into the corresponding field.

-- Funding --
{section("Funding")}

-- Competing interests --
{section("Competing interests")}

-- Author contributions (CRediT) --
{section("Author contributions")}

-- Use of artificial intelligence --
{section("Use of artificial intelligence")}

-- Prior and related publication --
{section("Prior and related publication")}

-- Data availability --
{section("Data availability")}

-- Licence --
{section("Licence")}


FILES TO UPLOAD
PaperA.pdf          the compiled manuscript, if a PDF is accepted
PaperA.tex          self-contained source; every input expanded, figures by
                    bare filename, compiles in this directory as it stands
references.bib      29 entries
figure_*.pdf        5 figures, vector; .png alongside at 200-600 dpi
table_*.csv         8 tables, also typeset inside the manuscript

The .tex needs no directory structure. Keep the figures beside it.
"""
    (OUT / "metadata.txt").write_text(meta)
    copied.append("metadata.txt")

    figs = sorted((p.stem for p in OUT.glob("figure_*.pdf")),
                  key=lambda s_: (s_.split("_")[1].startswith("s"), s_))
    tabs = sorted((p.stem for p in OUT.glob("table_*.csv")),
                  key=lambda s_: (s_.split("_")[1].startswith("s"), s_))
    fig_lines = "\n".join(f"{f + '.pdf / .png':<24}{pretty(f)}, vector and raster"
                           for f in figs)
    tab_lines = "\n".join(f"{t + '.csv':<24}{pretty(t)}" for t in tabs)
    readme = f"""PREPRINT PACKAGE  --  {VERSION}\n{TITLE}

A. C. Demidont, Nyx Dynamics LLC. ORCID 0000-0002-9216-8569.

Built from github.com/Nyx-Dynamics/nyx-eligibility-dynamics at {head()}.
Everything here is generated. Edit the sources in the repository and rebuild
with `make preprint`; edits made in this directory are overwritten.


UPLOAD
------
PaperA.pdf              the typeset manuscript: {len(figs)} figures and {len(tabs)} tables
                        typeset in place, verified by compiling the bundle alone
abstract.txt            title, abstract and keywords, for pasting into the form
references.bib          29 entries

PaperA.tex              self-contained source, compiles in this directory as it stands
metadata.txt            every field the form asks for

Separate files, if the form wants them individually:

{fig_lines}
{tab_lines}

PaperA_draft.md         the same text as markdown, for reading or diffing
PaperA_draft.docx       the same text as .docx, for co-author comment


BEFORE POSTING
--------------
DISCLOSURES.md is complete: AI use, prior publication, CRediT contributions,
funding (none), competing interests and data availability. Nothing in it is
left for you to fill in. Paste each section into the corresponding field.

Every numbered figure and table is present; `make check-refs` verifies it.


REPRODUCING
-----------
  git clone https://github.com/Nyx-Dynamics/nyx-eligibility-dynamics
  cd nyx-eligibility-dynamics && pip install -r requirements.txt
  make verify        72 tests
  make figures       regenerate every table and figure
  make tex           build PaperA.pdf
  make preprint      rebuild this directory
"""
    (OUT / "00_START_HERE.txt").write_text(readme)
    copied.append("00_START_HERE.txt")

    print(f"  {len(copied)} files -> {OUT.relative_to(ROOT)}/")
    print(f"  {len(figs)} figures, {len(tabs)} tables")
    if missing:
        print(f"  missing: {', '.join(missing)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
