# anomalyco/opencode 研究域 Agent 指南

本目录只研究当前规范仓库 `anomalyco/opencode`，即 OpenCode 开源 coding agent。

## 维护规则

- 动态 GitHub 事实写入 `domain.yml`，并标注 `observed_at`。
- `raw/` 只保存脚本拉取的一手事实，不手工改写原始快照。
- `README.md` 只写当前判断；架构、迁移和验证写入 `analysis.md`、`deep-dive.md` 或实验记录。
- `sst/opencode` 只作为历史仓库名或重定向来源记录，不另建重复研究域；其他 OpenCode 生态项目放在研究总索引或单独研究域。
- 修改后运行 `make sync-doc-toc` 和 `make test`。
