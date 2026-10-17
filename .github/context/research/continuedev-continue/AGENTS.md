# continuedev/continue 研究域 Agent 指南

本目录只研究 continuedev/continue 这个开源 coding agent 项目。

## 维护规则

- 动态 GitHub 事实写入 domain.yml，并标注 observed_at。
- raw/ 只保存脚本拉取的一手事实，不手工改写原始快照。
- README.md 只写当前判断；IDE、CLI、上下文、模型和评估机制写入 analysis.md、deep-dive.md 或实验记录。
- 不把 Continue 的配置、扩展和外部 provider 默认当作本仓推荐方案。
- 复现实验必须使用隔离项目和无敏感信息配置，记录版本、权限和验证命令。
- 修改后运行 make sync-doc-toc 和 make test。
