# web3-lab：EVM 已知漏洞靶场与候选-验证-证据闭环

本地隔离靶场，证明 `候选漏洞 -> 独立复现 -> 证据归档 -> 实证漏洞视图` 链路。
只运行于本机 Foundry 环境，无任何外部 RPC 或公网目标。

## 靶场漏洞（ground truth）

| ID | 合约 | 类别 | SWC | 验证测试 |
|---|---|---|---|---|
| EXP-01 | `src/ReentrancyVault.sol` | 重入 | SWC-107 | `test/EXP-01-Reentrancy.t.sol` |
| EXP-02 | `src/ArithmeticOverflow.sol` | unchecked 溢出 | SWC-101 | `test/EXP-02-Overflow.t.sol` |
| EXP-03 | `src/AccessControlVault.sol` | 缺失访问控制 | SWC-105 | `test/EXP-03-AccessControl.t.sol` |
| EXP-04 | `src/PriceOracleManipulation.sol` | 预言机操纵 | SWC-131 | `test/EXP-04-PriceOracle.t.sol` |

## 复跑方法

```bash
export PATH="$HOME/.foundry/bin:$PATH"
cd web3-lab
export PATH="../.venv-web3/bin:$PATH"

# 1. 构建与攻击验证（独立验证基准）
forge build && forge test -vv

# 2. 静态候选生成（Slither）
slither . --json /tmp/slither-out.json --solc-solcs-select 0.8.35

# 3. 属性模糊验证（Echidna，对 EXP-02）
../../.tools/echidna test/OverflowEchidna.t.sol --contract OverflowEchidna --config echidna.yaml

# 4. 证据一致性校验
python3 validate_lab_evidence.py
```

## 结果解读（2026-08-14 基线）

- Foundry 攻击测试 4/4 复现，全部 `confirmed`。
- Slither 命中 EXP-01（reentrancy-eth）与 EXP-03（arbitrary-send-eth 近似），
  漏报 EXP-02（unchecked 溢出）与 EXP-04（预言机操纵）。
- Echidna 找到 EXP-02 回绕反例（属性测试通道）。
- 结论：静态候选不能直接当实证；多通道交叉验证才能覆盖漏报面。

## 工具版本（固定基线）

| 工具 | 版本 | 来源 |
|---|---|---|
| Foundry | 1.7.1 (4072e48705) | foundryup 官方安装器 |
| Slither | 0.11.6 | PyPI 固定版本 |
| Echidna | 2.3.3 | GitHub release x86_64-linux |
| solc | 0.8.35 | solc-select（目标 pragma ^0.8.23） |

## 安全边界

- 本目录全部合约是有意植入漏洞的教学靶场，禁止用于任何真实协议。
- 工具输出只是候选；`status: confirmed` 仅表示本地攻击测试复现成功。
