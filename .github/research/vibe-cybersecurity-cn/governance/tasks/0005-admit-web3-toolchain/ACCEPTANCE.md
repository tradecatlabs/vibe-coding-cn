# Task-Level Acceptance

- 5 项 Web3 核心工具（Foundry、Slither、Echidna、solc、forge-std）完成
  8 门禁并标记 `admitted`，准入 JSON 通过校验器。
- forge-std 固定 v1.16.2，forge build/test 全部通过。
- Echidna 属性覆盖 4 个靶场漏洞；除记录为属性盲区外全部有反例或证明。
- Git 仓库初始化 + 初始提交完成；verification policy 转 enforce；
  `build_task_closeout.py` 的 closeout gate ready=true。
- 治理 strict/health 通过；无公网副作用。

# Validation Plan

```bash
python3 governance/tasks/0005-admit-web3-toolchain/validate_web3_admission.py
cd web3-lab && forge build && forge test
../../.tools/echidna test/ReentrancyEchidna.t.sol --contract ReentrancyEchidna --config echidna.yaml
../../.tools/echidna test/AccessControlEchidna.t.sol --contract AccessControlEchidna --config echidna.yaml
../../.tools/echidna test/PriceOracleEchidna.t.sol --contract PriceOracleEchidna --config echidna.yaml
python3 <CODEX_SKILLS>/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0005-admit-web3-toolchain --phase closeout
python3 <CODEX_SKILLS>/auto-tasks/scripts/build_task_closeout.py --task-dir governance/tasks/0005-admit-web3-toolchain --project-root . --reuse-sampling ... --verification-* ...
python3 governance/tools/validate_governance_package.py --project-root . --strict
python3 governance/tools/governance_health_report.py --project-root . --strict
```

# Review Gate

- `PASS`：8 门禁逐项有真实证据；forge-std 固定；属性基线有反例/盲区记录；
  closeout gate ready；索引同步。
- `WARN`：Echidna 某属性无法反例化时记录盲区并给出后续方案。
- `BLOCK`：门禁无证据、工具版本漂移、验证控制面强制门禁失败。

# Runtime Verification Gate

本任务在本地链与本地合约上运行；运行时验证为 `local-lab-only`。

# Ship Readiness

只交付本地文档、脚本与证据；不 push、不部署、不安装到生产。

# Task Package Acceptance

- TP-01：5 项工具全部 admitted，校验器 PASS。
- TP-02：forge-std v1.16.2，build/test PASS。
- TP-03：4 个属性合约，Echidna 反例/盲区记录齐全。
- TP-04：git 初始提交完成；enforce 策略；closeout gate ready=true。
- TP-05：治理 strict/health 与 closeout 新鲜通过。

# Anti-Goals

- 不 push 远端、不开 PR、不切换分支。
- 不伪造门禁证据；每项 admitted 绑定真实命令输出。
- 不把属性反例外推为真实协议结论。
