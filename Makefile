# Eligibility dynamics in cross-sectional HIV incidence estimation
#
#   make verify        theorem-level test suite (primary check)
#   make figures       everything not requiring external data
#   make figures-full  everything, including CEPHIA-dependent outputs
#   make croi-figure   the CROI falsification figure (slow: ~20 min, 5.7e9 draws)
#   make all           verify + figures
#   make clean         remove generated outputs

PY      ?= python3
PYTEST  ?= $(PY) -m pytest
ANALYSIS := analysis
OUT      := outputs

OFFLINE := reproduce_pan mortality_threshold validate_theorems frailty_mixture \
           wang_comparator eta_surface inter_test_process
DATADEP := empirical_phi

.PHONY: all verify verify-fast figures figures-full croi-figure clean check-env \
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

eta-sites: check-env
	@cd $(ANALYSIS) && $(PY) eta_surface.py --sites

clean:
	rm -rf $(OUT)/figures/*.png $(OUT)/figures/*.pdf $(OUT)/tables/*.csv
	find . -name __pycache__ -type d -prune -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache
