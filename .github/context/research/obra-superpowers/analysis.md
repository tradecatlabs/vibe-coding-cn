# obra/superpowers 研究分析

## 本轮结论

obra/superpowers 把软件开发方法论封装成可触发技能，覆盖头脑风暴、工作树、计划、TDD、调试、代码审查和分支收尾，并通过多个 harness 的插件入口分发。它与本仓的 skills、workflow 和质量门禁高度相关，是研究“方法如何变成可加载能力”的高价值对象。

## 本地证据

- raw/github-readme.raw.md.txt：方法论、安装入口、基本工作流和技能目录。
- raw/repository/skills/：brainstorming、writing-plans、TDD、systematic-debugging、review 和 completion 等技能。
- raw/repository/.codex-plugin/plugin.json：Codex 插件 manifest、技能目录和能力描述。
- raw/repository/.claude-plugin/：Claude 插件和 marketplace 入口。
- raw/repository/tests/：Codex、插件同步、技能行为和 shell lint 测试。
- raw/repository/docs/：不同 harness 的适配说明。

## 对标拆解

| 项 | 内容 |
|:---|:---|
| 参考对象 | obra/superpowers |
| 核心问题 | 让 Agent 在开发前先澄清、计划、测试、审查和收尾，而不是直接写代码 |
| 核心机制 | composable skills、自动触发、插件 manifest、TDD、review 和分支收尾 |
| 真正带来结果的动作 | 每个阶段有一个明确技能和输出，完成前必须验证 |
| 可迁移做法 | 让本仓 skill 写清触发、输入、输出、失败和验证 |
| 不可迁移条件 | 不复制外部 subagent、worktree 和多平台安装实现作为默认路径 |

## 改良迭代

| 改良目标 | 本仓版本 | 验证指标 |
|:---|:---|:---|
| 技能触发 | 按任务类型加载最小 skill | 不需要预读整个 .github/skills/ |
| 开发闭环 | 计划、实现、测试、审查、收尾分层 | 结果不依赖 Agent 自报 |
| 质量方法 | TDD、系统调试、完成前验证转成本仓检查项 | 有对应失败样例 |
| 多工具适配 | 将通用方法和 harness 适配分开 | Codex/OpenCode 文档不互相污染 |

## 可迁移清单

- 将一次性经验沉淀为技能，而不是堆进系统提示词。
- 对高频流程提供短入口，对复杂细节放入 references。
- 在完成声明前强制消费测试、diff、链接或结构证据。
- 用插件 manifest 表达能力、版本、来源和安装边界。

## 不可迁移清单

- 本仓根规则已经禁止原生 subagent；不迁移其默认 subagent-driven 路径。
- 不把外部插件直接安装到用户环境。
- 不为了“技能数量”增加重复 owner skill。

## 验证动作

| 动作 | 成功信号 | 失败信号 |
|:---|:---|:---|
| 抽样一个本仓 skill | 有触发条件、输入、输出和验证 | 只是长提示词 |
| 执行一项文档任务 | 能按技能得到可审查产物 | 任务依赖未记录的上下文 |
| 检查外部插件说明 | 来源、权限、版本和回滚明确 | 安装命令默认高权限运行 |

## 沉淀判断

“Skill 是可加载的流程能力包，必须有触发和验证契约”适合下沉到 .github/skills/AGENTS.md；具体 Superpowers 组合保持研究参考。
