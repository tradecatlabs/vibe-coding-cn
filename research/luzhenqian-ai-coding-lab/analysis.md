# luzhenqian/ai-coding-lab 研究分析

## 本轮结论

`luzhenqian/ai-coding-lab` 的核心价值是项目实验室。它用 agent、chatbot、creative、RAG、skills、
vibe-coding 等目录组织实践项目，适合研究如何把 AI Coding 从概念推进到可运行案例。

本仓最应该迁移的是“实践项目作为概念验收层”：概念和方法论如果没有项目验证，很容易变成空话。

## 本地证据

- 研究对象：`luzhenqian/ai-coding-lab`
- 当前研究角色：AI Coding 项目实验室
- 原始仓库：`raw/repository/`
- 原始来源清单：`raw/sources.yml`
- 事实摘要：`domain.yml`
- 深度证据：`deep-dive.md`

## 对标拆解

| 项 | 内容 |
|:---|:---|
| 参考对象 | `luzhenqian/ai-coding-lab` |
| 它解决的核心问题 | 用多个小项目覆盖 AI Coding 的主要实践方向 |
| 核心机制 | `agent/`、`chatbot/`、`creative/`、`rag/`、`skills/`、`vibe-coding/` 项目矩阵 |
| 真正带来结果的动作 | 用项目目录让学习者按方向进入实践 |
| 可迁移做法 | practice/example 层、项目模板、概念到项目的映射 |
| 不可迁移条件 | 不直接采用未验证项目，不把目录名当质量 |
| 下一步试用动作 | 为本仓设计“最小实践项目模板” |

## 改良迭代

| 改良目标 | 原模式 | 本仓版本 | 验证指标 |
|:---|:---|:---|:---|
| 实践矩阵 | 多方向项目目录 | workflow/practice 中按目标组织项目 | 每个项目有目标、运行命令、验收命令 |
| 概念验收 | 项目承接学习 | concepts 后接最小实践 | 概念能被运行或检查 |
| Skill 实验 | `skills/` 目录 | 本仓 skill 有评测和示例 | skill 不只停在说明 |

## 可迁移清单

- 建立最小实践项目模板。
- 让 agent、RAG、chatbot、skills 等方向对应学习分支。
- 每个项目必须有前置条件、运行命令、验收命令和常见失败。
- 将项目作为 L3 沉淀产物的一部分。

## 不可迁移清单

- 不复制项目代码。
- 不把实验室当作生产模板。
- 不新增 practice 层前先无限扩张目录；先用最小模板验证。

## 验证动作

| 动作 | 成功信号 | 失败信号 |
|:---|:---|:---|
| 设计一个最小实践项目模板 | 模板能指导新项目落地 | 只有项目标题无运行命令 |
| 抽样一个概念映射到练习 | 用户能通过练习验证概念 | 概念仍只能阅读 |
| 抽样一个 skill 增加示例 | 示例能复现 skill 行为 | skill 无法验证 |

## 沉淀判断

- 稳定结论进入 `docs/workflow/`，后续可引出独立 practice/examples 层。
- 本研究域保持 P2 实践项目对标对象。
