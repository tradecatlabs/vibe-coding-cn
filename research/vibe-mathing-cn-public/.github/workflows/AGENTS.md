# Workflow Agent Guide

`ci.yml` 是当前唯一 GitHub Actions 工作流，负责安装固定 Python 依赖并运行 `make check`。

## 依赖与职责

- 上游：仓库内 `requirements.txt`、`Makefile` 和 `scripts/check.sh`。
- 下游：GitHub push/PR checks。
- CI 只校验进入 Git 的可移植资产；被忽略的原始网页、上游缓存和电子书由本地 `make check-full` 校验。
- 禁止添加写权限、secrets、部署或网络抓取，除非任务明确要求并完成安全审查。
