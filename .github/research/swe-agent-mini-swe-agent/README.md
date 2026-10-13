# SWE-agent/mini-swe-agent 研究域

## 字多不看

- 本目录研究 SWE-agent 团队维护的 mini-SWE-agent。
- 当前优先级：P2；研究角色：GitHub issue 和命令行问题求解 Agent。
- 重点观察极简执行循环、配置边界、回归验证和基准评估如何互相约束。

## 快速导航

| 文档 | 定位 |
|:---|:---|
| [domain.yml](domain.yml) | 仓库事实快照、研究方向、优先级和来源证据。 |
| [analysis.md](analysis.md) | 极简软件工程 Agent 的结构化研究结论和迁移边界。 |
| [deep-dive.md](deep-dive.md) | Agent loop、配置、工具和基准验证的 L2 研究。 |
| [AGENTS.md](AGENTS.md) | 本研究域维护规则。 |

<details>
<summary><strong>完整细粒度目录（点击展开/收起）</strong></summary>

### 细粒度目录

- [domain.yml](domain.yml) - 仓库事实快照、研究方向、优先级和来源证据。
- [analysis.md](analysis.md) - 极简软件工程 Agent 的结构化研究结论和迁移边界。
- [deep-dive.md](deep-dive.md) - Agent loop、配置、工具和基准验证的 L2 研究。
- [AGENTS.md](AGENTS.md) - 本研究域维护规则。

</details>

## 使用方式

- 先读本 README 的判断，再读 analysis.md 和 deep-dive.md。
- 需要当前安装、参数或基准口径时，优先核验官方文档 https://mini-swe-agent.com/ 和 raw/ 快照。
- 研究其“最小闭环”而不是照搬其 benchmark 数字；所有真实执行必须有隔离、权限和回滚边界。

## 正文

### 研究定位

SWE-agent/mini-swe-agent 是一个极简软件工程 Agent，能够接收 GitHub issue 或命令行任务，并尝试使用工具完成修复或其他工程动作。

### 当前判断

它是“少量运行时 + 明确任务 + 可测量结果”的对标对象。对本仓最有价值的是用小而清晰的执行循环降低系统复杂度，同时把基准、测试和真实项目结果分开，不用宏大的 Agent 叙事替代证据。

### 观察字段

- GitHub URL：https://github.com/SWE-agent/mini-swe-agent
- 当前研究方向：issue-solving-agent
- 当前优先级：P2
- 当前归档状态：false
- 主要语言：Python
- 最新 release：v2.4.6
- 项目主页：https://mini-swe-agent.com

### 后续观察

- 100 行级别的最小 loop 如何处理工具失败、上下文和停止条件。
- 配置文件、命令行和评估脚本如何保证实验可复现。
- 哪些 issue -> patch -> test 的流程可以补充本仓 workflow 的回归闭环。
