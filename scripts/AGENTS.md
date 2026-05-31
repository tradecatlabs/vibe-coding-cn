# scripts/ Agent 指南

本目录维护仓库级自动化脚本，主要用于 Markdown、链接、锚点、metadata 和 AI 引用资产校验。

## 约束

- 脚本默认从仓库根目录运行，路径解析必须稳定。
- 新增检查脚本时，同步更新 `scripts/README.md`、`Makefile` 和根目录 `AGENTS.md` 的命令清单；只有 CI 环境稳定具备所需输入时才纳入 CI。
- `check-directory-docs.py` 对根 `.github/` 只要求 `AGENTS.md`，不要重新补 `.github/README.md`。
- 修改 docs README 或主题正文的主章节、锚点、索引后，优先运行 `python3 scripts/sync-doc-toc.py`，再运行 `make test`。
- 修改 GitHub Wiki 独立仓库后，运行 `make check-wiki WIKI_DIR=/path/to/wiki`；不要把 Wiki checkout 提交进主仓。
- 检查失败输出应包含文件路径、行号或可定位的错误信息。
- 跳过目录必须明确，至少跳过 `.git`、`.history`、`node_modules` 和外部源码快照。

## 验证

```bash
make test
```
