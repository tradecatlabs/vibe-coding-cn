#!/usr/bin/env python3
"""
使用 Gemini CLI 按固定系统提示词，将指定目录下的 .md 提示词批量转换为 JSONL。

特点：
- 内置系统提示词，与《Gemini 无头模式 JSONL 规范化指引》一致
- 禁用工具调用 (--allowed-tools ''), 输出纯文本，每个文件生成一行 JSON
- 默认输入目录为仓库根下的 `2/`，输出为 `2/prompts.jsonl`

用法示例：
  python3 gemini_jsonl_batch.py
  python3 gemini_jsonl_batch.py --input 2 --output 2/prompts.jsonl --model gemini-2.5-flash
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

# ==================== 固定系统提示词 ====================
SYS_PROMPT = """{"category_id": 1, "category": "JSONL规范化", "row": 2, "col": 1, "title": "# JSONL 提示词转换器 - 系统提示词", "content": "# JSONL 提示词转换器 - 系统提示词\n\n你是一个专业 的提示词格式转换器。将用户提供的提示词内容转换为标准 JSONL 格式。\n\n## 输出格式\n\n```json\n{\\"title\\\": \\"<标题>\\", \\"content\\\": \\"<完整内容>\\"}\n```\n\n### 字段说明\n\n| 字段 | 类型 | 说明 |\n|------|------|------|\n| `title` | string | 提示词标题，取内容的第一行或前 50 字符 |\n| `content` | string | 完整的提示词内容 |\n\n## 转换规则\n\n1. **标题提取**：\n   - 若内容以 `#` 开头，取第一个标题作为 title\n   - 否则取前 50 字符（去除换行）\n2. **内容转义**：\n   - 换行符 转为 `\\\\n`\n   - 双引号转为 `\\\\\"`\n   - 反斜杠转为 `\\\\\\\\`\n\n## 输出要求\n\n- 每行一个完整的 JSON 对象\n- 不要添加任何解释、注释或额外文字\n- 不要用 ```json 代码块包裹\n- 直接输出纯 JSONL 内容\n\n## 示例\n\n### 输入\n```\n# Role：智能文档助手\n\n## Background\n用户需要一个能够处理文档的 AI 助手。\n\n## Skills\n-  文档解析\n- 格式转换\n```\n\n### 输出\n```\n{\\"title\\\": \\"# Role：智能文档助手\\", \\"content\\\": \\"# Role：智能文档助手\\\\n\\\\n## Background\\\\n用户需要一个能够处 理文档的 AI 助手。\\\\n\\\\n## Skills\\\\n- 文档解析\\\\n- 格式转换\\"}\n```\n\n---\n\n现在，请将用户提供的内容转换为标准 JSONL 格式。"}"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="使用 Gemini CLI 批量将 .md 提示词转换为 JSONL（固定系统提示词）。",
    )
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        default=Path("2"),
        help="输入目录，遍历其中的 .md 文件（默认：仓库根目录下的 2/）",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="输出 JSONL 文件路径，默认写入 <input>/prompts.jsonl",
    )
    parser.add_argument(
        "-m",
        "--model",
        default="gemini-2.5-flash",
        help="Gemini 模型名称（默认：gemini-2.5-flash）",
    )
    parser.add_argument(
        "--gemini-cmd",
        default="gemini",
        help="Gemini CLI 可执行文件名或路径（默认：gemini）",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="输出处理中的详细信息",
    )
    return parser.parse_args()


def run_gemini(content: str, model: str, cmd: str) -> str:
    """调用 Gemini CLI，将单个文本转换为一行 JSON。"""
    proc = subprocess.run(
        [
            cmd,
            "-m",
            model,
            "--output-format",
            "text",
            "--allowed-tools",
            "",
            SYS_PROMPT,
        ],
        input=content.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    stdout = proc.stdout.decode("utf-8", errors="replace").strip()
    stderr = proc.stderr.decode("utf-8", errors="replace").strip()

    if proc.returncode != 0:
        raise RuntimeError(f"Gemini 调用失败 (code={proc.returncode}): {stderr or '无错误输出'}")

    if stderr:
        # 某些 CLI 可能在 stderr 打印警告，保留但不中断
        print(f"⚠️ Gemini 警告: {stderr}", file=sys.stderr)

    if not stdout:
        raise RuntimeError("Gemini 未返回内容")

    # 去除多余行，只保留非空行并合并
    lines = [ln for ln in stdout.splitlines() if ln.strip()]
    return " ".join(lines).strip()


def main() -> None:
    args = parse_args()
    input_dir = args.input.resolve()
    if not input_dir.exists() or not input_dir.is_dir():
        print(f"❌ 输入目录不存在: {input_dir}")
        sys.exit(1)

    output_path = args.output or (input_dir / "prompts.jsonl")
    output_path = output_path.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    md_files = sorted(f for f in input_dir.iterdir() if f.suffix == ".md")
    if not md_files:
        print(f"⚠️ 未找到任何 .md 文件: {input_dir}")
        sys.exit(0)

    results = []
    for md in md_files:
        content = md.read_text(encoding="utf-8")
        if args.verbose:
            print(f"→ 处理 {md.name}")
        try:
            json_line = run_gemini(content, args.model, args.gemini_cmd)
            results.append(json_line)
        except Exception as exc:  # noqa: BLE001
            print(f"❌ 处理失败 {md.name}: {exc}", file=sys.stderr)

    with output_path.open("w", encoding="utf-8") as f:
        for line in results:
            f.write(line + "\n")

    print(f"✅ 完成：{len(results)} 条 → {output_path}")


if __name__ == "__main__":
    main()
