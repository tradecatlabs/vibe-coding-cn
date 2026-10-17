# Review: Operator Runtime 参考闭环

## Scope

- `target`: merge_gate
- `review_depth`: deep
- `subject`: Runtime Core、参考 Harness、失败关闭测试、项目 gate 接入以及架构/治理同步
- `base`: `fd30904`（本轮开始时的 clean HEAD）
- `review mode`: 主 Codex 本地只读深审；不冒充外部独立 reviewer provenance

## Verdict

- `decision`: PASS（本地范围审查）
- `summary`: 共享层只增加三个宽松运行信封；具体选择、Binding、物化、验证与 Trace 留在参考 Harness。本地实现无模型、无工具、无网络、无外部写入，正常路径和关键失败路径均有自动化证据。外部独立 reviewer receipt 尚未提供，因此任务保持 `In Progress`。

## Findings

- 已修复：`OperatorRunRecord` 的候选项和事件原先允许任意嵌套字段，与“稳定对象拒绝未知字段”冲突；现已复用严格 `selectedOperator` 定义，并为事件保留显式 `extensions`。
- 已修复：Python 的 `bool` 是 `int` 子类，原预算检查会把 `true` 当成 `1`；现改为精确整数类型检查并补回归。
- 已修复：packet 被篡改时原实现把 `materialization_status` 也写成 `rejected`，与事件链矛盾；现保留“物化完成”，只把 verification verdict 和记录状态置为 rejected。
- 已修复：Verifier 原先重复加载两次目录；现单次独立重载后同时完成重算和记录，保持职责分离并降低不必要 I/O。
- 已修复：最小 RunRecord 样例使用 `catalog`，真实参考记录使用 `library`；样例已对齐真实 provenance 键。
- 未发现：中央 Runtime、通用 Planner、SDK、服务、数据库、插件系统、模型/工具执行、远端写入、凭据读取或 Operator Library 内容变更。

## Selected Audit Case Consumption

- `CASE-0008 declared-marker-substitutes-for-derived-proof`：已检查 digest/verdict 是否由 Verifier 从原始 request、Binding、library、taxonomy 和 packet 重算；篡改 packet/摘要会被拒绝，未知稳定字段和非法预算有负例。
- `CASE-0013 unverified-git-remote-target-before-destructive-delivery`：路由命中但本轮只允许本地普通提交，无 remote push、强推、删除或远端目标变更，判定不适用。
- `CASE-0014 pages-custom-domain-rebind-without-dns-write`：没有部署、域名、DNS 或 Cloudflare 操作，判定不适用。

## Evidence And Boundaries

- Runtime Core 真相源：`contracts/operator-runtime.schema.json`；统一校验入口：`scripts/validate_harness.py --operator-runtime/--self-test`。
- 参考消费方：`examples/reference_harness/`；运行者只物化 instruction packet，Verifier 负责最终 verdict 和摘要记录。
- `completed/accepted` 固定为 `instruction_materialization_only`，不证明原问题解决、方法有效或生产安全。
- Runtime 模块只重复检查执行所需的安全不变量；完整字段形状由前置 Core validator 检查，避免复制 JSON Schema。
- Verifier 与 Executor 仍在同一代码库，只证明职责分离，不构成外部独立审查。

## Security, Reliability And Performance

- `_safe_child` 对 pack 路径 canonical resolve 并拒绝 catalog 目录逃逸；未知 Binding、effect scope 扩大、模型/工具/外部写入、预算超限、未知/循环引用全部失败关闭。
- Trace 只保存摘要、标识和阶段，不复制 `problem` 正文；错误经 stderr 输出并以状态 2 终止，不产生 stdout 成功 bundle。
- Selector 时间复杂度 `O(n + c log c)`、运行内存 `O(n + c)`；当前 `n=468`。Verifier 额外执行一次同阶重算。10x/100x 规模且 profile 证明排序或 JSON 加载成为 hot path 前，不引入索引、缓存或服务。
- 本轮没有 DB、并发、远端 API、模型 token 或云资源成本；这些 review route 均不适用。

## Document Drift

- 已同步根 README/AGENTS、contracts/docs/scripts/tests/examples 的 AGENTS/README、Harness Model、Operator Spec、PSOA PRD、ADR-0007、QA-0004、项目操作模型、拓扑、工具链、context map/router 和 module contexts。
- `operators/` 内容保持 `411 source + 57 derived = 468`，无需修改 catalog/inventory/taxonomy。
- 上游 registry、lock、同步器和 checkout 未改变。

## Required Follow-up

- clean-HEAD 任务级 verification 已通过，四个 required gate 均无 issue；运行证据位于任务目录下被忽略的 `runtime/verification/`。
- 由真实 external reviewer 提供绑定最终 HEAD 的独立 receipt 后，才能关闭任务级独立审查门禁。
- 下一协议 proof 应由第二个独立 Harness 实现不同 Binding；真实 LLM/tool execution 必须另建权限、Observation/Evidence 和评测切片。

## Rollback

- 通过普通反向提交移除 Runtime Schema、参考 Harness、测试和文档/治理同步；不执行 reset、checkout 或 clean。当前没有持久业务状态、远端资源或数据迁移。
