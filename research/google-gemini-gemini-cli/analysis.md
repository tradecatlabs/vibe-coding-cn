# google-gemini/gemini-cli 研究分析

## 本轮结论

`google-gemini/gemini-cli` 是模型厂商直接维护的开源终端 Agent，重点不是单纯把 Gemini 接到 shell，而是把 CLI、项目上下文、工具、MCP、扩展、沙箱、checkpoint 和 GitHub 自动化组合成工作流。它与 Codex 的对照价值在于：两者都把模型接入本地执行，但上下文文件、扩展和权限机制的命名与边界不同。

## 本地证据

- `raw/github-readme.raw.md.txt`：CLI 能力、安装、认证、MCP、非交互模式、checkpoint 和 `GEMINI.md`。
- `raw/repository/packages/core/src/`：Agent、上下文、配置、权限、沙箱和扩展实现。
- `raw/repository/packages/cli/src/`：终端命令和交互入口。
- `raw/repository/docs/cli/gemini-md.md`、`docs/tools/mcp-server.md`、`docs/cli/sandbox.md`：上下文、MCP 和沙箱契约。
- `raw/repository/evals/prompt_injection_mcp.eval.ts`、`evals/shell_command_safety.eval.ts`：安全和工具行为评估样本。

## 对标拆解

| 项 | 内容 |
|:---|:---|
| 参考对象 | `google-gemini/gemini-cli` |
| 它解决的核心问题 | 在终端中以自然语言理解代码、调用工具、自动化任务并保留项目上下文 |
| 核心机制 | `GEMINI.md`、MCP、extensions、trusted folders、sandbox、checkpoint 和非交互执行 |
| 真正带来结果的动作 | 把上下文和工具能力放进可配置的 CLI 运行时，而不是只延长 prompt |
| 可迁移做法 | 项目上下文入口、扩展契约、命令安全评估、脚本化执行和会话恢复 |
| 不可迁移条件 | 不把 Gemini 账户、模型额度和供应商特有配置写成本仓唯一前置 |
| 下一步试用动作 | 用 `GEMINI.md` 与本仓 `AGENTS.md` 做一次上下文边界对照实验 |

## 改良迭代

| 改良目标 | 本仓版本 | 验证指标 |
|:---|:---|:---|
| 项目上下文 | 保持根和子目录 `AGENTS.md` 为正式规则入口 | Agent 读取路径和职责不含糊 |
| 工具扩展 | 将 MCP/外部工具只作为可审查能力接入 | 工具来源、权限和失败状态可追踪 |
| 会话恢复 | 用 Git、任务文档和研究 raw 固定状态 | 重开会话能恢复当前判断，不依赖隐含记忆 |
| 安全评估 | 增加命令安全、提示注入和权限负例 | 负例被拦截且返回非零或明确 BLOCK |

## 可迁移清单

- 用层级上下文文件降低长会话的信息丢失。
- 将扩展视为能力包，单独审查来源、权限和生命周期。
- 为非交互 CLI 设计固定输入、输出和退出码。
- 把提示注入、shell 安全和工具越界纳入评估集。
- 用 checkpoint 或 Git 检查点恢复长任务。

## 不可迁移清单

- 不把 `GEMINI.md` 与 `AGENTS.md` 视为完全同构的规则系统。
- 不把免费额度、默认模型或 Google 登录状态写成跨平台事实。
- 不把外部 eval 结果当作本仓安全通过证明。

## 验证动作

| 动作 | 成功信号 | 失败信号 |
|:---|:---|:---|
| 对一个项目上下文文件做层级读取实验 | Agent 能区分常驻规则和任务材料 | 上下文冲突时没有优先级或证据 |
| 运行一个只读非交互任务 | 输入、输出和退出码稳定 | 输出依赖终端交互或隐式认证 |
| 注入一个危险命令和一个提示注入样本 | 工具权限或评估门禁阻断 | 只靠模型自觉拒绝 |

## 沉淀判断

“上下文文件 + 工具权限 + 非交互入口 + 安全负例”可沉淀到本仓 `docs/gongfa/`；供应商特有命令和账号流程留在具体工具配置文档。
