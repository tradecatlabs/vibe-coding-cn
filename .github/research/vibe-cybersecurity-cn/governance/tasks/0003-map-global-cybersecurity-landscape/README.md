# Task Overview

- Task ID: `0003`
- Slug: `map-global-cybersecurity-landscape`
- Objective: 建立网络安全全局景观，统一资产面、威胁行为、防御生命周期、证据标准与成熟工具坐标，并明确本项目覆盖、集成和禁区。
- Status: `Done`

## In Scope

- 建立跨行业、技术层面的资产、防御、威胁和证据四轴地图。
- 把任务 0001 的 46 项研究候选映射回全局能力面。
- 固定本项目“直接建设 / 对接成熟系统 / 禁止自治”的产品边界。
- 同步长期上下文、ADR、入口文档和治理索引。

## Out of Scope

- 不执行扫描、漏洞利用、凭据测试或任何目标访问。
- 不下载、安装、固定或正式准入任何候选工具。
- 不代替国家、行业或组织专属合规映射。
- 不声称当前项目拥有运行时安全能力。

## Task Package Tree

```text
ROOT
├── TP-01 研究权威坐标轴
├── TP-02 绘制长期景观与产品边界
├── TP-03 映射 46 项候选和覆盖空白
└── TP-04 审查、文档同步与严格校验
```

## Requirement Alignment

- 用户要“全局景观”：以一张长期地图回答整个网络安全领域如何分层。
- 项目要“自动找漏洞”：明确它只是全局景观中的安全证据控制面，而非整个安全栈。
- 胶水原则：成熟框架定义语言，成熟工具提供能力，自研只承担授权、编排、适配和证据。

## Task Package Overview

| Node | Output | Acceptance |
|---|---|---|
| TP-01 | `SOURCE_LEDGER.md` | 来源均为官方框架、标准组织或既有官方候选账本 |
| TP-02 | `CYBERSECURITY_LANDSCAPE.md`、ADR-0001 | 四轴完整，项目边界清楚 |
| TP-03 | `LANDSCAPE_COVERAGE.md` | 八类计数合计 46，空白与处理原则明确 |
| TP-04 | `REVIEW.md`、严格校验结果 | 无占位符、死链或过度完成声明 |

## Reading Order

1. `governance/context/CYBERSECURITY_LANDSCAPE.md`
2. `LANDSCAPE_COVERAGE.md`
3. `SOURCE_LEDGER.md`
4. `governance/decisions/adr/ADR-0001-security-evidence-control-plane.md`
5. `STATUS.md`
