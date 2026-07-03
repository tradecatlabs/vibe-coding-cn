# RooCodeInc/Roo-Code 研究分析

## 本轮结论

- Roo Code 是已归档的多模式编辑器 agent 工具，当前更适合作为设计参考和历史样本。
- 虽然归档，但其 monorepo 结构、modes、schemas、webview-ui、packages 和 src 仍有研究价值。
- 本仓应借鉴它的模式配置、扩展 UI 与 agent 工具组织，但不应把它列为优先采用对象。

## 本地证据

- 研究对象：`RooCodeInc/Roo-Code`
- 当前研究角色：已归档多 Agent 编辑器工具
- 本轮成熟度：L1 初步理解
- 原始仓库：`raw/repository/`
- 原始来源清单：`raw/sources.yml`
- 事实摘要：`domain.yml`

## 结构观察

- 根目录包含 `apps/`、`packages/`、`src/`、`webview-ui/`、`schemas/`、`locales/`、`.roo/`、`.roomodes`。
- README 以 What Can Roo Code Do、Modes、Resources、Disclaimer、License 组织。
- 存在 pnpm workspace、turbo、changeset 等前端/扩展 monorepo 基础设施。

## 可借鉴点

- 多模式 agent 可以通过显式模式文件和 schema 管理。
- Webview UI 与扩展核心分离是 IDE agent 的常见形态。
- 归档项目仍可作为迁移风险和生态生命周期样本。

## 风险和边界

- `domain.yml` 已标记 archived，不能当作活跃生态主线。
- 历史实现可能已经被 fork 或替代，采用建议必须重新核验。
- 仓库体量较大，二轮研究要聚焦模式和 schema，不做全量阅读。

## 下一轮研究任务

- 阅读 `.roomodes`、`schemas/` 和 `src/` 中 mode/tool 相关代码。
- 整理“归档工具如何降级为参考对象”的研究归档规则。

## 沉淀判断

- 本轮只完成 L1 理解，不直接迁入 concepts、references、workflow 或 skills。
- 只有经过 L2 源码阅读、实验验证或交叉对照后的结论，才进入稳定层。