# Task Overview
- Task ID: `0003`
- Slug: `add-deepseek-harness-upstream`
- Objective: `将 DeepSeek Harness 官方 GitHub 仓库接入受治理上游同步、revision lock 与研究边界`
- Status: `Done`

## In Scope
- 登记并拉取 `deepseek-ai/deepseek-harness` 官方 `master` 分支。
- 以单一 source registry 同时驱动 checkout 同步与 revision lock 生成。
- 固定 commit、MIT 许可证、核心源码路径、文件计数与 developer preview 限制。
- 更新同步回归、研究文档、目录自述与治理上下文。

## Out of Scope
- 不执行、构建或安装任何上游代码。
- 不配置 DeepSeek API，不读取或保存 API key。
- 不把 `research/upstreams/` checkout 纳入本项目 Git 历史。
- 不做完整 Harness 架构评分或生产可用性背书。

## Task Package Tree
```text
TP-01 核验官方仓库与本地边界
  -> TP-02 接入单一登记源、同步逻辑、回归与文档
      -> TP-03 真实同步四源并执行验证、治理与交付收口
```

## Requirement Alignment
- 用户明确要求从 GitHub 拉取 `deepseek-ai/deepseek-harness`。
- 官方 README 将其定义为 DeepSeek AI 开发的开源 agent harness，当前为 developer preview。
- 本项目现有同步入口只登记三个上游，DeepSeek checkout 与 lock 条目均不存在。

## Task Package Overview
| ID | 目标 | 主要输出 | Depends On |
|---|---|---|---|
| TP-01 | 固定官方来源、分支、许可证、核心路径与 preview 边界 | revision 绑定的来源事实 | - |
| TP-02 | 将第四源接入单一登记源、安全同步、lock、测试和文档 | 可重跑实现与回归 | TP-01 |
| TP-03 | 真实拉取、幂等验证、项目门禁和本地 Git 交付 | checkout、lock、验证证据、commit | TP-02 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
