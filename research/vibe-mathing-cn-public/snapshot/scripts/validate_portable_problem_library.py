#!/usr/bin/env python3
# 做什么：校验可版本化问题记录、schema、manifest 和索引，不依赖被忽略的原始网页。
# 怎么运行：python3 scripts/validate_portable_problem_library.py
# 需要什么：Python 3、jsonschema；只读，不访问网络。

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, SchemaError


ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / "problem-library"
MANIFEST_PATH = LIBRARY / "manifest.json"
RECORDS_PATH = LIBRARY / "records" / "problems.jsonl"
SCHEMA_PATH = LIBRARY / "schema" / "problem.schema.json"
CATALOG_PATH = LIBRARY / "indexes" / "catalog.json"
BY_SOURCE_PATH = LIBRARY / "indexes" / "by-source.json"
BY_CATEGORY_PATH = LIBRARY / "indexes" / "by-category.json"

MAX_FILE_BYTES = 128_000_000
MAX_RECORDS = 100_000
MAX_LINE_BYTES = 30_000_000
MAX_PATH_CHARS = 4_096


def _nofollow_flag() -> int:
    value = getattr(os, "O_NOFOLLOW", None)
    if value is None:
        raise RuntimeError("当前平台缺少 O_NOFOLLOW，拒绝读取问题库文件")
    return value


def _safe_path(path: Path) -> Path:
    path = Path(path)
    if (
        len(str(path)) > MAX_PATH_CHARS
        or any(part in {".", ".."} for part in path.parts)
        or "\x00" in str(path)
        or "\\" in str(path)
    ):
        raise ValueError(f"问题库路径包含非法组件：{path}")
    candidate = Path(os.path.abspath(path if path.is_absolute() else ROOT / path))
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


def load_json(path: Path) -> Any:
    return json.loads(_read_bounded(path).decode("utf-8"), parse_constant=_reject_json_constant)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line_number, raw_line in enumerate(_read_bounded(path).splitlines(), 1):
        if len(raw_line) > MAX_LINE_BYTES:
            raise ValueError(f"问题库 JSONL 第 {line_number} 行超过大小上限")
        if not raw_line.strip():
            continue
        try:
            value = json.loads(raw_line.decode("utf-8"), parse_constant=_reject_json_constant)
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
            raise ValueError(f"问题库 JSONL 第 {line_number} 行无效：{exc}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"问题库 JSONL 第 {line_number} 行不是对象")
        records.append(value)
        if len(records) > MAX_RECORDS:
            raise ValueError(f"问题库 JSONL 记录数超过上限 {MAX_RECORDS}")
    return records


def sha256_file(path: Path, *, max_bytes: int = MAX_FILE_BYTES) -> str:
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


def main() -> int:
    errors: list[str] = []
    if not SCHEMA_PATH.is_file():
        print(f"ERROR: 缺少必需文件：{SCHEMA_PATH.relative_to(ROOT)}", file=sys.stderr)
        return 1

    dataset_paths = [MANIFEST_PATH, RECORDS_PATH, CATALOG_PATH, BY_SOURCE_PATH, BY_CATEGORY_PATH]
    existing_dataset_paths = [path for path in dataset_paths if path.is_file()]
    if not existing_dataset_paths:
        try:
            schema = load_json(SCHEMA_PATH)
            Draft202012Validator.check_schema(schema)
        except (OSError, ValueError, KeyError, TypeError, AttributeError, SchemaError) as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1
        print("可移植问题库校验通过：未携带可重建来源数据，schema 有效。")
        return 0
    if len(existing_dataset_paths) != len(dataset_paths):
        for path in dataset_paths:
            if not path.is_file():
                print(f"ERROR: 本地问题库数据不完整，缺少：{path.relative_to(ROOT)}", file=sys.stderr)
        return 1

    try:
        manifest = load_json(MANIFEST_PATH)
        records = load_jsonl(RECORDS_PATH)
        schema = load_json(SCHEMA_PATH)
        catalog = load_json(CATALOG_PATH)
        by_source = load_json(BY_SOURCE_PATH)
        by_category = load_json(BY_CATEGORY_PATH)
        if not all(isinstance(value, dict) for value in (manifest, schema, catalog, by_source, by_category)):
            raise ValueError("问题库 manifest、索引和 schema 顶层必须是对象")
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        ids: set[str] = set()
        calculated_by_source: dict[str, list[str]] = defaultdict(list)
        calculated_by_category: dict[str, list[str]] = defaultdict(list)
        for position, record in enumerate(records, 1):
            for error in sorted(validator.iter_errors(record), key=lambda item: list(item.path)):
                errors.append(f"第 {position} 条 schema 错误：{error.message}")
            record_id = record.get("id")
            if isinstance(record_id, str) and record_id in ids:
                errors.append(f"重复 id：{record_id}")
            if isinstance(record_id, str):
                ids.add(record_id)
                source = record.get("source")
                if not isinstance(source, str):
                    source = "<invalid-source>"
                calculated_by_source[source].append(record_id)
                categories = record.get("categories", [])
                if isinstance(categories, list):
                    for category in categories:
                        if isinstance(category, str):
                            calculated_by_category[category].append(record_id)
        source_counts = dict(sorted(Counter(
            item.get("source") if isinstance(item.get("source"), str) else "<invalid-source>"
            for item in records
        ).items()))
        status_counts = dict(sorted(Counter(
            item.get("status") if isinstance(item.get("status"), str) else "<invalid-status>"
            for item in records
        ).items()))
        category_counts = dict(
            sorted(Counter(
                category
                for item in records
                for category in (item.get("categories") if isinstance(item.get("categories"), list) else [])
                if isinstance(category, str)
            ).items())
        )
        if manifest.get("record_count") != len(records):
            errors.append("manifest record_count 与 records 不一致")
        if manifest.get("records_sha256") != sha256_file(RECORDS_PATH):
            errors.append("manifest records_sha256 与 records 不一致")
        if catalog.get("record_count") != len(records):
            errors.append("catalog record_count 与 records 不一致")
        if catalog.get("source_counts") != source_counts:
            errors.append("catalog source_counts 与 records 不一致")
        if catalog.get("status_counts") != status_counts:
            errors.append("catalog status_counts 与 records 不一致")
        if catalog.get("category_counts") != category_counts:
            errors.append("catalog category_counts 与 records 不一致")
        if by_source.get("items") != dict(sorted(calculated_by_source.items())):
            errors.append("by-source 索引与 records 不一致")
        if by_category.get("items") != dict(sorted(calculated_by_category.items())):
            errors.append("by-category 索引与 records 不一致")
    except (OSError, ValueError, KeyError, TypeError, AttributeError, SchemaError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"可移植问题库校验失败：{len(errors)} 个问题。", file=sys.stderr)
        return 1
    print(f"可移植问题库校验通过：{len(records)} 条来源记录。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
