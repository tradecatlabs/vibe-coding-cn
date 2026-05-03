# prompts-library

`tools/prompts-library/` 是本仓内的提示词格式转换工具，用于在 Excel、Markdown 和 JSONL 之间转换提示词资产。

它不是独立仓库首页，也不再引用旧的 `tukuaiai/prompt-library` 仓库口径。当前目录作为 `vibe-coding-cn` 的内部工具维护。

## 功能

- Excel -> Markdown：把表格提示词导出为 Markdown 文档目录。
- Markdown -> Excel：把 Markdown 文档目录还原为 Excel 工作簿。
- Markdown -> JSONL：把 Markdown 提示词转换为 JSONL。
- JSONL -> Excel：把 JSONL 数据转换为 Excel。
- Excel(JSONL) -> JSONL：把内部 JSONL 格式的 Excel 按工作表拆成 JSONL 文件。

## 目录结构

```text
tools/prompts-library/
  README.md
  AGENTS.md
  main.py
  requirements.txt
  docs/
  scripts/
```

## 安装依赖

```bash
cd tools/prompts-library
python3 -m pip install -r requirements.txt
```

部分辅助脚本有单独依赖：

```bash
python3 -m pip install -r scripts/requirements.txt
```

## 常用命令

查看入口参数：

```bash
python3 main.py --help
```

交互式转换：

```bash
python3 main.py
```

指定转换模式：

```bash
python3 main.py --select "prompt_excel/example.xlsx" --mode excel2docs
python3 main.py --select "prompt_docs/example" --mode docs2excel
python3 main.py --select "prompt_docs/example" --mode docs2jsonl
python3 main.py --select "prompt_jsonl/example.jsonl" --mode jsonl2excel
python3 main.py --select "prompt_excel/prompt_jsonl.xlsx" --mode jsonl_excel2jsonl
```

无交互执行：

```bash
python3 main.py --select "prompt_excel/example.xlsx" --mode excel2docs --non-interactive
```

## 输入输出约定

- 默认 Excel 输入目录：`prompt_excel/`
- 默认 Markdown 输入/输出目录：`prompt_docs/`
- 默认 JSONL 输出目录：`prompt_jsonl/`
- `prompt_jsonl/` 是生成物，已在 `.gitignore` 中忽略。

## 维护规则

- 修改转换逻辑时，优先阅读 `main.py` 和 `scripts/` 中对应脚本。
- 新增依赖必须同步更新 `requirements.txt` 或 `scripts/requirements.txt`。
- 不提交生成目录、缓存、临时导出或本地凭证。
- 修改后至少运行：

```bash
python3 main.py --help
```

如改动影响仓库文档或链接，还需要在仓库根目录运行：

```bash
make test
```
