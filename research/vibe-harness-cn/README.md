# Vibe Harness CN

Vibe Harness CN 是治理其他 agent harness 的元 harness。它不替代各业务 agent
的运行时，而是为 harness 及其问题求解算子库提供统一的规范、登记、分发、策略、验证、评估、
证据与生命周期控制面。

项目采用以下工作定义：

```text
Agent = LLM + Harness

Harness = Instructions + Context/Memory + Operator Library
        + Tools + Permissions + Loop/State
        + Validation + Observability + Environment Controls
```

这里的 `+` 表示组合，不表示模型与 harness 可以独立决定运行结果。更精确地说，
一次 agent 运行的行为是 `model × harness × task × environment × external state` 的函数；
元 harness 主要治理其中可工程化、可版本化、可验证的 harness 部分。

## 当前交付

- [`docs/HARNESS_MODEL.md`](docs/HARNESS_MODEL.md)：领域研究、边界和目标架构。
- [`docs/PROBLEM_SOLVING_OPERATOR_ARCHITECTURE_PRD.md`](docs/PROBLEM_SOLVING_OPERATOR_ARCHITECTURE_PRD.md)：
  Harness 内 AI 问题求解算子库的需求、边界、核心对象、验收与路线图。
- [`docs/OPERATOR_SPEC.md`](docs/OPERATOR_SPEC.md)：结构严格、内容宽松的 Core Contract、扩展规则与可选 Profile。
- [`research/UPSTREAMS.md`](research/UPSTREAMS.md)：15 个官方 GitHub 仓库的可研究范围与限制。
- [`research/HARNESS_RESEARCH.md`](research/HARNESS_RESEARCH.md)：11 个新增 Harness 的 revision 绑定源码研究档案。
- [`research/EXPANDED_OPERATOR_RESEARCH.md`](research/EXPANDED_OPERATOR_RESEARCH.md)：数学、物理、化学及多学科算子抽取的证据矩阵。
- [`research/HEURISTIC_METACOGNITIVE_RESEARCH.md`](research/HEURISTIC_METACOGNITIVE_RESEARCH.md)：按八类功能和母领域双轴深挖问题求解方法论。
- [`research/DOMAIN_EVIDENCE_MATRIX.md`](research/DOMAIN_EVIDENCE_MATRIX.md)：三十六个新增母领域的证据、迁移边界与停止理由矩阵。
- [`research/MATHEMATICAL_PROBLEM_SOLVING_RESEARCH.md`](research/MATHEMATICAL_PROBLEM_SOLVING_RESEARCH.md)：55 个数学问题求解方法的逐项去重、证据与算子 crosswalk。
- [`research/upstreams.sources.json`](research/upstreams.sources.json)：同步与 lock 共同消费的官方来源登记。
- [`research/upstreams.lock.json`](research/upstreams.lock.json)：官方 GitHub Harness 的精确 revision 清单。
- [`contracts/harness-manifest.schema.json`](contracts/harness-manifest.schema.json)：
  harness 登记契约的 JSON Schema。
- [`contracts/problem-solving-operator-pack.schema.json`](contracts/problem-solving-operator-pack.schema.json)：
  思维模型、原子算子和组合方法的宽松 Core JSON Schema。
- [`contracts/operator-runtime.schema.json`](contracts/operator-runtime.schema.json)：
  `OperatorBinding`、`OperatorRunRequest` 与 `OperatorRunRecord` 的宽松互操作信封。
- [`operators/`](operators/)：411 个跨学科原始方法条目和 57 个派生组合方法组成的本地参考库；分类视图见 [`operators/taxonomy/`](operators/taxonomy/)。
- [`examples/reference_harness/`](examples/reference_harness/)：确定性、无模型、无工具副作用的
  `Select → Bind → Materialize → Verify → Trace` 协议证明。
- [`contracts/examples/minimal-coding-harness.json`](contracts/examples/minimal-coding-harness.json)：
  最小有效样例。
- [`contracts/examples/minimal-operator-pack.json`](contracts/examples/minimal-operator-pack.json)：
  自定义领域与渐进式内容的最小 Core Pack 样例。
- [`scripts/validate_harness.py`](scripts/validate_harness.py)：可重跑的契约与策略校验入口。
- [`scripts/verify_project.py`](scripts/verify_project.py)：执行项目 Verification Policy 的确定性门禁。
- [`governance/`](governance/)：项目操作模型、ADR、Gate、任务证据和治理记忆。

## 验证

```bash
bash scripts/sync_upstreams.sh
uv run --locked --script scripts/validate_harness.py --self-test
uv run --locked --script scripts/validate_harness.py --operator-pack contracts/examples/minimal-operator-pack.json
uv run --locked --script scripts/validate_harness.py --operator-library operators/catalog.json
uv run --locked --script scripts/validate_harness.py --operator-runtime \
  contracts/examples/minimal-operator-binding.json \
  contracts/examples/minimal-operator-run-request.json \
  contracts/examples/minimal-operator-run-record.json
python3 -m unittest tests.test_reference_operator_harness
python3 examples/reference_harness/reference_harness.py
python3 scripts/verify_project.py --gate architecture
python3 governance/tools/rebuild_governance_index.py --project-root .
python3 governance/tools/validate_governance_package.py --project-root . --strict
python3 governance/tools/governance_health_report.py --project-root . --strict
```

`--self-test` 同时验证正例必须通过、负例必须被拒绝。任何意外结果都以非零状态退出。
项目 Verification Policy 还要求 architecture、behavior、contract、rollback、security 和 test
六类 capability；这套本地门禁尚未等价于生产 eval 或独立审查。

## 当前边界

首版只建立控制面契约与静态参考库，不实现具体模型调用、任务调度、Web UI、数据库或多 agent
编排。15 个上游 checkout 是研究输入，不等于 15 个 runtime adapter；只有实际适配器暴露查询、
并发、持久化或分发需求后，才用证据决定是否引入服务运行时和存储。PSOA 当前已交付
宽松 Core Pack Schema、`vibe-harness-cn/reference-library-v1` Profile、411/411 完整性清单、
本地参考库、Runtime Core 信封和一个无副作用参考 Harness。参考实现已经证明确定性 selector、本地
Binding、三种算子物化、独立摘要复验和脱敏 trace 可串成闭环；它不是生产 runtime，也不证明算子
有效。尚未交付第二个独立 Harness Binding、真实 LLM/tool execution、双 Harness 互操作 proof 或生产 eval。
