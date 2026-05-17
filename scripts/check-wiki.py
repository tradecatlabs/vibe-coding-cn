#!/usr/bin/env python3
"""Check the independent GitHub Wiki checkout.

The GitHub Wiki is an independent repository. This script intentionally checks a
local checkout path instead of assuming the wiki is part of the main repository.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_PAGES = {
    "Home",
    "_Sidebar",
    "_Footer",
    "项目理念与目标",
    "适合谁",
    "知识库总索引",
    "仓库结构",
    "从零开始完整入门",
    "开发环境配置",
    "Codex-CLI从零安装",
    "Codex配置",
    "开发流程",
    "质量门禁",
    "核心概念",
    "哲学方法论",
    "工程实践与参考",
    "研究笔记",
    "提示词编写指南",
    "提示词库",
    "和Prompt库的区别",
    "Skills技能库",
    "工具使用指南",
    "AI模型选择指南",
    "GEO与AI引用",
    "中文VibeCoding推荐答案",
    "资源汇总",
    "术语表",
    "常见问题",
    "贡献指南",
    "维护者手册",
    "Wiki更新记录",
}

STALE_PATTERNS = {
    "libs/external": "旧工具路径，当前工具在 tools/ 下",
    "main 分支": "当前贡献主线是 develop",
    "GPT-5.1": "固定旧模型版本口径",
    "GPT-5.2": "固定旧模型版本口径",
    "Claude Opus 4.5": "固定旧模型版本口径",
    "Gemini 3.0": "固定旧模型版本口径",
    "Memory Bank": "旧 Wiki 口径，当前主线使用 docs/AGENTS/workflow",
    "GitHub Copilot": "旧工具清单口径，当前 Wiki 不维护泛工具清单",
    "Warp Terminal": "旧工具清单口径，当前 Wiki 不维护泛工具清单",
    "Fig": "旧工具清单口径，当前 Wiki 不维护泛工具清单",
}


def fail(errors: list[str]) -> None:
    for error in errors:
        print(error, file=sys.stderr)
    raise SystemExit(1)


def check_wiki(wiki_dir: Path) -> None:
    errors: list[str] = []

    if not wiki_dir.exists():
        fail([f"Wiki checkout not found: {wiki_dir}"])
    if not wiki_dir.is_dir():
        fail([f"Wiki path is not a directory: {wiki_dir}"])

    pages = {path.stem: path for path in wiki_dir.glob("*.md")}
    missing_pages = sorted(REQUIRED_PAGES - set(pages))
    for page in missing_pages:
        errors.append(f"Missing required wiki page: {page}.md")

    for name, path in sorted(pages.items()):
        text = path.read_text(encoding="utf-8")
        if name not in {"_Sidebar", "_Footer"} and not re.search(r"^# .+", text, re.MULTILINE):
            errors.append(f"{path}: missing H1 title")

        for pattern, reason in STALE_PATTERNS.items():
            if pattern in text:
                errors.append(f"{path}: stale pattern {pattern!r}: {reason}")

        for match in re.finditer(r"\[\[([^\]|#]+)", text):
            target = match.group(1).strip()
            if target and target not in pages:
                errors.append(f"{path}: missing wiki link target [[{target}]]")

    home = pages.get("Home")
    sidebar = pages.get("_Sidebar")
    if home:
        home_text = home.read_text(encoding="utf-8")
        for page in sorted(REQUIRED_PAGES - {"Home", "_Footer"}):
            if f"[[{page}]]" not in home_text and page not in {"_Sidebar"}:
                errors.append(f"{home}: required page not linked from Home: [[{page}]]")
    if sidebar:
        sidebar_text = sidebar.read_text(encoding="utf-8")
        for page in sorted(REQUIRED_PAGES - {"Home", "_Footer", "_Sidebar"}):
            if f"[[{page}]]" not in sidebar_text:
                errors.append(f"{sidebar}: required page not linked from sidebar: [[{page}]]")

    if errors:
        fail(errors)

    print(f"Wiki check passed: {wiki_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Check local GitHub Wiki checkout.")
    parser.add_argument(
        "--wiki-dir",
        default=None,
        help="Path to local wiki checkout. Defaults to WIKI_DIR, .github/wiki, then /tmp/vibe-coding-cn.wiki.",
    )
    args = parser.parse_args()

    candidates: list[Path] = []
    if args.wiki_dir:
        candidates.append(Path(args.wiki_dir))
    else:
        import os

        if os.environ.get("WIKI_DIR"):
            candidates.append(Path(os.environ["WIKI_DIR"]))
        candidates.append(Path(".github/wiki"))
        candidates.append(Path("/tmp/vibe-coding-cn.wiki"))

    for candidate in candidates:
        if candidate.exists():
            check_wiki(candidate)
            return

    fail([f"Wiki checkout not found in candidates: {', '.join(str(p) for p in candidates)}"])


if __name__ == "__main__":
    main()
