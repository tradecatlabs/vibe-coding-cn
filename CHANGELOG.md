# Changelog

本文档记录知识库结构、入口、分类体系和重要内容的变更。

## Unreleased

- 启动标准知识库结构迁移：新增 `docs/`、`metadata/`、`scripts/`、`tools/` 骨架。
- 完成第一轮完全搬家：`assets/documents/` 迁入 `docs/`，`assets/skills/` 迁入 `skills/`，`assets/prompt/` 迁入 `prompts/`，`assets/config/` 迁入 `tools/config/`，`assets/repos/` 拆分为 `tools/external/`、`tools/prompts-library/`、`tools/chat-vault/` 与 `scripts/backups/`。
- 更新 README、AGENTS、llms、metadata、CI 与目录级 AGENTS，统一新知识库路径口径。
- 增加 `scripts/check-local-links.py`、`make check-links` 与 `make test`，把本地链接检查纳入质量门禁和 CI。
- 清退 `tools/external/my-nvim/nvim-config/nvim` 二进制运行时，改为文档说明从官方渠道安装 Neovim。
- 修复 `tools/prompts-library/main.py` 中 Excel(JSONL) -> JSONL 转换的行号偏移，保持导出记录与 Excel 原始行号一致。
- 清退 `tools/chat-vault/monitoring/grafana/monitor-tui/` 中误提交的第三方 btop 源码镜像，降低仓库噪音与语言统计污染。
