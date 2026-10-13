# openai/openai-agents-js 研究分析

## 本轮结论

openai/openai-agents-js 展示了一个把模型调用、工具、护栏、handoff、sandbox、session 和 tracing 组合成运行时的官方 TypeScript 实现。它与 Codex 的本地执行控制面不同，更适合研究应用层 Agent 如何保留状态、管理副作用并提供可观察证据。

## 本地证据

- raw/github-readme.raw.md.txt：官方概念、安装条件、文本 Agent、sandbox Agent 和 realtime Agent 说明。
- raw/repository/packages/agents-core/：Agent、runner、工具、状态和生命周期核心。
- raw/repository/packages/agents/、agents-openai/、agents-extensions/、agents-realtime/：公开包和适配层。
- raw/repository/.agents/references/：运行上下文、工具审批、sandbox、schema、session 和 tracing 的维护者研究材料。
- raw/repository/.agents/skills/：变更验证、文档同步、敏感日志审计和运行时探针技能。

## 对标拆解

| 项 | 内容 |
|:---|:---|
| 参考对象 | openai/openai-agents-js |
| 核心问题 | 让 Agent 的推理、工具调用、人工审批和运行结果进入一个可恢复、可观察的执行循环 |
| 核心机制 | Agent 定义、RunContext、runner、tool guardrail、handoff、session、sandbox 和 tracing 分层 |
| 真正带来结果的动作 | 先解析和校验工具意图，再按审批、执行、错误、恢复和最终输出顺序推进 |
| 可迁移做法 | 为本仓的脚本、skill 和 workflow 明确输入、权限、副作用、失败和验证证据 |
| 不可迁移条件 | 不复制 SDK 运行时、实时音频、云端 provider 或完整 sandbox 实现 |

## 改良迭代

| 改良目标 | 本仓版本 | 验证指标 |
|:---|:---|:---|
| 工具边界 | 给会写文件、跑命令或访问网络的入口登记权限和副作用 | 执行前能判断风险，失败后能恢复 |
| 运行状态 | 把任务输入、命令结果、验证结果和版本绑定起来 | 旧证据不能被新改动冒充 |
| 审批顺序 | 高风险动作先做参数校验和人工确认 | 拒绝动作不产生副作用 |
| 观察性 | 为研究和自动化动作保存来源、命令、退出码和产物摘要 | 结论可由 raw 和本仓文件复查 |

## 可迁移清单

- 把模型意图与实际执行分开。
- 把工具调用先归一化为执行计划，再进入权限和验证流程。
- 明确区分输入护栏、工具审批、工具执行、输出护栏和持久化。
- 将 session、usage、trace 和错误路径视为同一条生命周期，而不是附加日志。
- 对 sandbox 或本机执行保留最小权限和清理路径。

## 不可迁移清单

- 不把 Agents SDK 当作本仓文档系统的必要依赖。
- 不把 sandbox 示例中的 API key 或客户端 token 写入本仓配置。
- 不把 streaming、realtime 和多 Agent handoff 的复杂度强行引入简单文档任务。

## 验证动作

| 动作 | 成功信号 | 失败信号 |
|:---|:---|:---|
| 抽样一个会执行命令的本仓入口 | 有输入、权限、审批、执行、失败和回滚说明 | 只有“让 Agent 自己执行”的口头要求 |
| 抽样一个文档自动化流程 | 结果绑定当前版本和真实命令输出 | 只保存自然语言完成声明 |
| 复查敏感日志路径 | 凭据不进入日志、trace、任务文档或 raw 分析 | 失败输出可能泄露密钥或完整环境 |

## 沉淀判断

“Agent 运行时必须把意图、工具、审批、状态和证据分开”可以下沉到本仓 workflow 和 scripts 的治理规则。具体 SDK 类型和 provider 适配只保留在研究域。
