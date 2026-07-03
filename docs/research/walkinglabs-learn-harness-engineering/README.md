# walkinglabs/learn-harness-engineering 研究域

## 字多不看

- 本目录研究 `walkinglabs/learn-harness-engineering` 这个外部仓库。
- 当前优先级：P2；研究角色：Harness Engineering 课程、模板、Skill 与审计工具对标对象。
- GitHub 动态事实放在 `domain.yml`，观测日期为 2026-07-04。
- 它最值得迁移的不是站点形态，而是把 AI Agent 可靠性拆成指令、状态、验证、范围和生命周期。

## 快速导航

| 文档 | 定位 |
|:---|:---|
| [domain.yml](domain.yml) | 仓库事实快照、研究方向、优先级和来源证据。 |
| [analysis.md](analysis.md) | 本研究域的结构化研究结果、可迁移做法、风险和验证动作。 |
| [deep-dive.md](deep-dive.md) | L2 结构深度研究、关键机制和对本仓 Harness 体系的应用建议。 |
| [AGENTS.md](AGENTS.md) | 本研究域维护规则。 |

<details>
<summary><strong>完整细粒度目录（点击展开/收起）</strong></summary>

### 细粒度目录

- [domain.yml](domain.yml) - 仓库事实快照、研究方向、优先级和来源证据。
- [analysis.md](analysis.md) - 本研究域的结构化研究结果、可迁移做法、风险和验证动作。
- [deep-dive.md](deep-dive.md) - L2 结构深度研究、关键机制和对本仓 Harness 体系的应用建议。
- [AGENTS.md](AGENTS.md) - 本研究域维护规则。

</details>

## 使用方式

- 先读本 README 的判断，再读 `analysis.md` 和 `deep-dive.md` 的研究结论，最后读 `domain.yml`。
- 需要引用 stars、forks、release、归档状态、主页或主题标签时，先重新核验 GitHub。
- 需要更新原始事实时，运行 `python3 scripts/fetch-research-raw.py walkinglabs-learn-harness-engineering`。
- 如果形成稳定方法论，再下沉到 `docs/research/harness/`、`docs/workflow/` 或 `skills/`。

## 正文

### 研究定位

`walkinglabs/learn-harness-engineering` 的当前研究定位是：Harness Engineering
课程、模板、Skill 与审计工具对标对象。

### 当前判断

这是本仓 Harness 研究线的重要外部样本。它把 Harness Engineering 从概念解释推进到可操作系统：

- 用 12 讲解释 Agent 为什么会失败，以及 Harness 如何约束失败面。
- 用 6 个项目把同一个 Electron 知识库应用从 prompt-only 推进到完整 Harness。
- 用模板沉淀 `AGENTS.md`、`feature_list.json`、`init.sh`、进度文件、交接文件和评估表。
- 用 `skills/harness-creator` 与 `tools/audit-harness.sh` 把课程结论变成可运行工具。

对本仓最有价值的点是：把“AI 协作经验”升级成“仓库内可执行控制面”。经验如果只停留在提示词，
下一轮会丢失；经验如果写成状态机、验证命令、审计脚本和交接文件，就能被 Agent 反复执行。

### 观察字段

- GitHub URL：https://github.com/walkinglabs/learn-harness-engineering
- 当前研究方向：`harness-engineering`
- 当前优先级：P2
- 当前归档状态：`false`
- 主要语言：`TypeScript`

### 后续观察

- `skills/harness-creator` 是否继续演化出更强的自动创建、校验和 benchmark 能力。
- `tools/audit-harness.sh` 的五子系统审计是否能转成本仓 `make` 门禁或独立脚本。
- 课程项目中的 `feature_list.json`、`session-handoff.md`、`evaluator-rubric.md` 是否能改良成本仓任务治理模板。
- 它引用的 OpenAI、Anthropic、LangChain、Thoughtworks、Cursor 等 Harness 文章是否出现新版本或新范式。
