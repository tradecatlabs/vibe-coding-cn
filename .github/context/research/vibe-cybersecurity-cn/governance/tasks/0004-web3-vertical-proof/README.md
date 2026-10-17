# Task Overview

- Task ID: `0004`
- Slug: `web3-vertical-proof`
- Objective: Web3/区块链 EVM 垂直落地：聚焦供应链调研、本地隔离靶场与候选-验证-证据闭环。
- Status: `Done`

## In Scope

- 建立 Web3/EVM 聚焦供应链候选表（静态分析、模糊测试、形式化、靶场、漏洞库、工具链）。
- 固定本地工具链版本（Foundry、Slither、Echidna、solc）并记录来源。
- 构建本地已知漏洞靶场（重入、溢出、访问控制、预言机操纵）与 ground truth。
- 跑通 `候选 -> 独立复现 -> 证据归档` 纵向闭环并沉淀证据账本。
- 同步操作模型、工具链模型、拓扑、路由、README/AGENTS 与任务索引。

## Out of Scope

- 不扫描、不利用任何公网或未授权目标。
- 不把静态分析候选直接标成实证漏洞。
- 不进行供应链正式准入（admitted）或生产部署。
- 不覆盖非 EVM 链（Solana、Cosmos、Move 等）。

## Task Package Tree

```text
ROOT
├── TP-01 Web3/EVM 供应链聚焦调研
├── TP-02 本地工具链固定版本
├── TP-03 本地已知漏洞靶场
├── TP-04 候选-验证-证据纵向闭环
└── TP-05 治理同步、严格校验与 closeout
```

## Requirement Alignment

- 用户要求范围收敛到 Web3/区块链：本任务以 EVM/Solidity 为首个垂直切片。
- 项目要求"候选漏洞空间 -> 自动验证 -> 实证漏洞空间"：本任务用本地靶场证明该链路。
- 胶水原则：静态分析、模糊测试、本地链全部复用成熟工具，自研仅做靶场、编排与证据。

## Task Package Overview

| Node | Output | Acceptance |
|---|---|---|
| TP-01 | `web3-supply-chain-candidates.json`、`WEB3_CANDIDATE_TABLE.md` | 20 项候选通过校验器 |
| TP-02 | 工具版本与来源记录 | Foundry 1.7.1 / Slither 0.11.6 / Echidna 2.3.3 / solc 0.8.35 |
| TP-03 | `web3-lab/` 合约与 `ground-truth.json` | 4 类漏洞 manifest 齐备 |
| TP-04 | `web3-lab/evidence/` 证据账本 | forge test 4/4、`validate_lab_evidence.py` PASS |
| TP-05 | 治理资产与校验输出 | task docs closeout + governance strict/health |

## Reading Order

1. `web3-lab/README.md`
2. `WEB3_CANDIDATE_TABLE.md`
3. `web3-lab/evidence/findings-2026-08-14.json`
4. `CONTEXT.md`
5. `STATUS.md`
