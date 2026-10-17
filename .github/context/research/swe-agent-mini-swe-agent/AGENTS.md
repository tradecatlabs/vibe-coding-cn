# SWE-agent/mini-swe-agent 研究域 Agent 指南

本目录只研究 SWE-agent/mini-swe-agent 这个极简软件工程 Agent。

## 维护规则

- 动态 GitHub 事实写入 domain.yml，并标注 observed_at。
- raw/ 只保存脚本拉取的一手事实，不手工改写原始快照。
- README.md 只写当前判断；Agent loop、配置、基准和验证写入 analysis.md、deep-dive.md 或实验记录。
- 涉及真实仓库修复时，必须使用隔离副本、最小权限、明确停止条件和可回滚版本。
- 不能把 SWE-bench 分数直接当成本仓所有任务的质量证明，必须区分基准和实际项目。
- 修改后运行 make sync-doc-toc 和 make test。
