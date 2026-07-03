# ShouZhengAI/CS146S_CN 深度研究

## 研究级别

- 当前级别：L2 源码/结构深度研究。
- 研究对象：`ShouZhengAI/CS146S_CN`。
- 证据来源：本目录 `raw/` 下的 GitHub 元数据、README 快照和本地仓库工作树。
- 观察日期：2026-07-03。

## L2 结论

`ShouZhengAI/CS146S_CN` 是课程和 assignments 驱动的 AI 软件工程学习仓库。它把 coding LLM、
提示工程、coding agent、MCP、AI IDE、agent 模式、现代终端、测试安全、软件支持、UI 自动化等
主题按周次组织，并为部分周次提供作业、测试、Makefile 和最小全栈项目。

对本仓最有价值的是“课程周次 + 作业验证”的结构：它证明 AI Coding 教程不能只讲方法，还需要
作业、测试和评分标准来逼近真实能力。

## 源码证据

- `raw/repository/README.md`：课程简介、教学大纲、周次主题、阅读材料和作业入口。
- `raw/repository/Assignments/README.md`：作业环境和安装说明。
- `raw/repository/Assignments/pyproject.toml`：Python 依赖和作业工程入口。
- `raw/repository/Assignments/week1/README.md`：提示工程练习说明。
- `raw/repository/Assignments/week1/k_shot_prompting.py`：K-shot prompting 作业。
- `raw/repository/Assignments/week1/chain_of_thought.py`：Chain-of-thought 作业。
- `raw/repository/Assignments/week1/tool_calling.py`：Tool calling 作业。
- `raw/repository/Assignments/week1/self_consistency_prompting.py`：Self-consistency 作业。
- `raw/repository/Assignments/week1/rag.py`：RAG 作业。
- `raw/repository/Assignments/week1/reflexion.py`：Reflexion 作业。
- `raw/repository/Assignments/week2/assignment.md`：AI IDE 初探作业。
- `raw/repository/Assignments/week2/tests/test_extract.py`：作业测试。
- `raw/repository/Assignments/week4/Makefile`：周次作业命令入口。
- `raw/repository/Assignments/week5/README.md`：最小全栈 agent-driven workflow starter。
- `raw/repository/Assignments/week7/README.md`：带分页、排序、PATCH 等增强的全栈练习。
- `raw/repository/Resource/completed/coding_agent_from_scratch_lecture.py`：coding agent from scratch 完成练习。
- `raw/repository/Resource/completed/simple_mcp.py`：MCP 示例。
- `raw/repository/Resource/completed/design_doc_template.md`：设计文档模板。

## 关键机制

### 周次化让复杂主题可消化

AI 软件工程覆盖范围很大。这个仓库用周次把主题拆成提示工程、agent 架构、IDE、agent 模式、
终端、测试安全和 UI 自动化等模块，降低了学习路径的认知负担。

### Assignments 是能力验证层

week1 要求修改 TODO、运行模型、保存输出，week2 有测试文件，week4/5/7 有 Makefile 和最小全栈
项目。这比纯阅读更能验证学习者是否真的掌握。

### 本地模型和工具调用被前置

week1 使用 Ollama 和多种 prompting 技术，说明课程试图让学习者理解模型行为，而不是只调用在线
产品。对本仓来说，这提醒我们：底层概念要有可操作练习。

### 工程作业逐步逼近真实开发

week5 和 week7 的 FastAPI、SQLite、pytest、pre-commit、ruff、black、PATCH、分页排序等内容，
把 AI Coding 从“生成代码”带入“维护小型软件系统”的范围。

## 可迁移模式

- 本仓可以为 getting-started 增加 assignments 风格练习，而不是只给阅读路径。
- 每个关键概念配一个最小任务和验收方式：prompt、tool calling、RAG、MCP、agent workflow。
- 进阶路径应加入测试、安全、终端、部署后运维、UI 自动化等主题。
- 作业应尽量包含 `Makefile`、测试命令和预期结果，便于 AI 和人共同验证。
- 课程材料和作业材料要分层，避免正文变成资料堆。

## 对本仓的影响

本仓已经有知识库和质量门禁，但练习层还不够强。CS146S_CN 的价值在于提醒本仓：

- 学习路径需要“读完知道”。
- 作业路径需要“做完证明”。
- 门禁路径需要“跑完通过”。

这三层合起来，才是完整的 AI Coding 教育闭环。

## 风险和待验证项

- 部分周次作业状态仍在进行中，不能把课程计划当作已完成事实。
- 本轮没有运行作业测试、Ollama 模型或全栈 starter。
- 课程面向有一定编程基础的学习者，不完全等同于零基础教程。

## 下一步 L3 验证任务

- 选择 week1 prompting 作业作为最小验证对象，检查测试和运行路径。
- 将周次主题映射到本仓 getting-started / concepts / workflow。
- 设计本仓自己的最小 assignments：prompt、tool calling、RAG、MCP、agent workflow。
- 将设计文档模板和 agent from scratch 练习转成 references 候选材料。
