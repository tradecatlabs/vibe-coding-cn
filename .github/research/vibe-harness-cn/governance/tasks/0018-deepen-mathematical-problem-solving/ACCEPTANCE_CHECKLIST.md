# Acceptance Checklist

# Global Standards
- [x] 来源事实、项目综合分类和 Agent 迁移推断分开
- [x] 已有同义条目只 crosswalk，不复制
- [x] 内容保持 experimental/reference_only，不自行授权或裁决
- [x] 八个数学过程分组不替代项目八类 functional taxonomy

# Task Package Checklists
## TP-01
- 标题: 核验数学问题求解框架
- 验收项:
  - [x] 来源事实、项目综合分类和迁移推断明确分开
- Verify: 核对验收项: 来源事实、项目综合分类和迁移推断明确分开
- Gate: 任务目标与上下文已确认
- 输出物:
  - [x] research/MATHEMATICAL_PROBLEM_SOLVING_RESEARCH.md
- 标准清单:
  - [x] Verify: 核对验收项: 来源事实、项目综合分类和迁移推断明确分开
  - [x] Gate: 任务目标与上下文已确认
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-02
- 标题: 逐项审计 55 个方法
- 验收项:
  - [x] 55/55 行均有决策、目标 ID、过程组和功能主类
- Verify: 核对验收项: 55/55 行均有决策、目标 ID、过程组和功能主类
- Gate: 前置步骤已完成: research-frameworks
- 输出物:
  - [x] research/MATHEMATICAL_PROBLEM_SOLVING_RESEARCH.md
- 标准清单:
  - [x] Verify: 核对验收项: 55/55 行均有决策、目标 ID、过程组和功能主类
  - [x] Gate: 前置步骤已完成: research-frameworks
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-03
- 标题: 沉淀数学算子与组合方法
- 验收项:
  - [x] 411 source、57 derived、468 total 一致且新增条目结构完整
- Verify: 核对验收项: 411 source、57 derived、468 total 一致且新增条目结构完整
- Gate: 前置步骤已完成: crosswalk-55
- 输出物:
  - [x] operators/packs/mathematics.json
  - [x] operators/source-inventory.json
  - [x] operators/catalog.json
  - [x] operators/taxonomy/problem-solving-methodology.json
- 标准清单:
  - [x] Verify: 核对验收项: 411 source、57 derived、468 total 一致且新增条目结构完整
  - [x] Gate: 前置步骤已完成: crosswalk-55
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-04
- 标题: 同步文档与治理真相
- 验收项:
  - [x] 所有受影响 source-of-truth 一致或有明确豁免
- Verify: 核对验收项: 所有受影响 source-of-truth 一致或有明确豁免
- Gate: 前置步骤已完成: materialize-mathematics
- 输出物:
  - [x] research/
  - [x] docs/
  - [x] governance/
  - [x] README.md
  - [x] AGENTS.md
- 标准清单:
  - [x] Verify: 核对验收项: 所有受影响 source-of-truth 一致或有明确豁免
  - [x] Gate: 前置步骤已完成: materialize-mathematics
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-05
- 标题: 验证、审查与交付
- 验收项:
  - [x] required deterministic gates 绑定当前输入和 clean HEAD；独立审查缺失时不宣称完全完成
- Verify: 核对验收项: required deterministic gates 绑定当前输入和 clean HEAD；独立审查缺失时不宣称完全完成
- Gate: 前置步骤已完成: sync-docs-governance
- 输出物:
  - [x] governance/tasks/0018-deepen-mathematical-problem-solving/REVIEW.md
  - [x] governance/tasks/0018-deepen-mathematical-problem-solving/VERIFICATION_PLAN.json
- 标准清单:
  - [x] Verify: 核对验收项: required deterministic gates 绑定当前输入和 clean HEAD；独立审查缺失时不宣称完全完成
  - [x] Gate: 前置步骤已完成: sync-docs-governance
  - [ ] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检
