# hesreallyhim/awesome-claude-code 研究分析

## 本轮结论

`hesreallyhim/awesome-claude-code` 的核心价值不是链接多，而是把 Claude Code 生态资源做成可治理数据资产。
它有 CSV 主表、动态数据、资源目录、脚本、测试和模板，已经从普通 awesome list 进化成资源登记系统。

本仓最应该迁移的是资源治理模型：外部资源必须有主表、字段契约、状态、最后检查时间、许可证、失效标记、
生成/校验脚本和归档策略。

## 本地证据

- 研究对象：`hesreallyhim/awesome-claude-code`
- 当前研究角色：Claude Code 生态索引
- 原始仓库：`raw/repository/`
- 原始来源清单：`raw/sources.yml`
- 事实摘要：`domain.yml`
- 深度证据：`deep-dive.md`

## 对标拆解

| 项 | 内容 |
|:---|:---|
| 参考对象 | `hesreallyhim/awesome-claude-code` |
| 它解决的核心问题 | 让快速增长的 Claude Code 资源从链接堆变成可维护数据资产 |
| 核心机制 | `THE_RESOURCES_TABLE.csv`、`data/`、`resources/`、`scripts/`、`tests/`、`templates/` |
| 真正带来结果的动作 | 用结构化字段和校验脚本治理资源生命周期 |
| 可迁移做法 | 资源 schema、active/stale/removed 状态、last_checked、license、release 字段 |
| 不可迁移条件 | 不复制 Claude Code 生态分类，不让本仓变成泛 AI 资源大全 |
| 下一步试用动作 | 为 `assets/external-resources/` 建字段契约和过期检查规则 |

## 改良迭代

| 改良目标 | 原模式 | 本仓版本 | 验证指标 |
|:---|:---|:---|:---|
| 资源事实源 | CSV 主表 | 本地资源注册表 + schema | 每个资源有 id、category、source、status、last_checked |
| 生命周期治理 | active / stale / removed | active、stale、archived、removed | 过期资源能被脚本发现 |
| 展示与治理分离 | templates 生成展示 | README 作为展示，数据文件作为事实源 | README 不再手写漂移 |

## 可迁移清单

- 明确外部资源字段：ID、名称、分类、链接、作者、许可证、状态、最后检查时间、失效原因。
- 增加资源生命周期状态，不再只有“存在/不存在”。
- 把资源展示和资源事实源分离。
- 用脚本检查重复 ID、缺字段、过期检查和非法分类。

## 不可迁移清单

- 不复制 Claude Code 生态的具体分类体系。
- 不把所有资源都升级成研究域；只有高价值资源才进入 research。
- 不在 README 中手写所有资源事实。

## 验证动作

| 动作 | 成功信号 | 失败信号 |
|:---|:---|:---|
| 抽样 30 条本地资源做 schema 校验 | 能发现缺字段和过期资源 | 仍靠人工肉眼检查 |
| 为资源增加生命周期状态 | stale/removed 能被识别 | 失效资源仍在 active 列表 |
| 生成或校验展示索引 | 展示和事实源一致 | README 与数据源不一致 |

## 沉淀判断

- 稳定结论应进入 `assets/external-resources/`、`assets/AGENTS.md` 和资源校验脚本。
- 这是 P1 资源治理对标对象，不只是 Claude Code 生态目录。
