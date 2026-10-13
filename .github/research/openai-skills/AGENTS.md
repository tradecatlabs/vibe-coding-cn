# openai/skills 研究域 Agent 指南

本目录只研究 `openai/skills` 这个 Codex Skills Catalog。

## 维护规则

- 动态 GitHub 事实写入 `domain.yml`，并标注 `observed_at`。
- `raw/` 只保存脚本拉取的一手事实，不手工改写原始快照。
- `README.md` 只写当前判断；结构和迁移分析写入 `analysis.md`、`deep-dive.md` 或后续实验记录。
- 不把其他 OpenAI 仓库或多个技能混成新的聚合研究域；横向比较放在 `.github/research/README.md` 或综合文档。
- 修改后运行 `make sync-doc-toc` 和 `make test`。
