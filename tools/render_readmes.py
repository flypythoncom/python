#!/usr/bin/env python3
"""Render catalog sections: a condensed index in the root READMEs, the full
resource tables in catalog/README{,_cn}.md, and the Project Radar tables."""

from __future__ import annotations

import argparse
import html
import sys
from collections.abc import Mapping, Sequence
from datetime import date, datetime
from pathlib import Path
from typing import Any
from urllib.parse import quote

try:
    from tools.catalog import (
        CatalogLoadError,
        load_catalog,
        load_radar,
        validate_catalog,
        validate_radar,
    )
except ModuleNotFoundError:  # Direct ``python tools/render_readmes.py`` execution.
    from catalog import (
        CatalogLoadError,
        load_catalog,
        load_radar,
        validate_catalog,
        validate_radar,
    )


ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_CATALOG = ROOT_DIR / "catalog"
START_MARKER = "<!-- catalog-index:start -->"
END_MARKER = "<!-- catalog-index:end -->"
RADAR_START_MARKER = "<!-- radar-index:start -->"
RADAR_END_MARKER = "<!-- radar-index:end -->"

RADAR_CATEGORY_LABELS = {
    "en": {
        "tooling-packaging": "Tooling & Packaging",
        "code-quality": "Code Quality",
        "web-apis": "Web & APIs",
        "ai-agents": "AI Agents",
        "ai-tools": "AI Tools",
        "data-pipelines": "Data & Pipelines",
        "notebooks": "Interactive Notebooks",
    },
    "zh": {
        "tooling-packaging": "工具与打包",
        "code-quality": "代码质量",
        "web-apis": "Web 与 API",
        "ai-agents": "AI Agent",
        "ai-tools": "AI 工具",
        "data-pipelines": "数据与管线",
        "notebooks": "交互式笔记本",
    },
}
AI_FAMILIARITY_LABELS = {
    "en": {
        "low": "AI: low",
        "medium": "AI: medium",
        "high": "AI: high",
    },
    "zh": {
        "low": "AI 熟悉度：低",
        "medium": "AI 熟悉度：中",
        "high": "AI 熟悉度：高",
    },
}

LEVEL_LABELS = {
    "en": {
        "beginner": "Beginner",
        "intermediate": "Intermediate",
        "advanced": "Advanced",
        "all-levels": "All levels",
    },
    "zh": {
        "beginner": "入门",
        "intermediate": "进阶",
        "advanced": "高级",
        "all-levels": "所有阶段",
    },
}
LANGUAGE_LABELS = {
    "en": {"en": "English", "zh": "Chinese", "multilingual": "Multilingual"},
    "zh": {"en": "英语", "zh": "中文", "multilingual": "多语言"},
}
SOURCE_LABELS = {
    "en": {
        "official-docs": "Official docs",
        "official-standard": "Official standard",
        "official-project": "Official project",
    },
    "zh": {
        "official-docs": "官方文档",
        "official-standard": "正式标准",
        "official-project": "官方项目",
    },
}


def _text(value: Any) -> str:
    escaped = html.escape(str(value), quote=False)
    return (
        escaped.replace("\\", "\\\\")
        .replace("|", "\\|")
        .replace("[", "\\[")
        .replace("]", "\\]")
        .replace("\n", " ")
    )


def _url(value: Any) -> str:
    return quote(str(value), safe=":/?&=#%@+;,~-._")


def _date_text(value: Any) -> str:
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    return _text(value)


def _resource_meta(resource: Mapping[str, Any], lang: str) -> str:
    source = SOURCE_LABELS[lang][str(resource["source_type"])]
    featured = "Featured" if lang == "en" else "精选"
    if resource.get("featured"):
        return f"{source} · {featured}"
    return source


def _access_and_risk(resource: Mapping[str, Any], lang: str) -> str:
    if lang == "zh":
        access = (
            "通常需要 API Key" if resource["requires_key"] else "无需 API Key"
        )
        risk = (
            "检查权限与副作用" if resource["risk"] == "medium" else "低风险"
        )
    else:
        access = (
            "API key typically required"
            if resource["requires_key"]
            else "No API key"
        )
        risk = (
            "Review permissions and side effects"
            if resource["risk"] == "medium"
            else "Low risk"
        )
    return f"{access}<br>{risk}"


def _review_summary(
    metadata: Mapping[str, Any],
    resources: Sequence[Mapping[str, Any]],
    *,
    lang: str,
) -> str:
    engineering_depth_count = sum(
        resource["level"] in {"intermediate", "advanced"}
        for resource in resources
    )
    if lang == "zh":
        return (
            f"> **{len(resources)} 条已审核资源** · 最近整体审核："
            f"{_date_text(metadata['reviewed_on'])} · "
            f"{engineering_depth_count} 条进阶或高级资源 · 一手来源优先"
        )
    return (
        f"> **{len(resources)} reviewed resources** · Catalog reviewed "
        f"{_date_text(metadata['reviewed_on'])} · "
        f"{engineering_depth_count} intermediate or advanced · "
        "Primary sources first"
    )


def _path_bullets(
    metadata: Mapping[str, Any],
    resources: Sequence[Mapping[str, Any]],
    *,
    lang: str,
    link_prefix: str,
) -> list[str]:
    lines: list[str] = []
    for path in metadata["paths"]:
        title = path["title_zh"] if lang == "zh" else path["title_en"]
        summary = path["summary_zh"] if lang == "zh" else path["summary_en"]
        path_resources = [item for item in resources if item["path"] == path["id"]]
        unit = "条资源" if lang == "zh" else "resources"
        lines.append(
            f"- [**{_text(title)}**]({link_prefix}#path-{path['id']}) — {_text(summary)} "
            f"({len(path_resources)} {unit})"
        )
    return lines


def _contribution_line(*, lang: str) -> str:
    if lang == "zh":
        return (
            "没有找到合适的官方资料？可以[建议资源或报告错误]"
            "(https://github.com/flypythoncom/python/issues/new/choose)。"
        )
    return (
        "Missing an important official source? "
        "[Propose a resource or report a correction]"
        "(https://github.com/flypythoncom/python/issues/new/choose)."
    )


def render_catalog_index(
    data: Mapping[str, Any], *, lang: str, condensed: bool = False
) -> str:
    if lang not in {"en", "zh"}:
        raise ValueError("lang must be 'en' or 'zh'")

    metadata = data["catalog"]
    paths: Sequence[Mapping[str, Any]] = metadata["paths"]
    resources: Sequence[Mapping[str, Any]] = data["resources"]
    lines: list[str] = [
        START_MARKER,
        "<!-- Generated by tools/render_readmes.py; edit catalog/ instead. -->",
        _review_summary(metadata, resources, lang=lang),
    ]

    if condensed:
        # Root READMEs carry only the path summary and link to the catalog
        # READMEs for the full per-resource tables.
        catalog_readme = "catalog/README_cn.md" if lang == "zh" else "catalog/README.md"
        if lang == "zh":
            browse = (
                f"完整的收录理由、难度、访问与风险说明见"
                f"[完整目录]({catalog_readme})。"
            )
        else:
            browse = (
                f"Full tables — why each source is included, its level, and its "
                f"access and risk notes — live in [the catalog README]({catalog_readme})."
            )
        lines.extend(["", *_path_bullets(metadata, resources, lang=lang, link_prefix=catalog_readme), "", browse, ""])
        lines.extend([_contribution_line(lang=lang), END_MARKER])
        return "\n".join(lines)

    if lang == "zh":
        lines.extend(["", "### 选择学习路径", ""])
    else:
        lines.extend(["", "### Choose a learning path", ""])

    lines.extend(_path_bullets(metadata, resources, lang=lang, link_prefix=""))

    for path in paths:
        title = path["title_zh"] if lang == "zh" else path["title_en"]
        summary = path["summary_zh"] if lang == "zh" else path["summary_en"]
        path_resources = [item for item in resources if item["path"] == path["id"]]
        lines.extend(
            [
                "",
                f'<a id="path-{path["id"]}"></a>',
                f"### {_text(title)}",
                "",
                _text(summary),
                "",
            ]
        )

        if lang == "zh":
            lines.extend(
                [
                    "| 资源 | 为什么值得看 | 难度与语言 | "
                    "访问与风险 | 审核日期 |",
                    "| --- | --- | --- | --- | --- |",
                ]
            )
        else:
            lines.extend(
                [
                    "| Resource | Why it is useful | Level and language | "
                    "Access and risk | Reviewed |",
                    "| --- | --- | --- | --- | --- |",
                ]
            )

        for resource in path_resources:
            why = resource["why_zh"] if lang == "zh" else resource["why_en"]
            level = LEVEL_LABELS[lang][str(resource["level"])]
            language = LANGUAGE_LABELS[lang][str(resource["language"])]
            resource_link = (
                f"[{_text(resource['title'])}]({_url(resource['url'])})"
                f"<br><sub>{_resource_meta(resource, lang)}</sub>"
            )
            lines.append(
                "| "
                + " | ".join(
                    (
                        resource_link,
                        _text(why),
                        f"{level}<br>{language}",
                        _access_and_risk(resource, lang),
                        _date_text(resource["reviewed_on"]),
                    )
                )
                + " |"
            )

    lines.extend(["", _contribution_line(lang=lang), END_MARKER])
    return "\n".join(lines)


def replace_generated_block(content: str, generated: str) -> str:
    if content.count(START_MARKER) != 1 or content.count(END_MARKER) != 1:
        raise ValueError("README must contain exactly one catalog marker pair")
    before, remainder = content.split(START_MARKER, maxsplit=1)
    _, after = remainder.split(END_MARKER, maxsplit=1)
    return before + generated + after


def render_radar_index(
    projects: Sequence[Mapping[str, Any]], *, lang: str
) -> str:
    if lang not in {"en", "zh"}:
        raise ValueError("lang must be 'en' or 'zh'")

    lines: list[str] = [
        RADAR_START_MARKER,
        "<!-- Generated by tools/render_readmes.py; edit catalog/projects/*.yml instead. -->",
    ]
    if lang == "zh":
        lines.extend(
            [
                "| 项目 | 类别 | 状态 | AI 熟悉度 | 推荐理由 | 何时不用 / 风险 | 审核日期 |",
                "| --- | --- | --- | --- | --- | --- | --- |",
            ]
        )
    else:
        lines.extend(
            [
                "| Project | Category | Status | AI familiarity | Why it matters | When not to use / Risk | Reviewed |",
                "| --- | --- | --- | --- | --- | --- | --- |",
            ]
        )

    for project in projects:
        repo = str(project["repo"])
        name = repo.split("/", 1)[1]
        category = RADAR_CATEGORY_LABELS[lang][str(project["category"])]
        familiarity = AI_FAMILIARITY_LABELS[lang][str(project["ai_familiarity"])]
        if lang == "zh":
            rationale = project["rationale_zh"]
            caution = f"{project['when_not_to_use_zh']}<br>**风险：**{project['risk_zh']}"
        else:
            rationale = project["rationale_en"]
            caution = f"{project['when_not_to_use_en']}<br>**Risk:** {project['risk_en']}"
        project_link = (
            f"[{_text(name)}]({_url(project['url'])})"
            f"<br><sub>{_text(project['repo'])} · {_text(project['license'])}</sub>"
        )
        lines.append(
            "| "
            + " | ".join(
                (
                    project_link,
                    _text(category),
                    f"`{project['status']}`",
                    _text(familiarity),
                    _text(rationale),
                    _text(caution),
                    _date_text(project["reviewed_on"]),
                )
            )
            + " |"
        )

    lines.append(RADAR_END_MARKER)
    return "\n".join(lines)


def replace_radar_block(content: str, generated: str) -> str:
    if (
        content.count(RADAR_START_MARKER) != 1
        or content.count(RADAR_END_MARKER) != 1
    ):
        raise ValueError("Radar README must contain exactly one radar marker pair")
    before, remainder = content.split(RADAR_START_MARKER, maxsplit=1)
    _, after = remainder.split(RADAR_END_MARKER, maxsplit=1)
    return before + generated + after


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail when either generated README section is out of date",
    )
    return parser


def run(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        data = load_catalog(args.catalog)
    except CatalogLoadError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    try:
        radar_projects = load_radar(args.catalog / "projects")
    except CatalogLoadError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    issues = validate_catalog(data)
    issues += list(validate_radar(radar_projects))
    if issues:
        for issue in issues:
            print(f"{issue.location}: {issue.code}: {issue.message}", file=sys.stderr)
        return 1

    targets = (
        (
            ROOT_DIR / "README.md",
            render_catalog_index(data, lang="en", condensed=True),
            replace_generated_block,
        ),
        (
            ROOT_DIR / "README_cn.md",
            render_catalog_index(data, lang="zh", condensed=True),
            replace_generated_block,
        ),
        (
            ROOT_DIR / "catalog" / "README.md",
            render_catalog_index(data, lang="en"),
            replace_generated_block,
        ),
        (
            ROOT_DIR / "catalog" / "README_cn.md",
            render_catalog_index(data, lang="zh"),
            replace_generated_block,
        ),
        (
            ROOT_DIR / "catalog" / "projects" / "README.md",
            render_radar_index(radar_projects, lang="en"),
            replace_radar_block,
        ),
        (
            ROOT_DIR / "catalog" / "projects" / "README_cn.md",
            render_radar_index(radar_projects, lang="zh"),
            replace_radar_block,
        ),
    )
    stale: list[Path] = []
    for path, generated, replacer in targets:
        current = path.read_text(encoding="utf-8")
        try:
            expected = replacer(current, generated)
        except ValueError as exc:
            print(f"{path}: {exc}", file=sys.stderr)
            return 2
        if current == expected:
            continue
        if args.check:
            stale.append(path)
        else:
            path.write_text(expected, encoding="utf-8")
            print(f"updated {path}")

    if stale:
        for path in stale:
            print(f"generated section is out of date: {path}", file=sys.stderr)
        return 1
    if args.check:
        print("README catalog and radar sections current")
    return 0


def main() -> None:
    raise SystemExit(run())


if __name__ == "__main__":
    main()
