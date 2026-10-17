# continuedev/continue 研究分析

## 本轮结论

Continue 的公开 README 已明确说明仓库不再主动维护，并以最终 2.0.0 版本作为当前状态。因此它不应作为本仓现行工具推荐，而应作为“IDE/CLI coding agent 经过产品生命周期收束后的架构和迁移案例”保留研究价值。

## 本地证据

- raw/github-readme.raw.md.txt：只读/停止维护声明、最终 2.0.0、CLI、VS Code 和 JetBrains 入口。
- raw/repository/.continue/：agents、checks、prompts 和 rules。
- raw/repository/core/：context、commands、config、tools、LLM 和 indexing。
- raw/repository/extensions/、packages/、binary/：多入口和适配层。
- raw/repository/eval/：评估入口和测试资产。

## 对标拆解

| 项 | 内容 |
|:---|:---|
| 参考对象 | continuedev/continue |
| 核心问题 | 在 IDE、CLI 和多模型配置之间共享 coding agent 能力 |
| 核心机制 | core、extensions、packages、.continue agents/checks/rules 和 eval |
| 真正带来结果的动作 | 将上下文、命令、模型、工具和入口分层 |
| 可迁移做法 | 研究上下文来源、配置 schema、检查 agent 和入口生命周期 |
| 不可迁移条件 | 不把已停止维护的仓库作为当前安装或推荐路线 |

## 改良迭代

| 改良目标 | 本仓版本 | 验证指标 |
|:---|:---|:---|
| 维护状态 | 研究域明确标注只读/最终版本 | 索引不会误导为最新产品 |
| 上下文规则 | 将 AGENTS、技能、项目文档和临时错误分层 | 规则不会被一次对话覆盖 |
| 破坏性变更 | 保留 stale reference 检查思路 | 命令、API、配置重命名有影响面检查 |
| IDE 边界 | IDE 是承载入口，不替代 CLI 和质量门禁 | 教程不依赖某个编辑器 |

## 可迁移清单

- 为配置变更扫描过期引用、文档和测试。
- 把 context、commands、tools、models 和 indexing 分开分析。
- 对已停止维护的项目降低推荐等级，保留迁移和历史价值。
- 使用 checks/agents 形式沉淀可重复审查问题。

## 不可迁移清单

- 不将 Continue 2.0.0 写成当前主线工具。
- 不复制 IDE 插件、匿名遥测或已停止维护的配置。
- 不把 repository 的大量模块当作本仓需要的目录。

## 验证动作

| 动作 | 成功信号 | 失败信号 |
|:---|:---|:---|
| 检查研究索引 | 明确显示只读状态和观察日期 | 读者误以为仍在活跃迭代 |
| 抽样 breaking-change agent | 能发现命令/API/config 的陈旧引用 | 只审代码不审文档和配置 |
| 比较 IDE 与 CLI 入口 | 清楚共享层和适配层 | 将入口产品等同于 Agent 核心 |

## 沉淀判断

“研究域必须把维护状态纳入推荐判断”应补充 research-domain-contract.md；Continue 的具体架构只保留在研究域。
