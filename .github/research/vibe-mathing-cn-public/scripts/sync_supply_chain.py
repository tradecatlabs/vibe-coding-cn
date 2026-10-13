#!/usr/bin/env python3
# 做什么：按 vendor/sources.lock.json 同步或检查 Git 上游、无工作树参考缓存、本机研究归档镜像和审计快照。
# 怎么运行：python3 scripts/sync_supply_chain.py [--check] [--references-only]
# 需要什么：Python 3、Git、rsync；Git 上游同步需要网络，本机镜像不需要网络。

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path

from vibe_mathing.runtime import RuntimeErrorBase, execute_bounded


ROOT = Path(__file__).resolve().parents[1]
COMMAND_TIMEOUT_SECONDS = 300
LOCK_PATH = ROOT / "vendor" / "sources.lock.json"
VENDOR_ROOT = (ROOT / "vendor").resolve()
UPSTREAM_ROOT = (VENDOR_ROOT / "upstream").resolve()
REFERENCE_ROOT = (UPSTREAM_ROOT / "reference").resolve()
GITHUB_GIT_URL = re.compile(
    r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\.git"
)
GIT_BRANCH = re.compile(r"[A-Za-z0-9._-]+(?:/[A-Za-z0-9._-]+)*")
GIT_COMMIT = re.compile(r"[0-9a-f]{40}")
ROOT_LICENSE_PATH = re.compile(r"[A-Za-z0-9._-]+")
MAX_COMMAND_OUTPUT_BYTES = 8_000_000
MAX_VENDOR_FILE_BYTES = 256_000_000
MAX_LOCK_BYTES = 5_000_000
MAX_TREE_ENTRIES = 100_000
MAX_PATH_CHARS = 4_096
ALLOWED_SOURCE_KINDS = {"git", "git-reference", "local-mirror", "local-snapshot"}


def _safe_environment(*, allow_lazy_fetch: bool) -> dict[str, str]:
    allowed = {"PATH", "HOME", "LANG", "LC_ALL", "TMPDIR", "GIT_NO_LAZY_FETCH", "GIT_TERMINAL_PROMPT"}
    environment = {key: value for key, value in os.environ.items() if key in allowed}
    environment["PATH"] = environment.get("PATH", "/usr/local/bin:/usr/bin:/bin")
    environment["GIT_TERMINAL_PROMPT"] = "0"
    if allow_lazy_fetch:
        environment.pop("GIT_NO_LAZY_FETCH", None)
    else:
        environment["GIT_NO_LAZY_FETCH"] = "1"
    return environment


def _run_bounded(args: list[str], *, cwd: Path | None, allow_lazy_fetch: bool) -> dict[str, object]:
    effective_cwd = ROOT if cwd is None else cwd
    try:
        return execute_bounded(
            args,
            cwd=effective_cwd,
            timeout_seconds=COMMAND_TIMEOUT_SECONDS,
            max_output_bytes=MAX_COMMAND_OUTPUT_BYTES,
            memory_budget_mb=512,
            threads_max=1,
            env=_safe_environment(allow_lazy_fetch=allow_lazy_fetch),
        )
    except RuntimeErrorBase as exc:
        raise RuntimeError(f"供应链命令边界失败：{exc}") from exc


def run(args: list[str], *, cwd: Path | None = None) -> str:
    result = _run_bounded(args, cwd=cwd, allow_lazy_fetch=True)
    stdout = result["stdout"]
    stderr = result["stderr"]
    if not isinstance(stdout, str) or not isinstance(stderr, str):
        raise RuntimeError("供应链命令输出类型无效")
    if result["exit_code"] != 0:
        detail = stderr.strip() or stdout.strip()
        raise RuntimeError(f"命令失败（{result['exit_code']}）：{' '.join(args)}\n{detail}")
    return stdout.strip()


def run_bytes(
    args: list[str],
    *,
    cwd: Path | None = None,
    allow_lazy_fetch: bool = True,
) -> bytes:
    result = _run_bounded(args, cwd=cwd, allow_lazy_fetch=allow_lazy_fetch)
    stdout = result["stdout"]
    stderr = result["stderr"]
    if not isinstance(stdout, str) or not isinstance(stderr, str):
        raise RuntimeError("供应链命令输出类型无效")
    if result["exit_code"] != 0:
        detail = (stderr or stdout).strip()
        raise RuntimeError(f"命令失败（{result['exit_code']}）：{' '.join(args)}\n{detail}")
    return stdout.encode("utf-8")


def _reject_json_constant(value: str) -> object:
    raise ValueError(f"供应链 JSON 常量非法：{value}")


def _read_bounded(path: Path, max_bytes: int) -> bytes:
    path = Path(path)
    if (
        not isinstance(max_bytes, int)
        or isinstance(max_bytes, bool)
        or max_bytes <= 0
        or max_bytes > MAX_LOCK_BYTES
        or len(str(path)) > MAX_PATH_CHARS
        or "\x00" in str(path)
        or "\\" in str(path)
        or any(part in {".", ".."} for part in path.parts)
    ):
        raise RuntimeError("供应链文件读取预算或路径无效")
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise RuntimeError("当前平台无法安全读取供应链文件")
    descriptor = os.open(path, os.O_RDONLY | nofollow)
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode) or file_stat.st_size > max_bytes:
            raise RuntimeError(f"供应链文件超过大小预算：{path}")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(64 * 1024, max_bytes - total + 1))
            if not chunk:
                return b"".join(chunks)
            total += len(chunk)
            if total > max_bytes:
                raise RuntimeError(f"供应链文件超过大小预算：{path}")
            chunks.append(chunk)
    finally:
        os.close(descriptor)


def load_sources() -> list[dict[str, object]]:
    if LOCK_PATH.is_symlink() or LOCK_PATH.resolve() != LOCK_PATH:
        raise RuntimeError(f"供应链 lockfile 不能是 symlink：{LOCK_PATH}")
    data = json.loads(
        _read_bounded(LOCK_PATH, MAX_LOCK_BYTES).decode("utf-8"),
        parse_constant=_reject_json_constant,
    )
    sources = data.get("sources") if isinstance(data, dict) else None
    if not isinstance(sources, list):
        raise RuntimeError("供应链 lockfile sources 无效")
    if len(sources) > MAX_TREE_ENTRIES or any(not isinstance(item, dict) for item in sources):
        raise RuntimeError("供应链 lockfile source entry 无效或超过数量预算")
    ids: set[str] = set()
    for source in sources:
        source_id = source.get("id")
        kind = source.get("kind")
        path = source.get("path") if kind != "local-snapshot" else source.get("source_path")
        if (
            not isinstance(source_id, str)
            or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,255}", source_id)
            or source_id in ids
            or not isinstance(kind, str)
            or kind not in ALLOWED_SOURCE_KINDS
            or not isinstance(path, str)
            or not path
            or len(path) > MAX_PATH_CHARS
            or "\x00" in path
            or "\\" in path
            or any(part in {".", ".."} for part in Path(path).parts)
        ):
            raise RuntimeError("供应链 lockfile source entry 无效")
        ids.add(source_id)
    return list(sources)


def repo_path(source: dict[str, object]) -> Path:
    declared_value = source.get("path")
    if (
        not isinstance(declared_value, str)
        or not declared_value
        or len(declared_value) > MAX_PATH_CHARS
        or "\x00" in declared_value
        or "\\" in declared_value
    ):
        raise RuntimeError("供应链路径必须是有效字符串")
    declared = Path(declared_value)
    if declared.is_absolute() or any(part in {".", ".."} for part in declared.parts):
        raise RuntimeError(f"供应链路径必须是 vendor 内相对路径：{declared}")
    lexical = ROOT
    for part in declared.parts:
        lexical = lexical / part
        if lexical.is_symlink():
            raise RuntimeError(f"供应链路径不能包含 symlink：{declared}")
    path = ROOT / declared
    resolved = path.resolve()
    try:
        resolved.relative_to(VENDOR_ROOT)
    except ValueError as exc:
        raise RuntimeError(f"供应链路径越界：{resolved}") from exc
    return path


def git_repo_path(source: dict[str, object]) -> Path:
    path = repo_path(source)
    try:
        relative = path.relative_to(UPSTREAM_ROOT)
    except ValueError as exc:
        raise RuntimeError(f"Git 供应链路径必须位于 vendor/upstream：{path}") from exc
    if len(relative.parts) != 1:
        raise RuntimeError(f"Git 供应链路径必须是 upstream 的直接子项：{path}")
    return path


def reference_repo_path(source: dict[str, object]) -> Path:
    path = repo_path(source)
    try:
        relative = path.resolve().relative_to(REFERENCE_ROOT)
    except ValueError as exc:
        raise RuntimeError(f"reference 缓存路径越界：{path}") from exc
    if len(relative.parts) != 1:
        raise RuntimeError(f"reference 缓存必须是根目录的直接子项：{path}")
    return path


def validate_git_source(source: dict[str, object], *, label: str = "Git") -> None:
    url = source.get("url")
    branch = source.get("branch")
    commit = source.get("commit")
    license_path = source.get("license_path")
    license_sha256 = source.get("license_sha256")
    if not all(isinstance(value, str) for value in (url, branch, commit, license_path, license_sha256)):
        raise RuntimeError(f"{label} lockfile 字段类型无效")
    if not GITHUB_GIT_URL.fullmatch(url) or len(url) > MAX_PATH_CHARS:
        raise RuntimeError(f"{label} URL 非受支持的 GitHub HTTPS 地址：{url}")
    if not GIT_BRANCH.fullmatch(branch) or branch in {".", ".."} or branch.startswith("-"):
        raise RuntimeError(f"{label} branch 格式非法：{branch}")
    if not GIT_COMMIT.fullmatch(commit):
        raise RuntimeError(f"{label} commit 必须是 40 位小写十六进制：{commit}")
    if not ROOT_LICENSE_PATH.fullmatch(license_path) or license_path in {".", ".."}:
        raise RuntimeError(f"{label} 许可证必须是仓库根文件：{license_path}")
    if not re.fullmatch(r"[0-9a-f]{64}", license_sha256):
        raise RuntimeError(f"{label} 许可证 SHA-256 非法：{source['id']}")


def validate_git_reference_source(source: dict[str, object]) -> None:
    validate_git_source(source, label="reference")


def ensure_clean(path: Path) -> None:
    dirty = run(["git", "status", "--porcelain"], cwd=path)
    if dirty:
        raise RuntimeError(f"供应链缓存存在本地改动，拒绝覆盖：{path}")


def sha256(path: Path) -> str:
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise RuntimeError("当前平台无法安全读取供应链文件")
    try:
        descriptor = os.open(path, os.O_RDONLY | nofollow)
    except OSError as exc:
        raise RuntimeError(f"无法读取供应链文件：{path}") from exc
    digest = hashlib.sha256()
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode):
            raise RuntimeError(f"供应链路径不是普通文件：{path}")
        if file_stat.st_size > MAX_VENDOR_FILE_BYTES:
            raise RuntimeError(f"供应链文件超过大小预算：{path}")
        total = 0
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > MAX_VENDOR_FILE_BYTES:
                raise RuntimeError(f"供应链文件超过大小预算：{path}")
            digest.update(chunk)
    finally:
        os.close(descriptor)
    return digest.hexdigest()


def bytes_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def is_excluded(relative: Path, patterns: list[str]) -> bool:
    return any(
        pattern in relative.parts
        or fnmatch.fnmatch(relative.name, pattern)
        or fnmatch.fnmatch(relative.as_posix(), pattern)
        for pattern in patterns
    )


def regular_file_size(path: Path) -> int:
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise RuntimeError("当前平台无法安全读取供应链文件")
    descriptor = os.open(path, os.O_RDONLY | nofollow)
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode):
            raise RuntimeError(f"供应链路径不是普通文件：{path}")
        if file_stat.st_size > MAX_VENDOR_FILE_BYTES:
            raise RuntimeError(f"供应链文件超过大小预算：{path}")
        return file_stat.st_size
    finally:
        os.close(descriptor)


def tree_inventory(path: Path, exclusions: list[str]) -> dict[str, object]:
    if path.is_symlink() or not path.is_dir():
        raise RuntimeError(f"目录不存在或是 symlink：{path}")
    root = path.resolve()
    digest = hashlib.sha256()
    regular_files = 0
    directories = 0
    symlinks = 0
    skill_files = 0
    total_bytes = 0

    candidates = sorted(
        (
            candidate
            for candidate in path.rglob("*")
            if not is_excluded(candidate.relative_to(path), exclusions)
        ),
        key=lambda candidate: candidate.relative_to(path).as_posix(),
    )
    if len(candidates) > MAX_TREE_ENTRIES:
        raise RuntimeError(f"供应链树条目超过数量预算：{path}")
    for candidate in candidates:
        relative = candidate.relative_to(path)
        relative_text = relative.as_posix()
        if candidate.is_symlink():
            target = candidate.readlink().as_posix()
            try:
                candidate.resolve(strict=True).relative_to(root)
            except (OSError, ValueError) as exc:
                raise RuntimeError(
                    f"供应链镜像包含失效或越界符号链接：{candidate} -> {target}"
                ) from exc
            digest.update(f"L\0{relative_text}\0{target}\n".encode())
            symlinks += 1
        elif candidate.is_dir():
            digest.update(f"D\0{relative_text}\n".encode())
            directories += 1
        elif candidate.is_file():
            size = regular_file_size(candidate)
            file_digest = sha256(candidate)
            digest.update(
                f"F\0{relative_text}\0{size}\0{file_digest}\n".encode()
            )
            regular_files += 1
            total_bytes += size
            if total_bytes > 1_000_000_000:
                raise RuntimeError(f"供应链树总大小超过预算：{path}")
            if candidate.name == "SKILL.md":
                skill_files += 1
        else:
            raise RuntimeError(f"供应链树包含不支持的文件类型：{candidate}")

    return {
        "regular_files": regular_files,
        "directories": directories,
        "symlinks": symlinks,
        "skill_files": skill_files,
        "total_bytes": total_bytes,
        "tree_sha256": digest.hexdigest(),
    }


def local_source_path(source: dict[str, object]) -> Path:
    return Path(str(source["source_path"])).expanduser().resolve()


def _bounded_string_list(source: dict[str, object], key: str) -> list[str]:
    value = source.get(key, [])
    if not isinstance(value, list) or len(value) > MAX_TREE_ENTRIES or any(
        not isinstance(item, str)
        or not item
        or len(item) > MAX_PATH_CHARS
        or "\x00" in item
        or "\\" in item
        or any(part in {".", ".."} for part in Path(item).parts)
        for item in value
    ):
        raise RuntimeError(f"供应链 {key} 列表无效或超过预算")
    return list(value)


def sync_local_mirror(source: dict[str, object]) -> None:
    origin = local_source_path(source)
    target = repo_path(source)
    if not origin.is_dir():
        raise RuntimeError(f"本机归档不存在：{origin}")
    target.mkdir(parents=True, exist_ok=True)
    exclusions = _bounded_string_list(source, "exclusions")
    args = ["rsync", "-a", "--delete", "--delete-excluded"]
    for pattern in exclusions:
        suffix = "/" if pattern in {".git", "__pycache__"} else ""
        args.append(f"--exclude={pattern}{suffix}")
    args.extend([f"{origin}/", f"{target}/"])
    run(args)


def check_local_mirror(source: dict[str, object]) -> list[str]:
    origin = local_source_path(source)
    target = repo_path(source)
    if not origin.is_dir():
        return [f"缺少本机归档：{origin}"]
    if not target.is_dir():
        return [f"缺少本机归档镜像：{target}"]

    exclusions = _bounded_string_list(source, "exclusions")
    try:
        origin_inventory = tree_inventory(origin, exclusions)
        target_inventory = tree_inventory(target, exclusions)
    except (OSError, RuntimeError) as exc:
        return [str(exc)]

    errors: list[str] = []
    if origin_inventory != target_inventory:
        errors.append(f"本机归档镜像与来源不一致：{target}")
    expected = source.get("inventory")
    if not isinstance(expected, dict):
        errors.append(f"本机归档缺少锁定 inventory：{source['id']}")
    elif target_inventory != expected:
        errors.append(
            f"本机归档 inventory 漂移：{source['id']} 实际 "
            f"{json.dumps(target_inventory, ensure_ascii=False, sort_keys=True)}"
        )
    return errors


def sync_git(source: dict[str, object]) -> None:
    validate_git_source(source)
    path = git_repo_path(source)
    url = str(source["url"])
    commit = str(source["commit"])
    sparse_paths = _bounded_string_list(source, "sparse_paths")

    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        # Do not clone a moving branch. Initialize an empty repository and fetch
        # only the lockfile commit; a branch name is provenance metadata, not a
        # resolver for executable or materialized content.
        run(["git", "init", str(path)])
        run(["git", "remote", "add", "origin", url], cwd=path)
        run(
            ["git", "fetch", "--no-tags", "--depth", "1", "--filter=blob:none", "origin", commit],
            cwd=path,
        )
        run(["git", "switch", "--detach", commit], cwd=path)
    ensure_clean(path)

    actual_url = run(["git", "remote", "get-url", "origin"], cwd=path)
    if actual_url != url:
        raise RuntimeError(f"远端漂移：{path} 期望 {url}，实际 {actual_url}")

    actual_commit = run(["git", "rev-parse", "HEAD"], cwd=path)
    if actual_commit != commit:
        run(
            ["git", "fetch", "--no-tags", "--depth", "1", "--filter=blob:none", "origin", commit],
            cwd=path,
        )
        run(["git", "switch", "--detach", commit], cwd=path)

    if sparse_paths:
        run(["git", "sparse-checkout", "init", "--cone"], cwd=path)
        run(["git", "sparse-checkout", "set", *sparse_paths], cwd=path)


def check_git(source: dict[str, object]) -> list[str]:
    errors: list[str] = []
    try:
        validate_git_source(source)
        path = git_repo_path(source)
    except RuntimeError as exc:
        return [str(exc)]
    if not path.is_dir():
        return [f"缺少供应链仓库：{path}"]
    try:
        ensure_clean(path)
        actual_url = run(["git", "remote", "get-url", "origin"], cwd=path)
        actual_commit = run(["git", "rev-parse", "HEAD"], cwd=path)
    except RuntimeError as exc:
        return [str(exc)]
    if actual_url != source["url"]:
        errors.append(f"远端漂移：{path}")
    if actual_commit != source["commit"]:
        errors.append(f"commit 漂移：{path} 实际 {actual_commit}")
    for relative in source.get("sparse_paths", []):
        if not (path / str(relative)).exists():
            errors.append(f"缺少 sparse path：{path / str(relative)}")
    license_path = source.get("license_path")
    if license_path:
        candidate = path / str(license_path)
        if not candidate.is_file():
            errors.append(f"缺少许可证：{candidate}")
        elif sha256(candidate) != source.get("license_sha256"):
            errors.append(f"许可证哈希漂移：{candidate}")
    return errors


def ensure_reference_shape(path: Path) -> None:
    git_dir = path / ".git"
    if git_dir.is_symlink() is True or not git_dir.is_dir():
        raise RuntimeError(f"reference 缓存不是安全的 Git 仓库：{path}")
    materialized = sorted(item.name for item in path.iterdir() if item.name != ".git")
    if materialized:
        raise RuntimeError(
            f"reference 缓存意外包含工作树：{path} -> {', '.join(materialized)}"
        )


def reference_license_sha256(
    path: Path,
    commit: str,
    license_path: str,
    *,
    allow_lazy_fetch: bool,
) -> str:
    content = run_bytes(
        ["git", "show", f"{commit}:{license_path}"],
        cwd=path,
        allow_lazy_fetch=allow_lazy_fetch,
    )
    return bytes_sha256(content)


def sync_git_reference(source: dict[str, object]) -> None:
    validate_git_reference_source(source)
    path = reference_repo_path(source)
    url = str(source["url"])
    commit = str(source["commit"])
    license_path = str(source.get("license_path", ""))
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        # Keep the reference cache empty of a worktree and fetch only the
        # lockfile commit. Never resolve the moving branch named in the lock.
        run(["git", "init", str(path)])
        run(["git", "remote", "add", "origin", url], cwd=path)
        run(
            ["git", "fetch", "--no-tags", "--depth", "1", "--filter=blob:none", "origin", commit],
            cwd=path,
        )
        run(["git", "update-ref", "refs/heads/reference-pin", commit], cwd=path)
        run(["git", "symbolic-ref", "HEAD", "refs/heads/reference-pin"], cwd=path)
    ensure_reference_shape(path)

    actual_url = run(["git", "remote", "get-url", "origin"], cwd=path)
    if actual_url != url:
        raise RuntimeError(f"远端漂移：{path} 期望 {url}，实际 {actual_url}")

    actual_commit = run(["git", "rev-parse", "HEAD"], cwd=path)
    if actual_commit != commit:
        run(
            ["git", "fetch", "--no-tags", "--depth", "1", "--filter=blob:none", "origin", commit],
            cwd=path,
        )
        run(["git", "update-ref", "refs/heads/reference-pin", commit], cwd=path)
        run(["git", "symbolic-ref", "HEAD", "refs/heads/reference-pin"], cwd=path)

    actual_commit = run(["git", "rev-parse", "HEAD"], cwd=path)
    if actual_commit != commit:
        raise RuntimeError(f"commit 固定失败：{path} 实际 {actual_commit}")
    actual_license = reference_license_sha256(
        path, commit, license_path, allow_lazy_fetch=True
    )
    if actual_license != source["license_sha256"]:
        raise RuntimeError(
            f"许可证哈希漂移：{source['id']} 实际 {actual_license}"
        )
    ensure_reference_shape(path)


def check_git_reference(source: dict[str, object]) -> list[str]:
    errors: list[str] = []
    try:
        validate_git_reference_source(source)
        path = reference_repo_path(source)
    except RuntimeError as exc:
        return [str(exc)]
    if not path.is_dir():
        return [f"缺少 reference 缓存：{path}"]
    try:
        ensure_reference_shape(path)
        actual_url = run(["git", "remote", "get-url", "origin"], cwd=path)
        actual_commit = run(["git", "rev-parse", "HEAD"], cwd=path)
        license_path = str(source.get("license_path", ""))
        actual_license = reference_license_sha256(
            path, str(source["commit"]), license_path, allow_lazy_fetch=False
        )
        if actual_license != source["license_sha256"]:
            errors.append(f"许可证哈希漂移：{source['id']}")
    except RuntimeError as exc:
        return [str(exc)]
    if actual_url != source["url"]:
        errors.append(f"远端漂移：{path}")
    if actual_commit != source["commit"]:
        errors.append(f"commit 漂移：{path} 实际 {actual_commit}")
    return errors


def check_snapshot(source: dict[str, object]) -> list[str]:
    declared = Path(str(source["source_path"]))
    if declared.is_absolute() or any(part in {".", ".."} for part in declared.parts):
        return [f"snapshot 路径必须是仓库内相对路径：{declared}"]
    lexical = ROOT
    for part in declared.parts:
        lexical = lexical / part
        if lexical.is_symlink():
            return [f"snapshot 路径不能包含 symlink：{declared}"]
    path = (ROOT / declared).resolve()
    snapshot_root = (VENDOR_ROOT / "snapshots").resolve()
    if (
        VENDOR_ROOT != ROOT / "vendor"
        or snapshot_root != VENDOR_ROOT / "snapshots"
        or (path != snapshot_root and snapshot_root not in path.parents)
    ):
        return [f"snapshot 路径越界：{path}"]
    if not path.exists():
        return [f"缺少本机 snapshot：{path}"]
    errors: list[str] = []
    exclusions = _bounded_string_list(source, "exclusions")
    expected_tree = source.get("tree_sha256")
    if expected_tree:
        try:
            actual_tree = tree_inventory(path, exclusions)["tree_sha256"]
        except (OSError, RuntimeError) as exc:
            return [str(exc)]
        if actual_tree != expected_tree:
            errors.append(f"snapshot 树摘要漂移：{path}")
    files = source.get("files")
    if isinstance(files, dict):
        for relative, expected in files.items():
            if not isinstance(relative, str) or len(relative) > MAX_PATH_CHARS:
                errors.append(f"snapshot 文件路径无效：{relative}")
                continue
            relative_path = Path(relative)
            if relative_path.is_absolute() or any(part in {".", ".."} for part in relative_path.parts):
                errors.append(f"snapshot 文件路径越界：{relative}")
                continue
            candidate = path / relative_path if path.is_dir() else path
            try:
                candidate.resolve(strict=True).relative_to(path.resolve())
                lexical = path
                for part in relative_path.parts:
                    lexical = lexical / part
                    if lexical.is_symlink():
                        raise RuntimeError("snapshot 文件不能包含 symlink")
            except (OSError, ValueError, RuntimeError) as exc:
                errors.append(f"snapshot 文件路径无效：{candidate} ({exc})")
                continue
            if not candidate.is_file():
                errors.append(f"缺少 snapshot 文件：{candidate}")
            elif not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
                errors.append(f"snapshot 哈希配置无效：{candidate}")
            elif sha256(candidate) != expected:
                errors.append(f"snapshot 哈希漂移：{candidate}")
    elif source.get("sha256"):
        if not isinstance(source["sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", source["sha256"]):
            errors.append(f"snapshot SHA-256 配置无效：{path}")
        elif not path.is_file() or sha256(path) != source["sha256"]:
            errors.append(f"snapshot 哈希漂移：{path}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="同步或检查 Vibe Mathing 供应链")
    parser.add_argument("--check", action="store_true", help="只读检查，不访问或更新远端")
    parser.add_argument(
        "--references-only",
        action="store_true",
        help="只处理 kind=git-reference 的无工作树冷缓存",
    )
    args = parser.parse_args()

    errors: list[str] = []
    for source in load_sources():
        if args.references_only and source["kind"] != "git-reference":
            continue
        source_id = str(source["id"])
        try:
            if source["kind"] == "git":
                if not args.check:
                    sync_git(source)
                errors.extend(check_git(source))
            elif source["kind"] == "git-reference":
                if not args.check:
                    sync_git_reference(source)
                errors.extend(check_git_reference(source))
            elif source["kind"] == "local-mirror":
                if not args.check:
                    sync_local_mirror(source)
                errors.extend(check_local_mirror(source))
            elif source["kind"] == "local-snapshot":
                errors.extend(check_snapshot(source))
            else:
                errors.append(f"未知供应链来源类型：{source['kind']} ({source_id})")
            print(f"{'CHECK' if args.check else 'SYNC'} {source_id}")
        except RuntimeError as exc:
            errors.append(f"{source_id}: {exc}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("供应链检查通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
