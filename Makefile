# Recipes use repository-relative paths. Like Magpie's Makefile, fail closed
# when invoked with `make -f path/to/Makefile` from an unrelated directory.
ifeq ($(and $(wildcard pyproject.toml),$(wildcard tools/validate_catalog.py),$(wildcard catalog/catalog.yml)),)
  $(error run make in the Python repository (make -C path/to/python))
endif

.DEFAULT_GOAL := help
.PHONY: help setup check generated-check generate export render manifest solutions test verify courses paths lint lock lock-check all

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
	@echo "  make setup      - Create .venv using .python-version and install locked dev dependencies (requires uv)"
	@echo "  make check      - Run CI checks (use PYTHON=.venv/bin/python after setup)"
	@echo "  make generated-check - Check catalog, exports, READMEs, manifest, and solution hashes without rewriting"
	@echo "  make generate   - Regenerate all derived content in dependency order"
	@echo "  make export     - Regenerate catalog.json and radar.json"
	@echo "  make render     - Regenerate root and catalog README indexes plus the Radar table"
	@echo "  make manifest   - Regenerate content-manifest.json"
	@echo "  make solutions  - Regenerate course-solutions.json"
	@echo "  make lint       - Run ruff"
	@echo "  make test       - Run pytest test suite"
	@echo "  make verify     - Verify all runnable examples"
	@echo "  make courses    - Verify all course folders"
	@echo "  make paths      - Verify all learning-path contracts"
	@echo "  make lock       - Re-resolve requirements*.lock.txt from pyproject.toml (keeps existing pins where valid)"
	@echo "  make lock-check - Fail if the lock files no longer match pyproject.toml"
	@echo "  make all        - Regenerate all exports and run all checks and tests"

setup:
	$(UV) venv --python "$$(cat .python-version)" .venv
	$(UV) pip sync --python .venv/bin/python requirements-dev.lock.txt

check: lint test generated-check
	$(PYTHON) tools/verify_examples.py
	$(PYTHON) tools/verify_courses.py
	$(PYTHON) tools/verify_paths.py

generated-check:
	$(PYTHON) tools/validate_catalog.py
	$(PYTHON) tools/export_catalog.py --check --target both
	$(PYTHON) tools/render_readmes.py --check
	$(PYTHON) tools/build_content_manifest.py --check
	$(PYTHON) tools/build_solution_hashes.py --check

# Keep writers sequential even under make -j: README/manifest checks must not
# race against a producer. No automatic commit, content-pin update or deploy.
generate:
	$(MAKE) export
	$(MAKE) render
	$(MAKE) manifest
	$(MAKE) solutions

export:
	$(PYTHON) tools/export_catalog.py --target both

render:
	$(PYTHON) tools/render_readmes.py

manifest:
	$(PYTHON) tools/build_content_manifest.py

solutions:
	$(PYTHON) tools/build_solution_hashes.py

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

all: generate
	$(MAKE) check
