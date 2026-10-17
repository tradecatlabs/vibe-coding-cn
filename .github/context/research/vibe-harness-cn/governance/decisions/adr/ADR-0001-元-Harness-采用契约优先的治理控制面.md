---
id: ADR-0001
type: record
status: active
owner: engineering
created: 2026-08-14
last_reviewed: 2026-08-14
source: docs/HARNESS_MODEL.md
related_gates: [GATE-0000, GATE-0001]
---

# ADR-0001 元 Harness 采用契约优先的治理控制面

## 背景

项目需要治理多个异构 agent harness。直接先造统一运行时会把某个框架的执行模型固化为
全局边界，同时让控制面接管不该拥有的业务状态。只有文档又无法形成确定性准入。

## 决策或结论

采用契约优先的治理控制面：以供应商中立、版本化 Harness manifest 为声明真相源；
JSON Schema 与少量跨字段策略负责离线 conformance；具体 runtime 仍拥有任务执行和业务状态，
通过稳定适配器上报 trace/eval/evidence。首版不创建数据库、Web UI、队列、插件系统或统一 runtime。

目标终态：Registry、Policy、Conformance、Evaluation、Evidence、Lifecycle 六个正交控制面能力。

真实约束：权限和安全边界必须 fail closed；证据必须绑定 harness/model/policy/artifact revision；
不同 runtime 的业务状态不能被元 harness 直接接管。

惯性约束：当前目录为空，没有必须保留的旧 API、存量数据或外部集成。

Kill list：统一 agent runtime、首版数据库、首版 UI、多 agent 调度器、尚无第二实现的插件系统。

## 证据

- Proof point：有效 coding harness manifest 通过验证；缺停止条件和高风险工具免审批均被拒绝。
- Falsifier：第二类真实 harness 无法在不使用自由文本特例的前提下表达关键治理边界。
- 当前证据：`uv run --locked --script scripts/validate_harness.py --self-test`。
- 研究依据：`docs/HARNESS_MODEL.md` 中列出的一手资料与候选路径比较。

## 影响范围

- 新增 `contracts/`、`scripts/`、`tests/`、`docs/` 的职责边界和根 `AGENTS.md` 架构映射。
- 破坏性 manifest 变化必须升级 `api_version`；当前 `v1alpha1` 明确允许迭代。
- 回滚为恢复上一 Schema/manifest revision；没有数据迁移或在线服务副作用。

## 后续动作

- [ ] 接入第一个真实 runtime adapter，并记录字段覆盖与缺口。
- [ ] 接入第二类 runtime adapter 时执行 falsifier 审查，再决定是否引入适配器协议或 registry service。
