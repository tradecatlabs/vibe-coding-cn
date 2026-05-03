# tools/prompts-library/ Agent 指南

本目录维护提示词格式转换工具，支持 Excel、Markdown 和 JSONL 之间的转换。

## 约束

- 修改转换逻辑前先阅读 `README.md` 和 `main.py`，不要猜输入输出格式。
- 不提交生成目录、缓存和临时导出；`prompt_jsonl/` 为 ignored 生成物。
- 新增依赖必须更新本目录的 `requirements.txt` 或脚本专用依赖文件。
- 修改工具后，运行最小可用命令或说明无法运行的原因。

## 常用命令

```bash
cd tools/prompts-library
python3 main.py
```
