# datawhalechina/easy-vibe 研究分析

## 本轮结论

`datawhalechina/easy-vibe` 的核心价值是课程产品化：它不是单篇教程，而是把 Vibe Coding 按用户目标、
学习阶段、站点化文档、AI 可读入口和课程资源组织成可持续学习系统。

本仓最应该迁移的是学习路径分流：新手、原型构建者、全栈产品用户、AI-Native 进阶用户不应该读同一条路径。
但本仓不能直接复制站点结构，应该把它改良成 `getting-started` 的用户身份和产出导向路线。

## 本地证据

- 研究对象：`datawhalechina/easy-vibe`
- 当前研究角色：中文分阶段交互式课程
- 原始仓库：`raw/repository/`
- 原始来源清单：`raw/sources.yml`
- 事实摘要：`domain.yml`
- 深度证据：`deep-dive.md`

## 对标拆解

| 项 | 内容 |
|:---|:---|
| 参考对象 | `datawhalechina/easy-vibe` |
| 它解决的核心问题 | 让不同目标的中文用户知道从哪条路线开始学习 Vibe Coding |
| 核心机制 | `docs/` 课程内容、站点配置、脚本、`AGENTS.md`、`CLAUDE.md`、`llms.txt` |
| 真正带来结果的动作 | 用用户目标分流学习路径，而不是只按技术栈罗列知识 |
| 可迁移做法 | 新手 first win、idea to prototype、full-stack、AI-Native 进阶路径 |
| 不可迁移条件 | 不复制站点工程和大体量课程目录，本仓保持轻量文档知识库 |
| 下一步试用动作 | 重构 `docs/getting-started/learning-map.md` 的用户身份和阶段分流 |

## 改良迭代

| 改良目标 | 原模式 | 本仓版本 | 验证指标 |
|:---|:---|:---|:---|
| 用户分流 | 按学习目标给路线 | 零基础、开发者、创业者、维护者、高阶 Agent 用户 | 用户能在 30 秒内找到路线 |
| 产出导向 | 先给 first win | 每个阶段写清能做出什么 | 路线不再只列文档链接 |
| AI 可读入口 | `AGENTS.md`、`CLAUDE.md`、`llms.txt` | 本仓 `AGENTS.md`、`llms.txt`、`llms-full.txt` 协同 | AI 能按入口读取上下文 |

## 可迁移清单

- 让入门路径先回答“你会做出什么”，再讲概念。
- 按用户身份和目标组织学习地图。
- 在每个阶段写清前置条件、产出、验证方式和下一步。
- 保持 AI 可读入口和人类入口同步。

## 不可迁移清单

- 不把本仓变成大型课程站点。
- 不直接迁移其目录和站点构建方式。
- 不把课程包装等同于工程治理。

## 验证动作

| 动作 | 成功信号 | 失败信号 |
|:---|:---|:---|
| 抽样重写一个 getting-started 路线 | 用户能按身份选择路径 | 所有人仍读同一条线 |
| 给每阶段补产出和验证 | 每阶段有可见成果 | 仍只是资料链接 |
| 检查 AI 入口同步 | llms 和 README 指向一致 | AI 入口缺最新路径 |

## 沉淀判断

- 稳定结论进入 `docs/getting-started/` 和 `docs/README.md`。
- 本研究域保持 P2 教程产品化对标对象。
