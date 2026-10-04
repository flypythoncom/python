.PHONY: help check export render manifest test verify courses paths lint all

PYTHON ?= python3

help:
	@echo "FlyPython Development Workflow:"
	@echo "  make check      - Run the same checks as CI: lint, tests, catalog, radar, export, readme, manifest, example, course, and path checks"
	@echo "  make export     - Regenerate catalog.json and radar.json"
	@echo "  make render     - Regenerate README and README_cn catalog indexes plus the Radar table"
	@echo "  make manifest   - Regenerate content-manifest.json"
	@echo "  make lint       - Run ruff"
	@echo "  make test       - Run pytest test suite"
	@echo "  make verify     - Verify all runnable examples"
	@echo "  make courses    - Verify all course folders"
	@echo "  make paths      - Verify all learning-path contracts"
	@echo "  make all        - Regenerate all exports and run all checks and tests"

check: lint test
	$(PYTHON) tools/validate_catalog.py
	$(PYTHON) tools/export_catalog.py --check --target both
	$(PYTHON) tools/render_readmes.py --check
	$(PYTHON) tools/build_content_manifest.py --check
	$(PYTHON) tools/verify_examples.py
	$(PYTHON) tools/verify_courses.py
	$(PYTHON) tools/verify_paths.py

export:
	$(PYTHON) tools/export_catalog.py --target both

render:
	$(PYTHON) tools/render_readmes.py

manifest:
	$(PYTHON) tools/build_content_manifest.py

lint:
	$(PYTHON) -m ruff check .

test:
	$(PYTHON) -m pytest

verify:
	$(PYTHON) tools/verify_examples.py

courses:
	$(PYTHON) tools/verify_courses.py

paths:
	$(PYTHON) tools/verify_paths.py

all: export render manifest check
