# github/spec-kit 研究域

## 字多不看

- 本目录研究 GitHub 官方 Spec Kit。
- 当前优先级：P1；研究角色：面向 AI coding agent 的规格驱动开发工具包。
- 重点观察原则、规格、计划、任务、实现和收敛如何组成可重复开发闭环。

## 快速导航

| 文档 | 定位 |
|:---|:---|
| [domain.yml](domain.yml) | 仓库事实快照、研究方向、优先级和来源证据。 |
| [analysis.md](analysis.md) | Spec-Driven Development 流程的结构化研究结论和迁移边界。 |
| [deep-dive.md](deep-dive.md) | CLI、模板、扩展和集成的 L2 研究。 |
| [AGENTS.md](AGENTS.md) | 本研究域维护规则。 |

<details>
<summary><strong>完整细粒度目录（点击展开/收起）</strong></summary>

### 细粒度目录

- [domain.yml](domain.yml) - 仓库事实快照、研究方向、优先级和来源证据。
- [analysis.md](analysis.md) - Spec-Driven Development 流程的结构化研究结论和迁移边界。
- [deep-dive.md](deep-dive.md) - CLI、模板、扩展和集成的 L2 研究。
- [AGENTS.md](AGENTS.md) - 本研究域维护规则。

</details>

## 使用方式

- 先读本 README 的判断，再读 analysis.md 和 deep-dive.md。
- 需要当前命令和模板时，优先核验 Spec Kit 官方文档 https://github.github.com/spec-kit/ 与 raw/ 快照。
- 只迁移“先规格、再计划、再任务、再实现、再收敛”的可验证结构，不把具体 CLI 或集成当成本仓强依赖。

## 正文

### 研究定位

github/spec-kit 是 GitHub 官方的 Spec-Driven Development 工具包，为 AI coding agent 提供从项目原则到规格、计划、任务、实现和收敛的流程资产。

### 当前判断

它直接补足本仓“从想法到可交付产物”的前置规格层。最有价值的不是某个 slash command，而是把需求表达、技术方案、任务拆解和实现验证固定为中间产物，减少 Agent 从模糊请求直接跳到代码的风险。

### 观察字段

- GitHub URL：https://github.com/github/spec-kit
- 当前研究方向：spec-driven-development
- 当前优先级：P1
- 当前归档状态：false
- 主要语言：Python
- 最新 release：v1.0.4
- 项目主页：https://github.github.com/spec-kit/

### 后续观察

- constitution、specify、plan、tasks、implement 和 converge 的产物边界是否稳定。
- extensions、presets、bundles 和多 Agent 集成如何控制扩展复杂度。
- 哪些规格产物适合下沉到本仓 docs/gongfa 的规格与流程文集。
