---
id: CTX-DOCS
type: module-context
status: current
owner: engineering
created: 2026-09-03
last_reviewed: 2026-09-04
code_path: docs
---

# 领域与需求文档 Context

## 代码路径

`docs`

## 模块职责

- 解释 Vibe Harness CN 的稳定领域概念、系统边界和目标架构。
- 保存 Harness 内 PSOA 算子库的需求基线、非目标、验收、当前实现边界和演进路线。
- 解释 Operator Core Contract、可选 Profile、扩展与运行时安全的规范分层。
- 为 `contracts/`、ADR、实现任务和评审提供语义输入。

## 非职责

- 不复制 JSON Schema 的字段级机器约束。
- 不保存任务执行状态、运行证据、生产 trace 或生命周期事实。
- 不实现 Operator Library、Selector、Harness Runtime、Verifier、registry service 或业务 Binding；
  已实现内容只在此记录，其机器真相仍归 `contracts/`、`operators/` 与具体参考消费方。

## 禁止事项

- 禁止把外部标准的完整语义未经验证直接声明为项目契约。
- 禁止把 prompt、tool、operator、method、workflow 和 harness 混成同一概念。
- 禁止把 Operator Library 画成 Harness 外部的统一业务执行 runtime。
- 禁止把规划中的需求写成已经实现、已验证或生产可用的能力。

## 单一真相源

- Harness 总体领域模型：`docs/HARNESS_MODEL.md`。
- Harness 内 AI 问题求解算子库架构需求：`docs/PROBLEM_SOLVING_OPERATOR_ARCHITECTURE_PRD.md`。
- Operator Core/Profile 规范：`docs/OPERATOR_SPEC.md`。
- Operator Runtime Core 与参考 Harness 边界：`docs/OPERATOR_SPEC.md` 和 ADR-0007。
- 字段级机器契约：`contracts/`，文档只引用、不复制。
- 架构决策：`governance/decisions/adr/`。
- 数学问题求解研究输入：`research/MATHEMATICAL_PROBLEM_SOLVING_RESEARCH.md`；文档只消费其结论，不复制 55 项语义真相。

## 依赖边界

`research/` 与外部标准提供设计输入；`docs/` 固化稳定语义；ADR 记录长期取舍；`contracts/`
把已确认语义变成机器约束；`scripts/` 和未来 Harness Binding 只能消费这些契约，不能反向改写领域定义。

## 常用验证

- `python3 governance/tools/validate_governance_package.py --project-root . --strict`

## 相关治理文档

- `governance/decisions/adr/ADR-0001-元-Harness-采用契约优先的治理控制面.md`
- `governance/decisions/adr/ADR-0003-引入问题求解算子语义层.md`
- `governance/decisions/adr/ADR-0004-问题求解算子采用宽松核心与可选加严-Profile.md`

## Agent Rules

- 不要把本模块上下文散落到代码目录。
- 如需引用原模块 README，只在这里链接，不复制覆盖。
- 新增字段前先更新 owning PRD/领域模型，再另立契约任务同步 Schema、正例和负例。
- PRD 中的 SHOULD/MUST 是目标需求；只有实现、测试和版本绑定证据才能证明能力已经交付。
