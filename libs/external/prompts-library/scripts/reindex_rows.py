import json
import shutil
from collections import defaultdict

input_file = "prompt_jsonl/prompt_docs_refactored.jsonl"
output_file = "prompt_jsonl/prompt_docs_refactored_reindexed.jsonl"
backup_file = "prompt_jsonl/prompt_docs_refactored_before_reindex.jsonl.bak"

def reindex_rows():
    # 1. Backup
    shutil.copy(input_file, backup_file)
    print(f"Backup created: {backup_file}")

    # 2. Load and Group
    items_by_cat = defaultdict(list)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip(): continue
            item = json.loads(line)
            cat = item.get('category', 'Uncategorized')
            items_by_cat[cat].append(item)

    # 3. Sort and Reindex
    total_items = 0
    with open(output_file, 'w', encoding='utf-8') as f:
        # Sort categories for consistent file order
        for cat in sorted(items_by_cat.keys()):
            items = items_by_cat[cat]
            # Sort items by their OLD row to preserve relative order
            items.sort(key=lambda x: x.get('row', 0))
            
            # Reassign row numbers starting from 1
            for i, item in enumerate(items):
                item['row'] = i + 1
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
                total_items += 1
            
            print(f"Category '{cat}': re-indexed {len(items)} items.")

    print(f"Re-indexed file written: {output_file}")
    print(f"Total items: {total_items}")
    
    # Overwrite original
    shutil.move(output_file, input_file)
    print(f"Overwritten original file: {input_file}")

if __name__ == "__main__":
    reindex_rows()
