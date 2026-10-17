---
id: ADR-0007
type: record
status: active
owner: engineering
created: 2026-09-04
last_reviewed: 2026-09-04
source: docs/PROBLEM_SOLVING_OPERATOR_ARCHITECTURE_PRD.md
related_gates: [GATE-0000, GATE-0001]
---

# ADR-0007 以参考 Harness 验证 Operator Runtime 互操作契约

## 背景

项目已经有 468 条静态问题求解内容和宽松 Operator Pack Core，但没有可运行证据证明具体 Harness
能完成选择、绑定、物化、验证与溯源。直接在元 Harness 中建设中央 Runtime 会产生第二个执行 owner；
只增加 Schema 又无法检验运行语义。

## 决策或结论

- 新增宽松 `Operator Runtime Core`，只固定 `OperatorBinding`、`OperatorRunRequest` 和
  `OperatorRunRecord` 的交换信封、安全边界与摘要 provenance。
- 在 `examples/reference_harness/` 放置一个具体 Harness 参考消费方。它拥有自己的 Binding 和策略，
  但不成为元 Harness 服务，也不保存共享运行状态。
- 第一种 Binding 只做 `instruction_materialization`，效果范围固定为 `none`，禁止模型、工具和外部写入。
- Selector 对 catalog 做确定性 `O(n)` 元数据过滤与评分；Method 展开受 `max_steps` 约束。
- Executor 只产出候选信息和 instruction packet；Verifier 从原始请求、Binding、库和 taxonomy 重算，
  不信任 Executor 自报摘要。
- `completed/accepted` 的 claim scope 固定为 `instruction_materialization_only`，不得解释为问题已解决。

## 证据

- `contracts/operator-runtime.schema.json` 与三个最小 Runtime 样例。
- `examples/reference_harness/reference_harness.py` 和 Harness 本地 Binding。
- `tests/test_reference_operator_harness.py` 覆盖三种 Spec、组合展开、预算、策略、未知/循环引用、篡改与 CLI 非零退出。
- `uv run --locked --script scripts/validate_harness.py --self-test` 同时验证 Runtime 正例、扩展和稳定字段负例。

## 取舍

- 不选中央 Runtime：它会违反“Operator Library 属于具体 Harness”的 owner 边界。
- 不选只写 Schema：没有执行路径就无法证伪 Binding、预算、摘要与失败语义。
- 不选通用 Planner/SDK：只有一个参考消费方，提取框架会增加未经证明的所有权面。
- 不执行真实模型或工具：当前 proof point 是协议互操作，不是方法效果或生产安全。

## 目标终态

每个真实 Harness 本地实现 Selector、Binding、Execute、Verify 与 Trace；元 Harness 只发布共享 Core、
conformance corpus、评测和生命周期策略。两个独立 Harness 能使用同一 Operator 定义、不同 Binding，
产生同一语义范围内可比较的记录，且不共享内部业务状态。

## 真实约束与迁移

- Runtime Core 使用独立 `api_version`，不改变现有 Operator Pack `v1alpha1`。
- `problem` 与 `extensions` 保持开放；稳定字段拼写、类型、owner 与摘要边界严格校验。
- 第二个 Harness 出现前不提取共享 Binding SDK，不引入服务、数据库、队列或插件框架。
- 若真实 Harness 不能在不改写 Core 语义的情况下接入，应修订错误抽象，不保留双轨语义。

## 惯性约束

- 过去只有静态库和“运行态待实现”的文档不是必须保持的外部契约。
- 当前目录形状、单一 Python 实现和示例 Binding 都不能约束第二个真实 Harness 的正确设计。

## Kill list

- 中央 Operator Runtime、在线状态服务和通用 Planner。
- 只有一个消费方时抽取的 Binding SDK、插件系统和兼容双轨。
- 把物化成功包装成问题解决成功的结果模型。

## Proof point 与 falsifier

- Proof point：三种 Spec 经 Harness 本地 Binding 产生确定性 instruction packet，Verifier 能从原始输入
  重算并拒绝篡改，Trace 不复制问题正文。
- Falsifier：第二个独立 Harness 必须改写 Core 字段含义、无法表达本地策略上限，或无法产出相同
  claim scope 的记录；任一成立都要求回到契约层修订。

## Migration slice

本轮只增加 Runtime Core、一个无副作用参考 Harness 和 conformance 测试；下一切片接入第二个独立
Harness，只有两个实现出现重复稳定代码后才评估共享 SDK。

## 回滚路径

通过普通反向提交移除 Runtime Schema、参考 Harness、测试和本 ADR，并把文档恢复为“仅静态
conformance”。没有数据库、远端状态或生产流量需要迁移；静态 Operator Library 不受影响。

## 后续动作

- [ ] 接入第二个独立 Harness Binding，运行同一 conformance corpus。
- [ ] 为真实 LLM/tool execution 定义 Observation/Evidence，但保持执行者与 Verifier 职责分离。
- [ ] 建立开发集、密封留出集、质量/成本指标后，再讨论复杂 Selector 或 Planner。
