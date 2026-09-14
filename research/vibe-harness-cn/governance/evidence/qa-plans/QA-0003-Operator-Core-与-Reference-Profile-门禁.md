---
id: QA-0003
type: record
status: active
owner: engineering
created: 2026-09-03
last_reviewed: 2026-09-03
source: docs/OPERATOR_SPEC.md
related_gates: [GATE-0000, GATE-0001]
---

# QA-0003 Operator Core 与 Reference Profile 门禁

## 功能范围

验证公共 Core Contract 不锁死内容，同时本仓库 Reference Library Profile 保持完整性与安全门禁。
不执行 Operator，不证明方法效果，也不验证具体 Harness Binding。

## 用户旅程

第三方作者可提交自定义领域和渐进式 `draft` Pack，只要字段形状正确；本仓库维护者发布参考库时，
必须额外满足显式 Profile 的 411+57 内容、引用、计数和安全要求；双轴 taxonomy 只做分类审计，不增加 Core 字段要求。

## 验收场景

- [x] 最小 Core：自定义领域、最小 metadata、空 MentalModel semantics 可通过。
- [x] 空 Pack：`entries: []` 不因内容数量被 Core 拒绝。
- [x] 扩展：`extensions` 中的命名空间化内容可通过。
- [x] 字段格式：错误 SemVer 类型和未知同级字段被拒绝。
- [x] 类型边界：MentalModel 不得把 `effect` 伪装成动作语义。
- [x] Reference Profile：缺少成熟内容字段被拒绝。
- [x] 完整性：411/411 source、57/57 derived、总计 468 继续通过。
- [x] 安全：自授权、错误引用类型、Method 循环和路径逃逸继续被拒绝。

## 验证证据

```bash
uv run --locked --script scripts/validate_harness.py --operator-pack contracts/examples/minimal-operator-pack.json
uv run --locked --script scripts/validate_harness.py --operator-library operators/catalog.json
uv run --locked --script scripts/validate_harness.py --self-test
python3 scripts/verify_project.py --gate contract
python3 scripts/verify_project.py --gate test
```

验证复杂度仍为 `O(F + E + R)`；Core 单 Pack 校验为 `O(E)`。当前只读本地 JSON，没有网络、模型
调用或缓存，不是 hot path；在真实大型库 profile 显示 Schema 重复编译成为瓶颈前暂不优化。

## 剩余风险

- Core 通过只证明结构可解析，不证明内容完整、有效或安全可执行。
- `extensions` 内容由采用方理解；跨 Harness 依赖同一扩展时需要显式 Profile 或标准字段晋升。
- 尚未完成第二个真实 Harness 的互操作 proof。
