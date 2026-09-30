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
        f"{TITLE}\n\n{abstract}\n\nKeywords: {keywords}\n")
    copied.append("abstract.txt")

    def pretty(stem: str) -> str:
        """figure_s1 -> Figure S1; table_s3a -> Table S3a; table_3 -> Table 3."""
        kind, _, num = stem.partition("_")
        # Only the leading supplement marker is capitalised: the manuscript
        # writes S3a and S3b, not S3A.
        return f"{kind.capitalize()} {num[:1].upper()}{num[1:]}"

    figs = sorted((p.stem for p in OUT.glob("figure_*.pdf")),
                  key=lambda s_: (s_.split("_")[1].startswith("s"), s_))
    tabs = sorted((p.stem for p in OUT.glob("table_*.csv")),
                  key=lambda s_: (s_.split("_")[1].startswith("s"), s_))
    fig_lines = "\n".join(f"{f + '.pdf / .png':<24}{pretty(f)}, vector and raster"
                           for f in figs)
    tab_lines = "\n".join(f"{t + '.csv':<24}{pretty(t)}" for t in tabs)
    readme = f"""PREPRINT PACKAGE
{TITLE}

A. C. Demidont, Nyx Dynamics LLC. ORCID 0000-0002-9216-8569.

Built from github.com/Nyx-Dynamics/nyx-eligibility-dynamics at {head()}.
Everything here is generated. Edit the sources in the repository and rebuild
with `make preprint`; edits made in this directory are overwritten.


UPLOAD
------
PaperA.pdf              the typeset manuscript, with all {len(figs)} figures and {len(tabs)} tables in place
abstract.txt            title, abstract and keywords, for pasting into the form
references.bib          29 entries

Separate files, if the form wants them individually:

{fig_lines}
{tab_lines}

PaperA_draft.md         the same text as markdown, for reading or diffing
PaperA_draft.docx       the same text as .docx, for co-author comment


BEFORE POSTING
--------------
DISCLOSURES.md has three items marked with a warning that need your decision:
funding, competing interests, and authorship. The AI-use and prior-publication
declarations are already written in full -- the latter names the superseded
Zenodo deposit (doi:10.5281/zenodo.20344293), which is public and should be
declared whether or not the form insists.

Two figures and one table are absent because they need the CEPHIA dataset, which
is not redistributed. They are Figure S2 and Table S1, cited in §3.2. Either
retrieve the dataset and rebuild, or cut those citations before posting.


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
