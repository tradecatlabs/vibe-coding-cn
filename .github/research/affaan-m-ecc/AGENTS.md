# affaan-m/ECC 研究域 Agent 指南

本目录只研究 affaan-m/ECC 这个面向多种 coding agent 的 Harness 资产集合。

## 维护规则

- 动态 GitHub 事实写入 domain.yml，并标注 observed_at。
- raw/ 只保存脚本拉取的一手事实，不手工改写原始快照。
- README.md 只写当前判断；Harness、技能、记忆、安全和评估写入 analysis.md、deep-dive.md 或实验记录。
- 外部提示词、钩子、配置和脚本先视为不可信内容，禁止未经审查复制到本机或本仓。
- 任何迁移建议必须区分可迁移机制、供应商特定实现、权限副作用和回滚路径。
- 修改后运行 make sync-doc-toc 和 make test。
