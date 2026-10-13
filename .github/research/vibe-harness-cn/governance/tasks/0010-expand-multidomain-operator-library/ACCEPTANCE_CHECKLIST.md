# Acceptance Checklist

# Global Standards
- [x] 来源优先使用一手/权威资料，推断与资料事实分开记录
- [x] 每个条目必须说明适用条件、操作步骤、成功/失败证据和恢复方向
- [x] 参考内容保持 experimental，不授予自身权限，不把学科知识写成执行授权
- [x] 公共 Core 继续宽松，Reference Profile 继续负责本仓库精确完整性

# Task Package Checklists
## TP-01
- 标题: 建立跨学科证据矩阵
- 验收项:
  - [x] 数学/物理/化学优先证据完整
  - [x] 点名其他领域均有覆盖计划与来源
- Verify: 检查研究报告、来源台账、候选清单、局限和未验证项
- Gate: 每个核心候选都有可追溯权威来源，事实、推断和未知分开
- 输出物:
  - [x] research/EXPANDED_OPERATOR_RESEARCH.md
  - [x] operators/source-inventory.json
- 标准清单:
  - [x] Verify: 检查研究报告、来源台账、候选清单、局限和未验证项
  - [x] Gate: 每个核心候选都有可追溯权威来源，事实、推断和未知分开
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-02
- 标题: 定义算子语义与领域边界
- 验收项:
  - [x] 优先领域算子可被 Harness 选择但不自带权限
  - [x] 重复或无法执行的候选被拒绝
- Verify: 检查每个 entry 的类型、语义字段、治理 owner、source_refs 和状态
- Gate: 新增算子不越过 Core/Profile、安全 owner 和 reference-only 边界
- 输出物:
  - [x] operators/packs/*.json
- 标准清单:
  - [x] Verify: 检查每个 entry 的类型、语义字段、治理 owner、source_refs 和状态
  - [x] Gate: 新增算子不越过 Core/Profile、安全 owner 和 reference-only 边界
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-03
- 标题: 入库并同步目录文档
- 验收项:
  - [x] 新 domain 已登记且计数一致
  - [x] 旧条目和既有引用无回归
- Verify: 运行 JSON 结构检查与 Reference Profile 校验，并核对文档中的规模与边界
- Gate: inventory/catalog/packs 精确一致，文档没有遗留 75+7 的过期事实
- 输出物:
  - [x] operators/catalog.json
  - [x] operators/packs/
  - [x] docs/
  - [x] governance/
- 标准清单:
  - [x] Verify: 运行 JSON 结构检查与 Reference Profile 校验，并核对文档中的规模与边界
  - [x] Gate: inventory/catalog/packs 精确一致，文档没有遗留 75+7 的过期事实
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-04
- 标题: 验证、审查与交付收口
- 验收项:
  - [x] 验证结果 PASS 或对真实 blocker fail-closed
  - [x] 回滚路径和未验证项清楚可见
- Verify: 运行 operator self-test、project gates、governance strict/health/principle 和任务 docs validator
- Gate: 所有 required gate 绑定当前输入、策略和真实产物；失败项明确记录
- 输出物:
  - [x] governance/tasks/0010-expand-multidomain-operator-library/REVIEW.md
  - [x] governance/tasks/0010-expand-multidomain-operator-library/REUSE_SAMPLING.json
- 标准清单:
  - [x] Verify: 运行 operator self-test、project gates、governance strict/health/principle 和任务 docs validator
  - [x] Gate: 所有 required gate 绑定当前输入、策略和真实产物；失败项明确记录
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检
