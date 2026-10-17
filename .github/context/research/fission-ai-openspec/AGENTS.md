# Fission-AI/OpenSpec 研究域 Agent 指南

本目录只研究 Fission-AI/OpenSpec 这个规格驱动开发工具。

## 维护规则

- 动态 GitHub 事实写入 domain.yml，并标注 observed_at。
- raw/ 只保存脚本拉取的一手事实，不手工改写原始快照。
- README.md 只写当前判断；变更流程、schema、脚本和验证写入 analysis.md、deep-dive.md 或实验记录。
- 不把 Spec Kit、OpenCode、Codex 或其他 coding agent 混成当前研究对象；横向比较放在研究总索引或迁移综合文档。
- 外部脚本、配置和安装命令先做来源、权限和副作用审查，再决定是否复现实验。
- 修改后运行 make sync-doc-toc 和 make test。
