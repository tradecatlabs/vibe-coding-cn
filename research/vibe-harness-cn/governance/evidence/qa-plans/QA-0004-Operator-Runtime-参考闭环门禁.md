---
id: QA-0004
type: record
status: active
owner: engineering
created: 2026-09-04
last_reviewed: 2026-09-04
source: governance/tasks/0019-reference-operator-runtime-proof/ACCEPTANCE.md
related_gates: [GATE-0000, GATE-0001]
---

# QA-0004 Operator Runtime 参考闭环门禁

## 功能范围

验证 Runtime Core 可交换，且一个无副作用参考 Harness 能执行
`Select → Bind → Materialize → Verify → Trace`。不证明方法效果、真实模型/工具安全或双 Harness 互操作。

## 验收场景

- [x] `OperatorBinding`、`OperatorRunRequest`、`OperatorRunRecord` 三类样例通过 Core Schema。
- [x] 显式 `extensions` 可通过，未知稳定字段和缺失 `binding_id` 被拒绝。
- [x] Selector 从 468 条目录中确定性选择，记录候选、理由、拒绝摘要和预算。
- [x] `OperatorSpec`、`MentalModelSpec`、`MethodSpec` 均可物化，`use/apply_model` 受限展开。
- [x] Binding owner、效果范围、模型/工具/外部写入和预算不能被请求扩大。
- [x] 未知引用、循环引用和步骤超限失败关闭。
- [x] Verifier 重算并拒绝被篡改的 packet/摘要。
- [x] provenance 只保存摘要、标识和阶段事件，不复制问题正文。
- [x] CLI 失败返回非零且不向 stdout 输出成功 bundle。

## 验证证据

```bash
uv run --locked --script scripts/validate_harness.py --operator-runtime \
  contracts/examples/minimal-operator-binding.json \
  contracts/examples/minimal-operator-run-request.json \
  contracts/examples/minimal-operator-run-record.json
python3 -m unittest tests.test_reference_operator_harness
python3 scripts/verify_project.py --gate contract
python3 scripts/verify_project.py --gate behavior
python3 scripts/verify_project.py --gate test
```

## 效率与优化检查

Selector 对 `n` 个目录条目单次扫描并排序候选，时间复杂度 `O(n + c log c)`、内存 `O(n + c)`；
当前 `n=468`，Verifier 为独立性再做一次同阶重算。真实目录达到 10x/100x 且 profile 显示排序或
JSON 加载成为 hot path 后，再引入倒排索引或缓存；当前不引入服务和缓存一致性成本。

## 剩余风险

- 只有一个参考 Harness，尚不能证明跨实现互操作。
- 参考 Binding 不执行模型和工具，不能外推生产安全或任务质量。
- Verifier 与 Executor 位于同一代码库，属于职责分离证明，不是外部独立 reviewer provenance。
