# Task-Level Acceptance
- 六个候选母领域都有独立来源、方法提炼、适用边界和未验证项；证据不足的领域明确保留为缺口
- 新增 source pack 与 derived Method 的 source key、计数、引用、ID 和治理 owner 精确一致
- 新增条目可解析到八类功能主类，并保留来源母领域轴；公共 Core 继续宽松
- 任务开始时既有 196 source、20 derived 和 reference-only 边界无回归；当前新增后总量为 226 source、26 derived
- approved plan 已成功编译为递归任务树
- 叶子节点数量: 10
- 当前可立即执行叶子节点: TP-01.01, TP-01.02, TP-01.03, TP-01.04, TP-01.05, TP-01.06

# Validation Plan
- 运行 python3 scripts/validate_harness.py --operator-library operators/catalog.json
- 运行 python3 scripts/validate_harness.py --self-test
- 运行 python3 scripts/verify_project.py --gate architecture、behavior、contract、test
- 运行治理 strict、health、principle、任务文档、audit sampling 和任务级 verification 校验
- TP-01.01 | Verify: 核对验收项: 至少形成可审计的因果建模、干预或敏感性程序 | Gate: 父步骤范围已确认: research-evidence
- TP-01.02 | Verify: 核对验收项: 明确假设、参与者、收益、约束和均衡/偏离证据 | Gate: 父步骤范围已确认: research-evidence
- TP-01.03 | Verify: 核对验收项: 区分机制假设、观察证据、模型和现实实验边界 | Gate: 父步骤范围已确认: research-evidence
- TP-01.04 | Verify: 核对验收项: 把认知发现转换为问题空间动作而非人格或能力标签 | Gate: 父步骤范围已确认: research-evidence
- TP-01.05 | Verify: 核对验收项: 明确人为复核、升级、停止和恢复边界，不自动放行高影响动作 | Gate: 父步骤范围已确认: research-evidence
- TP-01.06 | Verify: 核对验收项: 所有结论标记为参考，明确不能替代专业诊疗或临床流程 | Gate: 父步骤范围已确认: research-evidence
- TP-02 | Verify: 核对验收项: 每个候选有 add/crosswalk/gap 决策；不因追求数量重复登记同义条目 | Gate: 前置步骤已完成: research-evidence
- TP-03 | Verify: 核对验收项: 所有新增 source 有来源和功能主类；治理字段保持 harness_policy、verifier、reference_only；derived Method 只引用已登记条目 | Gate: 前置步骤已完成: gap-audit
- TP-04 | Verify: 核对验收项: source inventory、pack 和 catalog 精确一致；所有受影响 source-of-truth 已更新或记录具体豁免 | Gate: 前置步骤已完成: define-operators
- TP-05 | Verify: 核对验收项: required gates 全部 PASS；任务级 verification 绑定 clean HEAD、当前输入、策略和 artifact；未验证项与后续路径已记录 | Gate: 前置步骤已完成: materialize-library

# Review Gate
- 每个候选领域有来源事实、迁移推断、边界和未知项
- 每个新增 source key 可回指报告、来源和功能主类
- 既有 196/20 基线与公共 Core 宽松契约保持；新增条目未改变 Core 必填字段
- 高影响领域没有被描述为自动执行或专业授权

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
- 标题: 因果推断研究
- 验收标准:
  - 至少形成可审计的因果建模、干预或敏感性程序
- Verify: 核对验收项: 至少形成可审计的因果建模、干预或敏感性程序
- Gate: 父步骤范围已确认: research-evidence
- 输出物: research/DOMAIN_EVIDENCE_MATRIX.md

### TP-01.02
- 标题: 经济与博弈研究
- 验收标准:
  - 明确假设、参与者、收益、约束和均衡/偏离证据
- Verify: 核对验收项: 明确假设、参与者、收益、约束和均衡/偏离证据
- Gate: 父步骤范围已确认: research-evidence
- 输出物: research/DOMAIN_EVIDENCE_MATRIX.md

### TP-01.03
- 标题: 生态与生物研究
- 验收标准:
  - 区分机制假设、观察证据、模型和现实实验边界
- Verify: 核对验收项: 区分机制假设、观察证据、模型和现实实验边界
- Gate: 父步骤范围已确认: research-evidence
- 输出物: research/DOMAIN_EVIDENCE_MATRIX.md

### TP-01.04
- 标题: 认知科学研究
- 验收标准:
  - 把认知发现转换为问题空间动作而非人格或能力标签
- Verify: 核对验收项: 把认知发现转换为问题空间动作而非人格或能力标签
- Gate: 父步骤范围已确认: research-evidence
- 输出物: research/DOMAIN_EVIDENCE_MATRIX.md

### TP-01.05
- 标题: 人因可靠性研究
- 验收标准:
  - 明确人为复核、升级、停止和恢复边界，不自动放行高影响动作
- Verify: 核对验收项: 明确人为复核、升级、停止和恢复边界，不自动放行高影响动作
- Gate: 父步骤范围已确认: research-evidence
- 输出物: research/DOMAIN_EVIDENCE_MATRIX.md

### TP-01.06
- 标题: 医学决策研究
- 验收标准:
  - 所有结论标记为参考，明确不能替代专业诊疗或临床流程
- Verify: 核对验收项: 所有结论标记为参考，明确不能替代专业诊疗或临床流程
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
  - 所有新增 source 有来源和功能主类
  - 治理字段保持 harness_policy、verifier、reference_only
  - derived Method 只引用已登记条目
- Verify: 核对验收项: 所有新增 source 有来源和功能主类；治理字段保持 harness_policy、verifier、reference_only；derived Method 只引用已登记条目
- Gate: 前置步骤已完成: gap-audit
- 输出物: operators/packs/；operators/source-inventory.json；operators/taxonomy/problem-solving-methodology.json

## TP-04
- 标题: 入库并同步目录文档
- 验收标准:
  - source inventory、pack 和 catalog 精确一致
  - 所有受影响 source-of-truth 已更新或记录具体豁免
- Verify: 核对验收项: source inventory、pack 和 catalog 精确一致；所有受影响 source-of-truth 已更新或记录具体豁免
- Gate: 前置步骤已完成: define-operators
- 输出物: operators/catalog.json；research/HEURISTIC_METACOGNITIVE_RESEARCH.md；docs/；governance/

## TP-05
- 标题: 验证、审查与交付收口
- 验收标准:
  - required gates 全部 PASS
  - 任务级 verification 绑定 clean HEAD、当前输入、策略和 artifact
  - 未验证项与后续路径已记录
- Verify: 核对验收项: required gates 全部 PASS；任务级 verification 绑定 clean HEAD、当前输入、策略和 artifact；未验证项与后续路径已记录
- Gate: 前置步骤已完成: materialize-library
- 输出物: governance/tasks/0012-expand-next-domain-heuristics/REVIEW.md；governance/tasks/0012-expand-next-domain-heuristics/VERIFICATION_PLAN.json

# Anti-Goals
- 不得修改 `governance/tasks/` 以外路径
- 不得虚构证据
- 不得越权补全未确认信息
