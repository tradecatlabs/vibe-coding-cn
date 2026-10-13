# openai/openai-cookbook 深度研究

## 研究级别

- 当前级别：L2 示例资产与评估结构研究。
- 研究对象：openai/openai-cookbook。
- 证据来源：本目录 raw/ 下的 README、registry、Codex 示例、Agents SDK 示例和评估样例。
- 观察日期：2026-09-08。

## L2 结论

Cookbook 的结构把“内容发现”和“示例事实”分开：registry.yaml 负责网站索引，examples/ 和 articles/ 负责材料，.codex/skills/ 负责仓库内文档协作。这个分层对本仓有直接启示：研究入口不应直接承载全部正文，研究结论必须能追溯到稳定路径和观察日期。

## 关键机制

### 登记表驱动发现

registry.yaml 为材料提供标题、路径、描述、日期、作者和标签。它让机器和人可以从用途进入样例，不必遍历整个仓库。

### Codex 主题集中

examples/codex/ 中可以看到迭代开发工作流、代码审查、Git 质量、自动修复和目标等主题，说明官方资料把 Codex 当作可编排的工程参与者，而不仅是聊天入口。

### Agent 示例分层

examples/agents_sdk/ 覆盖 session memory、parallel agents、agent evaluation、security review 和 improvement loop，形成“能力 -> 状态 -> 评估 -> 安全”的观察面。

### 示例的风险边界

部分材料涉及 API key、第三方服务、文件、网络或模型调用。研究时只能读取和分析，不得将原始安装或调用动作当作本仓门禁。

## 可迁移模式

- 为研究域增加主题、来源类型、最新观察时间和沉淀目标字段。
- 对每个新研究对象至少记录一个可复现动作和一个失败信号。
- 将“官方事实”和“本仓迁移判断”放在不同文件层。
- 对 Codex 相关资料优先保留官方入口，外部博客只做补充。

## 迁移边界

- Notebook 的运行环境、模型、网络和费用不是本仓默认前置。
- 示例中的密钥环境变量只作为风险提示，禁止复制到项目配置。
- Cookbook 的覆盖范围很广，只有与 Vibe Coding、Agent 或工程验证直接相关的部分进入本仓索引。

## L3 验证任务

1. 为 .github/research/README.md 增加研究对象的方向标签和沉淀目标。
2. 从 Codex 示例抽取一个不依赖外部账号的文档验证模板。
3. 对新增研究结论执行 raw 路径、链接、观察日期和事实/判断分层检查。
