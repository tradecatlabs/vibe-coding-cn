# tradecatlabs/vibe-coding-cn 研究分析

## 本轮结论

`tradecatlabs/vibe-coding-cn` 作为自研究域，价值不是自我表扬，而是用外部成熟样本反向校准自身。
本仓已经具备 docs、prompts、skills、assets、tools、metadata、scripts、AGENTS、llms 和质量门禁，
但真正的下一步是把这些入口变成“AI 原生知识库控制面”。

本仓最应该迁移的是自我审计机制：每次外部研究都必须反问本仓哪里该改、哪里不能膨胀、如何验证改动有效。

## 本地证据

- 研究对象：`tradecatlabs/vibe-coding-cn`
- 当前研究角色：中文主线工程化工作流
- 原始仓库：`raw/repository/`
- 原始来源清单：`raw/sources.yml`
- 事实摘要：`domain.yml`
- 深度证据：`deep-dive.md`

## 对标拆解

| 项 | 内容 |
|:---|:---|
| 参考对象 | `tradecatlabs/vibe-coding-cn` |
| 它解决的核心问题 | 用中文知识库、提示词、技能、资源和门禁组织 Vibe Coding 学习与实践 |
| 核心机制 | `docs/`、`prompts/`、`skills/`、`assets/`、`metadata/`、`scripts/`、`AGENTS.md`、`llms.txt` |
| 真正带来结果的动作 | 把文档知识库工程化，让 AI 和人类都能稳定读取、验证和交付 |
| 可迁移做法 | 自我研究、索引门禁、AI 引用入口、raw 事实层、资源治理 |
| 不可迁移条件 | 不因外部平台化项目而过早变成应用仓库或工具平台 |
| 下一步试用动作 | 用研究迁移综合驱动 scripts、resources、workflow、skills 的下沉任务 |

## 改良迭代

| 改良目标 | 原模式 | 本仓版本 | 验证指标 |
|:---|:---|:---|:---|
| 自我审计 | 外部研究后停留在 research | 每个研究结论映射到本仓改动或不采用理由 | 研究能产生下游任务 |
| 控制面 | docs/prompts/skills/assets/scripts 分散 | AI 原生知识库控制面 | 入口、owner、验证命令清楚 |
| 防膨胀 | 看到外部结构就想复制 | 只迁移机制，不复制外壳 | 新增对象有存在性证明 |

## 可迁移清单

- 将 Codex 的执行控制面迁移到 scripts 治理。
- 将 Aider 的 Git 闭环迁移到 workflow。
- 将 Cline 的多入口契约迁移到 README/AGENTS/llms/metadata。
- 将 awesome-claude-code 的资源治理迁移到 assets。
- 将 Claude Code Best Practice 的方法论资产化迁移到 concepts/workflow/skills。

## 不可迁移清单

- 不把本仓变成 Codex/Cline 类产品。
- 不把每个外部仓库结构都复制到本仓。
- 不让 research 无限变厚；成熟结论必须下沉。
- 不用自研究替代外部交叉审计。

## 验证动作

| 动作 | 成功信号 | 失败信号 |
|:---|:---|:---|
| 为 P1 研究结论建立下游任务 | 每条结论有目标位置和验收 | 研究停在总结 |
| 检查新增入口的同步链 | README、metadata、llms、AGENTS 同步 | 新入口只有一个文件知道 |
| 抽样一次自我审计 | 能指出应该删减或不做什么 | 只会增加新目录 |

## 沉淀判断

- 稳定结论进入 `research/research-transfer-synthesis.md`、`docs/workflow/`、`scripts/` 和 `assets/`。
- 本研究域保持 P1 自我校准对象。
