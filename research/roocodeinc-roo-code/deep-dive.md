# RooCodeInc/Roo-Code 深度研究

## 研究级别

- 当前级别：L2 结构深度研究。
- 研究对象：`RooCodeInc/Roo-Code`。
- 证据来源：本目录 `raw/` 下的 GitHub 元数据、release 快照、规则文件和本地仓库工作树。
- 观察日期：2026-07-03。

## L2 结论

`RooCodeInc/Roo-Code` 的核心价值不是当前采用，而是归档工具的生命周期样本。它曾经是一个大型
TypeScript 多 Agent 编辑器项目，仓库中保留了 `.roomodes`、`.roo/` 规则与技能、monorepo
工作区、VS Code 应用、核心包、release 资产和安全文档，但 GitHub 观测状态已经是 archived。

对本仓最重要的启发是：高星项目也必须被生命周期治理约束。已归档项目可以研究结构，不能作为
默认采用对象。

## 本地证据

- `domain.yml`：`archived: true`，最新 release 为 `v3.54.0`，研究优先级为 P3。
- `raw/repository/.roomodes`：模式定义入口。
- `raw/repository/.roo/`：Roo 规则、技能、命令和配置入口。
- `raw/repository/apps/`：应用层目录，包含 CLI、docs、VS Code 相关应用。
- `raw/repository/packages/`：包层目录，包含 core、ipc、types 等共享模块。
- `raw/repository/pnpm-workspace.yaml`：monorepo 工作区入口。
- `raw/repository/package.json`：项目脚本和依赖入口。
- `raw/repository/SECURITY.md`：安全政策。
- `raw/repository/releases/`：release 图片资产。

## 关键机制

### 显式模式和规则文件

`.roomodes` 和 `.roo/` 说明多 Agent 工具需要把模式、规则、技能和命令显式文件化。模式不是口头
提示，而是工具运行时可读取的配置资产。

### monorepo 分层

`apps/` 和 `packages/` 的拆分体现了大型工具项目的常见边界：应用入口、文档、测试环境和共享核心
能力分开维护。对本仓有启发的是“入口和核心能力要分层”，不是要复制其前端或扩展实现。

### 归档状态是硬事实

该项目 stars 很高，但已经归档。研究结论必须尊重生命周期字段：归档对象只能作为历史结构和设计
参考，不能作为活跃生态推荐。

## 可迁移模式

- 在资源治理中把 archived 设为强降级信号。
- 对 agent 工具研究记录模式文件、规则文件、技能文件和命令文件的边界。
- 为本仓 `skills/` 和 Agent 规则建立“模式、规则、技能、命令”四类概念边界。
- 研究大型工具时优先看 apps/packages 分层、脚本入口、安全文档和 release 资产。
- 对已归档项目保留替代入口或分叉观察字段。

## 对本仓的影响

该对象对本仓的直接影响是治理规则，而不是工具采用：

- `assets/external-resources/` 应把归档状态作为资源生命周期字段。
- `research/` 对 archived 项目应默认降级为设计参考。
- `skills/` 可借鉴显式模式/规则/命令边界，但不复制其运行时。
- 资源推荐页需要区分“可采用工具”“历史参考”“已归档设计样本”。

## 风险和待验证项

- 已归档状态意味着安全、兼容性和生态活跃度都不能默认满足。
- 仓库规模大，本轮只做结构研究，没有运行构建、测试或扩展。
- 该项目具体实现和当前主流工具生态可能已经分叉或迁移。
- 本仓是知识库，不应引入 Roo-Code 的 UI、runtime 或 monorepo 复杂度。

## 下一步 L3 验证任务

- 在资源 schema 中增加 archived、forked、replaced_by 和 last_verified 字段。
- 为研究域契约增加 archived 项目处理规则：只能作为参考，不能进入默认推荐。
- 对 `.roomodes`、`.roo/rules`、`.roo/skills` 做一次概念边界拆解，迁移到 Agent 规则设计文档。
- 查找当前活跃替代项目或分叉，并建立后续观察队列。
