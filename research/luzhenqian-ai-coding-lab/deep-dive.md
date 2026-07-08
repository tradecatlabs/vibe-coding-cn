# luzhenqian/ai-coding-lab 深度研究

## 研究级别

- 当前级别：L2 源码/结构深度研究。
- 研究对象：`luzhenqian/ai-coding-lab`。
- 证据来源：本目录 `raw/` 下的 GitHub 元数据、README 快照和本地仓库工作树。
- 观察日期：2026-07-03。

## L2 结论

`luzhenqian/ai-coding-lab` 是项目实验室型仓库。它用多个独立项目覆盖 Vibe Coding、Skills、RAG、
Chatbot、Agent、creative 等方向，核心价值是把 AI Coding 学习从“读概念”转成“选项目、跑项目、
改项目”的实践矩阵。

对本仓最有价值的是项目分组和难度梯度；最明显的问题是各项目质量和完成度可能不均，必须逐项目
验证，不能因为目录完整就默认可用。

## 源码证据

- `raw/repository/README.md`：项目矩阵入口，按方向、难度和产出组织。
- `raw/repository/vibe-coding/bio-link-page/README.md`：零基础个人主页项目。
- `raw/repository/vibe-coding/nextjs-blog/`：Next.js 博客项目。
- `raw/repository/vibe-coding/nextjs-blog-comment/`：博客评论项目。
- `raw/repository/vibe-coding/flow-board/`：看板项目。
- `raw/repository/skills/README.md`：Claude Skills 实战。
- `raw/repository/skills/packages/`：打包后的 skills。
- `raw/repository/skills/prompts/`：skills 评测提示词。
- `raw/repository/rag/ask-book/`：RAG 问答项目。
- `raw/repository/chatbot/mnemo/`：记忆聊天助手项目。
- `raw/repository/agent/repo-analyzer/README.md`：仓库分析 Agent 教学项目。
- `raw/repository/agent/mastra-orchestration/`：Agent 编排项目。
- `raw/repository/creative/cover-generator/README.md`：封面生成器项目。

## 关键机制

### 项目矩阵优先于线性课程

这个仓库允许读者按兴趣选择项目，不强制从第一章读到最后一章。它适合已经知道方向、想直接动手的
读者，也适合作为教程仓库的实践层。

### 难度和产出写在入口

README 中每个项目都有难度和“你将做出什么”。这比只列目录更有效，因为读者能立即判断投入成本和
产出价值。

### Skills 被做成独立实践对象

`skills/` 不只是解释概念，还包含 Skill 源文件、打包 zip、评测提示词和 API 调用 demo。
这对本仓很重要：skill 应该有可验证产物，而不是只写一段方法论。

### Agent 项目强调模式教学

`agent/repo-analyzer/README.md` 明确标出 Tool Calling、Workflow 和 Human-in-the-Loop，
说明好项目不是只展示成品，还要把背后的 agent 模式讲清。

## 可迁移模式

- 本仓可以建立“实践项目矩阵”，按 Vibe Coding、Skills、RAG、Agent、Workflow、Ops 分类。
- 每个实践项目必须写清难度、产出、前置条件、运行命令和验收方式。
- Skills 目录应补齐测试提示词、打包产物说明和调用示例。
- Agent 示例应显式标注 Tool Calling、Workflow、HITL、Memory、RAG 等模式。
- 项目型资料进入本仓前必须跑最小验证，不能只凭 README 判断。

## 对本仓的影响

本仓当前更强的是知识、研究和治理；AI Coding Lab 更强的是项目样例。合理结合方式是：

- concepts 解释概念。
- workflow 给流程。
- references 给模板。
- research 保留研究。
- 新增或强化 practice/examples 层承载可运行项目。

如果暂不新增目录，也可以先在 `docs/workflow/` 或 `docs/getting-started/` 中增加实践索引。

## 风险和待验证项

- 本轮没有逐个运行项目。
- 部分目录可能保留 create-next-app 默认 README，说明项目文档完成度不均。
- 多技术栈项目会引入较高维护成本，本仓不应直接复制代码。

## 下一步 L3 验证任务

- 优先验证 `skills/` 和 `agent/repo-analyzer/` 两个项目，因为它们最贴近本仓方向。
- 建立本仓实践项目准入清单：能运行、能解释、能验收、能维护。
- 从 `skills/` 抽取 Skill 打包和评测模式，回补本仓 `skills/` 治理。
- 将项目矩阵结构沉淀为 `docs/references/` 中的实践项目模板。
