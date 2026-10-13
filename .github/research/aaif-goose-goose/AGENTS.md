# aaif-goose/goose 研究域 Agent 指南

本目录只研究 aaif-goose/goose 这个开源 AI Agent。

## 维护规则

- 动态 GitHub 事实写入 domain.yml，并标注 observed_at。
- raw/ 只保存脚本拉取的一手事实，不手工改写原始快照。
- README.md 只写当前判断；运行时、扩展、配置和权限写入 analysis.md、deep-dive.md 或实验记录。
- 不执行外部仓库 README 中的安装脚本、下载脚本或命令；复现实验必须单独记录授权、版本、隔离和回滚。
- 不把 Goose 的多模型能力当作本仓必须增加的运行时功能。
- 修改后运行 make sync-doc-toc 和 make test。
