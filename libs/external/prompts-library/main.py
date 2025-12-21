#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
main.py

Unified controller for prompt-library conversions.

支持的转换模式
==============
1. Excel → Docs    : 将 Excel 工作簿转换为 Markdown 文档目录
2. Docs → Excel    : 将 Markdown 文档目录还原为 Excel 工作簿
3. Docs → JSONL    : 将 Markdown 文档转换为 JSONL 格式（保留完整元信息）
4. JSONL → Excel   : 将 JSONL 转换为 Excel（单元格存储 JSON 对象）

数据格式规范
============
Excel 结构:
  - 每个工作表(sheet) = 一个分类(category)
  - 行(row) = 不同提示词
  - 列(col) = 版本迭代

Docs 结构:
  - prompts/(N)_分类名/           # N = category_id
  - prompts/(N)_分类名/(r,c)_标题.md  # r=row, c=col

JSONL 格式 (每行一个 JSON 对象):
  {
    "category_id": 2,        # 分类编号
    "category": "元提示词",   # 分类名称  
    "row": 1,                # 原 Excel 行号
    "col": 1,                # 原 Excel 列号（版本号）
    "title": "...",          # 标题（截断80字符）
    "content": "..."         # 完整内容
  }

JSONL → Excel 单元格格式:
  {"title": "...", "content": "..."}  # 只保留 title 和 content

目录约定
========
- Excel 源文件: ./prompt_excel/
- Docs 源目录:  ./prompt_docs/
- JSONL 文件:   ./prompt_jsonl/
- 输出:
  - Excel→Docs: ./prompt_docs/prompt_docs_YYYY_MMDD_HHMMSS/
  - Docs→Excel: ./prompt_excel/prompt_excel_YYYY_MMDD_HHMMSS/rebuilt.xlsx
  - Docs→JSONL: ./prompt_jsonl/{docs_name}.jsonl
  - JSONL→Excel: ./prompt_excel/{jsonl_name}.xlsx

使用示例
========
  # 交互式选择
  python3 main.py

  # Excel → Docs
  python3 main.py --select "prompt_excel/prompt.xlsx"

  # Docs → Excel
  python3 main.py --select "prompt_docs/prompt_docs_2025_1222"

  # Docs → JSONL
  python3 main.py --select "prompt_docs/prompt_docs_2025_1222" --mode docs2jsonl

  # JSONL → Excel
  python3 main.py --select "prompt_jsonl/prompt_docs.jsonl"
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

# Optional Rich UI imports (fallback to plain if unavailable)
try:
    from rich.console import Console
    from rich.layout import Layout
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich import box
    from rich.prompt import IntPrompt
    _RICH_AVAILABLE = True
except Exception:  # pragma: no cover
    _RICH_AVAILABLE = False

# Optional InquirerPy for arrow-key selection
try:
    from InquirerPy import inquirer as _inq
    _INQUIRER_AVAILABLE = True
except Exception:  # pragma: no cover
    _INQUIRER_AVAILABLE = False


@dataclass
class Candidate:
    index: int
    kind: str  # "excel" | "docs" | "docs2jsonl" | "jsonl"
    path: Path
    label: str


def get_repo_root() -> Path:
    return Path(__file__).resolve().parent


def list_excel_files(excel_dir: Path) -> List[Path]:
    if not excel_dir.exists():
        return []
    return sorted([p for p in excel_dir.iterdir() if p.is_file() and p.suffix.lower() == ".xlsx"], key=lambda p: p.stat().st_mtime)


def has_prompt_files(directory: Path) -> bool:
    if not directory.exists():
        return False
    # Detect files like "(r,c)_*.md" anywhere under the directory
    for file_path in directory.rglob("*.md"):
        name = file_path.name
        if name.startswith("(") and ")_" in name:
            return True
    return False


def list_doc_sets(docs_dir: Path) -> List[Path]:
    results: List[Path] = []
    if not docs_dir.exists():
        return results
    # If the docs_dir itself looks like a set, include it
    if has_prompt_files(docs_dir):
        results.append(docs_dir)
    # Also include any immediate children that look like a docs set
    for child in sorted(docs_dir.iterdir()):
        if child.is_dir() and has_prompt_files(child):
            results.append(child)
    return results


def run_start_convert(start_convert: Path, mode: str, project_root: Path, select_path: Optional[Path] = None, excel_dir: Optional[Path] = None, docs_dir: Optional[Path] = None) -> int:
    """Delegate to scripts/start_convert.py with appropriate flags."""
    python_exe = sys.executable
    cmd: List[str] = [python_exe, str(start_convert), "--mode", mode]
    if select_path is not None:
        # Always pass as repo-root-relative or absolute string
        cmd.extend(["--select", str(select_path)])
    if excel_dir is not None:
        cmd.extend(["--excel-dir", str(excel_dir)])
    if docs_dir is not None:
        cmd.extend(["--docs-dir", str(docs_dir)])

    # Execute in repo root to ensure relative defaults resolve correctly
    proc = subprocess.run(cmd, cwd=str(project_root))
    return proc.returncode


def run_docs_to_jsonl(docs_path: Path, project_root: Path) -> int:
    """Convert docs folder to JSONL format."""
    import json
    import re
    
    prompts_dir = docs_path / "prompts"
    if not prompts_dir.exists():
        print(f"❌ 找不到 prompts 目录: {prompts_dir}")
        return 1
    
    output_dir = project_root / "prompt_jsonl"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{docs_path.name}.jsonl"
    
    records = []
    for category_dir in sorted(prompts_dir.iterdir()):
        if not category_dir.is_dir():
            continue
        
        m = re.match(r'\((\d+)\)_(.+)', category_dir.name)
        cat_id, cat_name = (m.groups() if m else (0, category_dir.name))
        
        for md_file in sorted(category_dir.glob("*.md")):
            if md_file.name == "index.md":
                continue
            
            fm = re.match(r'\((\d+),(\d+)\)_(.+)\.md', md_file.name)
            if not fm:
                continue
            
            row, col, title = fm.groups()
            content = md_file.read_text(encoding='utf-8')
            
            records.append({
                "category_id": int(cat_id),
                "category": cat_name,
                "row": int(row),
                "col": int(col),
                "title": title[:80],
                "content": content
            })
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    
    print(f"✅ Docs→JSONL OK: {docs_path.name} → {output_file.relative_to(project_root)}")
    return 0


def list_jsonl_files(jsonl_dir: Path) -> List[Path]:
    if not jsonl_dir.exists():
        return []
    return sorted([p for p in jsonl_dir.iterdir() if p.is_file() and p.suffix.lower() == ".jsonl"], key=lambda p: p.stat().st_mtime)


def run_jsonl_to_excel(jsonl_path: Path, project_root: Path) -> int:
    """Convert JSONL to Excel, each cell contains the full JSON object as string."""
    import json
    from collections import defaultdict
    try:
        import pandas as pd
    except ImportError:
        print("❌ 需要 pandas: pip install pandas openpyxl")
        return 1
    
    records = []
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    
    if not records:
        print(f"❌ JSONL 文件为空: {jsonl_path}")
        return 1
    
    # category -> {row -> {col -> json_string}}
    sheets_data: dict = defaultdict(lambda: defaultdict(dict))
    cat_id_map = {}
    
    for r in records:
        cat_name = r["category"]
        cat_id_map[r["category_id"]] = cat_name
        # 单元格内容只保留 title 和 content
        cell_data = {"title": r["title"], "content": r["content"]}
        sheets_data[cat_name][r["row"]][r["col"]] = json.dumps(cell_data, ensure_ascii=False)
    
    output_dir = project_root / "prompt_excel"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{jsonl_path.stem}.xlsx"
    
    sorted_cats = sorted(cat_id_map.items(), key=lambda x: x[0])
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        for cat_id, cat_name in sorted_cats:
            row_data = sheets_data[cat_name]
            if not row_data:
                continue
            
            max_row = max(row_data.keys())
            max_col = max(c for cols in row_data.values() for c in cols.keys())
            
            data = []
            for row_idx in range(1, max_row + 1):
                row_list = []
                for col_idx in range(1, max_col + 1):
                    row_list.append(row_data.get(row_idx, {}).get(col_idx, ""))
                data.append(row_list)
            
            df = pd.DataFrame(data)
            sheet_name = cat_name[:31]
            df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)
    
    print(f"✅ JSONL→Excel OK: {jsonl_path.name} → {output_file.relative_to(project_root)} ({len(sorted_cats)} 个工作表)")
    return 0


def build_candidates(project_root: Path, excel_dir: Path, docs_dir: Path) -> List[Candidate]:
    candidates: List[Candidate] = []
    idx = 1
    jsonl_dir = project_root / "prompt_jsonl"
    
    for path in list_excel_files(excel_dir):
        label = f"{path.name}"
        candidates.append(Candidate(index=idx, kind="excel", path=path, label=label))
        idx += 1
    for path in list_doc_sets(docs_dir):
        display = path.relative_to(project_root) if path.is_absolute() else path
        # Docs → Excel
        candidates.append(Candidate(index=idx, kind="docs", path=path, label=f"{display}"))
        idx += 1
        # Docs → JSONL
        candidates.append(Candidate(index=idx, kind="docs2jsonl", path=path, label=f"{display}"))
        idx += 1
    for path in list_jsonl_files(jsonl_dir):
        label = f"{path.name}"
        candidates.append(Candidate(index=idx, kind="jsonl", path=path, label=label))
        idx += 1
    return candidates


def select_interactively(candidates: Sequence[Candidate]) -> Optional[Candidate]:
    if not candidates:
        print("没有可用的 Excel 或 Docs 源。请将 .xlsx 放到 prompt_excel/ 或将文档放到 prompt_docs/ 下。")
        return None

    # Prefer arrow-key selection if available
    if _INQUIRER_AVAILABLE:
        try:
            choices = [
                {"name": f"[{c.kind.upper()}] {c.label}", "value": c.index}
                for c in candidates
            ]
            selection = _inq.select(
                message="选择要转换的源（上下箭头，回车确认，Ctrl+C 取消）:",
                choices=choices,
                default=choices[0]["value"],
            ).execute()
            match = next((c for c in candidates if c.index == selection), None)
            return match
        except KeyboardInterrupt:
            return None

    if _RICH_AVAILABLE:
        console = Console()
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="list"),
            Layout(name="footer", size=3),
        )
        header = Panel(Text("提示词库转换器", style="bold cyan"), subtitle="选择一个源开始转换", box=box.ROUNDED)

        table = Table(box=box.SIMPLE_HEAVY)
        table.add_column("编号", style="bold yellow", justify="right", width=4)
        table.add_column("类型", style="magenta", width=12)
        table.add_column("路径/名称", style="white")
        kind_labels = {"excel": "Excel→Docs", "docs": "Docs→Excel", "docs2jsonl": "Docs→JSONL", "jsonl": "JSONL→Excel"}
        for c in candidates:
            table.add_row(str(c.index), kind_labels.get(c.kind, c.kind), c.label)

        layout["header"].update(header)
        layout["list"].update(Panel(table, title="可选源", border_style="cyan"))
        layout["footer"].update(Panel(Text("输入编号并回车（0 退出）", style="bold"), box=box.ROUNDED))
        console.print(layout)

        while True:
            try:
                choice = IntPrompt.ask("编号", default=0)
            except Exception:
                return None
            if choice == 0:
                return None
            match = next((c for c in candidates if c.index == choice), None)
            if match is not None:
                return match
            console.print("[red]编号不存在，请重试[/red]")

    # Plain fallback
    kind_labels = {"excel": "Excel→Docs", "docs": "Docs→Excel", "docs2jsonl": "Docs→JSONL", "jsonl": "JSONL→Excel"}
    print("请选择一个源进行转换：")
    for c in candidates:
        print(f"  {c.index:2d}. [{kind_labels.get(c.kind, c.kind)}] {c.label}")
    print("  0. 退出")
    while True:
        try:
            raw = input("输入编号后回车：").strip()
        except EOFError:
            return None
        if not raw:
            continue
        if raw == "0":
            return None
        if not raw.isdigit():
            print("请输入有效数字。")
            continue
        choice = int(raw)
        match = next((c for c in candidates if c.index == choice), None)
        if match is None:
            print("编号不存在，请重试。")
            continue
        return match


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="prompt-library conversion controller")
    p.add_argument("--excel-dir", type=str, default="prompt_excel", help="Excel sources directory (default: prompt_excel)")
    p.add_argument("--docs-dir", type=str, default="prompt_docs", help="Docs sources directory (default: prompt_docs)")
    p.add_argument("--select", type=str, default=None, help="Path to a specific .xlsx file or a docs folder")
    p.add_argument("--mode", type=str, choices=["excel2docs", "docs2excel", "docs2jsonl", "jsonl2excel"], default=None, help="Conversion mode (auto-detect if not specified)")
    p.add_argument("--non-interactive", action="store_true", help="Do not prompt; require --select or exit")
    return p.parse_args()


def main() -> int:
    repo_root = get_repo_root()
    start_convert = repo_root / "scripts" / "start_convert.py"
    if not start_convert.exists():
        print("找不到 scripts/start_convert.py。")
        return 1

    args = parse_args()

    excel_dir = (repo_root / args.excel_dir).resolve() if not Path(args.excel_dir).is_absolute() else Path(args.excel_dir).resolve()
    docs_dir = (repo_root / args.docs_dir).resolve() if not Path(args.docs_dir).is_absolute() else Path(args.docs_dir).resolve()

    # Non-interactive path with explicit selection
    if args.non_interactive or args.select:
        if not args.select:
            print("--non-interactive 需要配合 --select 使用。")
            return 2
        selected = Path(args.select)
        if not selected.is_absolute():
            selected = (repo_root / selected).resolve()
        if not selected.exists():
            print(f"选择的路径不存在: {selected}")
            return 2
        if selected.is_file() and selected.suffix.lower() == ".xlsx":
            return run_start_convert(start_convert, mode="excel2docs", project_root=repo_root, select_path=selected, excel_dir=excel_dir)
        if selected.is_file() and selected.suffix.lower() == ".jsonl":
            return run_jsonl_to_excel(selected, repo_root)
        if selected.is_dir():
            # Check mode or default to docs2excel
            if args.mode == "docs2jsonl":
                return run_docs_to_jsonl(selected, repo_root)
            return run_start_convert(start_convert, mode="docs2excel", project_root=repo_root, select_path=selected, docs_dir=docs_dir)
        print("无法识别的选择类型。")
        return 2

    # Interactive selection
    candidates = build_candidates(repo_root, excel_dir, docs_dir)
    chosen = select_interactively(candidates)
    if chosen is None:
        return 0
    if chosen.kind == "excel":
        return run_start_convert(start_convert, mode="excel2docs", project_root=repo_root, select_path=chosen.path, excel_dir=excel_dir)
    elif chosen.kind == "docs2jsonl":
        return run_docs_to_jsonl(chosen.path, repo_root)
    elif chosen.kind == "jsonl":
        return run_jsonl_to_excel(chosen.path, repo_root)
    else:
        return run_start_convert(start_convert, mode="docs2excel", project_root=repo_root, select_path=chosen.path, docs_dir=docs_dir)


if __name__ == "__main__":
    sys.exit(main())
