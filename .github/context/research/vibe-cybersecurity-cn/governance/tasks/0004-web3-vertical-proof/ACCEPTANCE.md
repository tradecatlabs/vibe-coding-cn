# Task-Level Acceptance

- Web3/EVM 供应链候选表（20 项）通过校验器并生成可读表。
- 工具链固定版本并记录来源；所有执行限定本地。
- 本地靶场覆盖不少于 3 类已知漏洞，ground truth 与证据账本一致。
- 纵向闭环成立：Foundry 攻击测试 4/4 复现，Slither/Echidna 作为候选通道。
- 静态候选与实证漏洞严格分离：`confirmed` 只表示本地攻击测试复现成功。
- 没有公网扫描、未授权利用或生产可用声明。

# Validation Plan

```bash
python3 governance/tasks/0004-web3-vertical-proof/validate_web3_candidates.py
python3 web3-lab/validate_lab_evidence.py
cd web3-lab && forge test -vv
python3 <CODEX_SKILLS>/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0004-web3-vertical-proof --phase closeout
python3 governance/tools/rebuild_governance_index.py --project-root .
python3 governance/tools/validate_governance_package.py --project-root . --strict
python3 governance/tools/governance_health_report.py --project-root . --strict
```

# Review Gate

- `PASS`：工具版本真实、授权边界未越、候选-实证分离、证据 artifact 存在、索引同步。
- `WARN`：工具召回率只代表本地靶场基线，外推真实协议需重新测量。
- `BLOCK`：静态候选被标记为实证、靶场用于真实协议、或任何校验器失败。

# Runtime Verification Gate

本任务只在本地链与本地合约上运行（`forge test`、Slither、Echidna），
运行时验证为 `local-lab-only`。它不能证明任何生产扫描器效果。

# Ship Readiness

只交付本地文档、靶场与证据；不提交、不推送、不部署、不安装到生产。

# Task Package Acceptance

- TP-01：20 项候选，分类覆盖静态分析、模糊测试、形式化、靶场、漏洞库、工具链。
- TP-02：Foundry/Slither/Echidna/solc 版本与来源记录。
- TP-03：4 类漏洞合约 + ground truth manifest。
- TP-04：攻击测试 4/4 + 静态候选对照 + 证据账本校验通过。
- TP-05：closeout 与治理 strict/health 新鲜通过。

# Anti-Goals

- 不修改 0001/0002/0003 机器真相源。
- 不虚构工具版本、运行结果或验证结论。
- 不把靶场漏洞结论用于真实协议审计。
- 不进行供应链正式准入或生产部署。
