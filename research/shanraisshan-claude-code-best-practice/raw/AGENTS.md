# raw/ Agent 指南

本目录是 `shanraisshan/claude-code-best-practice` 的原始事实层。

## 维护规则

- 只保存从研究对象拉取的一手材料，不写分析判断。
- `repository/` 是本地 Git 工作树，刷新时由脚本 clone 或 fast-forward pull。
- 不手工改写 `*.raw.*` 文件内容；需要刷新时运行 `python3 scripts/fetch-research-raw.py`。
- `sources.yml` 必须记录拉取时间、来源命令和每个文件的状态。
- 外部 README 原文必须保存为 `.txt`，避免本仓库 Markdown 链接检查误判。
- 分析、判断、采用建议和沉淀路径写回上一级 `README.md`、`analysis.md` 或 `decisions.md`。
