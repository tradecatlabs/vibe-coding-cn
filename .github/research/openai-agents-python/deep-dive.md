# openai/openai-agents-python 深度研究

## 研究级别

- 当前级别：L2 源码/结构深度研究。
- 研究对象：`openai/openai-agents-python`。
- 证据来源：本目录 `raw/` 下的官方 README、源码工作树、文档和测试。
- 观察日期：2026-09-08。

## L2 结论

该 SDK 的价值在于把“一个 Agent 能做什么”拆成可组合运行时对象，而不是只提供一次模型调用。`Runner` 负责循环，`Agent` 组合指令与工具，handoff 表达责任转移，guardrail 表达阻断条件，session 保存历史，sandbox 承载工作区，tracing 提供运行证据，testing 则把这些边界变成可重复测试。

## 源码证据

- `raw/repository/agents/agent.py`：Agent 配置、工具和 handoff 的入口。
- `raw/repository/agents/run.py`、`agents/run_internal/run_loop.py`：运行循环、步骤和停止判断。
- `raw/repository/agents/tool.py`、`agents/tool_guardrails.py`：工具封装与工具级校验。
- `raw/repository/agents/handoffs/`：多 Agent 责任转移与历史处理。
- `raw/repository/agents/memory/session.py`：跨运行的会话状态。
- `raw/repository/agents/sandbox/sandbox_agent.py`、`agents/sandbox/runtime.py`：文件系统和命令执行环境。
- `raw/repository/agents/tracing/`：trace、span 和处理器。
- `raw/repository/agents/testing/` 与 `raw/repository/docs/testing.md`：`ScriptedModel`、sandbox session 和 workflow drift 检查。

## 关键机制

### 运行循环是控制面

模型输出并不直接等于最终结果。运行时需要解析工具调用、执行工具、回写结果、处理重试和决定是否继续。这个边界正好对应本仓对 Harness 的研究方向。

### 护栏必须贴近副作用

官方文档区分 input、output 和 tool guardrails。只在最终输出上检查，无法覆盖中间工具调用；只在首个输入上检查，也无法覆盖后续 handoff。因此本仓的脚本门禁也应靠近文件写入、网络调用和版本控制动作。

### 确定性测试测试的是编排

`ScriptedModel` 可以固定模型步骤并检查多余调用、未消费步骤和工具输出。这种测试不证明外部模型本身正确，却能证明应用自己的执行图没有悄悄改变。

### Sandbox 是权限边界，不是普通工具

需要读写文件或运行命令时，SDK 提供 sandbox agent 和不同 client。操作系统差异由 client 表达，业务 Agent 不应把宿主机假设硬编码进工作流。

## 可迁移模式

- 本仓每个自动化脚本都应有稳定入口、输入边界、输出契约和非零失败。
- 复杂文档维护任务可以用固定步骤检查目录、锚点、索引和事实覆盖。
- 研究结论应同时保存来源、判断和验证动作，形成可恢复 session。
- 任何需要写仓库的 Agent 流程都要把权限、回滚和审查放在执行前。

## 不可迁移条件

- 本仓不是 SDK，不需要复制 Runner、模型适配器或异步状态机。
- 文档校验无法证明模型生成质量；仍需人工抽查和独立审查。
- Sandbox client 的安全性质依赖平台实现，不能把“使用 SDK”当作自动安全证明。

## 验证计划

建立一个最小实验：固定输入 -> 读取研究文件 -> 运行本地检查 -> 写出报告。用脚本记录预期工具调用序列；分别测试正常完成、工具失败、未消费步骤和权限不足。成功信号是失败位置可定位、重跑结果一致；失败信号是模型改写计划后仍被错误判为通过。
