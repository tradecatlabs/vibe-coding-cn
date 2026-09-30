# Concepts 目录 Agent 指南

## 目录职责

`docs/concepts/` 存放项目的核心概念与工程认知框架。

这里的文档回答：

- Vibe Coding 的基本概念是什么。
- 新手如何定义问题、拆解问题和构建系统。
- 工程方法如何从经验沉淀为可复用模型。

## 文件地图

```text
concepts/
├── README.md  # 索引入口：核心概念导航
├── problem-solving.md
├── vibe-coding-cultivation-model.md  # 修仙单树本体的通俗解释与任务战力评价
├── cultivation-ontology-taxonomy.md  # V4 BFO 主干、领域稳定 ID/定义、关系与证据
├── glue-coding.md
├── system-building.md
├── development-paradigms.md
├── language-layers.md
├── keyword-system.md
├── recursive-self-optimizing-system.md
└── AGENTS.md  # 本目录操作规则
```

## 修改规则

- 继承 `docs/AGENTS.md` 的 README 结构契约：H1 后直接进入 `## 字多不看`，再按 `快速导航 -> 完整细粒度目录 -> 使用方式 -> 正文` 排列。
- 新增概念内容时，优先写入对应独立主题文档，并同步更新 `README.md` 索引。
- 新增同级主题 `.md` 文件前，必须确认它是稳定概念，并同步更新全仓链接、`metadata/taxonomy.yml` 和必要的 `redirects.yml`。
- 概念文档应优先使用稳定术语，避免同一概念多种叫法并存。
- 修仙领域以 `cultivation-ontology-taxonomy.md` 为唯一分类与语义契约入口；解释图层只引用，不维护并行的现实/知识分类树。
- V4 以用户指定的 BFO 2020 为固定前提，只在下层展开；保留原生 ID、定义与继承，不因适配困难擅自更换顶层。
- 区分类、实例与类外延：万魂幡引用会话类外延，不改成文档或物质聚合体；模型版本归属不等于 BFO 直接能力承载。未做公理验证不得宣称已完成。
- 领域类须在同一正文登记稳定 ID、工作定义、边界和依据，主父只由主树维护；改名不换 ID，拆并留去向，不用用途交叉类或复制身份掩盖分类冲突。
- 小说研究以《逆天邪神》最高权重，按已读范围保留原词和来源；不冻结心法/功法/阵法等跨书互斥叶类，不改变会话、集合、资源、权限和验收语义。
- 不把一次性操作步骤放入本目录；操作型内容应放入 `docs/getting-started/` 或 `docs/references/`。
- 不在 README 正文中写 `和其他目录的边界` 或 `维护规则`；维护者规则只写本文件。

## 质量要求

- 每个概念先说明它解决的问题。
- 尽量给出使用场景、判断标准和简单例子。
- 不确定的外部事实必须标注 TODO，或放入 `research/` 等待验证。
- 修改后必须运行 `make sync-doc-toc` 和 `make test`。
