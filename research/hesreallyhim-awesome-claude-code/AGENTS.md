# hesreallyhim/awesome-claude-code 研究域 Agent 指南

本目录维护 `hesreallyhim/awesome-claude-code` 的独立研究域。

## 目录职责

```text
hesreallyhim-awesome-claude-code/
├── README.md  # 研究域入口和判断层
├── AGENTS.md  # 本目录维护规则
├── domain.yml # 事实摘要层：仓库元数据、研究角色、来源证据
├── analysis.md # L1 结构化研究结论、可借鉴点、风险和下一轮任务
├── deep-dive.md # L2 源码/结构深度研究、关键机制和可迁移模式
└── raw/       # 原始事实层：拉取到本地的一手材料快照
```

## 维护规则

- 本目录只研究 `hesreallyhim/awesome-claude-code`，不要混入其他仓库的横向比较正文。
- 动态事实必须写入 `domain.yml.github_observed`，并更新 `observed_at`。
- `raw/` 保存原始事实层，必须通过 `python3 scripts/fetch-research-raw.py` 刷新。
- 不手工改写 `raw/*.raw.*` 文件；稳定事实摘要再同步到 `domain.yml`。
- README 只写判断、定位、使用方式和后续观察点，不堆外部 README 全文。
- `analysis.md` 写 L1 结构化理解；`deep-dive.md` 写 L2 源码证据、关键机制和可迁移模式。
- 如果需要横向比较，在 `research/README.md` 或新的对比文档中处理，不把本目录重新变成聚合域。
- 修改后运行 `make sync-doc-toc` 和 `make test`。
