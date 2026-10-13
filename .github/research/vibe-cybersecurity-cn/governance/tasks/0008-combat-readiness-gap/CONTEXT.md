# Repo Evidence

- 任务基线：0001-0007 全部 Done（INDEX.md）。
- 工具链：Foundry 1.7.1 / Slither 0.11.6 / Echidna 2.3.3 / solc 0.8.35 /
  forge-std v1.16.2，5 项 admitted（0005 ADMISSION_TABLE.md）。
- 靶场：web3-lab 4 类漏洞攻击测试 4/4 + Echidna 属性反例 4 份（evidence/）。
- 验证控制面：enforce 模式、git 输入摘要绑定、closeout gate ready=true。
- Skills：13 个 vendored skill（web3-bug-bounty-hunting `41238d8` MIT +
  smart-contract-audit `4c0b700` Apache-2.0）。
- 供应链审计：0006 报告 14 仓库无投毒。

# Constraints Matrix

| 约束 | 强制决策 |
|---|---|
| 实战目标未指定 | M1 之前不选择、不拉取真实协议仓库 |
| 凭据安全 | RPC 等凭据只能经凭据管理器运行时注入，不落盘 |
| 多 AI 并行工作区 | 禁 reset/clean/stash/checkout -f；不 push |
| 证据纪律 | 工具输出只是候选；未经独立验证不得晋升为实证 |
| 工具就绪 | 不依赖新工具安装即可启动 M1（Aderyn/Solodit 为增强项） |

# Change Boundary

新增 `governance/tasks/0008-combat-readiness-gap/` 任务目录与
`governance/context/COMBAT_READINESS.md` 就绪度真相源；同步拓扑、操作模型、
上下文地图、README、任务索引与 tasks/AGENTS.md；不改动 web3-lab 与 skills/。

# Risk Matrix

| 风险 | 影响 | 控制 |
|---|---|---|
| 评分主观 | 误导决策 | 每项得分绑定现状证据与权重说明 |
| 差距清单过宽 | M1 无法启动 | P0/P1/P2 分级，P1 只留最大工程缺口 |
| 实战承诺过度 | 越权或误报 | 文档明确"授权求交"与 HITL 复核 |
| 治理文档漂移 | 死链/占位 | strict/health + closeout 全绿 |

# Assumptions and Falsification

- 假设：综合就绪度 ≈47 分是对"真实授权协议 fork 级审计"的合理量化；
  推翻条件：用户给出更精确的实战定义或权重，重新评分。
- 假设：工具链已就绪、管线未成型是最大差距；
  推翻条件：M1 验证暴露工具缺失或环境不兼容，差距表更新。
- 假设：用户将提供授权协议仓库以启动 M1；
  推翻条件：用户明确不提供目标，则 M1 改为自建授权靶场协议。

# Critical Ambiguities

- 实战范围（单协议源码审计 vs 主网 fork 动态验证）需在 M1 开始时与用户确认。
- Node 依赖下的真实协议编译（Hardhat + 多版本 solc）尚未在本项目验证。
- 情报源（Solodit/DeFiHackLabs）接入方式与 API 凭据未定。

# Debug Evidence Contract

- 调试模式: `Optional`
- 本任务不是缺陷修复任务；失败由校验器、strict/health 或非零退出暴露。

# Task Package Context Map

- TP-01：INDEX.md、ADMISSION_TABLE.md、web3-lab/evidence、SKILLS_MANIFEST.json
- TP-02：`governance/context/COMBAT_READINESS.md`
- TP-03：PROJECT-TOPOLOGY.md、PROJECT_OPERATING_MODEL.md、CONTEXT-MAP.md、
  README.md、tasks/INDEX.md、tasks/AGENTS.md
- TP-04：STATUS.md、TODO.md、ACCEPTANCE_CHECKLIST.md、closeout 校验输出
