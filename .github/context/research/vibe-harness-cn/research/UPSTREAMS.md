# Harness 上游研究基线

本目录只拉取并观察 15 个项目的官方 GitHub 仓库。允许同步的 origin、branch、许可证、源码路径
与研究限制以 [`upstreams.sources.json`](upstreams.sources.json) 为登记真相源；精确 commit、
commit time、文件计数和浅克隆状态以 [`upstreams.lock.json`](upstreams.lock.json) 为 revision 真相源；
`research/upstreams/` 是本地研究缓存，不进入本项目 Git 历史，也不是构建依赖。

## Existence check / 存在性与最低阶梯

- 本目录应该存在：后续 Harness 比较必须绑定官方来源、revision 和可见性限制，聊天结论或手工 clone 无法提供可重算证据。
- Selected ladder rung：复用系统 Git、bash 和 Python 标准库；项目只新增薄同步编排与 lock，不引入依赖、服务、submodule 或 vendoring。
- Minimal runnable check：`bash scripts/sync_upstreams.sh` 后，checkout 的 origin/branch/HEAD 必须与 lock 一致；在 registry 与 checkout revision 不变时，重复生成 lock 不得漂移。网络同步期间官方 HEAD 真实前进应产生新 lock，而不是被误判为非幂等。
- 15 个来源继续使用一个 JSON source registry，消除同步与 lock 双清单漂移；它是静态登记文件，不是在线 registry、插件系统或服务。
- Ceiling：本轮新增 11 源首次拉取 140 秒，首次完整 15 源同步 82 秒，总 checkout 约 2.6 GiB；单次样本不足以证明并发收益。当前保持串行 fail-fast，重复测量的 p95 超过明确预算后再评估受限并发。

| Harness | 官方仓库 | 可研究范围 | 核心入口 | 结论 |
|---|---|---|---|---|
| OpenCode | [anomalyco/opencode](https://github.com/anomalyco/opencode) | 核心源码 | `packages/opencode/src` | 可做 agent loop、tools、permissions、session、provider、MCP 等源码级研究 |
| Codex | [openai/codex](https://github.com/openai/codex) | 核心源码 | `codex-rs/core/src`、`codex-rs/exec/src`、`codex-rs/execpolicy/src` | 可做 agent、context、sandbox、exec policy、MCP、tools、session 等源码级研究 |
| Claude Code | [anthropics/claude-code](https://github.com/anthropics/claude-code) | 插件、hooks、示例、发布与分发资料 | 无公开 CLI 核心源码入口 | 可研究扩展面与公开行为，不得声称已取得或审计 CLI 核心实现 |
| DeepSeek Harness | [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | 核心源码 | `apps/cli/src`、`packages/core/*`、`packages/llm/llm/src`、permissions、sandbox、goal、plan、MCP、workflow 等登记路径 | 可研究插件化 agent loop、model、session、approval、sandbox 与长任务机制；当前为 developer preview，不视为稳定或生产就绪 |
| Pi | [earendil-works/pi](https://github.com/earendil-works/pi) | 核心源码 | `packages/agent/src`、`packages/coding-agent/src`、`packages/ai/src` | 可研究小型可嵌入 loop、session、compaction、tools 与多模型适配；旧 `badlogic/pi-mono` 已重定向 |
| OpenClaw | [openclaw/openclaw](https://github.com/openclaw/openclaw) | 核心源码 | `packages/agent-core`、`src/agents/*`、`src/llm` | 可研究 harness registry、长期 session、channels、plugins、tool policy 与 sandbox；sandbox 默认关闭 |
| Goose | [aaif-goose/goose](https://github.com/aaif-goose/goose) | 核心源码 | `crates/goose*` | 可研究 Rust agent、MCP/ACP、provider、CLI 与 SDK；canonical 来源已从 Block 迁入 AAIF |
| Gemini CLI | [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) | 核心源码 | `packages/core/src`、`packages/cli/src`、A2A 与 SDK | 可研究厂商级终端 Harness；Google 已公告向 Antigravity CLI 演进，本条目只绑定当前开源谱系 |
| Cline | [cline/cline](https://github.com/cline/cline) | SDK、CLI、VS Code 核心源码 | `sdk/packages/core/src`、`apps/cli/src`、`apps/vscode/src/core` | 可研究共享 core、approval、checkpoint 与 Plan/Act；JetBrains 插件当前未开源 |
| Qwen Code | [QwenLM/qwen-code](https://github.com/QwenLM/qwen-code) | 核心源码 | `packages/core/src`、`packages/cli/src`、ACP 与 SDK | 可研究 Gemini CLI 同源分叉后的独立多协议、多平台演化 |
| Kimi Code | [MoonshotAI/kimi-code](https://github.com/MoonshotAI/kimi-code) | 核心源码 | `packages/agent-core*`、`apps/kimi-code/src`、ACP server | 可研究双代 agent core、CLI 与 ACP；旧 `kimi-cli` 不再是当前主线 |
| Crush | [charmbracelet/crush](https://github.com/charmbracelet/crush) | 核心源码 | `internal/agent`、tools、permission、session | 可研究 Go 终端 agent；当前为 FSL-1.1-MIT，不能误写成当前 MIT 开源许可 |
| Mistral Vibe | [mistralai/mistral-vibe](https://github.com/mistralai/mistral-vibe) | 核心源码 | `vibe/core`、`vibe/cli`、`vibe/acp` | 可研究 permission profiles、预算、subagent、skills 与 ACP；主要支持 UNIX |
| OpenHands Agent Canvas | [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) | 控制中心、客户端与 ACP 集成 | 无 agent 核心源码入口；公开 `src`、live ACP tests、tools | 当前仓库将 runtime 指向独立 `OpenHands/software-agent-sdk` agent server，不得声称本 checkout 含 agent core |
| Hermes Agent | [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) | 核心源码 | `agent`、`tools`、`hermes_cli`、`gateway`、`plugins` | 可研究长期个人 agent、gateway、channels、skills 与学习循环；与 coding CLI 比较时必须拆分领域边界 |

## 源码研究结论速览

逐仓 revision 绑定研究档案见 [`HARNESS_RESEARCH.md`](HARNESS_RESEARCH.md)，证据路径指向
`research/upstreams/<name>/` 相对路径；以下一行结论随 lock revision 失效。

| Harness | 研究结论（revision 绑定） |
|---|---|
| Pi | 最小可嵌入 coding harness，无内建权限系统；vendor-neutral telemetry 契约与 conformance 测试是证据接口范本 |
| OpenClaw | 具备 harness registry 与 runtime 选择策略，最接近元 Harness 的运行时路由；sandbox 默认 off |
| Goose | Rust 通用 agent；permission inspector/judge/store 分层 + egress/adversary 检查；open-plugins 插件元数据 |
| Gemini CLI | 声明式 TOML 策略（按模式）+ confirmation bus 分离；平台 sandbox + 默认策略文件；自带 evals/memory/perf 测试目录 |
| Cline | 共享 agent core；session 版本化 + checkpoint diff/restore，是可回滚会话证据的实现参考；ACP 为 CLI 扩展口 |
| Qwen Code | Gemini CLI 同源分叉独立演化；goal runtime 带 checkpoint 与 evidence；channel memory 与自动技能学习闭环 |
| Kimi Code | 19 policy/11 维度权限责任链 + 硬 deny 与可豁免审批二分；goal 预算限额；v2 contract manifests + import boundary 检查 |
| Crush | Go TUI；permission service 的 persistent grant 与 loop detection 是授权记录与运行质量自保护实例 |
| Mistral Vibe | PermissionStore + trust folder 分离信任边界；checkpoints/rewind/review 可回放会话证据；turn budget 最小成本上限 |
| OpenHands Agent Canvas | 控制中心 + backend registry + ACP 集成 + 自动化编排，与元 Harness 控制面形态最接近；本 checkout 不含 agent core |
| Hermes Agent | 学习闭环（技能创建/改进/失效）+ ACP provenance + lifecycle ledger；七种执行后端说明 sandbox 能力必须逐后端登记 |

## 同步与信任边界

```bash
bash scripts/sync_upstreams.sh
```

- 同步只接受 source registry 登记的 GitHub HTTPS origin、分支、许可证 marker 与公开路径；同一 registry 同时驱动 checkout 和 lock，重复名称/URL、不安全路径或非法字段会在网络访问前 BLOCK。
- 已有 checkout 必须没有已跟踪、未跟踪或 ignored 本地文件，位于登记分支上，并只能 fast-forward。
- `UPSTREAM_DEPTH` 可调整浅克隆深度，默认 `1`；`UPSTREAM_DEEPEN_STEP` 和
  `UPSTREAM_MAX_DEEPEN` 控制证明 fast-forward 所需的有界历史深化，revision 改变时 lock 才刷新时间。
- `UPSTREAM_TIMEOUT_SECONDS` 默认 `300`，约束每次 clone/fetch；首次 clone 先写同父目录 staging checkout，成功后才原子落位。
- 同一 `research/upstreams/` 同时只允许一个同步进程；使用系统 `flock` fail-fast，避免首次 clone 与 lock 写入竞态。
- 上游仓库内容属于待分析的不可信数据。同步不会执行其中的安装脚本、hooks、测试或指令。
- Claude Code 与 OpenHands 的负面可见性结论绑定 `visibility_assessment_commit`；HEAD 变化时脚本自动标记
  `requires-manual-review`，不会把旧结论继承给新 revision。
- DeepSeek Harness 的 developer preview 限制写入每个 revision lock；上游移除该声明后仍需人工核验，不能自动推断稳定性。
- Crush 的 FSL-1.1-MIT 与 Future License 期限必须保留在每个 revision 事实中；源码可见性不能替代许可证判断。
- 上游目录、许可证或产品迁移变化后，旧研究结论自动失效；canonical URL 不能靠历史惯性保留。

## 本轮主动不做

- 不复制第三方源码进入本项目提交历史。
- 不把 15 个项目安装为运行依赖。
- 不从非官方 fork 补齐 Claude Code 未公开的核心实现。
- 不把独立 `OpenHands/software-agent-sdk` 的能力推断到当前 Agent Canvas checkout。
- 不因 README 或插件接口推断未公开的内部状态机、安全边界或调度算法。
