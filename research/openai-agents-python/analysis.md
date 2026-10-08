# openai/openai-agents-python 研究分析

## 本轮结论

`openai/openai-agents-python` 把 Agent 应用拆成模型、工具、handoff、guardrail、session、sandbox 和 tracing 等可组合对象。它与 `openai/codex` 的关系是互补：Codex 更像本地 coding agent 的执行控制面，Agents SDK 更像可嵌入应用的 Agent 工作流运行时。

## 本地证据

- `raw/github-readme.raw.md.txt`：核心概念、安装方式、text agent、sandbox agent、realtime agent 和 voice agent 示例。
- `raw/repository/agents/run.py` 与 `agents/run_internal/run_loop.py`：运行循环与状态推进。
- `raw/repository/agents/guardrail.py`、`agents/tool_guardrails.py`：输入、输出和工具护栏。
- `raw/repository/agents/handoffs/`、`agents/memory/`、`agents/tracing/`：交接、会话和追踪边界。
- `raw/repository/agents/sandbox/`：工作区和命令执行环境。
- `raw/repository/docs/testing.md`：provider-neutral 的确定性测试方法。

## 对标拆解

| 项 | 内容 |
|:---|:---|
| 参考对象 | `openai/openai-agents-python` |
| 它解决的核心问题 | 将单个 Agent 和多 Agent 工作流组合成可运行、可验证的应用 |
| 核心机制 | Agent + Tools + Handoffs + Guardrails + Sessions + Tracing + Sandbox |
| 真正带来结果的动作 | 把运行状态、授权边界和观察证据从 prompt 中分离出来 |
| 可迁移做法 | 明确 Agent 责任、工具契约、护栏位置、会话持久化和运行追踪 |
| 不可迁移条件 | 不为文档仓库引入完整 SDK、异步运行时或多 Agent 服务端 |
| 下一步试用动作 | 用一个本仓文档校验任务写“计划 Agent -> 执行工具 -> 验证护栏”最小实验 |

## 改良迭代

| 改良目标 | 本仓版本 | 验证指标 |
|:---|:---|:---|
| 工具边界 | 给脚本标注输入、输出、权限和失败状态 | Agent 能在执行前判断风险 |
| 交接边界 | 将研究、实现、审查和交付作为不同阶段 | 阶段之间有明确产物，不靠聊天记忆传递 |
| 护栏位置 | 把链接、结构、敏感信息和质量检查放进机器门禁 | 违规结果能以非零状态失败 |
| 运行证据 | 保存命令、结果、diff 和测试摘要 | 结论能由当前输入和产物复查 |

## 可迁移清单

- 把工具调用与 Agent 的自然语言判断分开记录。
- 对输入和输出都设计验证点，不只校验最终文本。
- 需要长期任务时显式保存 session、状态和恢复边界。
- 用 tracing 或结构化日志记录关键决策与工具结果。
- 对工作区写入、命令执行和外部调用设置权限层级。

## 不可迁移清单

- 不把 SDK 的多 Agent 能力当作本仓默认需要的多 Agent 运行时。
- 不以 tracing 代替测试、审查或真实产物。
- 不把模型供应商能力等同于工具权限或业务正确性。

## 验证动作

| 动作 | 成功信号 | 失败信号 |
|:---|:---|:---|
| 用固定输入模拟一次文档校验流程 | 工具调用序列和失败分支可重复 | 每次依赖模型自由发挥，无法定位漂移 |
| 为高风险脚本增加工具级检查 | 未满足权限/输入条件时直接失败 | 仍靠 Agent 口头说明安全 |
| 记录一次研究到沉淀的交接 | 每个阶段都有文件和验证证据 | 结论只存在于会话文字 |

## 沉淀判断

“Agent 应用 = 模型 + 运行循环 + 工具 + 状态 + 护栏 + 证据”可下沉到 `docs/gongfa/`；SDK 的具体 Python API 留在本研究域，不扩散为本仓安装前置。
