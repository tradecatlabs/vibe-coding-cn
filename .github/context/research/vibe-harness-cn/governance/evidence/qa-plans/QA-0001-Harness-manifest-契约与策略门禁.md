---
id: QA-0001
type: record
status: active
owner: engineering
created: 2026-08-14
last_reviewed: 2026-08-14
source: contracts/harness-manifest.schema.json
related_gates: [GATE-0000, GATE-0001]
---

# QA-0001 Harness manifest 契约与策略门禁

## 功能范围

验证 `v1alpha1` Harness manifest 的结构完整性和关键跨字段策略，不验证真实模型效果或生产安全。

## 用户旅程

开发者提交 manifest，运行一个命令获得 PASS 或带 JSON path 的 BLOCK；错误必须非零退出，
验证输出不得回显凭据、完整 prompt 或工具内容。

## 验收场景

- [x] 成功路径：最小 coding harness 通过 Schema 与策略校验。
- [x] 失败路径：缺少 `loop.stop_conditions` 的 fixture 被 Schema 拒绝。
- [x] 策略路径：`privileged` 工具声明 `approval=never` 时被跨字段策略拒绝。
- [x] 边界输入：不提供路径或同时使用 `--self-test` 和路径时返回参数错误。

## 验证证据

```bash
uv run --locked --script scripts/validate_harness.py --self-test
uv run --locked --script scripts/validate_harness.py contracts/examples/minimal-coding-harness.json
python3 -m json.tool contracts/harness-manifest.schema.json
python3 -m py_compile scripts/validate_harness.py
```

门禁限制：本地自测只证明确定性 conformance，不提供独立 reviewer provenance，也不允许把
candidate manifest 直接晋升为生产可用。
