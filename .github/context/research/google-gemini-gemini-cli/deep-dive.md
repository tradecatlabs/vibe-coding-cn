# google-gemini/gemini-cli 深度研究

## 研究级别

- 当前级别：L2 源码/结构深度研究。
- 研究对象：`google-gemini/gemini-cli`。
- 证据来源：本目录 `raw/` 下的官方 README、源码、文档与评估文件。
- 观察日期：2026-09-08。

## L2 结论

Gemini CLI 的核心结构可以概括为：CLI 入口负责交互，core 负责 Agent 会话和工具，context 负责项目记忆，config 负责权限与扩展，MCP/extension 负责能力接入，evals 负责负例和行为回归。这个分层说明 coding agent 的可用性来自 Harness 组合，而不是模型文本生成本身。

## 源码证据

- `raw/repository/packages/cli/src/`：CLI 命令、交互和非交互运行入口。
- `raw/repository/packages/core/src/agent/`：Agent session 和事件处理。
- `raw/repository/packages/core/src/context/`：历史、压缩、记忆和上下文管理。
- `raw/repository/packages/core/src/config/`：配置、扩展、权限、trusted folders 和 sandbox。
- `raw/repository/docs/cli/gemini-md.md`：`GEMINI.md` 的项目上下文层级。
- `raw/repository/docs/tools/mcp-server.md`：MCP server 接入契约。
- `raw/repository/docs/extensions/writing-extensions.md`：扩展编写边界。
- `raw/repository/docs/cli/checkpointing.md`：会话 checkpoint 与恢复。
- `raw/repository/docs/hooks/index.md`：hook 配置、退出码和安全风险。
- `raw/repository/evals/prompt_injection_mcp.eval.ts`、`evals/shell_command_safety.eval.ts`：安全负例。

## 关键机制

### 上下文是分层资产

`GEMINI.md` 让项目规则与对话历史分开。对本仓而言，这对应 `AGENTS.md`、README 和任务/研究文件的不同职责：常驻契约不能被一次性任务材料覆盖。

### 扩展是受治理的工具面

MCP 和 extensions 让 Agent 继续增加能力，但同时增加了供应链、权限和提示注入风险。因此扩展必须有来源、配置 schema、退出码和负例，而不应只写“支持某工具”。

### 非交互模式是自动化接口

CLI 若能在脚本中运行，就必须输出稳定结果和退出码。它才能进入 CI、定时任务和本仓的质量闭环；交互式体验本身不能替代可重复执行。

### 评估覆盖失败路径

仓库中的 prompt injection MCP、shell command safety、sandbox recovery 和 validation fidelity 评估表明，Agent 系统应专门测试越权、恢复和验证失真，而不是只测正常回答。

## 可迁移模式

- 为本仓外部研究对象保存 raw 事实和 sources，避免分析与原文混在一起。
- 为每一个自动化入口定义退出码、稳定输出和失败语义。
- 为新 skill/工具设计 prompt injection 和权限负例。
- 用 checkpoint + Git 形成可回滚的长任务状态。

## 不可迁移条件

- Gemini CLI 的核心实现规模远超本仓文档仓库需要，不复制其 TypeScript monorepo。
- 外部扩展是否安全不能由文档描述推断，必须进行具体审查。
- 供应商认证、额度和模型默认值会动态变化，只能作为观察日事实。

## 验证计划

构造四个固定样本：正常只读任务、请求危险 shell、MCP 提示注入、上下文冲突。记录工具调用、退出码、产物和阻断原因。成功信号是每类样本都有确定性结论；失败信号是系统只返回自然语言拒绝而没有机器证据。
