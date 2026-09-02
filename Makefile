.PHONY: help check export render manifest test verify lint typecheck all

PYTHON ?= python3

help:
	@echo "FlyPython Development Workflow:"
	@echo "  make check      - Run all catalog, export, readme, manifest, and example checks"
	@echo "  make export     - Regenerate catalog.json"
	@echo "  make render     - Regenerate README and README_cn catalog indexes"
	@echo "  make manifest   - Regenerate content-manifest.json"
	@echo "  make test       - Run pytest test suite"
	@echo "  make verify     - Verify all runnable examples"
	@echo "  make all        - Regenerate all exports and run all checks and tests"

check:
	$(PYTHON) tools/validate_catalog.py
	$(PYTHON) tools/export_catalog.py --check
	$(PYTHON) tools/render_readmes.py --check
	$(PYTHON) tools/build_content_manifest.py --check
	$(PYTHON) tools/verify_examples.py

export:
	$(PYTHON) tools/export_catalog.py

render:
	$(PYTHON) tools/render_readmes.py

manifest:
	$(PYTHON) tools/build_content_manifest.py

test:
	$(PYTHON) -m pytest

verify:
	$(PYTHON) tools/verify_examples.py

all: export render manifest test check
