# mindfold-ai/Trellis 研究域

## 字多不看

- 本目录研究 `mindfold-ai/Trellis` 这个外部仓库。
- 当前优先级：P1；研究角色：跨平台 Agent Harness 框架、CLI 与任务/规格/记忆系统。
- GitHub 动态事实放在 `domain.yml`，观测日期为 2026-07-04。
- 它最值得迁移的不是 AGPL 代码，而是把任务、规格、记忆、验证和多平台适配沉淀为仓库控制面的机制。

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
- 需要更新原始事实时，运行 `python3 scripts/fetch-research-raw.py mindfold-ai-trellis`。
- 如果形成稳定方法论，再下沉到 `docs/research/harness/`、`docs/workflow/`、`scripts/` 或 `skills/`。

## 正文

### 研究定位

`mindfold-ai/Trellis` 的当前研究定位是：跨平台 Agent Harness 框架、CLI 与任务/规格/记忆系统。

### 当前判断

Trellis 是本仓 Harness 研究线的 P1 样本。它不是把 `AGENTS.md`、`CLAUDE.md` 或规则文件再包一层，
而是把 AI 编程过程做成仓库内可运行控制面：

- 用 `.trellis/spec/` 保存团队约束，让 Agent 通过任务上下文加载规则，而不是靠模型记忆。
- 用 `.trellis/tasks/` 保存 `prd.md`、`design.md`、`implement.md`、`implement.jsonl` 和 `check.jsonl`。
- 用 `.trellis/workflow.md` 保存状态机和每轮注入的 breadcrumb，约束从计划、执行到收尾的相位。
- 用 `.trellis/workspace/` 保存开发者会话记录，解决跨会话恢复和团队共享问题。
- 用 CLI 同时生成 Claude Code、Codex、Cursor、OpenCode、Gemini、Kiro、Qoder、Copilot 等平台适配层。
- 用 `channel`、`mem`、`task` 等核心原语把多 Agent 协作、会话检索和任务记录从文档推进到 runtime。

对本仓最有价值的点是：把“AI 协作经验”进一步升级为“可注入、可验证、可迁移、可升级的控制面”。
经验句子容易被遗忘；任务、规格、上下文清单、状态机和验证命令能被下一轮 Agent 继续执行。

### 观察字段

- GitHub URL：https://github.com/mindfold-ai/Trellis
- 当前研究方向：`agent-harness-framework`
- 当前优先级：P1
- 当前归档状态：`false`
- 主要语言：`TypeScript`

### 后续观察

- `channel` runtime 是否继续成熟为通用多 Agent 协作层。
- `mem` 是否从多平台会话检索扩展为更强的长期项目记忆。
- Codex、Copilot、Gemini 等 pull-based 平台的上下文注入方式是否继续收敛。
- `.trellis/spec/`、`.trellis/tasks/`、`.trellis/workflow.md` 的状态契约是否能稳定支撑团队协作。
- AGPL-3.0 许可证边界下，哪些机制可借鉴、哪些代码和模板不能直接搬入本仓。
