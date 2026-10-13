---
id: LESSON-0001
type: record
status: current
owner: engineering
created: 2026-08-14
last_reviewed: 2026-08-14
review_cycle: P90D
source: governance/tasks/0001-bootstrap-meta-harness/DEBUG.md
---

# 验证器必须消费 owner 契约

## 原子事实

验证器比被测对象“更严格”不必然更安全；如果它自行猜测输出类型或发明 owner 契约不存在
的字段，会把有效对象错误 BLOCK，并让验证控制面失去可信度。

## 适用规则

- 每个 gate 必须读取 owner 的机器 Schema、类型和状态语义，不能从自然语言或字段名猜结构。
- 对集合验证数量时先校验集合类型，再比较 `len`；不得把集合直接与整数比较。
- 若需要增强 owner 契约，先修改契约、样例和负例并版本化，再修改消费者。
- 修复 gate 误判时必须保留 RED/GREEN/反事实证据，不得通过放宽风险 profile 获得 PASS。

## 证据

- `governance/tasks/0001-bootstrap-meta-harness/DEBUG.md`
- `governance/tasks/0001-bootstrap-meta-harness/REGRESSION_EVIDENCE.json`
- `tests/test_verify_project.py`

## 失效条件

当所有 gate 输入都由类型系统生成且编译期证明消费者与 owner Schema 一致时，可重新评估本规则
的运行时检查部分；版本化与 owner 边界仍然成立。
