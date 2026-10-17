---
id: CTX-CONTRACTS
type: module-context
status: current
owner: engineering
created: 2026-08-14
last_reviewed: 2026-09-03
code_path: contracts
---

# Harness 契约 Context

## 代码路径

`contracts`

## 模块职责

定义供应商中立、版本化、可机检的 Harness manifest、Operator Pack Core 与 Operator Runtime Core，
并保存最小有效样例。

## 非职责

- 不实现模型调用、工具执行、任务调度、registry service 或运行时状态存储。
- 不证明实际效果、安全或生产晋升；这些需要版本绑定 eval 与运行证据。

## 禁止事项

- 禁止加入某个供应商 SDK 的私有 session/state 作为核心字段。
- 禁止把密钥、完整 prompt、工具参数/结果或客户数据写入 manifest 和样例。
- 禁止用自由文本替代权限、预算、停止条件、验证或证据绑定的结构化字段。

## 单一真相源

- 字段和结构：`contracts/harness-manifest.schema.json`。
- 算子 Core 结构：`contracts/problem-solving-operator-pack.schema.json`。
- 运行互操作信封：`contracts/operator-runtime.schema.json`。
- Core/Profile 语义：`docs/OPERATOR_SPEC.md`。
- 有效最小声明：`contracts/examples/minimal-coding-harness.json`。
- 领域语义：`docs/HARNESS_MODEL.md` 与 `governance/decisions/adr/ADR-0001-元-Harness-采用契约优先的治理控制面.md`。

## 常用验证

- `uv run --locked --script scripts/validate_harness.py --self-test`

## 相关治理文档

- `governance/standards/架构设计原则.md`
- `governance/decisions/adr/ADR-0001-元-Harness-采用契约优先的治理控制面.md`
- `governance/decisions/adr/ADR-0003-引入问题求解算子语义层.md`
- `governance/decisions/adr/ADR-0004-问题求解算子采用宽松核心与可选加严-Profile.md`
- `governance/evidence/qa-plans/QA-0001-Harness-manifest-契约与策略门禁.md`
- `governance/evidence/qa-plans/QA-0003-Operator-Core-与-Reference-Profile-门禁.md`

## Agent Rules

- 不要把本模块上下文散落到代码目录。
- 如需引用原模块 README，只在这里链接，不复制覆盖。
- Schema 变化必须同步正例、结构负例、策略负例和 `api_version` 破坏性变化判断。
- 不把特定领域、写作完整度、步骤/证据数量或 Reference Library exact-set 写进公共 Core Schema。
- Runtime Core 不规定 Selector 算法、领域 problem 字段或具体执行器；Binding 不能扩大 Harness policy。
