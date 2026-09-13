#!/usr/bin/env python3
# 做什么：校验项目级 skill 结构、来源映射、触发边界和禁止的旧工具依赖。
# 怎么运行：python3 scripts/validate_project.py
# 需要什么：Python 3；只读扫描当前项目，发现问题时非零退出。

from __future__ import annotations

import json
import os
import stat
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".codex" / "skills"
LOCK = ROOT / "vendor" / "sources.lock.json"
REQUIRED = [
    "## When to Use This Skill",
    "## Not For / Boundaries",
    "## Quick Reference",
    "## Examples",
    "## Maintenance",
]
MAX_FILE_BYTES = 5_000_000
MAX_SKILLS = 100
MAX_LOCK_SOURCES = 1_000
MAX_PATH_CHARS = 4_096


FORBIDDEN = [
    "mcp__codex__",
    "mcp__manual_review__",
    "mcp__zotero__",
    "mcp__obsidian-vault__",
    "allowed-tools: Agent",
]


def _reject_json_constant(value: str) -> object:
    raise ValueError(f"JSON 常量非法：{value}")


def _read_text(path: Path) -> str:
    path = Path(path)
    if len(str(path)) > MAX_PATH_CHARS or "\x00" in str(path) or "\\" in str(path):
        raise ValueError(f"路径超过大小预算：{path}")
    try:
        relative = path.relative_to(ROOT)
    except ValueError as exc:
        raise ValueError(f"路径越界：{path}") from exc
    lexical = ROOT
    for part in relative.parts:
        lexical = lexical / part
        if lexical.is_symlink():
            raise ValueError(f"路径不能包含 symlink：{path}")
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if nofollow is None:
        raise RuntimeError("O_NOFOLLOW unavailable; refusing project validation")
    descriptor = os.open(path, os.O_RDONLY | nofollow)
    try:
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode) or file_stat.st_size > MAX_FILE_BYTES:
            raise ValueError(f"文件超过大小预算：{path}")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(64 * 1024, MAX_FILE_BYTES - total + 1))
            if not chunk:
                return b"".join(chunks).decode("utf-8")
            total += len(chunk)
            if total > MAX_FILE_BYTES:
                raise ValueError(f"文件超过大小预算：{path}")
            chunks.append(chunk)
    finally:
        os.close(descriptor)


def frontmatter_value(text: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*[\"']?([^\n\"']+)", text)
    return match.group(1).strip() if match else None


def main() -> int:
    errors: list[str] = []
    if (
        ROOT.is_symlink()
        or ROOT.resolve() != ROOT
        or LOCK.is_symlink()
        or SKILLS.is_symlink()
        or any(parent.is_symlink() for parent in ROOT.parents)
    ):
        raise ValueError("项目关键路径不能是 symlink")
    lock = json.loads(_read_text(LOCK), parse_constant=_reject_json_constant)
    if (
        not isinstance(lock, dict)
        or not isinstance(lock.get("sources"), list)
        or len(lock["sources"]) > MAX_LOCK_SOURCES
    ):
        raise ValueError("供应链 lockfile 结构无效")
    source_ids: set[str] = set()
    for source in lock["sources"]:
        if not isinstance(source, dict) or not isinstance(source.get("id"), str):
            raise ValueError("供应链 lockfile source entry 无效")
        if source["id"] in source_ids:
            raise ValueError("供应链 lockfile source ID 重复")
        source_ids.add(source["id"])
    skill_dirs = sorted(
        path for path in SKILLS.iterdir()
        if path.is_symlink()
    )
    if skill_dirs:
        raise ValueError("active skill 目录不能是 symlink")
    skill_dirs = sorted(
        path for path in SKILLS.iterdir()
        if path.is_dir()
    )
    if len(skill_dirs) > MAX_SKILLS:
        raise ValueError("active skill 数量超过上限")

    for skill_dir in skill_dirs:
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"缺少 SKILL.md：{skill_dir}")
            continue
        text = _read_text(skill_file)
        name = frontmatter_value(text, "name")
        if name != skill_dir.name or not re.fullmatch(r"[a-z][a-z0-9-]*", name or ""):
            errors.append(f"skill 名称不匹配：{skill_dir} -> {name}")
        for heading in REQUIRED:
            if heading not in text:
                errors.append(f"{skill_dir.name} 缺少章节：{heading}")
        if text.count("### Example ") < 3:
            errors.append(f"{skill_dir.name} 缺少 3 个可复现实例")
        for filename in [
            "VERSION",
            "CHANGELOG.md",
            "references/index.md",
            "references/source-map.md",
            "references/pressure-tests.md",
        ]:
            if not (skill_dir / filename).is_file():
                errors.append(f"{skill_dir.name} 缺少 {filename}")
        for token in FORBIDDEN:
            if token in text:
                errors.append(f"{skill_dir.name} 含禁止的不可用依赖：{token}")
        source_map = skill_dir / "references" / "source-map.md"
        if source_map.is_file() and skill_dir.name != "vibe-mathing-router":
            mapped = _read_text(source_map)
            if not any(source_id in mapped for source_id in source_ids):
                errors.append(f"{skill_dir.name} 未映射 lockfile 来源")

    expected = {
        "vibe-mathing-router", "math-discovery", "math-derivation",
        "math-computation", "math-proof", "math-formalization",
    }
    actual = {path.name for path in skill_dirs}
    if actual != expected:
        errors.append(f"active skill 集合漂移：期望 {sorted(expected)}，实际 {sorted(actual)}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"项目校验通过：{len(skill_dirs)} 个 active skills")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValueError, TypeError, KeyError, UnicodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
