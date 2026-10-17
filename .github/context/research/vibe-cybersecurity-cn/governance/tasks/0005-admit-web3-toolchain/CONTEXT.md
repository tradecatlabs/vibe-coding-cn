# Repo Evidence

- 0004 已固定工具版本并跑通本地闭环：Foundry 1.7.1、Slither 0.11.6、
  Echidna 2.3.3、solc 0.8.35；forge-std 由 forge init 安装（无固定 tag）。
- 0002 定义了 8 门禁准入模型（research_source、license_review、immutable_pin、
  integrity_verification、security_review、interface_contract、isolation_policy、
  behavior_test、rollback_test），但其校验器硬绑定 0001 研究目录。
- 验证控制面 0004 以 shadow 校准运行；多叶子任务自动强制 verification plan，
  需要 git 仓库派生 owner 输入摘要基线。
- forge-std 最新 release：v1.16.2（2026-08-14 核实）。

# Constraints Matrix

| 约束 | 强制决策 |
|---|---|
| 0002 校验器绑定 0001 | Web3 准入独立建目录，源指向 0004 候选表 |
| admitted 要求全门禁 | 只对真实验证过的 5 项工具授予 admitted |
| 验证控制面需要 git | git init + 初始提交，不 push 远端 |
| 属性基线需覆盖全部漏洞 | Echidna 属性扩展到 EXP-01..04 |
| 多 AI 并行工作区 | git 只做 init/初始提交，禁 reset/clean/stash/checkout -f |

# Change Boundary

新增 `governance/tasks/0005-admit-web3-toolchain/`、Web3 准入 JSON/校验器、
Echidna 属性合约；重装 `web3-lab/lib/forge-std` 到 v1.16.2；初始化 Git 仓库并
做一次初始提交；更新 verification policy 为 enforce；同步治理资产。

# Risk Matrix

| 风险 | 影响 | 控制 |
|---|---|---|
| git init 影响并行 AI | 工作区状态变化 | 只 init+初始提交，不 push 不改他人文件 |
| forge-std 重装破坏工程 | 测试无法编译 | 旧目录先备份到 /tmp，验证后删除 |
| 属性测试误报 | 错误基线 | 以 ground truth 为准，反例需人工核对 |
| 准入门禁形式化 | 假 admitted | 每项门禁绑定真实证据（版本、输出、测试） |

# Assumptions and Falsification

- 假设：git init + 初始提交是验证控制面升级的必要前提且用户已授权补齐到 100%；
  推翻条件：用户明确禁止 git 操作则回退 shadow 模式。
- 假设：5 项核心工具完成 8 门禁即可称为 Web3 工具链 100% 基线；
  推翻条件：后续真实审计暴露工具面缺口，再扩展候选与准入。
- 假设：Echidna 属性覆盖 4 漏洞后动态验证基线完整；
  推翻条件：某漏洞属性无法在合理时间内找到反例，记录为属性盲区。

# Critical Ambiguities

- git 初始提交包含当前全部文件（除 .gitignore 排除）；无凭据，无远端。
- Echidna 对访问控制/预言机属性需要 wrapper 合约跟踪状态；复杂度可控。

# Debug Evidence Contract

- 调试模式: `Optional`
- 本任务不是缺陷修复任务；失败由校验器、测试失败或门禁非零退出暴露。

# Task Package Context Map

- TP-01：`web3-admission-candidates.json`、`validate_web3_admission.py`
- TP-02：`web3-lab/lib/forge-std`（v1.16.2）
- TP-03：`web3-lab/test/*Echidna*.t.sol`、`echidna.yaml`
- TP-04：`.git/`、`verification-policy.v1.json`（enforce）、TASK_CLOSEOUT_PACKET.json
- TP-05：治理上下文、`STATUS.md`、`REVIEW.md`
