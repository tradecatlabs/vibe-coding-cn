# Task-Level Acceptance
- 研究报告按八类功能分别记录来源、事实、项目推断、母领域映射、适用边界和未知项
- 统计学、决策科学、运筹学、设计方法及上位问题求解方法论形成可机检的新增覆盖
- 八类交叉索引覆盖当前参考库，entry 引用、pack、inventory、catalog 计数精确一致
- 既有条目和 Core/Profile、安全 owner、reference-only 边界无回归
- approved plan 已成功编译为递归任务树
- 叶子节点数量: 11
- 当前可立即执行叶子节点: TP-01.01, TP-01.02, TP-01.03, TP-01.04, TP-01.05, TP-01.06, TP-01.07, TP-01.08

# Validation Plan
- 运行 python3 scripts/validate_harness.py --operator-library operators/catalog.json
- 运行 python3 scripts/validate_harness.py --self-test
- 运行 python3 scripts/verify_project.py --gate architecture|behavior|contract|test
- 运行治理 strict、health、principle、任务文档和任务级 verification 校验
- TP-01.01 | Verify: 核对验收项: 记录表征改变如何缩小或重构问题空间 | Gate: 父步骤范围已确认: research-evidence
- TP-01.02 | Verify: 核对验收项: 记录子问题边界、依赖和合并证据 | Gate: 父步骤范围已确认: research-evidence
- TP-01.03 | Verify: 核对验收项: 记录变换保持什么、损失什么和如何回译 | Gate: 父步骤范围已确认: research-evidence
- TP-01.04 | Verify: 核对验收项: 记录搜索预算、剪枝条件和回退路径 | Gate: 父步骤范围已确认: research-evidence
- TP-01.05 | Verify: 核对验收项: 记录候选产物、可运行见证和失败处理 | Gate: 父步骤范围已确认: research-evidence
- TP-01.06 | Verify: 核对验收项: 区分证明、证伪、验证、确认和 inconclusive | Gate: 父步骤范围已确认: research-evidence
- TP-01.07 | Verify: 核对验收项: 记录最小失败案例、首个失效点和回归证据 | Gate: 父步骤范围已确认: research-evidence
- TP-01.08 | Verify: 核对验收项: 记录何时继续、停止、换路和升级人工 | Gate: 父步骤范围已确认: research-evidence
- TP-02 | Verify: 检查新增条目的 kind、语义、来源、主类/辅助类、治理 owner、失败和恢复 | Gate: 新增方法不把母领域事实写成权限，不引入重复或无法验证的空壳条目
- TP-03 | Verify: 运行 JSON/引用/计数检查并核对文档规模、双轴边界和未验证项 | Gate: catalog、inventory、packs、taxonomy 与文档没有漂移或悬空引用
- TP-04 | Verify: 运行 operator self-test、项目 gates、治理 strict/health/principle 和 task closeout validators | Gate: required gate 绑定当前输入、策略和真实产物；失败必须 fail-closed

# Review Gate
- 八类每一类都有独立来源小节、证据矩阵和边界说明
- 每个新增 source key 能回指来源与报告段落，交叉索引无悬空引用
- 统计/决策/运筹/设计/元认知缺口得到可机检覆盖，既有 163/14 基线保留
- 条目不自带权限、不把 experimental 写成有效性证明

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
- [ ] TP-01.07: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [ ] TP-01.08: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [ ] TP-02: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [ ] TP-03: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [ ] TP-04: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据

# Ship Readiness
- Reference Library validator 与 self-test PASS
- architecture、behavior、contract、test gates PASS
- 治理 strict/health/principle、task docs、review、reuse 和 verification PASS
- 回滚路径、未验证项和文档同步状态齐全

# Task Package Acceptance
## TP-01
- 标题: 八类功能分别深度抓取证据
- 验收标准:
  - 八类研究均独立记录
  - Schoenfeld/Pólya/Newell-Simon 与母领域来源关系清楚
- Verify: 检查研究报告是否有八个独立小节、来源矩阵、事实/推断/未知分层
- Gate: 每类核心候选至少有可追溯权威来源和明确停止条件
- 输出物: research/HEURISTIC_METACOGNITIVE_RESEARCH.md

### TP-01.01
- 标题: Representation 表征研究
- 验收标准:
  - 记录表征改变如何缩小或重构问题空间
- Verify: 核对验收项: 记录表征改变如何缩小或重构问题空间
- Gate: 父步骤范围已确认: research-evidence
- 输出物: research/HEURISTIC_METACOGNITIVE_RESEARCH.md

### TP-01.02
- 标题: Decomposition 分解研究
- 验收标准:
  - 记录子问题边界、依赖和合并证据
- Verify: 核对验收项: 记录子问题边界、依赖和合并证据
- Gate: 父步骤范围已确认: research-evidence
- 输出物: research/HEURISTIC_METACOGNITIVE_RESEARCH.md

### TP-01.03
- 标题: Transformation 变换研究
- 验收标准:
  - 记录变换保持什么、损失什么和如何回译
- Verify: 核对验收项: 记录变换保持什么、损失什么和如何回译
- Gate: 父步骤范围已确认: research-evidence
- 输出物: research/HEURISTIC_METACOGNITIVE_RESEARCH.md

### TP-01.04
- 标题: Search 搜索研究
- 验收标准:
  - 记录搜索预算、剪枝条件和回退路径
- Verify: 核对验收项: 记录搜索预算、剪枝条件和回退路径
- Gate: 父步骤范围已确认: research-evidence
- 输出物: research/HEURISTIC_METACOGNITIVE_RESEARCH.md

### TP-01.05
- 标题: Construction 构造研究
- 验收标准:
  - 记录候选产物、可运行见证和失败处理
- Verify: 核对验收项: 记录候选产物、可运行见证和失败处理
- Gate: 父步骤范围已确认: research-evidence
- 输出物: research/HEURISTIC_METACOGNITIVE_RESEARCH.md

### TP-01.06
- 标题: Verification/Falsification 验证证伪研究
- 验收标准:
  - 区分证明、证伪、验证、确认和 inconclusive
- Verify: 核对验收项: 区分证明、证伪、验证、确认和 inconclusive
- Gate: 父步骤范围已确认: research-evidence
- 输出物: research/HEURISTIC_METACOGNITIVE_RESEARCH.md

### TP-01.07
- 标题: Diagnosis/Revision 诊断修正研究
- 验收标准:
  - 记录最小失败案例、首个失效点和回归证据
- Verify: 核对验收项: 记录最小失败案例、首个失效点和回归证据
- Gate: 父步骤范围已确认: research-evidence
- 输出物: research/HEURISTIC_METACOGNITIVE_RESEARCH.md

### TP-01.08
- 标题: Control/Metacognition 控制元认知研究
- 验收标准:
  - 记录何时继续、停止、换路和升级人工
- Verify: 核对验收项: 记录何时继续、停止、换路和升级人工
- Gate: 父步骤范围已确认: research-evidence
- 输出物: research/HEURISTIC_METACOGNITIVE_RESEARCH.md

## TP-02
- 标题: 提炼母领域算子与双轴分类
- 验收标准:
  - 缺口母领域有可机检 source 覆盖
  - 每个新增条目可追溯并保持 experimental
- Verify: 检查新增条目的 kind、语义、来源、主类/辅助类、治理 owner、失败和恢复
- Gate: 新增方法不把母领域事实写成权限，不引入重复或无法验证的空壳条目
- 输出物: operators/packs/；operators/taxonomy/；operators/source-inventory.json

## TP-03
- 标题: 入库并同步交叉索引与文档
- 验收标准:
  - 新 pack 已登记且计数一致
  - 八类 crosswalk 覆盖全部当前参考条目
- Verify: 运行 JSON/引用/计数检查并核对文档规模、双轴边界和未验证项
- Gate: catalog、inventory、packs、taxonomy 与文档没有漂移或悬空引用
- 输出物: operators/catalog.json；operators/source-inventory.json；operators/taxonomy/；docs/；governance/

## TP-04
- 标题: 验证、审查与交付收口
- 验收标准:
  - 所有 required gate 有新鲜 PASS 证据
  - 未验证范围、回滚路径和文档同步状态清楚
- Verify: 运行 operator self-test、项目 gates、治理 strict/health/principle 和 task closeout validators
- Gate: required gate 绑定当前输入、策略和真实产物；失败必须 fail-closed
- 输出物: governance/tasks/0011-deepen-heuristic-metacognitive-operator-library/REVIEW.md；governance/tasks/0011-deepen-heuristic-metacognitive-operator-library/REUSE_SAMPLING.json

# Anti-Goals
- 不得修改 `governance/tasks/` 以外路径
- 不得虚构证据
- 不得越权补全未确认信息
