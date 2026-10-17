# Task Overview
- Task ID: `0005`
- Slug: `research-expanded-harness-sources`
- Objective: `对新增十一个官方 Harness 做 revision 绑定的源码级调研，产出可复核的研究报告并更新领域模型`
- Status: `Done`

## In Scope
- 在 15 个已锁定 checkout 中阅读 11 个新增 Harness 的官方文档与核心源码。
- 每个 Harness 记录 agent loop、工具/MCP/ACP、session/memory、权限审批、sandbox、provider 抽象与扩展机制。
- 产出 `research/HARNESS_RESEARCH.md`，横向比较并标注源码证据路径。
- 把元 Harness 治理控制面有借鉴意义的发现回写领域文档与 module context。

## Out of Scope
- 不执行、构建、安装或测试任何上游代码。
- 不配置模型/API，不读取或保存凭据。
- 不修改 source registry、同步器或 revision lock。
- 不为上游实现适配器、patch 或 PR。

## Task Package Tree
```text
TP-01 逐仓源码级调研 11 个新增 Harness
  -> TP-02 横向比较与元 Harness 治理借鉴
      -> TP-03 文档同步、门禁审查与本地交付
```

## Requirement Alignment
- 用户要求“开始继续调研；新增 11 个”，即对 0004 已同步的 11 个官方 Harness 做源码级研究。
- 现有 15 源 registry/lock 已提供 revision 绑定研究输入，不需要第二套来源登记。
- 元 Harness 的领域模型（docs/HARNESS_MODEL.md）需要真实 Harness 事实检验，本轮研究是第一个批量输入。

## Task Package Overview
| ID | 目标 | 主要输出 | Depends On |
|---|---|---|---|
| TP-01 | 逐仓记录 11 个 Harness 的六类维度事实 | HARNESS_RESEARCH.md 每仓小节 | - |
| TP-02 | 横向比较并提炼元 Harness 治理借鉴 | 领域文档更新 | TP-01 |
| TP-03 | 文档同步、门禁、治理与本地交付 | 验证证据与 commit | TP-02 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. TODO.md
6. STATUS.md
