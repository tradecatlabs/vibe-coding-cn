#!/usr/bin/env python3
# 校验电子书 Work/Edition/File/Relation 目录、引用完整性和本地文件摘要。
# 运行：python3 scripts/validate_literature.py
# 依赖：Python 3、jsonschema；只读访问 literature/，不修改电子书。

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, SchemaError


ROOT = Path(__file__).resolve().parents[1]
LITERATURE = ROOT / "literature"
CATALOG = LITERATURE / "catalog"
SCHEMA_PATH = LITERATURE / "schema" / "literature-records.schema.json"
MAX_CATALOG_BYTES = 128_000_000
MAX_RECORDS = 100_000
MAX_LINE_BYTES = 30_000_000
MAX_LOCAL_FILE_BYTES = 4 * 1024 * 1024 * 1024
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
        raise RuntimeError("当前平台缺少 O_NOFOLLOW，拒绝读取文献文件")
    return value


def _safe_path(path: Path, *, root: Path = ROOT) -> Path:
    path = Path(path)
    if (
        len(str(path)) > MAX_PATH_CHARS
        or any(part == ".." for part in path.parts)
        or "\x00" in str(path)
        or "\\" in str(path)
    ):
        raise ValueError(f"文献路径包含非法组件：{path}")
    candidate = Path(os.path.abspath(path if path.is_absolute() else root / path))
    try:
        relative = candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"文献路径越界：{candidate}") from exc
    current = root
    for part in relative.parts:
        current /= part
        if current.is_symlink():
            raise ValueError(f"文献路径不能包含 symlink：{candidate}")
    return candidate


def _read_bounded(path: Path, *, max_bytes: int = MAX_CATALOG_BYTES) -> bytes:
    if (
        not isinstance(max_bytes, int)
        or isinstance(max_bytes, bool)
        or max_bytes <= 0
        or max_bytes > MAX_CATALOG_BYTES
    ):
        raise ValueError("文献目录读取大小上限无效")
    candidate = _safe_path(path)
    descriptor = os.open(candidate, os.O_RDONLY | _nofollow_flag())
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode):
            raise ValueError(f"文献路径不是普通文件：{candidate}")
        if file_stat.st_size > max_bytes:
            raise ValueError(f"文献目录文件超过上限 {max_bytes} bytes：{candidate}")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(64 * 1024, max_bytes - total + 1))
            if not chunk:
                return b"".join(chunks)
            total += len(chunk)
            if total > max_bytes:
                raise ValueError(f"文献目录文件超过上限 {max_bytes} bytes：{candidate}")
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
        try:
            value = json.loads(raw_line.decode("utf-8"), parse_constant=_reject_json_constant)
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
            raise ValueError(f"{path.relative_to(ROOT)}:{line_number}: JSON 无效：{exc}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"{path.relative_to(ROOT)}:{line_number}: 记录不是对象。")
        records.append(value)
        if len(records) > MAX_RECORDS:
            raise ValueError(f"{path.relative_to(ROOT)}: 记录数超过上限 {MAX_RECORDS}")
    return records


def read_json(path: Path) -> Any:
    return json.loads(_read_bounded(path).decode("utf-8"), parse_constant=_reject_json_constant)


def regular_file_size(path: Path) -> int:
    candidate = _safe_path(path)
    descriptor = os.open(candidate, os.O_RDONLY | _nofollow_flag())
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode):
            raise ValueError(f"文献路径不是普通文件：{candidate}")
        if file_stat.st_size > MAX_LOCAL_FILE_BYTES:
            raise ValueError(f"电子书文件超过上限 {MAX_LOCAL_FILE_BYTES} bytes：{candidate}")
        return file_stat.st_size
    finally:
        os.close(descriptor)


def sha256_file(path: Path, *, max_bytes: int = MAX_LOCAL_FILE_BYTES) -> str:
    if (
        not isinstance(max_bytes, int)
        or isinstance(max_bytes, bool)
        or max_bytes <= 0
        or max_bytes > MAX_LOCAL_FILE_BYTES
    ):
        raise ValueError("文献文件哈希大小上限无效")
    candidate = _safe_path(path, root=ROOT)
    descriptor = os.open(candidate, os.O_RDONLY | _nofollow_flag())
    digest = hashlib.sha256()
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode):
            raise ValueError(f"文献路径不是普通文件：{candidate}")
        if file_stat.st_size > max_bytes:
            raise ValueError(f"电子书文件超过上限 {max_bytes} bytes：{candidate}")
        total = 0
        while True:
            chunk = os.read(descriptor, min(1024 * 1024, max_bytes - total + 1))
            if not chunk:
                return digest.hexdigest()
            total += len(chunk)
            if total > max_bytes:
                raise ValueError(f"电子书文件超过上限 {max_bytes} bytes：{candidate}")
            digest.update(chunk)
    finally:
        os.close(descriptor)


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

    schema = read_json(SCHEMA_PATH)
    if not isinstance(schema, dict) or not isinstance(schema.get("$defs"), dict):
        raise ValueError("文献 schema 顶层或 $defs 无效")
    Draft202012Validator.check_schema(schema)
    records = {kind: load_jsonl(path) for kind, path in FILES.items()}
    all_ids: dict[str, str] = {}
    id_fields = {"work": "work_id", "edition": "edition_id", "file": "file_id", "relation": "relation_id"}
    for kind, items in records.items():
        validator = Draft202012Validator({"$ref": f"#/$defs/{kind}", "$defs": schema["$defs"]})
        for position, record in enumerate(items, 1):
            for error in sorted(validator.iter_errors(record), key=lambda item: list(item.path)):
                errors.append(f"{kind} 第 {position} 条 schema 错误：{error.message}")
            record_id = record.get(id_fields[kind])
            if isinstance(record_id, str) and record_id in all_ids:
                errors.append(f"重复 ID：{record_id}")
            elif isinstance(record_id, str):
                all_ids[record_id] = kind

    work_ids = {record["work_id"] for record in records["work"]}
    edition_ids = {record["edition_id"] for record in records["edition"]}
    file_ids = {record["file_id"] for record in records["file"]}
    for edition in records["edition"]:
        if edition["work_id"] not in work_ids:
            errors.append(f"Edition 引用不存在的 Work：{edition['work_id']}")
        if not isbn13_valid(edition["isbn13"]):
            errors.append(f"ISBN-13 校验位错误：{edition['isbn13']}")
    for file_record in records["file"]:
        if file_record["edition_id"] not in edition_ids:
            errors.append(f"File 引用不存在的 Edition：{file_record['edition_id']}")
        relative_file = file_record.get("path")
        if (
            not isinstance(relative_file, str)
            or len(relative_file) > MAX_PATH_CHARS
            or "\x00" in relative_file
            or "\\" in relative_file
            or Path(relative_file).is_absolute()
            or ".." in Path(relative_file).parts
        ):
            errors.append(f"电子书路径越出 literature/files：{relative_file}")
            continue
        path = _safe_path(ROOT / relative_file)
        try:
            path.relative_to(_safe_path(LITERATURE / "files"))
        except ValueError:
            errors.append(f"电子书路径越出 literature/files：{relative_file}")
            continue
        try:
            actual_size = regular_file_size(path)
        except (OSError, ValueError) as exc:
            errors.append(f"电子书文件不可安全读取：{relative_file} ({exc})")
            continue
        if actual_size != file_record["size_bytes"]:
            errors.append(f"电子书大小漂移：{relative_file}")
        if sha256_file(path) != file_record["sha256"]:
            errors.append(f"电子书 SHA-256 漂移：{relative_file}")
    entity_ids = work_ids | edition_ids | file_ids
    expected_relations = {
        (edition["work_id"], "has_edition", edition["edition_id"])
        for edition in records["edition"]
    } | {
        (file_record["edition_id"], "has_file", file_record["file_id"])
        for file_record in records["file"]
    }
    actual_relations = {
        (relation["subject_id"], relation["predicate"], relation["object_id"])
        for relation in records["relation"]
    }
    for relation in records["relation"]:
        if relation["subject_id"] not in entity_ids:
            errors.append(f"Relation subject 不存在：{relation['subject_id']}")
        if relation["object_id"] not in entity_ids and relation["predicate"] in {"has_edition", "has_file"}:
            errors.append(f"Relation object 不存在：{relation['object_id']}")
    for relation in sorted(expected_relations - actual_relations):
        errors.append(f"缺少结构关系：{relation}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"文献库校验失败：{len(errors)} 个问题。", file=sys.stderr)
        return 1
    print(
        "文献库校验通过："
        f"Work {len(records['work'])}；Edition {len(records['edition'])}；"
        f"File {len(records['file'])}；Relation {len(records['relation'])}。"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError, AttributeError, SchemaError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
