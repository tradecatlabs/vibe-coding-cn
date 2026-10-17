#!/usr/bin/env python3
"""
将 prompt_docs 目录下的 md 文件转换为 JSONL 格式

用法:
  python md_to_jsonl.py <prompt_docs目录>
  python md_to_jsonl.py prompt_docs/prompt_docs_2025_1222_004537
"""
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "prompt_jsonl"

def convert(docs_dir: Path):
    prompts_dir = docs_dir / "prompts"
    if not prompts_dir.exists():
        print(f"❌ 找不到 prompts 目录: {prompts_dir}")
        return
    
    # 输出文件名基于输入目录名
    output_file = OUTPUT_DIR / f"{docs_dir.name}.jsonl"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
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
    
    print(f"✅ 转换完成: {len(records)} 条 → {output_file}")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    docs_dir = Path(sys.argv[1])
    if not docs_dir.is_absolute():
        docs_dir = REPO_ROOT / docs_dir
    
    convert(docs_dir)

if __name__ == "__main__":
    main()
