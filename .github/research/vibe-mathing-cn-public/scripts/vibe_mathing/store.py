"""Problem、Attempt、Result 与 Solution View 的单机事务存储。"""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

from jsonschema import Draft202012Validator, FormatChecker, SchemaError

try:
    import fcntl
except ImportError:  # pragma: no cover - unsupported platforms fail closed on use.
    fcntl = None  # type: ignore[assignment]


COLLECTIONS = {
    "problems": (
        "problem-library/records/canonical-problems.jsonl",
        "problem-library/schema/canonical-problem.schema.json",
        "problem_id",
    ),
    "attempts": (
        "research/records/attempts.jsonl",
        "research/schema/attempt.schema.json",
        "attempt_id",
    ),
    "results": (
        "result-library/records/results.jsonl",
        "result-library/schema/result.schema.json",
        "result_id",
    ),
}
MAX_COLLECTION_BYTES = 30_000_000
MAX_RECORDS = 100_000
MAX_SOLUTION_INDEX_BYTES = 5_000_000
MAX_RECORD_BYTES = 1_000_000
MAX_TRANSACTION_BYTES = MAX_COLLECTION_BYTES * len(COLLECTIONS)


MAX_PATH_CHARS = 4_096
MAX_LINE_BYTES = 30_000_000


class StoreError(RuntimeError):
    """事务、schema 或幂等契约失败。"""


def _reject_json_constant(value: str) -> Any:
    raise StoreError(f"JSON 含非法常量：{value}")


def _parse_timestamp(value: Any) -> datetime:
    if not isinstance(value, str):
        raise StoreError("时间戳必须是 ISO 8601 字符串")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise StoreError("时间戳必须是有效 ISO 8601 日期时间") from exc
    if parsed.tzinfo is None:
        raise StoreError("时间戳必须包含时区")
    return parsed.astimezone(timezone.utc)


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _fsync_directory(path: Path) -> None:
    nofollow = getattr(os, "O_NOFOLLOW", None)
    directory = getattr(os, "O_DIRECTORY", None)
    if nofollow is None or directory is None:
        raise StoreError("当前平台无法安全持久化存储目录")
    descriptor = os.open(path, os.O_RDONLY | nofollow | directory)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


class ResearchStore:
    def _safe_path(self, path: Path) -> Path:
        path = Path(path)
        if (
            len(str(path)) > MAX_PATH_CHARS
            or "\x00" in str(path)
            or "\\" in str(path)
            or any(part in {".", ".."} for part in path.parts)
        ):
            raise StoreError(f"存储路径包含非法组件：{path}")
        try:
            relative = path.relative_to(self.root)
        except ValueError as exc:
            raise StoreError(f"存储路径越界：{path}") from exc
        lexical = self.root
        for part in relative.parts:
            lexical = lexical / part
            if lexical.is_symlink():
                raise StoreError(f"存储路径不能包含 symlink：{path}")
        if not path.is_absolute() or path.resolve() != path:
            raise StoreError(f"存储路径不是规范绝对路径：{path}")
        return path

    def _read_bytes(self, path: Path, *, max_bytes: int = MAX_COLLECTION_BYTES) -> bytes:
        self._safe_path(path)
        if (
            not isinstance(max_bytes, int)
            or isinstance(max_bytes, bool)
            or max_bytes <= 0
            or max_bytes > MAX_COLLECTION_BYTES
        ):
            raise StoreError("存储读取预算无效")
        nofollow = getattr(os, "O_NOFOLLOW", None)
        if nofollow is None:
            raise StoreError("当前平台无法安全打开存储文件")
        try:
            descriptor = os.open(path, os.O_RDONLY | nofollow)
        except OSError as exc:
            raise StoreError(f"无法读取存储文件：{path}") from exc
        try:
            file_stat = os.fstat(descriptor)
            if not stat.S_ISREG(file_stat.st_mode):
                raise StoreError(f"存储路径不是普通文件：{path}")
            if file_stat.st_size > max_bytes:
                raise StoreError(f"存储文件超过大小预算：{path}")
            chunks: list[bytes] = []
            total = 0
            while True:
                chunk = os.read(descriptor, min(64 * 1024, max_bytes - total + 1))
                if not chunk:
                    return b"".join(chunks)
                total += len(chunk)
                if total > max_bytes:
                    raise StoreError(f"存储文件超过大小预算：{path}")
                chunks.append(chunk)
        finally:
            os.close(descriptor)

    def __init__(self, project_root: Path) -> None:
        project_root = Path(project_root)
        self.root = project_root.resolve()
        if project_root.is_symlink() or project_root.absolute() != self.root:
            raise StoreError("研究仓库根目录不能通过 symlink 访问")
        if not self.root.is_dir():
            raise StoreError(f"研究仓库根目录不存在：{self.root}")
        if fcntl is None:
            raise StoreError("当前平台不支持 fail-closed 文件锁")
        self.lock_path = self.root / "research" / ".store.lock"
        self.journal_path = self.root / "research" / ".store-transaction.json"
        self._safe_path(self.lock_path)
        self._safe_path(self.journal_path)

    @contextmanager
    def _locked(self) -> Iterator[None]:
        self._safe_path(self.lock_path.parent)
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        self._safe_path(self.lock_path.parent)
        nofollow = getattr(os, "O_NOFOLLOW", None)
        if nofollow is None:
            raise StoreError("当前平台无法安全打开存储锁")
        try:
            descriptor = os.open(
                self.lock_path,
                os.O_RDWR | os.O_CREAT | nofollow,
                0o600,
            )
        except OSError as exc:
            raise StoreError(f"无法打开研究仓库锁：{self.lock_path}") from exc
        try:
            with os.fdopen(descriptor, "a+b") as handle:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
                self._recover_locked()
                yield
        finally:
            # fdopen owns the descriptor after successful open; this is only
            # reached as a safety net if wrapping it failed.
            if descriptor >= 0:
                try:
                    os.close(descriptor)
                except OSError:
                    pass

    def locked(self) -> Iterator[None]:
        """为跨 collection 的外部只读校验提供一致快照锁。"""
        return self._locked()

    def _paths(self, collection: str) -> tuple[Path, Path, str]:
        if not isinstance(collection, str):
            raise StoreError("collection 名称必须是字符串")
        try:
            record_path, schema_path, id_field = COLLECTIONS[collection]
        except KeyError as exc:
            raise StoreError(f"未知 collection：{collection}") from exc
        record = self.root / record_path
        schema = self.root / schema_path
        self._safe_path(record)
        self._safe_path(schema)
        return record, schema, id_field

    def read(self, collection: str) -> list[dict[str, Any]]:
        """在恢复任何未完成事务后读取一致快照。"""
        with self._locked():
            return self._read_unlocked(collection)

    def snapshot(self) -> dict[str, list[dict[str, Any]]]:
        """在同一锁内校验并返回三张真相表的一致快照。"""
        with self._locked():
            snapshot = {
                collection: self._read_unlocked(collection)
                for collection in COLLECTIONS
            }
            for collection, records in snapshot.items():
                self._validate(collection, records)
            self._validate_integrity_locked(snapshot)
            return snapshot

    def _read_unlocked(self, collection: str) -> list[dict[str, Any]]:
        path, _, _ = self._paths(collection)
        if path.is_symlink() or not path.exists():
            if path.is_symlink():
                raise StoreError(f"存储记录不能是 symlink：{path}")
            return []
        raw = self._read_bytes(path)
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise StoreError(f"{path}: UTF-8 无效") from exc
        records: list[dict[str, Any]] = []
        for number, line in enumerate(text.splitlines(), 1):
            if len(line.encode("utf-8")) > MAX_LINE_BYTES:
                raise StoreError(f"{path}:{number}: JSONL 行超过大小预算")
            if not line.strip():
                continue
            if len(records) >= MAX_RECORDS:
                raise StoreError(f"{path}: 记录数超过预算")
            try:
                value = json.loads(line, parse_constant=_reject_json_constant)
            except json.JSONDecodeError as exc:
                raise StoreError(f"{path}:{number}: JSONL 无效") from exc
            if not isinstance(value, dict):
                raise StoreError(f"{path}:{number}: 记录不是对象")
            records.append(value)
        return records

    def _validate(self, collection: str, records: list[dict[str, Any]]) -> None:
        _, schema_path, id_field = self._paths(collection)
        try:
            schema = json.loads(
                self._read_bytes(schema_path, max_bytes=5_000_000).decode("utf-8"),
                parse_constant=_reject_json_constant,
            )
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, StoreError) as exc:
            raise StoreError(f"无法读取 schema：{schema_path}") from exc
        if not isinstance(schema, dict):
            raise StoreError(f"schema 顶层必须是 object：{schema_path}")
        try:
            validator = Draft202012Validator(schema, format_checker=FormatChecker())
        except (SchemaError, TypeError, ValueError) as exc:
            raise StoreError(f"schema 无效：{schema_path}") from exc
        seen: set[str] = set()
        if len(records) > MAX_RECORDS:
            raise StoreError(f"{collection}: 记录数超过预算")
        for index, record in enumerate(records, 1):
            try:
                encoded_record = json.dumps(record, ensure_ascii=False, allow_nan=False).encode("utf-8")
            except (TypeError, ValueError, UnicodeEncodeError) as exc:
                raise StoreError(f"{collection}:{index}: 记录不是可移植 JSON") from exc
            if len(encoded_record) > MAX_RECORD_BYTES:
                raise StoreError(f"{collection}:{index}: 记录超过大小预算")
            errors = sorted(validator.iter_errors(record), key=lambda item: list(item.path))
            if errors:
                raise StoreError(f"{collection}:{index}: {errors[0].message}")
            record_id = record.get(id_field)
            if not isinstance(record_id, str):
                raise StoreError(f"{collection}:{index}: ID 必须是字符串")
            if record_id in seen:
                raise StoreError(f"{collection}: 重复 ID：{record_id}")
            seen.add(record_id)

    def upsert(
        self,
        collection: str,
        record: dict[str, Any],
        *,
        fail_after_replace: int | None = None,
    ) -> bool:
        """按稳定 ID 幂等写入；相同 ID 不同内容拒绝覆盖。"""
        if not isinstance(record, dict):
            raise StoreError("存储记录必须是 object")
        with self._locked():
            records = self._read_unlocked(collection)
            _, _, id_field = self._paths(collection)
            record_id = record.get(id_field)
            for current in records:
                if current.get(id_field) == record_id:
                    if current == record:
                        return False
                    raise StoreError(f"{collection}: ID 已存在且内容不同：{record_id}")
            records.append(record)
            self.commit({collection: records}, fail_after_replace=fail_after_replace, locked=True)
            return True

    def replace_problem(self, record: dict[str, Any]) -> None:
        """只允许 ProblemContract lifecycle 单向转换，其他契约字段保持冻结。"""
        transitions = {
            "draft": {"active", "withdrawn"},
            "active": {"withdrawn"},
            "withdrawn": set(),
        }
        with self._locked():
            records = self._read_unlocked("problems")
            self._validate("problems", records)
            self._validate("problems", [record])
            for index, current in enumerate(records):
                if current.get("problem_id") != record.get("problem_id"):
                    continue
                old = current.get("lifecycle")
                new = record.get("lifecycle")
                frozen = {
                    key: value
                    for key, value in current.items()
                    if key not in {"lifecycle", "updated_at"}
                }
                proposed = {
                    key: value
                    for key, value in record.items()
                    if key not in {"lifecycle", "updated_at"}
                }
                if frozen != proposed or new not in transitions.get(old, set()):
                    raise StoreError(
                        f"ProblemContract 只允许 lifecycle 单向转换：{old} -> {new}"
                    )
                if _parse_timestamp(record.get("updated_at")) <= _parse_timestamp(
                    current.get("updated_at")
                ):
                    raise StoreError("ProblemContract lifecycle 转换必须推进 updated_at")
                records[index] = record
                break
            else:
                raise StoreError(f"Problem 不存在：{record.get('problem_id')}")
            self.commit({"problems": records}, locked=True)

    def replace_result(
        self, record: dict[str, Any], *, fail_after_replace: int | None = None
    ) -> None:
        """只允许 Result 追加 evidence 的版本化替换，不允许改写既有字段。"""
        with self._locked():
            records = self._read_unlocked("results")
            self._validate("results", records)
            self._validate("results", [record])
            for index, current in enumerate(records):
                if current.get("result_id") != record.get("result_id"):
                    continue
                frozen = {
                    key: value
                    for key, value in current.items()
                    if key not in {"evidence", "outcome"}
                }
                proposed = {
                    key: value
                    for key, value in record.items()
                    if key not in {"evidence", "outcome"}
                }
                outcome_change = (current.get("outcome"), record.get("outcome"))
                allowed_outcome_change = outcome_change[0] == outcome_change[1] or (
                    outcome_change[0] in {"established", "refuted", "supported"}
                    and outcome_change[1] == "withdrawn"
                )
                if (
                    frozen != proposed
                    or not allowed_outcome_change
                    or record.get("evidence", [])[: len(current.get("evidence", []))]
                    != current.get("evidence", [])
                ):
                    raise StoreError("Result 只能在 evidence 账本尾部追加记录")
                records[index] = record
                break
            else:
                raise StoreError(f"Result 不存在：{record.get('result_id')}")
            self.commit({"results": records}, fail_after_replace=fail_after_replace, locked=True)

    def replace_attempt(self, record: dict[str, Any]) -> None:
        """按允许的 lifecycle 单调转换更新 Attempt。"""
        transitions = {
            "planned": {"running", "blocked", "failed"},
            "running": {"completed", "blocked", "failed"},
            "blocked": {"running", "failed"},
            "completed": set(),
            "failed": set(),
        }
        with self._locked():
            records = self._read_unlocked("attempts")
            self._validate("attempts", records)
            self._validate("attempts", [record])
            for index, current in enumerate(records):
                if current.get("attempt_id") != record.get("attempt_id"):
                    continue
                old = current.get("lifecycle")
                new = record.get("lifecycle")
                if new != old and new not in transitions.get(old, set()):
                    raise StoreError(f"Attempt 非法状态转换：{old} -> {new}")
                records[index] = record
                break
            else:
                raise StoreError(f"Attempt 不存在：{record.get('attempt_id')}")
            self.commit({"attempts": records}, locked=True)

    def commit(
        self,
        changes: dict[str, list[dict[str, Any]]],
        *,
        fail_after_replace: int | None = None,
        locked: bool = False,
    ) -> None:
        if (
            not isinstance(changes, dict)
            or any(collection not in COLLECTIONS for collection in changes)
            or any(
                not isinstance(records, list)
                or len(records) > MAX_RECORDS
                or any(not isinstance(record, dict) for record in records)
                for records in changes.values()
            )
            or (
                fail_after_replace is not None
                and (
                    not isinstance(fail_after_replace, int)
                    or isinstance(fail_after_replace, bool)
                    or fail_after_replace <= 0
                    or fail_after_replace > len(COLLECTIONS)
                )
            )
        ):
            raise StoreError("事务 changes 或故障注入参数无效")
        if not locked:
            with self._locked():
                return self.commit(changes, fail_after_replace=fail_after_replace, locked=True)
        # Validate both the requested collections and every untouched collection
        # before applying cross-collection admission checks.
        for collection in COLLECTIONS:
            current_records = self._read_unlocked(collection)
            self._validate(collection, changes.get(collection, current_records))
        if "attempts" in changes:
            current_attempt_ids = {
                item["attempt_id"] for item in self._read_unlocked("attempts")
            }
            final_problems = changes.get("problems", self._read_unlocked("problems"))
            problems_by_id = {item["problem_id"]: item for item in final_problems}
            final_attempts = changes["attempts"]
            for attempt in final_attempts:
                if attempt.get("attempt_id") in current_attempt_ids:
                    continue
                problem = problems_by_id.get(attempt.get("problem_id"))
                if problem is None:
                    continue
                if problem.get("lifecycle") != "active":
                    raise StoreError("只有 active ProblemContract 允许创建新 Attempt")
                constraints = problem.get("constraints", {})
                if attempt.get("method") not in constraints.get("allowed_methods", []):
                    raise StoreError(
                        f"Attempt method={attempt.get('method')} 未被 ProblemContract 允许"
                    )
                problem_attempts = [
                    item
                    for item in final_attempts
                    if item.get("problem_id") == problem["problem_id"]
                ]
                if len(problem_attempts) > constraints.get("max_attempts", 0):
                    raise StoreError("ProblemContract 的 max_attempts 预算耗尽")
        self._validate_integrity_locked(changes)
        prepared: list[dict[str, str]] = []
        try:
            serialized_changes = json.dumps(
                changes, ensure_ascii=False, sort_keys=True, allow_nan=False
            ).encode()
        except (TypeError, ValueError) as exc:
            raise StoreError("事务数据不是可移植 JSON") from exc
        if len(serialized_changes) > MAX_TRANSACTION_BYTES:
            raise StoreError("事务数据超过大小预算")
        transaction_id = hashlib.sha256(serialized_changes).hexdigest()[:16]
        for collection, records in changes.items():
            target, _, id_field = self._paths(collection)
            target.parent.mkdir(parents=True, exist_ok=True)
            self._safe_path(target.parent)
            ordered = sorted(records, key=lambda item: item[id_field])
            try:
                data = b"".join(
                    (
                        json.dumps(
                            item, ensure_ascii=False, sort_keys=True, allow_nan=False
                        )
                        + "\n"
                    ).encode()
                    for item in ordered
                )
            except (TypeError, ValueError, UnicodeEncodeError) as exc:
                raise StoreError(f"{collection}: 记录不是可移植 JSON") from exc
            if len(data) > MAX_COLLECTION_BYTES:
                raise StoreError(f"{collection}: 写入数据超过大小预算")
            temporary = target.with_name(f".{target.name}.{transaction_id}.tmp")
            nofollow = getattr(os, "O_NOFOLLOW", None)
            if nofollow is None:
                raise StoreError("当前平台无法安全创建存储暂存文件")
            descriptor = os.open(
                temporary,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL | nofollow,
                0o600,
            )
            try:
                with os.fdopen(descriptor, "wb") as handle:
                    handle.write(data)
                    handle.flush()
                    os.fsync(handle.fileno())
            except BaseException:
                temporary.unlink(missing_ok=True)
                raise
            prepared.append(
                {
                    "target": str(target.relative_to(self.root)),
                    "temporary": str(temporary.relative_to(self.root)),
                    "sha256": _digest(data),
                }
            )
        journal = {
            "schema_version": "1.0.0",
            "transaction_id": transaction_id,
            "prepared": prepared,
        }
        journal_data = (
            json.dumps(journal, sort_keys=True, indent=2, allow_nan=False) + "\n"
        ).encode()
        journal_temporary = self.journal_path.with_suffix(".json.tmp")
        self._safe_path(journal_temporary)
        nofollow = getattr(os, "O_NOFOLLOW", None)
        if nofollow is None:
            raise StoreError("当前平台无法安全创建事务日志")
        journal_descriptor = os.open(
            journal_temporary,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | nofollow,
            0o600,
        )
        try:
            with os.fdopen(journal_descriptor, "wb") as handle:
                handle.write(journal_data)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(journal_temporary, self.journal_path)
        except BaseException:
            journal_temporary.unlink(missing_ok=True)
            raise
        _fsync_directory(self.journal_path.parent)
        for count, item in enumerate(prepared, 1):
            os.replace(self.root / item["temporary"], self.root / item["target"])
            _fsync_directory((self.root / item["target"]).parent)
            if fail_after_replace == count:
                raise StoreError("故障注入：事务提交中断")
        self.journal_path.unlink()
        _fsync_directory(self.journal_path.parent)

    def recover(self) -> None:
        with self._locked():
            return

    def _recover_locked(self) -> None:
        self._safe_path(self.journal_path)
        journal_temporary = self.journal_path.with_suffix(".json.tmp")
        self._safe_path(journal_temporary)
        if self.journal_path.is_symlink():
            raise StoreError("事务日志不能是 symlink")
        if not self.journal_path.is_file():
            journal_temporary.unlink(missing_ok=True)
            for record_path, _, _ in COLLECTIONS.values():
                target = self.root / record_path
                self._safe_path(target)
                for orphan in target.parent.glob(f".{target.name}.*.tmp"):
                    self._safe_path(orphan)
                    if orphan.is_symlink():
                        raise StoreError("发现 symlink 暂存文件")
                    orphan.unlink(missing_ok=True)
            return
        try:
            journal = json.loads(
                self._read_bytes(self.journal_path, max_bytes=5_000_000).decode("utf-8"),
                parse_constant=_reject_json_constant,
            )
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, StoreError) as exc:
            raise StoreError("事务日志损坏，拒绝继续写入") from exc
        if not isinstance(journal, dict):
            raise StoreError("事务日志顶层必须是 object")
        allowed_targets = {
            path for path, _, _ in COLLECTIONS.values()
        }
        prepared = journal.get("prepared")
        if (
            journal.get("schema_version") != "1.0.0"
            or not isinstance(journal.get("transaction_id"), str)
            or not re.fullmatch(r"[0-9a-f]{16}", journal["transaction_id"])
            or not isinstance(prepared, list)
        ):
            raise StoreError("事务日志契约无效，拒绝继续写入")
        if len(prepared) > len(COLLECTIONS):
            raise StoreError("事务日志 prepared 超出 collection 数量")
        seen_targets: set[str] = set()
        for item in prepared:
            if (
                not isinstance(item, dict)
                or not isinstance(item.get("target"), str)
                or item.get("target") not in allowed_targets
                or item.get("target") in seen_targets
                or not isinstance(item.get("temporary"), str)
                or not isinstance(item.get("sha256"), str)
                or not re.fullmatch(r"[0-9a-f]{64}", item.get("sha256", ""))
                or len(item.get("temporary", "")) > MAX_PATH_CHARS
                or "\x00" in item.get("temporary", "")
                or "\\" in item.get("temporary", "")
            ):
                raise StoreError("事务日志包含未授权 target")
            seen_targets.add(item["target"])
            target = self.root / item["target"]
            temporary = self.root / item["temporary"]
            self._safe_path(target)
            self._safe_path(temporary)
            if temporary.parent != target.parent or not temporary.name.startswith(
                f".{target.name}."
            ):
                raise StoreError("事务日志包含未授权暂存文件位置")
            if temporary.is_symlink():
                raise StoreError("事务暂存文件不能是 symlink")
            if temporary.exists() and not temporary.is_file():
                raise StoreError("事务暂存文件不是普通文件")
            if temporary.is_file():
                temporary_bytes = self._read_bytes(temporary)
                if _digest(temporary_bytes) != item["sha256"]:
                    raise StoreError(f"事务暂存文件完整性校验失败：{temporary}")
                os.replace(temporary, target)
                _fsync_directory(target.parent)
            try:
                target_bytes = self._read_bytes(target)
            except StoreError:
                raise StoreError(f"事务恢复无法证明目标完整：{target}")
            if _digest(target_bytes) != item.get("sha256"):
                raise StoreError(f"事务恢复无法证明目标完整：{target}")
        self.journal_path.unlink()
        _fsync_directory(self.journal_path.parent)

    def _validate_integrity_locked(
        self, changes: dict[str, list[dict[str, Any]]]
    ) -> None:
        from validate_research_spaces import validate_cross_references

        final = {
            collection: changes.get(collection, self._read_unlocked(collection))
            for collection in COLLECTIONS
        }
        problem_ids = {item["problem_id"] for item in final["problems"]}
        attempt_ids = {item["attempt_id"] for item in final["attempts"]}
        errors: list[str] = []
        validate_cross_references(
            final["problems"],
            problem_ids,
            final["attempts"],
            attempt_ids,
            final["results"],
            errors,
            project_root=self.root,
        )
        if errors:
            raise StoreError(f"跨记录完整性失败：{errors[0]}")

    def rebuild_solution_view(self) -> list[str]:
        from validate_research_spaces import derive_solution_ids

        with self._locked():
            snapshot = {
                collection: self._read_unlocked(collection)
                for collection in COLLECTIONS
            }
            for collection, records in snapshot.items():
                self._validate(collection, records)
            self._validate_integrity_locked(snapshot)
            attempts = {item["attempt_id"]: item for item in snapshot["attempts"]}
            solution_ids = derive_solution_ids(
                snapshot["results"], attempts, project_root=self.root
            )
            payload = {
                "schema_version": "2.0.0",
                "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
                "result_ids": solution_ids,
            }
            path = self.root / "result-library" / "indexes" / "solutions.json"
            self._safe_path(path)
            path.parent.mkdir(parents=True, exist_ok=True)
            self._safe_path(path.parent)
            try:
                data = (
                    json.dumps(
                        payload,
                        ensure_ascii=False,
                        indent=2,
                        allow_nan=False,
                    )
                    + "\n"
                ).encode("utf-8")
            except (TypeError, ValueError, UnicodeEncodeError) as exc:
                raise StoreError("solution index 不是可移植 JSON") from exc
            if len(data) > MAX_SOLUTION_INDEX_BYTES:
                raise StoreError("solution index 超过大小预算")
            temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
            nofollow = getattr(os, "O_NOFOLLOW", None)
            if nofollow is None:
                raise StoreError("当前平台无法安全创建 solution index")
            descriptor = os.open(
                temporary,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL | nofollow,
                0o600,
            )
            try:
                with os.fdopen(descriptor, "wb") as handle:
                    handle.write(data)
                    handle.flush()
                    os.fsync(handle.fileno())
                os.replace(temporary, path)
                _fsync_directory(path.parent)
            except BaseException:
                temporary.unlink(missing_ok=True)
                raise
        return solution_ids
