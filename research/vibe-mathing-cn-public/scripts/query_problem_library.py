#!/usr/bin/env python3
"""Query admitted source observations and isolated candidate observations.

The default collection is admitted. Neither collection is a canonical
ProblemContract and neither can directly create an Attempt.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / "problem-library"
RECORDS_PATH = LIBRARY / "records" / "problems.jsonl"
RAW = LIBRARY / "raw" / "candidates"
CANDIDATE_ROOT = LIBRARY / "derived" / "candidate-observations"
CANDIDATE_LATEST = CANDIDATE_ROOT / "latest.json"
MAX_FILE_BYTES = 128_000_000
MAX_RECORDS = 100_000
MAX_LIMIT = 1000
MAX_LINE_BYTES = 30_000_000
MAX_PATH_CHARS = 4_096
MAX_QUERY_CHARS = 4_096


def _reject_json_constant(value: str) -> object:
    raise ValueError(f"invalid JSON constant: {value}")


def _safe_repo_path(path: Path) -> Path:
    path = Path(path)
    if (
        len(str(path)) > MAX_PATH_CHARS
        or any(part == ".." for part in path.parts)
        or "\x00" in str(path)
        or "\\" in str(path)
    ):
        raise ValueError(f"path contains an invalid component: {path}")
    root = ROOT.resolve()
    candidate = path if path.is_absolute() else root / path
    try:
        relative = candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"path escapes project root: {candidate}") from exc
    if ".." in relative.parts:
        raise ValueError(f"path escapes project root: {candidate}")
    lexical = root
    for part in relative.parts:
        lexical = lexical / part
        if lexical.is_symlink():
            raise ValueError(f"path contains symlink: {candidate}")
    return candidate


def _read_bytes(path: Path, *, max_bytes: int = MAX_FILE_BYTES) -> bytes:
    if (
        not isinstance(max_bytes, int)
        or isinstance(max_bytes, bool)
        or max_bytes <= 0
        or max_bytes > MAX_FILE_BYTES
    ):
        raise ValueError("problem library read budget is invalid")
    path = _safe_repo_path(path)
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise ValueError("platform cannot safely read problem library files")
    try:
        descriptor = os.open(path, os.O_RDONLY | nofollow)
    except OSError as exc:
        raise ValueError(f"cannot read problem library file: {path}") from exc
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode):
            raise ValueError(f"problem library path is not regular: {path}")
        if file_stat.st_size > max_bytes:
            raise ValueError(f"problem library file exceeds size budget: {path}")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(64 * 1024, max_bytes - total + 1))
            if not chunk:
                return b"".join(chunks)
            total += len(chunk)
            if total > max_bytes:
                raise ValueError(f"problem library file exceeds size budget: {path}")
            chunks.append(chunk)
    finally:
        os.close(descriptor)


def read_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    raw = _read_bytes(path)
    records = 0
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"invalid UTF-8 JSONL in {path}") from exc
    for number, line in enumerate(text.splitlines(), 1):
        if len(line.encode("utf-8")) > MAX_LINE_BYTES:
            raise ValueError(f"JSONL row exceeds size budget in {path}:{number}")
        if line.strip():
            records += 1
            if records > MAX_RECORDS:
                raise ValueError(f"too many JSONL rows in {path}")
            value = json.loads(line, parse_constant=_reject_json_constant)
            if not isinstance(value, dict):
                raise ValueError(f"non-object JSONL row in {path}:{number}")
            yield value


def sha256_file(path: Path) -> str:
    path = _safe_repo_path(path)
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise ValueError("platform cannot safely hash problem library files")
    try:
        descriptor = os.open(path, os.O_RDONLY | nofollow)
    except OSError as exc:
        raise ValueError(f"cannot hash problem library file: {path}") from exc
    digest = hashlib.sha256()
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode):
            raise ValueError(f"problem library path is not regular: {path}")
        if file_stat.st_size > MAX_FILE_BYTES:
            raise ValueError(f"problem library file exceeds size budget: {path}")
        total = 0
        while True:
            block = os.read(descriptor, 1024 * 1024)
            if not block:
                break
            total += len(block)
            if total > MAX_FILE_BYTES:
                raise ValueError(f"problem library file exceeds size budget: {path}")
            digest.update(block)
    finally:
        os.close(descriptor)
    return digest.hexdigest()


def safe_candidate_path(value: object, *, label: str) -> Path:
    if (
        not isinstance(value, str)
        or not value
        or len(value) > MAX_PATH_CHARS
        or "\x00" in value
        or "\\" in value
    ):
        raise ValueError(f"candidate latest {label} must be a bounded string")
    relative = Path(value)
    prefix = "problem-library/derived/candidate-observations/"
    if relative.is_absolute() or ".." in relative.parts or not value.startswith(prefix):
        raise ValueError(f"unsafe candidate {label} path: {value}")
    if CANDIDATE_ROOT.is_symlink() or CANDIDATE_ROOT.resolve() != CANDIDATE_ROOT:
        raise ValueError(f"candidate snapshot root is a symlink: {value}")
    lexical = ROOT
    for part in relative.parts:
        lexical = lexical / part
        if lexical.is_symlink():
            raise ValueError(f"unsafe candidate {label} symlink: {value}")
    path = (ROOT / relative).resolve()
    allowed = CANDIDATE_ROOT.resolve()
    if path == allowed or allowed not in path.parents or not path.is_file():
        raise ValueError(f"candidate {label} path escapes snapshot root: {value}")
    return path


def candidate_path() -> Path:
    latest = json.loads(
        _read_bytes(CANDIDATE_LATEST, max_bytes=5_000_000).decode("utf-8"),
        parse_constant=_reject_json_constant,
    )
    if not isinstance(latest, dict) or latest.get("schema_version") != "candidate-latest.v1":
        raise ValueError("candidate latest pointer schema_version is invalid")
    path = safe_candidate_path(latest.get("observations_path"), label="observations")
    snapshot_path = safe_candidate_path(latest.get("snapshot_path"), label="snapshot")
    snapshot = json.loads(
        _read_bytes(snapshot_path, max_bytes=5_000_000).decode("utf-8"),
        parse_constant=_reject_json_constant,
    )
    if not isinstance(snapshot, dict) or latest.get("snapshot_id") != snapshot.get("snapshot_id"):
        raise ValueError("candidate latest pointer does not match snapshot")
    if snapshot.get("decision") != "PASS":
        raise ValueError(f"candidate snapshot is not PASS: {snapshot.get('decision')}")
    expected_inputs = {
        "inventory_sha256": sha256_file(RAW / "inventory.json"),
        "parser_sha256": sha256_file(ROOT / "scripts/consolidate_candidates.py"),
        "candidate_schema_sha256": sha256_file(ROOT / "problem-library/schema/candidate-observation.schema.json"),
        "source_registry_sha256": sha256_file(ROOT / "problem-library/registry/candidate-sources.json"),
    }
    if snapshot.get("inputs") != expected_inputs or latest.get("inputs") != expected_inputs:
        raise ValueError("candidate snapshot input digests are stale")
    output = snapshot.get("output", {})
    if (
        not isinstance(output, dict)
        or not isinstance(output.get("path"), str)
        or not isinstance(output.get("sha256"), str)
        or not isinstance(output.get("bytes"), int)
        or isinstance(output.get("bytes"), bool)
        or output.get("bytes") < 0
    ):
        raise ValueError("candidate snapshot output metadata is invalid")
    if output.get("path") != str(path.relative_to(ROOT)):
        raise ValueError("candidate snapshot output path is not latest-bound")
    if output.get("sha256") != sha256_file(path) or output.get("bytes") != len(_read_bytes(path)):
        raise ValueError("candidate snapshot output digest is stale")
    return path


def _validate_candidate_record(record: dict[str, Any]) -> None:
    if (
        not isinstance(record, dict)
        or not isinstance(record.get("observation_id"), str)
        or not isinstance(record.get("source"), str)
        or record.get("admission") != {
            "state": "candidate",
            "research_eligible": False,
        }
    ):
        raise ValueError("candidate observation is not a safe research-ineligible object")


def admitted_view(record: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(record, dict) or not isinstance(record.get("id"), str):
        raise ValueError("admitted problem record is invalid")
    value = dict(record)
    value.update(
        {
            "_collection": "admitted",
            "_record_id": record["id"],
            "_status_raw": record["status"],
            "_status_class": "unknown",
            "_research_eligible": False,
        }
    )
    return value


def candidate_view(record: dict[str, Any]) -> dict[str, Any]:
    _validate_candidate_record(record)
    value = dict(record)
    value.update(
        {
            "_collection": "candidate",
            "_record_id": record["observation_id"],
            "_status_raw": record["source_status_raw"],
            "_status_class": record["source_status_class"],
            "_research_eligible": False,
        }
    )
    return value


def records(collection: str) -> Iterable[dict[str, Any]]:
    if collection in {"admitted", "all"}:
        yield from (admitted_view(record) for record in read_jsonl(RECORDS_PATH))
    if collection in {"candidates", "all"}:
        yield from (candidate_view(record) for record in read_jsonl(candidate_path()))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="查询本地数学问题来源观察；默认不包含 candidates。")
    parser.add_argument("--collection", choices=("admitted", "candidates", "all"), default="admitted")
    parser.add_argument("--source", help="来源 ID；不硬编码枚举，以来源 registry 为准。")
    parser.add_argument("--status", help="来源原始状态，大小写不敏感。")
    parser.add_argument(
        "--status-class",
        choices=("open_claimed", "closed_claimed", "under_review", "unknown"),
        help="仅 candidate snapshot 提供规范化来源声称；不是数学 Result。",
    )
    parser.add_argument("--category", help="分类名，不区分大小写，支持子串。")
    parser.add_argument("--text", help="在标题与题面摘要中检索，不区分大小写。")
    parser.add_argument("--list-sources", action="store_true")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--json", action="store_true", help="输出带 collection 标记的 JSONL。")
    args = parser.parse_args()
    for name in ("source", "status", "category", "text"):
        value = getattr(args, name)
        if value is not None and len(value) > MAX_QUERY_CHARS:
            parser.error(f"{name} 查询条件超过大小上限")
    if args.limit < 1 or args.limit > MAX_LIMIT:
        parser.error(f"limit 必须在 [1, {MAX_LIMIT}] 内。")
    return args


def field(record: dict[str, Any], admitted_name: str, candidate_name: str) -> Any:
    return record.get(admitted_name) if record["_collection"] == "admitted" else record.get(candidate_name)


def matches(record: dict[str, Any], args: argparse.Namespace) -> bool:
    if args.source and record.get("source") != args.source:
        return False
    if args.status and str(record.get("_status_raw") or "").casefold() != args.status.casefold():
        return False
    if args.status_class and record.get("_status_class") != args.status_class:
        return False
    categories = field(record, "categories", "categories") or []
    if args.category:
        needle = args.category.casefold()
        if not any(needle in str(category).casefold() for category in categories):
            return False
    if args.text:
        title = str(record.get("title") or "")
        statement = str(field(record, "statement_excerpt", "statement_excerpt") or "")
        if args.text.casefold() not in f"{title}\n{statement}".casefold():
            return False
    return True


def main() -> int:
    args = parse_args()
    if not RECORDS_PATH.is_file() and args.collection in {"admitted", "all"}:
        print("ERROR: admitted problem source records have not been generated.", file=sys.stderr)
        return 1
    if not CANDIDATE_LATEST.is_file() and args.collection in {"candidates", "all"}:
        print("ERROR: candidate snapshot missing; run scripts/build_candidate_observations.py.", file=sys.stderr)
        return 1
    try:
        stream = list(records(args.collection)) if args.list_sources else records(args.collection)
        if args.list_sources:
            for source in sorted({record["source"] for record in stream}):
                print(source)
            return 0
        emitted = 0
        for record in stream:
            if not matches(record, args):
                continue
            if args.json:
                print(
                    json.dumps(
                        record, ensure_ascii=False, sort_keys=True, allow_nan=False
                    )
                )
            else:
                categories = " / ".join(str(item) for item in (record.get("categories") or [])) or "Unclassified"
                url = field(record, "detail_url", "source_url")
                status = record.get("_status_raw") or "unknown"
                print(
                    f"{record['_collection']}\t{record['_record_id']}\t[{status}]\t"
                    f"{categories}\t{record['title']}\t{url}"
                )
            emitted += 1
            if emitted >= args.limit:
                break
    except (OSError, UnicodeDecodeError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
