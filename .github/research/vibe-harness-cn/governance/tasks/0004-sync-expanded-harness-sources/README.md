# Task Overview
- Task ID: `0004`
- Slug: `sync-expanded-harness-sources`
- Objective: `将用户指定的十一项官方 Harness 纳入受治理同步、revision lock 与研究边界`
- Status: `Done`

## In Scope
- 拉取并登记用户明确列出的 11 个官方 Harness：Pi、OpenClaw、Goose、Gemini CLI、Cline、Qwen Code、Kimi Code、Crush、Mistral Vibe、OpenHands、Hermes Agent。
- 基于实际 checkout 核验 canonical origin、默认分支、许可证、核心源码路径与迁移/生命周期限制。
- 将 11 个来源接入现有单一 source registry、revision lock、同步回归与研究文档。
- 真实同步全部 15 个受治理来源并验证幂等、fail-closed 与本地 Git 交付。

## Out of Scope
- 不执行、构建、安装或测试任何上游仓库代码。
- 不配置模型/API，不读取或保存任何上游凭据。
- 不把 `research/upstreams/` checkout 纳入本项目 Git 历史。
- 不把未被用户列入本轮的 Aider、mini-SWE-agent、Trae、Zed 等研究样本顺手加入。
- 不在无测量证据时引入并发同步、数据库、插件框架或新依赖。

## Task Package Tree
```text
TP-01 核验 11 个官方来源与源码边界
  -> TP-02 接入 registry、lock、测试与文档
      -> TP-03 真实同步 15 源、审查、治理与本地交付
```

## Requirement Alignment
- 用户明确要求拉取其粘贴的最高优先级 4 项与第二梯队 7 项，共 11 项。
- 现有 source registry 已支持数据驱动扩容，不需要创建第二套候选清单或专用同步器。
- canonical 迁移必须如实处理：Pi 使用 `earendil-works/pi`、Goose 使用 `aaif-goose/goose`、Kimi 使用 `MoonshotAI/kimi-code`。

## Task Package Overview
| ID | 目标 | 主要输出 | Depends On |
|---|---|---|---|
| TP-01 | 固定 11 个官方来源、分支、许可证、核心路径与限制 | revision 绑定的来源事实 | - |
| TP-02 | 将 11 源接入现有 registry、lock、测试和文档 | 15 源可重跑同步实现 | TP-01 |
| TP-03 | 真实拉取、幂等验证、性能审查、门禁和本地交付 | checkout、lock、验证证据、commit | TP-02 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
8. REVIEW.md
9. AUDIT_CASE_SAMPLING.md
10. REUSE_SAMPLING.json
