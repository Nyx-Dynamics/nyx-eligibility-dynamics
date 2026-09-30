"""
Convert the manuscript's section files to LaTeX.

Pandoc does the markdown-to-LaTeX conversion; this script decides what it is
handed and what is done with the result. Three things it does that a bare
`pandoc section.md -o section.tex` does not:

  * drops the per-file banner and the drafting notes, which are editorial and
    must not reach a typeset manuscript;
  * emits section bodies only (no preamble, no \\begin{document}), so they can be
    \\input into a main file that owns the document class and the bibliography;
  * writes that main file, with the sections in order and the numbering that
    `assemble_manuscript.py` fixed.

    python3 analysis/build_tex.py

Math already reaches pandoc as LaTeX, so it passes through untouched. Tables
become `longtable`, which needs no extra package under most classes but is
declared in the preamble regardless.
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
M = ROOT / "manuscript"
TEX = M / "tex"

SECTIONS = [
    ("section0_abstract.md", "abstract"),
    ("section1_introduction.md", "introduction"),
    ("section2_theory.md", "theory"),
    ("section3_parameterisation.md", "parameterisation"),
    ("section4_results.md", "results"),
    ("section5_discussion.md", "discussion"),
    ("section6_supplement.md", "supplement"),
]

TITLE = ("Temporary Loss of Eligibility and Bias in\\\\\n"
         "Cross-Sectional HIV Incidence Estimation")
AUTHOR = "A.~C. Demidont"
AFFIL = "Nyx Dynamics LLC \\\\ ORCID 0000-0002-9216-8569"
VERSION = "Version 2"
DATE = "30 September 2026"

NOTE_HEAD = re.compile(r"^#+\s*Drafting notes.*$", re.M)
LIFT_ABSTRACT = [r"^##\s*Title\s*$", r"^##\s*Structured variant\s*$"]


def strip_notes(text: str) -> str:
    m = NOTE_HEAD.search(text)
    return (text[:m.start()] if m else text).strip()


def lift(text: str, patterns) -> str:
    for pat in patterns:
        m = re.search(pat, text, re.M)
        if not m:
            continue
        nxt = re.search(r"^##\s+\S", text[m.end():], re.M)
        end = m.end() + (nxt.start() if nxt else len(text[m.end():]))
        text = text[:m.start()] + text[end:]
    return text


def strip_banner(text: str) -> str:
    """Remove the '# Paper A — Section n' heading, the revision note and rule."""
    lines, out, started = text.split("\n"), [], False
    for ln in lines:
        if not started:
            if (ln.startswith("# Paper A") or ln.startswith("**Working title")
                    or ln.startswith("**Title:**") or ln.startswith("> ")
                    or ln.startswith("Notation follows")
                    or ln.strip() in ("", "---")):
                continue
            started = True
        out.append(ln)
    return "\n".join(out).strip()


# Pandoc wraps uncaptioned longtables in `{\def\LTcaptype{none} ...}` to stop
# the table counter advancing. longtable then calls \refstepcounter{none} and
# pdflatex dies with "No counter 'none' defined". Loading `caption` does not fix
# it. Neutralising the directive does, and is safe: the surrounding group brace
# is left in place so the file stays balanced, and the only effect is that these
# tables do not advance a counter they were never going to use.
LTCAPTYPE = re.compile(r"\{\\def\\LTcaptype\{none\}[^\n]*")

# Pandoc derives \label from heading text, so headings that repeat across
# sections collide -- "Absorbing loss" is both §3.4 and §4.4, "Composition with
# screening-stage selection" both §2.7 and §4.6. Nothing cross-references these
# (the prose cites section numbers), so the labels are dropped rather than
# uniquified, which would only create names nobody uses.
HEADLABEL = re.compile(r"(\\(?:sub)*section\{[^}]*\})\\label\{[^}]*\}")


def to_tex(md: str) -> str:
    r = subprocess.run(
        ["pandoc", "--from", "markdown+tex_math_dollars+pipe_tables",
         "--to", "latex", "--wrap=preserve",
         # The per-file "# Paper A — Section n" banner is stripped before this
         # runs, so pandoc's top level is "##". Without the shift it emits
         # \subsection for what is a section and the PDF numbers them 0.x.
         "--shift-heading-level-by=-1"],
        input=md, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"pandoc failed: {r.stderr[:400]}")
    return HEADLABEL.sub(r"\1", LTCAPTYPE.sub("{%", r.stdout))


def main():
    if not shutil.which("pandoc"):
        raise SystemExit("pandoc not found")
    TEX.mkdir(parents=True, exist_ok=True)

    for fname, stem in SECTIONS:
        p = M / fname
        if not p.exists():
            print(f"  missing {fname}"); continue
        md = strip_notes(p.read_text())
        if stem == "abstract":
            md = lift(md, LIFT_ABSTRACT)
        md = strip_banner(md)
        tex = to_tex(md)
        # the abstract is an environment, not a section
        if stem == "abstract":
            tex = re.sub(r"\\section\{Abstract\}\s*", "", tex)
        (TEX / f"{stem}.tex").write_text(tex)
        print(f"  {fname:<32} -> tex/{stem}.tex  ({len(tex.splitlines())} lines)")

    for src, dst in [("references.md", "references")]:
        p = M / src
        if p.exists():
            (TEX / f"{dst}.tex").write_text(to_tex(strip_notes(p.read_text())))
            print(f"  {src:<32} -> tex/{dst}.tex")

    main_tex = f"""\\documentclass[11pt,a4paper]{{article}}

% Generated by analysis/build_tex.py. Edit the markdown section files and
% regenerate; do not edit tex/ by hand.

\\usepackage[margin=1in]{{geometry}}
\\usepackage[T1]{{fontenc}}
\\usepackage{{textcomp}}
\\usepackage{{amsmath,amssymb,amsthm}}

% Greek and symbols reach the prose as literal Unicode rather than as math, so
% pdflatex needs them declared. Mapped to math equivalents so they typeset the
% same as the surrounding notation.
\\DeclareUnicodeCharacter{{03A9}}{{\\ensuremath{{\\Omega}}}}
\\DeclareUnicodeCharacter{{03B2}}{{\\ensuremath{{\\beta}}}}
\\DeclareUnicodeCharacter{{03B7}}{{\\ensuremath{{\\eta}}}}
\\DeclareUnicodeCharacter{{03B8}}{{\\ensuremath{{\\theta}}}}
\\DeclareUnicodeCharacter{{03BC}}{{\\ensuremath{{\\mu}}}}
\\DeclareUnicodeCharacter{{03BB}}{{\\ensuremath{{\\lambda}}}}
\\DeclareUnicodeCharacter{{03C1}}{{\\ensuremath{{\\rho}}}}
\\DeclareUnicodeCharacter{{03C6}}{{\\ensuremath{{\\varphi}}}}
\\DeclareUnicodeCharacter{{2264}}{{\\ensuremath{{\\leq}}}}
\\DeclareUnicodeCharacter{{2265}}{{\\ensuremath{{\\geq}}}}
\\DeclareUnicodeCharacter{{2212}}{{\\ensuremath{{-}}}}
\\DeclareUnicodeCharacter{{2248}}{{\\ensuremath{{\\approx}}}}
\\DeclareUnicodeCharacter{{2192}}{{\\ensuremath{{\\rightarrow}}}}
\\DeclareUnicodeCharacter{{207B}}{{\\ensuremath{{^{{-}}}}}}
\\DeclareUnicodeCharacter{{00B9}}{{\\ensuremath{{^{{1}}}}}}
\\DeclareUnicodeCharacter{{00B7}}{{\\textperiodcentered}}
\\DeclareUnicodeCharacter{{00D7}}{{\\ensuremath{{\\times}}}}

\\usepackage{{booktabs,longtable,array,calc}}
% pandoc's longtable column specs use \\real{{}} from calc; without it every
% table raises "Missing number" and typesets at zero width.
\\usepackage{{caption}}
\\captionsetup{{labelformat=empty,justification=raggedright,singlelinecheck=false}}
\\usepackage{{etoolbox}}
\\makeatletter
\\patchcmd\\longtable{{\\par}}{{\\if@noskipsec\\mbox{{}}\\fi\\par}}{{}}{{}}
\\makeatother
\\usepackage{{graphicx}}
% Resolves figures both here (pdflatex runs in manuscript/) and in a flat
% submission bundle where the figures sit beside the .tex file.
\\graphicspath{{{{../outputs/manuscript/}}{{./}}}}
\\usepackage[hidelinks]{{hyperref}}
\\usepackage{{csquotes}}

% The section files carry their own numbers in the heading text ("3.2 The
% recency function"), so LaTeX's automatic numbering produced "0.4.2 3.2 ...".
% Suppress it and let the prose numbering stand, which is what every
% cross-reference in the text refers to.
\\setcounter{{secnumdepth}}{{-2}}

\\newtheorem{{theorem}}{{Theorem}}
\\newtheorem{{corollary}}[theorem]{{Corollary}}
\\newtheorem{{remark}}[theorem]{{Remark}}

\\providecommand{{\\tightlist}}{{%
  \\setlength{{\\itemsep}}{{0pt}}\\setlength{{\\parskip}}{{0pt}}}}

\\title{{{TITLE}}}
\\author{{{AUTHOR}\\\\ \\small {AFFIL}}}
\\date{{{VERSION} \\\\ \\small {DATE}}}

\\begin{{document}}
\\maketitle

\\begin{{abstract}}
\\input{{tex/abstract}}
\\end{{abstract}}

\\input{{tex/introduction}}
\\input{{tex/theory}}
\\input{{tex/parameterisation}}
\\input{{tex/results}}
\\input{{tex/discussion}}

\\clearpage
\\input{{tex/supplement}}

\\clearpage
\\input{{tex/figures}}

\\clearpage
\\input{{tex/tables}}

\\clearpage
\\input{{tex/references}}

\\end{{document}}
"""
    (M / "PaperA.tex").write_text(main_tex)
    print("\n  wrote manuscript/PaperA.tex")
    print("  compile with:  cd manuscript && pdflatex PaperA.tex")
    return 0


if __name__ == "__main__":
    sys.exit(main())
