# mindfold-ai/Trellis 深度研究

## 一句话判断

Trellis 的底层设计是：把 AI 编程从“聊天驱动”改造成“仓库控制面驱动”，让任务、规格、上下文、
会话、验证和平台适配都成为可版本化对象。

## 结构拆解

| 层级 | 关键对象 | 作用 |
|:---|:---|:---|
| 仓库控制面 | `.trellis/` | 承载 workflow、spec、tasks、workspace、scripts、config，是 Agent 行为的本地真相源。 |
| 任务层 | `.trellis/tasks/{MM-DD-name}/` | 每个任务保存 `task.json`、`prd.md`、`design.md`、`implement.md`、`implement.jsonl`、`check.jsonl`。 |
| 规格层 | `.trellis/spec/` | 按 package/layer 管理编码规范、质量规则、架构约束和思考指南。 |
| 状态层 | `.trellis/workflow.md` | 定义 Plan、Execute、Finish 相位和 per-turn workflow-state breadcrumb。 |
| 记忆层 | `.trellis/workspace/` 与 `mem` | 保存会话日志，并从 Claude、Codex、OpenCode、Pi 等历史会话中检索上下文。 |
| 适配层 | `.claude/`、`.codex/`、`.cursor/`、`.opencode/` 等 | 把同一套 Trellis 工作流渲染到不同 AI coding 平台。 |
| runtime 层 | `channel`、worker、supervisor、event log | 支撑多 Agent 协作、消息路由、上下文挂载、worker 生命周期和中断。 |

## 关键机制

### 1. 规格注入，而不是模型记忆

Trellis 的 `.trellis/spec/` 把团队规则拆成 package 和 layer，再通过任务的 `implement.jsonl`、`check.jsonl`
选择性注入给实现 Agent 与检查 Agent。这里的关键不是“多写文档”，而是让文档参与运行时：

- spec 是长期规则；
- task artifact 是短期目标；
- jsonl manifest 是本次任务需要加载的上下文清单；
- implement/check Agent 只读与本次任务相关的部分，避免上下文膨胀。

对本仓的启示：`AGENTS.md`、`README.md`、`llms.txt`、`assets/ai-citation/llms-full.txt` 和研究域索引必须保持一致。
它们不是说明书，而是 AI 进入仓库时的上下文入口。

### 2. 任务是执行单元，不是聊天片段

Trellis 的任务目录把“要做什么”拆成可恢复 artifact：

- `task.json` 保存 24 字段的规范任务记录，包含 status、priority、assignee、branch、commit、PR、parent/children 等。
- `prd.md` 保存需求、约束和验收。
- `design.md` 保存边界、契约、数据流和取舍。
- `implement.md` 保存执行顺序、验证命令、review gate 和回滚点。
- `implement.jsonl`、`check.jsonl` 保存进入实现/检查阶段的上下文文件和原因。

对本仓的启示：复杂研究和文档治理任务不能只靠聊天推进。至少要能在文件里回答：目标是什么、上下文在哪里、
验收是什么、验证命令是什么、未完成项是什么。

### 3. workflow breadcrumb 把状态注入每一轮

Trellis 在 `.trellis/workflow.md` 中维护 `[workflow-state:STATUS]` 块，并通过 hook 在每轮用户输入时注入当前状态。
这解决的是 Agent 常见失败：忘记先计划、忘记进入检查、忘记提交前验证、忘记收尾沉淀。

关键设计点：

- `no_task` 要求先判断是否创建任务。
- `planning` 要求轻量任务至少有 PRD，复杂任务补齐 `design.md` 和 `implement.md`。
- `in_progress` 明确实现、检查、更新 spec、commit、finish-work 的顺序。
- Codex 可以走 inline 变体，适配平台子 Agent 隔离问题。

对本仓的启示：工作流规则不应该只写在长文档深处，而应出现在 Agent 每次开始任务时必读的位置。

### 4. 多平台适配不是复制多份规则

Trellis 的 `AI_TOOLS` registry 把 Claude Code、Cursor、OpenCode、Codex、Kilo、Kiro、Gemini、Antigravity、
Devin、Qoder、CodeBuddy、Copilot、Droid、Pi、Reasonix、ZCode、Trae 等平台统一成配置对象。
平台差异被压到 configurator、template 和 hook 能力矩阵中，核心工作流保持一致。

对本仓的启示：多 AI 工具支持应该有一个事实中心。根 `AGENTS.md`、`llms.txt`、`assets/ai-citation/llms-full.txt`
和工具目录不能各讲各的。

### 5. channel runtime 把多 Agent 协作变成事件系统

Trellis 的 `channel` API 暴露 channel、thread、message、context、worker、inbox、interrupt、watch、supervisor 等能力。
CLI 侧提供 `create`、`send`、`wait`、`interrupt`、`spawn`、`run`、`list`、`messages`、`kill`、`post` 等命令。

这说明 Trellis 对 Agent 协作的理解不是“开几个窗口”，而是：

- 共享事件日志；
- 明确 worker 身份；
- 消息有发送者、目标、线程和 delivery mode；
- 上下文可以挂到 channel 或 thread；
- supervisor 管理 worker 生命周期、空闲清理、超时和中断。

对本仓的启示：如果未来真的要做多 Agent 协同研究或 tmux worker 编排，应该优先采用“事件日志 + worker 状态 + 上下文挂载”
的模型，而不是只靠口头分工。

### 6. mem 把历史会话变成可检索材料

Trellis 的 `mem` 子系统从 Claude、Codex、OpenCode、Pi 等平台读取会话，提供 list、search、context、extract、projects。
它的重点不是把所有聊天永久塞回提示词，而是让 Agent 能检索过去发生过的事实、决策和问题。

对本仓的启示：聊天记录可以辅助检索，但稳定知识必须进入仓库文档。真正的长期记忆不是“记住一切”，
而是把有价值的经验晋升到可维护结构。

## 可迁移模式

### 模式一：任务 artifact 最小契约

本仓可以设计轻量版任务契约，不需要引入完整 Trellis runtime：

| 字段 | 最小含义 |
|:---|:---|
| 目的 | 本次任务要改变什么结果。 |
| 对象 | 涉及哪些文件、目录、研究域或流程。 |
| 约束 | 哪些地方不能动、哪些事实必须核验。 |
| 上下文 | 当前任务必须读取的文件和原因。 |
| 验收 | 什么状态算完成。 |
| 验证 | 可复跑的命令、检查或人工审计动作。 |
| 沉淀 | 哪些结论要进入 README、AGENTS、llms、research 或 skills。 |

### 模式二：规格入口一致性

本仓已有多个 AI 入口。Trellis 的启示是：入口可以多，事实只能一个。

最低要求：

- 根 `AGENTS.md` 说明仓库操作规则。
- `llms.txt` 提供短上下文入口。
- `assets/ai-citation/llms-full.txt` 提供完整 AI 引用入口。
- `docs/research/README.md` 和 `docs/README.md` 提供研究域索引。
- 新增研究域必须同步进入 metadata 和 llms。

### 模式三：验证后更新规格

Trellis 的 `trellis-update-spec` 思路可以转成本仓收尾规则：

1. 完成修改。
2. 运行质量门禁。
3. 如果发现新的稳定规则、坑、流程或边界，回写到对应 AGENTS、README、docs 或 skills。
4. 再提交。

这比“写完总结一下”更强，因为它要求下一次 Agent 能自动读到新规则。

## 不采用 Trellis 的边界

- AGPL-3.0 代码边界：本仓不能直接复制 Trellis 的实现、模板或 hook。
- 项目形态边界：本仓是中文 Vibe Coding 知识库，不是 Trellis runtime 分发包。
- 所有权边界：引入完整 CLI、多平台 configurator 和 channel runtime 会显著增加维护面。
- 需求边界：当前本仓主要需要研究域、文档治理和质量门禁，不需要立即运行 worker supervisor。

## 对本仓的下一步建议

1. 在 `docs/research/harness/` 补一份“Agent Harness 控制面检查清单”。
2. 为复杂文档任务定义轻量任务 artifact 契约。
3. 建立“验证后沉淀规格”的收尾规则，把高频教训写回 AGENTS、README 或 skills。
4. 对多 AI 入口做一致性检查，确保 `AGENTS.md`、`llms.txt`、`llms-full.txt` 和研究索引不漂移。
5. 如果未来需要多 Agent 并发执行，再研究 channel runtime 或 `auto-tmux` 的事件化改造。

## 最小试用动作

下一轮可以选一个真实文档任务试用轻量 Trellis 模式：

1. 写一个任务 artifact，明确目的、对象、约束、上下文、验收和验证。
2. 执行修改。
3. 用独立检查视角审计结果。
4. 把新经验回写到稳定入口。
5. 提交前确认索引和 AI 入口同步。
