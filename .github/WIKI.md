# GitHub Wiki 归属说明

`.github/wiki/` 不属于主仓库知识库结构，它是 GitHub Wiki 独立仓库的本地 checkout。

## 当前决策

- 主仓库不跟踪 `.github/wiki/`。
- `.github/wiki/` 保持在 `.gitignore` 中，避免把独立 wiki 仓库内容混入主仓库提交。
- 主仓库的权威知识库入口是 `docs/README.md`。
- 如果 Wiki 内容需要长期维护，应放入 `docs/` 后再纳入 `make test`、链接检查、metadata 和 AI citation 门禁。

## 操作规则

- 不要在主仓库提交 `.github/wiki/` 下的文件。
- 不要让 `docs/` 反向依赖 `.github/wiki/`。
- Wiki 若继续使用，按独立仓库自行提交和发布。
- Wiki 中沉淀出的稳定内容，应优先放入 `docs/` 的对应线性总文档。
