---
id: CTX-EXAMPLES
type: module-context
status: current
owner: engineering
created: 2026-09-04
last_reviewed: 2026-09-04
code_path: examples
---

# 协议参考消费方 Context

## 代码路径

`examples`

## 模块职责

- 提供共享契约的最小、可运行、非生产消费方。
- 当前参考 Harness 证明 Operator 的确定性选择、本地 Binding、无副作用物化、独立验证和摘要 Trace。
- 为第二个真实 Harness 接入提供 conformance 行为基线，而不是提供共享 Runtime SDK。

## 非职责

- 不成为中央 Runtime、在线服务、生产适配器或业务状态真相源。
- 不调用模型、执行工具、访问网络或声明方法有效。
- 不拥有 Operator Core、Reference Library 或项目 Gate 的规范真相。

## 单一真相源

- 交换字段：`contracts/operator-runtime.schema.json`。
- 算子内容与分类：`operators/catalog.json` 和 `operators/taxonomy/`。
- 参考 Binding：`examples/reference_harness/bindings/instruction-packet.json`。
- 架构取舍：`governance/decisions/adr/ADR-0007-以参考-Harness-验证-Operator-Runtime-互操作契约.md`。

## 常用验证

- `python3 -m unittest tests.test_reference_operator_harness`
- `python3 examples/reference_harness/reference_harness.py`

## Agent Rules

- 新增真实副作用、模型或工具前必须另立任务，并先建立权限、证据、恢复和安全门禁。
- 第二个 Harness 出现前不抽取 Binding SDK、插件接口或中央状态。
- 输出中的 `accepted` 只能描述当前 claim scope，不能扩大为问题解决或生产晋升。
