---
id: ADR-0004
type: record
status: active
owner: engineering
created: 2026-09-03
last_reviewed: 2026-09-03
source: docs/OPERATOR_SPEC.md
related_gates: [GATE-0000, GATE-0001]
---

# ADR-0004 问题求解算子采用宽松核心与可选加严 Profile

## 背景

首个 Operator Pack Schema 为了证明 75+7 参考库完整，把七个领域、说明字段、适用性、步骤、证据、
失败、恢复和集合数量都写成公共必填。这能约束当前库，却会让新领域、草稿条目和不同 Harness
必须复制本项目的内容写法，混淆“机器可交换”与“方法已经完整”。

## 决策或结论

- Operator Pack 采用两层 conformance：公共 `Core Contract` 与显式版本化 `Profile`。
- Core 只强制稳定 envelope、字段类型、ID/version、kind 判别、source 条件、显式 `extensions`
  和不可改写的权限/结果/sensitive owner。
- `domain`、效果/outcome 词汇和内容集合保持开放；说明、适用性、步骤、证据、失败、恢复和数量
  在 Core 中可选，由 Profile、review、eval 或 Harness runtime 按场景加严。
- 稳定对象继续拒绝未知同级字段；扩展必须放入 `extensions`，防止拼写错误静默通过。
- 省略治理字段不产生授权。实际权限、工具、预算和 outcome 仍由 Harness policy 与 Verifier 裁决。
- 本仓库 catalog 使用 `vibe-harness-cn/reference-library-v1`，继续严格验证 75/75 source、7/7
  derived、完整内容、计数、全局 ID、引用、无环、路径和安全 owner。
- Core 与 Profile 分别版本化；Profile 变化不能静默修改公共 Core 含义。

候选路径及取舍：

1. 保持单一严格 Schema：门禁简单，但把一个参考实现误当全球标准，拒绝。
2. 完全开放 `additionalProperties`：扩展方便，但字段拼写和语义漂移不可见，拒绝。
3. 宽松 Core + 显式 `extensions` + 可选 Profile：互操作、演进和局部质量门禁可分离，采用。

## 证据

- Proof point：自定义 `systems-thinking` 领域、空 `semantics` 与命名空间扩展的最小 Pack 通过
  Core；未知同级字段和错误类型被拒绝。
- Profile proof：既有 catalog 仍输出 `source_coverage=75/75 derived_methods=7/7 total=82`，删除
  Profile 内容字段会被拒绝。
- Falsifier：第二个真实 Harness 仍需修改 Core Schema 才能表达一个不改变安全边界的新领域或
  方法写法；若发生，继续收缩 Core，而不是增加供应商特例。

### Target end state

Core 是小而稳定的交换 ISA；Profile 是按消费场景选择的准入包；Evaluation 判断有效性；Harness
Runtime 拥有权限和执行。四层分别演进、显式绑定。

### Real constraints

- 既有 82 个条目必须继续通过，且无需迁移。
- 权限、自我批准、路径逃逸和引用类型不能因内容放宽而失守。
- JSON Schema 仍应发现未知稳定字段与错误类型。

### Inertia constraints

- 当前七领域、固定写作模板和 75+7 数量是参考库事实，不是公共协议承诺。
- 原 Schema 的必填列表已经存在，不构成继续保留的理由。

### Kill list

- 公共 Schema 中的封闭七领域枚举。
- 公共 Schema 中的内容字段、列表非空与固定数量门槛。
- 把 Reference Library exact-set 校验称为第三方 Core conformance。

### Migration slice

保持 `v1alpha1` 字段名和既有条目不变，只放宽可选性与开放词汇；新增最小 Core 样例、单 Pack
校验入口和显式 Reference Profile 标识。后续 Profile 只有在真实消费方出现后新增。

### Rejected short-term patches

- 不通过复制第二份几乎相同的严格 Schema 模拟宽松模式。
- 不用 CLI 隐藏开关让同一规则在不同场景下含义不明。
- 不允许任意未知顶层字段来换取表面扩展性。

## 影响范围

- `contracts/problem-solving-operator-pack.schema.json` 仍是 Core 字段真相源。
- `docs/OPERATOR_SPEC.md` 解释规范层级；PRD 描述成熟能力，不再等同于 Core required 字段。
- `operators/catalog.json` 与 `scripts/validate_operator_library.py` 共同实现 Reference Profile。
- 放宽是向后兼容变化，回滚可反向提交；没有持久数据或运行态迁移。

## 后续动作

- [ ] 用第二个真实 Harness/领域 pack 检验 Core 是否仍含本项目私有假设。
- [ ] 运行时 Evidence/Provenance 契约出现后，决定是否形成独立 execution Profile。
