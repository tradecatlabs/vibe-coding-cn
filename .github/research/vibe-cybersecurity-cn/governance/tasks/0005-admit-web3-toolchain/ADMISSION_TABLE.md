# Web3 工具链准入表

快照：`2026-08-14`。本表由 `web3-admission-candidates.json` 生成，禁止手工修改。

`admitted` 表示已完成 9 项门禁（含 research_source）并固定版本；运行权仍由 ScopeGrant 和运行时策略决定。

| 状态 | 工具 | 角色 | 固定版本 | 门禁 | 行为证据 |
|---|---|---|---|---|---|
| admitted | Foundry (forge/cast/anvil) | EVM 构建、测试、模糊测试与本地链执行面 | 1.7.1 (commit 4072e48705 2026-05-08) | 9/9 | web3-lab/evidence/forge-test-2026-08-14.log (4/4) |
| admitted | Slither | Solidity 静态候选生成器 | 0.11.6 (PyPI slither-analyzer) | 9/9 | evidence/slither-2026-08-14.json (命中 reentrancy-eth/arbitrary-send-eth) |
| admitted | Echidna | Solidity 属性模糊验证器 | 2.3.3 (x86_64-linux tar.gz) | 9/9 | evidence/echidna-*Echidna-2026-08-14.log (4 属性反例) |
| admitted | solc-select | Solidity 编译器版本管理 | solc 0.8.35 (solc-select install) | 9/9 | forge build + slither 编译一致（0.8.35） |
| admitted | Forge-std | Foundry 测试标准库（断言/作弊码） | v1.16.2 (commit bf647bd6046f2f7da30d0c2bf435e5c76a780c1b) | 9/9 | forge test 4/4（2026-08-14 重装后） |

## 汇总

- 准入候选：5
- 已正式纳入（admitted）：5

## 门禁含义

research_source / license_review / immutable_pin / integrity_verification / security_review / interface_contract / isolation_policy / behavior_test / rollback_test：
9 项全部 pass 才允许 admitted。
