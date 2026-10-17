# Task-Level Acceptance

# Acceptance Criteria
- 六个新增母领域都有独立来源、方法提炼、适用边界、证据要求和未验证项
- 新增 source pack 与 derived Method 的 source key、计数、引用、ID 和治理 owner 精确一致
- 新增条目可解析到八类功能主类并保留母领域来源轴；公共 Core 继续宽松
- 既有 256 source、32 derived 和 reference-only 边界无回归；当前扩展后为 286 source、38 derived、324 total
- approved plan 已成功编译为递归任务树
- 叶子节点数量: 10
- 当前可立即执行叶子节点: TP-01.01, TP-01.02, TP-01.03, TP-01.04, TP-01.05, TP-01.06

# Validation Plan
- 运行 uv run --locked --script scripts/validate_harness.py --operator-library operators/catalog.json
- 运行 uv run --locked --script scripts/validate_harness.py --self-test
- 运行 python3 scripts/verify_project.py --gate architecture、behavior、contract、test
- 运行治理 strict、health、principle、任务文档、audit sampling 和任务级 verification 校验
- TP-01.01 | Verify: 核对验收项: 形成可追溯的规格、子目标、反模型和内核证据程序 | Gate: 父步骤范围已确认: research-evidence
- TP-01.02 | Verify: 核对验收项: 保留观察、推断、辅助假设和未决分支的边界 | Gate: 父步骤范围已确认: research-evidence
- TP-01.03 | Verify: 核对验收项: 结论绑定观测、尺度、校准、质量平衡和验证条件 | Gate: 父步骤范围已确认: research-evidence
- TP-01.04 | Verify: 核对验收项: 保留仪器、背景、模型、尺度和独立确认的不确定性 | Gate: 父步骤范围已确认: research-evidence
- TP-01.05 | Verify: 核对验收项: 形成从加工变量到结构、性能和校准证据的受限链条 | Gate: 父步骤范围已确认: research-evidence
- TP-01.06 | Verify: 核对验收项: 区分检索相关性、来源权威、完整性、公平性和事实正确性 | Gate: 父步骤范围已确认: research-evidence
- TP-02 | Verify: 核对验收项: 每个候选有 add/crosswalk/gap 决策；不因追求数量重复登记同义条目 | Gate: 前置步骤已完成: research-evidence
- TP-03 | Verify: 核对验收项: 新增 source 有来源和功能主类；治理字段保持 harness_policy、verifier、reference_only；derived Method 只引用已登记条目 | Gate: 前置步骤已完成: gap-audit
- TP-04 | Verify: 核对验收项: source inventory、pack 和 catalog 精确一致；所有受影响 source-of-truth 已更新或记录具体豁免 | Gate: 前置步骤已完成: define-operators
- TP-05 | Verify: 核对验收项: required gates 全部 PASS；任务级 verification 绑定当前输入、策略和真实 artifact；未验证项与后续路径已记录 | Gate: 前置步骤已完成: materialize-library

# Review Gate
- 每个领域有来源事实、迁移推断、边界、失败/恢复和未知项
- 每个新增 source key 可回指报告、来源和功能主类
- 既有 256/32 基线与公共 Core 宽松契约保持
- 高风险领域没有被描述为自动执行、专业意见或责任授权

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
- 治理 strict/health/principle、task docs、review、reuse 和 verification PASS
- 回滚路径、未验证项和文档同步状态齐全

# Task Package Acceptance
## TP-01
- 标题: 六个新增母领域分别深度抓取证据
- 验收标准:
  - 六个领域均有独立来源与边界记录
  - 每个候选方法区分来源事实与项目推断
- Verify: 确认子节点范围、依赖与状态闭环
- Gate: 任务目标与上下文已确认
- 输出物: research/HEURISTIC_METACOGNITIVE_RESEARCH.md；research/DOMAIN_EVIDENCE_MATRIX.md

### TP-01.01
- 标题: 形式逻辑与自动推理研究
- 验收标准:
  - 形成可追溯的规格、子目标、反模型和内核证据程序
- Verify: 核对验收项: 形成可追溯的规格、子目标、反模型和内核证据程序
- Gate: 父步骤范围已确认: research-evidence
- 输出物: research/DOMAIN_EVIDENCE_MATRIX.md

### TP-01.02
- 标题: 哲学与科学认识论研究
- 验收标准:
  - 保留观察、推断、辅助假设和未决分支的边界
- Verify: 核对验收项: 保留观察、推断、辅助假设和未决分支的边界
- Gate: 父步骤范围已确认: research-evidence
- 输出物: research/DOMAIN_EVIDENCE_MATRIX.md

### TP-01.03
- 标题: 地球科学与地学研究
- 验收标准:
  - 结论绑定观测、尺度、校准、质量平衡和验证条件
- Verify: 核对验收项: 结论绑定观测、尺度、校准、质量平衡和验证条件
- Gate: 父步骤范围已确认: research-evidence
- 输出物: research/DOMAIN_EVIDENCE_MATRIX.md

### TP-01.04
- 标题: 天文学与天体物理研究
- 验收标准:
  - 保留仪器、背景、模型、尺度和独立确认的不确定性
- Verify: 核对验收项: 保留仪器、背景、模型、尺度和独立确认的不确定性
- Gate: 父步骤范围已确认: research-evidence
- 输出物: research/DOMAIN_EVIDENCE_MATRIX.md

### TP-01.05
- 标题: 材料科学研究
- 验收标准:
  - 形成从加工变量到结构、性能和校准证据的受限链条
- Verify: 核对验收项: 形成从加工变量到结构、性能和校准证据的受限链条
- Gate: 父步骤范围已确认: research-evidence
- 输出物: research/DOMAIN_EVIDENCE_MATRIX.md

### TP-01.06
- 标题: 信息与知识科学研究
- 验收标准:
  - 区分检索相关性、来源权威、完整性、公平性和事实正确性
- Verify: 核对验收项: 区分检索相关性、来源权威、完整性、公平性和事实正确性
- Gate: 父步骤范围已确认: research-evidence
- 输出物: research/DOMAIN_EVIDENCE_MATRIX.md

## TP-02
- 标题: 既有库缺口与重复审计
- 验收标准:
  - 每个候选有 add/crosswalk/gap 决策
  - 不因追求数量重复登记同义条目
- Verify: 核对验收项: 每个候选有 add/crosswalk/gap 决策；不因追求数量重复登记同义条目
- Gate: 前置步骤已完成: research-evidence
- 输出物: research/DOMAIN_EVIDENCE_MATRIX.md；operators/taxonomy/problem-solving-methodology.json

## TP-03
- 标题: 提炼新增算子与组合 Method
- 验收标准:
  - 新增 source 有来源和功能主类
  - 治理字段保持 harness_policy、verifier、reference_only
  - derived Method 只引用已登记条目
- Verify: 核对验收项: 新增 source 有来源和功能主类；治理字段保持 harness_policy、verifier、reference_only；derived Method 只引用已登记条目
- Gate: 前置步骤已完成: gap-audit
- 输出物: operators/packs/；operators/source-inventory.json；operators/taxonomy/problem-solving-methodology.json

## TP-04
- 标题: 入库并同步目录文档
- 验收标准:
  - source inventory、pack 和 catalog 精确一致
  - 所有受影响 source-of-truth 已更新或记录具体豁免
- Verify: 核对验收项: source inventory、pack 和 catalog 精确一致；所有受影响 source-of-truth 已更新或记录具体豁免
- Gate: 前置步骤已完成: define-operators
- 输出物: operators/catalog.json；research/；docs/；governance/；README.md；AGENTS.md

## TP-05
- 标题: 验证、审查与交付收口
- 验收标准:
  - required gates 全部 PASS
  - 任务级 verification 绑定当前输入、策略和真实 artifact
  - 未验证项与后续路径已记录
- Verify: 核对验收项: required gates 全部 PASS；任务级 verification 绑定当前输入、策略和真实 artifact；未验证项与后续路径已记录
- Gate: 前置步骤已完成: materialize-library
- 输出物: governance/tasks/0014-third-wave-domain-research/REVIEW.md；governance/tasks/0014-third-wave-domain-research/VERIFICATION_PLAN.json

# Anti-Goals
- 不把静态研究条目宣称为生产效果、专业意见或自动授权
- 不实现 selector、planner、runtime、Binding、数据库、在线 registry 或 UI
- 不修改公共 Core Schema、上游来源登记、revision lock 或被忽略 checkout
