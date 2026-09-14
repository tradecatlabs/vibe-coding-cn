# Governance Tasks Guidelines

`governance/tasks/` 保存阶段性任务契约、研究资产、执行状态和新鲜证据；它不是长期工程规则或生产数据仓。

## 目录结构

```text
governance/tasks/
├── README.md                                    # 任务域边界
├── AGENTS.md                                    # 本目录操作规则
├── INDEX.md                                     # 任务索引
├── lessons.md                                   # 候选教训整理池
├── 0001-survey-cybersecurity-supply-chain/      # 首轮供应链调研任务
├── 0002-prepare-supply-chain-admission/         # 供应链准入候选任务
├── 0003-map-global-cybersecurity-landscape/     # 全局景观、覆盖映射与边界证据
├── 0004-web3-vertical-proof/                    # Web3/EVM 聚焦供应链与本地靶场闭环
├── 0005-admit-web3-toolchain/                   # Web3 工具链准入与验证控制面升级
├── 0006-audit-security-skills-sandbox/          # 安全 skills 供应链审计沙盒
├── 0007-vendor-project-skills/                  # 项目级 skills vendored 落地
└── 0008-combat-readiness-gap/                   # 实战就绪度评估与差距清单
```

## 职责边界

- 每个任务目录拥有自己的目标、范围、验收、状态和局部研究证据。
- 任务结论只有经过审查和治理晋升后，才能成为 `standards/`、`architecture-gates/` 或 `context/` 的长期事实。
- 动态网络事实必须记录观察日期；工具能力声明必须回指官方仓库、官方文档或真实复跑证据。
- 不在任务目录保存凭据、目标秘密、未脱敏扫描响应或可利用 payload。

## 验证

任务文档使用 `auto-tasks` validator；任务自有机器资产使用任务目录声明的 owner validator。创建、删除或重划任务资产职责时同步本文件与任务 `README.md`。
