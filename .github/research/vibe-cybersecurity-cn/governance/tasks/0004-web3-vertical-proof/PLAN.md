# Planning Summary

目标终态是 Web3 授权审计的机器可审计闭环：合约源码进入后，
静态/动态工具产出候选，独立攻击测试验证，证据 JSON 归档，
只有验证通过的候选进入实证漏洞视图。本轮以本地靶场为 proof point。

# Lifecycle Gates

总生命周期为 `SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP`，任一 gate 不得跳过。

1. SPEC：任务意图、验收、授权边界（本地 ScopeGrant）明确。
2. PLAN：任务树、依赖、回滚、停止条件明确（本文件）。
3. BUILD：Web3 候选表、工具链固定、靶场、证据闭环落盘。
4. TEST：候选校验器、manifest/证据 schema、任务文档、治理 strict/health 通过。
5. REVIEW：专项自审检查版本真实性、授权边界、候选-实证分离、完成声明。
6. SHIP：只交付本地文档、脚本与证据；不安装到生产、不推送公网。

# Simplest Path

- 一个 Web3 候选 JSON + 校验器，复用 0001 的 schema 风格，不新建数据库。
- 工具链用官方安装器固定版本（foundryup / pip / GitHub release），记录版本与摘要。
- 靶场自写最小已知漏洞合约（4 个类别），不依赖大靶场仓库下载。
- 证据用单个 JSON 文件归档，schema 内嵌校验器，不引入 DB。
- 不实现生产编排器；本轮只证明"候选->验证->证据"链路可行。

# Split Strategy

- TP-01：Web3/EVM 供应链聚焦调研（候选 JSON + 校验器 + Markdown 表）。
- TP-02：本地工具链安装与固定版本（Foundry、Slither、Echidna、solc）。
- TP-03：本地已知漏洞靶场（合约 + ground truth manifest）。
- TP-04：纵向闭环演示（Slither 候选 -> Foundry/Echidna 验证 -> 证据 JSON）。
- TP-05：治理资产同步、strict/health 校验与 closeout。

# Execution Waves

```text
TP-01 -> TP-02 -> TP-03 -> TP-04 -> TP-05
```

# Runtime Workflow Contract

- Allowed：官方仓库只读检索、本地文件编辑、本地工具安装与运行、本地链测试。
- Forbidden：公网扫描、未授权目标动作、凭据访问、利用真实协议。
- Evidence：工具版本输出、命令日志、ground truth manifest、证据 JSON、治理校验结果。
- Stop：出现越权动作风险、工具供应链不可信（无固定版本/来源）、
  静态候选被直接标记为实证漏洞。

# Next Executable Leaves

无。本任务已完成；下一任务应实现真实授权协议 fork 级审计样例与
Echidna 属性基线扩展。

# Dependency Graph

```text
0001/0002/0003 调研基底
        |
        v
TP-01 Web3 聚焦调研 --> TP-02 工具链固定 --> TP-03 靶场 --> TP-04 闭环 --> TP-05 治理
```

# Rollback Protocol

- 删除 `governance/tasks/0004-web3-vertical-proof/` 与 `web3-lab/` 即可。
- 恢复 `INDEX.md` 当前任务行与操作模型/工具链模型变更。
- 无业务数据、外部资源或生产状态需要迁移。
