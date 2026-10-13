# Planning Summary

目标终态是稳定的网络安全坐标系：业务风险位于顶层，资产、攻击行为和防御生命周期构成主体，
证据可信度贯穿全链路。本项目只占据授权验证和证据晋升位置，通过成熟工具连接其他能力。

# Lifecycle Gates

总生命周期为 `SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP`，任何 gate 均不得跳过；任一失败必须保持非完成状态。

1. SPEC：任务意图有可执行验收，框架职责与安全边界明确。
2. PLAN：最短路径、任务包、依赖、回滚和停止条件明确。
3. BUILD：长期景观、ADR、来源账本和覆盖映射落盘。
4. TEST：46 项计数、Task Intent、task docs 与治理 strict/health 通过。
5. REVIEW：专项自审检查版本、概念、覆盖、范围和完成声明。
6. SHIP：只交付本地文档与治理资产，不安装、不部署、不推送。

# Simplest Path

- 一个长期景观文档承载坐标系，不建数据库或 taxonomy service。
- 一个 ADR 固定产品边界，不复制成第二套架构原则。
- 一个任务覆盖表引用现有机器目录，不另建工具目录。
- 不为纯文档地图新增业务脚本；使用既有任务和治理校验器。

# Split Strategy

- TP-01 固定来源和概念证据上限。
- TP-02 从未来终态定义全局坐标和产品位置。
- TP-03 反向映射现有候选，验证地图有解释力。
- TP-04 消除漂移并绑定新鲜验证。

# Execution Waves

```text
TP-01 -> TP-02 -> TP-03 -> TP-04
```

# Runtime Workflow Contract

- Allowed：官方资料只读检索、本地 Markdown/JSON 编辑、既有校验命令。
- Forbidden：下载/安装安全工具、主动扫描、利用、猜测凭据或访问目标。
- Evidence：官方 URL、目录分类计数、任务 closeout、治理 strict/health。
- Stop：候选被写成已验证能力、职责层互相混淆、出现无来源动态断言或治理校验失败。

# Next Executable Leaves

- TP-04：执行专项审查、严格验证和 closeout。

# Dependency Graph

```text
official frameworks / standards       0001 research catalog
                 \                     /
                  -> global landscape
                           |
                  ADR product boundary
                           |
                future vertical proof task
```

# Rollback Protocol

删除 0003 任务和新增景观/ADR，恢复项目入口及索引即可。没有业务数据、外部资源、工具安装或网络状态需要迁移。
