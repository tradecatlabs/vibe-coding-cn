import json
import re

jsonl_file = "prompt_jsonl/prompt_docs_refactored.jsonl"
report = []

def check_md_syntax(text, info_str):
    lines = text.split('\n')
    errors = []
    
    # 1. 检查分隔符 (--- 或 ***)
    # 规范：应独占一行，前后建议有空行
    # 正则匹配：行首开始，至少3个-或*，行尾结束，允许行尾有空白
    separator_pattern = re.compile(r'^\s*([-*]{3,})\s*$')
    
    # 2. 检查标题 (#)
    # 规范：#后必须有空格
    header_pattern = re.compile(r'^(#+)([^ \n].*)') # 捕获 #后紧跟非空格的

    # 3. 代码块 (```)
    code_block_count = 0
    
    for i, line in enumerate(lines):
        # 检查分隔符
        if separator_pattern.match(line):
            # 检查长度（虽然md规范>=3即可，但有些习惯是用3个）
            # 检查前后空行（非强制，但推荐）
            pass # 暂时只检查基本正则，如果夹杂在文本中通常不会独占一行

        # 检查错误标题： #Title
        m = header_pattern.match(line)
        if m:
            # 排除掉特殊的Shebang或注释，比如 #!/bin/bash 或 #_Role (这个文件里的Title字段用了#_)
            # 但这里是content字段，应该遵循MD规范
            # 检查是否在代码块内
            if code_block_count % 2 == 0:
                # 忽略一些特定的meta标记，比如 # Role (有些prompt习惯)
                # 实际上标准MD里 #Role 也是不规范的标题
                # 允许一些特殊情况? 暂时严格检查
                errors.append(f"Line {i+1}: 标题格式可能错误 (缺少空格): '{line[:20]}...'" )

        # 检查代码块闭合
        if line.strip().startswith('```'):
            code_block_count += 1
    
    if code_block_count % 2 != 0:
        errors.append("代码块 (```) 未闭合")
        
    if errors:
        report.append(f"\n📄 {info_str}")
        for e in errors:
            report.append(f"  - {e}")

def analyze():
    print("正在检查 Markdown 语法...")
    try:
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                if not line.strip(): continue
                try:
                    item = json.loads(line)
                except json.JSONDecodeError:
                    print(f"❌ JSON 解析错误在第 {line_num} 行")
                    continue
                
                cat = item.get('category', 'Unknown')
                row = item.get('row', '?')
                title = item.get('title', 'No Title')
                content = item.get('content', '')
                
                if not content:
                    report.append(f"\n⚠️ {cat} | Row {row} | {title}: 内容为空")
                    continue
                
                info = f"[{cat}] Row {row}: {title}"
                check_md_syntax(content, info)
                
    except FileNotFoundError:
        print("文件未找到")
        return

    if not report:
        print("✅ 未发现明显的 Markdown 语法问题。  ")
    else:
        print(f"⚠️ 发现潜在问题 ({len(report)} 处):")
        for msg in report:
            print(msg)

if __name__ == "__main__":
    analyze()
