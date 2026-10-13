# Task-Level Acceptance
- 六个领域均有权威来源、方法提炼、边界和未验证项
- 346/346 source、50/50 derived、396 total 通过 Reference Profile
- 公共 Core 保持宽松，新增高风险内容仍为 reference_only
- 治理文档、任务状态和当前快照一致
- approved plan 已成功编译为递归任务树
- 叶子节点数量: 10
- 当前可立即执行叶子节点: TP-01.01, TP-01.02, TP-01.03, TP-01.04, TP-01.05, TP-01.06

# Validation Plan
- uv run --locked --script scripts/validate_harness.py --operator-library operators/catalog.json
- uv run --locked --script scripts/validate_harness.py --self-test
- python3 scripts/verify_project.py --gate architecture/behavior/contract/test
- 治理 strict、health、principle、task docs、audit sampling 和任务级 verification
- TP-01.01 | Verify: 核对验收项: 形成概率状态、界限和停止程序 | Gate: 父步骤范围已确认: research-evidence
- TP-01.02 | Verify: 核对验收项: 形成动态状态、稳定性和参数变化程序 | Gate: 父步骤范围已确认: research-evidence
- TP-01.03 | Verify: 核对验收项: 形成模型构造、守恒检查和扰动验证程序 | Gate: 父步骤范围已确认: research-evidence
- TP-01.04 | Verify: 核对验收项: 形成连续介质尺度分析和模型检查程序 | Gate: 父步骤范围已确认: research-evidence
- TP-01.05 | Verify: 核对验收项: 形成只读反应机理与数据一致性审计程序 | Gate: 父步骤范围已确认: research-evidence
- TP-01.06 | Verify: 核对验收项: 形成只读电化学信号归因和边界程序 | Gate: 父步骤范围已确认: research-evidence
- TP-02 | Verify: 核对验收项: 每个候选有 add/crosswalk/gap 决策 | Gate: 前置步骤已完成: research-evidence
- TP-03 | Verify: 核对验收项: 新增条目通过 Core/Profile 结构与治理 owner 检查 | Gate: 前置步骤已完成: gap-audit
- TP-04 | Verify: 核对验收项: 所有受影响 source-of-truth 一致或记录豁免 | Gate: 前置步骤已完成: define-operators
- TP-05 | Verify: 核对验收项: required gates 通过并绑定当前输入、策略、artifact 和 clean HEAD | Gate: 前置步骤已完成: materialize-library

# Review Gate
- 每个领域有来源事实、迁移推断、边界、失败/恢复和未知项
- source key、引用、计数和 Method 图精确一致
- 既有基线与公共 Core 无回归
- 高风险内容没有自动执行或专业放行表述

# Runtime Verification Gate
- [ ] 每个 tool/action 结果都有可回指证据或明确未执行原因。
- [ ] 高风险动作没有由 worker/agent 自我批准；审批状态可追踪。
- [ ] compaction / resume 后目标、计划、修改文件、审批状态和验证项未丢失。
- [ ] verifier / 自审已检查关键发现是否有证据支持。
- [ ] closeout 明确 coverage gaps、failed packets 和 unresolved questions。
- [ ] TP-01.01: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [ ] TP-01.02: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [ ] TP-01.03: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [ ] TP-01.04: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [ ] TP-01.05: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [ ] TP-01.06: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [ ] TP-02: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [ ] TP-03: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [ ] TP-04: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [ ] TP-05: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据

# Ship Readiness
- Reference Library validator 与 self-test PASS
- architecture、behavior、contract、test gates PASS
- 治理 strict/health/principle、任务 docs、review、reuse 和 verification 校验通过
- 回滚路径、文档同步状态和未验证项齐全

# Task Package Acceptance
## TP-01
- 标题: 六个动态科学领域深度抓取证据
- 验收标准:
  - 六个领域都有来源、程序、边界和停止理由
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 任务目标与上下文已确认
- 输出物: research/HEURISTIC_METACOGNITIVE_RESEARCH.md；research/DOMAIN_EVIDENCE_MATRIX.md

### TP-01.01
- 标题: 随机过程与概率过程研究
- 验收标准:
  - 形成概率状态、界限和停止程序
- Verify: 核对验收项: 形成概率状态、界限和停止程序
- Gate: 父步骤范围已确认: research-evidence
- 输出物: research/DOMAIN_EVIDENCE_MATRIX.md

### TP-01.02
- 标题: 微分方程与动力系统研究
- 验收标准:
  - 形成动态状态、稳定性和参数变化程序
- Verify: 核对验收项: 形成动态状态、稳定性和参数变化程序
- Gate: 父步骤范围已确认: research-evidence
- 输出物: research/DOMAIN_EVIDENCE_MATRIX.md

### TP-01.03
- 标题: 经典力学与变分方法研究
- 验收标准:
  - 形成模型构造、守恒检查和扰动验证程序
- Verify: 核对验收项: 形成模型构造、守恒检查和扰动验证程序
- Gate: 父步骤范围已确认: research-evidence
- 输出物: research/DOMAIN_EVIDENCE_MATRIX.md

### TP-01.04
- 标题: 流体与连续介质研究
- 验收标准:
  - 形成连续介质尺度分析和模型检查程序
- Verify: 核对验收项: 形成连续介质尺度分析和模型检查程序
- Gate: 父步骤范围已确认: research-evidence
- 输出物: research/DOMAIN_EVIDENCE_MATRIX.md

### TP-01.05
- 标题: 化学动力学研究
- 验收标准:
  - 形成只读反应机理与数据一致性审计程序
- Verify: 核对验收项: 形成只读反应机理与数据一致性审计程序
- Gate: 父步骤范围已确认: research-evidence
- 输出物: research/DOMAIN_EVIDENCE_MATRIX.md

### TP-01.06
- 标题: 电化学与传质研究
- 验收标准:
  - 形成只读电化学信号归因和边界程序
- Verify: 核对验收项: 形成只读电化学信号归因和边界程序
- Gate: 父步骤范围已确认: research-evidence
- 输出物: research/DOMAIN_EVIDENCE_MATRIX.md

## TP-02
- 标题: 既有库缺口与重复审计
- 验收标准:
  - 每个候选有 add/crosswalk/gap 决策
- Verify: 核对验收项: 每个候选有 add/crosswalk/gap 决策
- Gate: 前置步骤已完成: research-evidence
- 输出物: research/DOMAIN_EVIDENCE_MATRIX.md；operators/taxonomy/problem-solving-methodology.json

## TP-03
- 标题: 提炼新增算子与组合 Method
- 验收标准:
  - 新增条目通过 Core/Profile 结构与治理 owner 检查
- Verify: 核对验收项: 新增条目通过 Core/Profile 结构与治理 owner 检查
- Gate: 前置步骤已完成: gap-audit
- 输出物: operators/packs/；operators/source-inventory.json；operators/catalog.json；operators/taxonomy/problem-solving-methodology.json

## TP-04
- 标题: 入库并同步目录文档
- 验收标准:
  - 所有受影响 source-of-truth 一致或记录豁免
- Verify: 核对验收项: 所有受影响 source-of-truth 一致或记录豁免
- Gate: 前置步骤已完成: define-operators
- 输出物: operators/；research/；docs/；governance/；README.md；AGENTS.md

## TP-05
- 标题: 验证、审查与交付收口
- 验收标准:
  - required gates 通过并绑定当前输入、策略、artifact 和 clean HEAD
- Verify: 核对验收项: required gates 通过并绑定当前输入、策略、artifact 和 clean HEAD
- Gate: 前置步骤已完成: materialize-library
- 输出物: governance/tasks/0016-fifth-wave-dynamic-science-research/REVIEW.md；governance/tasks/0016-fifth-wave-dynamic-science-research/VERIFICATION_PLAN.json

# Anti-Goals
- 不得修改 `governance/tasks/` 以外路径
- 不得虚构证据
- 不得越权补全未确认信息
