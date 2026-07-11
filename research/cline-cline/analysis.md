# cline/cline 研究分析

## 本轮结论

`cline/cline` 的核心价值不是“VS Code 插件怎么做”，而是展示了成熟 agent 产品会从单入口扩展成
IDE、CLI、SDK、rules、skills、examples、evals 和发布脚本共同组成的平台。

本仓最应该迁移的是入口契约：人类阅读入口、AI 上下文入口、脚本入口、skill 入口、资源入口和
metadata 入口不能各自为政，必须写清输入、输出、owner、验证命令和更新策略。

## 本地证据

- 研究对象：`cline/cline`
- 当前研究角色：IDE/SDK/CLI 自主编码 Agent
- 原始仓库：`raw/repository/`
- 原始来源清单：`raw/sources.yml`
- 事实摘要：`domain.yml`
- 深度证据：`deep-dive.md`

## 对标拆解

| 项 | 内容 |
|:---|:---|
| 参考对象 | `cline/cline` |
| 它解决的核心问题 | 让 agent 能力跨 IDE、CLI、SDK、规则、技能、示例和评估保持一致 |
| 核心机制 | `apps/` 多入口，`sdk/` 可复用能力，`.clinerules/` 规则，`.agents/skills` 技能，`evals/` 评估 |
| 真正带来结果的动作 | 把入口和规则文件化，让不同使用表面共享同一套行为边界 |
| 可迁移做法 | 为本仓所有入口建立入口矩阵和更新契约 |
| 不可迁移条件 | 不复制 VS Code 插件、SDK、hub 服务或复杂前端 UI |
| 下一步试用动作 | 梳理人类入口、AI 入口、脚本入口、skill 入口、资源入口和 metadata 入口 |

## 改良迭代

| 改良目标 | 原模式 | 本仓版本 | 验证指标 |
|:---|:---|:---|:---|
| 多入口一致性 | Cline 用 apps/sdk/rules/examples 承载不同入口 | 本仓用 README、AGENTS、llms、metadata、scripts、skills 协同 | 新入口新增时能找到 owner 和验证命令 |
| 规则文件化 | Cline 用 `.clinerules/` 固化 agent 行为 | 本仓用根和目录级 `AGENTS.md` 固化规则 | 架构变更后规则同步 |
| 示例驱动 | Cline 用 examples 展示 SDK/agent 用法 | 本仓为关键 workflow 和 skills 增加最小示例 | 用户能按示例复现流程 |

## 可迁移清单

- 写一张入口矩阵：入口、目标读者、输入、输出、owner、验证命令、更新触发。
- 把 `llms.txt`、`llms-full.txt`、`metadata/taxonomy.yml` 作为 AI 入口，而不是附属文件。
- 把 `scripts/` 和 `skills/` 作为执行入口，明确自动执行边界。
- 为关键 workflow 增加最小示例，避免只写原则。

## 不可迁移清单

- 不提前建设 SDK 或 hub 服务。
- 不为“平台感”增加不必要目录和运行时。
- 不把多入口扩张理解成所有能力都要产品化；本仓优先做文档和 Agent 可读入口一致性。

## 验证动作

| 动作 | 成功信号 | 失败信号 |
|:---|:---|:---|
| 建立入口矩阵 | 任意入口变更能找到同步位置 | 新增入口后 README、metadata、llms 漂移 |
| 抽样一个 skill 写清输入输出和验证 | Agent 能按规则触发和验证 | skill 只是 prompt 文本 |
| 抽样一个 workflow 增加最小示例 | 用户能复现流程 | 只能理解原则，不能操作 |

## 沉淀判断

- 稳定结论应下沉到 `docs/references/` 的多入口仓库结构模板或 `docs/workflow/` 的入口维护规则。
- `deep-dive.md` 保留源码证据；本文件负责把证据转成迁移动作。
