---
id: GOV-COMBAT-READINESS
type: context
status: current
owner: engineering
created: 2026-08-14
last_reviewed: 2026-09-02
review_cycle: P30D
---

# 实战就绪度评估（Web3 授权审计）

本文件回答："距离 S0 实战（公开协议源码 + 本地/fork 只读审计）还差多少"。
实战定义：给定 DeFi/Web3 公开协议仓库（代码公开即研究输入），完成 clone -> 固定 commit ->
编译 -> Slither/Foundry 候选 -> 本地 PoC -> fork 只读分析 -> 证据归档 -> 审计报告，
且结论可复查；如需链上主动交互（交易/利用验证），才绑定真实授权来源并退出默认 S0 面
（边界见 `AUTHORIZATION_BOUNDARIES.md`）。

## 现状盘点（2026-09-02）

| 维度 | 状态 | 证据 |
|---|---|---|
| 任务基线 | 0001-0007 全部 Done | tasks/INDEX.md |
| 工具链 | Foundry 1.7.1 / Slither 0.11.6 / Echidna 2.3.3 / solc 0.8.35，5 项 admitted | 0005 ADMISSION_TABLE |
| 靶场验证 | 4 类漏洞攻击测试 4/4 + 4 属性反例 | web3-lab/evidence |
| 验证控制面 | enforce 模式，git digest 绑定，closeout 全绿 | 0005 closeout |
| Skills 供应链 | 13 个项目级 skill（Web3 赏金/合约审计） | skills/SKILLS_MANIFEST.json |
| 供应链审计 | 14 仓库审计无投毒 | 0006 报告 |
| M1 审计管线骨架 | audit/run.sh 双模式跑通 EVK 全链路（build/slither/test/证据） | 0011 closeout、audit/README |

## 实战就绪度评分（0-100）

| 能力域 | 权重 | 得分 | 说明 |
|---|---:|---:|---|
| 方法学与工具链 | 25% | 80 | 工具齐、方法验证过，缺真实工程适配 |
| 供应链与 skills | 15% | 90 | 已 vendored 13 skill，含流程参考 |
| 端到端执行管线 | 25% | 45 | M1 骨架成型：clone->固定 commit->build->slither->test->证据 已在 EVK 跑通；缺完整套件/Hardhat/报告步骤 |
| 链上数据接入 | 10% | 10 | 无 RPC 凭据管理、无 fork 配置、无区块快照策略 |
| 情报与漏洞模式 | 10% | 30 | Solodit/DeFiHackLabs 未接入；skill 有 bug-classes |
| 报告与交付 | 10% | 20 | 证据账本有，审计报告模板/分级/修复建议无 |
| 授权与运行时安全 | 5% | 50 | 边界已收敛为宽松口径（只读放行/主动交互三通道）；ScopeGrant 尚无运行时执行器 |
| **综合** | 100% | **≈55** | 管线骨架成型（EVK 端到端证据），完整案例与情报源未接入 |

## 差距清单（按优先级）

### P0：S0 公开协议目标（代码公开即研究输入）

- 用户指定 DeFi/Web3 公开协议仓库（或从候选表自选公开仓库）；fork 级只读审计不需要额外授权。
- 默认动作：clone、固定 commit、编译、Slither/Foundry、本地 PoC、fork 只读状态分析。
- 默认禁止：真实链上交易、主动扫描线上目标、接触用户数据、把目标响应当授权依据。
- 仅当需要链上主动交互时，按三通道（自有资产 / 赏金规则 / 书面授权）导入 ScopeGrant，并作为 S1/S2 扩展处理。

### P1：端到端审计管线（最大工程缺口）

- 源码获取：克隆 + 固定 commit + 校验摘要。
- 工程编译：真实协议多为 Hardhat/Foundry + Node 依赖 + 多版本 solc；
  需验证 Node v22 环境下依赖安装与编译（当前只验证过纯 Foundry 工程）。
- 扫描步骤：Slither（+Aderyn 候选）产出结构化候选 JSON。
- 验证步骤：Foundry 攻击测试 + Echidna 协议级不变量（业务建模方法论未沉淀）。
- 报告步骤：证据账本 -> 审计报告（分级/影响/PoC/修复建议）。
- 编排脚本：一个可复跑 runner（`audit/run.sh` 或 Python 编排），参数外置、失败非零退出。

### P1：链上数据接入

- RPC 端点（Infura/Alchemy/公共端点）与凭据管理器接入（credential security 规则）。
- `anvil --fork-url <rpc> --fork-block-number <n>` 配置与快照策略。
- fork 数据缓存与成本/速率控制。

### P2：情报与报告

- Solodit API 接入（漏洞模式对照）、DeFiHackLabs 历史事件对照。
- 审计报告模板（SWC 映射、严重度分级、修复建议、时间线）。
- 人工复核（HITL）流程：审计结论必须由人确认后方可对外。

### P2：授权来源导入器与运行时执行器

- 按 `AUTHORIZATION_BOUNDARIES.md` 的 v1 字段契约实现三通道导入器
  （自有资产注册表 / bounty 规则导入 / 书面授权文件解析）。
- ScopeGrant 从文档升级为运行时检查（范围、动作等级、速率、停止条件）。
- 审计隔离目录与凭据注入规范落地。

## 里程碑路径

```text
M1（2026-09-02 完成）: S0 管线骨架 —— audit/run.sh 在 EVK 上双模式跑通
M2: 完整套件 + 第一个 S0 fork 案例 —— EVK 全量 fuzz/invariant；指定协议 fork 主网区块，静态候选 + 1-2 个本地 PoC/只读验证
M3: 完整案例 —— 候选 -> 验证 -> 证据 -> 报告全链，人工复核
M4: 能力固化 —— 情报源接入、不变量建模方法论沉淀、管线参数化复用
```

## 触发条件

- 用户提供 DeFi/Web3 公开协议仓库后，M1/M2 可立即启动（工具已就绪；S0 只读研究无需授权）。
- 不依赖新工具安装（Aderyn/Solodit 为增强项，非阻塞）。

## 反事实

- 如果管线建成后真实协议上"零发现"，需要对照靶场召回率区分：
  工具失灵 vs 目标确实干净 vs 不变量建模不足；不能把零发现当作审计通过声明。
