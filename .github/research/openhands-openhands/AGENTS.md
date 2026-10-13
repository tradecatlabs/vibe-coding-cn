# OpenHands/OpenHands 研究域 Agent 指南

本目录只研究 `OpenHands/OpenHands` 这个 AI 驱动开发项目。

## 维护规则

- 动态 GitHub 事实写入 `domain.yml`，并标注 `observed_at`。
- `raw/` 只保存脚本拉取的一手事实，不手工改写原始快照。
- `README.md` 只写当前判断；架构、迁移和验证写入 `analysis.md`、`deep-dive.md` 或实验记录。
- 不把 OpenHands 生态、模型服务或其他 coding agent 混成新的聚合研究域；横向比较放在研究总索引或综合文档。
- 修改后运行 `make sync-doc-toc` 和 `make test`。
