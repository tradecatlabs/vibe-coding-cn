# Review: 11 个新增 Harness 源码调研

## Scope

- `target`: merge_gate
- `review_depth`: deep
- `selected_profiles`: agent-harness, architecture, correctness, performance, reliability, repo-hygiene, security
- `specialized_routes`: agent-harness-runtime, knowledge-assets-zone
- `files`: `research/HARNESS_RESEARCH.md`、`research/UPSTREAMS.md`、`docs/HARNESS_MODEL.md`、
  research module context、根 README/AGENTS 指针与 0005 任务证据
- `base`: `fea46cc`（0004 已提交基线）
- `review mode`: 主 Codex 自审；只证明本地确定性门禁，不冒充外部独立 reviewer provenance

## Verdict

- `decision`: PASS
- `summary`: 11 个新增 Harness 的逐仓档案全部绑定 lock revision 与 `research/upstreams/<name>/`
  相对路径；宣传/实现差异与未验证项显式分级；横向结论与元 Harness 治理借鉴已回写领域文档，
  且明确标注为研究输入而非已实现能力。未发现剩余 BLOCK/WARN。

## Findings

### RV-001：sandbox 能力存在性必须按仓库分开判定（已按证据分级处理）

- `severity`: WARN（已处理）
- `confidence`: high
- `evidence`: Cline/Qwen/Kimi/Crush/Mistral 五仓的 sandbox 未在源码中定位明确实现，
  总览表与各仓小节统一标注“未验证”；Pi 无内建权限、OpenClaw 默认 off、Goose 只有
  inspector、Hermes 七后端均有明确源码或文档依据。
- `impact`: 若把“未验证”写成“不支持”或“默认安全”，会污染 registry 的能力事实。
- `minimal fix`: 研究档案固定“能力存在”与“默认姿态”两个独立列，未验证项不得推断；
  该规则已写入 `docs/HARNESS_MODEL.md` 9.3 与报告 13.3/14。

### RV-002：相邻仓库能力不得计入当前 checkout（边界已声明）

- `severity`: WARN（已处理）
- `confidence`: high
- `evidence`: OpenHands Agent Canvas 明确标注不含 agent core（runtime 在独立
  `OpenHands/software-agent-sdk`）；Claude Code 闭源 CLI 不参与本轮 11 仓范围。
- `impact`: 若不声明，控制面会把“控制中心”误记为“完整 harness”。
- `minimal fix`: 报告 0 节证据契约与 14 节局限显式声明边界，`UPSTREAMS.md` 保留负面可见性结论。

## Correctness And Source Boundaries

- 11 个研究目标的官方 origin、登记分支、lock revision 与 checkout HEAD 一致；结论全部可追溯到
  `research/upstreams/<name>/` 相对路径或 lock 绑定事实。
- 每个 Harness 小节固定结构：Revision、定位、Agent loop、Session/Memory、工具、权限、Sandbox、
  Provider、扩展、元 Harness 借鉴。
- 文档级证据（README/官方文档）与源码级证据显式分级；Goose AAIF 迁移、Gemini 向 Antigravity
  演进、Kimi v2 双 core、Crush FSL-1.1-MIT 等事实按 lock/文档绑定。

## Reliability And Security

- 本轮只做文本读取与 `rg`/`find` 检索，未执行、构建、安装或测试任何上游代码；未读取凭据。
- 未修改 source registry、同步器或 revision lock；checkout 保持 ignored 且不进入提交。
- 研究报告不含完整 prompt、工具参数或秘密；证据路径全部指向受治理 checkout 相对路径。

## Performance Audit

- `Complexity`: 调研为一次性静态阅读，报告本身无运行开销；检索使用索引式命令，未全量遍历
  2.6 GiB checkout。
- `Hot path`: 无运行时 hot path；报告维护成本随 harness 数量线性增长。
- `Decision`: 报告规模控制在每仓固定结构（共 205 行），不引入数据库、索引或服务；
  当 15 个以上 Harness 或需要机器查询时再评估结构化 registry 扩展。

## Principle And Document Review

- `Ponytail`: 复用既有 lock 与 Markdown 文档层；没有新增依赖、服务、数据库或第二来源登记。
- `Future-Optimal`: 横向结论指向 manifest 未来字段候选（权限语义类别、sandbox 默认姿态、
  控制协议、goal/budget），但明确不立即改 Schema，遵守既有契约变更规则。
- `Document drift`: 根 README、research/AGENTS、UPSTREAMS、领域模型、research module context
  与任务文档同步；研究结论与实现分离。
- `Test quality`: 本任务无代码变更；由 governance strict/health、task validators、四类项目
  门禁与 15 源一致性回归覆盖。

## Audit Case Consumption

- `route_review_scope.py` 与 `search_audit_cases.py` 对本次文件集合返回空命中；
  采样判定见 `AUDIT_CASE_SAMPLING.md`（no-case，附具体理由）。

## Unknowns And Evidence Boundary

- 静态源码阅读不是运行验证；sandbox/ACP/权限行为未实际执行。
- Cline/Qwen/Kimi/Crush/Mistral 的 sandbox 状态未在源码中定位，标为“未验证”，不推断能力。
- OpenHands agent core 不在本 checkout；Claude Code CLI 核心不在官方仓库。
- 各仓库目录结构随 revision 变化；结论随 `upstreams.lock.json` revision 失效。
- 没有远端、CI、PR 或外部 reviewer provenance；PASS 只表示本地确定性审查。

## Gate Checklist

- [x] correctness：11 仓事实绑定 revision 与源码路径，宣传/实现差异显式记录。
- [x] architecture：研究不改变系统边界；元 Harness 借鉴与控制面实现分离。
- [x] security：不执行上游、无凭据、checkout 保持 ignored。
- [x] performance：检索与报告零运行开销，规模上限与升级触发明确。
- [x] reliability：证据分级、revision 失效规则与相邻仓库边界声明完整。
- [x] repo-hygiene：选择性 stage，runtime/checkout 不进入提交。
- [x] document drift：领域模型、研究基线、module context 与任务证据同步。

## Required Post-Commit Verification

- 在最终提交后的 clean HEAD 上重跑 governance strict/health、task docs closeout validator、
  四类项目门禁与 15 源一致性检查，并生成任务级 verification result。
- 无 remote 时只形成本地 commit，不声称已 push、PR、CI 或生产就绪。
