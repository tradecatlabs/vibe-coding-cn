"""固定 Lean/Mathlib fixture 的 kernel、逃逸和公理审计 adapter。"""

from __future__ import annotations

import json
import os
import re
import stat
import shutil
from pathlib import Path
from typing import Any

from .evidence import create_evidence_receipt
from .runtime import execute_bounded, now


ESCAPE_PATTERN = re.compile(r"\b(?:sorry|admit|unsafe)\b")
EXPECTED_TOOLCHAIN = "leanprover/lean4:v4.33.0"
EXPECTED_VERSION_FRAGMENT = "version 4.33.0"
EXPECTED_MATHLIB_REV = "db584cd6d46c92f209a44c0f1c829460d327499d"
EXPECTED_DECLARATION = "theorem two_add_two : (2 : ℕ) + 2 = 4"
EXPECTED_AXIOM_AUDIT = "#print axioms VibeMathingFixture.two_add_two"
MAX_FIXTURE_FILE_BYTES = 30_000_000
MAX_OUTPUT_BYTES = 2_000_000
MAX_PATH_CHARS = 4_096
MAX_PACKAGES = 1_000


def _reject_json_constant(value: str) -> Any:
    raise RuntimeError(f"Lean JSON 含非法常量：{value}")


def _safe_component(value: str, label: str) -> str:
    if not isinstance(value, str) or len(value) > 256 or not re.fullmatch(
        r"[a-z0-9][a-z0-9.-]*", value
    ):
        raise RuntimeError(f"Lean {label} 路径组件无效")
    return value


def _safe_package_name(value: str) -> str:
    if not isinstance(value, str) or len(value) > 256 or not re.fullmatch(
        r"[A-Za-z0-9][A-Za-z0-9_.-]*", value
    ) or value in {".", ".."}:
        raise RuntimeError("Lean manifest package name 无效")
    return value


def _read_existing_output(path: Path) -> bytes:
    path = Path(path)
    if path.is_symlink() or path.resolve() != path:
        raise RuntimeError("Lean verifier output 不能是 symlink")
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise RuntimeError("当前平台无法安全读取 Lean verifier output")
    descriptor = os.open(path, os.O_RDONLY | nofollow)
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode) or file_stat.st_size > MAX_OUTPUT_BYTES:
            raise RuntimeError("已有 Lean verifier output 超过大小预算")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(64 * 1024, MAX_OUTPUT_BYTES - total + 1))
            if not chunk:
                return b"".join(chunks)
            total += len(chunk)
            if total > MAX_OUTPUT_BYTES:
                raise RuntimeError("已有 Lean verifier output 超过大小预算")
            chunks.append(chunk)
    finally:
        os.close(descriptor)


def _read_build_artifact_size(path: Path, max_bytes: int) -> int:
    if (
        not isinstance(max_bytes, int)
        or isinstance(max_bytes, bool)
        or max_bytes <= 0
        or max_bytes > MAX_OUTPUT_BYTES
    ):
        raise RuntimeError("Lean build artifact 大小预算无效")
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise RuntimeError("当前平台无法安全读取 Lean build artifact")
    descriptor = os.open(path, os.O_RDONLY | nofollow)
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode) or file_stat.st_size > max_bytes:
            raise RuntimeError("Lean build artifact 缺失或超过输出预算")
        return file_stat.st_size
    finally:
        os.close(descriptor)


def _safe_fixture_path(fixture_root: Path, relative: str) -> Path:
    root = fixture_root.resolve()
    if (
        not root.is_dir()
        or fixture_root.is_symlink()
        or fixture_root.absolute() != root
    ):
        raise RuntimeError("Lean fixture root 必须是非 symlink 目录")
    if not isinstance(relative, str) or not relative or len(relative) > MAX_PATH_CHARS:
        raise RuntimeError(f"Lean fixture 路径越界：{relative}")
    path = Path(relative)
    if (
        "\x00" in relative
        or "\\" in relative
        or path.is_absolute()
        or ".." in path.parts
        or "." in path.parts
        or any(part in {".", ".."} for part in relative.split("/"))
    ):
        raise RuntimeError(f"Lean fixture 路径越界：{relative}")
    lexical = root
    for part in path.parts:
        lexical = lexical / part
        if lexical.is_symlink():
            raise RuntimeError(f"Lean fixture 路径不能包含 symlink：{relative}")
    resolved = (root / path).resolve()
    if resolved != root and root not in resolved.parents:
        raise RuntimeError(f"Lean fixture 路径越界：{relative}")
    return resolved


def _read_fixture_text(path: Path) -> str:
    if path.is_symlink() or not path.is_file():
        raise RuntimeError(f"Lean fixture 文件不可读：{path}")
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise RuntimeError("当前平台无法安全读取 Lean fixture")
    descriptor = os.open(path, os.O_RDONLY | nofollow)
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode) or file_stat.st_size > MAX_FIXTURE_FILE_BYTES:
            raise RuntimeError(f"Lean fixture 文件不可读：{path}")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(64 * 1024, MAX_FIXTURE_FILE_BYTES - total + 1))
            if not chunk:
                break
            total += len(chunk)
            if total > MAX_FIXTURE_FILE_BYTES:
                raise RuntimeError(f"Lean fixture 文件超过大小预算：{path}")
            chunks.append(chunk)
    finally:
        os.close(descriptor)
    try:
        return b"".join(chunks).decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError(f"Lean fixture 文件不是 UTF-8：{path}") from exc


def _resolve_tool(name: str) -> str:
    """从 PATH 或 elan 官方默认目录解析 Lean 工具，不修改进程环境。"""
    resolved = shutil.which(name)
    if resolved:
        resolved_path = Path(resolved)
        if (
            resolved_path.is_symlink()
            or resolved_path.resolve() != resolved_path
            or not resolved_path.is_file()
        ):
            raise RuntimeError(f"Lean 工具路径不安全：{resolved}")
        return str(resolved_path)
    elan_tool = Path.home() / ".elan" / "bin" / name
    if elan_tool.is_symlink() or elan_tool.resolve() != elan_tool:
        raise RuntimeError(f"Lean 工具不能是 symlink：{elan_tool}")
    if elan_tool.is_file() and os.access(elan_tool, os.X_OK):
        return str(elan_tool)
    raise RuntimeError(
        f"找不到 {name}；请安装 elan/Lean，或将 ~/.elan/bin 加入 PATH"
    )


def _lean_environment(
    fixture_root: Path, manifest: dict[str, Any], lean: str
) -> dict[str, str]:
    """Construct a minimal, manifest-bound environment without invoking Lake."""
    if not isinstance(manifest, dict):
        raise RuntimeError("Lean manifest 必须是 object")
    packages_dir_value = manifest.get("packagesDir", ".lake/packages")
    if not isinstance(packages_dir_value, str):
        raise RuntimeError("Lean manifest packagesDir 无效")
    packages_dir = Path(packages_dir_value)
    if packages_dir.is_absolute() or ".." in packages_dir.parts:
        raise RuntimeError("Lean manifest packagesDir 越界")
    package_root = _safe_fixture_path(fixture_root, packages_dir_value)
    fixture_resolved = fixture_root.resolve()
    if fixture_resolved not in package_root.parents and package_root != fixture_resolved:
        raise RuntimeError("Lean manifest packagesDir 越界")
    lean_paths: list[str] = []
    package_bins: list[str] = []
    packages = manifest.get("packages", [])
    if not isinstance(packages, list) or len(packages) > MAX_PACKAGES:
        raise RuntimeError("Lean manifest packages 无效或超过数量预算")
    package_names: set[str] = set()
    for package in packages:
        if not isinstance(package, dict) or not isinstance(package.get("name"), str):
            raise RuntimeError("Lean manifest package entry 无效")
        name = _safe_package_name(package["name"])
        if name in package_names:
            raise RuntimeError("Lean manifest package name 重复")
        package_names.add(name)
        package_path = package_root / name
        if package_path.is_symlink():
            raise RuntimeError(f"Lean dependency cache 不能是 symlink：{name}")
        resolved_package = package_path.resolve()
        if (
            resolved_package != package_root
            and package_root not in resolved_package.parents
        ):
            raise RuntimeError(f"Lean manifest package 越界：{name}")
        if not resolved_package.is_dir():
            raise RuntimeError(f"Lean dependency cache 缺失：{name}")
        library_path = resolved_package / ".lake" / "build" / "lib" / "lean"
        binary_path = resolved_package / ".lake" / "build" / "bin"
        if library_path.is_symlink() or library_path.resolve() != library_path:
            raise RuntimeError(f"Lean dependency library path 不能是 symlink：{name}")
        if binary_path.is_symlink() or binary_path.resolve() != binary_path:
            raise RuntimeError(f"Lean dependency binary path 不能是 symlink：{name}")
        if library_path.is_dir():
            lean_paths.append(str(library_path))
        if binary_path.is_dir():
            package_bins.append(str(binary_path))
    root_library = _safe_fixture_path(
        fixture_root, ".lake/build/lib/lean"
    )
    root_library.mkdir(parents=True, exist_ok=True)
    if root_library.is_symlink() or root_library.resolve() != root_library:
        raise RuntimeError("Lean root library 不能是 symlink")
    lean_paths.extend([str(root_library), str(Path(lean).resolve().parents[1] / "lib" / "lean")])
    toolchain_bin = str(Path(lean).resolve().parent)
    safe_path = package_bins + [toolchain_bin, "/usr/local/bin", "/usr/bin", "/bin"]
    environment = {
        "PATH": os.pathsep.join(dict.fromkeys(safe_path)),
        "LEAN_PATH": os.pathsep.join(dict.fromkeys(lean_paths)),
        "HOME": os.environ.get("HOME", str(Path.home())),
        "LANG": os.environ.get("LANG", "C.UTF-8"),
        "LC_ALL": os.environ.get("LC_ALL", "C.UTF-8"),
        "TMPDIR": os.environ.get("TMPDIR", "/tmp"),
    }
    return environment


def _write_output(project_root: Path, run_key: str, name: str, payload: dict[str, Any]) -> str:
    run_key = _safe_component(run_key, "result")
    name = _safe_component(name, "output")
    relative = f"research/artifacts/outputs/{run_key}/{name}.json"
    root = project_root.resolve()
    if project_root.is_symlink() or project_root.absolute() != root or not root.is_dir():
        raise RuntimeError("Lean verifier output project root 不能通过 symlink 访问")
    path_parts = Path(relative)
    if ".." in path_parts.parts or path_parts.is_absolute():
        raise RuntimeError("Lean verifier output 路径越界")
    lexical = root
    for part in path_parts.parts:
        lexical = lexical / part
        if lexical.is_symlink():
            raise RuntimeError("Lean verifier output 路径不能包含 symlink")
    path = root / path_parts
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        encoded = (
            json.dumps(
                payload, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False
            )
            + "\n"
        )
    except (TypeError, ValueError) as exc:
        raise RuntimeError("Lean verifier output 不是可移植 JSON") from exc
    if len(encoded.encode("utf-8")) > MAX_OUTPUT_BYTES:
        raise RuntimeError("Lean verifier output 超过大小预算")
    if path.is_symlink():
        raise RuntimeError("Lean verifier output 不能是 symlink")
    if path.is_file():
        nofollow = getattr(os, "O_NOFOLLOW", None)
        if nofollow is None:
            raise RuntimeError("当前平台无法安全读取 Lean verifier output")
        existing = _read_existing_output(path)
        if existing.decode("utf-8") != encoded:
            raise RuntimeError(f"Lean verifier 输出已存在且内容不同：{relative}")
        return relative
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise RuntimeError("当前平台无法安全创建 Lean verifier output")
    directory = getattr(os, "O_DIRECTORY", None)
    if directory is None:
        raise RuntimeError("当前平台无法安全持久化 Lean verifier output")
    try:
        descriptor = os.open(
            temporary,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | nofollow,
            0o600,
        )
    except OSError as exc:
        raise RuntimeError("无法创建 Lean verifier output 暂存文件") from exc
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        directory_descriptor = os.open(path.parent, os.O_RDONLY | directory | nofollow)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise
    return relative


def verify_lean_fixture(
    *, project_root: Path, fixture_root: Path, result: dict[str, Any]
) -> list[dict[str, Any]]:
    """运行真实 Lean 命令并返回可被 Result 消费的三类证据。"""
    if not isinstance(result, dict):
        raise RuntimeError("Lean verifier result 必须是 object")
    fixture_root_input = Path(fixture_root)
    fixture_root = fixture_root_input.absolute()
    if (
        fixture_root_input.is_symlink()
        or fixture_root != fixture_root.resolve()
        or not fixture_root.is_dir()
    ):
        raise RuntimeError("Lean fixture root 不能通过 symlink 访问")
    source = _safe_fixture_path(fixture_root, "VibeMathingFixture.lean")
    axiom_audit = _safe_fixture_path(fixture_root, "AxiomAudit.lean")
    toolchain_path = _safe_fixture_path(fixture_root, "lean-toolchain")
    lakefile_path = _safe_fixture_path(fixture_root, "lakefile.toml")
    manifest_path = _safe_fixture_path(fixture_root, "lake-manifest.json")
    toolchain = _read_fixture_text(toolchain_path).strip()
    lakefile = _read_fixture_text(lakefile_path)
    try:
        manifest = json.loads(
            _read_fixture_text(manifest_path), parse_constant=_reject_json_constant
        )
    except json.JSONDecodeError as exc:
        raise RuntimeError("Lean lake-manifest.json 不是有效 JSON") from exc
    if (
        not isinstance(manifest, dict)
        or not isinstance(manifest.get("packages"), list)
        or len(manifest["packages"]) > MAX_PACKAGES
    ):
        raise RuntimeError("Lean lake-manifest.json 契约无效")
    source_text = _read_fixture_text(source)
    axiom_audit_text = _read_fixture_text(axiom_audit)
    for item in manifest["packages"]:
        if (
            not isinstance(item, dict)
            or not isinstance(item.get("name"), str)
            or not isinstance(item.get("rev"), str)
        ):
            raise RuntimeError("Lean lake-manifest.json package entry 无效")
        _safe_package_name(item["name"])
        if len(item["rev"]) > 128 or not re.fullmatch(r"[A-Za-z0-9._+-]+", item["rev"]):
            raise RuntimeError("Lean lake-manifest.json package revision 无效")
    package_names = [item["name"] for item in manifest["packages"]]
    if len(package_names) != len(set(package_names)):
        raise RuntimeError("Lean lake-manifest.json package name 重复")
    mathlib_revisions = {
        item["rev"]
        for item in manifest["packages"]
        if item["name"] == "mathlib"
    }
    if (
        toolchain != EXPECTED_TOOLCHAIN
        or EXPECTED_MATHLIB_REV not in lakefile
        or mathlib_revisions != {EXPECTED_MATHLIB_REV}
        or EXPECTED_AXIOM_AUDIT not in axiom_audit_text
    ):
        raise RuntimeError("Lean/Mathlib 固定版本契约漂移")
    escapes = ESCAPE_PATTERN.findall(source_text)
    declaration_match = EXPECTED_DECLARATION in source_text
    budgets = {
        "timeout_seconds": 600,
        "max_output_bytes": 2_000_000,
        # Lean's runtime reserves substantial virtual address space even for
        # this small fixture; 8192 MB is a hard ceiling, not a reservation.
        "memory_budget_mb": 8192,
        "threads_max": 1,
    }
    evidence_resource_budget = {
        "memory_budget_mb": budgets["memory_budget_mb"],
        "threads_max": budgets["threads_max"],
        "max_output_bytes": budgets["max_output_bytes"],
    }
    lean = _resolve_tool("lean")
    lean_env = _lean_environment(fixture_root, manifest, lean)
    version = execute_bounded(
        [lean, "-j1", "--version"],
        cwd=fixture_root,
        env=lean_env,
        **budgets,
    )
    build_output = _safe_fixture_path(
        fixture_root, ".lake/build/lib/lean/VibeMathingFixture.olean"
    )
    if build_output.is_symlink():
        raise RuntimeError("Lean build output 不能是 symlink")
    build = execute_bounded(
        [lean, "-j1", "-o", str(build_output), "VibeMathingFixture.lean"],
        cwd=fixture_root,
        env=lean_env,
        **budgets,
    )
    axioms = execute_bounded(
        [lean, "-j1", "AxiomAudit.lean"],
        cwd=fixture_root,
        env=lean_env,
        **budgets,
    )
    if any(
        not isinstance(value, dict)
        or isinstance(value.get("exit_code"), bool)
        or not isinstance(value.get("exit_code"), int)
        or not isinstance(value.get("stdout"), str)
        or not isinstance(value.get("stderr"), str)
        for value in (version, build, axioms)
    ):
        raise RuntimeError("Lean bounded command 返回类型无效")
    version_text = version["stdout"] + version["stderr"]
    if (
        version["exit_code"] != 0
        or EXPECTED_VERSION_FRAGMENT not in version_text
        or build["exit_code"] != 0
        or axioms["exit_code"] != 0
    ):
        raise RuntimeError("Lean 工具链或 fixture 构建失败")
    _read_build_artifact_size(build_output, budgets["max_output_bytes"])
    axiom_text = axioms["stdout"] + axioms["stderr"]
    axiom_clean = "does not depend on any axioms" in axiom_text
    result_id = result.get("result_id")
    if not isinstance(result_id, str) or not result_id.startswith("result:"):
        raise RuntimeError("Lean verifier result_id 无效")
    run_key = _safe_component(result_id.removeprefix("result:"), "result")
    kernel_locator = _write_output(
        project_root,
        run_key,
        "lean-kernel",
        {
            "toolchain": toolchain,
            "version": {
                "exit_code": version["exit_code"],
                "stdout": version["stdout"],
            },
            "build": {"exit_code": build["exit_code"]},
        },
    )
    audit_locator = _write_output(
        project_root,
        run_key,
        "lean-axiom-audit",
        {"escapes": escapes, "axiom_output": axiom_text, "axiom_clean": axiom_clean},
    )
    faithfulness_locator = _write_output(
        project_root,
        run_key,
        "lean-statement-faithfulness",
        {"expected_declaration": EXPECTED_DECLARATION, "match": declaration_match},
    )
    checked_at = now()
    return [
        create_evidence_receipt(
            project_root=project_root,
            result=result,
            generator="lean-generator",
            evidence_id=f"evidence:{run_key}.kernel",
            capability="kernel_check",
            verdict="accept",
            verifier="lean-kernel",
            checked_at=checked_at,
            output_locator=kernel_locator,
            command=["lean", "-j1", "-o", ".lake/build/lib/lean/VibeMathingFixture.olean", "VibeMathingFixture.lean"],
            timeout_seconds=budgets["timeout_seconds"],
            resource_budget=evidence_resource_budget,
            stop_condition="Lean build 完成或退出码非零",
            termination_status="completed",
            termination_reason="bounded Lean build returned",
            notes="固定 Lean/Mathlib 的真实 kernel build",
        ),
        create_evidence_receipt(
            project_root=project_root,
            result=result,
            generator="lean-generator",
            evidence_id=f"evidence:{run_key}.axioms",
            capability="axiom_escape_audit",
            verdict="accept" if not escapes and axiom_clean else "reject",
            verifier="lean-axiom-auditor",
            checked_at=checked_at,
            output_locator=audit_locator,
            command=["lean", "-j1", "AxiomAudit.lean"],
            timeout_seconds=budgets["timeout_seconds"],
            resource_budget=evidence_resource_budget,
            stop_condition="源码逃逸与 axiom audit 完成或退出码非零",
            termination_status="completed",
            termination_reason="bounded Lean axiom audit returned",
            notes="源码逃逸扫描与已编译模块上的 #print axioms",
        ),
        create_evidence_receipt(
            project_root=project_root,
            result=result,
            generator="lean-generator",
            evidence_id=f"evidence:{run_key}.faithfulness",
            capability="statement_faithfulness",
            verdict="accept" if declaration_match else "reject",
            verifier="lean-faithfulness-reviewer",
            checked_at=checked_at,
            output_locator=faithfulness_locator,
            command=["vibe-mathing", "verify-lean-statement-contract"],
            timeout_seconds=budgets["timeout_seconds"],
            resource_budget=evidence_resource_budget,
            stop_condition="fixture 陈述与 ProblemContract 比较完成",
            termination_status="completed",
            termination_reason="statement contract check returned",
            executor="in_process",
            notes="fixture 陈述与固定 Problem Contract 对应",
        ),
    ]
