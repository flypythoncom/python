from __future__ import annotations

from datetime import date
from typing import Any

import pytest


@pytest.fixture
def valid_catalog() -> dict[str, Any]:
    paths = []
    resources = []
    for order, path_id in enumerate(
        ("foundations", "web-apis", "automation", "ai-agents"), start=1
    ):
        paths.append(
            {
                "id": path_id,
                "title_en": f"{path_id} title",
                "title_zh": f"{path_id} 标题",
                "summary_en": f"{path_id} summary",
                "summary_zh": f"{path_id} 摘要",
                "order": order,
            }
        )
        resources.append(
            {
                "id": f"resource-{order}",
                "path": path_id,
                "title": f"Resource {order}",
                "url": f"https://example{order}.com/docs/",
                "source_type": "official-docs",
                "level": "beginner",
                "language": "en",
                "why_en": "Primary documentation maintained by the project.",
                "why_zh": "由项目维护的官方文档。",
                "reviewed_on": date(2026, 8, 31),
                "status": "active",
                "requires_key": False,
                "risk": "low",
                "featured": order == 1,
                "order": 1,
            }
        )
    return {
        "catalog": {
            "reviewed_on": date(2026, 8, 31),
            "status": "active",
            "paths": paths,
        },
        "resources": resources,
    }
