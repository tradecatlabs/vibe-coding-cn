"""可信证据产物、回执和 verifier registry 的唯一实现。"""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker, SchemaError


MAX_VERIFIER_JSON_BYTES = 2_000_000
MAX_TRUSTED_FILE_BYTES = 5_000_000
MAX_TIMEOUT_SECONDS = 86_400
MAX_MEMORY_BUDGET_MB = 131_072
MAX_THREADS = 1_024
MAX_OUTPUT_BYTES = 128_000_000
MAX_COMMAND_ITEMS = 4_096
MAX_COMMAND_BYTES = 8_000_000
MAX_PATH_CHARS = 4_096
MAX_FIELD_CHARS = 8_192
MAX_LIST_ITEMS = 10_000


class EvidenceError(ValueError):
    """证据无法在当前信任策略下成立。"""


def _reject_json_constant(value: str) -> Any:
    raise EvidenceError(f"JSON 含非法常量：{value}")


def _open_nofollow(path: Path, flags: int) -> int:
    path = Path(path)
    if (
        len(str(path)) > MAX_PATH_CHARS
        or "\x00" in str(path)
        or "\\" in str(path)
        or any(part in {".", ".."} for part in path.parts)
        or path.is_symlink()
        or path.resolve() != path
        or any(parent.is_symlink() for parent in path.parents)
    ):
        raise EvidenceError("证据路径包含非法组件")
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise EvidenceError("当前平台无法安全打开证据文件")
    try:
        return os.open(path, flags | nofollow)
    except OSError as exc:
        raise EvidenceError(f"无法安全打开证据文件：{path}") from exc


def _read_bounded(path: Path, *, max_bytes: int) -> bytes:
    if (
        not isinstance(max_bytes, int)
        or isinstance(max_bytes, bool)
        or max_bytes <= 0
        or max_bytes > MAX_TRUSTED_FILE_BYTES
    ):
        raise EvidenceError("证据读取大小上限无效")
    descriptor = _open_nofollow(path, os.O_RDONLY)
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode):
            raise EvidenceError("证据路径不是普通文件")
        if file_stat.st_size > max_bytes:
            raise EvidenceError("证据文件超过大小上限")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(64 * 1024, max_bytes - total + 1))
            if not chunk:
                return b"".join(chunks)
            total += len(chunk)
            if total > max_bytes:
                raise EvidenceError("证据文件超过大小上限")
            chunks.append(chunk)
    except OSError as exc:
        raise EvidenceError("无法读取证据文件") from exc
    finally:
        os.close(descriptor)


def sha256_file(path: Path, *, max_bytes: int | None = MAX_TRUSTED_FILE_BYTES) -> str:
    if max_bytes is None or (
        not isinstance(max_bytes, int)
        or isinstance(max_bytes, bool)
        or max_bytes <= 0
        or max_bytes > MAX_TRUSTED_FILE_BYTES
    ):
        raise EvidenceError("摘要大小上限必须在证据平台范围内")
    digest = hashlib.sha256()
    descriptor = _open_nofollow(path, os.O_RDONLY)
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode):
            raise EvidenceError("摘要路径不是普通文件")
        if file_stat.st_size > max_bytes:
            raise EvidenceError("证据文件超过大小上限")
        total = 0
        while True:
            chunk = os.read(descriptor, min(1024 * 1024, max_bytes - total + 1))
            if not chunk:
                break
            total += len(chunk)
            if total > max_bytes:
                raise EvidenceError("证据文件超过大小上限")
            digest.update(chunk)
    except OSError as exc:
        raise EvidenceError("无法读取证据文件") from exc
    finally:
        os.close(descriptor)
    return digest.hexdigest()


def _write_atomic(path: Path, data: bytes) -> None:
    path = Path(path)
    if (
        len(str(path)) > MAX_PATH_CHARS
        or "\x00" in str(path)
        or "\\" in str(path)
        or any(part in {".", ".."} for part in path.parts)
    ):
        raise EvidenceError("证据输出路径包含非法组件")
    if not isinstance(data, bytes) or len(data) > MAX_VERIFIER_JSON_BYTES:
        raise EvidenceError("证据输出超过大小上限")
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.parent.is_symlink() or path.is_symlink():
        raise EvidenceError("证据输出路径不能是 symlink")
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise EvidenceError("当前平台无法安全创建证据文件")
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
        directory = getattr(os, "O_DIRECTORY", None)
        if directory is None:
            raise EvidenceError("当前平台无法安全持久化证据目录")
        directory_descriptor = os.open(
            path.parent,
            os.O_RDONLY | directory | nofollow,
        )
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def _trusted_file(project_root: Path, locator: str) -> Path:
    if (
        not isinstance(locator, str)
        or not locator
        or len(locator) > MAX_PATH_CHARS
        or "\x00" in locator
        or "\\" in locator
        or Path(locator).is_absolute()
    ):
        raise EvidenceError("证据 locator 必须是非空仓库相对路径")
    relative = Path(locator)
    if any(part in {".", ".."} for part in relative.parts):
        raise EvidenceError("证据 locator 禁止路径逃逸")
    if relative.parts[:2] != ("research", "artifacts"):
        raise EvidenceError(f"证据文件不在可信根：{locator}")
    project_root_input = Path(project_root)
    resolved_project_root = project_root_input.resolve()
    if (
        not project_root_input.is_absolute()
        or project_root_input.absolute() != resolved_project_root
        or not resolved_project_root.is_dir()
    ):
        raise EvidenceError("项目根必须是规范绝对目录")
    trusted_root = resolved_project_root / "research" / "artifacts"
    if trusted_root.is_symlink():
        raise EvidenceError("可信证据根不能是 symlink")
    lexical = resolved_project_root
    for part in relative.parts:
        lexical = lexical / part
        if lexical.is_symlink():
            raise EvidenceError(f"可信证据路径禁止 symlink：{locator}")
    candidate = resolved_project_root / relative
    if candidate.is_symlink():
        raise EvidenceError(f"证据文件禁止 symlink：{locator}")
    try:
        candidate.relative_to(trusted_root)
    except ValueError as exc:
        raise EvidenceError(f"证据文件不在可信根：{locator}") from exc
    if not candidate.is_file():
        raise EvidenceError(f"证据 locator 不是普通文件：{locator}")
    try:
        if candidate.resolve(strict=True) != candidate:
            raise EvidenceError(f"证据文件禁止 symlink：{locator}")
    except FileNotFoundError as exc:
        raise EvidenceError(f"证据文件不存在：{locator}") from exc
    return candidate


def load_verifier_registry(project_root: Path) -> dict[str, dict[str, Any]]:
    project_root_input = Path(project_root)
    resolved_root = project_root_input.resolve()
    if (
        not project_root_input.is_absolute()
        or project_root_input.absolute() != resolved_root
        or not resolved_root.is_dir()
    ):
        raise EvidenceError("项目根必须是规范绝对目录")
    path = resolved_root / "research" / "verifiers.json"
    try:
        payload = json.loads(
            _read_bounded(path, max_bytes=MAX_TRUSTED_FILE_BYTES).decode("utf-8"),
            parse_constant=_reject_json_constant,
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, EvidenceError) as exc:
        raise EvidenceError(f"无法读取 verifier registry：{path}") from exc
    if not isinstance(payload, dict):
        raise EvidenceError("verifier registry 顶层必须是 object")
    _validate_schema(
        resolved_root / "research" / "schema" / "verifier-registry.schema.json",
        payload,
        "verifier registry",
    )
    entries: dict[str, dict[str, Any]] = {}
    principals = payload.get("principals", [])
    if not isinstance(principals, list) or len(principals) > MAX_LIST_ITEMS:
        raise EvidenceError("verifier registry principals 超过预算")
    for entry in principals:
        if not isinstance(entry, dict):
            raise EvidenceError("verifier registry principal 必须是 object")
        principal_id = entry.get("id")
        if (
            not isinstance(principal_id, str)
            or not principal_id
            or len(principal_id) > MAX_FIELD_CHARS
            or principal_id in entries
        ):
            raise EvidenceError("verifier registry 含无效或重复 principal ID")
        if entry.get("role") not in {"generator", "verifier"}:
            raise EvidenceError(f"{principal_id}: role 无效")
        if (
            not isinstance(entry.get("trust_domain"), str)
            or not entry["trust_domain"]
            or len(entry["trust_domain"]) > MAX_FIELD_CHARS
        ):
            raise EvidenceError(f"{principal_id}: 缺少 trust_domain")
        capabilities = entry.get("capabilities")
        if (
            not isinstance(capabilities, list)
            or len(capabilities) > MAX_LIST_ITEMS
            or not all(
                isinstance(item, str) and item and len(item) <= MAX_FIELD_CHARS
                for item in capabilities
            )
        ):
            raise EvidenceError(f"{principal_id}: capabilities 无效")
        if entry["role"] == "verifier" and (
            not isinstance(entry.get("policy"), str)
            or not entry["policy"]
            or len(entry["policy"]) > MAX_FIELD_CHARS
        ):
            raise EvidenceError(f"{principal_id}: verifier 缺少 policy")
        if entry["role"] == "generator" and entry.get("policy") is not None:
            raise EvidenceError(f"{principal_id}: generator 不应声明 verifier policy")
        entries[principal_id] = entry
    return entries


def _validate_schema(schema_path: Path, value: dict[str, Any], label: str) -> None:
    try:
        schema = json.loads(
            _read_bounded(schema_path, max_bytes=MAX_TRUSTED_FILE_BYTES).decode("utf-8"),
            parse_constant=_reject_json_constant,
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, EvidenceError) as exc:
        raise EvidenceError(f"无法读取 {label} schema：{schema_path}") from exc
    if not isinstance(schema, dict):
        raise EvidenceError(f"{label} schema 顶层必须是 object")
    if not isinstance(value, dict):
        raise EvidenceError(f"{label} 值必须是 object")
    try:
        errors = sorted(
            Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(value),
            key=lambda item: list(item.path),
        )
    except (SchemaError, TypeError, ValueError) as exc:
        raise EvidenceError(f"{label} schema 无效") from exc
    if errors:
        raise EvidenceError(f"{label} schema 无效：{errors[0].message}")


def _load_output_json(path: Path) -> dict[str, Any]:
    try:
        raw = _read_bounded(path, max_bytes=MAX_VERIFIER_JSON_BYTES)
        payload = json.loads(raw.decode("utf-8"), parse_constant=_reject_json_constant)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, EvidenceError) as exc:
        raise EvidenceError("verifier 输出必须是有效 JSON") from exc
    if not isinstance(payload, dict):
        raise EvidenceError("verifier 输出必须是 JSON object")
    return payload


def _validate_output_policy(
    *,
    policy: str,
    output_path: Path,
    verdict: str,
    capability: str,
    invalidates: list[str],
) -> None:
    if not isinstance(invalidates, list) or not all(
        isinstance(item, str) and item for item in invalidates
    ):
        raise EvidenceError("verifier invalidates 必须是字符串列表")
    output = _load_output_json(output_path)
    if verdict != "accept":
        if invalidates:
            if output.get("invalidates") != invalidates:
                raise EvidenceError("verifier 输出与回执 invalidates 不一致")
        elif output.get("verdict") != verdict:
            raise EvidenceError("非 accept 输出缺少对应 verdict")
        return
    valid = False
    if policy == "sympy-counterexample-fixture-v1":
        valid = output == {
            "x": "1/2",
            "x_squared": "1/4",
            "x_squared_lt_x": True,
        }
    elif policy == "sympy-statement-fixture-v1":
        valid = (
            output.get("expected") == "对所有实数 x，x^2 >= x。"
            and output.get("actual") == output.get("expected")
            and output.get("match") is True
        )
    elif policy == "sympy-smt-counterexample-fixture-v1":
        valid = (
            output.get("backend") == "sympy-1.14-sat-qf-lra"
            and output.get("sympy_version") == "1.14.0"
            and isinstance(output.get("propositional_sat"), dict)
            and bool(output["propositional_sat"])
            and output.get("propositional_unsat") is True
            and isinstance(output.get("qf_lra_sat"), dict)
            and bool(output["qf_lra_sat"])
            and output.get("qf_lra_contradiction_unsat") is True
            and output.get("witness") == "1/2"
            and output.get("exact_witness_ok") is True
            and output.get("verdict") == "accept"
        )
    elif policy == "smt-statement-fixture-v1":
        valid = (
            output.get("expected")
            == "对所有实数 x，若 0 <= x <= 1，则 x <= 0。"
            and output.get("actual") == output.get("expected")
            and output.get("match") is True
        )
    elif policy == "lean-kernel-fixture-v1":
        version = output.get("version", {})
        build = output.get("build", {})
        valid = (
            isinstance(version, dict)
            and isinstance(build, dict)
            and output.get("toolchain") == "leanprover/lean4:v4.33.0"
            and version.get("exit_code") == 0
            and "version 4.33.0" in version.get("stdout", "")
            and build.get("exit_code") == 0
        )
    elif policy == "lean-axiom-fixture-v1":
        valid = (
            output.get("escapes") == []
            and output.get("axiom_clean") is True
            and isinstance(output.get("axiom_output"), str)
            and "does not depend on any axioms" in output.get("axiom_output", "")
        )
    elif policy == "lean-statement-fixture-v1":
        valid = (
            output.get("expected_declaration")
            == "theorem two_add_two : (2 : ℕ) + 2 = 4"
            and output.get("match") is True
        )
    elif policy == "test-fixture-v1":
        valid = output.get("capability") == capability and output.get("verdict") == verdict
    else:
        raise EvidenceError(f"未知 verifier policy：{policy}")
    if not valid:
        raise EvidenceError(f"verifier 输出不满足 policy={policy}")


def create_evidence_receipt(
    *,
    project_root: Path,
    result: dict[str, Any],
    generator: str,
    evidence_id: str,
    capability: str,
    verdict: str,
    verifier: str,
    checked_at: str,
    output_locator: str,
    command: list[str],
    timeout_seconds: int,
    resource_budget: dict[str, int],
    stop_condition: str,
    termination_status: str,
    termination_reason: str,
    notes: str,
    executor: str = "subprocess",
    invalidates: list[str] | None = None,
) -> dict[str, Any]:
    """为已存在的 verifier 输出生成可现场重算的 Result evidence 项。"""
    if not isinstance(result, dict):
        raise EvidenceError("证据 subject result 必须是 object")
    if not isinstance(invalidates, (list, type(None))) or (
        invalidates is not None
        and (
            len(invalidates) > MAX_LIST_ITEMS
            or not all(
                isinstance(item, str)
                and item
                and len(item) <= MAX_FIELD_CHARS
                for item in invalidates
            )
        )
    ):
        raise EvidenceError("证据 invalidates 必须是字符串列表")
    if not isinstance(verdict, str) or verdict not in {"accept", "reject"}:
        raise EvidenceError("证据 verdict 无效")
    if invalidates and verdict != "reject":
        raise EvidenceError("只有 verdict=reject 的证据可以声明 invalidates")
    if (
        not isinstance(evidence_id, str)
        or len(evidence_id) > MAX_FIELD_CHARS
        or not re.fullmatch(r"evidence:[a-z0-9][a-z0-9.-]*", evidence_id)
    ):
        raise EvidenceError("证据 evidence_id 格式无效")
    for field in ("problem_id", "attempt_id", "result_id"):
        value = result.get(field)
        if not isinstance(value, str) or not value or len(value) > MAX_FIELD_CHARS:
            raise EvidenceError(f"证据 subject {field} 无效")
    result_id = result.get("result_id")
    if (
        not isinstance(result_id, str)
        or len(result_id) > MAX_FIELD_CHARS
        or not re.fullmatch(r"result:[a-z0-9][a-z0-9.-]*", result_id)
    ):
        raise EvidenceError("证据 subject result_id 格式无效")
    if (
        not isinstance(timeout_seconds, int)
        or isinstance(timeout_seconds, bool)
        or timeout_seconds <= 0
        or timeout_seconds > MAX_TIMEOUT_SECONDS
    ):
        raise EvidenceError("证据回执 timeout_seconds 超出平台上限")
    required_budget = {"memory_budget_mb", "threads_max", "max_output_bytes"}
    if (
        not isinstance(resource_budget, dict)
        or set(resource_budget) != required_budget
        or any(
            not isinstance(value, int)
            or isinstance(value, bool)
            or value <= 0
            or (
                (key == "memory_budget_mb" and value > MAX_MEMORY_BUDGET_MB)
                or (key == "threads_max" and value > MAX_THREADS)
                or (key == "max_output_bytes" and value > MAX_OUTPUT_BYTES)
            )
            for key, value in resource_budget.items()
        )
    ):
        raise EvidenceError("证据回执必须声明完整的正资源预算")
    if not isinstance(stop_condition, str) or not stop_condition.strip() or len(stop_condition) > MAX_FIELD_CHARS:
        raise EvidenceError("证据回执必须声明 stop_condition")
    if not isinstance(termination_status, str) or termination_status not in {"completed", "failed", "timed_out", "cancelled"}:
        raise EvidenceError("证据回执 termination.status 无效")
    if not isinstance(termination_reason, str) or not termination_reason.strip() or len(termination_reason) > MAX_FIELD_CHARS:
        raise EvidenceError("证据回执必须声明 termination.reason")
    if (
        not isinstance(command, list)
        or not command
        or len(command) > MAX_COMMAND_ITEMS
        or any(not isinstance(item, str) or not item for item in command)
        or any("\x00" in item for item in command)
        or sum(len(item.encode("utf-8")) + 1 for item in command) > MAX_COMMAND_BYTES
    ):
        raise EvidenceError("证据回执 command 超过大小或格式预算")
    if not isinstance(output_locator, str) or not output_locator or len(output_locator) > MAX_PATH_CHARS:
        raise EvidenceError("证据回执 output locator 无效")
    if not isinstance(capability, str) or not capability or len(capability) > MAX_FIELD_CHARS:
        raise EvidenceError("证据 capability 必须是有界字符串")
    if not isinstance(checked_at, str) or not checked_at or len(checked_at) > MAX_FIELD_CHARS:
        raise EvidenceError("证据 checked_at 必须是有界字符串")
    if not isinstance(notes, str) or len(notes) > MAX_FIELD_CHARS:
        raise EvidenceError("证据 notes 超过大小预算")
    if verdict == "accept" and termination_status != "completed":
        raise EvidenceError("accept 证据必须以 completed termination 结束")
    if (
        not isinstance(verifier, str)
        or not verifier
        or len(verifier) > MAX_FIELD_CHARS
        or not isinstance(generator, str)
        or not generator
        or len(generator) > MAX_FIELD_CHARS
    ):
        raise EvidenceError("证据 verifier/generator 必须是字符串")
    if verdict not in {"accept", "reject"}:
        raise EvidenceError("证据 verdict 无效")
    registry = load_verifier_registry(project_root)
    principal = registry.get(verifier)
    if principal is None or principal.get("role") != "verifier":
        raise EvidenceError(f"未注册 verifier：{verifier}")
    if capability not in principal["capabilities"]:
        raise EvidenceError(f"{verifier} 未注册 capability={capability}")
    if not isinstance(executor, str) or executor not in {"subprocess", "in_process"}:
        raise EvidenceError(f"未知 verifier executor：{executor}")
    output_path = _trusted_file(project_root, output_locator)
    _validate_output_policy(
        policy=principal["policy"],
        output_path=output_path,
        verdict=verdict,
        capability=capability,
        invalidates=invalidates or [],
    )
    generator_entry = registry.get(generator)
    if generator_entry is None or generator_entry.get("role") != "generator":
        raise EvidenceError(f"未注册 generator：{generator}")
    independent = principal["trust_domain"] != generator_entry["trust_domain"]
    receipt_locator = (
        f"research/artifacts/receipts/{result_id.removeprefix('result:')}/"
        f"{evidence_id.removeprefix('evidence:')}.json"
    )
    receipt = {
        "schema_version": "1.0.0",
        "evidence_id": evidence_id,
        "capability": capability,
        "verdict": verdict,
        "verifier": verifier,
        "checked_at": checked_at,
        "subject": {
            "problem_id": result["problem_id"],
            "attempt_id": result["attempt_id"],
            "result_id": result["result_id"],
        },
        "output": {
            "locator": output_locator,
            "sha256": sha256_file(output_path, max_bytes=MAX_VERIFIER_JSON_BYTES),
        },
        "command": {
            "executor": executor,
            "argv": command,
            "exit_code": 0,
            "timeout_seconds": timeout_seconds,
            "resource_budget": resource_budget,
            "stop_condition": stop_condition,
            "termination": {
                "status": termination_status,
                "reason": termination_reason,
            },
        },
    }
    _validate_schema(
        project_root / "research" / "schema" / "evidence-receipt.schema.json",
        receipt,
        "证据回执",
    )
    resolved_project_root = project_root.resolve()
    receipt_relative = Path(receipt_locator)
    lexical = resolved_project_root
    for part in receipt_relative.parts:
        lexical = lexical / part
        if lexical.is_symlink():
            raise EvidenceError("证据回执路径禁止 symlink")
    receipt_path = resolved_project_root / receipt_relative
    try:
        encoded = (
            json.dumps(
                receipt, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False
            )
            + "\n"
        ).encode()
    except (TypeError, ValueError) as exc:
        raise EvidenceError("证据回执不是可移植 JSON") from exc
    if receipt_path.exists():
        existing = _trusted_file(resolved_project_root, receipt_locator)
        if _read_bounded(existing, max_bytes=MAX_VERIFIER_JSON_BYTES) != encoded:
            raise EvidenceError(f"证据回执已存在且内容不同：{receipt_locator}")
    else:
        _write_atomic(receipt_path, encoded)
    return {
        "evidence_id": evidence_id,
        "capability": capability,
        "verdict": verdict,
        "verifier": verifier,
        "independent": independent,
        "locator": receipt_locator,
        "sha256": sha256_file(receipt_path, max_bytes=MAX_VERIFIER_JSON_BYTES),
        "checked_at": checked_at,
        "invalidates": invalidates or [],
        "notes": notes,
    }


def verify_evidence_receipt(
    *,
    project_root: Path,
    result: dict[str, Any],
    evidence: dict[str, Any],
    generator: str,
) -> str:
    """验证回执、底层输出、签发能力与派生独立性，返回 capability。"""
    if not isinstance(result, dict) or not isinstance(evidence, dict):
        raise EvidenceError("证据验证输入必须是 object")
    invalidates = evidence.get("invalidates", [])
    if (
        not isinstance(invalidates, list)
        or len(invalidates) > MAX_LIST_ITEMS
        or not all(isinstance(item, str) and item and len(item) <= MAX_FIELD_CHARS for item in invalidates)
    ):
        raise EvidenceError("证据 invalidates 必须是字符串列表")
    if not isinstance(generator, str) or not generator or len(generator) > MAX_FIELD_CHARS:
        raise EvidenceError("证据 generator 必须是有界字符串")
    verifier_id = evidence.get("verifier")
    if not isinstance(verifier_id, str) or not verifier_id or len(verifier_id) > MAX_FIELD_CHARS:
        raise EvidenceError("证据 verifier 必须是有界字符串")
    registry = load_verifier_registry(project_root)
    generator_entry = registry.get(generator)
    verifier_entry = registry.get(verifier_id)
    if generator_entry is None or generator_entry.get("role") != "generator":
        raise EvidenceError(f"未注册 generator：{generator}")
    if verifier_entry is None or verifier_entry.get("role") != "verifier":
        raise EvidenceError(f"未注册 verifier：{evidence.get('verifier')}")
    capability = evidence.get("capability")
    if not isinstance(capability, str) or not capability or len(capability) > MAX_FIELD_CHARS:
        raise EvidenceError("证据 capability 必须是有界字符串")
    if capability not in verifier_entry.get("capabilities", []):
        raise EvidenceError(f"verifier 未注册 capability={capability}")
    derived_independent = (
        verifier_entry["trust_domain"] != generator_entry["trust_domain"]
    )
    if evidence.get("independent") is not derived_independent:
        raise EvidenceError("independent 与 registry 派生值不一致")

    receipt_path = _trusted_file(project_root, evidence.get("locator", ""))
    claimed_digest = evidence.get("sha256")
    if not isinstance(claimed_digest, str) or sha256_file(
        receipt_path, max_bytes=MAX_VERIFIER_JSON_BYTES
    ) != claimed_digest:
        raise EvidenceError("回执 SHA-256 与现场文件不匹配")
    try:
        receipt = json.loads(
            _read_bounded(receipt_path, max_bytes=MAX_VERIFIER_JSON_BYTES).decode("utf-8"),
            parse_constant=_reject_json_constant,
        )
    except EvidenceError:
        raise
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EvidenceError("证据回执不是有效 JSON") from exc
    _validate_schema(
        project_root / "research" / "schema" / "evidence-receipt.schema.json",
        receipt,
        "证据回执",
    )
    for field in ("evidence_id", "capability", "verdict", "verifier", "checked_at"):
        if receipt.get(field) != evidence.get(field):
            raise EvidenceError(f"回执字段与 Result 不一致：{field}")
    expected_subject = {
        "problem_id": result.get("problem_id"),
        "attempt_id": result.get("attempt_id"),
        "result_id": result.get("result_id"),
    }
    if receipt.get("subject") != expected_subject:
        raise EvidenceError("回执 subject 与 Result 不一致")
    command = receipt.get("command", {})
    if evidence.get("verdict") == "accept" and command.get("exit_code") != 0:
        raise EvidenceError("accept 回执必须绑定成功 verifier 命令")
    if evidence.get("verdict") == "accept" and command.get("termination", {}).get("status") != "completed":
        raise EvidenceError("accept 回执必须绑定 completed termination")
    output = receipt.get("output", {})
    output_path = _trusted_file(project_root, output.get("locator", ""))
    if sha256_file(output_path, max_bytes=MAX_VERIFIER_JSON_BYTES) != output.get("sha256"):
        raise EvidenceError("verifier 输出 SHA-256 与现场文件不匹配")
    _validate_output_policy(
        policy=verifier_entry["policy"],
        output_path=output_path,
        verdict=evidence.get("verdict"),
        capability=capability,
        invalidates=evidence.get("invalidates", []),
    )
    return capability
