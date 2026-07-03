# hesreallyhim/awesome-claude-code 深度研究

## 研究级别

- 当前级别：L2 源码/结构深度研究。
- 研究对象：`hesreallyhim/awesome-claude-code`。
- 证据来源：本目录 `raw/` 下的 GitHub 元数据、README 快照和本地仓库工作树。
- 观察日期：2026-07-03。

## L2 结论

`hesreallyhim/awesome-claude-code` 不是普通 awesome list，而是一个数据驱动的 Claude Code 生态
资源登记系统。它用 CSV、脚本、测试、模板和资源目录把外部项目变成可维护清单，核心价值在于
把“资源推荐”治理成可检查、可更新、可归档的数据资产。

对本仓最重要的启发是：外部资源不应长期只保存在表格或 README 里，必须有本地事实层、字段契约、
状态字段、检查脚本和归档策略。

## 源码证据

- `raw/repository/THE_RESOURCES_TABLE.csv`：资源登记主表。
- 主表字段包含 `ID`、`Display Name`、`Category`、`Sub-Category`、`Primary Link`、
  `Secondary Link`、`Author Name`、`Author Link`、`Active`、`Date Added`、
  `Last Modified`、`Last Checked`、`License`、`Description`、`Removed From Origin`、
  `Stale`、`Repo Created`、`Latest Release`、`Release Version` 和 `Release Source`。
- `raw/repository/data/repo-ticker.csv`：仓库动态数据跟踪材料。
- `raw/repository/resources/`：资源详情或分类材料。
- `raw/repository/scripts/`：资源处理和维护脚本。
- `raw/repository/tests/`：清单质量检查。
- `raw/repository/templates/`：资源展示或生成模板。

## 关键机制

### CSV 是事实源

这个仓库的核心不是 README，而是资源主表。README 可以展示，脚本可以生成，测试可以校验，但资源
事实必须回到结构化表。这样才能进行去重、分类、状态检查、更新时间管理和归档。

### 资源有生命周期

`Active`、`Last Checked`、`Removed From Origin`、`Stale`、`Latest Release` 等字段说明：
资源不是“加进去就完事”，而是有活跃、陈旧、移除、更新和发布状态。

### 展示层和治理层分离

`templates/`、`scripts/` 和 `tests/` 共同说明，资源列表的展示可以自动生成，但治理字段必须稳定。
这比手写 awesome list 更适合长期维护。

## 可迁移模式

- 本仓外部资源应有本地结构化主表，不只依赖 Google Sheets 或 Markdown。
- 每个资源至少记录来源、分类、作者、许可证、最后检查时间、活跃状态和失效原因。
- 外部资源应支持 `active`、`stale`、`archived`、`removed` 等生命周期状态。
- 资源清单需要脚本校验：字段必填、URL 格式、重复 ID、分类合法性、过期检查。
- 展示文档可以由资源主表生成，避免手写索引漂移。

## 对本仓的影响

本仓已经开始把外部资源拉到 `assets/external-resources/`，并有 `scripts/check-external-resources.py`。
下一步应将资源治理推进为稳定契约：

- 明确主表字段和字段语义。
- 区分资源事实、展示文档和引用入口。
- 对资源状态、检查时间和失效处理建立硬门禁。
- 将云端表格视为输入源之一，而不是唯一事实源。

## 风险和待验证项

- 本轮没有执行该仓库自身脚本和测试，只做结构研究。
- awesome list 的分类体系具有主观性，本仓不应直接照搬分类。
- 本仓资源治理应服务中文 Vibe Coding 知识库，不应膨胀成泛 AI 资源大全。

## 下一步 L3 验证任务

- 对 `assets/external-resources/` 建立资源 schema 和字段必填校验。
- 增加资源生命周期字段：active、stale、archived、removed、last_checked。
- 设计从本地主表生成 README 或索引的流程。
- 把资源治理经验沉淀到 `docs/references/` 或 `assets/AGENTS.md`。
