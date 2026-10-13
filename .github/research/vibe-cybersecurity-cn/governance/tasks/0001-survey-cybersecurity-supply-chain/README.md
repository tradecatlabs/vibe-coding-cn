# Task Overview

- Task ID: `0001`
- Slug: `survey-cybersecurity-supply-chain`
- Objective: 调研可被授权安全 Agent 编排的开源网络安全供应链、资料、工具与评测基线，并形成可验证候选表。
- Status: `Done`
- Survey snapshot: `2026-08-13`

## In Scope

- 安全 Agent/harness、扫描执行与漏洞运营平台。
- 资产发现、网络/Web 验证、源码、云、IaC、SCA 和供应链工具。
- 漏洞情报、机器标准、本地靶场与 Agent benchmark。
- 官方来源、许可证初筛、机器接口、网络副作用、证据上限、隔离与供应链门禁。

## Out of Scope

- 下载、安装或执行候选工具。
- 扫描任何公网、自有或第三方目标。
- 生产工具选型批准、法律意见或完整许可证合规结论。
- 声称候选已经通过本地能力、误报率、性能或越权负例验证。

## Task Package Tree

- TP-01：冻结术语、检索范围、证据层级、评分和停止条件。
- TP-02：检索官方仓库、文档、标准、事故和评测，建立来源账本。
- TP-03：建立机器候选目录、生成候选表并做综合选型。
- TP-04：执行结构、来源、风险与治理校验，形成审查结论。

## Requirement Alignment

用户要求深度调研开源网络安全供应链、资料、工具并制作候选表。本任务完成了跨八类的第一轮系统检索，形成 `46` 个代表性候选及首批 MVP/pilot/reference/hold 状态。这里的“候选”是研究优先级，不是默认可执行清单。

## Evidence Assets

- [CANDIDATE_TABLE.md](CANDIDATE_TABLE.md)：自动生成的人类可读候选表。
- [supply-chain-candidates.json](supply-chain-candidates.json)：机器真相源。
- [SEARCH_PROTOCOL.md](SEARCH_PROTOCOL.md)：检索、评分、风险与停止条件。
- [SOURCE_LEDGER.md](SOURCE_LEDGER.md)：官方来源和证据边界。
- [SYNTHESIS.md](SYNTHESIS.md)：目标架构、首批组合和效率分析。
- [REVIEW.md](REVIEW.md)：当前 WARN、未知项和完成门禁。
- [REUSE_SAMPLING.json](REUSE_SAMPLING.json)：为何不重复创建全局 SOP。
- [RETROSPECTIVE_REQUIREMENT.json](RETROSPECTIVE_REQUIREMENT.json)：已派生的中风险复盘要求；全局 handoff 因 owner registry 陈旧证据暂未签发，见 `REVIEW.md`。

## Task Package Overview

| ID | Parent | Depth | Priority | Type | Leaf | Depends On | Ready | Objective |
|---|---|---:|---|---|---|---|---|---|
| TP-01 | ROOT | 1 | P1 | discovery-contract | Yes | - | No | 冻结检索与评估协议 |
| TP-02 | ROOT | 1 | P1 | evidence-search | Yes | TP-01 | No | 建立官方来源账本 |
| TP-03 | ROOT | 1 | P1 | catalog-synthesis | Yes | TP-02 | No | 形成机器候选表和架构结论 |
| TP-04 | ROOT | 1 | P1 | verification-review | Yes | TP-03 | No | 校验并审查首轮交付 |

## Reading Order

1. `SYNTHESIS.md`
2. `CANDIDATE_TABLE.md`
3. `SOURCE_LEDGER.md`
4. `SEARCH_PROTOCOL.md`
5. `REVIEW.md`
6. `STATUS.md`
