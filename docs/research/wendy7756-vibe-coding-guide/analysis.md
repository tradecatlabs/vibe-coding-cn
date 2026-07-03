# wendy7756/vibe-coding-guide 研究分析

## 本轮结论

- 这是面向非程序员的自然语言编程指南，价值在低门槛表达、工具解释和工作流概念化。
- 它把 IDEs and Tools、LLMs、Prompts、my-experience 分目录组织，适合观察非工程读者需要什么上下文。
- 本仓应吸收其“自然语言描述 -> AI 生成 -> 执行观察”的解释框架，但工程交付标准仍需更严格。

## 本地证据

- 研究对象：`wendy7756/vibe-coding-guide`
- 当前研究角色：非程序员自然语言编程指南
- 本轮成熟度：L1 初步理解
- 原始仓库：`raw/repository/`
- 原始来源清单：`raw/sources.yml`
- 事实摘要：`domain.yml`

## 结构观察

- 根目录包含 `IDEs-and-Tools/`、`LLMs/`、`Prompts/`、`my-experience/`、`README.md`、`README_EN.md`。
- README 包含什么是 Vibe Coding、核心定义、起源发展、技术基础、核心工作流程。
- 目录面向学习者，不是工具源码。

## 可借鉴点

- 非程序员入口要先解释语言、工具、模型和提示词之间的关系。
- 经验目录能补足正式教程缺少的真实使用感。
- 中英文 README 可以作为术语表达对照。

## 风险和边界

- 概念解释多，工程验证少。
- 非程序员视角可能弱化测试、版本控制和回滚。
- 需要避免把经验性表述上升为工程原则。

## 下一轮研究任务

- 抽取非程序员路径中的关键障碍，反馈到本仓 getting-started。
- 对照其 Prompts 目录，筛选可进入 prompts 表格的提示词模式。

## 沉淀判断

- 本轮只完成 L1 理解，不直接迁入 concepts、references、workflow 或 skills。
- 只有经过 L2 源码阅读、实验验证或交叉对照后的结论，才进入稳定层。