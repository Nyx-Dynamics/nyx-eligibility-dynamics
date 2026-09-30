# Eligibility dynamics in cross-sectional HIV incidence estimation
#
#   make verify        theorem-level test suite (primary check)
#   make figures       everything not requiring external data
#   make figures-full  everything, including CEPHIA-dependent outputs
#   make croi-figure   the CROI falsification figure (slow: ~20 min, 5.7e9 draws)
#   make figure-redraw rebuild the two-panel validation/poster figure (seconds)
#   make submission-fig the CROI submitted graphic, panel A only, 4x4in PNG
#   make docx          compile the CROI submission packet to a single .docx
#   make manuscript    assemble Paper A figures/tables under final numbers
#   make draft         concatenate the sections into one readable draft
#   make tex           convert the sections to LaTeX and build PaperA.pdf
#   make preprint      gather everything needed to post, into preprint/
#   make check-refs    verify every figure and table is present and cited
#   make all           verify + figures
#   make clean         remove generated outputs

PY      ?= python3
PYTEST  ?= $(PY) -m pytest
ANALYSIS := analysis
OUT      := outputs

OFFLINE := reproduce_pan mortality_threshold validate_theorems frailty_mixture \
           wang_comparator eta_surface inter_test_process
DATADEP := empirical_phi

.PHONY: all verify verify-fast figures figures-full croi-figure figure-redraw submission-fig docx manuscript draft tex preprint \
        check-refs \
        clean check-env \
        $(OFFLINE) $(DATADEP)

all: verify figures

check-env:
	@$(PY) -c "import numpy, scipy, pandas, statsmodels, sklearn" \
	  || { echo "missing dependencies -- run: pip install -r requirements.txt"; exit 1; }

verify: check-env
	$(PYTEST) tests/ -v

verify-fast: check-env
	$(PYTEST) tests/ -v -m "not slow"

$(OFFLINE) $(DATADEP): check-env
	@cd $(ANALYSIS) && $(PY) $@.py

figures: $(OFFLINE)
	@echo "\nOffline outputs written to $(OUT)/"

figures-full: figures $(DATADEP)
	@echo "\nAll outputs written to $(OUT)/"

# Deliberately NOT part of `figures`: 24 replicates x 15M draws x 19 cells is a
# few billion random numbers and about twenty minutes. The theorem-level suite
# already covers the same comparisons at lower precision; this target exists to
# regenerate the publication figure and its caption together.
croi-figure: check-env
	@cd $(ANALYSIS) && $(PY) falsification_figure.py

# Redraws the figure from the COMMITTED tables: no simulation, a few seconds.
# This is what makes `docx` work from a fresh clone, since rendered figures are
# not tracked (see .gitignore) but the numbers behind them are.
figure-redraw: check-env
	@cd $(ANALYSIS) && $(PY) falsification_figure.py --redraw

# The submitted graphic. Separate from figure-redraw: that one is the two-panel
# validation figure that now belongs to the poster, this one is panel A alone,
# authored at 4x4 in as PNG because the portal accepts PNG or JPEG only.
submission-fig: check-env
	@cd $(ANALYSIS) && $(PY) croi_submission_figure.py

# Reads body.txt, FIGURE_CAPTION.txt, README.md, CITATION.cff and the submitted
# figure. Depends on both figure targets so neither the embedded plot nor the
# caption can lag the committed numbers.
docx: figure-redraw submission-fig
	@$(PY) -c "import docx" || { echo "pip install python-docx"; exit 1; }
	@$(PY) manuscript/croi2027/build_docx.py

# Copies rather than regenerates: run `figures` first. The source scripts name
# outputs after what they compute; this maps those to final manuscript numbers,
# which live in one place so a renumbering is a single edit.
manuscript: check-env
	@cd $(ANALYSIS) && $(PY) assemble_manuscript.py

# Sections are written and frozen separately; a reader needs one document.
# Lifts each file's drafting notes out of the body and collects them at the end.
draft: check-env
	@cd $(ANALYSIS) && $(PY) assemble_draft.py --docx

# Pandoc does the conversion; build_tex.py decides what it is handed, strips the
# drafting notes, and writes the main file. Compiles twice for cross-references.
tex: check-env
	@cd $(ANALYSIS) && $(PY) build_tex.py
	@cd manuscript && pdflatex -interaction=nonstopmode PaperA.tex >/dev/null \
	  && pdflatex -interaction=nonstopmode PaperA.tex >/dev/null || true
	@cd manuscript && $(PY) -c "from pathlib import Path; \
	  L=Path('PaperA.log').read_text(encoding='utf8',errors='replace').split(chr(10)); \
	  e=[l for l in L if l.startswith('!')]; \
	  o=[l for l in L if 'Output written' in l]; \
	  print('  errors:', len(e)); print(' ', o[0] if o else 'NO PDF')"

# Copies only. Depends on nothing so the ordering stays explicit: run figures,
# manuscript and tex first, or the package will be built from stale artifacts.
preprint: check-env
	@cd $(ANALYSIS) && $(PY) build_preprint.py

# Non-zero exit if any numbered item is missing or uncited. Suitable for CI.
check-refs: check-env
	@cd $(ANALYSIS) && $(PY) assemble_manuscript.py --check

eta-sites: check-env
	@cd $(ANALYSIS) && $(PY) eta_surface.py --sites

clean:
	rm -rf $(OUT)/figures/*.png $(OUT)/figures/*.pdf $(OUT)/tables/*.csv
	find . -name __pycache__ -type d -prune -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache
