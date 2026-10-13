# Task-Level Acceptance
- 研究报告包含来源、证据、提炼规则、局限和未验证项
- 数学/物理/化学优先条目与其他点名领域均有可机检覆盖
- inventory、catalog、packs 的 source key、计数、ID、引用和治理不变量精确一致
- 既有 75 个 source 与 7 个 derived 的兼容性保持，Core/Profile 分层不被削弱
- approved plan 已成功编译为递归任务树
- 叶子节点数量: 4
- 当前可立即执行叶子节点: TP-01

# Validation Plan
- 运行 uv run --locked --script scripts/validate_harness.py --operator-library operators/catalog.json
- 运行 uv run --locked --script scripts/validate_harness.py --self-test
- 运行 python3 scripts/verify_project.py --gate architecture|behavior|contract|test
- 运行治理 strict、health、principle、任务文档和任务级 verification 校验
- TP-01 | Verify: 检查研究报告、来源台账、候选清单、局限和未验证项 | Gate: 每个核心候选都有可追溯权威来源，事实、推断和未知分开
- TP-02 | Verify: 检查每个 entry 的类型、语义字段、治理 owner、source_refs 和状态 | Gate: 新增算子不越过 Core/Profile、安全 owner 和 reference-only 边界
- TP-03 | Verify: 运行 JSON 结构检查与 Reference Profile 校验，并核对文档中的规模与边界 | Gate: inventory/catalog/packs 精确一致，文档没有遗留 75+7 的过期事实
- TP-04 | Verify: 运行 operator self-test、project gates、governance strict/health/principle 和任务 docs validator | Gate: 所有 required gate 绑定当前输入、策略和真实产物；失败项明确记录

# Review Gate
- 每个新增 source key 都能回指研究报告与权威来源
- 新旧 domain、pack、catalog、inventory 计数精确一致
- 物理/化学方法没有自授权或隐含现实副作用
- 不得以条目数量冒充真实效果，experimental 与未知项保持可见

# Runtime Verification Gate
- [ ] 每个 tool/action 结果都有可回指证据或明确未执行原因。
- [ ] 高风险动作没有由 worker/agent 自我批准；审批状态可追踪。
- [ ] compaction / resume 后目标、计划、修改文件、审批状态和验证项未丢失。
- [ ] verifier / 自审已检查关键发现是否有证据支持。
- [ ] closeout 明确 coverage gaps、failed packets 和 unresolved questions。
- [ ] TP-01: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [ ] TP-02: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [ ] TP-03: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据
- [ ] TP-04: 输出格式 `按 outputs/acceptance 汇报`；证据要求：默认可复核证据

# Ship Readiness
- Reference Library 校验和 self-test PASS
- architecture、behavior、contract、test gates PASS
- 治理 strict/health/principle 与任务 docs 校验 PASS
- REUSE_SAMPLING、review、verification 和回滚说明齐全

# Task Package Acceptance
## TP-01
- 标题: 建立跨学科证据矩阵
- 验收标准:
  - 数学/物理/化学优先证据完整
  - 点名其他领域均有覆盖计划与来源
- Verify: 检查研究报告、来源台账、候选清单、局限和未验证项
- Gate: 每个核心候选都有可追溯权威来源，事实、推断和未知分开
- 输出物: research/EXPANDED_OPERATOR_RESEARCH.md；operators/source-inventory.json

## TP-02
- 标题: 定义算子语义与领域边界
- 验收标准:
  - 优先领域算子可被 Harness 选择但不自带权限
  - 重复或无法执行的候选被拒绝
- Verify: 检查每个 entry 的类型、语义字段、治理 owner、source_refs 和状态
- Gate: 新增算子不越过 Core/Profile、安全 owner 和 reference-only 边界
- 输出物: operators/packs/*.json

## TP-03
- 标题: 入库并同步目录文档
- 验收标准:
  - 新 domain 已登记且计数一致
  - 旧条目和既有引用无回归
- Verify: 运行 JSON 结构检查与 Reference Profile 校验，并核对文档中的规模与边界
- Gate: inventory/catalog/packs 精确一致，文档没有遗留 75+7 的过期事实
- 输出物: operators/catalog.json；operators/packs/；docs/；governance/

## TP-04
- 标题: 验证、审查与交付收口
- 验收标准:
  - 验证结果 PASS 或对真实 blocker fail-closed
  - 回滚路径和未验证项清楚可见
- Verify: 运行 operator self-test、project gates、governance strict/health/principle 和任务 docs validator
- Gate: 所有 required gate 绑定当前输入、策略和真实产物；失败项明确记录
- 输出物: governance/tasks/0010-expand-multidomain-operator-library/REVIEW.md；governance/tasks/0010-expand-multidomain-operator-library/REUSE_SAMPLING.json

# Anti-Goals
- 不得修改 `research/upstreams.sources.json`、`research/upstreams.lock.json`、上游 checkout 或运行时状态
- 不得虚构证据、把静态研究写成真实效果验证
- 不得越权补全未确认的学科结论、实验授权或外部能力
