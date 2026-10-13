# Acceptance Checklist

## Global Standards

- [x] 未来终态、真实约束、惯性约束、proof point 和 falsifier 已记录。
- [x] 新增长期对象已通过存在性检查；靶场与证据是闭环必需，未引入运行时抽象。
- [x] 成熟工具优先（Foundry/Slither/Echidna），自研仅靶场与证据。
- [x] 网络副作用为零：仅官方安装源下载与本地运行。

## Task Package Checklists

### TP-01

- [x] Web3/EVM 候选 JSON 与校验器落盘，可读表生成。
- Verify: `validate_web3_candidates.py` 输出 PASS。
- Gate: 版本、许可证、来源均有记录；候选不等于已安装。

### TP-02

- [x] Foundry 1.7.1、Slither 0.11.6、Echidna 2.3.3、solc 0.8.35 固定。
- Verify: `forge --version`、`slither --version`、`echidna --version`。
- Gate: 工具只在本机用户目录/venv 运行，不污染系统。

### TP-03

- [x] 4 类已知漏洞合约与 ground truth manifest。
- Verify: `web3-lab/ground-truth.json` 存在且与证据账本 ID 一致。
- Gate: 靶场合约必须是有意植入漏洞的教学代码。

### TP-04

- [x] forge test 4/4 复现；Slither/Echidna 候选对照记录；证据账本校验 PASS。
- Verify: `validate_lab_evidence.py` 与 `forge test` 输出。
- Gate: `confirmed` 只来自独立攻击测试，静态候选不直接晋升。

### TP-05

- [x] 操作模型、工具链模型、拓扑、路由、README/AGENTS、任务索引同步。
- Verify: task docs closeout、governance strict/health 与 principle gate。
- Gate: 文档或状态在最终验证后改变必须重跑。
