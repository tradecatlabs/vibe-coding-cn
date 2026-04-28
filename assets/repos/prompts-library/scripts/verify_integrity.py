import json
import os
from collections import defaultdict

jsonl_path = "prompt_jsonl/prompt_docs_refactored.jsonl"
docs_root = "prompt_docs/prompt_docs_refactored/prompts"

def verify():
    print("=== 开始全面完整性检查 ===\n")
    
    # 1. JSONL 数据加载与基础检查
    if not os.path.exists(jsonl_path):
        print(f"❌ 错误: JSONL 文件不存在: {jsonl_path}")
        return

    data = []
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError:
                    print(f"❌ 错误: 发现无效的 JSON 行: {line[:50]}...")

    total_items = len(data)
    print(f"✅ JSONL 读取成功，共 {total_items} 条数据。")

    # 2. 规则验证
    errors = []
    categories = defaultdict(list)
    
    expected_categories = {
        "内容创作", "商业分析", "学习教育", "提示词工程", "综合杂项", "编程技术", "逻辑工具箱"
    }

    for item in data:
        cat = item.get('category')
        row = item.get('row')
        col = item.get('col')
        title = item.get('title')
        content = item.get('content')

        # 收集分类数据用于后续分析
        categories[cat].append(row)

        # 检查 1: 分类合法性
        if cat not in expected_categories:
            errors.append(f"❌ 未知分类: '{cat}' (Title: {title[:20]}...)")

        # 检查 2: 列归位 (col == 1)
        if col != 1:
            errors.append(f"❌ 列未归位: Category '{cat}', Row {row}, Col {col} (应为 1)")

        # 检查 3: 内容完整性 (简单检查)
        if not title:
            errors.append(f"⚠️ 警告: 标题为空 (Category '{cat}', Row {row})")
        if not content or len(content) < 5:
            errors.append(f"⚠️ 警告: 内容过短或为空 (Category '{cat}', Row {row}, Content len: {len(content) if content else 0})")

    # 检查 4: 行连续性
    print("\n--- 分类与行号连续性检查 ---")
    for cat, rows in categories.items():
        rows.sort()
        count = len(rows)
        if count == 0:
            print(f"⚠️ 分类 '{cat}' 为空")
            continue
            
        max_row = rows[-1]
        expected_rows = list(range(1, count + 1))
        
        status = "✅ 正常"
        if rows != expected_rows:
            status = "❌ 异常 (行号不连续或重复)"
            errors.append(f"行号错误: {cat} (Expect 1-{count}, Got max {max_row})")
        
        print(f"{cat.ljust(10)}: {count} 条 | Max Row: {max_row} | {status}")

    # 3. 文件系统同步检查
    print("\n--- 文档文件同步检查 ---")
    files_found = 0
    if os.path.exists(docs_root):
        for root, dirs, files in os.walk(docs_root):
            for file in files:
                if file.endswith(".md") and not file.startswith("index"):
                    files_found += 1
    else:
        print(f"❌ 文档目录不存在: {docs_root}")

    print(f"JSONL 条目数: {total_items}")
    print(f"Markdown 文件数: {files_found}")
    
    if total_items == files_found:
        print("✅ 文件数量一致")
    else:
        print(f"❌ 文件数量不匹配! (差值: {files_found - total_items})")
        errors.append("文件系统数量与 JSONL 不一致")

    # 4. 总结
    print("\n=== 检查总结 ===")
    if not errors:
        print("🎉 完美！所有检查通过。数据结构完整、规范。")
    else:
        print(f"发现 {len(errors)} 个问题，请检视：")
        for err in errors:
            print(err)

if __name__ == "__main__":
    verify()
