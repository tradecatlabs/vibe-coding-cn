# research/harness/raw/ Agent 指南

## 目录职责

`research/harness/raw/` 保存 Harness 研究对象的一手材料、原文快照和可追溯事实来源。

## 文件地图

```text
raw/
├── README.md  # raw 事实层入口
├── lilian-weng-harness-engineering-for-self-improvement.md  # Lilian Weng 原文抓取
└── AGENTS.md  # 本目录操作规则
```

## 修改规则

- raw 文档只保存来源事实，不写二次分析、采用建议或稳定结论。
- 新增 raw 材料时，保留来源标题、URL、抓取时间或可追溯说明。
- 不为了满足本仓 Markdown 风格重写外部原文内容；必要修正只限路径、标题和来源说明。
- 分析判断写入上级 `../harness-engineering.md` 或 notes，不写在 raw 文件中。
