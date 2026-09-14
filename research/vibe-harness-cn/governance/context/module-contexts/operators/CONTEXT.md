---
id: CTX-OPERATORS
type: module-context
status: current
owner: engineering
created: 2026-09-03
last_reviewed: 2026-09-04
code_path: operators
---

# 问题求解算子库 Context

## 代码路径

`operators`

## 模块职责

- 保存 Harness 可装载的供应商中立问题求解内容。
- 用独立 source inventory 固定当前跨学科清单的 411 个原始条目。
- 用五十六个 pack 保存 411 个 source 条目和 57 个显式 derived Method，并声明 Reference Library Profile。
- 用 `operators/taxonomy/problem-solving-methodology.json` 分离母领域出处与八类功能映射；该视图不执行算子。

## 非职责

- 不执行算子，不选择下一步，不调用模型或工具。
- 不拥有 Harness-specific Binding、权限、业务状态、Evidence 裁决或生产生命周期。
- 不冒充 PDDL、HTN、BPMN、CMMN、DMN、TEVV、PROV 或 Essence 的完整实现。

## 单一真相源

- 原始条目完整性：`operators/source-inventory.json`。
- pack 注册和全库计数：`operators/catalog.json`。
- 条目内容：`operators/packs/*.json`。
- 双轴分类视图：`operators/taxonomy/problem-solving-methodology.json`。
- Core 结构契约：`contracts/problem-solving-operator-pack.schema.json`。
- Core/Profile 规范：`docs/OPERATOR_SPEC.md`。
- 架构语义：`docs/PROBLEM_SOLVING_OPERATOR_ARCHITECTURE_PRD.md` 与 `ADR-0003`。

## 不变量

- 当前 Reference Profile 下，source keys 必须与 inventory 精确相等，不能缺少、增加或重复。
- 全局 entry ID 唯一；Method 引用和来源引用必须解析。
- `MentalModelSpec` 不得伪装现实副作用；derived 条目必须是明确标记的 `MethodSpec`。
- 权限归 Harness policy，结果归 Verifier，敏感值只允许受控引用。
- 未完成真实 Binding 与 eval 前，条目状态保持 `experimental`。

## 常用验证

- `uv run --locked --script scripts/validate_harness.py --operator-library operators/catalog.json`
- `uv run --locked --script scripts/validate_harness.py --self-test`

## Agent Rules

- 修改条目时同步 inventory、pack metadata、catalog totals 和相关文档。
- 不用修改 inventory 与 pack 的同一项来掩盖清单缩水；任务验收必须回看用户来源清单。
- 不把整库默认注入模型上下文；未来 selector 必须先做廉价适用性过滤。
- 不把本仓库 411+57 内容规则或八类功能映射提升为第三方 pack 的 Core Contract。
