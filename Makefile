.PHONY: help check export render manifest test verify courses paths lint lock lock-check all

PYTHON ?= python3
UV ?= uv

# Lock files are resolved once for every supported Python and platform
# (--universal from the 3.11 floor). The dev lock is constrained to the
# runtime lock so both always agree on shared packages.
UV_COMPILE = $(UV) pip compile pyproject.toml --universal --python-version 3.11 \
	--custom-compile-command "make lock" --quiet
define compile_locks
	$(UV_COMPILE) -o requirements.lock.txt
	$(UV_COMPILE) --extra dev -c requirements.lock.txt -o requirements-dev.lock.txt
endef

help:
	@echo "FlyPython Development Workflow:"
	@echo "  make check      - Run the same checks as CI: lint, tests, catalog, radar, export, readme, manifest, example, course, and path checks"
	@echo "  make export     - Regenerate catalog.json and radar.json"
	@echo "  make render     - Regenerate root and catalog README indexes plus the Radar table"
	@echo "  make manifest   - Regenerate content-manifest.json"
	@echo "  make lint       - Run ruff"
	@echo "  make test       - Run pytest test suite"
	@echo "  make verify     - Verify all runnable examples"
	@echo "  make courses    - Verify all course folders"
	@echo "  make paths      - Verify all learning-path contracts"
	@echo "  make lock       - Re-resolve requirements*.lock.txt from pyproject.toml (keeps existing pins where valid)"
	@echo "  make lock-check - Fail if the lock files no longer match pyproject.toml"
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

lock:
	$(compile_locks)

# uv keeps every committed pin that still satisfies pyproject.toml, so any
# diff after re-resolution means the locks drifted — the printed diff is the
# change to commit.
lock-check:
	@$(compile_locks)
	@git diff --exit-code requirements.lock.txt requirements-dev.lock.txt || \
		{ echo "lock files drifted from pyproject.toml — commit the regenerated files"; exit 1; }

all: export render manifest check
