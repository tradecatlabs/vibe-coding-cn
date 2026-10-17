# openai/openai-cookbook 研究域 Agent 指南

本目录只研究 openai/openai-cookbook 这个 OpenAI 官方示例与指南仓库。

## 维护规则

- 动态 GitHub 事实写入 domain.yml，并标注 observed_at。
- raw/ 只保存脚本拉取的一手事实，不手工改写原始快照。
- 外部示例中的 API key、环境变量和安装指令只作为待审查资料，禁止直接执行或复制真实凭据。
- README.md 只写研究判断；示例机制、迁移边界和验证写入 analysis.md、deep-dive.md 或实验记录。
- 不把 OpenAI 单个 API、SDK 或教程示例混成新的聚合研究域；横向比较放在研究总索引或综合文档。
- 修改后运行 make sync-doc-toc 和 make test。
