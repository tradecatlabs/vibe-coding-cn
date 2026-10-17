# Task Overview
- Task ID: `0006`
- Slug: `define-problem-solving-operator-prd`
- Objective: `建立 AI 问题求解算子架构的需求基线、系统边界、核心对象、能力要求与验收标准`
- Status: `Done`

## In Scope
- 形成 `docs/PROBLEM_SOLVING_OPERATOR_ARCHITECTURE_PRD.md` 需求基线。
- 定义系统定位、相邻概念边界、三类状态、核心对象、功能/非功能需求、MVP 与验收。
- 新增 ADR-0003，并同步 docs module context、项目入口、项目操作模型和拓扑。
- 完成文档漂移审查、治理严格校验与项目门禁。

## Out of Scope
- 不实现 Operator/Method JSON Schema、validator、planner、registry、executor 或 adapter。
- 不修改现有 Harness manifest 契约、验证脚本和测试行为。
- 不批量开采具体算子，不引入服务、数据库、UI 或依赖。
- 不宣称完整兼容任何外部 planning/workflow/provenance 标准。

## Task Package Tree
```text
TP-01 冻结 PSOA 需求与领域边界
  -> TP-02 同步架构决策、导航与治理上下文
      -> TP-03 自审、严格校验与本地交付
```

## Requirement Alignment
- 用户要求把跨学科问题求解方法整理成 AI Harness 可调用的标准算子库，并开始制作需求文档。
- 已确认核心不是 prompt 集合，而是任务意图与 Harness 执行之间的语义层。
- JSON 是后续序列化载体；本任务先冻结产品需求、语义和验收，不提前锁死字段实现。
- STRIPS/PDDL、HTN、BPMN/CMMN、DMN、TEVV、PROV、Essence 作为设计输入，不成为首版完整依赖。

## Task Package Overview
| ID | 目标 | 主要输出 | Depends On |
|---|---|---|---|
| TP-01 | 冻结问题、用户、边界、对象、需求和验收 | PSOA PRD | - |
| TP-02 | 把新组件登记进长期架构真相 | ADR、module context、README/AGENTS、操作模型 | TP-01 |
| TP-03 | 检查一致性、风险和可交付状态 | REVIEW、校验与提交证据 | TP-02 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
