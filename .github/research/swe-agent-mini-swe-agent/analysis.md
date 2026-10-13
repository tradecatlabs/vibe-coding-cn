# SWE-agent/mini-SWE-agent 研究分析

## 本轮结论

mini-SWE-agent 用极少运行时结构完成 GitHub issue 和命令行任务求解，把模型、环境、Agent loop 和 trajectory 分开，并提供 step、cost、wall-time、格式错误和交互确认限制。它是“最小可验证 Agent”对标，而不是本仓默认工具。

## 本地证据

- raw/github-readme.raw.md.txt：极简定位、bash-only、线性历史、环境选项和 SWE-bench 说明。
- raw/repository/src/minisweagent/agents/default.py：AgentConfig、运行循环、限制、执行动作和 trajectory 序列化。
- raw/repository/src/minisweagent/agents/interactive.py：human、confirm、yolo 三种执行模式。
- raw/repository/src/minisweagent/environments/：local、docker、singularity、bubblewrap 等环境适配。
- raw/repository/docs/advanced/ 和 reference/：控制流、配置、环境、模型和运行命令文档。
- raw/repository/tests/：Agent、环境、模型、运行和序列化测试。

## 对标拆解

| 项 | 内容 |
|:---|:---|
| 参考对象 | SWE-agent/mini-swe-agent |
| 核心问题 | 用小而透明的 Agent loop 执行软件工程任务并保存结果 |
| 核心机制 | bash action、线性消息、独立 subprocess、环境适配、限制和 trajectory |
| 真正带来结果的动作 | 每一步都将模型输出转成动作，执行后追加观察并可保存 |
| 可迁移做法 | 为自动化任务设置步数、费用、时间、格式错误和结果保存边界 |
| 不可迁移条件 | 不把 SWE-bench 分数当作本仓教程质量证明 |

## 改良迭代

| 改良目标 | 本仓版本 | 验证指标 |
|:---|:---|:---|
| 运行限制 | 研究脚本有超时、重试和输出边界 | 失控任务能停止 |
| 交互边界 | 自动执行与人工确认明确区分 | 高风险动作不会静默执行 |
| 轨迹证据 | 保存命令、退出码、产物和当前 HEAD | 结果可复盘和回滚 |
| 最小实现 | 优先使用现有 shell/Python 工具 | 不因引入 Agent runtime 增加复杂度 |

## 可迁移清单

- 将任务循环拆成 query、action、observation、stop。
- 对长循环设置时间、次数、成本和格式错误上限。
- 为自动化输出保存可审查的 trajectory 或等价证据。
- 把本地环境和容器环境作为不同风险边界。

## 不可迁移清单

- 不在本仓自动运行外部仓库修复任务。
- 不将 yolo 模式作为默认安全路径。
- 不依据单个 benchmark 结果推导普遍生产能力。

## 验证动作

| 动作 | 成功信号 | 失败信号 |
|:---|:---|:---|
| 运行一个研究拉取循环 | 有明确超时、重试和停止条件 | 请求可以无限等待 |
| 审查自动命令 | confirm/权限/作用域明确 | 只因为模型生成就直接运行 |
| 检查结果文件 | 包含当前版本、输出和失败状态 | 只有“完成”字符串 |

## 沉淀判断

“自动执行必须有有界循环和可保存轨迹”适合下沉到 .github/scripts/AGENTS.md 与 workflow 研究规则。
