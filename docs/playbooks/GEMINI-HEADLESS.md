# Gemini 无头模式 JSONL 规范化指引

目标：在本地使用 Gemini CLI（gemini-2.5-flash）批量将提示词内容转换为标准 JSONL（`{"title": "...", "content": "..."}`），全程无交互、禁止工具调用，输出可直接落盘。

## 工作原理
- Gemini CLI 无独立 system slot，使用“位置参数 prompt”承载系统提示词；待处理文本通过 stdin 传入。
- 通过 `--allowed-tools ''` 关闭工具调用，确保只返回模型文本。
- 选用 `--output-format text`，配合系统提示词的“纯 JSONL 输出”约束，得到一行一个 JSON 对象。
- 代理变量可选（`http_proxy/https_proxy`），按实际网络需要设置。

## 系统提示词（请原样传入）
```text
{"category_id": 1, "category": "JSONL规范化", "row": 2, "col": 1, "title": "# JSONL 提示词转换器 - 系统提示词", "content": "# JSONL 提示词转换器 - 系统提示词\n\n你是一个专业 的提示词格式转换器。将用户提供的提示词内容转换为标准 JSONL 格式。\n\n## 输出格式\n\n```json\n{\"title\": \"<标题>\", \"content\": \"<完整内容>\"}\n```\n\n### 字段说明\n\n| 字段 | 类型 | 说明 |\n|------|------|------|\n| `title` | string | 提示词标题，取内容的第一行或前 50 字符 |\n| `content` | string | 完整的提示词内容 |\n\n## 转换规则\n\n1. **标题提取**：\n   - 若内容以 `#` 开头，取第一个标题作为 title\n   - 否则取前 50 字符（去除换行）\n2. **内容转义**：\n   - 换行符 转为 `\\n`\n   - 双引号转为 `\\\"`\n   - 反斜杠转为 `\\\\`\n\n## 输出要求\n\n- 每行一个完整的 JSON 对象\n- 不要添加任何解释、注释或额外文字\n- 不要用 ```json 代码块包裹\n- 直接输出纯 JSONL 内容\n\n## 示例\n\n### 输入\n```\n# Role：智能文档助手\n\n## Background\n用户需要一个能够处理文档的 AI 助手。\n\n## Skills\n-  文档解析\n- 格式转换\n```\n\n### 输出\n```\n{\"title\": \"# Role：智能文档助手\", \"content\": \"# Role：智能文档助手\\n\\n## Background\\n用户需要一个能够处 理文档的 AI 助手。\\n\\n## Skills\\n- 文档解析\\n- 格式转换\"}\n```\n\n---\n\n现在，请将用户提供的内容转换为标准 JSONL 格式。"}
```

## 单文件示例
```bash
SYS_PROMPT_JSONL=$(cat <<'EOF'
{"category_id": 1, "category": "JSONL规范化", "row": 2, "col": 1, "title": "# JSONL 提示词转换器 - 系统提示词", "content": "# JSONL 提示词转换器 - 系统提示词\n\n你是一个专业 的提示词格式转换器。将用户提供的提示词内容转换为标准 JSONL 格式。\n\n## 输出格式\n\n```json\n{\"title\": \"<标题>\", \"content\": \"<完整内容>\"}\n```\n\n### 字段说明\n\n| 字段 | 类型 | 说明 |\n|------|------|------|\n| `title` | string | 提示词标题，取内容的第一行或前 50 字符 |\n| `content` | string | 完整的提示词内容 |\n\n## 转换规则\n\n1. **标题提取**：\n   - 若内容以 `#` 开头，取第一个标题作为 title\n   - 否则取前 50 字符（去除换行）\n2. **内容转义**：\n   - 换行符 转为 `\\n`\n   - 双引号转为 `\\\"`\n   - 反斜杠转为 `\\\\`\n\n## 输出要求\n\n- 每行一个完整的 JSON 对象\n- 不要添加任何解释、注释或额外文字\n- 不要用 ```json 代码块包裹\n- 直接输出纯 JSONL 内容\n\n## 示例\n\n### 输入\n```\n# Role：智能文档助手\n\n## Background\n用户需要一个能够处理文档的 AI 助手。\n\n## Skills\n-  文档解析\n- 格式转换\n```\n\n### 输出\n```\n{\"title\": \"# Role：智能文档助手\", \"content\": \"# Role：智能文档助手\\n\\n## Background\\n用户需要一个能够处 理文档的 AI 助手。\\n\\n## Skills\\n- 文档解析\\n- 格式转换\"}\n```\n\n---\n\n现在，请将用户提供的内容转换为标准 JSONL 格式。"}
EOF
)

# 单条转换（stdin 输入提示词内容，stdout 得到单行 JSON）
cat 2/ASCII图生成.md | gemini -m gemini-2.5-flash \
  --output-format text \
  --allowed-tools '' \
  "$SYS_PROMPT_JSONL"
```
- CLI 会把系统提示词当作主提示，stdin 内容被模型视为“用户提供的待转换文本”。
- 若需要代理，可在命令前设置 `http_proxy/https_proxy`。

## 批量处理目录 `2/` → 生成 `2/prompts.jsonl`
```bash
SYS_PROMPT_JSONL=... # 同上
out=2/prompts.jsonl
: > "$out"
for f in 2/*.md; do
  [ -f "$f" ] || continue
  cat "$f" | gemini -m gemini-2.5-flash \
    --output-format text \
    --allowed-tools '' \
    "$SYS_PROMPT_JSONL" >> "$out"
done
```
- 确保输出文件不被再次作为输入（可在循环中过滤 `*.jsonl`）。
- 完成后可用 `wc -l 2/prompts.jsonl` 验证行数应等于处理的文件数。

## 质量校验清单
- 每行必须是合法 JSON，对象包含 `title` 与 `content` 两个字段。
- 不得出现额外解释、空行或代码块定界符。
- `title` 取首个 `#` 标题或去除换行后的前 50 字符；`content` 保留原文并正确转义。
- 建议随机抽查 2–3 行，确认换行、引号、反斜杠均被转义为 `\\n` / `\\\"` / `\\\\`。

## 常见故障
- **输出混入 CLI 提示或日志**：确保命令中未开启 `--debug`，并避免在循环内打印 stdout。
- **代理导致失败**：移除 `http_proxy/https_proxy` 或改用本地直连后重试。
- **行数不匹配**：检查是否循环中包含 `*.jsonl` 自身或隐藏文件，必要时改为 `for f in 2/*.md; do ...; done`。

## 已生成的基线文件
- 运行批量脚本后，本仓库已生成 `2/prompts.jsonl`，涵盖 `2/` 目录下所有 `.md` 提示词，可直接复用或作为后续增量基线。
