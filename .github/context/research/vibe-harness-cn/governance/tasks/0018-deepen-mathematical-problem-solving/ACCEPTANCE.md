# Task-Level Acceptance
- 55/55 个方法有明确 reuse/add 决策和目标 ID
- 411/411 source、57/57 derived、468 total 通过 Reference Profile
- 新增方法均有步骤、证据、停止条件和失败模式
- 公共 Core 保持宽松，目录文档和治理快照一致
- approved plan 已成功编译为递归任务树
- 叶子节点数量: 5
- 当前可立即执行叶子节点: TP-05（本地确定性收口已完成；最终关闭仍等待外部独立 reviewer）

# Validation Plan
- uv run --locked --script scripts/validate_harness.py --operator-library operators/catalog.json
- uv run --locked --script scripts/validate_harness.py --self-test
- python3 scripts/verify_project.py --gate architecture/behavior/contract/test
- 治理 strict、health、principle、task docs、audit sampling 和任务级 verification
- TP-01 | Verify: 核对验收项: 来源事实、项目综合分类和迁移推断明确分开 | Gate: 任务目标与上下文已确认
- TP-02 | Verify: 核对验收项: 55/55 行均有决策、目标 ID、过程组和功能主类 | Gate: 前置步骤已完成: research-frameworks
- TP-03 | Verify: 核对验收项: 411 source、57 derived、468 total 一致且新增条目结构完整 | Gate: 前置步骤已完成: crosswalk-55
- TP-04 | Verify: 核对验收项: 所有受影响 source-of-truth 一致或有明确豁免 | Gate: 前置步骤已完成: materialize-mathematics
- TP-05 | Verify: 核对验收项: required deterministic gates 绑定当前输入和 clean HEAD；独立审查缺失时不宣称完全完成 | Gate: 前置步骤已完成: sync-docs-governance

# Review Gate
- 55 行 crosswalk 数量和名称逐项吻合
- 新增 source key、ID、引用、计数和 Method 图一致
- 样例/计算实验不冒充证明，reference-only 边界不变
- 公共 Core、既有 432 条基线和其他 pack 无回归

# Runtime Verification Gate
- [x] 每个 tool/action 结果都有可回指证据或明确未执行原因。
- [x] 高风险动作没有由 worker/agent 自我批准；审批状态可追踪。
- [x] compaction / resume 后目标、计划、修改文件、审批状态和验证项未丢失。
- [x] verifier / 自审已检查关键发现是否有证据支持。
- [x] closeout 明确 coverage gaps、failed packets 和 unresolved questions。
- [x] TP-01: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [x] TP-02: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [x] TP-03: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [x] TP-04: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [x] TP-05: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据

# Ship Readiness
- Reference Library validator 与 self-test PASS
- architecture、behavior、contract、test gates PASS
- 治理 strict/health/principle、任务 docs、reuse 和 verification 校验通过
- 独立 reviewer 缺失时任务保持 In Progress，不伪造最终 PASS

# Task Package Acceptance
## TP-01
- 标题: 核验数学问题求解框架
- 验收标准:
  - 来源事实、项目综合分类和迁移推断明确分开
- Verify: 核对验收项: 来源事实、项目综合分类和迁移推断明确分开
- Gate: 任务目标与上下文已确认
- 输出物: research/MATHEMATICAL_PROBLEM_SOLVING_RESEARCH.md

## TP-02
- 标题: 逐项审计 55 个方法
- 验收标准:
  - 55/55 行均有决策、目标 ID、过程组和功能主类
- Verify: 核对验收项: 55/55 行均有决策、目标 ID、过程组和功能主类
- Gate: 前置步骤已完成: research-frameworks
- 输出物: research/MATHEMATICAL_PROBLEM_SOLVING_RESEARCH.md

## TP-03
- 标题: 沉淀数学算子与组合方法
- 验收标准:
  - 411 source、57 derived、468 total 一致且新增条目结构完整
- Verify: 核对验收项: 411 source、57 derived、468 total 一致且新增条目结构完整
- Gate: 前置步骤已完成: crosswalk-55
- 输出物: operators/packs/mathematics.json；operators/source-inventory.json；operators/catalog.json；operators/taxonomy/problem-solving-methodology.json

## TP-04
- 标题: 同步文档与治理真相
- 验收标准:
  - 所有受影响 source-of-truth 一致或有明确豁免
- Verify: 核对验收项: 所有受影响 source-of-truth 一致或有明确豁免
- Gate: 前置步骤已完成: materialize-mathematics
- 输出物: research/；docs/；governance/；README.md；AGENTS.md

## TP-05
- 标题: 验证、审查与交付
- 验收标准:
  - required deterministic gates 绑定当前输入和 clean HEAD；独立审查缺失时不宣称完全完成
- Verify: 核对验收项: required deterministic gates 绑定当前输入和 clean HEAD；独立审查缺失时不宣称完全完成
- Gate: 前置步骤已完成: sync-docs-governance
- 输出物: governance/tasks/0018-deepen-mathematical-problem-solving/REVIEW.md；governance/tasks/0018-deepen-mathematical-problem-solving/VERIFICATION_PLAN.json

# Anti-Goals
- 不得修改公共 Core Schema、运行时权限模型或 Harness 执行状态
- 不得修改上游 registry、lock、同步器或 checkout
- 不得执行上游代码、现实实验、部署、远端写入或凭据读取
- 不得虚构证据
- 不得把静态来源与结构校验宣称为真实 Agent 效果或独立审查
