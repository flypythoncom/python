"""Loading and validation helpers for the FlyPython catalog directory."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any
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
    "order",
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
        if not isinstance(key, str):
            raise ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "mapping keys must be strings",
                key_node.start_mark,
            )
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
    """Load either a composed catalog directory or a single YAML mapping.

    The public catalog uses three source layers under ``catalog/``:
    ``catalog.yml`` for metadata, ``paths.yml`` for ordered paths, and one
    file per reviewed resource under ``resources/``. Single-file loading is
    retained for focused validation tests and custom tooling inputs.
    """

    catalog_path = Path(path)
    if catalog_path.is_dir():
        metadata = _load_yaml(catalog_path / "catalog.yml")
        paths = _load_yaml(catalog_path / "paths.yml")
        resources_dir = catalog_path / "resources"

        if not isinstance(metadata, dict):
            metadata_path = catalog_path / "catalog.yml"
            raise CatalogLoadError(
                f"{metadata_path} must contain a YAML mapping"
            )
        if not isinstance(paths, list):
            paths_path = catalog_path / "paths.yml"
            raise CatalogLoadError(f"{paths_path} must contain a YAML list")
        if not resources_dir.is_dir():
            raise CatalogLoadError(f"missing resource directory: {resources_dir}")

        resources: list[dict[str, Any]] = []
        for resource_path in sorted(resources_dir.glob("*.yml")):
            resource = _load_yaml(resource_path)
            if not isinstance(resource, dict):
                raise CatalogLoadError(f"{resource_path} must contain a YAML mapping")
            resource_id = resource.get("id")
            if resource_id != resource_path.stem:
                raise CatalogLoadError(
                    f"{resource_path}: resource id must match filename "
                    f"{resource_path.stem!r}"
                )
            resources.append(resource)

        path_orders: dict[str, int] = {}
        for entry in paths:
            if not isinstance(entry, dict):
                continue
            path_id = entry.get("id")
            path_order = entry.get("order")
            if (
                isinstance(path_id, str)
                and isinstance(path_order, int)
                and not isinstance(path_order, bool)
            ):
                path_orders[path_id] = path_order

        def resource_sort_key(resource: Mapping[str, Any]) -> tuple[int, int, str]:
            path_id = resource.get("path")
            resource_order = resource.get("order")
            return (
                path_orders.get(path_id, 10_000)
                if isinstance(path_id, str)
                else 10_000,
                resource_order
                if isinstance(resource_order, int)
                and not isinstance(resource_order, bool)
                else 10_000,
                str(resource.get("id", "")),
            )

        resources.sort(key=resource_sort_key)
        return {
            "catalog": {**metadata, "paths": paths},
            "resources": resources,
        }

    value = _load_yaml(catalog_path)
    if not isinstance(value, dict):
        raise CatalogLoadError(f"{catalog_path} must contain a YAML mapping")
    return value


def _load_yaml(catalog_path: Path) -> Any:
    try:
        with catalog_path.open("r", encoding="utf-8") as handle:
            value = yaml.load(handle, Loader=UniqueKeyLoader)
    except (OSError, yaml.YAMLError) as exc:
        raise CatalogLoadError(f"cannot load {catalog_path}: {exc}") from exc
    return value


def canonical_hostname(value: str) -> str:
    """Return the lowercase IDNA form used for URL equality and host buckets."""

    return value.rstrip(".").encode("idna").decode("ascii").lower()


def normalize_url(value: str) -> str:
    parsed = urlsplit(value.strip())
    host = canonical_hostname(parsed.hostname or "")
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
    string_keys = {key for key in value if isinstance(key, str)}
    for key in value:
        if not isinstance(key, str):
            issues.append(
                ValidationIssue(
                    "invalid-key",
                    f"{location}[{key!r}]",
                    "mapping keys must be strings",
                )
            )
    for key in sorted(expected - string_keys):
        issues.append(ValidationIssue("missing-field", location, f"missing {key!r}"))
    for key in sorted(string_keys - expected):
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

    expected_path_orders = set(range(1, len(EXPECTED_PATH_IDS) + 1))
    if path_orders != expected_path_orders:
        missing = sorted(expected_path_orders - path_orders)
        extra = sorted(path_orders - expected_path_orders)
        issues.append(
            ValidationIssue(
                "order-parity",
                "$.catalog.paths",
                f"expected consecutive path orders 1-{len(EXPECTED_PATH_IDS)}; "
                f"missing={missing}, extra={extra}",
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
    resource_orders: dict[str, set[int]] = {
        path_id: set() for path_id in EXPECTED_PATH_IDS
    }
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

        order = resource.get("order")
        if not isinstance(order, int) or isinstance(order, bool) or order < 1:
            issues.append(
                ValidationIssue(
                    "invalid-order",
                    f"{location}.order",
                    "must be a positive integer",
                )
            )
        elif isinstance(path_id, str) and path_id in resource_orders:
            if order in resource_orders[path_id]:
                issues.append(
                    ValidationIssue(
                        "duplicate-resource-order",
                        f"{location}.order",
                        f"duplicate order {order} in path {path_id!r}",
                    )
                )
            resource_orders[path_id].add(order)

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
        expected_orders = set(range(1, count + 1))
        if resource_orders[path_id] != expected_orders:
            issues.append(
                ValidationIssue(
                    "resource-order-parity",
                    "$.resources",
                    f"path {path_id!r} must use consecutive resource orders 1-{count}",
                )
            )
    return issues


def catalog_resources(data: Mapping[str, Any]) -> Sequence[Mapping[str, Any]]:
    resources = data.get("resources")
    return resources if isinstance(resources, list) else []
