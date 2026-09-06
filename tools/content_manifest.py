"""Load and validate bilingual first-party content for the public manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import yaml

CONTENT_GLOBS = ("guides/**/*.md", "playbooks/**/*.md", "examples/**/*.md")
REQUIRED = {
    "id",
    "type",
    "title",
    "summary",
    "lang",
    "content_version",
    "status",
    "reviewed_on",
}
LANGUAGES = {"en-US", "zh-CN"}
TYPES = {"guide", "playbook", "example"}


class ContentManifestError(ValueError):
    """Raised when first-party content violates the manifest contract."""


def _metadata(path: Path) -> dict[str, Any] | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    parts = text.split("---\n", maxsplit=2)
    if len(parts) != 3:
        raise ContentManifestError(f"{path}: malformed YAML front matter")
    data = yaml.safe_load(parts[1])
    if not isinstance(data, dict):
        raise ContentManifestError(f"{path}: front matter must be an object")
    return data


def build_manifest(root: Path) -> dict[str, Any]:
    records: dict[str, list[dict[str, Any]]] = {}
    errors: list[str] = []

    paths = sorted({path for pattern in CONTENT_GLOBS for path in root.glob(pattern)})
    for path in paths:
        metadata = _metadata(path)
        if metadata is None:
            continue
        missing = sorted(REQUIRED - metadata.keys())
        if missing:
            errors.append(f"{path.relative_to(root)}: missing {', '.join(missing)}")
            continue
        if metadata["lang"] not in LANGUAGES:
            errors.append(f"{path.relative_to(root)}: unsupported lang")
        if metadata["type"] not in TYPES:
            errors.append(f"{path.relative_to(root)}: unsupported type")
        if metadata["status"] != "reviewed":
            errors.append(f"{path.relative_to(root)}: public content must be reviewed")

        relative = path.relative_to(root).as_posix()
        records.setdefault(str(metadata["id"]), []).append(
            {
                "lang": metadata["lang"],
                "path": relative,
                "title": metadata["title"],
                "summary": metadata["summary"],
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "metadata": metadata,
            }
        )

    documents: list[dict[str, Any]] = []
    for content_id, locales in sorted(records.items()):
        languages = {locale["lang"] for locale in locales}
        if languages != LANGUAGES or len(locales) != 2:
            errors.append(f"{content_id}: expected exactly en-US and zh-CN")
            continue
        versions = {locale["metadata"]["content_version"] for locale in locales}
        types = {locale["metadata"]["type"] for locale in locales}
        reviewed_dates = {
            str(locale["metadata"]["reviewed_on"]) for locale in locales
        }
        if len(versions) != 1 or len(types) != 1 or len(reviewed_dates) != 1:
            errors.append(f"{content_id}: paired metadata does not match")
            continue
        documents.append(
            {
                "id": content_id,
                "type": types.pop(),
                "content_version": versions.pop(),
                "status": "reviewed",
                "reviewed_on": reviewed_dates.pop(),
                "locales": [
                    {key: locale[key] for key in ("lang", "path", "title", "summary", "sha256")}
                    for locale in sorted(locales, key=lambda item: item["lang"])
                ],
            }
        )

    if errors:
        raise ContentManifestError("\n".join(errors))
    return {"schema_version": 1, "documents": documents}


def dump_manifest(manifest: dict[str, Any]) -> str:
    return json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=False) + "\n"
