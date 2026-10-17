# Task-Level Acceptance
- 最小合法 Core Pack 与显式 extensions 通过
- 未知稳定字段、错误字段类型和类型错配被拒绝
- Reference Library Profile 继续严格验证 75/75、7/7、引用、计数与安全边界
- 规范、Schema、CLI 和治理真相源对分层边界表述一致
- approved plan 已成功编译为递归任务树
- 叶子节点数量: 4
- 当前可立即执行叶子节点: TP-01

# Validation Plan
- 运行 Operator Pack Core Contract 正反例
- 运行 Reference Library canonical validation 与完整 self-test
- 运行项目 architecture、behavior、contract、test gates
- 运行 governance strict、health、principle 与任务文档校验
- bugfix / regression / flaky 任务必须把 DEBUG.md 的回归证据串到 Recent Evidence
- TP-01 | Verify: 检查规范覆盖 Core、Profile、extensions、兼容性和安全边界 | Gate: 任何字段强制项都能由互操作或安全必要性解释
- TP-02 | Verify: 运行 JSON Schema 自校验和既有 7 个 pack 校验 | Gate: 既有内容兼容，最小自定义领域 pack 可通过，未知稳定字段被拒绝
- TP-03 | Verify: 运行 --operator-pack、--operator-library 与 --self-test | Gate: Core 正例通过、结构负例拒绝、Reference 75+7 回归通过
- TP-04 | Verify: 运行 project gates、governance strict/health、task docs 与 Git 输入检查 | Gate: 没有文档漂移或未解释的长期约束

# Review Gate
- Core 不得强制七领域、固定内容字段或固定集合数量
- Profile 不能绕过路径、权限 owner、引用解析和完整性门禁
- 不把本地自审冒充独立 reviewer provenance

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
- 全部 required project gates 通过
- governance、task、reuse 和 clean HEAD verification 有新鲜证据

# Task Package Acceptance
## TP-01
- 标题: 定义宽松核心与 Profile 边界
- 验收标准:
  - Core 与 Reference Profile 职责不重叠
  - 安全边界有明确保留理由
- Verify: 检查规范覆盖 Core、Profile、extensions、兼容性和安全边界
- Gate: 任何字段强制项都能由互操作或安全必要性解释
- 输出物: docs/OPERATOR_SPEC.md；governance/decisions/adr/ADR-0004-问题求解算子采用宽松核心与可选加严-Profile.md

## TP-02
- 标题: 放宽 Schema 并标注参考库 Profile
- 验收标准:
  - 领域、描述和语义集合不再被公共 Schema 过度限制
  - extensions 是唯一开放扩展容器
- Verify: 运行 JSON Schema 自校验和既有 7 个 pack 校验
- Gate: 既有内容兼容，最小自定义领域 pack 可通过，未知稳定字段被拒绝
- 输出物: contracts/problem-solving-operator-pack.schema.json；operators/catalog.json

## TP-03
- 标题: 实现 Core 与 Reference 回归
- 验收标准:
  - 最小 pack 与 extensions 有正例
  - 错类型、未知字段、自授权、坏引用和路径逃逸仍失败
- Verify: 运行 --operator-pack、--operator-library 与 --self-test
- Gate: Core 正例通过、结构负例拒绝、Reference 75+7 回归通过
- 输出物: scripts/validate_harness.py；scripts/validate_operator_library.py

## TP-04
- 标题: 同步文档治理并完成验证
- 验收标准:
  - 项目入口、模块上下文、QA 和 ADR 一致
  - 最终证据绑定当前代码与策略
- Verify: 运行 project gates、governance strict/health、task docs 与 Git 输入检查
- Gate: 没有文档漂移或未解释的长期约束
- 输出物: README.md；AGENTS.md；docs/；governance/；governance/tasks/0009-define-permissive-operator-contract/

# Anti-Goals
- 不得修改 `governance/tasks/` 以外路径
- 不得虚构证据
- 不得越权补全未确认信息
