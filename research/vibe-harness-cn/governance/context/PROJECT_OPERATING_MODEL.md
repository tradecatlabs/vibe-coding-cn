---
id: GOV-PROJECT-OPERATING-MODEL
type: context
status: current
owner: engineering
created: 2026-08-13
last_reviewed: 2026-09-04
review_cycle: P90D
---

# Project Operating Model

本文件是项目级人类入口和代理入口的共享操作模型。它只记录项目当前应该如何被理解、修改、验证和交付；不替代代码、契约、ADR、任务包、README 或 AGENTS。

## 项目一句话定义

Vibe Harness CN 是治理其他 agent harness 的元 harness：统一其声明，以及 Harness 内问题求解
算子库的规范、目录、分发、策略、准入、评估、证据和生命周期，但不接管业务运行时状态。

## 业务模型

- 核心用户：harness 平台工程师、agent 开发者、评估/安全/运维负责人。
- 核心对象：版本化 Harness manifest、共享 Operator/Method 规范、Harness 本地库存摘要与 Binding、
  策略、conformance 结果、eval、trace/evidence 与生命周期状态。
- 关键流程：登记 manifest/operator -> 策略/契约校验 -> 分发到 Harness 本地库 -> Binding/conformance
  -> eval -> 审查与晋升 -> 观测、暂停或回滚。
- 不属于本项目的范围：替代具体 agent runtime、保存业务任务状态、统一实现所有工具、直接持有生产凭据。

## 技术模型

- 主要运行形态：当前为契约优先的离线控制面；在线 registry/API 必须由真实规模需求触发。
- 核心模块：`research/` 固定上游输入、`docs/` 维护领域模型、`contracts/` 声明契约、`operators/`
  保存静态参考内容、`examples/` 提供非生产协议消费证明、`scripts/` 提供薄验证入口、`governance/` 管理项目工程记忆。
- 数据事实源：manifest 与 Operator Pack Core Schema 位于 `contracts/`；Core/可选 Profile 规范位于
  `docs/OPERATOR_SPEC.md`；411 项跨学科完整清单位于 `operators/source-inventory.json`，双轴分类位于 `operators/taxonomy/`；Runtime Core 位于 `contracts/operator-runtime.schema.json`，运行事实由具体 Harness 按该信封上报。
- 外部依赖：验证脚本通过 `uv` 使用锁定版本 `jsonschema`；未来协议优先复用 MCP 与 OpenTelemetry。
- 主要验证入口：`uv run --locked --script scripts/validate_harness.py --self-test`。
- 上游同步入口：`bash scripts/sync_upstreams.sh`；checkout 仅是被忽略的研究缓存。
- 项目验证策略：`governance/control-plane/verification-policy.v1.yaml` 与 capability registry；
  `scripts/verify_project.py` 只执行已登记命令并生成任务证据。

## 工具链模型

工具链边界以 `context/TOOLCHAIN_MODEL.md` 为准。这里仅记录最短摘要：

- 构建：当前无构建产物。
- 测试：`uv run --locked --script scripts/validate_harness.py --self-test`。
- 类型检查：当前脚本规模无需单独类型检查器；以 Python 编译检查和行为自测为门禁。
- 格式 / lint：JSON 使用 `python3 -m json.tool`；Markdown 由治理 strict validator 检查结构与链接。
- 发布 / 回滚：当前未接入发布；契约回滚为恢复上一受支持 `api_version`/revision。

## 目录和真相源地图

| 事实类型 | 真相源 | 备注 |
|---|---|---|
| 项目操作模型 | `governance/context/PROJECT_OPERATING_MODEL.md` | 人类和代理的项目入口 |
| 上下文路由 | `governance/context/CONTEXT-ROUTER.md` | 任务类型到最小上下文包 |
| 工程流程 | `governance/processes/DOCUMENT_DRIVEN_DEVELOPMENT.md` | 文档先行和文档回填规则 |
| 工具链边界 | `governance/context/TOOLCHAIN_MODEL.md` | 成熟工具、项目脚本和禁用做法 |
| 机器契约 | `governance/context/project_operating_model_contract.v1.yaml` | 脚本和 agent 可读取的契约 |
| 架构决策 | `governance/decisions/adr/` | 不可逆或高影响决策 |
| 任务证据 | `governance/tasks/` | 执行计划、状态、验收、closeout |
| Harness 领域模型 | `docs/HARNESS_MODEL.md` | 稳定概念、边界、proof point 与 falsifier |
| PSOA 需求基线 | `docs/PROBLEM_SOLVING_OPERATOR_ARCHITECTURE_PRD.md` | Harness 内 Operator Library、共享规范、本地 Binding、证据与演进路线 |
| 官方 Harness 上游登记 | `research/upstreams.sources.json` | 允许同步的 URL、分支、许可证、公开路径与限制 |
| 官方 Harness 上游 revision | `research/upstreams.lock.json` | URL、commit、许可证、公开范围和研究限制 |
| 上游研究边界 | `research/UPSTREAMS.md` | 人类可读的证据范围与禁止推断事项 |
| 数学问题求解研究 | `research/MATHEMATICAL_PROBLEM_SOLVING_RESEARCH.md` | 用户点名 55 项方法的证据、去重与算子 crosswalk |
| Harness manifest 契约 | `contracts/harness-manifest.schema.json` | 字段与结构的机器真相源 |
| Operator 规范 | `docs/OPERATOR_SPEC.md` | Core Contract、Profile、扩展和安全分层 |
| Operator Pack 契约 | `contracts/problem-solving-operator-pack.schema.json` | 思维模型、原子算子与组合方法的宽松 Core 结构真相源 |
| Operator Runtime 契约 | `contracts/operator-runtime.schema.json` | Binding、RunRequest 与 RunRecord 的宽松互操作信封 |
| Operator 来源清单 | `operators/source-inventory.json` | 当前跨学科 411 项的独立完整性基线 |
| Operator 参考库 | `operators/catalog.json` 与 `operators/packs/` | Reference Profile；411 个 source + 57 个 derived 条目 |
| Operator 双轴分类 | `operators/taxonomy/problem-solving-methodology.json` | 母领域出处与八类功能的审计映射 |
| Harness 与 Operator 本地准入 | `scripts/validate_harness.py` | Schema、策略、完整覆盖与跨文件引用检查 |
| Operator Runtime 参考消费方 | `examples/reference_harness/` | 无副作用 Select/Bind/Materialize/Verify/Trace 协议证明 |
| 项目验证策略 | `governance/control-plane/verification-policy.v1.yaml` | 风险 profile 与 fail-closed 模式 |
| 项目验证能力 | `governance/control-plane/verification-capabilities.v1.yaml` | 真实命令、owner、timeout 与 artifact |
| 项目验证运行产物 | `governance/runtime/verification-artifacts/` | 可重建且被忽略，不绑定任何历史任务 |

## 变更入口

非平凡工程变更开始前必须判断：

- 是否需要先更新本操作模型。
- 是否需要更新文档驱动开发流程。
- 是否需要更新工具链模型。
- 是否需要新增或更新 ADR、Gate、module context、contracts、catalog、README 或 AGENTS。

## 验证入口

```bash
python3 governance/tools/governance_context_bundle.py --project-root . --task-type docs
python3 governance/tools/validate_governance_package.py --project-root . --strict
python3 governance/tools/governance_health_report.py --project-root . --strict
```

## 最近一次 review

- 日期：2026-09-04
- 结论：Operator Library 是 Harness 的内部能力组件；公共 Pack/Runtime Core 只约束稳定信封与安全 owner，
  `vibe-harness-cn/reference-library-v1` Profile 精确覆盖 411 个原始条目和 57 个派生 Method；一个
  无副作用参考 Harness 已证明本地 Selector/Binding/物化/验证/Trace，元 Harness 未创建外部统一 Runtime。
- 后续动作：由第二个独立 Harness 使用不同 Binding 跑同一 conformance corpus，再补真实
  Observation/Evidence 和生产 eval。
