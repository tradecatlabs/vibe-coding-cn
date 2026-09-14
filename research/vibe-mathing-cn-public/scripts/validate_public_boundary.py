#!/usr/bin/env python3
"""Validate that the current Git tree is safe for the public repository."""

from __future__ import annotations

import argparse
import json
import os
import stat
import re
import subprocess
import sys
from pathlib import Path

from vibe_mathing.runtime import RuntimeErrorBase, execute_bounded

sys.dont_write_bytecode = True
BOUNDARY_COMMAND_TIMEOUT_SECONDS = 30
MAX_COMMAND_OUTPUT_BYTES = 8_000_000
MAX_TRACKED_FILE_BYTES = 128_000_000
PUBLIC_ORIGINS = {
    # actions/checkout configures the HTTPS form without `.git`; developer
    # clones may retain `.git`. Keep both exact identities rather than
    # weakening the repository boundary to suffix matching.
    "https://github.com/vibemathing/vibe-mathing-cn-public",
    "https://github.com/vibemathing/vibe-mathing-cn-public.git",
    "git@github.com:vibemathing/vibe-mathing-cn-public.git",
}

FORBIDDEN_PATH_PATTERNS = (
    re.compile(r"^governance/tasks/001[0-5]-millennium-"),
    re.compile(r"^governance/tasks/millennium-goals/"),
    re.compile(r"^governance/verification/ledger/"),
    re.compile(r"^research/artifacts/(?!README\.md$)"),
    re.compile(r"^research/runs/"),
    re.compile(r"(^|/)RECOVERY_MANIFEST\.json$"),
)
FORBIDDEN_SUFFIXES = (
    ".olean",
    ".pyc",
    ".log",
    ".pdf",
    ".sqlite",
    ".sqlite3",
    ".db",
    ".bin",
    ".zip",
    ".tar",
    ".tgz",
    ".gz",
    ".zst",
    ".7z",
    ".safetensors",
)

# Build sensitive literals in pieces so the validator does not flag its own source.
PRIVATE_REPOSITORY_NAME = b"vibe-mathing-cn-" + b"internal"
USER_PROJECT_PATH = re.compile(b"/" + b"home" + rb"/[^/]+/\.projects/vibe-mathing-cn(?:/|\b)")
WSL_UNC_PATH = re.compile(rb"\\\\wsl(?:\.localhost|\$)\\", re.IGNORECASE)
PRIVATE_IPV4 = re.compile(
    rb"(?<![A-Za-z0-9.-])(?:10\.(?:\d{1,3}\.){2}\d{1,3}|192\.168\.(?:\d{1,3}\.)\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.(?:\d{1,3}\.)\d{1,3})(?![A-Za-z0-9.-])"
)
SESSION_IDENTIFIER = re.compile(
    rb"\b(?:" + b"01" + rb"[a-f0-9]{6,}|" + b"019" + rb"[a-f0-9]{6,})-[a-f0-9-]{20,}\b",
    re.IGNORECASE,
)
CREDENTIAL_PATTERNS = {
    "private_key": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----"),
    "bearer_token": re.compile(rb"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{16,}"),
    "github_token": re.compile(rb"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}\b"),
    "openai_like_key": re.compile(rb"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "aws_access_key": re.compile(rb"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
}


def _safe_environment() -> dict[str, str]:
    allowed = {"PATH", "HOME", "LANG", "LC_ALL", "TMPDIR"}
    environment = {
        key: value for key, value in os.environ.items() if key in allowed
    }
    environment["PATH"] = environment.get("PATH", "/usr/local/bin:/usr/bin:/bin")
    return environment


def run_git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    argv = ["git", "-C", str(root), *args]
    try:
        result = execute_bounded(
            argv,
            cwd=root,
            timeout_seconds=BOUNDARY_COMMAND_TIMEOUT_SECONDS,
            max_output_bytes=MAX_COMMAND_OUTPUT_BYTES,
            memory_budget_mb=512,
            threads_max=1,
            env=_safe_environment(),
        )
    except RuntimeErrorBase as exc:
        raise RuntimeError(f"git boundary command failed: {exc}") from exc
    completed = subprocess.CompletedProcess(
        argv,
        result["exit_code"],
        result["stdout"].encode("utf-8", "replace"),
        result["stderr"].encode("utf-8", "replace"),
    )
    if check and completed.returncode != 0:
        raise RuntimeError(f"git boundary command exited with {completed.returncode}")
    return completed


def read_tracked_file(path: Path) -> bytes:
    if (
        not path.is_absolute()
        or len(str(path)) > 4_096
        or "\x00" in str(path)
        or "\\" in str(path)
    ):
        raise RuntimeError("tracked path is invalid")
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise RuntimeError("O_NOFOLLOW unavailable; refusing boundary scan")
    descriptor = os.open(path, os.O_RDONLY | nofollow)
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode):
            raise RuntimeError("tracked path is not a regular file")
        if file_stat.st_size > MAX_TRACKED_FILE_BYTES:
            raise RuntimeError("tracked file exceeds boundary size budget")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(64 * 1024, MAX_TRACKED_FILE_BYTES - total + 1))
            if not chunk:
                return b"".join(chunks)
            total += len(chunk)
            if total > MAX_TRACKED_FILE_BYTES:
                raise RuntimeError("tracked file exceeds boundary size budget")
            chunks.append(chunk)
    finally:
        os.close(descriptor)


def forbidden_path(path: str) -> bool:
    lower = path.lower()
    return lower.endswith(FORBIDDEN_SUFFIXES) or any(pattern.search(path) for pattern in FORBIDDEN_PATH_PATTERNS)


def content_findings(data: bytes) -> list[str]:
    findings: list[str] = []
    if PRIVATE_REPOSITORY_NAME in data:
        findings.append("private_repository_name")
    if USER_PROJECT_PATH.search(data):
        findings.append("absolute_user_project_path")
    if WSL_UNC_PATH.search(data):
        findings.append("wsl_unc_path")
    if PRIVATE_IPV4.search(data):
        findings.append("private_ipv4")
    if SESSION_IDENTIFIER.search(data):
        findings.append("session_identifier")
    for name, pattern in CREDENTIAL_PATTERNS.items():
        if pattern.search(data):
            findings.append(name)
    return findings


def validate(root: Path) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    if (
        not root.is_absolute()
        or len(str(root)) > 4_096
        or "\x00" in str(root)
        or "\\" in str(root)
        or root.is_symlink()
        or not root.is_dir()
        or root.resolve() != root
        or any(parent.is_symlink() for parent in [root.parent, *root.parents])
    ):
        return [{"code": "unsafe_project_root", "path": str(root), "message": "public root is not a regular directory"}]
    git_path = root / ".git"
    if (
        git_path.is_symlink()
        or not git_path.is_dir()
        or git_path.resolve() != git_path
    ):
        return [{"code": "not_git_repository", "path": str(root), "message": "public root is not a Git repository"}]

    origin = run_git(root, "remote", "get-url", "origin", check=False)
    if origin.returncode != 0:
        issues.append({"code": "missing_public_origin", "path": "origin", "message": "public repository origin is missing"})
    elif origin.stdout.decode().strip() not in PUBLIC_ORIGINS:
        issues.append({"code": "wrong_public_origin", "path": "origin", "message": "origin is not the public repository"})
    remotes = run_git(root, "remote").stdout.decode().splitlines()
    for remote in remotes:
        url = run_git(root, "remote", "get-url", remote, check=False).stdout
        if PRIVATE_REPOSITORY_NAME in url:
            issues.append({"code": "private_remote_configured", "path": remote, "message": "public repository has a private remote"})

    tracked = [item.decode("utf-8", "surrogateescape") for item in run_git(root, "ls-files", "-z").stdout.split(b"\0") if item]
    for relative in tracked:
        if forbidden_path(relative):
            issues.append({"code": "forbidden_public_path", "path": relative, "message": "path is not publishable"})
            continue
        relative_path = Path(relative)
        if (
            relative_path.is_absolute()
            or any(part in {".", ".."} for part in relative_path.parts)
            or "\\" in relative
            or "\x00" in relative
        ):
            issues.append({"code": "unsafe_tracked_path", "path": relative, "message": "tracked path escapes public root"})
            continue
        path = root / relative_path
        lexical = root
        if any(
            (lexical := lexical / part).is_symlink()
            for part in relative_path.parts
        ):
            issues.append({"code": "public_symlink", "path": relative, "message": "tracked path contains a symlink"})
            continue
        if path.is_symlink():
            issues.append({"code": "public_symlink", "path": relative, "message": "tracked symlinks are not allowed"})
            continue
        try:
            data = read_tracked_file(path)
        except OSError as error:
            issues.append({"code": "unreadable_tracked_file", "path": relative, "message": str(error)})
            continue
        if b"\0" in data:
            issues.append({"code": "unclassified_binary", "path": relative, "message": "binary tracked file is not allowlisted"})
            continue
        for finding in content_findings(data):
            issues.append({"code": finding, "path": relative, "message": "sensitive content pattern found"})
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()
    project_root = Path(os.path.abspath(args.project_root))
    issues = validate(project_root)
    payload = {"decision": "PASS" if not issues else "BLOCK", "issue_count": len(issues), "issues": issues}
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False))
    else:
        print(f"Public repository boundary: {payload['decision']}")
        for issue in issues:
            print(f"- {issue['code']} {issue['path']}: {issue['message']}")
    return 0 if not issues else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"Public repository boundary: BLOCK\n- boundary_error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
