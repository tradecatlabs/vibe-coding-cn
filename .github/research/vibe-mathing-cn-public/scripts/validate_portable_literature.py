#!/usr/bin/env python3
# 做什么：校验可版本化的文献目录、schema 和引用，不依赖本地电子书二进制。
# 怎么运行：python3 scripts/validate_portable_literature.py
# 需要什么：Python 3、jsonschema；只读，不访问电子书文件。

from __future__ import annotations

import json
import os
import stat
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, SchemaError


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "literature" / "catalog"
SCHEMA_PATH = ROOT / "literature" / "schema" / "literature-records.schema.json"
MAX_CATALOG_BYTES = 128_000_000
MAX_RECORDS = 100_000
MAX_LINE_BYTES = 30_000_000
MAX_PATH_CHARS = 4_096


FILES = {
    "work": CATALOG / "works.jsonl",
    "edition": CATALOG / "editions.jsonl",
    "file": CATALOG / "files.jsonl",
    "relation": CATALOG / "relations.jsonl",
}


def _nofollow_flag() -> int:
    value = getattr(os, "O_NOFOLLOW", None)
    if value is None:
        raise RuntimeError("当前平台缺少 O_NOFOLLOW，拒绝读取文献目录")
    return value


def _safe_path(path: Path) -> Path:
    path = Path(path)
    if (
        len(str(path)) > MAX_PATH_CHARS
        or any(part in {".", ".."} for part in path.parts)
        or "\x00" in str(path)
        or "\\" in str(path)
    ):
        raise ValueError(f"文献路径包含非法组件：{path}")
    candidate = Path(os.path.abspath(path if path.is_absolute() else ROOT / path))
    try:
        relative = candidate.relative_to(ROOT)
    except ValueError as exc:
        raise ValueError(f"文献路径越界：{candidate}") from exc
    current = ROOT
    for part in relative.parts:
        current /= part
        if current.is_symlink():
            raise ValueError(f"文献路径不能包含 symlink：{candidate}")
    return candidate


def _read_bounded(path: Path) -> bytes:
    candidate = _safe_path(path)
    descriptor = os.open(candidate, os.O_RDONLY | _nofollow_flag())
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode) or file_stat.st_size > MAX_CATALOG_BYTES:
            raise ValueError(f"文献目录文件超过大小预算：{candidate}")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(64 * 1024, MAX_CATALOG_BYTES - total + 1))
            if not chunk:
                return b"".join(chunks)
            total += len(chunk)
            if total > MAX_CATALOG_BYTES:
                raise ValueError(f"文献目录文件超过大小预算：{candidate}")
            chunks.append(chunk)
    finally:
        os.close(descriptor)


def _reject_json_constant(value: str) -> Any:
    raise ValueError(f"JSON 常量非法：{value}")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line_number, raw_line in enumerate(_read_bounded(path).splitlines(), 1):
        if len(raw_line) > MAX_LINE_BYTES:
            raise ValueError(f"{path.relative_to(ROOT)}:{line_number}: 行超过大小上限")
        if not raw_line.strip():
            continue
        value = json.loads(raw_line.decode("utf-8"), parse_constant=_reject_json_constant)
        if not isinstance(value, dict):
            raise ValueError(f"{path.relative_to(ROOT)}:{line_number}: 记录不是对象")
        records.append(value)
        if len(records) > MAX_RECORDS:
            raise ValueError(f"{path.relative_to(ROOT)}: 记录数超过上限 {MAX_RECORDS}")
    return records


def load_json(path: Path) -> Any:
    return json.loads(_read_bounded(path).decode("utf-8"), parse_constant=_reject_json_constant)


def isbn13_valid(value: str) -> bool:
    if len(value) != 13 or not value.isdigit():
        return False
    total = sum(int(char) * (1 if index % 2 == 0 else 3) for index, char in enumerate(value[:12]))
    return (10 - total % 10) % 10 == int(value[-1])


def main() -> int:
    errors: list[str] = []
    required = [SCHEMA_PATH, *FILES.values()]
    for path in required:
        if not path.is_file():
            errors.append(f"缺少必需文件：{path.relative_to(ROOT)}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    try:
        schema = load_json(SCHEMA_PATH)
        if not isinstance(schema, dict) or not isinstance(schema.get("$defs"), dict):
            raise ValueError("文献 schema 顶层或 $defs 无效")
        Draft202012Validator.check_schema(schema)
        records = {kind: load_jsonl(path) for kind, path in FILES.items()}
        all_ids: set[str] = set()
        id_fields = {"work": "work_id", "edition": "edition_id", "file": "file_id", "relation": "relation_id"}
        for kind, items in records.items():
            validator = Draft202012Validator({"$ref": f"#/$defs/{kind}", "$defs": schema["$defs"]})
            for position, record in enumerate(items, 1):
                for error in sorted(validator.iter_errors(record), key=lambda item: list(item.path)):
                    errors.append(f"{kind} 第 {position} 条 schema 错误：{error.message}")
                record_id = record.get(id_fields[kind])
                if isinstance(record_id, str) and record_id in all_ids:
                    errors.append(f"重复 ID：{record_id}")
                if isinstance(record_id, str):
                    all_ids.add(record_id)
        work_ids = {item["work_id"] for item in records["work"]}
        edition_ids = {item["edition_id"] for item in records["edition"]}
        file_ids = {item["file_id"] for item in records["file"]}
        for edition in records["edition"]:
            if edition["work_id"] not in work_ids:
                errors.append(f"Edition 引用不存在的 Work：{edition['work_id']}")
            if not isbn13_valid(edition["isbn13"]):
                errors.append(f"ISBN-13 校验位错误：{edition['isbn13']}")
        for item in records["file"]:
            if item["edition_id"] not in edition_ids:
                errors.append(f"File 引用不存在的 Edition：{item['edition_id']}")
            file_path = item["path"]
            if (
                not isinstance(file_path, str)
                or len(file_path) > MAX_PATH_CHARS
                or "\x00" in file_path
                or "\\" in file_path
                or Path(file_path).is_absolute()
                or any(part in {".", ".."} for part in Path(file_path).parts)
                or not file_path.startswith("literature/files/")
            ):
                errors.append(f"File 路径越出 literature/files：{file_path}")
        entity_ids = work_ids | edition_ids | file_ids
        for relation in records["relation"]:
            if relation["subject_id"] not in entity_ids:
                errors.append(f"Relation subject 不存在：{relation['subject_id']}")
            if relation["predicate"] in {"has_edition", "has_file"} and relation["object_id"] not in entity_ids:
                errors.append(f"Relation object 不存在：{relation['object_id']}")
    except (OSError, ValueError, KeyError, TypeError, AttributeError, SchemaError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"可移植文献库校验失败：{len(errors)} 个问题。", file=sys.stderr)
        return 1
    print(
        "可移植文献库校验通过："
        f"Work {len(records['work'])}；Edition {len(records['edition'])}；"
        f"File {len(records['file'])}；Relation {len(records['relation'])}。"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
