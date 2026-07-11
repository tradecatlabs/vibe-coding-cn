# tradecatlabs/vibe-coding-cn 深度研究

## 研究级别

- 当前级别：L2 源码/结构深度研究。
- 研究对象：`tradecatlabs/vibe-coding-cn`。
- 证据来源：本目录 `raw/` 下的 GitHub 元数据、README 快照、本地仓库工作树和当前工作区对照。
- 观察日期：2026-07-03。

## L2 结论

`tradecatlabs/vibe-coding-cn` 的研究价值不只在内容本身，而在它正在从“中文 Vibe Coding 文档仓库”
演化为“文档、提示词、技能、研究域、外部资源、机器索引和质量门禁共同组成的 AI 工程知识系统”。

本轮对照发现：raw 快照代表上游公开仓库状态，当前工作区已经继续增加研究域、raw 原始事实层、
外部资源本地化、脚本门禁和更多索引入口。也就是说，本仓正在形成自我研究和自我治理能力。

## 源码证据

raw 快照中已经存在的主结构：

- `raw/repository/README.md`：项目主入口。
- `raw/repository/AGENTS.md`：AI Agent 操作规则。
- `raw/repository/docs/`：知识库。
- `raw/repository/prompts/`：提示词入口。
- `raw/repository/skills/`：技能库。
- `raw/repository/assets/`：资源和 AI 引用资产。
- `raw/repository/tools/`：工具与外部依赖。
- `raw/repository/metadata/`：机器可读索引。
- `raw/repository/scripts/`：自动化脚本。
- `raw/repository/Makefile`：质量门禁入口。
- `raw/repository/llms.txt`：AI 短上下文入口。

当前工作区新增或强化的结构：

- `research/`：从短篇研究扩展为“一对象一研究域”。
- `research/*/raw/`：外部研究对象的一手事实层。
- `scripts/fetch-research-raw.py`：研究域 raw 拉取脚本。
- `scripts/check-research-raw.py`：研究域 raw 完整性检查脚本。
- `assets/external-resources/`：外部资源本地化管理入口。
- `scripts/check-external-resources.py`：外部资源校验脚本。
- `metadata/taxonomy.yml`：跨目录机器索引。
- `assets/ai-citation/llms-full.txt`：AI 完整上下文入口。

## 关键机制

### 仓库正在从内容库变成控制面

早期价值是把 Vibe Coding 经验整理成中文文档；当前价值开始转向结构治理：目录职责、索引、
raw 事实、质量门禁、AI 引用入口和脚本控制面共同约束内容演化。

### 研究域让外部资料可审计

一仓库一研究域、raw 原始事实层、domain.yml 和 analysis/deep-dive 分层，解决了外部链接容易漂移、
二手总结不可复查、研究结论难以下沉的问题。

### 机器入口让仓库能被 AI 稳定读取

`llms.txt`、`llms-full.txt` 和 `metadata/taxonomy.yml` 让仓库不只面向人类浏览，也面向 AI 检索、
引用和上下文注入。这是 Vibe Coding 仓库区别于普通教程仓库的关键方向。

### 质量门禁让文档进入工程状态

`Makefile`、Markdown lint、链接检查、目录结构检查、metadata 检查和 research raw 检查说明：
文档不是随手写的文本，而是有结构约束的工程资产。

## 可迁移模式

- 把文档仓库当作工程系统治理，而不是内容集合治理。
- 对外部资料建立 raw 事实层，避免只保存二手判断。
- 对所有长期入口建立机器索引，服务 AI 读取和自动审计。
- 将研究、资源、提示词、技能和脚本统一纳入质量门禁。
- 把本仓自身作为研究对象，定期用外部优秀仓库反向校准结构。

## 对本仓的影响

本仓应继续沿着“文档知识库 + Agent 控制面 + 研究事实层 + 资源治理层”的方向推进，但要防止膨胀。
正确的下一步不是无限新增目录，而是把已有对象的契约补齐：

- 研究域需要 L2/L3 成熟度推进和下沉机制。
- 外部资源需要结构化主表和生命周期字段。
- scripts 需要 manifest、风险等级和审计说明。
- skills 需要触发条件、输入输出、验证和归档策略。
- metadata 需要持续校验路径、标题、角色和引用入口。

## 风险和待验证项

- 自我研究容易产生自我确认，重要结论必须与外部仓库交叉审计。
- 当前工作区有大量未提交变更，研究结论应在提交前通过完整门禁。
- raw 快照与当前工作区存在时间差，不能把 raw 快照误认为当前全部状态。
- 本仓不应因为研究外部平台化项目而过早变成复杂应用仓库。

## 下一步 L3 验证任务

- 建立研究域成熟度看板：L0 raw、L1 analysis、L2 deep-dive、L3 下沉、L4 archive。
- 将 P1 研究对象的稳定结论迁入 `docs/references/` 或 `docs/workflow/`。
- 为 `scripts/` 增加 manifest 和风险等级治理。
- 为 `assets/external-resources/` 增加资源 schema、检查时间和生命周期状态。
- 对本仓自我结论执行一次跨模型或新会话审计，避免同一上下文自我确认。
