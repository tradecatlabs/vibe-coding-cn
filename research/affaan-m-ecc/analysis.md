# affaan-m/ECC 研究分析

## 本轮结论

ECC 是一个面向 Claude Code、Codex、OpenCode、Cursor 等工具的 Harness 资产集合，覆盖 skills、rules、memory、hooks、security、research 和 Codex plugin/compatibility sync。它与本仓 Harness Engineering 方向高度相关，但安装和 hooks 会改变本机行为，必须作为高风险外部参考审查，不能直接复制。

## 本地证据

- raw/github-readme.raw.md.txt：安装模式、Codex 原生 plugin、legacy sync、skills、hooks、memory 和安全说明。
- raw/repository/.codex/、.codex-plugin/：Codex 项目配置、agents 和 plugin manifest。
- raw/repository/manifests/：组件、模块和 profile 安装清单。
- raw/repository/skills/：agent-harness-construction、agent-eval、ai-regression-testing 等能力。
- raw/repository/hooks/、scripts/hooks/：session、质量、成本、配置保护和自动化钩子。
- raw/repository/rules/、contexts/、schemas/：规则、上下文和结构化契约。

## 对标拆解

| 项 | 内容 |
|:---|:---|
| 参考对象 | affaan-m/ECC |
| 核心问题 | 将 Agent 的技能、记忆、安全、规则和性能优化组成跨工具 Harness |
| 核心机制 | skills、rules、contexts、hooks、manifests、plugin 和评估资产 |
| 真正带来结果的动作 | 将会话生命周期、质量门禁、记忆持久化和工具适配做成可管理模块 |
| 可迁移做法 | 对本仓 skill、hook、配置和脚本分别记录所有权、风险和验证 |
| 不可迁移条件 | 不把 hooks、MCP、全局配置同步或权限扩大直接引入用户环境 |

## 改良迭代

| 改良目标 | 本仓版本 | 验证指标 |
|:---|:---|:---|
| 配置治理 | 公开配置只保留模板，用户配置先备份 | 可回滚且不含本机路径/密钥 |
| Harness 分层 | skills、rules、contexts、hooks 分开说明 | 用户知道每层改变什么 |
| 评估与回归 | 对自动化方法保存失败样本和比较指标 | 不用主观体验宣布优化 |
| 跨工具适配 | Codex 主线、OpenCode 备选各自维护 | 不把兼容脚本误当官方能力 |

## 可迁移清单

- 将记忆、规则、技能、hook 和插件看作不同资产。
- 为全局安装和项目本地安装提供不同风险说明。
- 为配置同步实现备份、所有权清单、dry-run 和恢复路径。
- 对 Agent Harness 性能优化保留 benchmark 和成本证据。

## 不可迁移清单

- 不执行 ECC 的安装、hook 或配置同步脚本。
- 不把其 Codex plugin 或 legacy sync 作为本仓用户的默认安装路径。
- 不复制大量供应商特定 rules/skills 到本仓。

## 验证动作

| 动作 | 成功信号 | 失败信号 |
|:---|:---|:---|
| 审查一个外部 hook | 明确触发点、权限、写入位置和关闭方式 | 只看文件名就安装 |
| 审查 Codex 配置同步 | 先备份、只修改拥有字段、可 dry-run 和恢复 | 覆盖用户配置且无 manifest |
| 审查性能优化 | 有 token、延迟、成本或上下文指标 | 只写“更快/更省” |

## 沉淀判断

“Harness 资产必须按规则、上下文、技能、hook、插件和记忆分层，并绑定权限与回滚”适合下沉到 tools/config、skills 和 docs/gongfa。
