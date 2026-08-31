"""Loading and validation helpers for ``_data/resources.yml``."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence
from urllib.parse import urlsplit, urlunsplit

import yaml
from yaml.constructor import ConstructorError
from yaml.resolver import BaseResolver


EXPECTED_PATH_IDS = {"foundations", "web-apis", "automation", "ai-agents"}
CATALOG_KEYS = {"reviewed_on", "status", "paths"}
PATH_KEYS = {"id", "title_en", "title_zh", "summary_en", "summary_zh", "order"}
RESOURCE_KEYS = {
    "id",
    "path",
    "title",
    "url",
    "source_type",
    "level",
    "language",
    "why_en",
    "why_zh",
    "reviewed_on",
    "status",
    "requires_key",
    "risk",
    "featured",
}
SOURCE_TYPES = {"official-docs", "official-standard", "official-project"}
LEVELS = {"beginner", "intermediate", "advanced", "all-levels"}
LANGUAGES = {"en", "zh", "multilingual"}
STATUSES = {"active"}
RISKS = {"low", "medium"}
ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class CatalogLoadError(ValueError):
    """Raised when the catalog cannot be parsed safely."""


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def _construct_unique_mapping(
    loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    BaseResolver.DEFAULT_MAPPING_TAG, _construct_unique_mapping
)


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    location: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {
            "code": self.code,
            "location": self.location,
            "message": self.message,
        }


def load_catalog(path: str | Path) -> dict[str, Any]:
    catalog_path = Path(path)
    try:
        with catalog_path.open("r", encoding="utf-8") as handle:
            value = yaml.load(handle, Loader=UniqueKeyLoader)
    except (OSError, yaml.YAMLError) as exc:
        raise CatalogLoadError(f"cannot load {catalog_path}: {exc}") from exc
    if not isinstance(value, dict):
        raise CatalogLoadError(f"{catalog_path} must contain a YAML mapping")
    return value


def normalize_url(value: str) -> str:
    parsed = urlsplit(value.strip())
    host = (parsed.hostname or "").lower()
    port = parsed.port
    default_port = (parsed.scheme.lower() == "https" and port == 443) or (
        parsed.scheme.lower() == "http" and port == 80
    )
    display_host = f"[{host}]" if ":" in host else host
    netloc = display_host
    if port and not default_port:
        netloc = f"{display_host}:{port}"
    path = parsed.path or "/"
    if path != "/":
        path = path.rstrip("/")
    return urlunsplit((parsed.scheme.lower(), netloc, path, parsed.query, ""))


def _date_value(value: Any) -> date | None:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value)
        except ValueError:
            return None
    return None


def _missing_or_unknown(
    value: Mapping[str, Any], expected: set[str], location: str
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for key in sorted(expected - set(value)):
        issues.append(ValidationIssue("missing-field", location, f"missing {key!r}"))
    for key in sorted(set(value) - expected):
        issues.append(
            ValidationIssue("unknown-field", f"{location}.{key}", "unknown field")
        )
    return issues


def _required_text(
    value: Mapping[str, Any], key: str, location: str
) -> list[ValidationIssue]:
    raw = value.get(key)
    if not isinstance(raw, str) or not raw.strip():
        return [
            ValidationIssue(
                "invalid-text", f"{location}.{key}", "must be a non-empty string"
            )
        ]
    return []


def validate_catalog(
    data: Mapping[str, Any], *, today: date | None = None, max_review_age_days: int = 366
) -> list[ValidationIssue]:
    """Validate schema, uniqueness, HTTPS, review dates, and bilingual parity."""

    today = today or date.today()
    issues: list[ValidationIssue] = []
    expected_top = {"catalog", "resources"}
    issues.extend(_missing_or_unknown(data, expected_top, "$"))

    metadata = data.get("catalog")
    if not isinstance(metadata, dict):
        issues.append(
            ValidationIssue("invalid-type", "$.catalog", "must be a mapping")
        )
        metadata = {}
    else:
        issues.extend(_missing_or_unknown(metadata, CATALOG_KEYS, "$.catalog"))

    catalog_date = _date_value(metadata.get("reviewed_on"))
    if catalog_date is None:
        issues.append(
            ValidationIssue(
                "invalid-date", "$.catalog.reviewed_on", "must be YYYY-MM-DD"
            )
        )
    elif catalog_date > today:
        issues.append(
            ValidationIssue(
                "future-date", "$.catalog.reviewed_on", "cannot be in the future"
            )
        )
    if metadata.get("status") not in STATUSES:
        issues.append(
            ValidationIssue(
                "invalid-enum", "$.catalog.status", "must be 'active'"
            )
        )

    paths = metadata.get("paths")
    path_ids: set[str] = set()
    path_orders: set[int] = set()
    if not isinstance(paths, list):
        issues.append(
            ValidationIssue("invalid-type", "$.catalog.paths", "must be a list")
        )
        paths = []
    for index, path_entry in enumerate(paths):
        location = f"$.catalog.paths[{index}]"
        if not isinstance(path_entry, dict):
            issues.append(ValidationIssue("invalid-type", location, "must be a mapping"))
            continue
        issues.extend(_missing_or_unknown(path_entry, PATH_KEYS, location))
        for key in ("id", "title_en", "title_zh", "summary_en", "summary_zh"):
            issues.extend(_required_text(path_entry, key, location))
        path_id = path_entry.get("id")
        if isinstance(path_id, str):
            if path_id in path_ids:
                issues.append(
                    ValidationIssue("duplicate-path", f"{location}.id", path_id)
                )
            path_ids.add(path_id)
        order = path_entry.get("order")
        if not isinstance(order, int) or isinstance(order, bool) or order < 1:
            issues.append(
                ValidationIssue(
                    "invalid-order", f"{location}.order", "must be a positive integer"
                )
            )
        elif order in path_orders:
            issues.append(
                ValidationIssue("duplicate-order", f"{location}.order", str(order))
            )
        else:
            path_orders.add(order)

    if path_ids != EXPECTED_PATH_IDS:
        missing = sorted(EXPECTED_PATH_IDS - path_ids)
        extra = sorted(path_ids - EXPECTED_PATH_IDS)
        issues.append(
            ValidationIssue(
                "path-parity",
                "$.catalog.paths",
                f"expected four canonical paths; missing={missing}, extra={extra}",
            )
        )

    resources = data.get("resources")
    if not isinstance(resources, list):
        issues.append(
            ValidationIssue("invalid-type", "$.resources", "must be a list")
        )
        resources = []

    seen_ids: set[str] = set()
    seen_urls: dict[str, str] = {}
    resources_per_path = {path_id: 0 for path_id in EXPECTED_PATH_IDS}
    for index, resource in enumerate(resources):
        location = f"$.resources[{index}]"
        if not isinstance(resource, dict):
            issues.append(ValidationIssue("invalid-type", location, "must be a mapping"))
            continue
        issues.extend(_missing_or_unknown(resource, RESOURCE_KEYS, location))
        for key in ("id", "path", "title", "url", "why_en", "why_zh"):
            issues.extend(_required_text(resource, key, location))

        resource_id = resource.get("id")
        if isinstance(resource_id, str):
            if not ID_PATTERN.fullmatch(resource_id):
                issues.append(
                    ValidationIssue(
                        "invalid-id",
                        f"{location}.id",
                        "must be a lowercase kebab-case identifier",
                    )
                )
            if resource_id in seen_ids:
                issues.append(
                    ValidationIssue("duplicate-id", f"{location}.id", resource_id)
                )
            seen_ids.add(resource_id)

        path_id = resource.get("path")
        if isinstance(path_id, str):
            if path_id not in path_ids:
                issues.append(
                    ValidationIssue(
                        "unknown-path", f"{location}.path", f"unknown path {path_id!r}"
                    )
                )
            if path_id in resources_per_path:
                resources_per_path[path_id] += 1

        url = resource.get("url")
        if isinstance(url, str) and url.strip():
            try:
                parsed = urlsplit(url)
                normalized = normalize_url(url)
            except ValueError as exc:
                issues.append(
                    ValidationIssue("invalid-url", f"{location}.url", str(exc))
                )
            else:
                if parsed.scheme.lower() != "https" or not parsed.hostname:
                    issues.append(
                        ValidationIssue(
                            "https-required",
                            f"{location}.url",
                            "must be an absolute HTTPS URL",
                        )
                    )
                if parsed.username or parsed.password:
                    issues.append(
                        ValidationIssue(
                            "url-credentials",
                            f"{location}.url",
                            "must not contain embedded credentials",
                        )
                    )
                previous = seen_urls.get(normalized)
                if previous:
                    issues.append(
                        ValidationIssue(
                            "duplicate-url",
                            f"{location}.url",
                            f"duplicates {previous}",
                        )
                    )
                else:
                    seen_urls[normalized] = str(resource_id or location)

        enum_fields = {
            "source_type": SOURCE_TYPES,
            "level": LEVELS,
            "language": LANGUAGES,
            "status": STATUSES,
            "risk": RISKS,
        }
        for key, allowed in enum_fields.items():
            if resource.get(key) not in allowed:
                issues.append(
                    ValidationIssue(
                        "invalid-enum",
                        f"{location}.{key}",
                        f"must be one of {sorted(allowed)}",
                    )
                )
        for key in ("requires_key", "featured"):
            if not isinstance(resource.get(key), bool):
                issues.append(
                    ValidationIssue(
                        "invalid-boolean", f"{location}.{key}", "must be a boolean"
                    )
                )

        reviewed_on = _date_value(resource.get("reviewed_on"))
        if reviewed_on is None:
            issues.append(
                ValidationIssue(
                    "invalid-date", f"{location}.reviewed_on", "must be YYYY-MM-DD"
                )
            )
        else:
            if reviewed_on > today:
                issues.append(
                    ValidationIssue(
                        "future-date",
                        f"{location}.reviewed_on",
                        "cannot be in the future",
                    )
                )
            elif (today - reviewed_on).days > max_review_age_days:
                issues.append(
                    ValidationIssue(
                        "stale-review",
                        f"{location}.reviewed_on",
                        f"older than {max_review_age_days} days",
                    )
                )
            if catalog_date and reviewed_on > catalog_date:
                issues.append(
                    ValidationIssue(
                        "date-parity",
                        f"{location}.reviewed_on",
                        "cannot be newer than catalog.reviewed_on",
                    )
                )

    for path_id, count in sorted(resources_per_path.items()):
        if count == 0:
            issues.append(
                ValidationIssue(
                    "empty-path", "$.resources", f"path {path_id!r} has no resources"
                )
            )
    return issues


def catalog_resources(data: Mapping[str, Any]) -> Sequence[Mapping[str, Any]]:
    resources = data.get("resources")
    return resources if isinstance(resources, list) else []
