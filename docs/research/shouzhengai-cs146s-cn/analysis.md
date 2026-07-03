# ShouZhengAI/CS146S_CN 研究分析

## 本轮结论

`ShouZhengAI/CS146S_CN` 的核心价值是课程化和 assignments。它把 coding LLM、coding agent、AI IDE、
agent 模式、现代终端、测试安全、软件支持和 UI 自动化放进周次节奏，并用作业承接学习。

本仓最应该迁移的是“作业作为验证层”：学习路径不能只给阅读材料，还要给可提交、可检查、可反馈的任务。

## 本地证据

- 研究对象：`ShouZhengAI/CS146S_CN`
- 当前研究角色：中文课程与 assignments
- 原始仓库：`raw/repository/`
- 原始来源清单：`raw/sources.yml`
- 事实摘要：`domain.yml`
- 深度证据：`deep-dive.md`

## 对标拆解

| 项 | 内容 |
|:---|:---|
| 参考对象 | `ShouZhengAI/CS146S_CN` |
| 它解决的核心问题 | 用课程大纲和 assignments 把 AI 软件工程学习变成阶段任务 |
| 核心机制 | 周次大纲、`Assignments/`、`Resource/`、课程主题分层 |
| 真正带来结果的动作 | 让学习者通过作业验证工具、agent、测试和自动化能力 |
| 可迁移做法 | assignments 验证层、阶段学习节奏、测试安全进入进阶路径 |
| 不可迁移条件 | 不复制课程内容，不把课程节奏当生产工程流程 |
| 下一步试用动作 | 为本仓 learning-map 增加最小 assignments 列表 |

## 改良迭代

| 改良目标 | 原模式 | 本仓版本 | 验证指标 |
|:---|:---|:---|:---|
| 阶段学习 | 周次课程大纲 | getting-started 分阶段路线 | 每阶段有任务和验收 |
| 作业验证 | Assignments | 本仓练习任务或 workflow checklist | 用户能提交结果或自检 |
| 进阶主题 | 测试安全、终端、自动化 UI | workflow / references 进阶路径 | 进阶内容不只停留在概念 |

## 可迁移清单

- 为学习路径增加 assignments，而不是只放阅读链接。
- 把测试、安全、自动化 UI 纳入进阶路径。
- 将 prompt、tool calling、RAG、MCP、agent workflow 等主题拆成练习。
- 每个练习提供目标、输入、输出、验证方式和常见失败。

## 不可迁移清单

- 不复制课程内容或作业答案。
- 不把课堂节奏等同于项目交付节奏。
- 不在没有验证路径时扩张练习数量。

## 验证动作

| 动作 | 成功信号 | 失败信号 |
|:---|:---|:---|
| 抽样设计 3 个 assignments | 每个有目标、交付物、验收 | 只是阅读题 |
| 将一个进阶主题转成练习 | 用户能执行并检查结果 | 仍只是概念介绍 |
| 给练习补常见失败 | 卡住时有排查路径 | 失败只能回到问 AI |

## 沉淀判断

- 稳定结论进入 `docs/getting-started/` 和 `docs/workflow/`。
- 本研究域保持 P2 课程 assignments 对标对象。
