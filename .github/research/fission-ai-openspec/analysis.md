# Fission-AI/OpenSpec 研究分析

## 本轮结论

Fission-AI/OpenSpec 提供了另一种规格驱动路径：以变更提案、需求场景、设计和任务作为变更单元，并通过 apply、verify、archive 等动作推进。它强调流动、迭代、brownfield 和多工具适配，适合与 Spec Kit 对照研究，而不是简单二选一。

## 本地证据

- raw/github-readme.raw.md.txt：OpenSpec 的原则、/opsx 工作流、快速开始和支持工具。
- raw/repository/openspec/changes/：变更提案和实施顺序材料。
- raw/repository/openspec/specs/、work/、explorations/：规格、工作区和探索资产。
- raw/repository/schemas/spec-driven/schema.yaml：规格驱动 schema。
- raw/repository/skills/：new、propose、apply、verify、archive 等 skill。
- raw/repository/src/commands/、src/core/：CLI 命令和核心实现。

## 对标拆解

| 项 | 内容 |
|:---|:---|
| 参考对象 | Fission-AI/OpenSpec |
| 核心问题 | 让需求变更先形成可审查的提案和规格，再由 Agent 执行和验证 |
| 核心机制 | explore、propose、apply、verify、archive 与 changes/specs 目录 |
| 真正带来结果的动作 | 变更拥有独立生命周期，实施后把稳定规格同步回主资产 |
| 可迁移做法 | 把“研究结论转入教程”看成有来源、验证和归档的变更 |
| 不可迁移条件 | 不复制其 CLI、遥测、模板和 30+ 工具适配作为本仓依赖 |

## 改良迭代

| 改良目标 | 本仓版本 | 验证指标 |
|:---|:---|:---|
| 变更隔离 | 研究、分析和下沉文档分层保存 | 未验证判断不会直接变成稳定规则 |
| 场景化需求 | 重要方法用行为场景描述 | 读者能判断成功和失败 |
| 归档机制 | 失效研究域保留来源和归档理由 | 不把过期工具继续当推荐 |
| 多工具适配 | 只保留本仓真实使用的入口 | 不为支持数量牺牲清晰度 |

## 可迁移清单

- 给长期研究对象建立提案、验证、下沉和归档状态。
- 用具体场景表达需求和验收，而非只写抽象目标。
- 对 brownfield 修改保留影响面和回滚路径。
- 将工具适配放在边界层，核心方法保持工具中立。

## 不可迁移清单

- 不把 OpenSpec 的推荐模型、版本和 CLI 命令直接写成本仓事实。
- 不运行 raw 中的安装或更新脚本。
- 不把 telemetry 或外部 dashboard 引入本仓文档门禁。

## 验证动作

| 动作 | 成功信号 | 失败信号 |
|:---|:---|:---|
| 抽样一个研究下沉任务 | 有提案、来源、验证、下沉结果和回滚说明 | 研究结论直接覆盖正文 |
| 检查一个场景 | WHEN/THEN 或等价验收明确 | 只有“应该可用” |
| 检查工具适配 | 适配入口与核心内容分离 | 文档被单一工具命令绑死 |

## 沉淀判断

“研究结论进入稳定文档前必须经过变更、验证和归档判断”适合补充研究域契约；OpenSpec 的具体命令留在本研究域。
