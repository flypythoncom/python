#!/usr/bin/env python3
"""Export website metadata and claim contracts without importing course code."""
from __future__ import annotations

import argparse
import ast
import json
import re
from pathlib import Path

from jsonschema import validate

from tools.content_manifest import _metadata, build_manifest

ROOT = Path(__file__).resolve().parents[1]


def verifier_contract(path: Path) -> dict:
    values = {}
    for node in ast.parse(path.read_text(encoding="utf-8")).body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in {"COURSE_ID", "COURSE_SALT", "CHECKPOINTS"}:
                    values[target.id] = ast.literal_eval(node.value)
    if not re.fullmatch(r"course-[a-z0-9-]+", values["COURSE_ID"]) or not re.fullmatch(r"[0-9a-f]{16}", values["COURSE_SALT"]):
        raise ValueError(f"{path}: invalid course ID or public salt")
    checkpoints = values["CHECKPOINTS"]
    ids = [cp["id"] for cp in checkpoints]
    if not ids or len(ids) != len(set(ids)):
        raise ValueError(f"{path}: duplicate or missing checkpoints")
    if any(cp["gate"] not in {"attest", "starter-suite", "both-suites"} for cp in checkpoints):
        raise ValueError(f"{path}: unsupported checkpoint gate")
    return {"courseId": values["COURSE_ID"], "salt": values["COURSE_SALT"],
            "checkpoints": ids, "gated": [cp["id"] for cp in checkpoints if cp["gate"] != "attest"]}


def build_registry(root: Path = ROOT) -> dict:
    schema = json.loads((root / "schemas/course-website.schema.json").read_text())
    manifest = {doc["id"]: doc for doc in build_manifest(root)["documents"]}
    records = []
    contracts = {}
    agent_tools = []
    orders = set()
    course_ids = set()
    folders = sorted((root / "courses").glob("*/COURSE.md"))
    for document in folders:
        folder = document.parent
        source = json.loads((folder / "website.json").read_text(encoding="utf-8"))
        validate(source, schema)
        metadata = _metadata(document)
        if metadata is None:
            raise ValueError(f"{document}: missing course metadata")
        translated = _metadata(folder / "COURSE_cn.md")
        if translated is None or translated["course_id"] != metadata["course_id"]:
            raise ValueError(f"{folder}: bilingual course_id mismatch")
        course = {key: value for key, value in source.items() if key not in {"order", "agentTool", "aliases"}}
        if source["id"] != folder.name or source["order"] in orders:
            raise ValueError(f"{folder}: slug mismatch or duplicate order")
        orders.add(source["order"])
        contract = verifier_contract(folder / "verify.py")
        if contract["courseId"] != metadata["course_id"] or contract["courseId"] in course_ids:
            raise ValueError(f"{folder}: course_id mismatch or duplicate")
        course_ids.add(contract["courseId"])
        if [lesson["id"] for lesson in course["lessons"]] != contract["checkpoints"]:
            raise ValueError(f"{folder}: lessons must match verifier checkpoints in order")
        for lesson in course["lessons"]:
            for suffix in (".md", "_cn.md"):
                if not (folder / "lessons" / (lesson["id"].upper() + suffix)).is_file():
                    raise ValueError(f"{folder}: missing bilingual lesson {lesson['id']}{suffix}")
        entry = manifest[metadata["id"]]
        course.update(repoDir=folder.relative_to(root).as_posix(), manifestId=entry["id"],
                      manifestVersion=entry["content_version"], reviewedAt=entry["reviewed_on"])
        records.append((source["order"], course))
        for slug in [course["id"], *source["aliases"]]:
            if slug in contracts:
                raise ValueError(f"duplicate course or alias: {slug}")
            contracts[slug] = dict(contract)
            if slug != course["id"]:
                contracts[slug]["aliasOf"] = course["id"]
        if source["agentTool"]:
            agent_tools.append((source["order"], course["id"]))
    if not records:
        raise ValueError("no courses found")
    ordered_contracts = {}
    for _, course in sorted(records):
        ordered_contracts[course["id"]] = contracts[course["id"]]
        ordered_contracts.update((slug, contract) for slug, contract in contracts.items()
                                 if contract.get("aliasOf") == course["id"])
    return {"schema_version": 1, "courses": [course for _, course in sorted(records)],
            "contracts": ordered_contracts,
            "agentToolCourseIds": [slug for _, slug in sorted(agent_tools)]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    rendered = json.dumps(build_registry(), ensure_ascii=False, indent=2) + "\n"
    target = ROOT / "course-registry.json"
    if args.check:
        if not target.exists() or target.read_text(encoding="utf-8") != rendered:
            parser.exit(1, "course-registry.json is stale; run make registry\n")
        print("course registry is current")
    else:
        target.write_text(rendered, encoding="utf-8")
        print("wrote course-registry.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
