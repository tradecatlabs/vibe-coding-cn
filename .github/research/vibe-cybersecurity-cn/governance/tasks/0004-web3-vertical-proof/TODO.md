# Execution Checklist

[x] TP-01 | P1 | Web3/EVM 供应链聚焦调研 | Verify: validate_web3_candidates.py + WEB3_CANDIDATE_TABLE.md | Gate: 候选不等于已安装 | Parallelizable: No
[x] TP-02 | P1 | 本地工具链安装与固定版本 | Verify: forge/slither/echidna/solc 版本输出 | Gate: 官方来源与固定版本 | Parallelizable: No
[x] TP-03 | P1 | 本地已知漏洞靶场 | Verify: ground-truth.json + forge build | Gate: 教学 ground truth 明确 | Parallelizable: No
[x] TP-04 | P1 | 候选-验证-证据闭环 | Verify: forge test 4/4 + validate_lab_evidence.py | Gate: confirmed 仅来自独立复现 | Parallelizable: No
[x] TP-05 | P1 | 治理同步与 closeout | Verify: task docs + governance strict/health | Gate: 无占位、死链或过度声明 | Parallelizable: No
