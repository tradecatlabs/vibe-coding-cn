#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
convert_local.py

Reads a local Excel file and converts its contents into a structured prompt library
under `prompt-library/` per the development guide. It generates:
- prompts/<category>/ (one file per non-empty cell across columns for each prompt row)
- prompts/index.json (summary + traceability)
- prompts/<category>/index.md (table + version matrix)
- docs/tools.md, docs/support.md, docs/excel-data.md
- README.md (top-level for prompt-library)

Usage:
  python prompt-library/scripts/convert_local.py \
    [--excel "/absolute/or/relative/path/to/prompt (2).xlsx"] \
    [--config prompt-library/scripts/config.yaml] \
    [--category-name prompt-category]

If no arguments are provided, it will:
- load config from prompt-library/scripts/config.yaml (if present)
- resolve Excel path from config.source.excel_file relative to project root
- default category to "prompt-category"

Dependencies: pandas, openpyxl, PyYAML
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None  # Optional; script still works without YAML if no config provided


@dataclass
class RowClassification:
    row_index: int  # zero-based excel index
    kind: str  # prompt|tool|social|wallet_header|wallet|warning|other
    data: Dict


class ExcelPromptConverter:
    def __init__(
        self,
        project_root: Path,
        prompt_library_dir: Path,
        excel_path: Path,
        category_name: str = "prompt-category",
        config_path: Optional[Path] = None,
        output_root: Optional[Path] = None,
    ) -> None:
        self.project_root = project_root
        self.prompt_library_dir = prompt_library_dir
        # If an output_root is provided, write into that snapshot directory
        # rather than the in-repo prompts/docs locations.
        if output_root is not None:
            self.output_root = output_root
            self.prompts_dir = output_root / "prompts"
            self.docs_dir = output_root / "docs"
            self.readme_target_root = output_root
        else:
            self.output_root = None
            self.prompts_dir = prompt_library_dir / "prompts"
            self.docs_dir = prompt_library_dir / "docs"
            self.readme_target_root = prompt_library_dir
        self.scripts_dir = prompt_library_dir / "scripts"
        self.category_name = category_name  # fallback if single sheet
        self.category_dir = self.prompts_dir / self.category_name
        self.excel_path = excel_path
        self.config_path = config_path
        self.config = self._load_config(config_path)
        self.now = datetime.now()

        # Per-sheet prompts map: {sheet_name: {excel_row -> {title, versions{col->file}}}}
        self.prompts_info_by_sheet: Dict[str, Dict[int, Dict]] = {}
        self.tools: List[Dict] = []
        self.social: List[Dict] = []
        self.wallets: Dict[str, Dict] = {}
        self.misc: List[Dict] = []
        self.total_rows = 0
        self.total_cols = 0
        self.sheet_names_order: List[str] = []

    def _load_config(self, config_path: Optional[Path]) -> Dict:
        if config_path and config_path.exists() and yaml is not None:
            with config_path.open("r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        return {}

    def _sanitize_filename(self, text: str, max_length: int = 60) -> str:
        if not text:
            return "untitled"
        text = str(text).strip()
        text = re.sub(r"[\\/:*?\"<>|\r\n]+", "", text)
        text = text.replace(" ", "_")
        if len(text) > max_length:
            text = text[:max_length].rstrip("_-")
        return text or "untitled"

    def _extract_title(self, contents: List[str]) -> str:
        for c in contents:
            if c and c.strip():
                first_line = c.strip().splitlines()[0]
                words = first_line.split()
                candidate = " ".join(words[:6])
                return self._sanitize_filename(candidate)
        return "untitled"

    def _read_excel_sheets(self) -> Dict[str, pd.DataFrame]:
        # Read all sheets; if workbook has single sheet, still returns dict with one entry
        sheets: Dict[str, pd.DataFrame] = pd.read_excel(self.excel_path, header=None, engine="openpyxl", sheet_name=None)  # type: ignore
        normalized: Dict[str, pd.DataFrame] = {}
        for sheet_name, df in sheets.items():
            try:
                df = df.map(lambda v: v.strip() if isinstance(v, str) else v)  # pandas >=2.1
            except Exception:
                df = df.applymap(lambda v: v.strip() if isinstance(v, str) else v)  # fallback
            normalized[sheet_name] = df
        # preserve order of sheets
        self.sheet_names_order = list(normalized.keys())
        # set global rows/cols to first sheet for summary; detailed per-sheet handled later
        if normalized:
            any_df = normalized[self.sheet_names_order[0]]
            self.total_rows, self.total_cols = any_df.shape
        return normalized

    def _classify_rows(self, df: pd.DataFrame) -> List[RowClassification]:
        classifications: List[RowClassification] = []
        wallet_mode = False

        for r in range(df.shape[0]):
            row_vals = [df.iloc[r, c] if c < df.shape[1] else None for c in range(df.shape[1])]
            non_empty = [v for v in row_vals if isinstance(v, str) and v.strip()]
            any_http = any(isinstance(v, str) and v.startswith("http") for v in row_vals)

            if not non_empty:
                classifications.append(RowClassification(r, "other", {"empty": True}))
                continue

            # Wallet header detection (e.g., contains "网络" and a label like "礼貌要饭地址")
            joined = " ".join([v for v in non_empty])
            if any(k in joined for k in ["网络", "网络名称"]) and any(
                k in joined for k in ["礼貌要饭地址", "钱包", "地址"]
            ):
                wallet_mode = True
                classifications.append(RowClassification(r, "wallet_header", {"raw": row_vals}))
                continue

            if wallet_mode:
                # If the row still looks like wallet data (two columns: network, address)
                first, second = row_vals[0] if len(row_vals) > 0 else None, row_vals[1] if len(row_vals) > 1 else None
                if (first and isinstance(first, str)) and (second and isinstance(second, str)):
                    classifications.append(
                        RowClassification(
                            r,
                            "wallet",
                            {
                                "network": first,
                                "address": second,
                                "raw": row_vals,
                            },
                        )
                    )
                    continue
                else:
                    wallet_mode = False  # end wallet section if pattern breaks

            # Tools and social heuristics
            if any_http:
                url = next(v for v in row_vals if isinstance(v, str) and v.startswith("http"))
                desc = None
                for v in row_vals:
                    if v and isinstance(v, str) and not v.startswith("http"):
                        desc = v
                        break
                kind = "social" if ("x.com" in url or "twitter.com" in url) else "tool"
                classifications.append(RowClassification(r, kind, {"url": url, "description": desc or "", "raw": row_vals}))
                continue

            # Warnings or misc markers
            if any("广告位" in v for v in non_empty if isinstance(v, str)):
                classifications.append(RowClassification(r, "warning", {"content": joined, "raw": row_vals}))
                continue

            # Placeholder rows to ignore as prompts
            if any(v in {"...", "….", "...."} for v in non_empty):
                classifications.append(RowClassification(r, "other", {"placeholder": True, "raw": row_vals}))
                continue

            # Otherwise: treat as prompt row (one logical prompt per row with multiple versions across columns)
            prompt_versions: Dict[int, str] = {}
            for c in range(df.shape[1]):
                cell = df.iloc[r, c] if c < df.shape[1] else None
                if isinstance(cell, str) and cell.strip():
                    prompt_versions[c + 1] = cell.strip()
            if prompt_versions:
                classifications.append(RowClassification(r, "prompt", {"versions": prompt_versions}))
            else:
                classifications.append(RowClassification(r, "other", {"raw": row_vals}))

        return classifications

    def _ensure_dirs(self) -> None:
        self.prompts_dir.mkdir(parents=True, exist_ok=True)
        self.category_dir.mkdir(parents=True, exist_ok=True)
        self.docs_dir.mkdir(parents=True, exist_ok=True)

    def _write_prompt_file(self, row_num: int, col_num: int, title: str, content: str, versions_in_row: List[int]) -> str:
        """Write a prompt file containing ONLY the prompt text, nothing else."""
        row_col = f"({row_num},{col_num})"
        filename = f"{row_col}_{title}.md"
        filepath = self.category_dir / filename
        # Ensure content ends with newline and contains no surrounding fences/headers added by us
        pure = (content or "").rstrip("\n") + "\n"
        filepath.write_text(pure, encoding="utf-8")
        return filename

    def _generate_category_index(self, sheet_name: str, category_dir: Path, prompts_info: Dict[int, Dict]) -> None:
        index_path = category_dir / "index.md"
        total_prompts = len(prompts_info)
        total_versions = sum(len(meta["versions"]) for meta in prompts_info.values())
        avg_versions = total_versions / total_prompts if total_prompts else 0

        lines: List[str] = []
        lines.append(f"# 📂 提示词分类 - {sheet_name}（基于Excel原始数据)\n")
        lines.append(f"最后同步: {self.now.strftime('%Y-%m-%d %H:%M:%S')}\n")
        lines.append("\n## 📊 统计\n")
        lines.append(f"- 提示词总数: {total_prompts}\n")
        lines.append(f"- 版本总数: {total_versions}  \n")
        lines.append(f"- 平均版本数: {avg_versions:.1f}\n\n")
        lines.append("## 📋 提示词列表\n")
        lines.append("\n| 序号 | 标题 | 版本数 | 查看 |\n|------|------|--------|------|\n")
        for row in sorted(prompts_info.keys()):
            info = prompts_info[row]
            title = info["title"]
            versions = info["versions"]
            links = " / ".join([f"[v{v}](./({row},{v})_{title}.md)" for v in sorted(versions.keys())])
            lines.append(f"| {row} | {title} | {len(versions)} | {links} |\n")

        # Version matrix
        max_col = 0
        for info in prompts_info.values():
            if info["versions"]:
                max_col = max(max_col, max(info["versions"].keys()))
        lines.append("\n## 🗂️ 版本矩阵\n")
        header = ["行"] + [f"v{i}" for i in range(1, max_col + 1)] + ["备注"]
        lines.append("\n| " + " | ".join(header) + " |\n" + "|" + "---|" * len(header) + "\n")
        for row in sorted(prompts_info.keys()):
            info = prompts_info[row]
            row_cells = [str(row)]
            for c in range(1, max_col + 1):
                row_cells.append("✅" if c in info["versions"] else "—")
            row_cells.append("")
            lines.append("| " + " | ".join(row_cells) + " |\n")

        index_path.write_text("\n".join(lines), encoding="utf-8")

    def _generate_prompts_index_json(self) -> None:
        index_json_path = self.prompts_dir / "index.json"
        total_prompts = sum(len(p) for p in self.prompts_info_by_sheet.values())
        total_versions = sum(sum(len(meta["versions"]) for meta in p.values()) for p in self.prompts_info_by_sheet.values())
        stats = {
            "sheets": len(self.prompts_info_by_sheet),
            "prompts": total_prompts,
            "versions": total_versions,
            "tools": len(self.tools) if self.tools else 0,
            "social_accounts": len(self.social) if self.social else 0,
            "crypto_wallets": len(self.wallets) if self.wallets else 0,
        }
        categories = []
        for sheet_name in self.sheet_names_order:
            prompts_info = self.prompts_info_by_sheet.get(sheet_name, {})
            categories.append(
                {
                    "name": sheet_name,
                    "prompt_count": len(prompts_info),
                    "version_count": sum(len(meta["versions"]) for meta in prompts_info.values()),
                    "prompts": [
                        {
                            "row": row,
                            "title": info["title"],
                            "versions": sorted(list(info["versions"].keys())),
                            "files": [info["versions"][v] for v in sorted(info["versions"].keys())],
                        }
                        for row, info in sorted(prompts_info.items())
                    ],
                }
            )
        excel_data = {
            "total_rows": self.total_rows,
            "total_cols": self.total_cols,
            "sheets": list(self.prompts_info_by_sheet.keys()),
        }
        tools = {}
        if self.tools:
            for t in self.tools:
                name = t.get("name") or "tool"
                tools[name] = {k: v for k, v in t.items() if k != "name"}
        social_media = {}
        if self.social:
            for s in self.social:
                name = s.get("name") or "social"
                social_media[name] = {k: v for k, v in s.items() if k != "name"}
        support = {
            "description": "礼貌要饭地址",
            "crypto_wallets": self.wallets,
        }
        data = {
            "last_updated": self.now.strftime("%Y-%m-%dT%H:%M:%S"),
            "source": self.excel_path.name,
            "stats": stats,
            "categories": categories,
            "excel_data": excel_data,
            "tools": tools,
            "social_media": social_media,
            "support": support,
            "misc": self.misc,
        }
        index_json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def _generate_docs(self, sheets: Dict[str, pd.DataFrame]) -> None:
        # docs/excel-data.md (full table)
        excel_doc_path = self.docs_dir / "excel-data.md"
        lines: List[str] = []
        lines.append("# 📊 Excel原始数据完整记录\n")
        lines.append("## 数据来源\n")
        lines.append(f"- **文件**: {self.excel_path.name}\n")
        lines.append(f"- **处理时间**: {self.now.strftime('%Y-%m-%d')}\n")
        lines.append(f"- **工作表数量**: {len(sheets)}\n\n")
        for sheet_name, df in sheets.items():
            rows, cols = df.shape
            lines.append(f"## 工作表: {sheet_name} ({rows}行×{cols}列)\n")
            lines.append("\n| 行号 | 列1 | 列2 | 列3 |\n|-----:|-----|-----|-----|\n")
            for r in range(rows):
                c1 = df.iloc[r, 0] if cols > 0 else ""
                c2 = df.iloc[r, 1] if cols > 1 else ""
                c3 = df.iloc[r, 2] if cols > 2 else ""
                def fmt(x) -> str:
                    try:
                        if x is None or (isinstance(x, float) and pd.isna(x)) or (hasattr(pd, 'isna') and pd.isna(x)):
                            return ""
                    except Exception:
                        pass
                    s = str(x)
                    return s.replace("|", "\\|")
                lines.append(f"| {r} | {fmt(c1)} | {fmt(c2)} | {fmt(c3)} |\n")
            lines.append("\n")
        lines.append("\n---\n*完整数据提取自 {0}*\n".format(self.excel_path.name))
        excel_doc_path.write_text("\n".join(lines), encoding="utf-8")

        # docs/tools.md
        tools_path = self.docs_dir / "tools.md"
        t_lines: List[str] = []
        t_lines.append("# 🛠️ 工具与资源（从Excel提取）\n")
        if self.tools:
            t_lines.append("\n## AI优化工具\n")
            for t in self.tools:
                t_lines.append("\n### {0}\n- **URL**: {1}\n- **描述**: {2}\n- **数据来源**: Excel表格第{3}行\n".format(
                    t.get("name") or "工具",
                    t.get("url", ""),
                    t.get("description", ""),
                    (t.get("excel_row") or 0) + 1,
                ))
        if self.social:
            t_lines.append("\n## 社交媒体\n")
            for s in self.social:
                t_lines.append("\n### {0}\n- **URL**: {1}\n- **描述**: {2}\n- **数据来源**: Excel表格第{3}行\n".format(
                    s.get("name") or "社交账号",
                    s.get("url", ""),
                    s.get("description", ""),
                    (s.get("excel_row") or 0) + 1,
                ))
        t_lines.append("\n## 使用建议\n\n1. **OpenAI优化器**: 可以用来测试和改进本库中的提示词\n2. **社交媒体**: 关注获取项目更新和使用技巧\n3. **集成方式**: 可以将这些工具集成到自动化工作流中\n\n---\n*数据来源: {0}*\n".format(self.excel_path.name))
        tools_path.write_text("\n".join(t_lines), encoding="utf-8")

        # docs/support.md
        support_path = self.docs_dir / "support.md"
        s_lines: List[str] = []
        s_lines.append("# 💰 项目支持（从Excel提取）\n")
        s_lines.append("\n## 支持说明\n**礼貌要饭地址** - 如果这个项目对您有帮助，欢迎通过以下方式支持\n")
        if self.wallets:
            s_lines.append("\n## 加密货币钱包地址\n\n### 主流网络支持\n")
            s_lines.append("\n| 网络名称 | 钱包地址 | Excel行号 |\n|----------|----------|-----------|\n")
            for net, data in self.wallets.items():
                s_lines.append("| **{0}** | `{1}` | 第{2}行 |\n".format(net.upper(), data.get("address", ""), (data.get("excel_row") or 0) + 1))
        if self.misc:
            for m in self.misc:
                if m.get("type") == "warning" or "广告位" in m.get("content", ""):
                    s_lines.append("\n⚠️ **重要提醒**: {0}\n".format(m.get("content")))
        s_lines.append("\n### 使用建议\n1. 请确认钱包地址的准确性\n2. 建议小额测试后再进行大额转账\n3. 不同网络的转账费用不同，请选择合适的网络\n\n---\n*钱包地址来源: {0}*\n".format(self.excel_path.name))
        support_path.write_text("\n".join(s_lines), encoding="utf-8")

    def _generate_readme(self) -> None:
        readme_path = self.readme_target_root / "README.md"
        total_prompts = sum(len(p) for p in self.prompts_info_by_sheet.values())
        total_versions = sum(sum(len(meta["versions"]) for meta in p.values()) for p in self.prompts_info_by_sheet.values())
        readme = []
        readme.append("# 📚 提示词库（Excel转换版）\n")
        readme.append("![同步状态](https://img.shields.io/badge/status-synced-green)")
        readme.append(f"![提示词数量](https://img.shields.io/badge/prompts-{total_prompts}-blue)")
        readme.append(f"![版本总数](https://img.shields.io/badge/versions-{total_versions}-orange)")
        readme.append(f"![数据来源](https://img.shields.io/badge/source-Excel-yellow)\n")
        readme.append(f"最后更新: {self.now.strftime('%Y-%m-%d %H:%M:%S')}\n")
        readme.append("\n## 📊 总览\n")
        readme.append(f"- **数据来源**: {self.excel_path.name}\n")
        readme.append(f"- **分类数量**: {len(self.prompts_info_by_sheet)}  \n- **提示词总数**: {total_prompts}\n- **版本总数**: {total_versions}\n")
        readme.append("\n## 📂 分类导航\n")
        for i, sheet_name in enumerate(self.sheet_names_order, start=1):
            prompts_info = self.prompts_info_by_sheet.get(sheet_name, {})
            folder = f"({i})_{self._sanitize_filename(sheet_name)}"
            ver_count = sum(len(meta["versions"]) for meta in prompts_info.values())
            readme.append(f"- [{sheet_name}](./prompts/{folder}/) - {len(prompts_info)} 个提示词, {ver_count} 个版本\n")
        readme.append("\n## 🔄 同步信息\n")
        readme.append(f"- **数据源**: {self.excel_path.name}\n- **处理时间**: {self.now.strftime('%Y-%m-%d %H:%M:%S')}\n")
        readme.append("\n## 📝 许可证\n本项目采用 MIT 许可证\n")
        readme.append("\n---\n*完全基于 Excel 表格自动生成*\n")
        readme_path.write_text("\n".join(readme), encoding="utf-8")

    def convert(self) -> None:
        self._ensure_dirs()
        sheets = self._read_excel_sheets()
        # If no sheets returned (shouldn't happen), fallback to empty
        for idx, sheet_name in enumerate(self.sheet_names_order, start=1):
            df = sheets[sheet_name]
            # Prepare per-sheet folder
            folder_name = f"({idx})_{self._sanitize_filename(sheet_name)}"
            category_dir = self.prompts_dir / folder_name
            category_dir.mkdir(parents=True, exist_ok=True)

            # Classify rows
            rows = self._classify_rows(df)
            prompts_info: Dict[int, Dict] = {}

            # Build prompt files for this sheet
            for rc in rows:
                if rc.kind == "prompt":
                    excel_row_number = rc.row_index + 1
                    versions: Dict[int, str] = rc.data["versions"]
                    title = self._extract_title(list(versions.values()))
                    prompts_info[excel_row_number] = {"title": title, "versions": {}}
                    # Rewrite files directly into category_dir
                    for col_num, content in versions.items():
                        row_col = f"({excel_row_number},{col_num})"
                        filename = f"{row_col}_{title}.md"
                        (category_dir / filename).write_text((content or "").rstrip("\n") + "\n", encoding="utf-8")
                        prompts_info[excel_row_number]["versions"][col_num] = filename
                elif rc.kind == "tool":
                    url = rc.data.get("url", "")
                    self.tools.append({
                        "name": "OpenAI 提示词优化平台" if "openai" in url else "工具",
                        "url": url,
                        "description": rc.data.get("description", ""),
                        "excel_row": rc.row_index,
                        "sheet": sheet_name,
                    })
                elif rc.kind == "social":
                    url = rc.data.get("url", "")
                    name = "Twitter/X 账号" if ("x.com" in url or "twitter.com" in url) else "社交账号"
                    self.social.append({
                        "name": name,
                        "url": url,
                        "description": rc.data.get("description", ""),
                        "excel_row": rc.row_index,
                        "sheet": sheet_name,
                    })
                elif rc.kind == "wallet":
                    network = str(rc.data.get("network", "")).strip()
                    address = str(rc.data.get("address", "")).strip()
                    if network and address:
                        self.wallets[network.lower()] = {
                            "address": address,
                            "excel_row": rc.row_index,
                            "sheet": sheet_name,
                        }
                elif rc.kind == "warning":
                    self.misc.append({"type": "warning", "excel_row": rc.row_index, "content": rc.data.get("content", ""), "sheet": sheet_name})

            # Save per-sheet prompts map and index
            self.prompts_info_by_sheet[sheet_name] = prompts_info
            self._generate_category_index(sheet_name, category_dir, prompts_info)

        # Global indices and docs
        self._generate_prompts_index_json()
        self._generate_docs(sheets)
        self._generate_readme()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert local Excel into prompt library structure")
    parser.add_argument("--excel", type=str, default=None, help="Path to the Excel file (default from config)")
    parser.add_argument("--config", type=str, default=None, help="Path to config.yaml (optional)")
    parser.add_argument("--category-name", type=str, default="prompt-category", help="Output category folder name")
    parser.add_argument("--out-dir", type=str, default=None, help="Optional snapshot output root. If set, writes to <out-dir>/prompts and <out-dir>/docs")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    script_path = Path(__file__).resolve()
    prompt_library_dir = script_path.parent.parent
    project_root = prompt_library_dir.parent

    config_path = Path(args.config).resolve() if args.config else (prompt_library_dir / "scripts" / "config.yaml")

    # Resolve Excel path
    if args.excel:
        excel_path = Path(args.excel)
        if not excel_path.is_absolute():
            excel_path = (project_root / excel_path).resolve()
    else:
        # Try config
        cfg_excel = None
        if config_path.exists() and yaml is not None:
            with config_path.open("r", encoding="utf-8") as f:
                cfg = yaml.safe_load(f) or {}
                cfg_excel = ((cfg.get("source") or {}).get("excel_file") or None)
        excel_path = (project_root / cfg_excel).resolve() if cfg_excel else (project_root / "prompt (2).xlsx").resolve()

    if not excel_path.exists():
        raise FileNotFoundError(f"Excel file not found: {excel_path}")

    out_dir = Path(args.out_dir).resolve() if args.out_dir else None

    converter = ExcelPromptConverter(
        project_root=project_root,
        prompt_library_dir=prompt_library_dir,
        excel_path=excel_path,
        category_name=args.category_name,
        config_path=config_path if config_path.exists() else None,
        output_root=out_dir,
    )
    converter.convert()
    target = out_dir if out_dir else prompt_library_dir
    print(f"✅ Conversion complete. Output under: {target}")


if __name__ == "__main__":
    main()
