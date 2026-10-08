# research/harness/ Agent 指南

## 目录职责

`research/harness/` 是 Harness 研究对象目录，维护 AI 生成系统中的工程控制、评估器、反馈闭环、上下文注入、架构约束和长期治理判断。

这里的文档回答：

- Harness 是什么。
- Harness 解决 AI 生成系统中的什么可靠性问题。
- 哪些机制属于 Harness，哪些只是普通工具调用或脚本封装。
- 哪些结论已经可采用，哪些仍处于观察或待验证状态。
- 可复用解释、准则和方法进入功法正文；可执行能力进入 skills。

## 文件地图

```text
harness/
├── README.md                # 对象入口：导航、定位和阅读顺序
├── raw/                     # raw 事实层：外部来源抓取、原始材料
│   ├── README.md
│   ├── AGENTS.md
│   └── lilian-weng-harness-engineering-for-self-improvement.md
├── notes/                   # 研究摘记：中文提纲、短摘和待提炼线索
│   ├── README.md
│   ├── AGENTS.md
│   ├── lilian-weng-harness-rsi-outline.md
│   └── lilian-weng-harness-rsi-short-note.md
└── AGENTS.md                # 本目录操作规则
```

## 对象边界

- 本目录只维护 Harness 作为研究对象的判断、证据、风险和采用建议。
- 不承载独立的可复用方法正文；Harness 解析、流程与工程模板统一归 `docs/gongfa/`。
- 当前 Harness 正文入口是 `docs/gongfa/harness-engineering.md`，本目录保留对象、来源、摘记和验证观察。
- 不承载可执行能力；可复用能力迁移到 `skills/`。
- 不把单个工具、单篇文章或单次实验直接包装成稳定结论。

## 证据要求

- 外部事实优先引用官方文档、原始仓库、论文或可信一手来源。
- AI 摘要不能作为事实源，只能作为待核验线索。
- 新增结论必须区分：事实、解释、采用判断、风险和待验证项。
- 涉及最新模型、工具、仓库状态或产品能力时，必须核验当前来源。

## 修改规则

- 具体 Harness 研究观察放本目录；可复用哲学、解释或方法正文归功法，不在本目录另行维护副本。
- 新增、删除、移动或重命名本目录文档时，必须同步更新本目录 `README.md`、上级 `research/README.md`、根 `README.md`、必要的 `docs/README.md` 跨入口、`metadata/taxonomy.yml` 和必要的 `metadata/redirects.yml`。
- 面向 AI 引用的重要入口变化，必须同步更新 `llms.txt` 和 `assets/ai-citation/llms-full.txt`。
- 修改后运行 `make sync-doc-toc` 和 `make test`。
