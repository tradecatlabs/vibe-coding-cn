# Vibe Harness CN 架构说明

本项目是 harness 的治理控制面。根目录只承载入口、跨模块规则和长期架构映射；
业务 harness 的执行状态不应写入本仓库作为运行真相。

## 目录树

```text
.
├── .gitignore                        # 忽略 Python 缓存与任务运行期证据
├── README.md                         # 人类入口、当前能力与验证命令
├── AGENTS.md                         # 目录职责、依赖方向与维护约束
├── contracts/                        # 机器可读的 harness 登记契约和样例
│   ├── AGENTS.md
│   ├── harness-manifest.schema.json
│   ├── operator-runtime.schema.json
│   ├── problem-solving-operator-pack.schema.json
│   └── examples/
│       ├── minimal-coding-harness.json
│       ├── minimal-operator-pack.json
│       ├── minimal-operator-binding.json
│       ├── minimal-operator-run-request.json
│       └── minimal-operator-run-record.json
├── examples/                         # 非生产协议消费方与可运行证明
│   ├── AGENTS.md
│   └── reference_harness/            # 无副作用 Operator Runtime 参考闭环
├── operators/                        # Harness 可装载的静态问题求解内容库
│   ├── AGENTS.md
│   ├── README.md
│   ├── catalog.json
│   ├── source-inventory.json
│   ├── taxonomy/                     # 母领域来源与八类功能的双轴分类视图
│   └── packs/                        # 411 个 source + 57 个 derived 条目，五十六个领域 pack
├── docs/                             # 领域模型、组件需求与目标架构
│   ├── AGENTS.md
│   ├── HARNESS_MODEL.md
│   ├── OPERATOR_SPEC.md
│   └── PROBLEM_SOLVING_OPERATOR_ARCHITECTURE_PRD.md
├── research/                         # 官方上游来源、revision lock 与问题求解方法研究
│   ├── AGENTS.md
│   ├── UPSTREAMS.md
│   ├── upstreams.sources.json          # 官方 origin、分支、许可证与研究路径登记
│   ├── upstreams.lock.json
│   └── upstreams/                    # gitignored：15 个受治理官方 Harness checkout
├── scripts/                          # 薄验证入口，只连接成熟工具与项目策略
│   ├── AGENTS.md
│   ├── sync_upstreams.sh
│   ├── validate_harness.py
│   ├── validate_operator_library.py
│   ├── validate_harness.py.lock      # uv 脚本依赖闭包与 artifact hash
│   └── verify_project.py             # 项目 Verification Policy 的确定性 gate runner
├── tests/                            # 反例与回归输入
│   ├── AGENTS.md
│   ├── __init__.py
│   ├── test_reference_operator_harness.py
│   ├── test_sync_upstreams.sh
│   ├── test_verify_project.py
│   └── fixtures/                     # Harness 与 Runtime 负例
└── governance/                       # 项目工程记忆、ADR、Gate 和任务证据
    └── control-plane/                # 项目验证策略与 capability registry
```

## 依赖方向

```text
研究 ──输入──> docs 与 ADR ──定义──> contracts
PSOA PRD ──约束──> operator/method contracts、Harness libraries 与未来 bindings
source-inventory.json ──完整性基线──> operators/packs/*.json
contracts ──约束──> operators ──被校验──> scripts/validate_operator_library.py
research/upstreams.sources.json ──驱动──> scripts/sync_upstreams.sh
GitHub 上游 ──同步/锁定──> research/upstreams.lock.json
contracts ──被消费──> scripts/validate_harness.py
contracts + operators ──被消费──> examples/reference_harness
examples/reference_harness ──行为证明──> tests/test_reference_operator_harness.py
tests/fixtures ──验证拒绝能力──> scripts/validate_harness.py
governance ──约束──> 全部项目变更
```

- `contracts/` 是 Harness manifest、Operator Pack 与 Operator Runtime Core 结构的单一真相源；Core 只约束互操作字段和安全边界。
- `operators/` 是当前 Reference Library Profile、参考内容和精确来源清单的单一真相源，不拥有运行态选择、权限或结果。
- `docs/PROBLEM_SOLVING_OPERATOR_ARCHITECTURE_PRD.md` 是 PSOA 需求真相源；Operator Library 属于
  Harness，跨 Harness 的字段级规范仍独立落入 `contracts/`，manifest 只登记支持版本与库存摘要。
- `scripts/` 可以消费契约和测试输入，但不得反向定义领域语义。
- `examples/reference_harness/` 是具体 Harness 的本地协议证明，不拥有中央状态，也不代表生产适配器。
- `docs/` 解释“为什么”；`contracts/` 规定“必须长什么样”；`governance/` 记录
  “项目如何安全演进”。三者不得互相替代。
- 元 harness 控制面不得直接拥有受管 harness 的业务状态；运行态通过稳定适配器上报证据。

## 变更规则

- 新增 manifest 字段时，同步更新 Schema、有效样例、负例和领域文档。
- 破坏性契约变更必须升级 `api_version`，并记录 ADR 与迁移路径。
- 不得把密钥、完整 prompt、工具参数或工具结果写入样例、日志和验证输出。
- 新增服务、数据库、队列、插件系统或 UI 前，必须先有第二个真实消费方或测量证据。
- 创建、删除、移动文件或重划职责时，同步更新本文件及受影响目录的 `AGENTS.md`。

## 近期架构变更

- 2026-09-03：纠正 PSOA 边界；Operator Library 属于 Harness，元 Harness 只治理共享规范、目录、
  分发、评测与生命周期。
- 2026-09-03：扩展跨学科 Operator Library，精确覆盖 163 个原始条目，并新增 14 个显式派生
  Method；新增科学方法论、系统科学、信息论、复杂性科学、算法、物理学和化学 pack；selector、Binding 和运行时继续留在边界外。
- 2026-09-03：新增通用问题求解、统计、决策科学、运筹学、设计方法和工程学 pack，将库扩展为 196 个 source、20 个 derived；用 taxonomy 双轴分开母领域与八类功能。
- 2026-09-03：继续深挖因果推断、经济学/博弈论、生态/生物学、认知科学、人因可靠性和医学决策，新增 6 个 pack、30 个 source、6 个 derived；库扩展为 226 个 source、26 个 derived、252 个总条目，证据矩阵单独记录迁移边界。
- 2026-09-03：继续深挖法律推理、伦理与公共政策、教育与学习科学、语言学、历史推理和社会科学方法，新增 6 个 pack、30 个 source、6 个 derived；库扩展为 256 个 source、32 个 derived、288 个总条目，继续保持 experimental/reference-only 边界。
- 2026-09-03：继续深挖形式逻辑与自动推理、哲学与科学认识论、地球科学、天文学与天体物理、材料科学、信息与知识科学，新增 6 个 pack、30 个 source、6 个 derived；库扩展为 286 个 source、38 个 derived、324 个总条目，继续保持 experimental/reference-only 边界。
- 2026-09-03：继续深挖控制论、数值分析与科学计算、离散组合数学、热力学与统计物理、有机化学反应设计、分析化学与计量学，新增 6 个 pack、30 个 source、6 个 derived；库扩展为 316 个 source、44 个 derived、360 个总条目，继续保持 experimental/reference-only 边界。
- 2026-09-03：第五轮继续深挖随机过程、微分方程与动力系统、经典力学与变分方法、流体与连续介质、化学动力学、电化学与传质，新增 6 个 pack、30 个 source、6 个 derived；库扩展为 346 个 source、50 个 derived、396 个总条目，继续保持 experimental/reference-only 边界。
- 2026-09-04：第六轮继续深挖线性代数谱方法、拓扑几何、电磁场方法、量子算子方法、溶液热力学相平衡和光谱结构解析，新增 6 个 pack、30 个 source、6 个 derived；库扩展为 376 个 source、56 个 derived、432 个总条目，继续保持 experimental/reference-only 边界。
- 2026-09-04：专项深挖数学问题求解过程，对用户点名的 55 个方法逐项去重；复用 20 个既有语义，向 mathematics pack 补 35 个 source 和 1 个 derived，库扩展为 411 个 source、57 个 derived、468 个总条目，公共 Core 保持宽松。
- 2026-09-03：把 Operator Pack 拆成宽松 Core Contract 与可选 Conformance Profile；公共 Schema
  不再把七领域、内容字段或集合数量强加给所有 Harness。
- 2026-09-04：新增宽松 Operator Runtime Core 和无副作用参考 Harness，以确定性 `O(n)` 选择、
  本地 Binding、受预算物化、独立摘要复验和脱敏 provenance 证明运行协议；第二个独立 Harness
  与真实模型/工具执行仍留在后续互操作阶段。
