# earyantLe/vibe-coding-skill 研究分析

## 本轮结论

`earyantLe/vibe-coding-skill` 的价值在“小型方法论如何封装成 Skill”。它不是大型教程，也不是复杂应用，
但它有 `SKILL.md`、`references/`、发布说明和提交流程，适合研究最小可发布 Skill 的骨架。

本仓最应该迁移的是 Skill 产品化边界：一个 Skill 不能只是长提示词，必须有触发条件、输入输出、
引用资料、约束、验证和发布检查。

## 本地证据

- 研究对象：`earyantLe/vibe-coding-skill`
- 当前研究角色：Vibe Coding Skill / SOP 化
- 原始仓库：`raw/repository/`
- 原始来源清单：`raw/sources.yml`
- 事实摘要：`domain.yml`

## 对标拆解

| 项 | 内容 |
|:---|:---|
| 参考对象 | `earyantLe/vibe-coding-skill` |
| 它解决的核心问题 | 把 Vibe Coding 方法封装成可调用 Skill |
| 核心机制 | `SKILL.md`、`references/`、`PUBLISH.md`、`SUBMISSION.md` |
| 真正带来结果的动作 | 让方法论从文档变成有入口、有资料、有发布流程的能力单元 |
| 可迁移做法 | Skill 最小结构、发布检查、引用资料组织 |
| 不可迁移条件 | 不把小型 Skill 当成完整方法论体系 |
| 下一步试用动作 | 为本仓 skills 建最小发布检查清单 |

## 改良迭代

| 改良目标 | 原模式 | 本仓版本 | 验证指标 |
|:---|:---|:---|:---|
| Skill 入口 | 单个 `SKILL.md` | 每个 skill 明确触发、边界、输入输出 | Agent 能判断何时调用 |
| 引用资料 | `references/` 支撑正文 | 引用资料按任务路由读取 | 不一次性加载无关资料 |
| 发布检查 | PUBLISH / SUBMISSION | 本仓 skill 校验和归档规则 | skill 可验证、可维护 |

## 可迁移清单

- 为 Skill 补触发条件、输入输出、边界和验证命令。
- 把长方法论拆成 `SKILL.md` 和 `references/`。
- 为发布和提交增加检查清单。
- 将 SOP 化经验转入 skills，而不是留在零散文档。

## 不可迁移清单

- 不把每个经验都做成 Skill。
- 不用 Skill 包装还没验证的方法。
- 不因为目录完整就认为能力可用。

## 验证动作

| 动作 | 成功信号 | 失败信号 |
|:---|:---|:---|
| 抽样一个本仓 skill 做发布检查 | 触发、输入、输出、验证都明确 | 只有提示词正文 |
| 把一条 SOP 转成 skill 候选 | 能说明为什么需要 skill | 文档已经足够却新增复杂度 |
| 校验 references 读取边界 | 只读任务相关资料 | skill 一启动就加载全部资料 |

## 沉淀判断

- 稳定结论进入 `skills/AGENTS.md`、`skills/README.md` 或 skill 创建规范。
- 本研究域保持 P3 Skill 骨架观察对象。
