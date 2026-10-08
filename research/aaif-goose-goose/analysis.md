# aaif-goose/goose 研究分析

## 本轮结论

aaif-goose/goose 是一个跨模型、跨平台的 AI Agent，提供桌面、CLI 和 API 入口，并通过 provider、MCP extension、workspace、workflow recipe 和评估资产扩展能力。它适合研究“Agent 产品如何把模型、工具和多种交互入口分层”。

## 本地证据

- raw/github-readme.raw.md.txt：桌面、CLI、API、多 provider 和 MCP 定位。
- raw/repository/crates/：Rust workspace，包括 agent、provider、MCP、SDK 和上下文管理包。
- raw/repository/documentation/：安装、自动化、插件和用户文档。
- raw/repository/workflow_recipes/：release risk check 等流程配方。
- raw/repository/evals/：评估和运行样例。
- raw/repository/.github/：CI、脚本和仓库自动化入口。

## 对标拆解

| 项 | 内容 |
|:---|:---|
| 参考对象 | aaif-goose/goose |
| 核心问题 | 让同一个 Agent 能在桌面、终端和 API 中使用多个模型和扩展执行任务 |
| 核心机制 | provider、agent、MCP、SDK、context management、workflow recipes 和多 UI |
| 真正带来结果的动作 | 将模型选择、工具扩展、执行环境和用户入口拆开 |
| 可迁移做法 | 本仓在工具选择文档中区分模型、Harness、工具、扩展和权限 |
| 不可迁移条件 | 不复制完整 Rust 平台、桌面应用或 provider 集成 |

## 改良迭代

| 改良目标 | 本仓版本 | 验证指标 |
|:---|:---|:---|
| 工具选型 | docs 将 CLI、IDE、数据库、系统工具分层 | 用户知道工具承担什么职责 |
| 扩展治理 | 外部 MCP/插件先登记来源和权限 | 不因能安装就默认可信 |
| 工作流配方 | 把重复任务沉淀为可验证 workflow | 配方有输入、输出和失败恢复 |
| 多入口一致性 | Codex 主线与 OpenCode 备选各自写清边界 | 不混淆订阅、API key 和运行权限 |

## 可迁移清单

- 用 provider、tool、extension 和 workspace 分离复杂度。
- 为工具扩展提供授权、停用和卸载路径。
- 将流程配方绑定风险检查和结果证据。
- 把桌面体验、CLI 体验和 API 嵌入视为不同入口。

## 不可迁移清单

- 不把 Goose 支持的模型、订阅和扩展清单变成本仓推荐清单。
- 不执行其下载脚本或 provider 配置。
- 不以跨平台数量替代安全、稳定和维护性判断。

## 验证动作

| 动作 | 成功信号 | 失败信号 |
|:---|:---|:---|
| 评估一个外部 MCP | 来源、权限、网络、凭据和回滚已知 | 只看名称和安装命令 |
| 评估一个 workflow recipe | 风险、输入、检查项和输出可复现 | 只是一段自然语言流程 |
| 比较桌面和 CLI 入口 | 能指出共享能力和入口差异 | 把 UI 差异误认为模型差异 |

## 沉淀判断

“工具扩展是有权限和生命周期的外部能力，不是普通配置项”适合下沉到 docs/gongfa 和 tools/AGENTS.md。
