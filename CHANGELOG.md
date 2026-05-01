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
- 创建 `baseline-skill-cleanup-20260502-041941` 基线标签，开始清理领域型/工具型 Skills。
- 清退 `ccxt`、`claude-code-guide`、`claude-cookbooks`、`coingecko`、`cryptofeed`、`ddd-doc-steward`、`headless-cli`、`hummingbot`、`markdown-to-epub`、`polymarket`、`postgresql`、`proxychains`、`snapdom`、`sop-generator`、`telegram-dev`、`timescaledb`、`tmux-autopilot`、`twscrape` 等 Skill 目录，仅保留 `auto-skill` 与 Claude 官方 skills 软链接入口。
- 清退 `docs/case-studies/` 实战案例目录，并同步更新 docs 索引、目录级 AGENTS、metadata、labeler 和相关 README 链接口径。
- 清退 `docs/playbooks/` 下 7 个工具型/旧方法论文档，并同步更新 playbooks 索引、README、学习地图与相关概念页链接。
- 清退 `docs/playbooks/REMOTE_TUNNEL_GUIDE.md`，继续收缩工具型旧文档。
