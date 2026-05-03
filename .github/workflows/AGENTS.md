# .github/workflows/ Agent 指南

本目录只放 GitHub Actions 工作流。

## 约束

- 不新增无法在本地解释的黑盒步骤。
- 不在 workflow 中写入密钥明文。
- 修改 CI 后必须运行 `make test`，并在推送后查看 GitHub Actions 结果。
- 外链检查配置优先修改仓库根目录 `.lychee.toml`，不要在 workflow 里堆长排除列表。
