# tools/prompts-library/scripts

提示词转换工具的辅助脚本目录。

## 常见脚本

- `excel_to_docs.py` - Excel 转 Markdown。
- `docs_to_excel.py` - Markdown 转 Excel。
- `md_to_jsonl.py` - Markdown 转 JSONL。
- `jsonl_to_excel.py` - JSONL 转 Excel。
- `gemini_jsonl_batch.py` - 使用 Gemini CLI 批处理 Markdown 到 JSONL。

## 维护规则

- 新增脚本必须有清晰 CLI 参数和 `--help`。
- 新增依赖必须更新 `requirements.txt`。
- 不提交生成数据、缓存或临时导出。
