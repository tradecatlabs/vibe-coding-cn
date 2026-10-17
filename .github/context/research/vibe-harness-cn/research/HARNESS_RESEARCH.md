# Harness 源码级研究档案

> 本文件是 11 个新增官方 Harness 的 revision 绑定研究档案。所有结论以
> `research/upstreams/<name>/` 下实际源码或 lock 绑定事实为准；README 宣传与源码
> 不一致处显式标注。研究只读 checkout，不执行上游代码。

## 0. 方法与证据契约

- Revision：每个 Harness 的 commit 取自 `research/upstreams.lock.json`；结论随 revision 失效。
- 证据分级：`[源码]` 指向 `research/upstreams/<name>/` 内相对路径；`[文档]` 指向官方 README/文档；两者都不是运行验证。
- 研究维度：agent loop、工具/MCP/ACP、session/memory、权限审批、sandbox、provider、扩展机制、元 Harness 借鉴。
- 边界：不把相邻仓库（OpenHands/software-agent-sdk、Claude Code 闭源 CLI 等）的能力算进当前 checkout。

## 1. 总览对比

| Harness | 语言/形态 | Agent loop | 工具协议 | Session/Memory | 权限模型 | Sandbox | 对元 Harness 最有价值点 |
|---|---|---|---|---|---|---|---|
| Pi | TS/Bun 库+CLI | `packages/agent/src/agent-loop.ts` | 内建工具+扩展；无 MCP 包 | SQLite 后端、分支、compaction | 无内建权限 | 无，文档给容器化模式 | vendor-neutral telemetry 契约与 conformance 测试 |
| OpenClaw | Node/TS 网关 | `packages/agent-core/src/agent-loop.ts` | MCP、skills、plugins、工具策略 | 长期 session、树、compaction | tool policy + 审批绑定 | 可选 sandbox backend，默认 off | harness registry 与 runtime 选择策略 |
| Goose | Rust crate | `crates/goose/src/agents/agent.rs` | MCP、ACP server、open-plugins | session manager、chat history search | permission.yaml 三级 | security inspector（无沙箱本体） | permission inspector/judge/store 分层与 egress 检查 |
| Gemini CLI | TS CLI | `packages/core/src/agent/agent-session.ts` | MCP、浏览器、代码助手、A2A | session；memory-tests | TOML policy + confirmation-bus | sandbox/linux|macos|windows | 声明式策略文件与子代理协议 |
| Cline | TS SDK+CLI+IDE | `sdk/packages/core/src/ClineCore.ts` | MCP、ACP agent | session 版本化、checkpoint、compaction | 审批+auto-approve | 未验证 | checkpoint diff/restore 与 session manifest |
| Qwen Code | TS CLI | `packages/core/src/agents/` | MCP、LSP、ACP bridge | channel memory、索引 | autoMode 分类器+危险规则 | 未验证 | goal 运行时带 checkpoint 与 evidence |
| Kimi Code | TS CLI+ACP | `packages/agent-core/src/loop/` | MCP、skills、plugins、ACP server | session、minidb | 19 policy/11 维度责任链 | 未验证 | 权限链与硬 deny 分离；v2 契约 manifests |
| Crush | Go TUI | `internal/agent/coordinator.go` | LSP、MCP、内建 shell/edit/grep | session、SQLite | permission service + persistent grant | 未验证 | 权限服务与 loop detection |
| Mistral Vibe | Python CLI | `vibe/core/agent_loop/_loop.py` | ACP、app server、skills | session、compaction、checkpoints | PermissionStore + trust folders | 未验证 | trust folder 与 turn budget |
| OpenHands Agent Canvas | TS/React 控制中心 | 不在此仓库 | ACP 后端、MCP 服务 | conversation/workspaces | 未验证 | Docker/VM/cloud 后端 | 多 agent backend registry 与自动化编排 |
| Hermes Agent | Python 网关 | `agent/conversation_loop.py` | MCP、ACP adapter、delegation | FTS5 会话检索、learning graph | approval modes | 7 种执行后端 | 学习闭环、provenance、lifecycle ledger |

## 2. Pi（earendil-works/pi）

- Revision：`e429d90b800f9a37c8a5812f4c9c10a8cdcc85a7`；MIT；TypeScript/Bun monorepo。
- 定位：最小可嵌入 coding harness；官方明确跳过 subagents 与 plan mode，用扩展与 Pi Packages 替代。
- Agent loop：`[源码] packages/agent/src/agent-loop.ts`、`agent.ts`；`harness/agent-harness.ts`、`reducer.ts`、`events.ts` 提供状态化 agent、工具执行与事件流。
- Session/Memory：`[源码] packages/agent` 会话抽象；SQLite 后端独立成包（`@earendil-works/pi-session-backend-sqlite-node`，README 说明避免核心包引入原生依赖）；coding-agent 有 compaction 与 branch summarization（`core/compaction/compaction.ts`、`branch-summarization.ts`）、session tree。
- 工具：`[源码] packages/ai` 定义工具与参数校验、流式工具调用；coding-agent `core/bash-executor.ts`、`exec.ts`、`output-guard.ts`。
- 权限：`[文档] README 明确无内建权限系统，默认以启动用户权限运行；隔离靠容器化`；`[源码] core/restore-sandbox-env.ts` 配合外部沙箱。
- Provider：`[源码] packages/ai` 统一多 provider API，自动 auth 解析、token/cost 跟踪、跨 provider 上下文交接；providers 目录含 OpenAI/Anthropic/Google/Vertex 等。
- 扩展：`[源码] core/extensions/loader.ts|runner.ts|wrapper.ts`、`harness/skills.ts`、prompt templates、themes；CLI 四模式（interactive/print-JSON/RPC/SDK）。
- 元 Harness 借鉴：`[源码] packages/telemetry` 是供应商中立 telemetry 契约（span/attribute/event/status、显式 context、NOOP + in-memory 参考实现、adapter conformance 测试）。这是“证据接口 + 一致性测试”的成熟范本，可直接映射到元 Harness 的 evidence 适配器契约。

## 3. OpenClaw（openclaw/openclaw）

- Revision：`38379a9a2ee1f274a992482f9f3028ec8dfe6226`；MIT；Node/TypeScript 网关。
- 定位：单操作者长期运行的个人助理平台：Gateway（会话/工具/事件/渠道控制面）+ 渠道（WhatsApp/Telegram/Slack/Discord 等）+ 可选节点。
- Agent loop：`[源码] packages/agent-core/src/agent-loop.ts`、`agent.ts`；`src/agents/embedded-agent-runner/` 是内建 attempt loop、模型选择、compaction、transcript。
- Harness registry（关键）：`[源码] src/agents/harness/registry.ts`、`selection.ts`、`policy.ts`、`auto-selection.ts`、`builtin-openclaw.ts`、`codex-app-server-extensions.ts`——插件可注册额外 runtime id（如 `codex`），`agentRuntime.id` 按 model/provider 作用域选择，`auto` 按 provider 路由选插件 harness 否则回退内建。这是与“元 Harness”最接近的运行时路由实现。
- Session：`[源码] src/agents/sessions/`：session-manager、session tree、compaction、extensions 加载、prompt templates/skills/themes；`agent-hooks/` 含 compaction safeguard 与 context pruning。
- 工具与策略：`[源码] src/agents/agent-tools*.ts`：工具定义、参数 schema、tool policy、before/after 适配器；`sandbox/tool-policy.ts`、`sandbox-tool-policy.ts`、`tool-policy-audit.ts`；MCP 经 `agent-bundle-mcp-harness.ts`。
- 权限：`[源码]` gateway-question、native-hook-relay（approval binding/approval-wait）、lifecycle hooks。
- Sandbox：`[文档] docs/gateway/sandboxing.md`——默认 `off`，由 `agents.defaults.sandbox` 控制；mode `off|non-main|all`、scope `agent|session|shared`；`tools.elevated` 逃逸；Gateway 进程始终在 host。
- Provider：`[源码] src/llm/` model/provider registry 与 provider stream；model runtime generation 是“auth template + model registry + projected catalog”的原子快照，agent run 从快照 fork 可变 store。
- Manifest：`[文档] docs/agent-runtime-architecture.md`——资源包在 package.json `openclaw` 字段声明 extensions/skills/prompts/themes，缺省回退约定目录。
- 元 Harness 借鉴：harness registry + 选择策略 + 资源 manifest + 原子 runtime generation。治理控制面可以照此把“哪些 harness 可被哪个 provider/model 选择”建模为策略事实，但 OpenClaw 自己拥有运行态，元 Harness 只应持有治理事实。

## 4. Goose（aaif-goose/goose）

- Revision：`433d1b3c8fde932a6d1a94fa36c9daa696ce0a67`；Apache-2.0；Rust；已入 Linux Foundation AAIF。
- 定位：通用 agent（桌面/CLI/API），15+ provider、70+ MCP extensions。
- Agent loop：`[源码] crates/goose/src/agents/agent.rs`（Agent/AgentConfig，reply loop、retry、final output tool、stop-hook 死循环保护）；`state_machine.rs`、`tool_execution.rs`、`tool_confirmation_router.rs`。
- 扩展：`[源码] agents/extension_manager.rs`、`mcp_client.rs`、`extension_malware_check.rs`、`validate_extensions.rs`；`plugins/mod.rs` 支持 open-plugins 格式、自动更新、`.goose-plugin-install.json` 安装元数据；`skills/`。
- 权限：`[源码] config/permission.rs` 定义 `PermissionLevel {AlwaysAllow, AskBefore, NeverAllow}` 与 permission.yaml；`permission/permission_inspector.rs|judge.rs|store.rs` 分层：检查器 → 判定 → 存储。
- Session/Memory：`[源码] session/session_manager.rs`、`chat_history_search.rs`、session 命名；compaction triggers 在 `execute_commands.rs`；`context_mgmt/` 管理上下文。
- 安全：`[源码] security/`：adversary_inspector、egress_inspector、scanner、patterns（prompt injection 与出口流量检查）。
- 协议：`[源码] acp/server.rs|provider.rs|tools.rs|mcp_app_proxy.rs`；`gateway/`（handler、pairing、telegram）；MCP client。
- 执行：`[源码] execution/manager.rs` 并行执行；subagent handler；`schedule_tool.rs`。
- 遥测：`[源码] otel`、`agents/gen_ai_telemetry.rs`、`posthog.rs`（feature）。
- 元 Harness 借鉴：permission 检查/判定/存储分层、extension 恶意性检查、egress/adversary inspector 可作为“权限与安全边界审计”参考；open-plugins 插件元数据与自动更新是技能/插件治理的实例。

## 5. Gemini CLI（google-gemini/gemini-cli）

- Revision：`c0d192452b4e2df7efb6d62a60385f475bfd6779`；Apache-2.0；TypeScript。
- 定位：厂商终端 agent；官方公告终端产品向 Antigravity CLI 演进，本档案只绑定当前开源谱系。
- Agent loop：`[源码] packages/core/src/agent/agent-session.ts`（AgentSession implements AgentProtocol）；`agents/` 有 generalist-agent、local/remote subagent protocol、agent-scheduler、a2a-client-manager、local-executor、registry。
- 权限：`[源码] policy/policy-engine.ts` + `policy/policies/*.toml`（agents、non-interactive、plan、read-only、sandbox-default、write、yolo）；`confirmation-bus/`；`safety/`（conseca）、shell-safety。
- Sandbox：`[源码] sandbox/linux|macos|windows` + `sandboxPolicyManager.ts`；sandbox-default.toml 定义默认策略。
- Context：`[源码] context/` pipeline、processors、graph、config。
- 工具：`[源码] core/`、`mcp/`、`browser/`、`code_assist/`；A2A 在 `agents/a2aUtils.ts`、`a2a-client-manager.ts`。
- 评估资产：`[目录] evals/、memory-tests/、perf-tests/`——官方自带 memory/性能测试目录，是“harness 自带评估套件”实例。
- 元 Harness 借鉴：声明式 TOML 策略文件（按模式选策略）与 confirmation bus 分离；sandbox 策略可插拔；子代理协议分 local/remote 并有 acknowledgement registry；评估目录结构值得纳入 conformance 调研。

## 6. Cline（cline/cline）

- Revision：`3e0aac53a2f5f408a89a957d75430f6ec4084497`；Apache-2.0；TypeScript；README 明确 JetBrains 插件未开源。
- 定位：IDE 与终端共享 agent core；CLI 支持交互与 headless（CI/CD）。
- Agent loop：`[源码] sdk/packages/core/src/ClineCore.ts`；`cline-core/` 含 automation runtime（CronService）、start-input、telemetry、runtime-services。
- Session：`[源码] sdk/packages/core/src/session/`：checkpoint-diff、checkpoint-restore、session-graph、session-manifest、session-versioning-service、compaction、persistence-service、team-persistence-store、atomic-file stores。
- 权限/模式：`[源码] apps/cli/src/acp/permissions.ts`、`auto-approve.ts`、`session-load.ts`；plan mode 相关在 CLI mode tests/palette；checkpoint 覆盖 plan/act 流程。
- 并行：`[文档] README`——Kanban 独立仓库用 worktree + auto-commit + dependency chains 并行多 agent。
- 协议：`[源码] apps/cli/src/acp/acpAgent.ts`（ACP agent 接入）。
- 元 Harness 借鉴：session 版本化 + checkpoint diff/restore 是“可回滚会话证据”的实现参考；team persistence 与 automation runtime 说明多会话治理需要明确归属；ACP 是其 CLI 扩展口。

## 7. Qwen Code（QwenLM/qwen-code）

- Revision：`a669957f3d45557900a8255283ad0a2a3f7a14e6`；Apache-2.0；TypeScript。
- 定位：终端 coding agent；`[文档] README` 自述原基于 Gemini CLI v0.8.2，v0.1 起停止上游同步独立演化，支持 OpenAI/Anthropic/Gemini/Qwen 多协议。
- Agent loop：`[源码] packages/core/src/agents/`：agent-transcript、workflow-run-registry、background-tasks、background-agent-resume、subagent-result。
- Memory：`[源码] packages/core/src/memory/`：channel-memory、indexer、lifecycle、memory-scoped agent config、dreamAgentPlanner（规划式记忆整理）。
- Skills：`[源码] packages/core/src/skills/`：learn-skill-agent、extraction、pending-skills、manager——自动学习技能闭环。
- Goals：`[源码] packages/core/src/goals/`：goal-runtime、goal-reducer、goal-persistence、goal-checkpoint、goal-evidence、goal-tools、activeGoalStore——结构化目标带 checkpoint 与 evidence。
- 权限：`[源码] packages/core/src/permissions/`：autoMode、classifier、dangerous-rules、denial-tracking、destructive-commands、shell-semantics；confirmation-bus。
- 协议：`[源码] packages/acp-bridge`；tools/、mcp/、lsp/、extension/、hooks/、followup/、telemetry/。
- 元 Harness 借鉴：goal 运行时的 checkpoint 与 evidence 是“目标级治理证据”的直接实例；channel memory 与 skill 学习说明记忆/技能生命周期需要治理；denial tracking 是权限行为的可审计记录。

## 8. Kimi Code（MoonshotAI/kimi-code）

- Revision：`7475c2e2e3dd86ac0b8a8d51d4f1d233ed7df797`；MIT；TypeScript；当前产品主线（旧 kimi-cli 退役）。
- 定位：单二进制终端 agent + ACP；视频输入、AI-native MCP 配置、子代理、lifecycle hooks、plugin marketplace。
- Agent loop：`[源码] packages/agent-core/src/loop/`、`agent/`；agent-core-v2（`packages/agent-core-v2/src/`）重排为 features/kosong/wire/os/persistence/workspace/agent/tool/session。
- 权限（最有价值）：`[文档] packages/agent-core-v2/docs/Permission.md` 与 `[源码] packages/agent-core/src/agent/permission/`——有序责任链 + 首个命中赢，19 个 policy 归并为 11 个权限维度；`PermissionPolicyResult` 是携带续体/副作用的 approve/deny/ask 行为包；plan mode、AgentSwarm、goal 预算等是“无 ask 通道的硬 deny”（veto 监听器），与可豁免权限分离；产物审批（plan review/goal-start review）经 `IAgentToolApprovalService` 往返。
- Goals：`[文档] GOAL.md`——goal 是 runtime 结构化状态机（active/paused/blocked/complete），带完成标准、停止原因、token/统计限额、持久记录。
- 工具/扩展：`[源码] packages/agent-core/src/tools/`、`mcp/`、`skill/`、`plugin.ts`、`packages/plugins`；v2 `mcpCore/`。
- 契约 manifests：`[源码] packages/agent-core-v2/docs/config-manifest.toml|state-manifest.d.ts|wire-manifest.d.ts` 与 `scripts/check-import-boundaries.mjs`——配置/状态/消息契约由 manifest 生成并做边界检查。
- ACP：`[源码] packages/acp-server/`（server、session、approval、modes、model-catalog、interaction-bridge）。
- 元 Harness 借鉴：权限“硬约束 vs 可豁免审批”二分是治理模型的关键概念；goal 预算/统计限额是成本治理实例；生成式契约 manifest + import boundary 检查是“机器可读契约治理”的实现范本。

## 9. Crush（charmbracelet/crush）

- Revision：`051955a84c14550254d7929b4f27d01b84b4fdde`；FSL-1.1-MIT；Go。
- 定位：终端 coding agent；会话制、LSP 增强、MCP 可扩展；Charm 生态。
- Agent loop：`[源码] internal/agent/agent.go`、`coordinator.go`（含 coordinator MCP gate）、`dispatch`、`runid`/run marker、`loop_detection.go`（循环检测）。
- 工具：`[源码] internal/agent/tools/`：bash、edit、glob、grep、ls、fetch、download、job kill/output、diagnostics；LSP 工具（call hierarchy、definition、rename、references 等）；MCP（list_mcp_resources、coordinator MCP gate）。
- Session：`[源码] internal/session/session.go`；DB：`internal/db`（SQLite，含 migrations/sql）。
- 权限：`[源码] internal/permission/permission.go`：permission service、persistent grants、skip mode、grant 订阅通知（测试覆盖顺序 grant 与持久 grant）。
- Hooks：`[源码] internal/hooks/`（hooks、runner、input）。
- 并行：`[源码] internal/herdr/`（client/runner）与 csync。
- 元 Harness 借鉴：permission service 的 persistent grant 语义（同一请求自动放行）是可审计授权记录边界；loop detection 是 harness 运行质量的自保护机制；LSP 作为上下文来源与 MCP 并存的工具面值得纳入工具分类。

## 10. Mistral Vibe（mistralai/mistral-vibe）

- Revision：`4530b9ce6f74046afbeadf63a2c89be9e35ee2bb`；Apache-2.0；Python 3.12+；官方主要支持 UNIX。
- 定位：Mistral 模型驱动的 CLI coding assistant；支持子代理、交互式提问、voice、programmatic 模式。
- Agent loop：`[源码] vibe/core/agent_loop/_loop.py`、`_request_broker.py`、`manager.py`；`plan_session.py`；`agents/`。
- Session/Memory：`[源码] vibe/core/session/`（file_store、fs、history）、`compaction/`（context、checkpointer、recorder）、`checkpoints/`、`rewind/`、`review/`。
- 权限：`[源码] vibe/core/tools/permissions.py`（PermissionStore）、`tools/models.py`（ToolPermission/ PermissionContext）、`trusted_folders.py`（trust folder 系统）。
- 预算：`[源码] vibe/core/agent_loop/_loop.py` turn budget 计数。
- 工具/子代理：`[源码] vibe/core/tools/`、`subagents.py`、`worktree.py`（worktree 隔离）、`skills/`、`hooks/agent_loop_hooks.py`。
- 协议：`[源码] vibe/acp/`（agent、commands、tools、controller）、`vibe/app_server/`（runtime、turns）。
- 元 Harness 借鉴：trust folder 与 PermissionStore 分离是“信任边界 + 权限状态”实例；checkpoints/rewind/review 提供可回放会话证据；turn budget 是运行成本上限的最小实现。

## 11. OpenHands Agent Canvas（OpenHands/OpenHands）

- Revision：`e6c90d65383f6f5108ceede35f5e289a6562a7b1`；MIT；TypeScript/React。
- 定位：自托管开发控制中心，运行 OpenHands/Claude Code/Codex/Gemini 或任何 ACP agent 于 local/Docker/VM/cloud 后端。`[文档] README` 明确 agent runtime 指向独立 `OpenHands/software-agent-sdk`，本 checkout 不含 agent core。
- 控制面（关键）：`[源码] src/api/`：acp-service、backend-registry、automation-service、bash-service、conversation-service、event-service、git-service、mcp-health、mcp-service、runtime-service、settings-service、workspaces-service；`manifests/`。
- 自动化：`[源码] src/api/automation-service/`；README 描述 schedule/webhook 触发与 Slack/GitHub/Linear/Notion 集成。
- 前端：`[源码] src/components|hooks|routes`：会话 UI、浏览器、终端、文件、设置。
- 元 Harness 借鉴：这是“控制中心 + 多 agent 后端注册 + ACP 协议 + 自动化编排”的完整参考形态，与本项目元 Harness 的控制面意图最接近；但它拥有运行态与 UI，元 Harness 只应借鉴其 backend registry 与 ACP 集成边界，不复制其运行态所有权。

## 12. Hermes Agent（NousResearch/hermes-agent）

- Revision：`1f8fdc7bd824c8d07e3cefe109bd96425ec3171f`；MIT；Python。
- 定位：自改进个人 agent；内置学习闭环（技能创建/改进、知识持久化、跨会话检索、用户建模）。
- Agent loop：`[源码] agent/conversation_loop.py`、`context_engine.py`、`context_compressor.py`、`conversation_compression.py`、`bounded_response.py`、`iteration_budget.py`。
- 学习/记忆：`[源码] agent/learning_graph.py`、`learn_prompt.py`、`curator.py`、`insights.py`；`hermes_state_search.py`（FTS5 会话检索）、`tools/session_search_tool.py`；skills 目录与 optional-skills；README 声明兼容 agentskills.io 开放标准。
- 工具：`[源码] tools/`：delegation（delegate_tool、async_delegation、delegation_context）、budget_config、checkpoint_manager、cronjob_tools、computer_use、browser（camofox/CDP）、approval.py、managed_tool_gateway、mcp_dashboard_oauth。
- 权限：`[源码] hermes_cli/approval_mode.py`、`approvals.py`、`approval_transport.py`；`acp_adapter/permissions.py`、`edit_approval.py`。
- 网关：`[源码] gateway/`：channels（Telegram/Discord/Slack/WhatsApp/Signal）、platform_registry、delivery、lifecycle_ledger、pairing、authz、hooks、profile_routing、restart_loop_guard。
- 执行后端：`[文档] README`——local、Docker、SSH、Singularity、Modal、Daytona、Vercel Sandbox 七种，含 serverless 持久化。
- 协议：`[源码] acp_adapter/`（server、session、tools、provenance）。
- Provider：`[源码] agent/`：anthropic_adapter、gemini_native_adapter、codex_responses_adapter、bedrock_adapter、azure_identity_adapter。
- 元 Harness 借鉴：ACP adapter 自带 provenance、lifecycle ledger、approval modes；学习闭环（技能创建/改进/失效）是技能治理生命周期实例；FTS5 会话检索是证据检索参考；七后端说明“sandbox 能力”必须按后端逐一登记。

## 13. 横向观察

### 13.1 Agent loop 已收敛
所有 11 个 Harness 都有“模型调用 → 工具执行 → 结果回填 → 上下文管理”的 attempt/reply 循环，且多数有独立 loop 模块（Pi/OpenClaw `agent-loop.ts`、Goose `agent.rs`、Gemini `agent-session.ts`、Cline `ClineCore.ts`、Kimi `loop/`、Crush `coordinator.go`、Mistral `agent_loop/_loop.py`、Hermes `conversation_loop.py`）。元 Harness 不需要再造一个循环，而是治理循环的边界事实（版本、工具面、权限、证据）。

### 13.2 权限语义高度异质
- 声明式：Gemini TOML 策略文件；Goose permission.yaml 三级。
- 代码链：Kimi 19 policy/11 维度责任链；Qwen 分类器 + 危险规则；OpenClaw tool policy；Mistral PermissionStore；Crush permission service。
- 审批流：Cline auto-approve；Hermes approval modes；Kimi approval service；OpenClaw gateway-question/native-hook-relay。
- 硬约束 vs 可豁免：Kimi 明确区分“harness 约束（硬 deny，无 ask 通道）”与“权限（可豁免 ask/deny）”。
结论：元 Harness 的权限治理必须是“登记 + 一致性审计”而非统一引擎；manifest 需要表达权限语义类别与默认姿态。

### 13.3 Sandbox 能力 ≠ 默认安全
- Pi 无内建权限/沙箱（文档给容器化模式）；OpenClaw sandbox 默认 off（mode/scope/elevated）；Hermes 七种后端；Gemini 平台 sandbox + 默认策略文件；Goose 只有检查器无沙箱本体；其余未在源码中验证。
结论：registry 必须逐 revision 记录“能力存在”与“默认姿态”两个独立事实。

### 13.4 证据与契约机制成熟度
- Pi telemetry conformance 测试；Kimi v2 config/state/wire manifests + import boundary 检查；OpenClaw 原子 model runtime generation；Qwen goal evidence/checkpoint；Hermes ACP provenance + lifecycle ledger；Gemini evals/memory-tests/perf-tests；Goose gen_ai_telemetry/otel。
结论：元 Harness 的 evidence 层应借鉴“契约 manifest + conformance 测试 + 原子快照 + 可审计行为记录”的组合。

### 13.5 ACP 正在成为跨 harness 控制协议
OpenHands、Kimi、Goose、Cline、Mistral、Hermes 都提供或消费 ACP；Gemini 用 A2A。元 Harness 的控制面适配器应把 ACP 视为第一候选协议，但保留对原生协议（如 Codex app-server、Claude Code 插件面）的登记。

### 13.6 学习闭环与技能治理
Hermes 技能自改进、Qwen auto-skills、Pi skills/packages、OpenClaw skills、Kimi skills、Mistral skills：技能（skill）是跨 harness 的通用资产类型，元 Harness 需要技能版本、来源、信任级别与失效机制。

## 14. 局限与未验证项

- 本档案是静态源码阅读，不是运行验证；sandbox/ACP/权限行为未实际执行。
- Cline/Qwen/Kimi/Crush/Mistral 的 sandbox 状态未在源码中定位到明确实现，标为“未验证”，不推断其能力。
- OpenHands agent core 在 `OpenHands/software-agent-sdk`，不在本 checkout；Claude Code CLI 核心不在官方仓库。
- 各仓库功能命名与目录随 revision 变化；任何结论随 lock revision 失效。

## 15. 元 Harness 借鉴清单（回写领域模型的输入）

1. Harness registry 与 runtime 选择策略：参考 OpenClaw `src/agents/harness/` 与 OpenHands `backend-registry`，但元 Harness 只登记治理事实，不拥有运行态。
2. 权限治理：参考 Kimi 硬约束/可豁免二分、Goose 三级权限、Gemini TOML 策略、OpenClaw tool policy；manifest 必须表达权限语义类别与默认姿态。
3. 证据与遥测：参考 Pi telemetry conformance、Kimi contract manifests、OpenClaw 原子 runtime generation、Hermes provenance。
4. 控制协议：ACP 为第一候选适配协议；A2A、原生 app-server、插件面为备选。
5. Sandbox 登记：能力存在与默认姿态分开记录（Pi 无、OpenClaw off、Hermes 多后端）。
6. 技能/插件治理：版本、来源、信任级别、自动更新元数据、恶意性检查（Goose extension_malware_check）。
7. 目标与预算治理：Qwen goal evidence/checkpoint、Kimi goal 预算限额、Mistral turn budget、Hermes iteration budget。
