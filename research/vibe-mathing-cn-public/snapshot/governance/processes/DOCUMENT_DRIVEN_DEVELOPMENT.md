---
id: PROC-DOCUMENT-DRIVEN-DEVELOPMENT
type: process
status: current
owner: engineering
created: 2026-08-13
last_reviewed: 2026-08-13
review_cycle: P90D
---

# Document Driven Development

文档驱动开发不是多写文档，而是让项目的关键事实先有稳定真相源，再让代码、任务、审查和交付围绕这些真相源闭环。

## 适用范围

默认适用于：

- 新增功能、接口、数据模型、配置、依赖、任务流程或运行模式。
- 修改既有业务逻辑、模块边界、公共契约、工具链或发布方式。
- 产生长期影响的 bug 修复、复盘、审查反馈或架构决策。

## 执行顺序

1. 读取 `context/PROJECT_OPERATING_MODEL.md`。
2. 使用 `context/CONTEXT-ROUTER.md` 选择最小上下文。
3. 判断本次变更影响哪些真相源。
4. 若变更会改变项目理解、模块边界、流程、契约或工具链，先更新对应文档或在任务包中记录明确豁免理由。
5. 实现代码、运行验证、记录证据。
6. closeout 前执行文档同步检查，确认所有受影响真相源已更新或明确无需更新。

## 文档影响分类

| 影响类型 | 默认落点 | 说明 |
|---|---|---|
| 项目整体理解变化 | `context/PROJECT_OPERATING_MODEL.md` | 项目定位、边界、核心流程、事实源变化 |
| 执行流程变化 | `processes/DOCUMENT_DRIVEN_DEVELOPMENT.md` | 开发、验证、交付、回填流程变化 |
| 工具链变化 | `context/TOOLCHAIN_MODEL.md` | 构建、测试、发布、脚本、成熟工具边界变化 |
| 架构决策 | `decisions/adr/` | 有 trade-off、难反转、未来会惊讶的决策 |
| 质量护栏 | `architecture-gates/rules/` | 可复发、可检测、必须阻止的问题 |
| 任务执行证据 | `tasks/` | 计划、状态、验收、验证、closeout |
| 模块事实 | `context/module-contexts/` 或项目局部 README/AGENTS | 模块职责、边界、上下游、验证入口 |

## Closeout 必填判断

每个非平凡任务 closeout 必须回答：

- 本次是否改变项目操作模型。
- 本次是否改变工具链模型。
- 本次是否改变文档驱动开发流程。
- 本次是否改变模块上下文、ADR、Gate、contract、catalog、README 或 AGENTS。
- 若没有更新文档，原因是什么。

## 不接受的做法

- 代码已经改变系统事实，但文档仍描述旧事实。
- 只在聊天记录里说明变更，不落到项目可迁移资产。
- 把任务包临时结论当成长期真相源。
- 用泛泛的“无需更新文档”绕过 closeout 证据。
