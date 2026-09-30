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
    ("section7_backmatter.md", "backmatter"),
]

TITLE = ("Temporary Loss of Eligibility and Bias in\\\\\n"
         "Cross-Sectional HIV Incidence Estimation")
AUTHOR = "A.~C. Demidont"
AFFIL = "Nyx Dynamics LLC \\\\ ORCID 0000-0002-9216-8569"
VERSION = "Version 2"
DATE = "30 September 2026"

NOTE_HEAD = re.compile(r"^#+\s*Drafting notes.*$", re.M)

# "Figure 3", "Table S3a", "Figure S2A". The suffix is ambiguous and the two
# cases must not be conflated: a LOWERCASE letter is part of the label itself
# (Table S3a and Table S3b are different tables), while an UPPERCASE letter is a
# panel reference within one figure (Figure S2A is panel A of Figure S2). Only
# the lowercase form is kept when resolving to a label.
CITE = re.compile(r"\b(Figure|Table)\s+(S?\d+)([a-zA-Z])?\b")


def _label(m) -> str:
    suffix = m.group(3) or ""
    if suffix.isupper():
        suffix = ""                     # panel reference, not part of the label
    return f"{m.group(1)} {m.group(2)}{suffix}"


def place_floats(tex: str, pending: dict) -> str:
    """
    Insert each float after the paragraph that first cites it.

    Collecting floats at the end makes a reader leaf back and forth; a figure
    belongs beside the sentence that argues from it. Paragraphs in pandoc's
    output are blank-line separated, so the insertion point is the first blank
    line after the citation. Anything still pending when a section ends stays
    pending and is placed by a later section, or reported.
    """
    if not pending:
        return tex
    out, pos = [], 0
    for m in CITE.finditer(tex):
        label = _label(m)
        if label not in pending:
            continue
        # do not fire on the float's own caption
        if tex.rfind(r"egin{figure}", 0, m.start()) > tex.rfind(r"\end{figure}", 0, m.start()):
            continue
        if tex.rfind(r"egin{table}", 0, m.start()) > tex.rfind(r"\end{table}", 0, m.start()):
            continue
        brk = tex.find("\n\n", m.end())
        brk = len(tex) if brk < 0 else brk + 2
        if brk < pos:
            continue
        out.append(tex[pos:brk])
        out.append(pending.pop(label) + "\n")
        pos = brk
    out.append(tex[pos:])
    return "".join(out)
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


def order_labels(d):
    """Figures before tables, main before supplement, numeric within each."""
    def key(l):
        m = re.search(r"(S?)(\d+)([a-z]?)", l)
        return (l.startswith("Table"), m.group(1) == "S", int(m.group(2)), m.group(3))
    return sorted(d, key=key)


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


def preamble(title: str) -> str:
    """Shared preamble. The manuscript and the supplement must not drift
    apart in Unicode declarations, table packages or numbering."""
    return f"""\\documentclass[11pt,a4paper]{{article}}

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
\\date{{{VERSION} \\\\ \\small {DATE}}}"""


def main():
    if not shutil.which("pandoc"):
        raise SystemExit("pandoc not found")
    TEX.mkdir(parents=True, exist_ok=True)
    # Floats used to be emitted as figures.tex/tables.tex and appended at the end.
    # They are now placed inline, so those files are orphans; left on disk they
    # look like current output and were picked up by a verification pass.
    for orphan in ("figures.tex", "tables.tex", "captions.tex"):
        (TEX / orphan).unlink(missing_ok=True)
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from build_floats import environments
    all_env = environments()
    # Supplementary floats live in the supplement document. The main text cites
    # them -- "see Figure S1" -- but does not contain them, which is the usual
    # arrangement and the reason the two documents are built separately.
    supp = {k: v for k, v in all_env.items() if k.split()[1].startswith("S")}
    pending = {k: v for k, v in all_env.items() if k not in supp}
    n_total = len(pending)

    for fname, stem in SECTIONS:
        p = M / fname
        if not p.exists():
            print(f"  missing {fname}"); continue
        md = strip_notes(p.read_text())
        if stem == "abstract":
            md = lift(md, LIFT_ABSTRACT)
        md = strip_banner(md)
        tex = to_tex(md)
        tex = place_floats(tex, pending)
        # the abstract is an environment, not a section
        if stem == "abstract":
            tex = re.sub(r"\\section\{Abstract\}\s*", "", tex)
        (TEX / f"{stem}.tex").write_text(tex)
        print(f"  {fname:<32} -> tex/{stem}.tex  ({len(tex.splitlines())} lines)")

    if pending:
        print(f"  NOT PLACED: {', '.join(sorted(pending))} — cited nowhere in the "
              f"section bodies")
    print(f"  {n_total - len(pending)} of {n_total} main-text floats placed inline")

    # --- the supplement, as its own compilable document --------------------
    sp = M / "section6_supplement.md"
    if sp.exists():
        body = strip_banner(strip_notes(sp.read_text()))
        n_supp = len(supp)
        stex = place_floats(to_tex(body), supp)
        left = dict(supp)                       # place_floats pops what it uses
        for label in order_labels(left):        # cited only from the main text
            stex += "\n" + left[label]
        (TEX / "supplement.tex").write_text(stex)

        supp_doc = (preamble("Supplementary material \\\\ \\large " + TITLE)
                    + "\n\\begin{document}\n\\maketitle\n\n"
                      "\\input{tex/supplement}\n\n\\end{document}\n")
        (M / "Supplement.tex").write_text(supp_doc)
        print(f"  wrote manuscript/Supplement.tex — {n_supp} supplementary "
              f"floats: {n_supp - len(left)} placed at citation within the "
              f"supplement, {len(left)} appended because they are cited only "
              f"from the main text")

    for src, dst in [("references.md", "references")]:
        p = M / src
        if p.exists():
            (TEX / f"{dst}.tex").write_text(to_tex(strip_notes(p.read_text())))
            print(f"  {src:<32} -> tex/{dst}.tex")

    main_tex = preamble(f"{TITLE}") + f"""\\begin{{document}}
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
\\input{{tex/backmatter}}

\\clearpage
\\input{{tex/references}}

\\end{{document}}
"""
    (M / "PaperA.tex").write_text(main_tex)
    # The supplement is its own document. An earlier revision added the back
    # matter without removing this input, so the supplement was typeset into
    # both and nothing complained. Checked after the write, on what was written.
    if "tex/supplement" in main_tex:
        raise SystemExit("PaperA.tex inputs tex/supplement: the supplement "
                         "would appear in both documents")
    print("\n  wrote manuscript/PaperA.tex")
    print("  compile with:  cd manuscript && pdflatex PaperA.tex")
    return 0


if __name__ == "__main__":
    sys.exit(main())
