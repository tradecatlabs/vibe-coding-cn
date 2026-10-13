# addyosmani/agent-skills 研究分析

## 本轮结论

addyosmani/agent-skills 将工程生命周期压缩成 /spec、/plan、/build、/test、/constraints、/review、/code-simplify、/webperf 和 /ship 等入口，并以 24 个生命周期技能、references 和 evals 承载细节。它是研究“短命令如何映射到质量门禁”的强对标。

## 本地证据

- raw/github-readme.raw.md.txt：生命周期命令、安装方式、各 harness 适配和技能清单。
- raw/repository/skills/：context-engineering、spec-driven-development、planning、incremental implementation、testing、review、shipping 等技能。
- raw/repository/commands/、agents/：命令入口和 Agent 定义。
- raw/repository/references/：共享检查清单和工程规范。
- raw/repository/evals/：case、fixture 和技能评估资料。
- raw/repository/.codex-plugin/、.claude-plugin/、.opencode/：多工具分发适配。

## 对标拆解

| 项 | 内容 |
|:---|:---|
| 参考对象 | addyosmani/agent-skills |
| 核心问题 | 让工程最佳实践随任务阶段自动加载，并用质量门禁约束 Agent |
| 核心机制 | 生命周期命令、技能目录、共享 references、evals 和多 harness 适配 |
| 真正带来结果的动作 | 将定义、计划、实现、验证、审查和发布拆成可调用阶段 |
| 可迁移做法 | 以任务入口组织本仓已有能力，而不是让用户在 .github/skills/ 中盲搜 |
| 不可迁移条件 | 不复制其全部技能、命令和共享 references |

## 改良迭代

| 改良目标 | 本仓版本 | 验证指标 |
|:---|:---|:---|
| 入口发现 | 根 README 和 docs 入口按任务组织 | 用户能从目标找到一个入口 |
| 阶段质量 | 每个阶段绑定最小验证命令 | 不能跳过测试/审查而声明完成 |
| 上下文治理 | 常驻规则与按需技能分离 | 上下文体积和职责边界清晰 |
| 安装可移植性 | 记录单 skill 安装可能缺共享资料 | 安装后路径不静默失效 |

## 可迁移清单

- 用短命令或短标题表达阶段，用文档承载完整规则。
- 把 context engineering 作为独立关注点。
- 将代码简化、性能和安全作为可触发质量技能。
- 用 eval case 检查技能是否真的改变 Agent 行为。

## 不可迁移清单

- 不把 slash command 名称当作本仓必须采用的接口。
- 不在没有评估的情况下声称某 skill 提升质量。
- 不把第三方安装器或 marketplace 当作安全可信来源。

## 验证动作

| 动作 | 成功信号 | 失败信号 |
|:---|:---|:---|
| 从一个用户目标选择入口 | 只需一个明确导航跳转 | 需要读完 .github/skills/ 才能决定 |
| 抽样一个阶段技能 | 有输入、输出、门禁和反例 | 只有经验性建议 |
| 检查共享引用 | 单独安装不会产生静默缺资料 | references 路径失效却无提示 |

## 沉淀判断

“技能入口要短，质量规则要可验证，评估要独立于技能自述”适合下沉到 .github/skills/AGENTS.md 和 workflow 规则。
