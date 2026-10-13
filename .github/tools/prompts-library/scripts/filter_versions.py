import json
import shutil
from collections import defaultdict

input_file = "prompt_jsonl/prompt_docs_refactored.jsonl"
output_file = "prompt_jsonl/prompt_docs_refactored_clean.jsonl"
backup_file = "prompt_jsonl/prompt_docs_refactored.jsonl.bak"

def filter_versions():
    # 1. Backup
    shutil.copy(input_file, backup_file)
    print(f"Backup created: {backup_file}")

    # 2. Group by (category, row) and find max col
    latest_versions = {} # Key: (category, row), Value: item_dict
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip(): continue
            item = json.loads(line)
            
            cat = item.get('category', 'Uncategorized')
            row = item.get('row', 0)
            col = item.get('col', 0)
            
            key = (cat, row)
            
            if key not in latest_versions:
                latest_versions[key] = item
            else:
                # If current item has higher col, replace it
                if col > latest_versions[key].get('col', 0):
                    latest_versions[key] = item

    # 3. Write filtered data
    count = 0
    with open(output_file, 'w', encoding='utf-8') as f:
        # Sort by category then row for tidiness
        sorted_keys = sorted(latest_versions.keys(), key=lambda x: (x[0], x[1]))
        for key in sorted_keys:
            item = latest_versions[key]
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
            count += 1
            
    print(f"Filtered file written: {output_file}")
    print(f"Total prompts retained: {count}")
    
    # Overwrite original for downstream scripts
    shutil.move(output_file, input_file)
    print(f"Overwritten original file: {input_file}")

if __name__ == "__main__":
    filter_versions()
