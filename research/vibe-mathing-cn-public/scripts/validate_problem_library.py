#!/usr/bin/env python3
# 校验本地问题库的覆盖率、唯一性、来源追踪、缓存哈希与索引一致性。
# 运行：python3 scripts/validate_problem_library.py
# 依赖：Python 3；不访问网络，不修改问题库。

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator, SchemaError
except ImportError as exc:  # pragma: no cover - 由启动环境决定
    raise SystemExit(
        "缺少 schema 校验依赖。请安装 requirements-problem-library.txt 后重试。"
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / "problem-library"
MANIFEST_PATH = LIBRARY / "manifest.json"
RECORDS_PATH = LIBRARY / "records" / "problems.jsonl"
CATALOG_PATH = LIBRARY / "indexes" / "catalog.json"
BY_SOURCE_PATH = LIBRARY / "indexes" / "by-source.json"
BY_CATEGORY_PATH = LIBRARY / "indexes" / "by-category.json"
SCHEMA_PATH = LIBRARY / "schema" / "problem.schema.json"

MAX_FILE_BYTES = 128_000_000
MAX_RECORDS = 100_000
MAX_LINE_BYTES = 30_000_000
MAX_PATH_CHARS = 4_096


REQUIRED_FIELDS = {
    "id",
    "source",
    "source_native_id",
    "source_order",
    "source_page",
    "detail_url",
    "record_scope",
    "title",
    "statement_excerpt",
    "status",
    "difficulty",
    "categories",
    "problem_sets",
    "related_urls",
    "source_revision",
    "retrieved_at",
    "license",
}


def _nofollow_flag() -> int:
    value = getattr(os, "O_NOFOLLOW", None)
    if value is None:
        raise RuntimeError("当前平台缺少 O_NOFOLLOW，拒绝读取问题库文件")
    return value


def _safe_path(path: Path) -> Path:
    path = Path(path)
    if (
        len(str(path)) > MAX_PATH_CHARS
        or any(part == ".." for part in path.parts)
        or "\x00" in str(path)
        or "\\" in str(path)
    ):
        raise ValueError(f"问题库路径包含非法组件：{path}")
    candidate = path if path.is_absolute() else ROOT / path
    candidate = Path(os.path.abspath(candidate))
    try:
        relative = candidate.relative_to(ROOT)
    except ValueError as exc:
        raise ValueError(f"问题库路径越界：{candidate}") from exc
    current = ROOT
    for part in relative.parts:
        current /= part
        if current.is_symlink():
            raise ValueError(f"问题库路径不能包含 symlink：{candidate}")
    return candidate


def _read_bounded(path: Path, *, max_bytes: int = MAX_FILE_BYTES) -> bytes:
    if (
        not isinstance(max_bytes, int)
        or isinstance(max_bytes, bool)
        or max_bytes <= 0
        or max_bytes > MAX_FILE_BYTES
    ):
        raise ValueError("问题库文件读取大小上限无效")
    candidate = _safe_path(path)
    descriptor = os.open(candidate, os.O_RDONLY | _nofollow_flag())
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode):
            raise ValueError(f"问题库路径不是普通文件：{candidate}")
        if file_stat.st_size > max_bytes:
            raise ValueError(f"问题库文件超过上限 {max_bytes} bytes：{candidate}")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(64 * 1024, max_bytes - total + 1))
            if not chunk:
                return b"".join(chunks)
            total += len(chunk)
            if total > max_bytes:
                raise ValueError(f"问题库文件超过上限 {max_bytes} bytes：{candidate}")
            chunks.append(chunk)
    finally:
        os.close(descriptor)


def _reject_json_constant(value: str) -> Any:
    raise ValueError(f"JSON 常量非法：{value}")


def sha256_file(path: Path, *, max_bytes: int = MAX_FILE_BYTES) -> str:
    # Hash through the same no-follow, regular-file and byte budget checks used
    # for parsing so a concurrent symlink or oversized raw page cannot escape.
    candidate = _safe_path(path)
    if (
        not isinstance(max_bytes, int)
        or isinstance(max_bytes, bool)
        or max_bytes <= 0
        or max_bytes > MAX_FILE_BYTES
    ):
        raise ValueError("问题库哈希大小上限无效")
    descriptor = os.open(candidate, os.O_RDONLY | _nofollow_flag())
    digest = hashlib.sha256()
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode):
            raise ValueError(f"问题库路径不是普通文件：{candidate}")
        if file_stat.st_size > max_bytes:
            raise ValueError(f"问题库文件超过上限 {max_bytes} bytes：{candidate}")
        total = 0
        while True:
            chunk = os.read(descriptor, min(1024 * 1024, max_bytes - total + 1))
            if not chunk:
                return digest.hexdigest()
            total += len(chunk)
            if total > max_bytes:
                raise ValueError(f"问题库文件超过上限 {max_bytes} bytes：{candidate}")
            digest.update(chunk)
    finally:
        os.close(descriptor)


def read_json(path: Path) -> Any:
    return json.loads(_read_bounded(path).decode("utf-8"), parse_constant=_reject_json_constant)


def manifest_path(value: Any, label: str) -> Path:
    if (
        not isinstance(value, str)
        or not value
        or len(value) > MAX_PATH_CHARS
        or "\x00" in value
        or "\\" in value
        or Path(value).is_absolute()
        or any(part in {".", ".."} for part in Path(value).parts)
    ):
        raise ValueError(f"{label} 路径必须是仓库内相对路径")
    return _safe_path(ROOT / value)


def load_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    data = _read_bounded(RECORDS_PATH)
    for line_number, raw_line in enumerate(data.splitlines(), 1):
        if len(raw_line) > MAX_LINE_BYTES:
            raise ValueError(f"records JSONL 第 {line_number} 行超过大小上限")
        if not raw_line.strip():
            continue
        try:
            value = json.loads(
                raw_line.decode("utf-8"), parse_constant=_reject_json_constant
            )
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
            raise ValueError(f"records JSONL 第 {line_number} 行无效：{exc}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"records JSONL 第 {line_number} 行不是对象。")
        records.append(value)
        if len(records) > MAX_RECORDS:
            raise ValueError(f"records JSONL 记录数超过上限 {MAX_RECORDS}")
    return records


def validate() -> list[str]:
    errors: list[str] = []
    required_paths = [MANIFEST_PATH, RECORDS_PATH, CATALOG_PATH, BY_SOURCE_PATH, BY_CATEGORY_PATH, SCHEMA_PATH]
    for path in required_paths:
        if not path.is_file():
            errors.append(f"缺少必需文件：{path.relative_to(ROOT)}")
    if errors:
        return errors
    manifest = read_json(MANIFEST_PATH)
    catalog = read_json(CATALOG_PATH)
    by_source = read_json(BY_SOURCE_PATH)
    by_category = read_json(BY_CATEGORY_PATH)
    records = load_records()
    schema = read_json(SCHEMA_PATH)
    if not all(isinstance(value, dict) for value in (manifest, catalog, by_source, by_category, schema)):
        raise ValueError("问题库 manifest、索引和 schema 顶层必须是对象")
    Draft202012Validator.check_schema(schema)
    schema_validator = Draft202012Validator(schema)
    if manifest.get("records_sha256") != sha256_file(RECORDS_PATH):
        errors.append("records_sha256 与当前 problems.jsonl 不一致。")
    if manifest.get("record_count") != len(records):
        errors.append(f"manifest record_count={manifest.get('record_count')}，实际={len(records)}。")
    ids: set[str] = set()
    native_id_counts: Counter[str] = Counter()
    calculated_by_source: dict[str, list[str]] = defaultdict(list)
    calculated_by_category: dict[str, list[str]] = defaultdict(list)
    for number, record in enumerate(records, 1):
        schema_errors = sorted(schema_validator.iter_errors(record), key=lambda item: list(item.path))
        if schema_errors:
            details = "; ".join(error.message for error in schema_errors[:3])
            errors.append(f"第 {number} 条不符合 problem schema：{details}")
        missing = REQUIRED_FIELDS - record.keys()
        if missing:
            errors.append(f"第 {number} 条缺字段：{sorted(missing)}")
            continue
        record_id = record["id"]
        if not isinstance(record_id, str) or not record_id:
            errors.append(f"第 {number} 条 id 无效。")
            continue
        if record_id in ids:
            errors.append(f"重复 id：{record_id}")
        ids.add(record_id)
        source = record["source"]
        source_key = source if isinstance(source, str) else "<invalid-source>"
        if source_key not in {"wikipedia", "unsolvedmath"}:
            errors.append(f"未知来源：{source}")
        native_id = record["source_native_id"]
        if source == "unsolvedmath" and isinstance(native_id, str) and native_id:
            native_id_counts[native_id] += 1
        if not record["title"] or not record["statement_excerpt"]:
            errors.append(f"空标题或摘要：{record_id}")
        if not isinstance(record["categories"], list) or not record["categories"]:
            errors.append(f"分类缺失：{record_id}")
        license_info = record["license"]
        if not isinstance(license_info, dict) or not license_info.get("name") or not license_info.get("attribution"):
            errors.append(f"许可/归属缺失：{record_id}")
        calculated_by_source[source_key].append(record_id)
        categories = record["categories"] if isinstance(record["categories"], list) else []
        for category in categories:
            if isinstance(category, str):
                calculated_by_category[category].append(record_id)
    source_counts = dict(sorted(Counter(
        record.get("source") if isinstance(record.get("source"), str) else "<invalid-source>"
        for record in records
    ).items()))
    status_counts = dict(sorted(Counter(
        record.get("status") if isinstance(record.get("status"), str) else "<invalid-status>"
        for record in records
    ).items()))
    category_counts = dict(
        sorted(Counter(
            category
            for record in records
            for category in (record.get("categories") if isinstance(record.get("categories"), list) else [])
            if isinstance(category, str)
        ).items())
    )
    if catalog.get("record_count") != len(records):
        errors.append("catalog record_count 不一致。")
    if catalog.get("source_counts") != source_counts:
        errors.append("catalog source_counts 不一致。")
    if catalog.get("status_counts") != status_counts:
        errors.append("catalog status_counts 不一致。")
    if catalog.get("category_counts") != category_counts:
        errors.append("catalog category_counts 不一致。")
    if by_source.get("items") != dict(sorted(calculated_by_source.items())):
        errors.append("by-source 索引与 records 不一致。")
    if by_category.get("items") != dict(sorted(calculated_by_category.items())):
        errors.append("by-category 索引与 records 不一致。")
    sources = manifest.get("sources", {})
    if not isinstance(sources, dict):
        raise ValueError("问题库 manifest.sources 必须是对象")
    unsolved = sources.get("unsolvedmath", {})
    wikipedia = sources.get("wikipedia", {})
    if not isinstance(unsolved, dict) or not isinstance(wikipedia, dict):
        raise ValueError("问题库来源元数据必须是对象")
    if unsolved.get("record_count") != unsolved.get("expected_record_count"):
        errors.append("UnsolvedMath 实际条目数未达到目录声明总数。")
    if unsolved.get("record_count") != source_counts.get("unsolvedmath"):
        errors.append("UnsolvedMath manifest 条目数与 records 不一致。")
    anomalies = unsolved.get("identity_anomalies", {})
    if not isinstance(anomalies, dict):
        raise ValueError("UnsolvedMath identity_anomalies 必须是对象")
    calculated_conflicts = {native_id for native_id, count in native_id_counts.items() if count > 1}
    conflicts = anomalies.get("conflicts", {})
    if not isinstance(conflicts, dict):
        raise ValueError("UnsolvedMath conflicts 必须是对象")
    reported_conflicts = set(conflicts)
    if anomalies.get("distinct_native_id_count") != len(native_id_counts):
        errors.append("UnsolvedMath distinct_native_id_count 与 records 不一致。")
    if anomalies.get("conflicting_native_id_count") != len(calculated_conflicts):
        errors.append("UnsolvedMath conflicting_native_id_count 与 records 不一致。")
    if anomalies.get("excess_rows_over_distinct_native_ids") != sum(native_id_counts.values()) - len(native_id_counts):
        errors.append("UnsolvedMath excess_rows_over_distinct_native_ids 与 records 不一致。")
    if reported_conflicts != calculated_conflicts:
        errors.append("UnsolvedMath manifest 冲突 ID 集合与 records 不一致。")
    pages = unsolved.get("pages", []) if isinstance(unsolved, dict) else []
    if not isinstance(pages, list) or len(pages) > MAX_RECORDS:
        raise ValueError("UnsolvedMath 原始分页数量无效")
    if len(pages) != unsolved.get("page_count"):
        errors.append("UnsolvedMath 原始分页数与 page_count 不一致。")
    page_numbers = [page.get("page") for page in pages if isinstance(page, dict)]
    if len(page_numbers) != len(pages) or page_numbers != list(range(1, len(pages) + 1)):
        errors.append("UnsolvedMath 原始分页序号不连续。")
    page_record_counts = [
        page.get("record_count")
        for page in pages
        if isinstance(page, dict)
    ]
    if any(
        not isinstance(count, int) or isinstance(count, bool) or count < 0
        for count in page_record_counts
    ):
        raise ValueError("UnsolvedMath page record_count 无效")
    page_record_total = sum(page_record_counts)
    if page_record_total != unsolved.get("record_count"):
        errors.append("UnsolvedMath 分页行数之和与 record_count 不一致。")
    for page in pages:
        if not isinstance(page, dict):
            errors.append("UnsolvedMath 原始页条目不是对象。")
            continue
        raw_path = manifest_path(page.get("raw_file"), "UnsolvedMath 原始页")
        if not raw_path.is_file():
            errors.append(f"缺少 UnsolvedMath 原始页：{page.get('raw_file')}")
        elif sha256_file(raw_path) != page.get("raw_sha256"):
            errors.append(f"UnsolvedMath 原始页哈希漂移：{page.get('raw_file')}")
    wiki_raw = manifest_path(wikipedia.get("raw_file"), "Wikipedia 原始快照")
    if not wiki_raw.is_file():
        errors.append(f"缺少 Wikipedia 原始快照：{wikipedia.get('raw_file')}")
    elif sha256_file(wiki_raw) != wikipedia.get("raw_sha256"):
        errors.append("Wikipedia 原始快照哈希漂移。")
    if wikipedia.get("record_count") != source_counts.get("wikipedia"):
        errors.append("Wikipedia manifest 条目数与 records 不一致。")
    wikipedia_license = wikipedia.get("license", {})
    if not isinstance(wikipedia_license, dict) or wikipedia_license.get("url") != "https://creativecommons.org/licenses/by-sa/4.0/deed.en":
        errors.append("Wikipedia 许可不是抓取时 API 返回的 CC BY-SA 4.0。")
    discovery_path = manifest_path(unsolved.get("discovery_file"), "UnsolvedMath 来源发现证据")
    if not discovery_path.is_file():
        errors.append(f"缺少 UnsolvedMath 来源发现证据：{unsolved.get('discovery_file')}")
    elif sha256_file(discovery_path) != unsolved.get("discovery_sha256"):
        errors.append("UnsolvedMath 来源发现证据哈希漂移。")
    discovery = unsolved.get("discovery", {})
    if not isinstance(discovery, dict):
        raise ValueError("UnsolvedMath discovery 必须是对象")
    for name in ("robots", "sitemap"):
        item = discovery.get(name, {})
        if not isinstance(item, dict) or item.get("status") != 404 or not item.get("body_sha256") or not item.get("observed_at"):
            errors.append(f"UnsolvedMath {name} 探测证据不完整或状态不再是 404。")
    return errors


def main() -> int:
    try:
        errors = validate()
    except (OSError, ValueError, KeyError, TypeError, AttributeError, SchemaError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"问题库校验失败：{len(errors)} 个问题。", file=sys.stderr)
        return 1
    manifest = read_json(MANIFEST_PATH)
    sources = manifest["sources"]
    print(
        "问题库校验通过："
        f"总计 {manifest['record_count']} 条；"
        f"Wikipedia {sources['wikipedia']['record_count']}；"
        f"UnsolvedMath {sources['unsolvedmath']['record_count']} / "
        f"{sources['unsolvedmath']['expected_record_count']}，"
        f"原始分页 {sources['unsolvedmath']['page_count']}。"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
