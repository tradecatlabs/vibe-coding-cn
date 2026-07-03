# mindfold-ai/Trellis 研究分析

## 本轮结论

`mindfold-ai/Trellis` 的核心价值不是“又一个 AI 编程提示词集合”，而是把 AI 编程的关键过程做成
仓库内控制面：规格注入、任务状态、上下文清单、会话记忆、验证 Agent、多平台适配和可升级模板。

本仓最应该迁移的是它的对象化治理方式：把上下文、约束和验证从聊天窗口中抽离出来，落到仓库文件、
脚本和索引中，让不同 Agent 在不同会话中仍然执行同一套工作流。对本仓而言，最有价值的迁移方向是：

- 把 `docs/research/` 的研究域继续强化为“对象目录 + raw 事实层 + 分析层 + 深度层 + 索引层”。
- 把 `docs/research/harness/` 的概念研究补成任务、规格、记忆、验证四件套的控制面清单。
- 把 `.trellis/tasks/` 的任务 artifact 思想迁移到重要文档任务：目的、约束、验收、验证命令和证据。
- 把 `.trellis/spec/` 的规格注入思想迁移到本仓 AGENTS、README、llms 和 module context 的同步策略。
- 把 `trellis-check`、`trellis-update-spec` 的收尾机制迁移为“验证后沉淀经验”的固定闭环。

## 本地证据

- 研究对象：`mindfold-ai/Trellis`
- 当前研究角色：跨平台 Agent Harness 框架、CLI 与任务/规格/记忆系统
- 原始仓库：`raw/repository/`
- 原始来源清单：`raw/sources.yml`
- 事实摘要：`domain.yml`
- 深度证据：`deep-dive.md`

## 对标拆解

| 项 | 内容 |
|:---|:---|
| 参考对象 | `mindfold-ai/Trellis` |
| 它解决的核心问题 | AI 编程会话从零开始、规则分散、任务状态不稳定、验证闭环弱、多平台配置割裂、跨会话记忆无法复用 |
| 核心机制 | `.trellis/spec/`、`.trellis/tasks/`、`.trellis/workflow.md`、`.trellis/workspace/`、平台配置生成器、`channel` runtime、`mem` 检索、`task` schema |
| 真正带来结果的动作 | 把规则、任务、上下文、验证和会话历史变成仓库内可读、可执行、可升级的 artifact |
| 可迁移做法 | 规格注入、任务 artifact、jsonl 上下文清单、workflow breadcrumb、finish-work 收尾、spec update、跨平台适配矩阵 |
| 不可迁移条件 | 不复制 AGPL 代码或模板；不把本仓改造成 Trellis 运行时；不为了完整性引入过重的 CLI/runtime 所有权面 |
| 下一步试用动作 | 为本仓设计一份“任务 artifact 最小契约”：目标、约束、上下文清单、验证命令、沉淀路径和交接摘要 |

## 改良迭代

| 改良目标 | 原模式 | 本仓版本 | 验证指标 |
|:---|:---|:---|:---|
| 上下文稳定 | Trellis 用 `.trellis/spec/` 和 jsonl 清单给 Agent 注入规则 | 本仓用 AGENTS、README、llms、研究域索引和 raw 事实层形成上下文路由 | 新会话能不用聊天记录也理解目录边界和验证路径 |
| 任务可恢复 | Trellis 每个任务有 PRD、设计、实现计划、上下文清单和状态 | 本仓重要研究/文档任务使用对象目录和分析层记录目的、证据、验收 | 中断后可从文件恢复下一步 |
| 验证闭环 | `trellis-check` 检查 diff，`trellis-update-spec` 沉淀新规则 | 本仓用 `make test`、链接检查、结构检查和研究域审计作为收尾门禁 | 交付前有可复跑命令和失败修复路径 |
| 多平台一致 | CLI 生成 Claude、Codex、Cursor、OpenCode 等平台配置 | 本仓维护根 `AGENTS.md`、`llms.txt`、`assets/ai-citation/llms-full.txt` 和工具配置入口 | 不同 AI 工具读取到同一套项目事实 |
| 会话记忆 | `mem` 检索 Claude、Codex、OpenCode、Pi 会话 | 本仓将稳定经验写入文档、研究域和技能，而不是依赖聊天历史 | 同类问题能被文档和索引复用 |

## 可迁移清单

- 规格不靠记忆：项目规则必须写入仓库文件，并通过明确入口被 Agent 加载。
- 任务不靠聊天：复杂任务必须有目标、上下文、验收、验证、状态和交接。
- 上下文不全量塞入：用清单声明哪些文件为什么进入当前任务，减少噪声。
- 状态不靠自觉：用 workflow phase 或检查清单强制计划、执行、验证、沉淀的顺序。
- 验证不靠同一上下文自信：实现后必须有独立检查层，重要结论要能交叉审计。
- 经验不只复盘：失败、约束和新模式要回写到规范层，让下一次自动加载。
- 平台不各自为政：Claude、Codex、Cursor 等入口应共享同一项目事实，不维护冲突规则。
- runtime 不默认引入：通道、worker 和会话检索机制值得研究，但本仓先采用轻量文档控制面。

## 不可迁移清单

- 不直接复制 Trellis 的 AGPL-3.0 代码、模板、hook 或脚本。
- 不把 `.trellis/` 原样引入本仓作为新的真相源，除非先完成许可证、维护成本和门禁评估。
- 不把多平台生成器当成所有项目的必选项；小型知识库先维护少量明确入口。
- 不把 channel runtime 当成当前本仓必需能力；只有出现真实多 Agent 并发协作需求时再评估。
- 不用复杂状态机替代清晰文档；只有任务会跨会话、跨 Agent 或需要审计时才提升治理等级。

## 验证动作

| 动作 | 成功信号 | 失败信号 |
|:---|:---|:---|
| 为本仓设计任务 artifact 最小契约 | 新会话能从文件读出目标、约束、上下文和验证 | 仍需要翻聊天记录才能继续 |
| 对现有研究域做一次 Trellis 式上下文清单审计 | 每个研究域都有事实层、分析层、索引层和沉淀路径 | 研究报告读完仍不知道可应用什么 |
| 抽取一条新增经验并回写到稳定入口 | 后续 Agent 能自动读取并执行 | 经验只留在本次回答里 |
| 评估多平台入口一致性 | `AGENTS.md`、`llms.txt`、`llms-full.txt` 指向一致 | 不同入口对项目结构说法冲突 |

## 沉淀判断

- 稳定概念进入 `docs/research/harness/` 和 `docs/workflow/`。
- 可执行任务 artifact 契约成熟后，可进入 `docs/references/` 或 `scripts/`。
- 与 Skill、Agent、workflow 相关的可复用能力成熟后，再考虑进入 `skills/`。
- 本研究域保持 P1，对齐 Agent Harness、任务控制面和多平台 AI 编程运行时。
