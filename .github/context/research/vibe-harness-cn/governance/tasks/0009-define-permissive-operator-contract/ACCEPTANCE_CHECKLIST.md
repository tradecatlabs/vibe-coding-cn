# Acceptance Checklist

# Global Standards
- [x] 公共契约只约束互操作所需结构和不可省略的安全边界
- [x] 方法质量与内容完整度使用 SHOULD、lint、eval 或显式 Profile，不混入 Core Schema
- [x] 扩展进入 extensions，不能暗改标准字段含义
- [x] 放宽契约不得削弱 Reference Library 的完整性回归

# Task Package Checklists
## TP-01
- 标题: 定义宽松核心与 Profile 边界
- 验收项:
  - [x] Core 与 Reference Profile 职责不重叠
  - [x] 安全边界有明确保留理由
- Verify: 检查规范覆盖 Core、Profile、extensions、兼容性和安全边界
- Gate: 任何字段强制项都能由互操作或安全必要性解释
- 输出物:
  - [x] docs/OPERATOR_SPEC.md
  - [x] governance/decisions/adr/ADR-0004-问题求解算子采用宽松核心与可选加严-Profile.md
- 标准清单:
  - [x] Verify: 检查规范覆盖 Core、Profile、extensions、兼容性和安全边界
  - [x] Gate: 任何字段强制项都能由互操作或安全必要性解释
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-02
- 标题: 放宽 Schema 并标注参考库 Profile
- 验收项:
  - [x] 领域、描述和语义集合不再被公共 Schema 过度限制
  - [x] extensions 是唯一开放扩展容器
- Verify: 运行 JSON Schema 自校验和既有 7 个 pack 校验
- Gate: 既有内容兼容，最小自定义领域 pack 可通过，未知稳定字段被拒绝
- 输出物:
  - [x] contracts/problem-solving-operator-pack.schema.json
  - [x] operators/catalog.json
- 标准清单:
  - [x] Verify: 运行 JSON Schema 自校验和既有 7 个 pack 校验
  - [x] Gate: 既有内容兼容，最小自定义领域 pack 可通过，未知稳定字段被拒绝
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-03
- 标题: 实现 Core 与 Reference 回归
- 验收项:
  - [x] 最小 pack 与 extensions 有正例
  - [x] 错类型、未知字段、自授权、坏引用和路径逃逸仍失败
- Verify: 运行 --operator-pack、--operator-library 与 --self-test
- Gate: Core 正例通过、结构负例拒绝、Reference 75+7 回归通过
- 输出物:
  - [x] scripts/validate_harness.py
  - [x] scripts/validate_operator_library.py
- 标准清单:
  - [x] Verify: 运行 --operator-pack、--operator-library 与 --self-test
  - [x] Gate: Core 正例通过、结构负例拒绝、Reference 75+7 回归通过
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检
  - [x] `debug_required=false`，无需创建 DEBUG.md；回归证据由 self-test 与 project gates 保存

## TP-04
- 标题: 同步文档治理并完成验证
- 验收项:
  - [x] 项目入口、模块上下文、QA 和 ADR 一致
  - [ ] 最终证据绑定当前代码与策略
- Verify: 运行 project gates、governance strict/health、task docs 与 Git 输入检查
- Gate: 没有文档漂移或未解释的长期约束
- 输出物:
  - [x] README.md
  - [x] AGENTS.md
  - [x] docs/
  - [x] governance/
  - [x] governance/tasks/0009-define-permissive-operator-contract/
- 标准清单:
  - [x] Verify: 运行 project gates、governance strict/health、task docs 与 Git 输入检查
  - [ ] Gate: 没有文档漂移或未解释的长期约束（高风险 retrospective handoff 待外部 reviewer）
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [ ] 交付前完成 REVIEW / SHIP 自检（产品 review 已完成，task closeout 尚未完成）
