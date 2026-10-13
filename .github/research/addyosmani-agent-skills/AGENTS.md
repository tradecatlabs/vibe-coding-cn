# addyosmani/agent-skills 研究域 Agent 指南

本目录只研究 addyosmani/agent-skills 这个面向 AI coding agent 的工程技能仓库。

## 维护规则

- 动态 GitHub 事实写入 domain.yml，并标注 observed_at。
- raw/ 只保存脚本拉取的一手事实，不手工改写原始快照。
- README.md 只写当前判断；技能契约、命令映射、质量门禁和迁移写入 analysis.md、deep-dive.md 或实验记录。
- 外部技能、脚本和引用资料先审查许可证、来源、权限和副作用，不能因为支持 Codex 就默认安全。
- 不将单个技能复制进本仓；需要吸收时必须写明改良理由、所有权和验证路径。
- 修改后运行 make sync-doc-toc 和 make test。
