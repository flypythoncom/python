#!/usr/bin/env python3
"""Generate or verify the first-party FlyPython content manifest."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from tools.content_manifest import (
        ContentManifestError,
        build_manifest,
        dump_manifest,
    )
except ModuleNotFoundError:
    from content_manifest import ContentManifestError, build_manifest, dump_manifest


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "content-manifest.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        rendered = dump_manifest(build_manifest(ROOT))
    except ContentManifestError as exc:
        print(exc, file=sys.stderr)
        return 1

    if args.check:
        current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
        if current != rendered:
            print("content-manifest.json is stale; regenerate it", file=sys.stderr)
            return 1
        print("content manifest is current")
        return 0

    OUTPUT.write_text(rendered, encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
