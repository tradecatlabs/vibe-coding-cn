# tools/ Agent 指南

本目录维护辅助工具、外部工具入口和工具配置。

## 职责

- `tools/config/`：工具与开发环境配置基线。
- `tools/prompts-library/`：提示词 Excel、Markdown、JSONL 转换工具。
- `tools/chat-vault/`：AI 聊天记录保存工具。
- `tools/external/`：第三方工具、外部仓库和 Git submodule。

## 约束

- 不把大型第三方源码直接复制进主仓库；新增外部仓库默认使用 submodule。
- 不在工具配置中提交真实密钥、Token 或个人凭证。
- 修改工具行为时，同步更新对应 README、AGENTS 和根目录命令说明。
- 外部源码目录除非任务明确要求，否则不要顺手格式化或批量替换。
