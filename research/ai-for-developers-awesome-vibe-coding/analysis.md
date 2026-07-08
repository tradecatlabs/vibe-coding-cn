# ai-for-developers/awesome-vibe-coding 研究分析

## 本轮结论

`ai-for-developers/awesome-vibe-coding` 的核心价值不是深度判断，而是轻量资源雷达。它用一个
README 把 Web builder、IDE、移动工具、插件、本地应用和 CLI 工具粗分出来，适合帮助本仓发现
候选资源和补分类词表。

本仓不能直接复制它的条目，因为它缺少结构化字段、状态、许可证、最后检查时间和采用风险。正确用法是：
把它作为 `assets/external-resources/` 的候选输入源，经过二次筛选后再进入本地资源注册表。

## 本地证据

- 研究对象：`ai-for-developers/awesome-vibe-coding`
- 当前研究角色：精选 Vibe Coding 资料清单
- 原始仓库：`raw/repository/`
- 原始来源清单：`raw/sources.yml`
- 事实摘要：`domain.yml`

## 对标拆解

| 项 | 内容 |
|:---|:---|
| 参考对象 | `ai-for-developers/awesome-vibe-coding` |
| 它解决的核心问题 | 快速发现 Vibe Coding 工具生态中的候选对象 |
| 核心机制 | 单 README 分类索引，按工具形态组织入口 |
| 真正带来结果的动作 | 用低成本分类让读者知道生态里有哪些工具族 |
| 可迁移做法 | 补充本仓资源分类、发现候选工具、观察工具族变化 |
| 不可迁移条件 | 不直接复制条目，不把 awesome list 当推荐结论 |
| 下一步试用动作 | 抽取分类词，与 `assets/external-resources/categories.yml` 做对照 |

## 改良迭代

| 改良目标 | 原模式 | 本仓版本 | 验证指标 |
|:---|:---|:---|:---|
| 资源发现 | README 手工分类 | 候选资源进入本地注册表前先二次筛选 | 新资源有 category、source、status、last_checked |
| 分类补齐 | Web / IDE / CLI 等工具族 | 本仓资源 category 增加缺失工具族 | 分类能覆盖 Web builder、IDE agent、CLI、plugin、local app |
| 候选升级 | 条目停留在列表 | 高价值条目升级为独立研究域 | 进入 P1/P2 候选必须有采用理由和风险 |

## 可迁移清单

- 使用它补全 Vibe Coding 工具族分类。
- 将条目作为资源候选，不作为最终推荐。
- 对重复出现的工具族提取关键词，反馈到关键词系统。
- 对高频出现的 coding agent、IDE agent、CLI 工具建立 P1/P2 研究候选。

## 不可迁移清单

- 不复制整张 awesome list。
- 不把没有许可证、维护状态和风险说明的条目放进推荐区。
- 不把它当作学习路径或工程规范。

## 验证动作

| 动作 | 成功信号 | 失败信号 |
|:---|:---|:---|
| 抽取分类词并对照本仓资源分类 | 发现缺失分类并能补齐 | 分类无变化，只多一批链接 |
| 抽样 20 条资源做二次筛选 | 每条有采用/不采用理由 | 仍然只是链接搬运 |
| 挑出 3 个高价值工具进入候选研究 | 能说明为什么值得深挖 | 候选没有优先级和风险 |

## 沉淀判断

- 稳定结果进入 `assets/external-resources/` 和 `metadata/taxonomy.yml`。
- 本研究域保持 P3 低频雷达，不升级为方法论主线。
