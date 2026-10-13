#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
start_convert.py

Launcher that orchestrates conversions between Excel workbooks and prompt documents
using the following conventions:

Input locations (relative to repo root):
- ./prompt_excel/  # place .xlsx files here for Excel → Docs
- ./prompt_docs/   # place prompt folders here for Docs → Excel

Output locations (under repo root, named by source file/folder mtime):
- ./prompt_docs_YYYYMMDD_HHMMSS/  # Excel → Docs results (copies of prompts/*)
- ./prompt_excel_YYYYMMDD_HHMMSS/ # Docs → Excel results (rebuilt.xlsx)

Usage:
  # Auto mode: if there are .xlsx under prompt_excel, run Excel→Docs;
  # if there is a docs set under prompt_docs, run Docs→Excel.
  python prompt-library/scripts/start_convert.py

  # Force a mode:
  python prompt-library/scripts/start_convert.py --mode excel2docs
  python prompt-library/scripts/start_convert.py --mode docs2excel

Notes:
- No interactive prompts; behavior is driven by the file presence and CLI flags
- Requires pandas, openpyxl, PyYAML (see scripts/requirements.txt)
"""
from __future__ import annotations

import argparse
import importlib.util
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import List


def ts_from_path(p: Path) -> str:
    st = p.stat()
    # Prefer creation/birth time when available; fall back to mtime
    ts = getattr(st, "st_birthtime", None)
    if ts is None:
        # On Windows, st_ctime is creation; on Linux it's inode change time
        # We still prefer mtime for consistency if birthtime is unavailable.
        ts = st.st_mtime
    # Format: YYYY_MMDD_HHMMSS per requirement example 2025_0102_2309
    return datetime.fromtimestamp(ts).strftime("%Y_%m%d_%H%M%S")


def load_module(py_path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, str(py_path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module: {py_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)  # type: ignore
    return module


def run_excel_to_docs_for_file(excel_path: Path, prompt_library_dir: Path, out_root: Path) -> Path:
    convert_path = prompt_library_dir / "scripts" / "convert_local.py"
    mod = load_module(convert_path, "convert_local")

    project_root = prompt_library_dir.parent
    # Prepare snapshot output directory under repo_root/prompt_docs/
    base_dir = out_root / "prompt_docs"
    base_dir.mkdir(parents=True, exist_ok=True)
    out_dir = base_dir / f"prompt_docs_{ts_from_path(excel_path)}"
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    converter = mod.ExcelPromptConverter(
        project_root=project_root,
        prompt_library_dir=prompt_library_dir,
        excel_path=excel_path,
        category_name="prompt-category",
        config_path=None,
        output_root=out_dir,
    )
    converter.convert()

    return out_dir


def run_docs_to_excel_for_dir(prompts_dir: Path, scripts_dir: Path, out_root: Path) -> Path:
    docs2excel_path = scripts_dir / "docs_to_excel.py"
    mod = load_module(docs2excel_path, "docs_to_excel")

    # Determine timestamp from folder creation (or mtime fallback)
    base_dir = out_root / "prompt_excel"
    base_dir.mkdir(parents=True, exist_ok=True)
    ts_fmt = ts_from_path(prompts_dir)
    out_dir = base_dir / f"prompt_excel_{ts_fmt}"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "rebuilt.xlsx"

    # Resolve actual prompts root (support either the prompts/ subfolder or direct sheet folders)
    prompts_root = prompts_dir / "prompts" if (prompts_dir / "prompts").exists() else prompts_dir
    # Invoke module's main via argparse emulation
    sys.argv = [str(docs2excel_path), "--prompts-dir", str(prompts_root), "--out", str(out_path)]
    mod.main()  # type: ignore

    return out_dir


def find_xlsx_files(input_excel_dir: Path) -> List[Path]:
    if not input_excel_dir.exists():
        return []
    return sorted([p for p in input_excel_dir.iterdir() if p.is_file() and p.suffix.lower() in {".xlsx"}], key=lambda p: p.stat().st_mtime)


def has_prompt_files(input_docs_dir: Path) -> bool:
    if not input_docs_dir.exists():
        return False
    for p in input_docs_dir.rglob("*.md"):
        if p.name.startswith("(") and ")_" in p.name:
            return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Start conversion between Excel and prompt docs")
    parser.add_argument("--mode", choices=["auto", "excel2docs", "docs2excel"], default="auto")
    parser.add_argument("--excel-dir", default="prompt_excel", help="Input directory containing .xlsx files")
    parser.add_argument("--docs-dir", default="prompt_docs", help="Input directory containing prompt folders")
    parser.add_argument("--select", type=str, default=None, help="Optional path to a specific Excel file or prompts folder to convert")
    args = parser.parse_args()

    script_path = Path(__file__).resolve()
    prompt_library_dir = script_path.parent.parent  # repo root (prompt-library)
    project_root = prompt_library_dir  # use prompt-library as root for I/O

    input_excel_dir = (prompt_library_dir / args.excel_dir).resolve()
    input_docs_dir = (prompt_library_dir / args.docs_dir).resolve()

    ran_any = False

    if args.mode in ("auto", "excel2docs"):
        # If user explicitly selected a file, prefer it
        if args.select:
            sel = Path(args.select)
            if not sel.is_absolute():
                sel = (project_root / sel).resolve()
            if sel.is_file() and sel.suffix.lower() == ".xlsx":
                out_dir = run_excel_to_docs_for_file(sel, prompt_library_dir, project_root)
                rel = out_dir.relative_to(prompt_library_dir)
                print(f"✅ Excel→Docs OK: {sel.name} → {rel}")
                ran_any = True
        else:
            xlsx_files = find_xlsx_files(input_excel_dir)
            for xlsx in xlsx_files:
                out_dir = run_excel_to_docs_for_file(xlsx, prompt_library_dir, project_root)
                rel = out_dir.relative_to(prompt_library_dir)
                print(f"✅ Excel→Docs OK: {xlsx.name} → {rel}")
                ran_any = True

    if args.mode in ("auto", "docs2excel"):
        if args.select:
            sel = Path(args.select)
            if not sel.is_absolute():
                sel = (project_root / sel).resolve()
            if sel.exists() and sel.is_dir():
                out_dir = run_docs_to_excel_for_dir(sel, prompt_library_dir / "scripts", project_root)
                rel = out_dir.relative_to(prompt_library_dir)
                # show sel relative as well when possible
                try:
                    sel_rel = Path(sel).relative_to(prompt_library_dir)
                except Exception:
                    sel_rel = Path(sel)
                print(f"✅ Docs→Excel OK: {sel_rel} → {rel}")
                ran_any = True
        else:
            if has_prompt_files(input_docs_dir):
                out_dir = run_docs_to_excel_for_dir(input_docs_dir, prompt_library_dir / "scripts", project_root)
                rel = out_dir.relative_to(prompt_library_dir)
                print(f"✅ Docs→Excel OK: {args.docs_dir} → {rel}")
                ran_any = True

    if not ran_any:
        print("ℹ️ Nothing to do. Place .xlsx under ./prompt_excel or prompt docs under ./prompt_docs, or use --mode to force.")


if __name__ == "__main__":
    main()
