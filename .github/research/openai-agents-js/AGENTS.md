# openai/openai-agents-js 研究域 Agent 指南

本目录只研究 openai/openai-agents-js 这个 OpenAI 官方 JavaScript/TypeScript Agents SDK。

## 维护规则

- 动态 GitHub 事实写入 domain.yml，并标注 observed_at。
- raw/ 只保存脚本拉取的一手事实，不手工改写原始快照。
- README.md 只写当前判断；架构、迁移和验证写入 analysis.md、deep-dive.md 或实验记录。
- 不把 OpenAI API、Python SDK 或其他 Agent 框架混成新的聚合研究域；横向比较放在研究总索引或综合文档。
- 涉及 sandbox、工具执行或真实 API 调用时，必须记录权限边界、凭据风险和可复现验证路径。
- 修改后运行 make sync-doc-toc 和 make test。
