# Task-Level Acceptance
- 六个领域均有权威来源、方法提炼、边界和未验证项
- 376/376 source、56/56 derived、432 total 通过 Reference Profile
- 公共 Core 保持宽松，新增科学内容仍为 reference_only
- 治理文档、任务状态和当前快照一致
- approved plan 已成功编译为递归任务树
- 叶子节点数量: 10
- 当前可立即执行叶子节点: TP-01.01, TP-01.02, TP-01.03, TP-01.04, TP-01.05, TP-01.06

# Validation Plan
- uv run --locked --script scripts/validate_harness.py --operator-library operators/catalog.json
- uv run --locked --script scripts/validate_harness.py --self-test
- python3 scripts/verify_project.py --gate architecture/behavior/contract/test
- 治理 strict、health、principle、task docs、audit sampling 和任务级 verification
- TP-01.01 | Verify: 核对验收项: 形成线性结构诊断链 | Gate: 父步骤范围已确认: research-evidence
- TP-01.02 | Verify: 核对验收项: 形成结构保持与障碍检查链 | Gate: 父步骤范围已确认: research-evidence
- TP-01.03 | Verify: 核对验收项: 形成场问题建模验证链 | Gate: 父步骤范围已确认: research-evidence
- TP-01.04 | Verify: 核对验收项: 形成算子模型和近似有效性检查链 | Gate: 父步骤范围已确认: research-evidence
- TP-01.05 | Verify: 核对验收项: 形成相平衡模型一致性检查链 | Gate: 父步骤范围已确认: research-evidence
- TP-01.06 | Verify: 核对验收项: 形成多证据结构解析链 | Gate: 父步骤范围已确认: research-evidence
- TP-02 | Verify: 核对验收项: 每个候选有 add/crosswalk/gap 决策 | Gate: 前置步骤已完成: research-evidence
- TP-03 | Verify: 核对验收项: 新增条目通过 Core/Profile 结构与治理 owner 检查 | Gate: 前置步骤已完成: gap-audit
- TP-04 | Verify: 核对验收项: 所有受影响 source-of-truth 一致或记录豁免 | Gate: 前置步骤已完成: define-operators
- TP-05 | Verify: 核对验收项: required gates 通过并绑定当前输入、策略、artifact 和 clean HEAD | Gate: 前置步骤已完成: materialize-library

# Review Gate
- 每个领域有来源事实、迁移推断、边界、失败恢复和未知项
- source key、引用、计数和 Method 图精确一致
- 既有基线与公共 Core 无回归
- 科学内容没有自动执行或专业放行表述

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
- 标题: 六个基础领域深度抓取证据
- 验收标准:
  - 六个领域都有来源、程序、边界和停止理由
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 任务目标与上下文已确认
- 输出物: research/HEURISTIC_METACOGNITIVE_RESEARCH.md；research/DOMAIN_EVIDENCE_MATRIX.md

### TP-01.01
- 标题: 线性代数与谱方法研究
- 验收标准:
  - 形成线性结构诊断链
- Verify: 核对验收项: 形成线性结构诊断链
- Gate: 父步骤范围已确认: research-evidence
- 输出物: research/DOMAIN_EVIDENCE_MATRIX.md

### TP-01.02
- 标题: 拓扑与几何研究
- 验收标准:
  - 形成结构保持与障碍检查链
- Verify: 核对验收项: 形成结构保持与障碍检查链
- Gate: 父步骤范围已确认: research-evidence
- 输出物: research/DOMAIN_EVIDENCE_MATRIX.md

### TP-01.03
- 标题: 电磁场方法研究
- 验收标准:
  - 形成场问题建模验证链
- Verify: 核对验收项: 形成场问题建模验证链
- Gate: 父步骤范围已确认: research-evidence
- 输出物: research/DOMAIN_EVIDENCE_MATRIX.md

### TP-01.04
- 标题: 量子算子方法研究
- 验收标准:
  - 形成算子模型和近似有效性检查链
- Verify: 核对验收项: 形成算子模型和近似有效性检查链
- Gate: 父步骤范围已确认: research-evidence
- 输出物: research/DOMAIN_EVIDENCE_MATRIX.md

### TP-01.05
- 标题: 溶液热力学与相平衡研究
- 验收标准:
  - 形成相平衡模型一致性检查链
- Verify: 核对验收项: 形成相平衡模型一致性检查链
- Gate: 父步骤范围已确认: research-evidence
- 输出物: research/DOMAIN_EVIDENCE_MATRIX.md

### TP-01.06
- 标题: 光谱结构解析研究
- 验收标准:
  - 形成多证据结构解析链
- Verify: 核对验收项: 形成多证据结构解析链
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
- 输出物: governance/tasks/0017-sixth-wave-foundational-methods-research/REVIEW.md；governance/tasks/0017-sixth-wave-foundational-methods-research/VERIFICATION_PLAN.json

# Anti-Goals
- 不得修改 `governance/tasks/` 以外路径
- 不得虚构证据
- 不得越权补全未确认信息
