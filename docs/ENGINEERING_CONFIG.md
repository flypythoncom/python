# Engineering configuration

The Python repository already has a locked Python toolchain, a Makefile,
SHA-pinned GitHub Actions and deterministic bilingual-content gates. These remain
the source of truth. The configuration additions reference
[yetone/magpie](https://github.com/yetone/magpie) (reviewed 2026-10-22), adapting
its engineering practices rather than its Go/desktop stack.

| Reference | FlyPython adaptation |
| --- | --- |
| [Makefile](https://github.com/yetone/magpie/blob/main/Makefile) | Guard repository-relative recipes against the wrong working directory; extend the existing command entry point rather than add another task runner. |
| [.gitattributes](https://github.com/yetone/magpie/blob/main/.gitattributes) | Force LF for text checkouts, keeping source checksums and generated output stable across platforms. Binary files remain auto-detected. |
| [CLAUDE.md](https://github.com/yetone/magpie/blob/main/CLAUDE.md) | Import the existing AGENTS.md; do not maintain two copies of the same agent rules. |
| [test workflow](https://github.com/yetone/magpie/blob/main/.github/workflows/test.yml) | Allow manual validation; do not cancel an in-progress default-branch run on every new push, while superseded PR runs are canceled. |

## Local commands

Use a POSIX shell and `make` from this repository (or `make -C path/to/python`).
`make setup` requires uv, selects `.python-version`, and syncs
`requirements-dev.lock.txt` into `.venv`. It does not update dependency locks.
Use `make check PYTHON=.venv/bin/python` after setup; the Make default remains
`python3` so existing CI and activated environments keep working. Native Windows
contributors can run the direct Python commands in CONTRIBUTING.md or use WSL.

`make generated-check` runs validation and read-only checks of catalog/radar,
README sections, content manifest and course solution hashes. `make generate`
regenerates those artifacts sequentially; `make all` regenerates, then checks.
The ordering holds under `make -j` too. No target publishes content or deploys.

## Intentionally not copied

- Go, Bun, GTK/WebKit, native binary packaging and Docker publishing do not fit
  this content-and-Python-tools repository.
- No automatic website pin update, release or production deployment is added.
- Existing exact locks, CI Python version matrix, least-privilege permissions,
  SHA-pinned actions and job timeout remain intact.
- No mass formatting or line-ending renormalization is performed. If a future
  byte-sensitive fixture deliberately needs CRLF, add a narrow per-file
  attributes exception; do not disable LF for ordinary source files.

Configuration regression tests verify the thin agent entry point, wrong-directory
Make guard, locked setup command, read-only generated checks and parallel-safe
regeneration ordering. They run in the existing pytest/CI suite.
