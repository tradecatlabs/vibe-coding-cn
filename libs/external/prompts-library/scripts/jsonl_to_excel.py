import json
import pandas as pd

input_file = "prompt_jsonl/prompt_docs_refactored.jsonl"
output_file = "prompt_excel/prompt_docs_refactored.xlsx"

def process():
    data_by_cat = {}
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip(): continue
            item = json.loads(line)
            cat = item['category']
            if cat not in data_by_cat:
                data_by_cat[cat] = []
            
            # Reconstruct the JSON string for the cell as it was in original Excel
            cell_data = {
                "title": item.get('title', ''),
                "content": item.get('content', '')
            }
            data_by_cat[cat].append(json.dumps(cell_data, ensure_ascii=False))

    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Sort categories to keep a consistent order
        sorted_cats = sorted(data_by_cat.keys())
        for cat in sorted_cats:
            items = data_by_cat[cat]
            # Each item in its own row, column 0
            df = pd.DataFrame(items)
            df.to_excel(writer, sheet_name=cat, index=False, header=False)
    
    print(f"Excel created: {output_file}")

if __name__ == "__main__":
    process()
